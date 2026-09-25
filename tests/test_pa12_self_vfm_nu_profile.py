import csv
import json
import tempfile
import unittest
from pathlib import Path

from tools.audit_pa12_self_vfm_nu_profile import profile


class PoissonProfileTests(unittest.TestCase):
    def test_profile_recovers_known_poisson_ratio_from_independent_axis_strains(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result_path = root / "result.json"
            work_path = root / "work.csv"
            result_path.write_text(
                json.dumps({"方法": {"nu": 0.375, "ROI长度_mm": [10.0, 8.0], "厚度_mm": 1.0}}),
                encoding="utf-8",
            )
            reference_nu = 0.375
            true_nu = 0.30
            true_modulus = 2000.0
            strain_integrals = [(1.0, 2.0), (2.0, 1.0), (1.5, 3.0), (3.0, 1.0)]
            fields = [
                "平均exx", "平均eyy", "X向力/N", "Y向力/N",
                "X虚场系数/N每MPa", "Y虚场系数/N每MPa",
            ]
            with work_path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                for integral_x, integral_y in strain_integrals:
                    coefficient_x = (integral_x + true_nu * integral_y) / ((1 - true_nu**2) * 8.0)
                    coefficient_y = (integral_y + true_nu * integral_x) / ((1 - true_nu**2) * 10.0)
                    reference_x = (integral_x + reference_nu * integral_y) / ((1 - reference_nu**2) * 8.0)
                    reference_y = (integral_y + reference_nu * integral_x) / ((1 - reference_nu**2) * 10.0)
                    writer.writerow({
                        "平均exx": 0.001,
                        "平均eyy": 0.001,
                        "X向力/N": true_modulus * coefficient_x,
                        "Y向力/N": true_modulus * coefficient_y,
                        "X虚场系数/N每MPa": reference_x,
                        "Y虚场系数/N每MPa": reference_y,
                    })

            rows = profile(result_path, work_path, [0.25, 0.30, 0.35, 0.375])

        best = min(rows, key=lambda row: row["rmse_N"])
        self.assertEqual(best["nu"], true_nu)
        self.assertAlmostEqual(best["E_MPa"], true_modulus)
        self.assertAlmostEqual(best["rmse_N"], 0.0, places=10)


if __name__ == "__main__":
    unittest.main()
