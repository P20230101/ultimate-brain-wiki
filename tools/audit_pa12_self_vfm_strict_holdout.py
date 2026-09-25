from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pa12_self_vfm import equivalent_plastic_strain_plane_stress, equivalent_stress_plane_stress, fit_elastic_modulus


def _v(row: dict[str, str], key: str) -> float:
    return float(row[key])


def _machine_axis_strains(row: dict[str, str], mapping: dict[str, str]) -> tuple[float, float]:
    x_axis = mapping["machine_x_dic_axis"]
    y_axis = mapping["machine_y_dic_axis"]
    return _v(row, f"平均e{x_axis}{x_axis}"), _v(row, f"平均e{y_axis}{y_axis}")


def _hardening_indices(
    rows: list[dict[str, str]],
    plastic_strains: list[float],
    config: dict,
    roi_lengths: tuple[float, float] | list[float],
) -> list[int]:
    equivalent_stresses = [_v(row, "等效应力/MPa") for row in rows]
    peak_index = max(range(len(rows)), key=equivalent_stresses.__getitem__)
    minimum_stress = float(config["minimum_force_n"]) / max(map(float, roi_lengths))
    return [
        index for index, (stress, strain) in enumerate(zip(equivalent_stresses, plastic_strains))
        if index <= peak_index
        and stress > minimum_stress
        and strain >= float(config["minimum_plastic_strain"])
    ]


def _holdout_status(test_point_count: int, minimum_points: int) -> str:
    return "PASS" if test_point_count >= minimum_points else "INSUFFICIENT_TEST_POINTS"


def audit(path: Path, train_fraction: float = 0.75, config_path: Path = Path("configs/pa12_self_vfm.json")) -> dict[str, float | int | str]:
    result_path = path.with_name(path.name.replace("_内外虚功.csv", "_结果.json"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    mapping = result["方法"]["机器轴—DIC映射"]
    roi_lengths = result["方法"]["ROI长度_mm"]
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    split = int(len(rows) * train_fraction)
    train, test = rows[:split], rows[split:]
    elastic = [
        row for row in train
        if max(abs(_v(row, "平均exx")), abs(_v(row, "平均eyy"))) <= float(config["elastic_strain_limit"])
        and (_v(row, "X向力/N") > float(config["minimum_force_n"]) or _v(row, "Y向力/N") > float(config["minimum_force_n"]))
    ]
    coefficients, forces = [], []
    for row in elastic:
        for coefficient, force in (("X虚场系数/N每MPa", "X向力/N"), ("Y虚场系数/N每MPa", "Y向力/N")):
            if _v(row, coefficient) != 0 and _v(row, force) > float(config["minimum_force_n"]):
                coefficients.append(_v(row, coefficient))
                forces.append(_v(row, force))
    if len(coefficients) < 2:
        return {"status": "INSUFFICIENT_ELASTIC_POINTS", "train_rows": len(train), "test_rows": len(test), "elastic_points": len(coefficients)}
    modulus = float(fit_elastic_modulus(coefficients=coefficients, external_forces=forces)["modulus_mpa"])
    def plastic(row: dict[str, str]) -> tuple[float, float]:
        stress = equivalent_stress_plane_stress(_v(row, "边界σx/MPa"), _v(row, "边界σy/MPa"))
        machine_exx, machine_eyy = _machine_axis_strains(row, mapping)
        strain = equivalent_plastic_strain_plane_stress(
            exx=machine_exx, eyy=machine_eyy, exy=_v(row, "平均exy"),
            sigma_x_mpa=_v(row, "边界σx/MPa"), sigma_y_mpa=_v(row, "边界σy/MPa"),
            modulus_mpa=modulus, nu=float(config["nu"]),
        )
        return strain, stress
    train_points = [plastic(row) for row in train]
    test_points = [plastic(row) for row in test]
    train_indices = _hardening_indices(train, [p for p, _ in train_points], config, roi_lengths)
    fit_points = [train_points[index] for index in train_indices]
    if len(fit_points) < int(config["minimum_hardening_points"]):
        return {"status": "INSUFFICIENT_PLASTIC_POINTS", "train_rows": len(train), "test_rows": len(test), "E_MPa": modulus, "elastic_points": len(coefficients), "plastic_train_points": len(fit_points)}
    x = [p for p, _ in fit_points]; y = [s for _, s in fit_points]
    xb, yb = sum(x) / len(x), sum(y) / len(y)
    hardening = sum((a - xb) * (b - yb) for a, b in zip(x, y)) / sum((a - xb) ** 2 for a in x)
    yield_stress = yb - hardening * xb
    test_indices = _hardening_indices(test, [p for p, _ in test_points], config, roi_lengths)
    selected_test_points = [test_points[index] for index in test_indices]
    if not selected_test_points:
        return {"status": "INSUFFICIENT_TEST_POINTS", "train_rows": len(train), "test_rows": len(test), "E_MPa": modulus, "elastic_points": len(coefficients), "plastic_train_points": len(fit_points), "plastic_test_points": 0}
    residuals = [yield_stress + hardening * p - s for p, s in selected_test_points]
    return {"status": _holdout_status(len(selected_test_points), int(config["minimum_hardening_points"])), "train_rows": len(train), "test_rows": len(test), "elastic_points": len(coefficients), "plastic_train_points": len(fit_points), "plastic_test_points": len(selected_test_points), "E_MPa": modulus, "Y_MPa": yield_stress, "H_MPa": hardening, "test_rmse_MPa": math.sqrt(sum(v * v for v in residuals) / len(residuals)), "machine_x_dic_axis": mapping["machine_x_dic_axis"], "machine_y_dic_axis": mapping["machine_y_dic_axis"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--config", type=Path, default=Path("configs/pa12_self_vfm.json"))
    args = parser.parse_args()
    print(audit(args.csv, config_path=args.config))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
