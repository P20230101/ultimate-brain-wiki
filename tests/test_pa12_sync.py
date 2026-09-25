import json
import gzip
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd

from tools.pa12_sync import (
    VFMOutputBlocked,
    average_press_channels,
    detect_force_events,
    frame_sequence_gaps,
    interpolate_force_values,
    shared_photo_time_axis,
    photo_time_from_frame_numbers,
    summarize_frame_numbers,
    discover_frames,
    select_frames_from_capture_offsets,
    select_frame_numbers,
    validate_nonnegative_vfm_forces,
    validate_active_vfm_forces,
    validate_vfm_lengths,
    process_experiment,
    _device_displacement,
    _plot_check,
)
from tools.run_pa12_batch import _manifest_row, _write_batch_report, run_batch
from tools.audit_pa12_outputs import _write_report, audit_outputs, audit_vfm_triplet
from tools.pa12_mechanics import analyze_curve, relative_displacement
from tools.matchid_prepare import extract_matchid_dat_metadata, parse_job_metadata


class Pa12SyncTests(unittest.TestCase):
    def test_shared_photo_time_axis_rejects_different_axes(self):
        self.assertTrue(
            shared_photo_time_axis(
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
            )
        )
        self.assertFalse(
            shared_photo_time_axis(
                np.array([0.0, 1.0]),
                np.array([0.0, 1.1]),
            )
        )

    def test_batch_manifest_preserves_end_event_label(self):
        row = _manifest_row(
            {"experiment_id": "S23_Y_2", "notes": ""},
            status="DATA_LIMITED",
            result={
                "end_event_label": "力文件记录终点（未记录掉载）",
                "force_analysis_end_index": 15327,
            },
        )

        self.assertEqual(row["end_event_label"], "力文件记录终点（未记录掉载）")
        self.assertEqual(row["force_analysis_end_index"], 15327)

    def test_unconfirmed_endpoint_is_not_reported_as_fracture_photo(self):
        report_path = Path("Agents/PA12实验数据处理/处理记录/S23_Y_2_处理报告.md")
        report = report_path.read_text(encoding="utf-8")

        self.assertIn("断裂前最后有力照片", report)
        self.assertIn("视觉断裂时刻的力值：缺失", report)
        self.assertNotIn("- 断裂照片：", report)

    def test_check_plot_uses_end_event_label(self):
        axis = MagicMock()
        figure = MagicMock()
        with patch("tools.pa12_sync.plt.subplots", return_value=(figure, axis)):
            _plot_check(
                Path("check.png"),
                "S23_Y_2",
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                0.0,
                0.5,
                1.0,
                "力文件记录终点（未记录掉载）",
            )

        labels = [call.kwargs["label"] for call in axis.axvline.call_args_list]
        self.assertIn("力文件记录终点（未记录掉载）", labels)

    def test_check_plot_marks_visual_fracture_after_force_record_end(self):
        axis = MagicMock()
        figure = MagicMock()
        with patch("tools.pa12_sync.plt.subplots", return_value=(figure, axis)):
            _plot_check(
                Path("check.png"),
                "S23_Y_2",
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                np.array([0.0, 1.0]),
                0.0,
                0.5,
                1.0,
                "力文件记录终点（视觉断裂力缺失）",
                visual_fracture_time=1.2,
            )

        visual_marker = next(
            call for call in axis.axvline.call_args_list
            if call.kwargs.get("label") == "估算视觉断裂时刻（力值缺失）"
        )
        self.assertEqual(visual_marker.args[0], 1.2)

    def test_rotated_batch_config_uses_existing_paper_pairs(self):
        config = json.loads(Path("configs/pa12_rotated_batch.json").read_text(encoding="utf-8"))
        self.assertEqual(len(config["experiments"]), 10)
        self.assertEqual(config["defaults"]["geometry"]["thickness_mm"], 1.0)
        self.assertEqual(config["defaults"]["geometry"]["overall_thickness_mm"], 3.0)
        for entry in config["experiments"]:
            image_folder = Path(entry["image_folder"])
            force_file = Path(entry["force_file"])
            self.assertIn("vertical_all_45°\\PAPER", str(image_folder))
            self.assertNotIn("\\CHECK", str(image_folder))
            self.assertTrue(image_folder.is_dir())
            self.assertTrue(force_file.is_file())
            self.assertGreater(len(discover_frames(image_folder).paired), 0)

    def test_detects_negative_load_and_drop(self):
        time = np.arange(0.0, 10.0, 0.01)
        signal = np.full_like(time, 10.0)
        loading = (time >= 1.0) & (time < 6.0)
        signal[loading] = 10.0 - (time[loading] - 1.0) * 100.0
        signal[time >= 6.0] = -500.0
        signal[time >= 6.5] = 10.0
        x = signal
        y = signal + 2.0

        events = detect_force_events(
            time,
            x,
            y,
            baseline_window_s=0.5,
            start_threshold_n=10.0,
            persistence_s=0.1,
            fracture_fraction=0.2,
            smoothing_window_s=0.05,
        )

        self.assertAlmostEqual(events.baseline_x, 10.0, places=6)
        self.assertAlmostEqual(events.baseline_y, 12.0, places=6)
        self.assertAlmostEqual(time[events.start_index], 1.1, delta=0.08)
        self.assertAlmostEqual(time[events.peak_index], 6.0, delta=0.08)
        self.assertAlmostEqual(time[events.fracture_index], 6.5, delta=0.08)
        self.assertEqual(events.load_polarity, -1.0)

    def test_manual_force_endpoints_allow_missing_automatic_drop(self):
        time = np.arange(0.0, 5.0, 0.01)
        signal = np.zeros_like(time)
        signal[time >= 1.0] = -(time[time >= 1.0] - 1.0) * 100.0

        events = detect_force_events(
            time,
            signal,
            signal,
            baseline_window_s=0.5,
            start_threshold_n=5.0,
            persistence_s=0.1,
            fracture_fraction=0.2,
            smoothing_window_s=0.05,
            manual_start_index=100,
            manual_fracture_index=400,
        )

        self.assertEqual(events.start_index, 100)
        self.assertEqual(events.fracture_index, 400)
        self.assertEqual(events.peak_index, 400)

    def test_default_same_direction_channels_are_averaged(self):
        frame = pd.DataFrame(
            {
                "X1_Press": [1.0, 3.0],
                "X2_Press": [3.0, 5.0],
                "Y1_Press": [2.0, 4.0],
                "Y2_Press": [4.0, 6.0],
            }
        )
        x, y = average_press_channels(
            frame,
            ["X1_Press", "X2_Press"],
            ["Y1_Press", "Y2_Press"],
        )
        np.testing.assert_allclose(x, [2.0, 4.0])
        np.testing.assert_allclose(y, [3.0, 5.0])

    def test_interpolation_uses_one_photo_time_axis_and_zeroes_first_row(self):
        force_time = np.array([0.0, 1.0, 2.0])
        x = np.array([10.0, 20.0, 30.0])
        y = np.array([100.0, 200.0, 300.0])
        photo_time = np.array([0.5, 1.5])
        result = interpolate_force_values(
            force_time,
            x,
            y,
            photo_time,
            baseline_x=10.0,
            baseline_y=100.0,
            force_sign=1.0,
        )
        np.testing.assert_allclose(result.x, [0.0, 15.0])
        np.testing.assert_allclose(result.y, [0.0, 150.0])
        np.testing.assert_array_equal(result.photo_time, photo_time)

    def test_default_interpolation_returns_positive_tensile_force(self):
        force_time = np.array([0.0, 1.0, 2.0])
        x = np.array([10.0, 5.0, 0.0])
        y = np.array([20.0, 15.0, 10.0])
        photo_time = np.array([0.0, 1.0, 2.0])
        result = interpolate_force_values(
            force_time,
            x,
            y,
            photo_time,
            baseline_x=10.0,
            baseline_y=20.0,
        )
        np.testing.assert_allclose(result.x, [0.0, 5.0, 10.0])
        np.testing.assert_allclose(result.y, [0.0, 5.0, 10.0])
        validate_nonnegative_vfm_forces(result.x, result.y)

    def test_negative_vfm_force_values_are_rejected(self):
        with self.assertRaises(VFMOutputBlocked):
            validate_nonnegative_vfm_forces(
                np.array([0.0, 1.0]),
                np.array([0.0, -0.01]),
            )

    def test_zero_after_first_vfm_row_is_rejected(self):
        with self.assertRaises(VFMOutputBlocked):
            validate_nonnegative_vfm_forces(
                np.array([0.0, 1.0, 0.0]),
                np.array([0.0, 1.0, 2.0]),
            )

    def test_nonloading_direction_zero_is_allowed_but_active_direction_must_be_positive(self):
        validate_active_vfm_forces(
            np.array([0.0, 1.0]),
            np.array([0.0, 0.0]),
            ["X"],
        )
        with self.assertRaises(VFMOutputBlocked):
            validate_active_vfm_forces(
                np.array([0.0, -1.0]),
                np.array([0.0, 0.0]),
                ["X"],
            )

    def test_selects_start_and_end_frames_from_setting_frequency(self):
        frames = list(range(259))
        selected = select_frame_numbers(
            frames,
            load_start_time=0.1,
            fracture_time=25.8,
            camera_setting_fps=10.0,
        )
        self.assertEqual(selected[0], 1)
        self.assertEqual(selected[-1], 258)
        self.assertEqual(len(selected), 258)

    def test_selects_only_existing_sparse_paired_frames(self):
        selected = select_frame_numbers(
            [0, 8, 16, 24],
            load_start_time=0.0,
            fracture_time=1.6,
            camera_setting_fps=10.0,
        )
        self.assertEqual(selected, [0, 8, 16])

    def test_sparse_frame_times_preserve_frame_number_gaps(self):
        photo_time = photo_time_from_frame_numbers(
            [0, 8, 16],
            start_time=1.0,
            fracture_time=2.6,
            camera_setting_fps=10.0,
        )
        np.testing.assert_allclose(photo_time, [1.0, 1.8, 2.6])

    def test_summarizes_sparse_frame_numbers_for_reports(self):
        self.assertEqual(
            summarize_frame_numbers([1, 2, 3, 8, 9, 16]),
            "1-3, 8-9, 16",
        )

    def test_vfm_length_mismatch_is_blocked(self):
        with self.assertRaises(VFMOutputBlocked):
            validate_vfm_lengths(258, 257, 258)

        validate_vfm_lengths(258, 258, 258)

    def test_reports_frame_number_gaps(self):
        self.assertEqual(frame_sequence_gaps([0, 1, 2, 4, 7]), [3, 5, 6])

    def test_uses_capture_time_shape_when_exif_is_available(self):
        numbers, photo_time = select_frames_from_capture_offsets(
            [0, 1, 2, 3, 4],
            np.array([0.0, 0.10, 0.25, 0.50, 0.60]),
            load_start_time=0.1,
            fracture_time=0.52,
        )
        self.assertEqual(numbers, [1, 2, 3])
        self.assertAlmostEqual(photo_time[0], 0.1)
        self.assertAlmostEqual(photo_time[-1], 0.52)
        self.assertGreater(photo_time[2] - photo_time[1], photo_time[1] - photo_time[0])

    def test_batch_passes_output_root_to_single_experiment(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory) / "vault"
            config_path = Path(temporary_directory) / "batch.json"
            config_path.write_text(
                json.dumps(
                    {
                        "output_root": str(output_root),
                        "defaults": {"press_sheet": "Press"},
                        "experiments": [{"experiment_id": "demo"}],
                    }
                ),
                encoding="utf-8",
            )

            def fake_process_experiment(config):
                self.assertEqual(config["output_root"], str(output_root))
                return {
                    "vfm_allowed": False,
                    "overview_row": None,
                }

            with patch("tools.run_pa12_batch.process_experiment", fake_process_experiment):
                result = run_batch(config_path)

            self.assertEqual(result["rows"][0]["status"], "DIAGNOSTIC_ONLY")

    def test_batch_overview_keeps_unknown_row_for_unresolved_experiment(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory) / "vault"
            config_path = Path(temporary_directory) / "batch.json"
            config_path.write_text(
                json.dumps(
                    {
                        "output_root": str(output_root),
                        "experiments": [
                            {
                                "experiment_id": "S24_Y_20",
                                "status": "UNRESOLVED",
                                "loading_speed": 20.0,
                                "camera_setting_fps": 500.0,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = run_batch(config_path)
            with Path(result["overview_csv"]).open(encoding="utf-8-sig") as handle:
                overview = list(csv.DictReader(handle))

            self.assertEqual(len(overview), 1)
            self.assertEqual(overview[0]["速度"], "20 mm/s")
            self.assertEqual(overview[0]["设置频率"], "500 Hz")
            self.assertEqual(overview[0]["照片数量"], "UNKNOWN")
            self.assertEqual(overview[0]["力数据时间"], "UNKNOWN")

    def test_batch_classifies_preload_release_without_formal_outputs(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            output_root = temporary_root / "vault"
            config_path = temporary_root / "batch.json"
            config_path.write_text(
                json.dumps(
                    {
                        "output_root": str(output_root),
                        "experiments": [
                            {
                                "experiment_id": "S24_Y_20",
                                "status": "PRELOAD_RELEASE_ONLY",
                                "loading_speed": 20.0,
                                "camera_setting_fps": 500.0,
                                "notes": "文件从预载开始，只能作为预载释放记录。",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = run_batch(config_path)

            self.assertEqual(result["rows"][0]["status"], "PRELOAD_RELEASE_ONLY")
            with Path(result["overview_csv"]).open(encoding="utf-8-sig") as handle:
                overview = list(csv.DictReader(handle))
            self.assertEqual(len(overview), 1)
            self.assertEqual(overview[0]["照片数量"], "UNKNOWN")
            self.assertEqual(overview[0]["力数据时间"], "UNKNOWN")

    def test_audit_vfm_triplet_reports_mismatched_rows(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            match_path = root / "match.csv"
            x_path = root / "x.csv"
            y_path = root / "y.csv"
            match_path.write_text(
                "照片,时间/s,X向力/N,Y向力/N\n000000.jpg,0,0,0\n000001.jpg,1,1,1\n",
                encoding="utf-8-sig",
            )
            x_path.write_text("0.000000\n1.000000\n", encoding="utf-8")
            y_path.write_text("0.000000\n", encoding="utf-8")

            audit = audit_vfm_triplet(
                match_path,
                x_path,
                y_path,
                active_axes=["X", "Y"],
            )

            self.assertFalse(audit["sync_triplet_ready"])
            self.assertIn("数量不一致", "；".join(audit["failures"]))

    def test_output_audit_distinguishes_clean_audit_from_all_experiments_formal_ready(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            agent_root = root / "Agents" / "PA12实验数据处理"
            record_root = agent_root / "处理记录"
            (agent_root / "实验概览").mkdir(parents=True)
            (agent_root / "照片力匹配").mkdir(parents=True)
            (agent_root / "VFM专用力值" / "X方向").mkdir(parents=True)
            (agent_root / "VFM专用力值" / "Y方向").mkdir(parents=True)
            (agent_root / "MatchID_VFM准备").mkdir(parents=True)
            record_root.mkdir(parents=True)
            config_path = root / "config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "output_root": str(root),
                        "experiments": [
                            {
                                "experiment_id": "S1",
                                "stress_strain_axes": ["X"],
                                "speed_label": "1",
                            },
                            {"experiment_id": "S2", "stress_strain_axes": ["Y"]},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (record_root / "PA12批量处理清单.json").write_text(
                json.dumps(
                    [
                        {"experiment_id": "S1", "status": "VFM_READY", "vfm_allowed": True, "photo_count": 2},
                        {"experiment_id": "S2", "status": "DATA_LIMITED", "vfm_allowed": False, "photo_count": 2},
                    ]
                ),
                encoding="utf-8",
            )
            (agent_root / "实验概览" / "PA12实验概览_汇总.csv").write_text(
                "速度,照片数量\n1 mm/s,2\n2 mm/s,2\n", encoding="utf-8-sig"
            )
            (agent_root / "MatchID_VFM准备" / "PA12_MatchID_VFM实验级索引.csv").write_text(
                "实验编号\nS1\nS2\n", encoding="utf-8-sig"
            )
            (agent_root / "照片力匹配" / "S1_照片-力对应表.csv").write_text(
                "照片,时间/s,X向力/N,Y向力/N\n000000.jpg,0,0,0\n000001.jpg,1,1,0\n",
                encoding="utf-8-sig",
            )
            (agent_root / "照片力匹配" / "S2_照片-力对应表.csv").write_text(
                "照片,时间/s,X向力/N,Y向力/N\n000000.jpg,0,0,0\n000001.jpg,1,0,1\n",
                encoding="utf-8-sig",
            )
            (agent_root / "VFM专用力值" / "X方向" / "X-1-2.csv").write_text(
                "0\n1\n", encoding="utf-8"
            )
            (agent_root / "VFM专用力值" / "Y方向" / "Y-1-2.csv").write_text(
                "0\n1\n", encoding="utf-8"
            )

            audit = audit_outputs(config_path)

            self.assertTrue(audit["audit_passed"], audit["failures"])
            self.assertTrue(audit["experiments"][0]["vfm"]["sync_triplet_ready"])
            self.assertNotIn("formal_vfm_ready", audit["experiments"][0]["vfm"])
            self.assertFalse(audit["all_sync_triplets_ready"])

    def test_output_audit_report_calls_triplets_sync_inputs_not_formal_vfm(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            report_path = Path(temporary_directory) / "audit.md"
            _write_report(
                report_path,
                {
                    "experiment_count": 1,
                    "overview_count": 1,
                    "matchid_index_count": 1,
                    "audit_passed": True,
                    "all_sync_triplets_ready": True,
                    "formal_vfm_ready": False,
                    "experiments": [
                        {
                            "experiment_id": "S1",
                            "status": "VFM_READY",
                            "failures": [],
                            "sync_triplet_ready": True,
                            "vfm": {"match_count": 2, "x_count": 2, "y_count": 2, "sync_triplet_ready": True},
                        }
                    ],
                },
            )

            report = report_path.read_text(encoding="utf-8")

            self.assertIn("同步输入三文件审计对象", report)
            self.assertIn("同步输入数量契约在全部配置实验中就绪", report)
            self.assertIn("本报告只审计同步输入契约", report)
            self.assertIn("正式材料参数/VFM 发布就绪", report)
            self.assertNotIn("正式 VFM 三文件审计对象", report)

    def test_audit_report_records_locally_validated_matchid_mapping(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            report_path = Path(temporary_directory) / "audit.md"
            _write_report(
                report_path,
                {
                    "experiment_count": 0,
                    "overview_count": 0,
                    "matchid_index_count": 0,
                    "audit_passed": True,
                    "all_sync_triplets_ready": False,
                    "formal_vfm_ready": False,
                    "experiments": [],
                },
            )

            report = report_path.read_text(encoding="utf-8")

            self.assertIn("当前版本本地交叉验证", report)
            self.assertNotIn("导出一帧标准 DIC CSV，确认", report)

    def test_batch_report_records_locally_validated_matchid_mapping(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            report_path = Path(temporary_directory) / "batch.md"
            _write_batch_report(report_path, [], Path(temporary_directory))

            report = report_path.read_text(encoding="utf-8")

            self.assertIn("当前版本本地交叉验证", report)
            self.assertNotIn("导出一帧标准 DIC CSV，确认", report)
            self.assertIn("外围机器力按用户确认直接作为中心 ROI 边界合力输入", report)
            self.assertIn("所有双轴均为等双轴", report)
            self.assertNotIn("不要把当前正力 CSV 直接当成边界载荷场", report)

    def test_zero_nonloading_direction_does_not_block_formal_vfm(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            image_folder = root / "images"
            image_folder.mkdir()
            from PIL import Image

            for number in range(3):
                image_path = image_folder / f"{number:06d}.jpg"
                Image.new("RGB", (2, 2), color="white").save(image_path)
                (image_folder / f"{number:06d}.jpg.dat").write_bytes(b"dat")

            time = np.arange(0.0, 5.0, 0.1)
            x = np.zeros_like(time)
            x[10:31] = -np.linspace(0.0, 100.0, 21)
            x[31:] = -1.0
            press = pd.DataFrame(
                {
                    "T": time,
                    "X1_Press": x,
                    "X2_Press": x,
                    "Y1_Press": np.zeros_like(time),
                    "Y2_Press": np.zeros_like(time),
                }
            )
            position = pd.DataFrame(
                {
                    "T": time,
                    "X1_Pos": time,
                    "X2_Pos": time,
                    "Y1_Pos": np.zeros_like(time),
                    "Y2_Pos": np.zeros_like(time),
                }
            )
            force_file = root / "force.xlsx"
            with pd.ExcelWriter(force_file, engine="openpyxl") as writer:
                position.to_excel(writer, sheet_name="Pos", index=False)
                press.to_excel(writer, sheet_name="Press", index=False)

            result = process_experiment(
                {
                    "experiment_id": "single_axis_zero_transverse",
                    "image_folder": str(image_folder),
                    "force_file": str(force_file),
                    "output_root": str(root / "output"),
                    "camera_setting_fps": 1.0,
                    "loading_speed": 1.0,
                    "formal_vfm_allowed": True,
                    "displacement_mode": "device",
                    "position_columns": ["X1_Pos", "X2_Pos"],
                    "manual": {
                        "force_start_index": 10,
                        "force_fracture_index": 40,
                        "start_frame": 0,
                        "end_frame": 2,
                    },
                }
            )

            self.assertTrue(result["vfm_allowed"])
            self.assertTrue(Path(result["stress_strain"]).is_file())
            y_vfm = np.loadtxt(root / "output" / "Agents" / "PA12实验数据处理" / "VFM专用力值" / "Y方向" / "Y-1.0-3.csv")
            np.testing.assert_allclose(y_vfm, 0.0)

    def test_explicit_dic_invalid_frames_are_excluded_from_all_photo_outputs(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            image_folder = root / "images"
            image_folder.mkdir()
            from PIL import Image

            for number in range(5):
                image_path = image_folder / f"{number:06d}.jpg"
                Image.new("RGB", (2, 2), color="white").save(image_path)
                (image_folder / f"{number:06d}.jpg.dat").write_bytes(b"dat")

            time = np.arange(0.0, 5.0, 0.1)
            force = np.zeros_like(time)
            force[5:41] = -np.linspace(0.0, 100.0, 36)
            force[41:] = -1.0
            press = pd.DataFrame(
                {
                    "T": time,
                    "X1_Press": force,
                    "X2_Press": force,
                    "Y1_Press": force,
                    "Y2_Press": force,
                }
            )
            position = pd.DataFrame(
                {
                    "T": time,
                    "X1_Pos": time,
                    "X2_Pos": time,
                    "Y1_Pos": time,
                    "Y2_Pos": time,
                }
            )
            force_file = root / "force.xlsx"
            with pd.ExcelWriter(force_file, engine="openpyxl") as writer:
                position.to_excel(writer, sheet_name="Pos", index=False)
                press.to_excel(writer, sheet_name="Press", index=False)

            result = process_experiment(
                {
                    "experiment_id": "dic_exclusion",
                    "image_folder": str(image_folder),
                    "force_file": str(force_file),
                    "output_root": str(root / "output"),
                    "camera_setting_fps": 1.0,
                    "loading_speed": 1.0,
                    "formal_vfm_allowed": True,
                    "displacement_mode": "device",
                    "position_columns": ["X1_Pos", "X2_Pos"],
                    "manual": {
                        "force_start_index": 5,
                        "force_analysis_end_index": 45,
                        "start_frame": 0,
                        "end_frame": 4,
                    },
                    "excluded_frame_numbers": [0, 1],
                }
            )

            self.assertEqual(result["photo_count"], 3)
            with Path(result["match"]).open(encoding="utf-8-sig") as handle:
                match_rows = list(csv.DictReader(handle))
            self.assertEqual([row["照片"] for row in match_rows], ["000002.jpg", "000003.jpg", "000004.jpg"])
            self.assertEqual([row["时间/s"] for row in match_rows], ["2.5000", "3.5000", "4.5000"])
            self.assertEqual(result["excluded_frame_numbers"], [0, 1])
            self.assertTrue(result["vfm_allowed"])
            x_vfm = np.loadtxt(result["x_vfm"])
            self.assertEqual(np.atleast_1d(x_vfm).size, 3)

    def test_device_displacement_uses_two_grip_relative_change_sum(self):
        position = pd.DataFrame(
            {
                "T": [0.0, 1.0],
                "X1_Pos": [10.0, 12.0],
                "X2_Pos": [10.0, 14.0],
            }
        )

        displacement = _device_displacement(
            position,
            np.array([0.0, 1.0]),
            0.0,
            1.0,
            ["X1_Pos", "X2_Pos"],
        )

        self.assertAlmostEqual(displacement, 6.0)

    def test_relative_displacement_is_zero_at_first_photo_and_sums_two_grips(self):
        position = pd.DataFrame(
            {
                "T": [0.0, 1.0, 2.0],
                "X1_Pos": [10.0, 11.0, 12.0],
                "X2_Pos": [10.0, 12.0, 14.0],
            }
        )

        displacement = relative_displacement(
            position,
            np.array([0.0, 0.5, 1.0]),
            ["X1_Pos", "X2_Pos"],
        )

        np.testing.assert_allclose(displacement, [0.0, 1.5, 3.0])

    def test_relative_displacement_uses_monotonic_loading_envelope(self):
        position = pd.DataFrame(
            {
                "T": [0.0, 1.0, 2.0],
                "X1_Pos": [0.0, 1.0, 0.5],
                "X2_Pos": [0.0, 0.0, 0.0],
            }
        )

        displacement = relative_displacement(
            position,
            np.array([0.0, 1.0, 2.0]),
            ["X1_Pos", "X2_Pos"],
        )

        np.testing.assert_allclose(displacement, [0.0, 1.0, 1.0])

    def test_bilinear_curve_reports_linear_segment_and_yield_candidate(self):
        strain = np.linspace(0.0, 0.10, 101)
        stress = np.where(strain <= 0.03, 1000.0 * strain, 30.0 + 150.0 * (strain - 0.03))

        analysis = analyze_curve(strain, stress, linear_fraction=0.25)

        self.assertGreater(analysis.linear_r2, 0.99)
        self.assertIsNotNone(analysis.yield_index)
        self.assertAlmostEqual(strain[analysis.yield_index], 0.03, delta=0.01)

    def test_curve_without_deviation_has_no_forced_yield_point(self):
        strain = np.linspace(0.0, 0.10, 101)
        stress = 1000.0 * strain

        analysis = analyze_curve(strain, stress, linear_fraction=0.25)

        self.assertIsNone(analysis.yield_index)

    def test_curve_analysis_tolerates_small_measurement_retrace(self):
        strain = np.array([0.0, 0.01, 0.009, 0.02, 0.03, 0.04])
        stress = 1000.0 * strain

        analysis = analyze_curve(strain, stress)

        self.assertGreater(analysis.linear_r2, 0.99)

    def test_reads_matchid_dat_header_metadata_with_locally_validated_field_map(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "000001.jpg.dat"
            content = (
                "\x1e***MatchID 2D-Version 19.2.2.0"
                "<11>=<0.087464><16>=<0;2;False;395;413;329;329;388;406>"
                "<55>=<100491><18>=<0;a;b><53>=<0;True;c>"
            )
            with gzip.open(path, "wt", encoding="latin1") as handle:
                handle.write(content)

            metadata = extract_matchid_dat_metadata(path)

            self.assertEqual(metadata["version"], "19.2.2.0")
            self.assertAlmostEqual(metadata["conversion_mm_per_pixel"], 0.087464)
            self.assertEqual(metadata["point_count"], 100491)
            self.assertEqual(metadata["record_counts"], {"18": 1, "53": 1})
            self.assertTrue(metadata["raw_field_semantics_confirmed"])
            self.assertEqual(metadata["raw_field_map"]["x"], "field[1] + field[5]")
            self.assertIn("Results Viewer", metadata["raw_field_note"])

    def test_reads_matchid_job_metadata(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "Job.m2inp"
            path.write_text(
                "<Reference$image>=<000000.jpg>\n"
                "<Deformed$image>=<000001.jpg;3;0;0;None>\n"
                "<Conversion>=<0.087464>\n"
                "<Export$unit>=<1>\n"
                "<Shape>=<2;0;False;4;395;413;724;413;724;742;395;742;531;591>\n",
                encoding="utf-8",
            )

            metadata = parse_job_metadata(path)

            self.assertEqual(metadata["reference_image"], "000000.jpg")
            self.assertEqual(metadata["deformed_image_count"], 1)
            self.assertEqual(metadata["export_unit"], "mm")
            self.assertEqual(metadata["shape"].startswith("2;0;False"), True)

if __name__ == "__main__":
    unittest.main()
