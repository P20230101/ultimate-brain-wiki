from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path


def _read_single_column_values(path: Path) -> list[float]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    values: list[float] = []
    for row_number, row in enumerate(rows, start=1):
        if len(row) != 1 or not row[0].strip():
            raise ValueError(f"{path.name} 第 {row_number} 行不是单列数值")
        value = float(row[0])
        if not math.isfinite(value):
            raise ValueError(f"{path.name} 第 {row_number} 行不是有限数值")
        values.append(value)
    return values


def _read_match_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def _strictly_increasing(values: list[float]) -> bool:
    return len(values) >= 2 and all(right > left for left, right in zip(values, values[1:]))


def _photo_numbers(rows: list[dict[str, str]]) -> list[int]:
    numbers: list[int] = []
    for row in rows:
        match = re.fullmatch(r"(\d+)\.jpg", row["照片"])
        if match is None:
            raise ValueError(f"照片字段不是帧号 JPG：{row['照片']}")
        numbers.append(int(match.group(1)))
    return numbers


def audit_vfm_triplet(
    match_path: Path,
    x_path: Path,
    y_path: Path,
    *,
    active_axes: list[str],
) -> dict:
    failures: list[str] = []
    match_count = x_count = y_count = 0
    rows: list[dict[str, str]] = []
    x_values: list[float] = []
    y_values: list[float] = []

    for path in (match_path, x_path, y_path):
        if not path.is_file():
            failures.append(f"缺少文件：{path}")

    if not failures:
        try:
            rows, fields = _read_match_rows(match_path)
            match_count = len(rows)
            required_fields = {"照片", "X向力/N", "Y向力/N"}
            if not required_fields.issubset(fields):
                failures.append(f"照片—力表缺少字段：{sorted(required_fields - set(fields))}")
            if "时间/s" in fields:
                times = [float(row["时间/s"]) for row in rows]
                if not _strictly_increasing(times):
                    failures.append("照片时间不严格递增")
            numbers = _photo_numbers(rows)
            if len(set(numbers)) != len(numbers):
                failures.append("照片帧号重复")
            if numbers != sorted(numbers):
                failures.append("照片帧号不是递增顺序")
            x_values = _read_single_column_values(x_path)
            y_values = _read_single_column_values(y_path)
            x_count = len(x_values)
            y_count = len(y_values)
        except (KeyError, ValueError, UnicodeError) as error:
            failures.append(str(error))

    if not (match_count == x_count == y_count):
        failures.append(f"数量不一致：照片={match_count}，X={x_count}，Y={y_count}")
    if x_values and y_values:
        if abs(x_values[0]) > 1e-9 or abs(y_values[0]) > 1e-9:
            failures.append("VFM 第一行未归零")
        if "X" in active_axes and any(value <= 0.0 for value in x_values[1:]):
            failures.append("X 主动方向存在非正力值")
        if "Y" in active_axes and any(value <= 0.0 for value in y_values[1:]):
            failures.append("Y 主动方向存在非正力值")

    return {
        "sync_triplet_ready": not failures,
        "match_count": match_count,
        "x_count": x_count,
        "y_count": y_count,
        "failures": failures,
    }


def _active_axes(entry: dict) -> list[str]:
    axes = entry.get("stress_strain_axes")
    if axes:
        return list(axes)
    orientation = str(entry.get("orientation", "X")).upper()
    return ["X", "Y"] if "XY" in orientation else ["Y"] if orientation == "Y" else ["X"]


def _speed_label(entry: dict) -> str:
    return str(entry.get("speed_label", entry.get("loading_speed", "UNKNOWN")))


def _audit_experiment(entry: dict, manifest_row: dict, agent_root: Path) -> dict:
    experiment_id = entry["experiment_id"]
    safe_id = re.sub(r'[<>:"/\\|?*]', "_", experiment_id)
    match_path = agent_root / "照片力匹配" / f"{safe_id}_照片-力对应表.csv"
    photo_count = manifest_row.get("photo_count", "UNKNOWN")
    result = {
        "experiment_id": experiment_id,
        "status": manifest_row.get("status", "UNKNOWN"),
        "failures": [],
        "vfm": None,
    }

    if manifest_row.get("status") == "VFM_READY":
        if photo_count == "UNKNOWN":
            result["failures"].append("正式 VFM 状态却没有照片数量")
        else:
            speed = _speed_label(entry)
            x_path = agent_root / "VFM专用力值" / "X方向" / f"X-{speed}-{photo_count}.csv"
            y_path = agent_root / "VFM专用力值" / "Y方向" / f"Y-{speed}-{photo_count}.csv"
            result["vfm"] = audit_vfm_triplet(
                match_path,
                x_path,
                y_path,
                active_axes=_active_axes(entry),
            )
            result["failures"].extend(result["vfm"]["failures"])
            if result["vfm"]["match_count"] != int(photo_count):
                result["failures"].append(
                    f"清单照片数量与匹配表不一致：清单={photo_count}，匹配表={result['vfm']['match_count']}"
                )
    elif manifest_row.get("status") == "DATA_LIMITED":
        if not match_path.is_file():
            result["failures"].append("数据受限实验缺少诊断照片—力表")
    elif manifest_row.get("status") == "UNRESOLVED":
        if match_path.is_file():
            result["failures"].append("未解决实验不应有正式照片—力表")

    for field in ("stress_strain", "stress_strain_plot", "stress_strain_report"):
        value = manifest_row.get(field, "UNKNOWN")
        if value not in ("UNKNOWN", "") and not Path(value).is_file():
            result["failures"].append(f"清单记录的文件不存在：{value}")

    return result


