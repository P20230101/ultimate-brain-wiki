from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

if __package__:
    from .matchid_dic import (
        audit_dat_rows,
        classify_dat_point_count_anomalies,
        inspect_dat_file,
    )
else:
    from matchid_dic import audit_dat_rows, classify_dat_point_count_anomalies, inspect_dat_file


def extract_matchid_dat_metadata(dat_path: Path) -> dict:
    metadata = inspect_dat_file(dat_path)
    metadata.update(
        {
            "raw_field_semantics_confirmed": True,
            "raw_field_map": {
                "x": "field[1] + field[5]",
                "y": "field[2] + field[6]",
                "u": "field[7]",
                "v": "field[8]",
                "x_pixels": "<18> field[1] + field[5]",
                "y_pixels": "<18> field[2] + field[6]",
                "x_mm": "x_pixels × <11>",
                "y_mm": "y_pixels × <11>",
                "u_mm": "<18> field[7] × <11>",
                "v_mm": "<18> field[8] × <11>",
                "r": "<18> field[13]",
                "sigma": "<18> field[14]",
                "valid": "<53> field[1]",
                "exx": "<53> field[2]",
                "eyy": "<53> field[3]",
                "exy": "<53> field[4]",
                "e1": "<53> field[5]",
                "e2": "<53> field[6]",
                "gamma": "<53> field[7]",
            },
            "raw_field_note": (
                "已通过同版本 MatchID 2D 19.2.2.0 Results Viewer CSV 与同帧 DAT 交叉验证；"
                "这是本地数据验证，不是官方 DAT 格式文档。"
            ),
        }
    )
    return metadata


def _job_tags(text: str) -> dict[str, list[str]]:
    tags: dict[str, list[str]] = {}
    for key, value in re.findall(r"<([^>]+)>=<([^>]*)>", text):
        tags.setdefault(key, []).append(value)
    return tags


