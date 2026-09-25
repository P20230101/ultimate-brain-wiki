import unittest
from pathlib import Path

from tools.pa12_vfm_check import build_current_check, roi_bounds_px, roi_size_mm, summarize_check


class Pa12VfmCheckTests(unittest.TestCase):
    def test_current_batch_report_uses_separate_matchid_state_snapshot(self):
        audit = build_current_check(Path("configs/pa12_rotated_batch.json"))

        self.assertEqual(audit["experiment_count"], 4)
        by_id = {row["实验编号"]: row for row in audit["experiments"]}
        self.assertEqual(by_id["S16_XY_0.2"]["Y"], "中间候选 61.94 MPa（第 28 轮；非最终）")
        self.assertEqual(by_id["S16_XY_0.2"]["H"], "中间候选 139.60 MPa（第 28 轮；非最终）")
        self.assertIn("进度未显示", by_id["S16_XY_0.2"]["结论"])
        self.assertIn("VFM力序列未闭合", by_id["S16_XY_0.2"]["时间同步"])
        self.assertIn("VFM力序列未核对", by_id["S17_XY_20"]["时间同步"])
        self.assertIn("x=402–714", by_id["S16_XY_0.2"]["结论"])
        self.assertIn("末有效同步帧力：000284.jpg", by_id["S15_XY_0.2"]["结论"])

    def test_roi_size_comes_from_shape_polygon_and_calibration(self):
        shape = "2;0;False;4;402;410;714;410;714;730;402;730;555;554"

        self.assertEqual(roi_size_mm(shape, 0.087209), "27.21 × 27.91 mm")

    def test_roi_position_reports_shape_bounds_and_center(self):
        shape = "2;0;False;4;402;410;714;410;714;730;402;730;555;554"

        self.assertEqual(roi_bounds_px(shape), "x=402–714, y=410–730 px；中心=(558.0, 570.0) px")

    def test_check_marks_parameters_and_virtual_work_uncomputed(self):
        row = summarize_check(
            experiment_id="S16_XY_0.2",
            loading_speed=0.2,
            photo_names=["000001.jpg", "000002.jpg"],
            times=[0.0, 0.1],
            table_x=[0.0, 10.0],
            table_y=[0.0, 11.0],
            x_forces=[0.0, 10.0],
            y_forces=[0.0, 11.0],
            roi_size="27.21 × 27.91 mm",
            roi_thickness_mm=1.0,
            fracture_photo="000002.jpg",
            reference_image="000000.jpg",
            identification_snapshot={
                "iteration": 16,
                "yield_mpa": 63.93,
                "hardening_mpa": 41.55,
                "progress_percent": 70,
                "residual_label": "剩余的",
                "residual_display_value": 1214,
                "internal_virtual_work": "界面曲线可见；数值未导出",
                "external_virtual_work": "界面曲线可见；数值未导出",
                "parameter_boundary_status": "未核实",
            },
            vfm_force_status="旧 Forces 与同步表不匹配；当前保存文件 Forces 帧数为 0",
            vfm_input_status="VFM 同步序列不一致",
            roi_position="x=402–714, y=410–730 px；中心=(558.0, 570.0) px",
        )

        self.assertEqual(row["数量一致"], "是（2/2/2）")
        self.assertEqual(row["时间同步"], "预处理通过；VFM力序列未闭合")
        self.assertEqual(row["起始力"], "X 0.000000 / Y 0.000000 N")
        self.assertEqual(row["ν"], "固定 0.375")
        self.assertEqual(row["E"], "阶段1结果未见")
        self.assertIn("63.93", row["Y"])
        self.assertIn("41.55", row["H"])
        self.assertIn("中间候选", row["结论"])
        self.assertEqual(row["内部虚功"], "界面曲线可见；数值未导出")
        self.assertEqual(row["外部虚功"], "界面曲线可见；数值未导出")
        self.assertIn("MatchID Job 参考图 000000.jpg", row["结论"])
        self.assertIn("ROI位置：x=402–714", row["结论"])
        self.assertIn("1214", row["残差"])
        self.assertIn("末有效同步帧力：000002.jpg", row["结论"])

    def test_check_blocks_nonmonotonic_time_and_force_mismatch(self):
        row = summarize_check(
            experiment_id="S1_XY_0.2",
            loading_speed=0.2,
            photo_names=["000001.jpg", "000002.jpg"],
            times=[0.1, 0.05],
            table_x=[0.0, 10.0],
            table_y=[0.0, 11.0],
            x_forces=[0.0, 9.0],
            y_forces=[0.0, 11.0],
            roi_size="27.00 × 27.00 mm",
            roi_thickness_mm=1.0,
            fracture_photo="000002.jpg",
            reference_image="000000.jpg",
            identification_snapshot=None,
            vfm_force_status=None,
        )

        self.assertEqual(row["数量一致"], "是（2/2/2）")
        self.assertIn("时间非单调", row["时间同步"])
        self.assertIn("X CSV 与照片—力表不一致", row["时间同步"])
        self.assertIn("阻断", row["结论"])


if __name__ == "__main__":
    unittest.main()
