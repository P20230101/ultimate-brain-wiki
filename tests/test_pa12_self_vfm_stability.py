import csv
import tempfile
import unittest
from pathlib import Path

from tools.audit_pa12_self_vfm_stability import audit


class StabilityAuditTests(unittest.TestCase):
    def test_fixed_windows_fit_linear_hardening_with_positive_slope(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "vfm.csv"
            fields = ["照片", "平均exx", "平均eyy", "X向力/N", "Y向力/N", "X虚场系数/N每MPa", "Y虚场系数/N每MPa", "等效塑性应变", "等效应力/MPa"]
            rows = []
            for index in range(8):
                plastic = index / 100
                rows.append({"照片": f"{index:06d}.jpg", "平均exx": "0.001", "平均eyy": "0.001", "X向力/N": "10", "Y向力/N": "10", "X虚场系数/N每MPa": "0.01", "Y虚场系数/N每MPa": "0.01", "等效塑性应变": str(plastic), "等效应力/MPa": str(20 + 100 * plastic)})
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            result = audit(path, windows=2)
            self.assertEqual(len(result), 2)
            self.assertGreater(result[0]["H_MPa"], 0)
            self.assertGreater(result[1]["H_MPa"], 0)


if __name__ == "__main__":
    unittest.main()
