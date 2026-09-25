from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def profile(
    result_json: Path,
    work_csv: Path,
    nu_values: list[float],
    *,
    minimum_force_n: float = 5.0,
    elastic_strain_limit: float = 0.005,
) -> list[dict[str, float | int]]:
    result = json.loads(result_json.read_text(encoding="utf-8"))
    reference_nu = float(result["方法"]["nu"])
    length_x, length_y = (float(value) for value in result["方法"]["ROI长度_mm"])
    thickness = float(result["方法"]["厚度_mm"])
    with work_csv.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    elastic_rows = [
        row for row in rows
        if max(abs(float(row["平均exx"])), abs(float(row["平均eyy"]))) <= elastic_strain_limit
        and (float(row["X向力/N"]) > minimum_force_n or float(row["Y向力/N"]) > minimum_force_n)
    ]
    observations: list[tuple[str, float, float, float]] = []
    for row in elastic_rows:
        coefficient_x = float(row["X虚场系数/N每MPa"])
        coefficient_y = float(row["Y虚场系数/N每MPa"])
        integral_x_numerator = coefficient_x * length_y * (1.0 - reference_nu**2) / thickness
        integral_y_numerator = coefficient_y * length_x * (1.0 - reference_nu**2) / thickness
        integral_x = (integral_x_numerator - reference_nu * integral_y_numerator) / (1.0 - reference_nu**2)
        integral_y = (integral_y_numerator - reference_nu * integral_x_numerator) / (1.0 - reference_nu**2)
        force_x = float(row["X向力/N"])
        force_y = float(row["Y向力/N"])
        if force_x > minimum_force_n:
            observations.append(("X", integral_x, integral_y, force_x))
        if force_y > minimum_force_n:
            observations.append(("Y", integral_x, integral_y, force_y))
    if len(observations) < 2:
        raise ValueError(f"{work_csv} 的弹性段有效虚功观测不足，无法计算 ν 剖面")

    output: list[dict[str, float | int]] = []
    for nu in nu_values:
        coefficients = [
            thickness * (integral_x + nu * integral_y) / ((1.0 - nu**2) * length_y)
            if axis == "X"
            else thickness * (integral_y + nu * integral_x) / ((1.0 - nu**2) * length_x)
            for axis, integral_x, integral_y, _ in observations
        ]
        forces = [force for _, _, _, force in observations]
        modulus = sum(coefficient * force for coefficient, force in zip(coefficients, forces)) / sum(
            coefficient * coefficient for coefficient in coefficients
        )
        residuals = [modulus * coefficient - force for coefficient, force in zip(coefficients, forces)]
        rmse = math.sqrt(sum(residual * residual for residual in residuals) / len(residuals))
        output.append(
            {
                "nu": float(nu),
                "E_MPa": float(modulus),
                "rmse_N": float(rmse),
                "max_abs_residual_N": max(abs(residual) for residual in residuals),
                "relative_rmse": float(rmse / max(forces)),
                "observation_count": len(observations),
            }
        )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="对自建 VFM 阶段1执行 E—ν 虚功残差剖面审计")
    parser.add_argument("result_json", type=Path)
    parser.add_argument("work_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--nu-min", type=float, default=-0.99)
    parser.add_argument("--nu-max", type=float, default=0.499)
    parser.add_argument("--nu-step", type=float, default=0.001)
    args = parser.parse_args()
    if not -1.0 < args.nu_min < args.nu_max < 0.5:
        parser.error("ν 范围必须位于平面应力各向同性可行区间 (-1, 0.5) 内")
    if args.nu_step <= 0.0:
        parser.error("ν 步长必须为正")
    count = math.floor(math.nextafter((args.nu_max - args.nu_min) / args.nu_step, math.inf)) + 1
    nu_values = [args.nu_min + index * args.nu_step for index in range(count)]
    rows = profile(args.result_json, args.work_csv, nu_values)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    best = min(rows, key=lambda row: float(row["rmse_N"]))
    print(json.dumps({"output_csv": str(args.output_csv), "best_profile_point": best}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