def parse_job_metadata(job_path: Path) -> dict:
    text = job_path.read_text(encoding="utf-8", errors="replace")
    tags = _job_tags(text)
    export_unit = tags.get("Export$unit", [None])[0]
    unit_name = {"0": "pixels", "1": "mm"}.get(export_unit, export_unit)
    deformed_images = [Path(value.split(";", 1)[0]).name for value in tags.get("Deformed$image", [])]
    return {
        "path": str(job_path),
        "reference_image": tags.get("Reference$image", [None])[0],
        "deformed_image_count": len(tags.get("Deformed$image", [])),
        "deformed_images": deformed_images,
        "conversion_mm_per_pixel": float(tags["Conversion"][0]) if tags.get("Conversion") else None,
        "export_unit": unit_name,
        "export_format": tags.get("Export$format", [None])[0],
        "delimiter": tags.get("Delimiter", [None])[0],
        "shape": tags.get("Shape", [None])[0],
        "strain_convention": tags.get("Strain$convention", [None])[0],
        "strain_interpolation": tags.get("Strain$interpolation", [None])[0],
        "subset_size": tags.get("Subset$size", [None])[0],
        "step_size": tags.get("Step$size", [None])[0],
        "automatic_export": tags.get("Automatic$export", [None])[0],
    }


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_dat_audit_report(path: Path, audits: list[dict]) -> None:
    status_counts: dict[str, int] = {}
    for row in audits:
        status = row["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    unusable = [row for row in audits if row["status"] != "DIC_FIELDS_AVAILABLE"]
    lines = [
        "# PA12 DAT 逐帧质量审计",
        "",
        "本报告审计同一照片索引下的 `.jpg.dat` 文件是否存在及是否包含 MatchID 记录。字段映射已通过同版本 MatchID 2D 19.2.2.0 Results Viewer 与同帧 DAT 交叉验证；这不是官方 DAT 格式文档。",
        "",
        "## 状态统计",
        "",
    ]
    lines.extend(f"- `{status}`：`{count}` 帧。" for status, count in sorted(status_counts.items()))
    lines += ["", "## 不可直接进入 DIC 全场合并的帧", ""]
    if unusable:
        lines.extend(
            f"- `{row['实验编号']}/{row['照片']}`：`{row['status']}`；记录数 `<18>/<53>` = `{row['record_counts']['18']}/{row['record_counts']['53']}`。"
            for row in unusable
        )
    else:
        lines.append("- 无。")
    lines += [
        "",
        "## 判定边界",
        "",
        "- `DIC_FIELDS_AVAILABLE` 表示 `<18>` 和 `<53>` 均有记录；逐字段映射以各实验元数据 JSON 的 `dat.raw_field_map` 为准。",
        "- `Job` 中是否列出照片单独记录；Job 缺帧不能覆盖 DAT 的实际记录状态。",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_matchid_preparation(config_path: Path) -> dict:
    batch = json.loads(config_path.read_text(encoding="utf-8"))
    output_root = Path(batch["output_root"])
    agent_root = output_root / "Agents" / "PA12实验数据处理"
    preparation_root = agent_root / "MatchID_VFM准备"
    record_root = agent_root / "处理记录"
    manifest_path = record_root / "PA12批量处理清单.json"
    manifest = {
        row["experiment_id"]: row
        for row in json.loads(manifest_path.read_text(encoding="utf-8"))
    }
    summary_rows: list[dict] = []
    index_paths: list[str] = []
    all_dat_audits: list[dict] = []

    for entry in batch["experiments"]:
        experiment_id = entry["experiment_id"]
        image_folder = Path(entry["image_folder"])
        job_value = entry.get("dic_job_file")
        job_path = Path(job_value) if job_value else image_folder / "Job.m2inp"
        job_metadata = parse_job_metadata(job_path)
        paired = sorted(
            [path for path in image_folder.glob("*.jpg") if (image_folder / f"{path.name}.dat").is_file()],
            key=lambda path: path.name,
        )
        dat_metadata = extract_matchid_dat_metadata(image_folder / f"{paired[0].name}.dat") if paired else {}
        result = manifest[experiment_id]
        match_path = agent_root / "照片力匹配" / f"{experiment_id}_照片-力对应表.csv"
        frame_index_path = preparation_root / f"{experiment_id}_帧—力—时间索引.csv"
        if match_path.is_file():
            with match_path.open("r", newline="", encoding="utf-8-sig") as handle:
                match_rows = list(csv.DictReader(handle))
            index_rows = []
            for row in match_rows:
                image_name = row["照片"]
                index_rows.append(
                    {
                        "照片": image_name,
                        "DAT": f"{image_name}.dat",
                        "时间/s": row.get("时间/s", ""),
                        "X向力/N": row.get("X向力/N", ""),
                        "Y向力/N": row.get("Y向力/N", ""),
                        "JPG原始路径": str(image_folder / image_name),
                        "DAT原始路径": str(image_folder / f"{image_name}.dat"),
                    }
                )
            _write_csv(
                frame_index_path,
                index_rows,
                ["照片", "DAT", "时间/s", "X向力/N", "Y向力/N", "JPG原始路径", "DAT原始路径"],
            )
            index_paths.append(str(frame_index_path))
        selected_names = [row["照片"] for row in match_rows] if match_path.is_file() else []
        dat_audits = audit_dat_rows(
            image_folder,
            [{"照片": name} for name in selected_names],
        )
        dat_audits = classify_dat_point_count_anomalies(dat_audits)
        for audit in dat_audits:
            audit["实验编号"] = experiment_id
        all_dat_audits.extend(dat_audits)
        dat_audit_path = preparation_root / f"{experiment_id}_DAT逐帧质量审计.csv"
        _write_csv(
            dat_audit_path,
            dat_audits,
            [
                "实验编号",
                "照片",
                "DAT",
                "status",
                "version",
                "conversion_mm_per_pixel",
                "point_count",
                "point_count_reference",
                "point_count_fraction",
                "record_counts",
                "error",
            ],
        )
        dat_status_counts: dict[str, int] = {}
        for audit in dat_audits:
            status = audit["status"]
            dat_status_counts[status] = dat_status_counts.get(status, 0) + 1
        dat_unusable = [
            audit["照片"]
            for audit in dat_audits
            if audit["status"] != "DIC_FIELDS_AVAILABLE"
        ]
        job_names = set(job_metadata["deformed_images"])
        missing_job_frames = [name for name in selected_names if name not in job_names]
        job_frame_coverage_complete = bool(selected_names) and not missing_job_frames
        metadata = {
            "experiment_id": experiment_id,
            "status": result["status"],
            "image_folder": str(image_folder),
            "job": job_metadata,
            "dat": dat_metadata,
            "paired_jpg_dat_count": len(paired),
            "excluded_frame_numbers": entry.get("excluded_frame_numbers", []),
            "excluded_frame_reason": entry.get("excluded_frame_reason", "无"),
            "force_match_table": str(match_path) if match_path.is_file() else None,
            "frame_force_index": str(frame_index_path) if frame_index_path.is_file() else None,
            "dat_quality_audit": {
                "path": str(dat_audit_path),
                "selected_frame_count": len(dat_audits),
                "status_counts": dat_status_counts,
                "usable_frame_count": dat_status_counts.get("DIC_FIELDS_AVAILABLE", 0),
                "unusable_frame_count": len(dat_unusable),
                "unusable_frames": dat_unusable,
            },
            "formal_vfm_allowed": result.get("vfm_allowed", False),
            "job_frame_coverage": {
                "selected_frame_count": len(selected_names),
                "job_deformed_image_count": len(job_names),
                "missing_selected_frame_count": len(missing_job_frames),
                "missing_selected_frames": missing_job_frames,
                "complete": job_frame_coverage_complete,
            },
            "field_semantics": {
                "Press": "X/Y力同步表已确认",
                "DAT_18_53": "已通过 MatchID 2D 19.2.2.0 Results Viewer 同帧交叉验证；映射见 dat.raw_field_map",
            },
        }
        metadata_path = preparation_root / f"{experiment_id}_DIC元数据.json"
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary_rows.append(
            {
                "实验编号": experiment_id,
                "状态": result["status"],
                "配对JPG-DAT数": len(paired),
                "有效帧数": result.get("photo_count", "UNKNOWN"),
                "起始照片": result.get("first_image", "UNKNOWN"),
                "结束照片": result.get("last_image", "UNKNOWN"),
                "DIC标定/mm/pixel": job_metadata.get("conversion_mm_per_pixel"),
                "DAT标定/mm/pixel": dat_metadata.get("conversion_mm_per_pixel"),
                "ROI": dat_metadata.get("roi_raw"),
                "DAT点数": dat_metadata.get("point_count"),
                "DAT<18>记录数": dat_metadata.get("record_counts", {}).get("18"),
                "DAT<53>记录数": dat_metadata.get("record_counts", {}).get("53"),
                "Job变形图数": job_metadata.get("deformed_image_count"),
                "Job覆盖有效帧": "完整" if job_frame_coverage_complete else "不完整",
                "Job缺少有效帧数": len(missing_job_frames),
                "DAT可用全场帧": dat_status_counts.get("DIC_FIELDS_AVAILABLE", 0),
                "DAT不可用帧": len(dat_unusable),
                "DAT质量审计": str(dat_audit_path),
                "帧力索引": str(frame_index_path) if frame_index_path.is_file() else "未生成",
                "DIC元数据": str(metadata_path),
                "原始Job": str(job_path),
                "备注": (
                    "；".join(
                        part
                        for part in [
                            "Job 未覆盖全部有效帧；需在 Results Viewer 重新导出缺失帧。"
                            if missing_job_frames
                            else "",
                            f"{len(dat_unusable)} 个选定 DAT 没有可用的 <18>/<53> 全场记录。"
                            if dat_unusable
                            else "",
                            (
                                "配置排除帧："
                                + ", ".join(f"{int(number):06d}.jpg" for number in entry["excluded_frame_numbers"])
                                + "；"
                                + str(entry.get("excluded_frame_reason", ""))
                            )
                            if entry.get("excluded_frame_numbers")
                            else "",
                            "DAT逐字段映射已由同版本 Results Viewer 与同帧 DAT 交叉验证；不是官方 DAT 格式文档。",
                        ]
                        if part
                    )
                ),
            }
        )

    summary_path = preparation_root / "PA12_MatchID_VFM实验级索引.csv"
    _write_csv(summary_path, summary_rows, list(summary_rows[0]))
    dat_audit_csv = preparation_root / "PA12_DIC_DAT质量审计.csv"
    _write_csv(
        dat_audit_csv,
        all_dat_audits,
        [
            "实验编号",
            "照片",
            "DAT",
            "status",
            "version",
            "conversion_mm_per_pixel",
            "point_count",
            "point_count_reference",
            "point_count_fraction",
            "record_counts",
            "error",
        ],
    )
    dat_audit_json = preparation_root / "PA12_DIC_DAT质量审计.json"
    _write_json(dat_audit_json, all_dat_audits)
    dat_audit_report = preparation_root / "PA12_DIC_DAT质量审计.md"
    _write_dat_audit_report(dat_audit_report, all_dat_audits)
    instructions = [
        "# PA12 MatchID VFM 准备包",
        "",
        "## 用户意图",
        "",
        "后续把同一有效照片帧的 DIC 位移/应变场、同步的 X/Y 力、试样几何和边界载荷接入 MatchID VFM 模块，继续识别材料参数。当前包只完成输入索引和元数据核对，不宣称已经完成 VFM 识别。",
        "",
        "## 已生成",
        "",
        f"- 实验级索引：`{summary_path}`。",
        f"- 逐帧 DAT 质量审计：`{dat_audit_report}`、`{dat_audit_csv}`、`{dat_audit_json}`。",
        "- 环境检查：`MatchID_VFM准备/PA12_环境检查.md` 和 `PA12_环境检查.json`。",
        "- 闭环状态：`MatchID_VFM准备/PA12_MatchID_VFM闭环状态.md` 和 `PA12_MatchID_VFM闭环状态.json`。",
        "- 每个实验的 DIC 元数据 JSON：包含 Job 标定、ROI、DAT 点数、记录计数和输入路径。",
        "- 每个已完成同步实验的帧—力—时间索引：同一照片名对应同名 DAT、X/Y 力和同步时间。",
        "- 已增加 Job 覆盖和 DAT 逐帧有效性检查；Job 不覆盖或 DAT 没有 `<53>` 记录的帧不能直接当作已完成 DIC 全场输入。",
        "- 已用同版本 Results Viewer 交叉验证 DAT 字段映射；`valid=False` 的 `<53>` 点被明确排除，绝不填零或插值。",
        "",
        "## 原始方向与旋转后边界映射",
        "",
        "- 方向证据图片：`raw/assets/PA12原始方向与旋转标定方向.jpg`；可复用边界配置：`configs/pa12_vfm_boundary.json`；审计结果：`MatchID_VFM准备/PA12_VFM边界载荷审计.json`。",
        "- 原始机器右上/左下为 `Y1/Y2`，右下/左上为 `X1/X2`；正式旋转 DIC 的边界映射为：顶部=`X2`、底部=`X1`、左侧=`Y2`、右侧=`Y1`。",
        "- MatchID Boundary 顺序固定为 `0=顶部、1=左侧、2=右侧、3=底部`；双轴使用 X 顶/底、Y 左/右，单轴只使用受力方向两边；拉伸力为正。",
        "- 外围夹持/加载结构厚度记录为 `3 mm`；中心 ROI 必须完全位于 `1 mm` 减薄区，MatchID 工程厚度使用 `1 mm`；完整 S16 `.vfm` 只作为格式/方向证据。",
        "- 所有当前双轴试验均为等双轴；外围机器力按用户确认直接作为 ROI 边界合力输入 MatchID 自带 VFM；按 `0.2、2、20 mm/s` 分速率识别。",
        "- 参数策略：阶段 1 固定 `ν=0.375` 识别 `E`；阶段 2 固定该 `E、ν` 识别屈服 `Y` 和硬化 `H`。没有运行输出的参数写未识别/未计算。",
        "- 当前检查结果：`MatchID_VFM准备/PA12等双轴VFM当前检查结果.md/.csv`；记录 ROI/力同步/帧数及当前识别状态。",
        "",
        "## 已确认规则",
        "",
        "- 正式 DIC 来源只使用 `vertical_all_45°/PAPER`；不使用 `CHECK` 或 `orginal_all`。",
        "- `Press` 是力；等双轴默认 X/Y 各自取两条同向通道平均。",
        "- X/Y 力使用同一组有效照片时间轴插值。",
        "- DAT 原始文件保持不变；MatchID 可直接读取原 DAT。",
        "- 当前 Python 依赖和原始输入路径均可用；环境检查已发现 MatchID 2D 19.2.2.0，DAT 字段映射和标准导出列已完成当前版本本地同帧交叉验证；各实验仍需按闭环状态完成导出/重构。",
        "",
        "## 尚未确认",
        "",
        "- S15 正式 DIC/VFM 使用 `000001–000284.jpg`；`000285.jpg` 是视觉断裂帧，其 DAT 点数异常，不进入有效场；原始 JPG/DAT 保留。S22 有 8 个没有 `<53>` 的 DAT 帧，已排除出有效全场。",
        "- 需要逐步核验 ROI 在中心减薄区内的位置、1 mm MatchID 厚度、旋转后 XY 方向、参考帧/零力映射和逐帧力序列；用户已确认机器力直接作为 ROI 边界合力，不恢复四边牵引分布。",
        "- 厚度 3 mm、宽度 30 mm、标距 30 mm 当前只是名义应力—应变审核的工作参数。",
        "- 当前选定 DAT 逐帧审计结果必须先读 `PA12_DIC_DAT质量审计.md`；S22 的 8 个 `NO_STRAIN_RECORDS` 帧不能直接进入 DIC 全场合并。",
        "",
        "## 下一步操作顺序",
        "",
        "1. 保持所有实验使用与 S16 相同的 MatchID 2D 版本、导出列和单位；换版本时重新做同帧交叉验证。",
        "2. 对导出缺失、含 NaN 或点数与 DAT 不一致的帧，运行 `python tools/merge_matchid_exports.py`，程序会在 DAT 映射可用时重构并标记 `DAT_RECONSTRUCTED`。",
        "3. DAT 无 `<53>`、无法解析或缺失时，程序保持阻断并写出具体帧，不填零、不插值、不静默删点。",
        "4. 对等双轴各速度按当前检查结果核对 ROI、厚度、XY 方向、同步、首帧、末帧和数量，再使用 MatchID 自带 VFM；非等双轴数据不是前置要求。",
        "5. 每个速度分开运行参数识别，并记录内外虚功、残差、参数边界、收敛及识别区间。",
        "6. 每次继续工作前先运行 `python tools/audit_matchid_dic.py --config configs/pa12_rotated_batch.json`，以闭环状态 JSON 为机器判断入口。",
        "",
        "## 可复现命令",
        "",
        "```powershell",
        "python tools/matchid_prepare.py --config configs/pa12_rotated_batch.json",
        "```",
    ]
    instructions_path = preparation_root / "PA12_MatchID_VFM准备说明.md"
    instructions_path.write_text("\n".join(instructions) + "\n", encoding="utf-8")
    return {
        "summary": str(summary_path),
        "instructions": str(instructions_path),
        "frame_force_indexes": index_paths,
        "dat_audit_csv": str(dat_audit_csv),
        "dat_audit_json": str(dat_audit_json),
        "dat_audit_report": str(dat_audit_report),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 PA12 MatchID VFM 准备包")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build_matchid_preparation(args.config), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
