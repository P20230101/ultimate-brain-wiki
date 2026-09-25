import csv
import json
import tempfile
import unittest
from pathlib import Path

from tools.audit_pa12_self_vfm_cross_experiment import _linear_fit_quality, _render_markdown, _stage2_observations, audit


class CrossExperimentAuditTests(unittest.TestCase):
    def test_markdown_report_includes_every_pair_and_production_error_definition(self):
        records = [
            {
                "训练实验": "S16_XY_0.2", "留出实验": "S15_XY_0.2", "训练E_MPa": 3410.4,
                "训练E阶段1状态": "PASS", "训练E阶段1相对RMSE": 0.0476,
                "E迁移相对RMSE": 0.191, "训练Y_MPa": 39.5, "训练H_MPa": 156.4,
                "阶段2训练状态": "PASS", "阶段2训练相对RMSE": 0.1259,
                "阶段2迁移RMSE_MPa": 11.1, "阶段2训练点数": 222,
            },
            {
                "训练实验": "S17_XY_20", "留出实验": "S15_XY_0.2", "训练E_MPa": 4997.7,
                "训练E阶段1状态": "PASS", "训练E阶段1相对RMSE": 0.0565,
                "E迁移相对RMSE": 0.447, "训练Y_MPa": None, "训练H_MPa": None,
                "阶段2训练状态": "NOT_COMPUTED", "阶段2训练相对RMSE": None,
                "阶段2迁移RMSE_MPa": None, "阶段2训练点数": 4,
            },
        ]
        report = _render_markdown(records)
        self.assertEqual(report.count("| S"), 2)
        self.assertIn("RMSE/max(σ)", report)
        self.assertIn("| 4 |", report)

    def test_stage2_quality_uses_maximum_fitted_stress_as_runner_does(self):
        config = {"stage2_acceptance": {"minimum_points": 3, "max_relative_rmse": 0.25}}
        x = [0.001, 0.002, 0.003]
        y = [10.0, 20.0, 40.0]
        fit, quality = _linear_fit_quality(x, y, config)
        self.assertIsNotNone(fit)
        # Production runner normalizes by the maximum fitted equivalent stress.
        residuals = [fit[0] + fit[1] * value - observed for value, observed in zip(x, y)]
        relative = (sum(value * value for value in residuals) / len(residuals)) ** 0.5 / max(y)
        self.assertAlmostEqual(relative, 0.05893, places=4)
        self.assertEqual(quality["status"], "PASS")
        self.assertAlmostEqual(quality["relative_rmse"], relative, places=10)

    def test_stage2_selection_blocks_when_stage1_modulus_is_unusable(self):
        config = {
            "minimum_force_n": 5.0,
            "minimum_plastic_strain": 0.001,
            "stage2_acceptance": {"minimum_points": 3, "max_relative_rmse": 0.25},
        }
        rows = [
            {"等效应力/MPa": "10", "等效塑性应变": "0.002"},
            {"等效应力/MPa": "20", "等效塑性应变": "0.003"},
            {"等效应力/MPa": "30", "等效塑性应变": "0.004"},
        ]
        result = {"方法": {"ROI长度_mm": [10.0, 10.0]}, "阶段1": {"E_MPa": -1.0}}
        self.assertEqual(_stage2_observations(rows, result, config), ([], []))

    def test_leave_one_experiment_out_recovers_parameters_on_synthetic_holdout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = {
                "nu": 0.0,
                "minimum_force_n": 1.0,
                "elastic_strain_limit": 0.005,
                "minimum_plastic_strain": 0.001,
                "stage2_acceptance": {"minimum_points": 3, "max_relative_rmse": 0.25},
            }
            (root / "config.json").write_text(json.dumps(config), encoding="utf-8")
            fields = ["照片", "平均exx", "平均eyy", "X向力/N", "Y向力/N", "X虚场系数/N每MPa", "Y虚场系数/N每MPa", "等效塑性应变", "等效应力/MPa"]
            for experiment in ("S15_XY_0.2", "S16_XY_0.2"):
                output = root / experiment
                output.mkdir()
                rows = []
                for index in range(5):
                    plastic = 0.002 + index * 0.002
                    rows.append({
                        "照片": f"{index:06d}.jpg",
                        "平均exx": "0.001", "平均eyy": "0.001",
                        "X向力/N": str(2000 * 0.01), "Y向力/N": "0",
                        "X虚场系数/N每MPa": "0.01", "Y虚场系数/N每MPa": "0",
                        "等效塑性应变": str(plastic), "等效应力/MPa": str(25 + 120 * plastic),
                    })
                with (output / f"{experiment}_内外虚功.csv").open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(rows)
                result = {
                    "方法": {"厚度_mm": 1.0, "ROI长度_mm": [10.0, 10.0]},
                    "阶段1": {"E_MPa": 2000.0, "质量": {"status": "PASS", "relative_rmse": 0.0}},
                    "阶段2": {"Y_MPa": 25.0, "H_MPa": 120.0},
                    "积分质量": {"minimum_observed_area_ratio": 0.99},
                }
                (output / f"{experiment}_结果.json").write_text(json.dumps(result), encoding="utf-8")
            report = audit(root, root / "config.json")
            self.assertEqual(len(report), 2)
            self.assertAlmostEqual(report[0]["E迁移虚功RMSE_N"], 0.0, places=8)
            self.assertAlmostEqual(report[0]["阶段2迁移RMSE_MPa"], 0.0, places=8)
            self.assertEqual(report[0]["状态"], "DIAGNOSTIC_ONLY")
            self.assertEqual(report[0]["训练E阶段1状态"], "PASS")
            self.assertEqual(report[0]["阶段2训练状态"], "PASS")
            self.assertEqual(report[0]["训练E点数"], 5)


if __name__ == "__main__":
    unittest.main()
