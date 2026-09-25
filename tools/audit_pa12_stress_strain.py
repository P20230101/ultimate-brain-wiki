from __future__ import annotations

import argparse
import csv
import json
import math
import struct
from pathlib import Path

import numpy as np

if __package__:
    from .pa12_mechanics import analyze_curve
else:
    from pa12_mechanics import analyze_curve


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"应力—应变 CSV 没有表头：{path}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"应力—应变 CSV 没有数据：{path}")
    return rows


def _numeric_column(rows: list[dict[str, str]], column: str) -> tuple[np.ndarray | None, int, int]:
    values: list[float] = []
    missing_count = 0
    invalid_count = 0
    for row in rows:
        raw = (row.get(column) or "").strip()
        if not raw:
            missing_count += 1
            continue
        try:
            value = float(raw)
        except ValueError:
            invalid_count += 1
            continue
        if not math.isfinite(value):
            invalid_count += 1
            continue
        values.append(value)
    if missing_count or invalid_count:
        return None, missing_count, invalid_count
    return np.asarray(values, dtype=float), 0, 0


def _png_info(path: Path) -> dict:
    if not path.is_file():
        return {"exists": False, "valid": False, "width": None, "height": None}
    payload = path.read_bytes()
    if len(payload) < 24 or payload[:8] != b"\x89PNG\r\n\x1a\n":
        return {"exists": True, "valid": False, "width": None, "height": None}
    width, height = struct.unpack(">II", payload[16:24])
    return {
        "exists": True,
        "valid": width > 0 and height > 0,
        "width": width,
        "height": height,
    }


def _audit_axis(
    rows: list[dict[str, str]],
    axis: str,
    active: bool,
) -> dict:
    strain_column = f"{axis}向应变"
    stress_column = f"{axis}向应力/MPa"
    populated = sum(
        bool((row.get(strain_column) or "").strip()) or bool((row.get(stress_column) or "").strip())
        for row in rows
    )
    if not active:
        return {
            "status": "FABRICATED" if populated else "NOT_APPLICABLE",
            "populated_rows": populated,
            "strain_column": strain_column,
            "stress_column": stress_column,
        }

    strain, strain_missing, strain_invalid = _numeric_column(rows, strain_column)
    stress, stress_missing, stress_invalid = _numeric_column(rows, stress_column)
    result = {
        "status": "INVALID",
        "strain_column": strain_column,
        "stress_column": stress_column,
        "point_count": len(rows),
        "strain_missing_count": strain_missing,
        "strain_invalid_count": strain_invalid,
        "stress_missing_count": stress_missing,
        "stress_invalid_count": stress_invalid,
        "finite": strain is not None and stress is not None,
        "strain_monotonic": False,
        "force_nonnegative_after_first": False,
        "first_force_near_zero": False,
        "has_peak_and_drop": False,
        "peak_index": None,
        "peak_stress_mpa": None,
        "post_peak_min_ratio": None,
        "min_strain_step": None,
        "linear_r2": None,
        "yield_index": None,
        "yield_strain": None,
        "yield_stress_mpa": None,
    }
    if strain is None or stress is None or len(strain) != len(stress) or len(strain) < 5:
        return result

    strain_steps = np.diff(strain)
    result["min_strain_step"] = float(np.min(strain_steps)) if len(strain_steps) else None
    result["strain_monotonic"] = bool(np.all(strain_steps >= -1e-8))
    result["force_nonnegative_after_first"] = bool(np.all(stress[1:] >= -1e-9))
    result["first_force_near_zero"] = bool(abs(float(stress[0])) <= 1e-6)
    peak_index = int(np.argmax(stress))
    peak_stress = float(stress[peak_index])
    result["peak_index"] = peak_index
    result["peak_stress_mpa"] = peak_stress
    post_peak = stress[peak_index + 1 :]
    if len(post_peak) and peak_stress > 0.0:
        post_peak_min_ratio = float(np.min(post_peak) / peak_stress)
        result["post_peak_min_ratio"] = post_peak_min_ratio
        result["has_peak_and_drop"] = post_peak_min_ratio <= 0.2

    analysis = analyze_curve(strain, stress)
    result["linear_r2"] = analysis.linear_r2
    result["yield_index"] = analysis.yield_index
    result["yield_strain"] = analysis.yield_strain
    result["yield_stress_mpa"] = analysis.yield_stress
    result["status"] = "PASS" if all(
        (
            result["finite"],
            result["strain_monotonic"],
            result["force_nonnegative_after_first"],
            result["first_force_near_zero"],
            result["has_peak_and_drop"],
        )
    ) else "REVIEW_REQUIRED"
    return result


def audit_stress_strain_file(
    csv_path: Path,
    plot_path: Path,
    report_path: Path,
    *,
    active_axes: tuple[str, ...] | list[str],
) -> dict:
    try:
        rows = _read_rows(csv_path)
    except (OSError, ValueError) as error:
        return {
            "status": "INVALID",
            "csv": str(csv_path),
            "error": str(error),
            "axes": {},
            "plot": _png_info(plot_path),
            "report_exists": report_path.is_file() and report_path.stat().st_size > 0,
        }

    axes = {
        axis: _audit_axis(rows, axis, axis in active_axes)
        for axis in ("X", "Y")
    }
    plot = _png_info(plot_path)
    report_exists = report_path.is_file() and report_path.stat().st_size > 0
    active_pass = all(axes[axis]["status"] == "PASS" for axis in active_axes)
    inactive_pass = all(axes[axis]["status"] == "NOT_APPLICABLE" for axis in ("X", "Y") if axis not in active_axes)
    status = "PASS" if active_pass and inactive_pass and plot["valid"] and report_exists else "REVIEW_REQUIRED"
    return {
        "status": status,
        "csv": str(csv_path),
        "row_count": len(rows),
        "active_axes": list(active_axes),
        "axes": axes,
        "plot": plot,
        "report_exists": report_exists,
    }


