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
    modulus = result["阶段1"].get("E_MPa")
    if modulus is None or not math.isfinite(float(modulus)) or float(modulus) <= 0:
        return [], []
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
    return (
        [float(rows[index]["等效塑性应变"]) for index in indices],
        [float(rows[index]["等效应力/MPa"]) for index in indices],
    )


def _linear_fit_quality(x: list[float], y: list[float], config: dict) -> tuple[tuple[float, float] | None, dict[str, float | int | str]]:
    if len(x) < int(config["stage2_acceptance"]["minimum_points"]):
        return None, {"status": "NOT_COMPUTED", "point_count": len(x)}
    fitted = _fit_linear(x, y)
    residuals = [fitted[0] + fitted[1] * value - observed for value, observed in zip(x, y)]
    rmse = math.sqrt(sum(value * value for value in residuals) / len(residuals))
    maximum_stress = max(y)
    relative = rmse / maximum_stress if maximum_stress else 0.0
    quality = {
        "status": "PASS" if relative <= float(config["stage2_acceptance"]["max_relative_rmse"]) else "REVIEW_REQUIRED",
        "point_count": len(x),
        "relative_rmse": relative,
        "acceptance_limit": float(config["stage2_acceptance"]["max_relative_rmse"]),
        "rmse_mpa": rmse,
    }
    return fitted, quality


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
        if "XY" not in experiment_id:
            continue
        experiments.append((experiment_id, rows, result))

    output = []
    active_axes = ("X", "Y")
    for target_id, target_rows, target_result in experiments:
        trainers = []
        for source_id, source_rows, source_result in experiments:
            if source_id == target_id:
                continue
            e, e_points = _fit_e(source_rows, config, active_axes)
            x, stress = _stage2_observations(source_rows, source_result, config)
            if e is not None:
                stage2_fit, stage2_quality = _linear_fit_quality(x, stress, config) if x else (None, {"status": "NOT_COMPUTED", "point_count": 0})
                trainers.append((source_id, e, e_points, stage2_fit, stage2_quality, len(x), source_result))
        if not trainers:
            continue
        for source_id, e, e_points, stage2_fit, stage2_quality, train_n, source_result in trainers:
            target_e, target_e_points = _fit_e(target_rows, config, active_axes)
            e_errors = []
            target_active_forces = []
            for row in target_rows:
                if max(abs(float(row["平均exx"])), abs(float(row["平均eyy"]))) <= float(config["elastic_strain_limit"]):
                    for axis in active_axes:
                        coefficient = float(row[f"{axis}虚场系数/N每MPa"])
                        force = float(row[f"{axis}向力/N"])
                        if coefficient != 0 and force > float(config["minimum_force_n"]):
                            e_errors.append(e * coefficient - force)
                            target_active_forces.append(force)
            e_rmse = math.sqrt(sum(value * value for value in e_errors) / len(e_errors)) if e_errors else None
            force_rms = math.sqrt(sum(force * force for force in target_active_forces) / len(target_active_forces)) if target_active_forces else None
            tx, ty = _stage2_observations(target_rows, target_result, config)
            stage2_rmse = None
            if stage2_fit is not None and tx:
                yield_stress, hardening = stage2_fit
                residuals = [yield_stress + hardening * value - observed for value, observed in zip(tx, ty)]
                stage2_rmse = math.sqrt(sum(value * value for value in residuals) / len(residuals))
            output.append({
                "训练实验": source_id,
                "留出实验": target_id,
                "训练E_MPa": e,
                "训练E阶段1状态": source_result["阶段1"]["质量"]["status"],
                "训练E阶段1相对RMSE": source_result["阶段1"]["质量"].get("relative_rmse"),
                "留出E独立拟合_MPa": target_e,
                "E迁移虚功RMSE_N": e_rmse,
                "E迁移相对RMSE": None if e_rmse is None or not force_rms else e_rmse / force_rms,
                "E留出观测数": len(e_errors),
                "训练E点数": e_points,
                "留出E点数": target_e_points,
                "阶段2训练点数": train_n,
                "阶段2留出点数": len(tx),
                "阶段2训练状态": stage2_quality["status"],
                "阶段2训练相对RMSE": stage2_quality.get("relative_rmse"),
                "阶段2训练拟合RMSE_MPa": stage2_quality.get("rmse_mpa"),
                "训练Y_MPa": None if stage2_fit is None else stage2_fit[0],
                "训练H_MPa": None if stage2_fit is None else stage2_fit[1],
                "阶段2迁移RMSE_MPa": stage2_rmse,
                "状态": "DIAGNOSTIC_ONLY",
                "备注": "该审计未解除ROI、独立ν、虚功残差及重复性门槛；不得发布正式材料参数。",
            })
    return output


def _render_markdown(records: list[dict[str, object]]) -> str:
    lines = [
        "# PA12 等双轴跨实验留出审计",
        "",
        f"共 {len(records)} 个有向配对；全部为诊断结果，不构成正式材料参数或跨速率泛化结论。",
        "",
        "阶段 1 的 E 迁移相对 RMSE，以匹配弹性观测点外力 RMS 归一化。阶段 2 训练相对 RMSE 按生产 runner 定义为 `RMSE/max(σ)`；少于配置规定的 20 个训练点时不拟合。",
        "",
        "| 训练 → 留出 | 训练 E (MPa) | E 阶段1状态/RMSE | E 迁移相对 RMSE | 训练 Y/H (MPa) | 阶段2状态/RMSE | 阶段2迁移 RMSE (MPa) | 阶段2训练点数 |",
        "| --- | ---: | --- | ---: | --- | --- | ---: | ---: |",
    ]
    for row in records:
        e_rmse = row["训练E阶段1相对RMSE"]
        e_transfer = row["E迁移相对RMSE"]
        stage2_relative = row["阶段2训练相对RMSE"]
        stage2_rmse = row["阶段2迁移RMSE_MPa"]
        y, hardening = row["训练Y_MPa"], row["训练H_MPa"]
        yh = "未拟合" if y is None else f"{float(y):.2f}/{float(hardening):.2f}"
        stage2_quality = "未计算" if stage2_relative is None else f"{float(stage2_relative):.5f}"
        transfer = "—" if stage2_rmse is None else f"{float(stage2_rmse):.2f}"
        lines.append(
            f"| {row['训练实验']} → {row['留出实验']} | {float(row['训练E_MPa']):.2f} | "
            f"{row['训练E阶段1状态']} / {float(e_rmse):.5f} | {float(e_transfer):.2%} | "
            f"{yh} | {row['阶段2训练状态']} / {stage2_quality} | {transfer} | "
            f"{int(row['阶段2训练点数'])} |")
    lines += [
        "",
        "S15–S18 的加载速度和实验组别混杂，且没有同速率重复试样；跨组迁移误差不能单独归因于加载速率，也不能证明材料重复性。S17 阶段 2只有 4 个候选点，低于 20 点门槛。",
        "",
        "复现：",
        "",
        "```powershell",
        "python tools/audit_pa12_self_vfm_cross_experiment.py --results-root \"Agents/PA12实验数据处理/VFM自建/实验结果\" --config configs/pa12_self_vfm.json --output \"Agents/PA12实验数据处理/VFM自建/汇总/PA12等双轴跨实验留出审计.csv\" --markdown-output \"Agents/PA12实验数据处理/VFM自建/汇总/PA12等双轴跨实验留出审计.md\"",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-root", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    args = parser.parse_args()
    records = audit(args.results_root, args.config)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        fields = list(records[0])
        with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(records)
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(_render_markdown(records), encoding="utf-8")
    for record in records:
        print(json.dumps(record, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
