from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path

if __package__:
    from .matchid_prepare import parse_job_metadata
else:
    from matchid_prepare import parse_job_metadata


REPORT_FIELDS = [
    "实验编号",
    "加载速度",
    "有效照片数",
    "有效力值数",
    "ROI尺寸",
    "ROI厚度",
    "X/Y方向",
    "起始照片",
    "断裂照片",
    "起始力",
    "峰值力",
    "数量一致",
    "时间同步",
    "E",
    "ν",
    "Y",
    "H",
    "残差",
    "内部虚功",
    "外部虚功",
    "是否撞边界",
    "结论",
]


def _shape_coordinates(shape: str) -> tuple[list[float], list[float]]:
    fields = shape.split(";")
    vertex_count = int(fields[3])
    coordinates = [float(value) for value in fields[4 : 4 + 2 * vertex_count]]
    x = coordinates[::2]
    y = coordinates[1::2]
    return x, y


def roi_bounds_px(shape: str) -> str:
    x, y = _shape_coordinates(shape)
    center_x = (min(x) + max(x)) / 2.0
    center_y = (min(y) + max(y)) / 2.0
    return (
        f"x={min(x):g}–{max(x):g}, y={min(y):g}–{max(y):g} px；"
        f"中心=({center_x:.1f}, {center_y:.1f}) px"
    )


def roi_size_mm(shape: str, conversion_mm_per_pixel: float) -> str:
    x, y = _shape_coordinates(shape)
    width = (max(x) - min(x)) * conversion_mm_per_pixel
    height = (max(y) - min(y)) * conversion_mm_per_pixel
    return f"{width:.2f} × {height:.2f} mm"


def _frame_number(name: str) -> int:
    match = re.fullmatch(r"(\d+)\.jpg", name, re.IGNORECASE)
    if match is None:
        raise ValueError(f"照片名称不是编号 JPG：{name}")
    return int(match.group(1))


def _read_values(path: Path) -> list[float]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    values: list[float] = []
    for number, row in enumerate(rows, start=1):
        if len(row) != 1 or not row[0].strip():
            raise ValueError(f"{path} 第 {number} 行不是单列力值")
        value = float(row[0])
        if not math.isfinite(value):
            raise ValueError(f"{path} 第 {number} 行力值不是有限数")
        values.append(value)
    return values