def _active_axes(entry: dict) -> tuple[str, ...]:
    configured = entry.get("stress_strain_axes")
    if configured:
        return tuple(configured)
    return ("X", "Y") if entry.get("orientation") == "XY" else (entry["orientation"],)


def audit_experiment(entry: dict, manifest_row: dict, output_root: Path) -> dict:
    experiment_id = entry["experiment_id"]
    if manifest_row.get("status") == "PRELOAD_RELEASE_ONLY":
        return {
            "experiment_id": experiment_id,
            "status": "PRELOAD_RELEASE_ONLY",
            "active_axes": list(_active_axes(entry)),
            "reason": "已确认是预载释放记录，不生成拉伸应力—应变结果。",
        }
    if manifest_row.get("status") == "UNRESOLVED" or manifest_row.get("stress_strain") in (None, "", "UNKNOWN"):
        return {
            "experiment_id": experiment_id,
            "status": "NOT_PROCESSED",
            "active_axes": list(_active_axes(entry)),
            "reason": "未生成应力—应变结果；实验起点或预载仍未确认。",
        }
    csv_path = Path(manifest_row["stress_strain"])
    plot_path = Path(manifest_row["stress_strain_plot"])
    report_path = Path(manifest_row["stress_strain_report"])
    result = audit_stress_strain_file(
        csv_path,
        plot_path,
        report_path,
        active_axes=_active_axes(entry),
    )
    result["experiment_id"] = experiment_id
    return result


def build_audit(config_path: Path) -> dict:
    batch = json.loads(config_path.read_text(encoding="utf-8"))
    output_root = Path(batch["output_root"])
    record_root = output_root / "Agents" / "PA12实验数据处理" / "处理记录"
    manifest = {
        row["experiment_id"]: row
        for row in json.loads((record_root / "PA12批量处理清单.json").read_text(encoding="utf-8"))
    }
    experiments = [audit_experiment(entry, manifest[entry["experiment_id"]], output_root) for entry in batch["experiments"]]
    return {
        "config": str(config_path),
        "experiments": experiments,
        "status_counts": {
            status: sum(1 for item in experiments if item["status"] == status)
            for status in sorted({item["status"] for item in experiments})
        },
        "formal_curve_audit_ready": all(item["status"] == "PASS" for item in experiments),
    }


def _write_report(path: Path, audit: dict) -> None:
    lines = [
        "# PA12 应力—应变曲线审计",
        "",
        f"- 全部实验曲线审计通过：`{'是' if audit['formal_curve_audit_ready'] else '否'}`。",
        "- 本报告只检查已有派生结果，不修改应力—应变 CSV 或图片。",
        "",
        "| 实验 | 状态 | X 轴 | Y 轴 | PNG | 说明 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in audit["experiments"]:
        if item["status"] == "NOT_PROCESSED":
            lines.append(f"| {item['experiment_id']} | NOT_PROCESSED | - | - | - | {item['reason']} |")
            continue
        if item["status"] == "PRELOAD_RELEASE_ONLY":
            lines.append(
                f"| {item['experiment_id']} | PRELOAD_RELEASE_ONLY | - | - | - | {item['reason']} |"
            )
            continue
        x_status = item["axes"]["X"]["status"]
        y_status = item["axes"]["Y"]["status"]
        plot_status = "有效" if item["plot"]["valid"] else "无效/缺失"
        lines.append(f"| {item['experiment_id']} | {item['status']} | {x_status} | {y_status} | {plot_status} | 行数 {item['row_count']}，报告存在={item['report_exists']} |")
    lines += [
        "",
        "## 判定说明",
        "",
        "- `PASS`：活动加载轴有限、应变不下降、首行应力接近零、后续应力非负，且峰值后最低应力不高于峰值的 20%。",
        "- `REVIEW_REQUIRED`：至少一项数值或事件检查未通过；不代表原始实验错误，只表示不能自动确认。",
        "- 单轴非加载方向必须保持空值；出现数值时标记为 `FABRICATED`。",
        "- `NOT_PROCESSED`：输入实验事件尚未确定，不能补生成曲线。",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(config_path: Path) -> dict:
    audit = build_audit(config_path)
    batch = json.loads(config_path.read_text(encoding="utf-8"))
    output_root = Path(batch["output_root"])
    record_root = output_root / "Agents" / "PA12实验数据处理" / "处理记录"
    json_path = record_root / "PA12应力应变曲线审计.json"
    markdown_path = record_root / "PA12应力应变曲线审计.md"
    json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_report(markdown_path, audit)
    return {"json": str(json_path), "markdown": str(markdown_path), **audit}


def main() -> int:
    parser = argparse.ArgumentParser(description="审计 PA12 应力—应变派生结果")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    result = write_outputs(args.config)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
