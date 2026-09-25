from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import pandas as pd

if __package__:
    from .pa12_sync import process_experiment
else:
    from pa12_sync import process_experiment


MANIFEST_FIELDS = [
    "experiment_id",
    "status",
    "force_file",
    "image_folder",
    "camera_setting_fps",
    "camera_setting_source",
    "photo_count",
    "first_image",
    "last_image",
    "force_start_index",
    "force_peak_index",
    "force_fracture_index",
    "force_analysis_end_index",
    "end_event_label",
    "visual_fracture_confirmed",
    "visual_fracture_frame",
    "visual_fracture_time_estimate",
    "last_force_supported_photo",
    "force_missing_at_visual_fracture",
    "camera_actual_fps",
    "effective_time",
    "photo_displacement",
    "force_displacement",
    "stress_strain",
    "stress_strain_plot",
    "stress_strain_report",
    "vfm_allowed",
    "vfm_error",
    "notes",
]

OVERVIEW_FIELDS = [
    "速度",
    "照片数量",
    "设置频率",
    "实际频率",
    "照片位移",
    "力数量",
    "力位移",
    "力数据时间",
    "力传感频率",
]


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _manifest_row(entry: dict, *, status: str, result: dict | None = None, error: str = "") -> dict:
    result = result or {}
    return {
        "experiment_id": entry["experiment_id"],
        "status": status,
        "force_file": entry.get("force_file", "UNKNOWN"),
        "image_folder": entry.get("image_folder", "UNKNOWN"),
        "camera_setting_fps": entry.get("camera_setting_fps", "UNKNOWN"),
        "camera_setting_source": entry.get("camera_setting_source", "UNKNOWN"),
        "photo_count": result.get("photo_count", "UNKNOWN"),
        "first_image": result.get("first_image", "UNKNOWN"),
        "last_image": result.get("last_image", "UNKNOWN"),
        "force_start_index": result.get("force_start_index", "UNKNOWN"),
        "force_peak_index": result.get("force_peak_index", "UNKNOWN"),
        "force_fracture_index": result.get("force_fracture_index", "UNKNOWN"),
        "force_analysis_end_index": result.get("force_analysis_end_index", "UNKNOWN"),
        "end_event_label": result.get("end_event_label", "UNKNOWN"),
        "visual_fracture_confirmed": result.get("visual_fracture_confirmed", False),
        "visual_fracture_frame": result.get("visual_fracture_frame", "UNKNOWN"),
        "visual_fracture_time_estimate": result.get("visual_fracture_time_estimate", "UNKNOWN"),
        "last_force_supported_photo": result.get("last_force_supported_photo", "UNKNOWN"),
        "force_missing_at_visual_fracture": result.get("force_missing_at_visual_fracture", False),
        "camera_actual_fps": result.get("camera_actual_fps", "UNKNOWN"),
        "effective_time": result.get("effective_time", "UNKNOWN"),
        "photo_displacement": result.get("photo_displacement", "UNKNOWN"),
        "force_displacement": result.get("force_displacement", "UNKNOWN"),
        "stress_strain": result.get("stress_strain", "UNKNOWN"),
        "stress_strain_plot": result.get("stress_strain_plot", "UNKNOWN"),
        "stress_strain_report": result.get("stress_strain_report", "UNKNOWN"),
        "vfm_allowed": result.get("vfm_allowed", False),
        "vfm_error": result.get("vfm_error", error),
        "notes": (
            f"{entry.get('notes', '')}；终点判定：{result.get('end_event_label', 'UNKNOWN')}"
            if not error
            else error
        ),
    }