def audit_outputs(config_path: Path) -> dict:
    batch = json.loads(config_path.read_text(encoding="utf-8"))
    output_root = Path(batch["output_root"])
    agent_root = output_root / "Agents" / "PA12实验数据处理"
    record_root = agent_root / "处理记录"
    manifest_path = record_root / "PA12批量处理清单.json"
    overview_path = agent_root / "实验概览" / "PA12实验概览_汇总.csv"
    matchid_path = agent_root / "MatchID_VFM准备" / "PA12_MatchID_VFM实验级索引.csv"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_by_id = {row["experiment_id"]: row for row in manifest}
    experiment_results = [
        _audit_experiment(entry, manifest_by_id[entry["experiment_id"]], agent_root)
        for entry in batch["experiments"]
    ]
    failures: list[str] = []

    with overview_path.open("r", newline="", encoding="utf-8-sig") as handle:
        overview_rows = list(csv.DictReader(handle))
    if len(overview_rows) != len(batch["experiments"]):
        failures.append(
            f"实验概览行数不等于配置实验数：概览={len(overview_rows)}，配置={len(batch['experiments'])}"
        )

    matchid_rows: list[dict[str, str]] = []
    if not matchid_path.is_file():
        failures.append(f"缺少 MatchID 实验级索引：{matchid_path}")
    else:
        with matchid_path.open("r", newline="", encoding="utf-8-sig") as handle:
            matchid_rows = list(csv.DictReader(handle))
        if len(matchid_rows) != len(batch["experiments"]):
            failures.append(
                f"MatchID 实验级索引行数不等于配置实验数：索引={len(matchid_rows)}，配置={len(batch['experiments'])}"
            )

    for result in experiment_results:
        failures.extend(f"{result['experiment_id']}：{failure}" for failure in result["failures"])

    all_sync_triplets_ready = all(
        item["status"] == "VFM_READY"
        and item["vfm"] is not None
        and item["vfm"]["sync_triplet_ready"]
        for item in experiment_results
    )
    return {
        "audit_passed": not failures,
        "all_sync_triplets_ready": not failures and all_sync_triplets_ready,
        "config": str(config_path),
        "output_root": str(output_root),
        "experiment_count": len(batch["experiments"]),
        "overview_count": len(overview_rows),
        "matchid_index_count": len(matchid_rows),
        "experiments": experiment_results,
        "failures": failures,
    }


def _write_report(path: Path, audit: dict) -> None:
    ready = [item for item in audit["experiments"] if item["status"] == "VFM_READY"]
    blocked = [item for item in audit["experiments"] if item["status"] != "VFM_READY"]
    lines = [
        "# PA12 数据合理性审计报告",
        "",
        "## 审计目的",
        "",
        "检查照片—力对应表与 X/Y 同步力文件的机器可读数量和数值契约；不判定材料参数或 VFM 识别是否正式发布。",
        "",
        "## 总体结论",
        "",
        f"- 配置实验数：`{audit['experiment_count']}`。",
        f"- 实验概览行数：`{audit['overview_count']}`。",
        f"- MatchID 实验级索引行数：`{audit['matchid_index_count']}`。",
        f"- 同步输入三文件审计对象：`{len(ready)}` 个。",
        f"- 阻断或待人工确认对象：`{len(blocked)}` 个。",
        f"- 输出契约审计：**{'通过' if audit['audit_passed'] else '存在失败项'}**。",
        f"- 照片—力—X/Y 同步输入数量契约在全部配置实验中就绪：**{'是' if audit['all_sync_triplets_ready'] else '否'}**。",
        "- 本报告只审计同步输入契约，不代表正式材料参数/VFM 发布就绪。",
        "",
        "## 分实验结果",
        "",
    ]
    for item in audit["experiments"]:
        vfm = item["vfm"]
        if vfm is None:
            lines.append(f"- `{item['experiment_id']}`（{item['status']}）：不属于完整同步输入三文件审计对象。")
        else:
            lines.append(
                f"- `{item['experiment_id']}`：照片 `{vfm['match_count']}`，X `{vfm['x_count']}`，Y `{vfm['y_count']}`；"
                f"三者一致={'是' if vfm['sync_triplet_ready'] else '否'}。"
            )
        if item["failures"]:
            lines.extend(f"  - 失败：{failure}" for failure in item["failures"])
    lines += [
        "",
        "## 下一步",
        "",
        "- 同步力值通过数量和数值契约后，仍需确认 DIC Job 是否覆盖同一批有效帧。",
        "- MatchID 2D 19.2.2.0 的 Results Viewer 字段、分隔符和单位已在当前版本本地交叉验证；更换版本时需重新验证 DAT 映射。",
        "- S23 已由视觉确认断裂，但力文件在断裂前结束，断裂时力缺失；不补造断裂力。S24 是预载释放记录，不进入完整拉伸识别。",
        "- 此输出审计不代替 VFM 虚功、材料参数识别或物理证据门槛；外围机器力按用户确认直接作为中心 ROI 边界合力，相关定义见自建 VFM 方法记录。",
        "- 双轴数据均为等双轴；按 0.2、2、20 mm/s 分速率识别。阶段 1 固定 ν=0.375 识别 E；阶段 2 固定 E、ν 识别 Y、H。",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="审计 PA12 批处理输出")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    audit = audit_outputs(args.config)
    output_root = Path(audit["output_root"])
    record_root = output_root / "Agents" / "PA12实验数据处理" / "处理记录"
    report_path = record_root / "PA12数据合理性审计报告.md"
    json_path = record_root / "PA12数据合理性审计结果.json"
    _write_report(report_path, audit)
    json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(report_path), "json": str(json_path), **audit}, ensure_ascii=False, indent=2))
    return 0 if audit["audit_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