def summarize_check(
    *,
    experiment_id: str,
    loading_speed: float,
    photo_names: list[str],
    times: list[float],
    table_x: list[float],
    table_y: list[float],
    x_forces: list[float],
    y_forces: list[float],
    roi_size: str,
    roi_thickness_mm: float,
    fracture_photo: str,
    reference_image: str,
    identification_snapshot: dict | None = None,
    vfm_force_status: str | None = None,
    vfm_input_status: str | None = None,
    roi_location_status: str = "Job Shape 外接尺寸待物理位置复核",
    roi_position: str = "未计算",
) -> dict[str, str]:
    photo_count = len(photo_names)
    x_count = len(x_forces)
    y_count = len(y_forces)
    count_matches = photo_count == len(table_x) == len(table_y) == x_count == y_count
    reasons: list[str] = []
    if len(times) != photo_count or any(not math.isfinite(value) for value in times):
        reasons.append("时间缺失或非有限值")
    elif any(right <= left for left, right in zip(times, times[1:])):
        reasons.append("时间非单调")
    frame_numbers = [_frame_number(name) for name in photo_names]
    if any(right <= left for left, right in zip(frame_numbers, frame_numbers[1:])):
        reasons.append("照片序号非单调")
    if len(table_x) != x_count or any(
        not math.isclose(table_x[i], x_forces[i], rel_tol=0.0, abs_tol=1e-6)
        for i in range(min(len(table_x), x_count))
    ):
        reasons.append("X CSV 与照片—力表不一致")
    if len(table_y) != y_count or any(
        not math.isclose(table_y[i], y_forces[i], rel_tol=0.0, abs_tol=1e-6)
        for i in range(min(len(table_y), y_count))
    ):
        reasons.append("Y CSV 与照片—力表不一致")
    if x_forces and abs(x_forces[0]) > 1e-6:
        reasons.append("X 首行不为零")
    if y_forces and abs(y_forces[0]) > 1e-6:
        reasons.append("Y 首行不为零")
    if any(value < -1e-9 for value in x_forces + y_forces):
        reasons.append("拉伸力存在负值")

    notes = ["预处理数量/时间检查通过" if count_matches and not reasons else "前处理存在阻断项"]
    if fracture_photo in photo_names:
        fracture_index = photo_names.index(fracture_photo)
        notes.append(
            f"末帧力对应：{fracture_photo}，X {x_forces[fracture_index]:.6f} / "
            f"Y {y_forces[fracture_index]:.6f} N"
        )
    else:
        notes.append(f"末帧/断裂照片 {fracture_photo} 不在当前同步力表内")
    if photo_names and x_forces and y_forces:
        notes.append(
            f"末有效同步帧力：{photo_names[-1]}，X {x_forces[-1]:.6f} / Y {y_forces[-1]:.6f} N"
        )
    if roi_thickness_mm != 1.0:
        notes.append("MatchID ROI 厚度不是 1.0 mm")
    if reference_image and reference_image not in photo_names:
        notes.append(
            f"MatchID Job 参考图 {reference_image} 在当前同步表外；VFM运行须核对参考帧零力映射"
        )
    notes.append(f"ROI位置：{roi_position}；{roi_location_status}")
    if identification_snapshot:
        progress_text = (
            f"进度约 {identification_snapshot['progress_percent']}%"
            if identification_snapshot.get("progress_percent") is not None
            else "进度未显示"
        )
        notes.append(
            "MatchID 截图中存在进行中的中间候选："
            f"第 {identification_snapshot['iteration']} 轮，"
            f"Y₀={identification_snapshot['yield_mpa']:.2f} MPa，"
            f"H={identification_snapshot['hardening_mpa']:.2f} MPa，"
            f"{progress_text}；此状态不是最终识别结果，E 未显示；"
            f"界面‘{identification_snapshot['residual_label']}’={identification_snapshot['residual_display_value']}，定义/单位未核实"
        )
    else:
        notes.append("尚无可核实的参数识别运行记录")
    if vfm_force_status:
        notes.append(vfm_force_status)
    if vfm_input_status:
        notes.append(vfm_input_status)
    if not identification_snapshot:
        notes.append("当前未记录参数识别运行")

    return {
        "实验编号": experiment_id,
        "加载速度": f"{loading_speed:g} mm/s",
        "有效照片数": str(photo_count),
        "有效力值数": str(min(x_count, y_count)) if x_count == y_count else f"X={x_count}, Y={y_count}",
        "ROI尺寸": roi_size,
        "ROI厚度": f"{roi_thickness_mm:g} mm（外围整体厚度 3 mm）",
        "X/Y方向": "X：顶部 X2、底部 X1；Y：右侧 Y1、左侧 Y2",
        "起始照片": photo_names[0] if photo_names else "UNKNOWN",
        "断裂照片": fracture_photo,
        "起始力": (
            f"X {x_forces[0]:.6f} / Y {y_forces[0]:.6f} N"
            if x_forces and y_forces
            else "未计算"
        ),
        "峰值力": (
            f"X {max(x_forces):.6f} / Y {max(y_forces):.6f} N"
            if x_forces and y_forces
            else "未计算"
        ),
        "数量一致": (
            f"是（{photo_count}/{x_count}/{y_count}）"
            if count_matches
            else f"否（照片={photo_count}, X={x_count}, Y={y_count}）"
        ),
        "时间同步": (
            "阻断：" + "；".join(reasons)
            if reasons
            else "预处理通过；VFM力序列未闭合"
            if vfm_input_status and ("不一致" in vfm_input_status or "未闭合" in vfm_input_status or "为0" in vfm_input_status)
            else "预处理通过；VFM力序列未核对"
            if vfm_input_status and ("未发现" in vfm_input_status or "逐步实现" in vfm_input_status or "未运行" in vfm_input_status)
            else "预处理通过；VFM输入状态见结论"
            if vfm_input_status
            else "预处理通过"
        ),
        "E": identification_snapshot.get("E", "阶段1结果未见") if identification_snapshot else "未识别",
        "ν": "固定 0.375",
        "Y": (
            f"中间候选 {identification_snapshot['yield_mpa']:.2f} MPa（第 {identification_snapshot['iteration']} 轮；非最终）"
            if identification_snapshot
            else "未识别"
        ),
        "H": (
            f"中间候选 {identification_snapshot['hardening_mpa']:.2f} MPa（第 {identification_snapshot['iteration']} 轮；非最终）"
            if identification_snapshot
            else "未识别"
        ),
        "残差": (
            f"界面‘{identification_snapshot['residual_label']}’={identification_snapshot['residual_display_value']}；定义/单位未核实"
            if identification_snapshot
            else "未计算"
        ),
        "内部虚功": identification_snapshot.get("internal_virtual_work", "未计算") if identification_snapshot else "未计算",
        "外部虚功": identification_snapshot.get("external_virtual_work", "未计算") if identification_snapshot else "未计算",
        "是否撞边界": identification_snapshot.get("parameter_boundary_status", "未核实") if identification_snapshot else "未运行",
        "结论": "；".join(notes),
    }


