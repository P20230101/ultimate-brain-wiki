from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pa12_self_vfm import equivalent_plastic_strain_plane_stress, equivalent_stress_plane_stress, fit_elastic_modulus


def _v(row: dict[str, str], key: str) -> float:
    return float(row[key])


def audit(path: Path, train_fraction: float = 0.75) -> dict[str, float | int | str]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    split = int(len(rows) * train_fraction)
    train, test = rows[:split], rows[split:]
    elastic = [
        row for row in train
        if max(abs(_v(row, "平均exx")), abs(_v(row, "平均eyy"))) <= 0.005
        and (_v(row, "X向力/N") > 5 or _v(row, "Y向力/N") > 5)
    ]
    coefficients, forces = [], []
    for row in elastic:
        for coefficient, force in (("X虚场系数/N每MPa", "X向力/N"), ("Y虚场系数/N每MPa", "Y向力/N")):
            if _v(row, coefficient) != 0 and _v(row, force) > 5:
                coefficients.append(_v(row, coefficient))
                forces.append(_v(row, force))
    if len(coefficients) < 2:
        return {"status": "INSUFFICIENT_ELASTIC_POINTS", "train_rows": len(train), "test_rows": len(test), "elastic_points": len(coefficients)}
    modulus = float(fit_elastic_modulus(coefficients=coefficients, external_forces=forces)["modulus_mpa"])
    def plastic(row: dict[str, str]) -> tuple[float, float]:
        stress = equivalent_stress_plane_stress(_v(row, "边界σx/MPa"), _v(row, "边界σy/MPa"))
        strain = equivalent_plastic_strain_plane_stress(
            exx=_v(row, "平均eyy"), eyy=_v(row, "平均exx"), exy=_v(row, "平均exy"),
            sigma_x_mpa=_v(row, "边界σx/MPa"), sigma_y_mpa=_v(row, "边界σy/MPa"), modulus_mpa=modulus, nu=0.375,
        )
        return strain, stress
    train_points = [plastic(row) for row in train]
    test_points = [plastic(row) for row in test]
    fit_points = [(p, s) for p, s in train_points if p >= 0.001 and s > 0]
    if len(fit_points) < 2:
        return {"status": "INSUFFICIENT_PLASTIC_POINTS", "train_rows": len(train), "test_rows": len(test), "E_MPa": modulus, "elastic_points": len(coefficients)}
    x = [p for p, _ in fit_points]; y = [s for _, s in fit_points]
    xb, yb = sum(x) / len(x), sum(y) / len(y)
    hardening = sum((a - xb) * (b - yb) for a, b in zip(x, y)) / sum((a - xb) ** 2 for a in x)
    yield_stress = yb - hardening * xb
    test_points = [(p, s) for p, s in test_points if p >= 0.001 and s > 0]
    residuals = [yield_stress + hardening * p - s for p, s in test_points]
    return {"status": "PASS", "train_rows": len(train), "test_rows": len(test), "elastic_points": len(coefficients), "plastic_train_points": len(fit_points), "plastic_test_points": len(test_points), "E_MPa": modulus, "Y_MPa": yield_stress, "H_MPa": hardening, "test_rmse_MPa": math.sqrt(sum(v * v for v in residuals) / len(residuals))}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    args = parser.parse_args()
    print(audit(args.csv))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