def _write_batch_report(path: Path, rows: list[dict], output_root: Path) -> None:
    completed = [row for row in rows if row["status"] == "VFM_READY"]
    diagnostic = [row for row in rows if row["status"] == "DIAGNOSTIC_ONLY"]
    data_limited = [row for row in rows if row["status"] == "DATA_LIMITED"]
    preload_only = [row for row in rows if row["status"] == "PRELOAD_RELEASE_ONLY"]
    unresolved = [row for row in rows if row["status"] == "UNRESOLVED"]
    errors = [row for row in rows if row["status"] == "INPUT_ERROR"]
    lines = [
        "# PA12 批量照片—力同步处理报告",
        "",
        "## 用户意图",
        "",
        "建立可重复的 PA12 单轴/双轴实验数据流程：以有效 DIC 照片为主索引，将 `Press` 力数据按同一照片时间轴插值，生成正拉伸力 CSV、名义应力—应变审核结果和 MatchID VFM 准备索引。后续 GPT 应先读取本报告和批量清单，再继续做 DIC 全场导出、边界力和 VFM 参数接入。",
        "",
        "## 本批次规则",
        "",
        "- 当前正式图像来源固定为 `vertical_all_45°/PAPER`；`CHECK` 和早期 `orginal_all` 不作为本批次正式输入。",
        "- `Press` 是力；等双轴默认 `X=(X1_Press+X2_Press)/2`，`Y=(Y1_Press+Y2_Press)/2`。",
        "- 零点校正后按拉伸正值输出：`F_corrected = -(F_raw - F_baseline)`；主动加载方向首行外必须为正，单轴非加载方向可为零。",
        "- X/Y 使用同一组照片时间点插值；当前 VFM 力值候选需照片、X、Y 行数完全相等。",
        "- 主索引是同名 JPG+DAT 配对帧；稀疏 DAT 的帧号缺口记录为未导出帧，不补造连续帧。",
        "- 原始 JPG、DAT、XLS 未修改；所有新增结果写入当前 Second Brain 仓库的 `Agents/PA12实验数据处理/`。",
        "- 正式 VFM 力值候选要求：时间严格递增、无 NaN、首行归零、照片/X/Y 数量一致、加载/断裂事件已确定；单轴非加载方向明确置零，主动方向首行外严格为正。",
        "- 实际相机频率按有效首尾照片帧号差除以有效实验时间计算；DAT 稀疏时，配对帧数只决定 VFM 行数，不冒充相机频率。",
        "- 设备位移按两侧位置增量绝对值之和计算；旋转目录中的 0.2/2/20 按两侧相对加载速度记录，力文件名中的 0.1/1/10 按单个执行通道速度解释。",
        "- 概览中的“照片位移”是加载速度×有效时间的独立推算值；“力位移”来自 XLS 的 Pos 设备通道。当前尚未从 DAT 全场字段得到独立 DIC 位移。",
        "- 已生成名义应力—应变表和曲线图；当前使用中心有效宽度 30 mm、中心厚度 1 mm、名义截面积 30 mm²、标距 30 mm；整体厚度 3 mm 只作几何记录，厚度和标距仍需实验确认。",
        "- 这些 CSV 只代表同步后的力值，不代表已经完成 DIC 全场解析、VFM 边界力建模或材料参数识别。",
        "",
        "## 状态统计",
        "",
        f"- 正式 VFM：{len(completed)} 个。",
        f"- 诊断结果：{len(diagnostic)} 个。",
        f"- 数据受限但已生成诊断结果：{len(data_limited)} 个。",
        f"- 预载释放记录：{len(preload_only)} 个。",
        f"- 输入未解决：{len(unresolved)} 个。",
        f"- 处理错误或未检测到事件：{len(errors)} 个。",
        "",
        "## 正式 VFM 已完成",
        "",
    ]
    lines += [
        f"- `{row['experiment_id']}`：照片 `{row['photo_count']}`，有效时间 `{row['effective_time']}` s，位移 `{row['photo_displacement']}` mm，VFM={'允许' if row['vfm_allowed'] else '禁止'}。"
        for row in completed
    ] or ["- 无。"]
    lines += ["", "## 已完成诊断但禁止正式 VFM", ""]
    lines += [
        f"- `{row['experiment_id']}`：照片 `{row['photo_count']}`，有效时间 `{row['effective_time']}` s；原因：{row['vfm_error'] or row['notes'] or 'UNKNOWN'}。"
        for row in diagnostic
    ] or ["- 无。"]
    lines += ["", "## 数据受限但已生成诊断结果", ""]
    lines += [
        f"- `{row['experiment_id']}`：照片 `{row['photo_count']}`，有效时间 `{row['effective_time']}` s；终点={row.get('end_event_label', 'UNKNOWN')}；原因：{row['vfm_error'] or row['notes'] or 'UNKNOWN'}。"
        for row in data_limited
    ] or ["- 无。"]
    lines += ["", "## 未完成", ""]
    for row in preload_only:
        lines.append(f"- `{row['experiment_id']}`：已确定为预载释放记录，不作为完整拉伸实验；{row['notes'] or '不生成正式 VFM。'}")
    for row in unresolved + errors:
        lines.append(f"- `{row['experiment_id']}`：{row['notes'] or row['vfm_error'] or 'UNKNOWN'}")
    if not unresolved and not errors:
        lines.append("- 无。")
    lines += [
        "",
        "## 输出位置",
        "",
        f"- 批量清单：`{output_root / 'Agents/PA12实验数据处理/处理记录/PA12批量处理清单.csv'}`",
        f"- 批量 JSON：`{output_root / 'Agents/PA12实验数据处理/处理记录/PA12批量处理清单.json'}`",
        f"- 汇总概览：`{output_root / 'Agents/PA12实验数据处理/实验概览/PA12实验概览_汇总.csv'}`",
        f"- 汇总概览 Excel：`{output_root / 'Agents/PA12实验数据处理/实验概览/PA12实验概览_汇总.xlsx'}`",
        f"- 输出审计报告：`{output_root / 'Agents/PA12实验数据处理/处理记录/PA12数据合理性审计报告.md'}`",
        f"- 输出审计 JSON：`{output_root / 'Agents/PA12实验数据处理/处理记录/PA12数据合理性审计结果.json'}`",
        "",
        "## MatchID 下一步",
        "",
        "1. 先审核每个实验检查图和应力—应变图中的加载起点、峰值、掉载点、线性段和屈服候选。",
        "2. 对诊断状态实验确认单轴非加载方向的 MatchID 边界表示；对 S23/S24 人工确认起止力索引。",
        "3. 使用 `MatchID_VFM准备/` 中的实验级索引和帧—力—时间索引，沿用已由 MatchID 2D 19.2.2.0 Results Viewer 在当前版本本地交叉验证的字段、单位和坐标约定；更换版本时重新复核。",
        "4. 基准使用 MatchID 自带 VFM；外围机器力按用户确认直接作为中心 ROI 边界合力输入，中心 ROI 厚度 1 mm，外围结构厚度 3 mm。",
        "5. 所有双轴均为等双轴；按 0.2、2、20 mm/s 分速率识别。阶段 1 固定 ν=0.375 识别 E，阶段 2 固定 E、ν 识别 Y、H。",
        "6. 进入 VFM 前使用 `MatchID_VFM准备/PA12等双轴VFM当前检查结果.md` 核对 ROI、方向、逐帧力、首帧、末帧和数量；识别后核对内外虚功、参数边界与残差。",
        "7. 批量处理后运行 `python tools/audit_pa12_outputs.py --config configs/pa12_rotated_batch.json`，把审计报告作为下一次 GPT 的机器可读检查入口。",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_batch(config_path: Path) -> dict:
    batch = json.loads(config_path.read_text(encoding="utf-8"))
    output_root = Path(batch["output_root"])
    rows: list[dict] = []
    overview_rows: list[dict] = []

    for entry in batch["experiments"]:
        if entry.get("status") in {"UNRESOLVED", "PRELOAD_RELEASE_ONLY"}:
            rows.append(_manifest_row(entry, status=entry["status"]))
            overview_rows.append(
                {
                    "速度": (
                        f"{float(entry['loading_speed']):g} mm/s"
                        if "loading_speed" in entry
                        else "UNKNOWN"
                    ),
                    "照片数量": "UNKNOWN",
                    "设置频率": (
                        f"{float(entry['camera_setting_fps']):g} Hz"
                        if "camera_setting_fps" in entry
                        else "UNKNOWN"
                    ),
                    "实际频率": "UNKNOWN",
                    "照片位移": "UNKNOWN",
                    "力数量": "UNKNOWN",
                    "力位移": "UNKNOWN",
                    "力数据时间": "UNKNOWN",
                    "力传感频率": "UNKNOWN",
                }
            )
            continue
        config = dict(batch.get("defaults", {}))
        config.update(entry)
        config["output_root"] = str(output_root)
        try:
            result = process_experiment(config)
            if result["vfm_allowed"]:
                status = "VFM_READY"
            elif entry.get("status") == "DATA_LIMITED":
                status = "DATA_LIMITED"
            else:
                status = "DIAGNOSTIC_ONLY"
            rows.append(_manifest_row(entry, status=status, result=result))
            if result.get("overview_row"):
                overview_rows.append(result["overview_row"])
        except Exception as exc:
            rows.append(_manifest_row(entry, status="INPUT_ERROR", error=f"{type(exc).__name__}: {exc}"))

    record_root = output_root / "Agents" / "PA12实验数据处理" / "处理记录"
    overview_root = output_root / "Agents" / "PA12实验数据处理" / "实验概览"
    manifest_csv = record_root / "PA12批量处理清单.csv"
    manifest_json = record_root / "PA12批量处理清单.json"
    overview_csv = overview_root / "PA12实验概览_汇总.csv"
    overview_xlsx = overview_root / "PA12实验概览_汇总.xlsx"
    report_path = record_root / "PA12批量处理报告.md"
    _write_csv(manifest_csv, rows, MANIFEST_FIELDS)
    manifest_json.parent.mkdir(parents=True, exist_ok=True)
    manifest_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_csv(overview_csv, overview_rows, OVERVIEW_FIELDS)
    pd.DataFrame(overview_rows, columns=OVERVIEW_FIELDS).to_excel(overview_xlsx, index=False)
    _write_batch_report(report_path, rows, output_root)
    return {
        "rows": rows,
        "manifest_csv": str(manifest_csv),
        "manifest_json": str(manifest_json),
        "overview_csv": str(overview_csv),
        "overview_xlsx": str(overview_xlsx),
        "report": str(report_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="PA12 批量照片—力同步与 VFM 生成")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run_batch(args.config), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
