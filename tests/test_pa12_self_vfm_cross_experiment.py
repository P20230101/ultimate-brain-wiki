import csv
import json
import tempfile
import unittest
from pathlib import Path

from tools.audit_pa12_self_vfm_cross_experiment import audit


class CrossExperimentAuditTests(unittest.TestCase):
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
                    "阶段1": {"E_MPa": 2000.0},
                    "阶段2": {"Y_MPa": 25.0, "H_MPa": 120.0},
                    "积分质量": {"minimum_observed_area_ratio": 0.99},
                }
                (output / f"{experiment}_结果.json").write_text(json.dumps(result), encoding="utf-8")
            report = audit(root, root / "config.json")
            self.assertEqual(len(report), 2)
            self.assertAlmostEqual(report[0]["E迁移虚功RMSE_N"], 0.0, places=8)
            self.assertAlmostEqual(report[0]["阶段2迁移RMSE_MPa"], 0.0, places=8)
            self.assertEqual(report[0]["状态"], "DIAGNOSTIC_ONLY")


if __name__ == "__main__":
    unittest.main()
