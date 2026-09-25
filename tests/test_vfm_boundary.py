import json
import gzip
import tempfile
import unittest
from pathlib import Path

from tools.audit_pa12_vfm_boundary import _write_markdown, build_boundary_audit
from tools.vfm_boundary import (
    load_vfm_boundary_config,
    parse_matchid_vfm_metadata,
    validate_vfm_boundary_config,
)


class VfmBoundaryTests(unittest.TestCase):
    def test_boundary_report_preserves_user_force_rule_for_self_built_vfm(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "boundary.md"
            _write_markdown(
                path,
                {
                    "audit_passed": True,
                    "vfm_path": "sample.vfm",
                    "center_roi_thickness_mm": 1.0,
                    "overall_thickness_mm": 3.0,
                    "boundary_count": 4,
                    "force_series_count": 4,
                    "force_frame_counts": [258],
                    "force_values_nonnegative": True,
                    "first_force_samples_zero": True,
                    "later_force_values_positive": True,
                    "boundary_mapping": [
                        {"boundary_id": 0, "side": "顶部", "machine_channel": "X2", "force_axis": "X"},
                        {"boundary_id": 1, "side": "左侧", "machine_channel": "Y2", "force_axis": "Y"},
                        {"boundary_id": 2, "side": "右侧", "machine_channel": "Y1", "force_axis": "Y"},
                        {"boundary_id": 3, "side": "底部", "machine_channel": "X1", "force_axis": "X"},
                    ],
                    "failures": [],
                },
            )
            report = path.read_text(encoding="utf-8")

            self.assertIn("自建 VFM 主路径和 MatchID 对照均按用户确认", report)
            self.assertIn("机器力传感器读数直接作为 ROI 边界合力", report)
            self.assertIn("所有当前双轴试验均为等双轴", report)
            self.assertIn("按 0.2、2、20 mm/s 分速率识别", report)
            self.assertNotIn("力臂仍需确认", report)

    def test_boundary_audit_reports_mapping_and_real_vfm_contract(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vfm_path = root / "sample.vfm"
            payload = "\n".join(
                [
                    "<Thickness>=<1>",
                    "<Conversion>=<0.087464>",
                    "<Boundary>=<0;1;2;3>",
                    "<Forces>=<0;2;000000.jpg;0;000001.jpg;5>",
                    "<Boundary>=<1;1;2;3>",
                    "<Forces>=<1;2;000000.jpg;0;000001.jpg;6>",
                    "<Boundary>=<2;1;2;3>",
                    "<Forces>=<2;2;000000.jpg;0;000001.jpg;6>",
                    "<Boundary>=<3;1;2;3>",
                    "<Forces>=<3;2;000000.jpg;0;000001.jpg;5>",
                ]
            ).encode("utf-8")
            with gzip.open(vfm_path, "wb") as handle:
                handle.write(payload)
            config_path = root / "config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "source": {"vfm_format_evidence": str(vfm_path)},
                        "geometry": {
                            "center_roi_thickness_mm": 1.0,
                            "overall_thickness_mm": 3.0,
                        },
                        "rotated_boundary_mapping": {
                            "顶部": "X2",
                            "底部": "X1",
                            "左侧": "Y2",
                            "右侧": "Y1",
                        },
                        "loading_modes": {
                            "双轴": {
                                "positive_sides": {
                                    "X": ["顶部", "底部"],
                                    "Y": ["左侧", "右侧"],
                                }
                            },
                            "单轴 X": {
                                "positive_sides": {"X": ["顶部", "底部"]}
                            },
                            "单轴 Y": {
                                "positive_sides": {"Y": ["左侧", "右侧"]}
                            },
                        },
                        "matchid_boundary_order": ["顶部", "左侧", "右侧", "底部"],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_boundary_audit(config_path)

            self.assertTrue(audit["audit_passed"], audit["failures"])
            self.assertEqual(audit["boundary_count"], 4)
            self.assertEqual(audit["force_frame_counts"], [2])
            self.assertTrue(audit["first_force_samples_zero"])
            self.assertTrue(audit["later_force_values_positive"])
            self.assertEqual(
                [row["side"] for row in audit["boundary_mapping"]],
                ["顶部", "左侧", "右侧", "底部"],
            )

    def test_rotated_boundary_mapping_is_explicit_and_positive(self):
        config = load_vfm_boundary_config(Path("configs/pa12_vfm_boundary.json"))

        validate_vfm_boundary_config(config)

        self.assertEqual(config["geometry"]["center_roi_thickness_mm"], 1.0)
        self.assertEqual(config["geometry"]["overall_thickness_mm"], 3.0)
        self.assertEqual(
            config["rotated_boundary_mapping"],
            {
                "顶部": "X2",
                "底部": "X1",
                "左侧": "Y2",
                "右侧": "Y1",
            },
        )
        self.assertEqual(
            config["loading_modes"]["双轴"]["positive_sides"],
            {"X": ["顶部", "底部"], "Y": ["左侧", "右侧"]},
        )
        self.assertEqual(
            config["loading_modes"]["单轴 X"]["positive_sides"],
            {"X": ["顶部", "底部"]},
        )

    def test_matchid_vfm_metadata_reads_four_boundaries_and_force_series(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "sample.vfm"
            payload = "\n".join(
                [
                    "<Thickness>=<1>",
                    "<Conversion>=<0.087464>",
                    "<Boundary>=<0;1;1;2;3;2;2;0;False;False;0;-90;200>",
                    "<Forces>=<0;2;000000.jpg;0;000001.jpg;5>",
                    "<Boundary>=<1;1;4;2;4;5;6;3;False;False;0;270;200>",
                    "<Forces>=<1;2;000000.jpg;0;000001.jpg;6>",
                    "<Boundary>=<2;1;7;2;7;5;8;3;False;False;0;-90;200>",
                    "<Forces>=<2;2;000000.jpg;0;000001.jpg;6>",
                    "<Boundary>=<3;1;6;6;1;6;2;8;True;False;0;-90;200>",
                    "<Forces>=<3;2;000000.jpg;0;000001.jpg;5>",
                ]
            ).encode("utf-8")
            with gzip.open(path, "wb") as handle:
                handle.write(payload)

            metadata = parse_matchid_vfm_metadata(path)

            self.assertEqual(metadata["thickness_mm"], 1.0)
            self.assertEqual(metadata["boundary_count"], 4)
            self.assertEqual(metadata["force_series_count"], 4)
            self.assertEqual(metadata["force_series"][0]["values"], [0.0, 5.0])
            self.assertTrue(metadata["all_force_values_nonnegative"])
            self.assertTrue(metadata["first_force_samples_zero"])
            self.assertTrue(metadata["later_force_values_positive"])


if __name__ == "__main__":
    unittest.main()