def _read_match_table(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"照片", "时间/s", "X向力/N", "Y向力/N"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} 缺少字段：{sorted(missing)}")
        return list(reader)


def build_current_check(config_path: Path) -> dict:
    batch = json.loads(config_path.read_text(encoding="utf-8"))
    vfm_config_path = config_path.with_name("pa12_vfm_boundary.json")
    vfm_config = json.loads(vfm_config_path.read_text(encoding="utf-8"))
    output_root = Path(batch["output_root"])
    agent_root = output_root / "Agents" / "PA12实验数据处理"
    rows: list[dict[str, str]] = []
    for entry in batch["experiments"]:
        if entry.get("loading_mode") != "双轴":
            continue
        experiment_id = entry["experiment_id"]
        match_path = agent_root / "照片力匹配" / f"{experiment_id}_照片-力对应表.csv"
        match_rows = _read_match_table(match_path)
        count = len(match_rows)
        speed = str(entry.get("speed_label", entry["loading_speed"]))
        x_path = agent_root / "VFM专用力值" / "X方向" / f"X-{speed}-{count}.csv"
        y_path = agent_root / "VFM专用力值" / "Y方向" / f"Y-{speed}-{count}.csv"
        x_values = _read_values(x_path)
        y_values = _read_values(y_path)
        job_path = Path(entry.get("dic_job_file", Path(entry["image_folder"]) / "Job.m2inp"))
        job = parse_job_metadata(job_path)
        snapshot = vfm_config.get("current_matchid_state_snapshot", {}).get(experiment_id)
        if snapshot:
            snapshot = {
                **snapshot,
                "yield_mpa": snapshot["yield_candidate_mpa"],
                "hardening_mpa": snapshot["hardening_candidate_mpa"],
                "progress_percent": snapshot["progress_percent_approx"],
            }
        rows.append(
            summarize_check(
                experiment_id=experiment_id,
                loading_speed=float(entry["loading_speed"]),
                photo_names=[row["照片"] for row in match_rows],
                times=[float(row["时间/s"]) for row in match_rows],
                table_x=[float(row["X向力/N"]) for row in match_rows],
                table_y=[float(row["Y向力/N"]) for row in match_rows],
                x_forces=x_values,
                y_forces=y_values,
                roi_size=roi_size_mm(job["shape"], float(job["conversion_mm_per_pixel"])),
                roi_thickness_mm=float(batch["defaults"]["geometry"]["thickness_mm"]),
                fracture_photo=str(entry.get("report_fracture_label", entry.get("visual_fracture_frame", f"未视觉确认（末有效帧 {match_rows[-1]['照片']}）"))),
                reference_image=Path(job["reference_image"]).name,
                identification_snapshot=snapshot,
                vfm_input_status=vfm_config.get("vfm_input_status", {}).get(experiment_id),
                roi_location_status=vfm_config.get("roi_location_status", {}).get(experiment_id, "Job Shape外接尺寸已计算；物理中心减薄边界叠合待逐组核验"),
                roi_position=roi_bounds_px(job["shape"]),
            )
        )
    return {"experiments": rows, "experiment_count": len(rows)}


def write_current_check(config_path: Path) -> dict:
    audit = build_current_check(config_path)
    output_root = Path(json.loads(config_path.read_text(encoding="utf-8"))["output_root"])
    output_dir = output_root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
    markdown_path = output_dir / "PA12等双轴VFM当前检查结果.md"
    csv_path = output_dir / "PA12等双轴VFM当前检查结果.csv"
    fields = REPORT_FIELDS
    output_dir.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(audit["experiments"])
    lines = ["# PA12等双轴VFM当前检查结果", ""]
    lines.extend(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
        ]
    )
    for row in audit["experiments"]:
        lines.append("| " + " | ".join(row[field].replace("|", "\\|") for field in fields) + " |")
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"markdown": str(markdown_path), "csv": str(csv_path), **audit}


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 PA12 等双轴 VFM 当前检查结果")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(write_current_check(args.config), ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
