import csv
import struct
import tempfile
import unittest
from pathlib import Path

from tools.audit_pa12_stress_strain import audit_experiment, audit_stress_strain_file, _write_report


class Pa12StressStrainAuditTests(unittest.TestCase):
    def _write_curve(self, folder: Path) -> tuple[Path, Path, Path]:
        csv_path = folder / "S19_X_0.2_应力应变.csv"
        plot_path = folder / "S19_X_0.2_应力应变.png"
        report_path = folder / "S19_X_0.2_应力应变分析.md"
        fields = [
            "照片", "时间/s", "X向力/N", "Y向力/N", "X向位移/mm", "X向应变", "X向应力/MPa",
            "Y向位移/mm", "Y向应变", "Y向应力/MPa",
        ]
        rows = [
            ["000001.jpg", "0", "0", "", "0", "0", "0", "", "", ""],
            ["000002.jpg", "1", "10", "", "0.3", "0.01", "10", "", "", ""],
            ["000003.jpg", "2", "20", "", "0.6", "0.02", "20", "", "", ""],
            ["000004.jpg", "3", "4", "", "0.9", "0.03", "4", "", "", ""],
            ["000005.jpg", "4", "2", "", "1.2", "0.04", "2", "", "", ""],
            ["000006.jpg", "5", "1", "", "1.5", "0.05", "1", "", "", ""],
        ]
        with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.writer(handle)
            writer.writerow(fields)
            writer.writerows(rows)
        png_header = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8 + struct.pack(">II", 64, 48)
        plot_path.write_bytes(png_header)
        report_path.write_text("# curve\n", encoding="utf-8")
        return csv_path, plot_path, report_path

    def test_audit_reports_drop_linear_fit_yield_and_nonloading_axis(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path, plot_path, report_path = self._write_curve(Path(temporary_directory))

            result = audit_stress_strain_file(
                csv_path,
                plot_path,
                report_path,
                active_axes=("X",),
            )

            self.assertEqual(result["status"], "PASS")
            self.assertTrue(result["axes"]["X"]["has_peak_and_drop"])
            self.assertGreater(result["axes"]["X"]["linear_r2"], 0.99)
            self.assertIsNotNone(result["axes"]["X"]["yield_index"])
            self.assertEqual(result["axes"]["Y"]["status"], "NOT_APPLICABLE")
            self.assertTrue(result["plot"]["valid"])

    def test_audit_experiment_keeps_unresolved_experiment_unprocessed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = audit_experiment(
                {
                    "experiment_id": "S24_Y_20",
                    "orientation": "Y",
                    "stress_strain_axes": ["Y"],
                },
                {"status": "UNRESOLVED", "stress_strain": "UNKNOWN"},
                Path(temporary_directory),
            )

            self.assertEqual(result["status"], "NOT_PROCESSED")
            self.assertIn("未生成", result["reason"])

    def test_audit_experiment_keeps_preload_release_unprocessed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = audit_experiment(
                {
                    "experiment_id": "S24_Y_20",
                    "orientation": "Y",
                    "stress_strain_axes": ["Y"],
                },
                {"status": "PRELOAD_RELEASE_ONLY", "stress_strain": "UNKNOWN"},
                Path(temporary_directory),
            )

            self.assertEqual(result["status"], "PRELOAD_RELEASE_ONLY")
            self.assertIn("预载", result["reason"])

    def test_stress_audit_report_handles_preload_release_status(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            report_path = Path(temporary_directory) / "audit.md"
            _write_report(
                report_path,
                {
                    "formal_curve_audit_ready": False,
                    "experiments": [
                        {
                            "experiment_id": "S24_Y_20",
                            "status": "PRELOAD_RELEASE_ONLY",
                            "reason": "已确认是预载释放记录。",
                        }
                    ],
                },
            )

            report = report_path.read_text(encoding="utf-8")
            self.assertIn("预载释放记录", report)

    def test_stress_audit_report_explains_missing_fracture_drop(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            report_path = Path(temporary_directory) / "audit.md"
            _write_report(
                report_path,
                {
                    "formal_curve_audit_ready": False,
                    "experiments": [
                        {
                            "experiment_id": "S15_XY_0.2",
                            "status": "REVIEW_REQUIRED",
                            "active_axes": ["X", "Y"],
                            "row_count": 284,
                            "report_exists": True,
                            "plot": {"valid": True},
                            "axes": {
                                "X": {
                                    "status": "REVIEW_REQUIRED",
                                    "finite": True,
                                    "strain_monotonic": True,
                                    "force_nonnegative_after_first": True,
                                    "first_force_near_zero": True,
                                    "has_peak_and_drop": False,
                                    "post_peak_min_ratio": None,
                                },
                                "Y": {
                                    "status": "REVIEW_REQUIRED",
                                    "finite": True,
                                    "strain_monotonic": True,
                                    "force_nonnegative_after_first": True,
                                    "first_force_near_zero": True,
                                    "has_peak_and_drop": False,
                                    "peak_stress_mpa": 53.461,
                                    "post_peak_min_ratio": 0.9997,
                                },
                            },
                        }
                    ],
                },
            )

            report = report_path.read_text(encoding="utf-8")
            self.assertIn("未观察到峰值后的明显掉载", report)
            self.assertIn("峰后最低应力/峰值=0.9997", report)


if __name__ == "__main__":
    unittest.main()
