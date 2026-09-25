from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def _read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_summary(path: Path) -> dict[str, dict[str, str]]:
    if not path.is_file():
        return {}
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return {row["实验编号"]: row for row in csv.DictReader(handle)}


def _force_status(row: dict) -> str:
    if row.get("visual_fracture_confirmed") and row.get("force_missing_at_visual_fracture"):
        return "FORCE_SYNC_VISUAL_FRACTURE_FORCE_MISSING"
    status = row.get("status")
    if status == "VFM_READY" and row.get("vfm_allowed") is True:
        return "FORCE_SYNC_READY"
    if status == "DATA_LIMITED":
        return "FORCE_SYNC_DIAGNOSTIC"
    if status == "PRELOAD_RELEASE_ONLY":
        return "FORCE_SYNC_PRELOAD_RELEASE_ONLY"
    if status == "UNRESOLVED":
        return "FORCE_SYNC_UNRESOLVED"
    return "FORCE_SYNC_NOT_READY"


def build_closure_status(config_path: Path) -> dict:
    batch = _read_json(config_path)
    output_root = Path(batch["output_root"])
    agent_root = output_root / "Agents" / "PA12实验数据处理"
    record_root = agent_root / "处理记录"
    preparation_root = agent_root / "MatchID_VFM准备"
    manifest = {
        row["experiment_id"]: row
        for row in _read_json(record_root / "PA12批量处理清单.json")
    }
    dat_audit_path = preparation_root / "PA12_DIC_DAT质量审计.json"
    dat_rows = _read_json(dat_audit_path) if dat_audit_path.is_file() else []
    dat_by_experiment: dict[str, list[dict]] = {}
    for row in dat_rows:
        dat_by_experiment.setdefault(row["实验编号"], []).append(row)
    summary = _read_summary(preparation_root / "PA12_MatchID_VFM实验级索引.csv")

    experiments: list[dict] = []
    for entry in batch["experiments"]:
        experiment_id = entry["experiment_id"]
        force = manifest.get(experiment_id, {})
        rows = dat_by_experiment.get(experiment_id, [])
        dat_counts = Counter(row["status"] for row in rows)
        if not rows:
            dic_status = "DIC_NOT_INDEXED"
        elif dat_counts["DIC_FIELDS_AVAILABLE"] == len(rows):
            dic_status = "DIC_DAT_READY"
        else:
            dic_status = "DIC_DAT_INCOMPLETE"
        summary_row = summary.get(experiment_id, {})
        job_missing = int(summary_row.get("Job缺少有效帧数", "0") or 0)
        job_status = "JOB_COVERAGE_COMPLETE" if job_missing == 0 else "JOB_COVERAGE_REVIEW_REQUIRED"
        merged_status_path = preparation_root / experiment_id / f"{experiment_id}_DIC全场—力状态.json"
        merged_payload = _read_json(merged_status_path) if merged_status_path.is_file() else {}
        merged_status = merged_payload.get("status", "EXPORT_NOT_RUN")
        selected_frame_count = len(rows)
        dic_usable_frame_count = dat_counts["DIC_FIELDS_AVAILABLE"]
        if merged_status == "MATCHID_VFM_INPUT_READY":
            selected_frame_count = int(merged_payload["frame_count"])
            dic_usable_frame_count = selected_frame_count
        force_status = _force_status(force)
        if force_status == "FORCE_SYNC_PRELOAD_RELEASE_ONLY":
            overall_status = "PRELOAD_RELEASE_ONLY"
        elif force_status != "FORCE_SYNC_READY":
            overall_status = "FORCE_REVIEW_REQUIRED"
        elif dic_status == "DIC_DAT_INCOMPLETE":
            overall_status = "DIC_DAT_REVIEW_REQUIRED"
        elif dic_status == "DIC_NOT_INDEXED":
            overall_status = "DIC_INDEX_REQUIRED"
        elif merged_status == "MATCHID_VFM_INPUT_READY":
            overall_status = "MATCHID_VFM_INPUT_READY"
        elif merged_status == "EXPORT_INVALID":
            overall_status = "EXPORT_INVALID"
        else:
            overall_status = "EXPORT_REQUIRED"
        experiments.append(
            {
                "experiment_id": experiment_id,
                "force_status": force_status,
                "dic_status": dic_status,
                "job_status": job_status,
                "export_status": merged_status,
                "overall_status": overall_status,
                "selected_frame_count": selected_frame_count,
                "dic_usable_frame_count": dic_usable_frame_count,
                "dic_unusable_frame_count": selected_frame_count - dic_usable_frame_count,
                "dic_status_counts": dict(dat_counts),
                "job_missing_frame_count": job_missing,
            }
        )
    return {
        "config": str(config_path),
        "experiments": experiments,
        "status_counts": dict(Counter(row["overall_status"] for row in experiments)),
        "formal_matchid_vfm_ready": all(
            row["overall_status"] == "MATCHID_VFM_INPUT_READY" for row in experiments
        ),
    }


