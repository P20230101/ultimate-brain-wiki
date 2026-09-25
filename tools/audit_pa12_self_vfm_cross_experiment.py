"""对现有等双轴 Job ROI 逐帧结果执行留一实验参数迁移审计。"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def _fit_e(rows: list[dict[str, str]], config: dict, axes: tuple[str, ...] = ("X", "Y")) -> tuple[float | None, int]:
    minimum_force = float(config["minimum_force_n"])
    strain_limit = float(config["elastic_strain_limit"])
    coefficients: list[float] = []
    forces: list[float] = []
    for row in rows:
        if max(abs(float(row["平均exx"])), abs(float(row["平均eyy"]))) > strain_limit:
            continue
        for axis in axes:
            force = float(row[f"{axis}向力/N"])
            coefficient = float(row[f"{axis}虚场系数/N每MPa"])
            if force > minimum_force and coefficient != 0.0:
                coefficients.append(coefficient)
                forces.append(force)
    denominator = sum(value * value for value in coefficients)
    if len(coefficients) < 2 or denominator == 0:
        return None, len(coefficients)
    return sum(x * y for x, y in zip(coefficients, forces)) / denominator, len(coefficients)


def _stage2_observations(rows: list[dict[str, str]], result: dict, config: dict) -> tuple[list[float], list[float]]:
    geometry = result["方法"]
    length_x, length_y = map(float, geometry["ROI长度_mm"])
    minimum_stress = float(config["minimum_force_n"]) / max(length_x, length_y)
    peak = max(range(len(rows)), key=lambda index: float(rows[index]["等效应力/MPa"]))
    indices = [
        index for index, row in enumerate(rows)
        if index <= peak
        and float(row["等效应力/MPa"]) > minimum_stress
        and float(row["等效塑性应变"]) >= float(config["minimum_plastic_strain"])
    ]
    if len(indices) < int(config["stage2_acceptance"]["minimum_points"]):
        return [], []
    return (
        [float(rows[index]["等效塑性应变"]) for index in indices],
        [float(rows[index]["等效应力/MPa"]) for index in indices],
    )


def _linear_fit_quality(x: list[float], y: list[float], config: dict) -> tuple[float | None, float | None]:
    if len(x) < int(config["stage2_acceptance"]["minimum_points"]):
        return None, None
    fitted = _fit_linear(x, y)
    residuals = [fitted[0] + fitted[1] * value - observed for value, observed in zip(x, y)]
    rmse = math.sqrt(sum(value * value for value in residuals) / len(residuals))
    stress_range = max(y) - min(y)
    relative = rmse / stress_range if stress_range else None
    if relative is not None and relative > float(config["stage2_acceptance"]["max_relative_rmse"]):
        return None, None
    return fitted


def _fit_linear(x: list[float], y: list[float]) -> tuple[float, float]:
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    slope = sum((a - x_mean) * (b - y_mean) for a, b in zip(x, y)) / sum((a - x_mean) ** 2 for a in x)
    return y_mean - slope * x_mean, slope


def audit(results_root: Path, config_path: Path) -> list[dict[str, object]]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    experiments = []
    for result_path in sorted(results_root.glob("*/*_结果.json")):
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if "分析口径" in result.get("方法", {}) and result["方法"]["分析口径"] != "完整 Job ROI 主结果":
            continue
        csv_path = result_path.with_name(result_path.name.replace("_结果.json", "_内外虚功.csv"))
        with csv_path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        experiment_id = result.get("实验编号", result_path.parent.name)
        loading_axes = ("X", "Y") if "XY" in experiment_id else ("X",) if "_X_" in experiment_id else ("Y",)
        experiments.append((experiment_id, rows, result, loading_axes))

    output = []
    for target_id, target_rows, target_result, target_axes in experiments:
        trainers = []
        for source_id, source_rows, source_result, source_axes in experiments:
            if source_id == target_id or source_axes != target_axes:
                continue
            e, e_points = _fit_e(source_rows, config, source_axes)
            x, stress = _stage2_observations(source_rows, source_result, config)
            if e is not None:
                stage2 = _linear_fit_quality(x, stress, config) if x else (None, None)
                trainers.append((source_id, e, e_points, stage2, len(x), source_result))
        if not trainers:
            continue
        for source_id, e, e_points, stage2_fit, train_n, source_result in trainers:
            target_e, target_e_points = _fit_e(target_rows, config, target_axes)
            e_errors = []
            target_active_forces = []
            for row in target_rows:
                if max(abs(float(row["平均exx"])), abs(float(row["平均eyy"]))) <= float(config["elastic_strain_limit"]):
                    for axis in target_axes:
                        coefficient = float(row[f"{axis}虚场系数/N每MPa"])
                        force = float(row[f"{axis}向力/N"])
                        if coefficient != 0 and force > float(config["minimum_force_n"]):
                            e_errors.append(e * coefficient - force)
                            target_active_forces.append(force)
            e_rmse = math.sqrt(sum(value * value for value in e_errors) / len(e_errors)) if e_errors else None
            force_rms = math.sqrt(sum(force * force for force in target_active_forces) / len(target_active_forces)) if target_active_forces else None
            tx, ty = _stage2_observations(target_rows, target_result, config)
            stage2_rmse = None
            if stage2_fit[0] is not None and tx:
                yield_stress, hardening = stage2_fit
                residuals = [yield_stress + hardening * value - observed for value, observed in zip(tx, ty)]
                stage2_rmse = math.sqrt(sum(value * value for value in residuals) / len(residuals))
            output.append({
                "训练实验": source_id,
                "留出实验": target_id,
                "训练E_MPa": e,
                "留出E独立拟合_MPa": target_e,
                "E迁移虚功RMSE_N": e_rmse,
                "E迁移相对RMSE": None if e_rmse is None or not force_rms else e_rmse / force_rms,
                "E留出观测数": len(e_errors),
                "阶段2训练点数": train_n,
                "阶段2留出点数": len(tx),
                "训练Y_MPa": stage2_fit[0],
                "训练H_MPa": stage2_fit[1],
                "阶段2迁移RMSE_MPa": stage2_rmse,
                "状态": "DIAGNOSTIC_ONLY",
                "备注": "该审计未解除ROI、独立ν、虚功残差及重复性门槛；不得发布正式材料参数。",
            })
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-root", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    records = audit(args.results_root, args.config)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        fields = list(records[0])
        with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(records)
    for record in records:
        print(json.dumps(record, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