def _write_markdown(path: Path, status: dict) -> None:
    lines = [
        "# PA12 MatchID VFM 闭环状态",
        "",
        "本文件把同步力值、DAT 全场记录、Job 覆盖和 Results Viewer 导出分开判断。同步力值通过不等于 MatchID VFM 输入已经完成。",
        "",
        f"- 正式 MatchID VFM 输入已闭合：`{'是' if status['formal_matchid_vfm_ready'] else '否'}`",
        "",
        "| 实验 | 力值状态 | DAT 状态 | Job 状态 | 导出状态 | 当前状态 | 选定帧 | DAT 可用帧 | DAT 不可用帧 |",
        "| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: |",
    ]
    for row in status["experiments"]:
        lines.append(
            f"| {row['experiment_id']} | {row['force_status']} | {row['dic_status']} | {row['job_status']} | {row['export_status']} | {row['overall_status']} | {row['selected_frame_count']} | {row['dic_usable_frame_count']} | {row['dic_unusable_frame_count']} |"
        )
    lines += [
        "",
        "## 状态含义",
        "",
        "- `FORCE_SYNC_READY`：照片—力同步 CSV 已通过当前力值契约。",
        "- `FORCE_SYNC_VISUAL_FRACTURE_FORCE_MISSING`：照片已确认视觉断裂，但力文件在断裂前结束；不能补造断裂力或发布正式 VFM。",
        "- `DIC_DAT_READY`：选定 DAT 均含 `<18>` 和 `<53>` 记录；逐字段映射已由同版本 Results Viewer 与同帧 DAT 交叉验证，映射写在各实验元数据 JSON。",
        "- `JOB_COVERAGE_REVIEW_REQUIRED`：当前 Job 未覆盖全部选定照片，需要在 Results Viewer 重新导出或确认覆盖。",
        "- `EXPORT_REQUIRED`：缺少导出且对应 DAT 不能重构，或仍有缺失帧；不能生成正式合并索引。",
        "- `EXPORT_INVALID`：导出和对应 DAT 都不能满足字段契约，或 DAT 无法重构；不能填零、插值或静默删点。",
        "- `MATCHID_VFM_INPUT_READY`：逐帧导出 CSV 或 DAT 重构结果已按声明字段、单位和同步力合并；这仍不是材料参数识别完成。",
        "",
        "## 旋转后 VFM 边界约定",
        "",
        "- 原始机器右上/左下为 `Y1/Y2`，右下/左上为 `X1/X2`；正式旋转 DIC 的边界映射为：顶部=`X2`、底部=`X1`、左侧=`Y2`、右侧=`Y1`。",
        "- MatchID Boundary 顺序固定为 `0=顶部、1=左侧、2=右侧、3=底部`；双轴使用 X 顶/底、Y 左/右，单轴只使用受力方向两边；拉伸力为正。",
        "- 外围夹持/加载结构厚度记录为 `3 mm`；中心 ROI 完全位于 `1 mm` 减薄区，MatchID 工程厚度用 `1 mm`。用户确认外围机器力传感器读数直接作为 ROI 边界合力输入 MatchID 自带 VFM。",
        "- 所有当前双轴均为等双轴，按 `0.2、2、20 mm/s` 分速率识别；不要求非等双轴路径，也不恢复四边牵引分布。",
        "- 阶段 1 固定 `ν=0.375` 识别 `E`；阶段 2 固定该 `E、ν` 识别屈服 `Y` 与硬化 `H`。闭环状态通过不等于 VFM 参数识别完成。",
        "",
        "## 下一步",
        "",
        "1. 先处理 `FORCE_REVIEW_REQUIRED`、`DIC_DAT_REVIEW_REQUIRED` 和 `JOB_COVERAGE_REVIEW_REQUIRED`。",
        "2. 检查各实验合并状态中的 `DIC数据来源`、`DAT原始点数` 和 `排除无效点数`；确认 `DAT_RECONSTRUCTED` 仅排除了 DAT 明确标记为无效的点。",
        "3. 对 `EXPORT_REQUIRED`、`EXPORT_INVALID` 和 `DIC_DAT_REVIEW_REQUIRED` 的实验回到 MatchID 处理，不能用力值数量相等代替 DIC 全场完整性。",
        "4. 先按等双轴 VFM 当前检查结果核对 ROI 位置/尺寸、厚度、旋转后 XY、逐帧力同步、首帧零力和断裂/末帧对应；MatchID 参考图若为加载前零力帧，应单独核对其帧序映射。",
        "5. 每个速度分开运行 MatchID 自带 VFM；记录内外虚功、残差、参数是否撞界和收敛状态。没有数值输出的字段写未识别/未计算。",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_closure_outputs(config_path: Path) -> dict:
    status = build_closure_status(config_path)
    output_root = Path(_read_json(config_path)["output_root"])
    preparation_root = output_root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
    json_path = preparation_root / "PA12_MatchID_VFM闭环状态.json"
    markdown_path = preparation_root / "PA12_MatchID_VFM闭环状态.md"
    preparation_root.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_markdown(markdown_path, status)
    return {"json": str(json_path), "markdown": str(markdown_path), **status}


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 PA12 MatchID VFM 闭环状态")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    result = write_closure_outputs(args.config)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["formal_matchid_vfm_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
