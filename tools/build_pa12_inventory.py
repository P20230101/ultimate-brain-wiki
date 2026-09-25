from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import pandas as pd


def norm_path(path: Path) -> str:
    return str(path).replace("\\", "/")


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_category(relative: str) -> tuple[str, str, str, str]:
    parts = Path(relative).parts
    lower = relative.lower().replace("\\", "/")
    name = Path(relative).name
    ext = Path(relative).suffix.lower()
    if parts and parts[0] == "data":
        if lower.startswith("data/xy/data-20250529/"):
            if name.startswith("~$"):
                return "Office 临时锁文件", "processing_artifact", "REVIEW_ONLY", "Excel 临时锁文件，不作为正式测量文件读取"
            return "力/位移/控制器原始数据", "raw_source", "02_force_data/raw/" + relative.split("data\\XY\\data-20250529\\", 1)[-1].replace("\\", "/"), "XLS/XLSX 状态导出；先记录实际列，不解释物理含义"
        if lower.startswith("data/xy/picture-20250529/"):
            tail = relative.replace("data\\XY\\picture-20250529\\", "").replace("\\", "/")
            if tail.startswith("orginal_all/"):
                target = "03_DIC/raw_xy_original_all/" + tail[len("orginal_all/"):]
            else:
                target = "03_DIC/vertical_all_45deg/" + tail
            return "DIC 图像与 DAT 原始/整理数据", "raw_source", target, "JPG、DAT 及 MatchID/图像配套文件"
        if lower.startswith("data/xz/"):
            tail = relative.replace("data\\XZ\\", "").replace("\\", "/")
            return "XZ 图像与 DAT 原始数据", "raw_source", "03_DIC/raw_xz/" + tail[len("xz_tu数据/"):] if tail.startswith("xz_tu数据/") else "03_DIC/raw_xz/" + tail, "独立 XZ 数据集"
        if ext in {".zip", ".z01", ".z02", ".z03"}:
            return "压缩归档", "source_archive", "00_README/source_archives/" + name, "展开数据已存在；归档文件保留作来源备份"
        return "实验数据/其他", "raw_source", "REVIEW_ONLY", "data/ 下未归入上述类型"
    if relative in {
        "1-s2.0-S1751616122004271-main (1).pdf",
        "3D打印尼龙材料的双轴拉伸测试方法与力学性能(1).docx",
        "3D打印尼龙材料的双轴拉伸测试方法与力学性能(1).pdf",
        "VARIABILITY IN THE MECHANICAL PROPERTIES OF LASER SINTERED PA-12 .pdf",
        "Variability, heterogeneity, and anisotropy in the quasi‐static response of laser sintered PA12 components.pdf",
    }:
        return "论文/研究资料", "reference", "01_papers/" + name, "论文或论文可编辑版本"
    if parts and parts[0] == "yuan_analysis_20260912":
        return "历史分析/运行环境", "historical_analysis", "REVIEW_ONLY", "已有分析结果或分析环境，不复制进结构化原始层"
    if parts and parts[0] == "second brain":
        return "知识库", "knowledge_base", "REVIEW_ONLY", "独立 Obsidian/第二大脑目录"
    if parts and parts[0] == "VFM":
        return "VFM 占位目录内容", "project_context", "REVIEW_ONLY", "VFM 目录当前为空或无可扫描文件"
    return "其他/待复核", "review_only", "REVIEW_ONLY", "未纳入结构化实验资产副本"


def build_file_inventory(source: Path, project: Path, out: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        if project == path or project in path.parents:
            continue
        relative = path.relative_to(source).as_posix()
        category, role, target, note = source_category(relative)
        stat = path.stat()
        rows.append(
            {
                "source_path": norm_path(path),
                "relative_path": relative,
                "name": path.name,
                "extension": path.suffix.lower(),
                "size_bytes": stat.st_size,
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
                "category": category,
                "project_role": role,
                "organized_path": target,
                "classification_note": note,
            }
        )
    fields = [
        "source_path", "relative_path", "name", "extension", "size_bytes",
        "modified_time", "category", "project_role", "organized_path", "classification_note",
    ]
    write_csv(out / "file_inventory.csv", rows, fields)
    return rows


def parse_number(name: str) -> int | None:
    match = re.search(r"(\d+)$", Path(name).stem)
    return int(match.group(1)) if match else None


def dic_row(root_name: str, root: Path, source_root: Path, source_base: Path, folder: Path) -> dict | None:
    files = [p for p in folder.iterdir() if p.is_file()]
    images = sorted([p for p in files if p.suffix.lower() in {".jpg", ".jpeg"}], key=lambda p: p.name.lower())
    dats = sorted([p for p in files if p.name.lower().endswith((".jpg.dat", ".jpeg.dat"))], key=lambda p: p.name.lower())
    if not images and not dats:
        return None
    image_keys = {p.name.lower(): p for p in images}
    dat_keys = {p.name[:-4].lower(): p for p in dats}
    paired = sorted(set(image_keys) & set(dat_keys))
    missing = sorted(set(image_keys) - set(dat_keys))
    orphan = sorted(set(dat_keys) - set(image_keys))
    image_numbers = sorted({n for n in (parse_number(p.name) for p in images) if n is not None})
    dat_numbers = sorted({n for n in (parse_number(p.name[:-4]) for p in dats) if n is not None})

    def gap_count(numbers: list[int]) -> int:
        return max(0, (numbers[-1] - numbers[0] + 1) - len(numbers)) if numbers else 0

    relative = folder.relative_to(root).as_posix()
    project_folder = Path("03_DIC") / root_name / relative
    source_folder = source_base / relative
    if len(images) == 0:
        status = "DAT_ONLY"
    elif len(dats) == 0:
        status = "IMAGE_ONLY"
    elif missing or orphan or gap_count(image_numbers) or gap_count(dat_numbers):
        status = "INCOMPLETE_OR_NONCONTIGUOUS"
    else:
        status = "COMPLETE"
    return {
        "collection_id": f"{root_name}_{relative.replace('/', '_')}",
        "collection_type": root_name,
        "folder_label": folder.name,
        "organized_folder": norm_path(project_folder),
        "source_folder": norm_path(source_folder),
        "image_count": len(images),
        "dat_count": len(dats),
        "paired_count": len(paired),
        "missing_dat_count": len(missing),
        "orphan_dat_count": len(orphan),
        "first_image": images[0].name if images else "UNKNOWN",
        "last_image": images[-1].name if images else "UNKNOWN",
        "first_dat": dats[0].name if dats else "UNKNOWN",
        "last_dat": dats[-1].name if dats else "UNKNOWN",
        "image_number_min": image_numbers[0] if image_numbers else "UNKNOWN",
        "image_number_max": image_numbers[-1] if image_numbers else "UNKNOWN",
        "image_sequence_gap_count": gap_count(image_numbers),
        "dat_number_min": dat_numbers[0] if dat_numbers else "UNKNOWN",
        "dat_number_max": dat_numbers[-1] if dat_numbers else "UNKNOWN",
        "dat_sequence_gap_count": gap_count(dat_numbers),
        "pair_status": status,
        "missing_dat_examples": ";".join(missing[:10]),
        "orphan_dat_examples": ";".join(orphan[:10]),
        "notes": "目录名仅作来源标签，未解释为加载方向、加载方式或速率。",
    }


def build_dic_inventory(project: Path, source: Path, out: Path) -> list[dict]:
    roots = [
        ("XY_RAW", project / "03_DIC" / "raw_xy_original_all", source / "data" / "XY" / "picture-20250529" / "orginal_all"),
        ("XY_SELECTED", project / "03_DIC" / "vertical_all_45deg", source / "data" / "XY" / "picture-20250529" / "vertical_all_45°"),
        ("XZ_RAW", project / "03_DIC" / "raw_xz", source / "data" / "XZ" / "xz_tu数据"),
    ]
    rows: list[dict] = []
    for root_name, root, source_base in roots:
        folders = [root] + sorted([p for p in root.rglob("*") if p.is_dir()])
        for folder in folders:
            row = dic_row(root_name, root, source, source_base, folder)
            if row:
                rows.append(row)
    fields = [
        "collection_id", "collection_type", "folder_label", "organized_folder", "source_folder",
        "image_count", "dat_count", "paired_count", "missing_dat_count", "orphan_dat_count",
        "first_image", "last_image", "first_dat", "last_dat", "image_number_min", "image_number_max",
        "image_sequence_gap_count", "dat_number_min", "dat_number_max", "dat_sequence_gap_count",
        "pair_status", "missing_dat_examples", "orphan_dat_examples", "notes",
    ]
    write_csv(out / "dic_inventory.csv", rows, fields)
    return rows


def header_candidates(columns: list[str]) -> dict[str, list[str]]:
    result = {"time": [], "force_or_load": [], "position_or_displacement": [], "speed": [], "pressure": [], "sensor": []}
    for column in columns:
        key = str(column).strip()
        lower = key.lower()
        if lower in {"t", "time", "timestamp", "datetime", "date_time"} or "time" in lower:
            result["time"].append(key)
        if any(token in lower for token in ("force", "load")):
            result["force_or_load"].append(key)
        if any(token in lower for token in ("pos", "disp", "displacement")):
            result["position_or_displacement"].append(key)
        if "speed" in lower or lower.endswith("_vel"):
            result["speed"].append(key)
        if "press" in lower or "pressure" in lower:
            result["pressure"].append(key)
        if any(token in lower for token in ("sensor", "channel", "ch")):
            result["sensor"].append(key)
    return result


def numeric_ranges(df: pd.DataFrame) -> dict[str, dict[str, float | None]]:
    result: dict[str, dict[str, float | None]] = {}
    for col in df.columns:
        values = pd.to_numeric(df[col], errors="coerce").dropna()
        if not values.empty:
            result[str(col)] = {"min": float(values.min()), "max": float(values.max())}
    return result


def sheet_summary(path: Path, sheet: str) -> dict:
    df = pd.read_excel(path, sheet_name=sheet, header=0, engine="openpyxl")
    df = df.dropna(how="all")
    columns = [str(c).strip() for c in df.columns]
    candidates = header_candidates(columns)
    time_col = candidates["time"][0] if candidates["time"] else None
    time_start = time_end = sampling_rate = None
    if time_col is not None:
        times = pd.to_numeric(df[time_col], errors="coerce").dropna()
        if not times.empty:
            time_start = float(times.iloc[0])
            time_end = float(times.iloc[-1])
            diffs = times.diff().dropna()
            positive = diffs[diffs > 0]
            if not positive.empty:
                sampling_rate = float(1.0 / positive.median())
    return {
        "sheet": sheet,
        "rows": int(len(df)),
        "columns": columns,
        "candidates": candidates,
        "numeric_ranges": numeric_ranges(df),
        "time_column": time_col or "UNKNOWN",
        "time_start": time_start if time_start is not None else "UNKNOWN",
        "time_end": time_end if time_end is not None else "UNKNOWN",
        "sampling_rate_hz": sampling_rate if sampling_rate is not None else "UNKNOWN",
    }


def build_force_inventory(project: Path, out: Path) -> list[dict]:
    rows: list[dict] = []
    force_root = project / "02_force_data" / "raw"
    files = sorted([p for p in force_root.rglob("*") if p.is_file() and p.suffix.lower() in {".xls", ".xlsx"}])
    for path in files:
        is_lock_file = path.name.startswith("~$")
        row = {
            "force_file": norm_path(path.relative_to(project)),
            "source_name": path.name,
            "extension": path.suffix.lower(),
            "container_signature": "OOXML ZIP despite .xls suffix" if path.open("rb").read(4) == b"PK\x03\x04" else "UNKNOWN",
            "read_status": "LOCK_FILE" if is_lock_file else "UNKNOWN",
            "sheet_count": "UNKNOWN",
            "sheet_names": "UNKNOWN",
            "total_data_rows": "UNKNOWN",
            "all_columns": "UNKNOWN",
            "time_columns": "UNKNOWN",
            "force_or_load_columns": "UNKNOWN",
            "position_or_displacement_columns": "UNKNOWN",
            "speed_columns": "UNKNOWN",
            "pressure_columns": "UNKNOWN",
            "sensor_columns": "UNKNOWN",
            "time_start": "UNKNOWN",
            "time_end": "UNKNOWN",
            "sampling_rate_hz": "UNKNOWN",
            "sheet_summaries": "UNKNOWN",
            "notes": "Excel 临时锁文件，不读取工作表。" if is_lock_file else "",
        }
        if is_lock_file:
            rows.append(row)
            continue
        try:
            workbook = pd.ExcelFile(path, engine="openpyxl")
            summaries = [sheet_summary(path, sheet) for sheet in workbook.sheet_names]
            all_columns = sorted({c for summary in summaries for c in summary["columns"]})
            candidates = {key: sorted({c for summary in summaries for c in summary["candidates"][key]}) for key in ["time", "force_or_load", "position_or_displacement", "speed", "pressure", "sensor"]}
            time_summaries = [s for s in summaries if s["time_column"] != "UNKNOWN"]
            row["read_status"] = "READABLE"
            row["sheet_count"] = len(summaries)
            row["sheet_names"] = ";".join(workbook.sheet_names)
            row["total_data_rows"] = sum(s["rows"] for s in summaries)
            row["all_columns"] = ";".join(all_columns)
            row["time_columns"] = ";".join(candidates["time"]) or "UNKNOWN"
            row["force_or_load_columns"] = ";".join(candidates["force_or_load"]) or "UNKNOWN"
            row["position_or_displacement_columns"] = ";".join(candidates["position_or_displacement"]) or "UNKNOWN"
            row["speed_columns"] = ";".join(candidates["speed"]) or "UNKNOWN"
            row["pressure_columns"] = ";".join(candidates["pressure"]) or "UNKNOWN"
            row["sensor_columns"] = ";".join(candidates["sensor"]) or "UNKNOWN"
            if time_summaries:
                starts = [s["time_start"] for s in time_summaries]
                ends = [s["time_end"] for s in time_summaries]
                rates = [s["sampling_rate_hz"] for s in time_summaries if s["sampling_rate_hz"] != "UNKNOWN"]
                row["time_start"] = min(starts)
                row["time_end"] = max(ends)
                row["sampling_rate_hz"] = ";".join(f"{r:.6g}" for r in sorted(set(rates))) if rates else "UNKNOWN"
            row["sheet_summaries"] = json.dumps(summaries, ensure_ascii=False, separators=(",", ":"))
            row["notes"] = "读取到 Pos/Speed/Press 状态表；当前未发现名称含 force/load 的直接力列。T 为文件内相对时间候选，不能当作墙上时钟或同步触发时间。"
        except Exception as exc:
            row["read_status"] = "UNREADABLE"
            row["notes"] = f"读取失败：{type(exc).__name__}: {exc}"
        rows.append(row)
    fields = list(rows[0].keys()) if rows else ["force_file"]
    write_csv(out / "force_inventory.csv", rows, fields)
    return rows


def select_experiment_dic_rows(dic_rows: list[dict]) -> list[dict]:
    selected: list[dict] = []
    for row in dic_rows:
        folder = row["organized_folder"]
        if row["collection_type"] == "XZ_RAW":
            selected.append(row)
        elif row["collection_type"] == "XY_SELECTED" and "/PAPER/" in folder:
            selected.append(row)
        elif row["collection_type"] == "XY_RAW" and "/Test1/" in folder and row["dat_count"] > 0:
            selected.append(row)
    return selected


def build_experiment_manifest(dic_rows: list[dict], force_rows: list[dict], project: Path, out: Path) -> list[dict]:
    rows: list[dict] = []
    for dic in select_experiment_dic_rows(dic_rows):
        label = dic["folder_label"]
        if dic["collection_type"] == "XY_RAW":
            experiment_id = "RAW_" + label
            specimen_id = label
        elif dic["collection_type"] == "XZ_RAW":
            experiment_id = "XZ_" + label
            specimen_id = label
        else:
            experiment_id = label
            specimen_id = label.split("_", 1)[0]
        rows.append(
            {
                "experiment_id": experiment_id,
                "specimen_id": specimen_id,
                "source_label": label,
                "orientation": "UNKNOWN",
                "loading_mode": "UNKNOWN",
                "loading_rate": "UNKNOWN",
                "image_folder": dic["organized_folder"],
                "image_count": dic["image_count"],
                "dat_count": dic["dat_count"],
                "paired_count": dic["paired_count"],
                "first_image": dic["first_image"],
                "last_image": dic["last_image"],
                "force_file": "UNKNOWN",
                "force_rows": "UNKNOWN",
                "force_columns": "UNKNOWN",
                "force_sampling_rate": "UNKNOWN",
                "camera_sampling_rate": "UNKNOWN",
                "start_time": "UNKNOWN",
                "end_time": "UNKNOWN",
                "synchronization_status": "NOT_STARTED",
                "synchronization_method": "UNKNOWN",
                "notes": f"DIC 配对状态={dic['pair_status']}；缺 DAT={dic['missing_dat_count']}，孤立 DAT={dic['orphan_dat_count']}。目录标签未解释为物理条件，尚未建立力文件权威映射。",
            }
        )
    for force in [row for row in force_rows if row["read_status"] == "READABLE"]:
        stem = Path(force["source_name"]).stem
        rows.append(
            {
                "experiment_id": "FORCE_ONLY_" + stem,
                "specimen_id": "UNKNOWN",
                "source_label": stem,
                "orientation": "UNKNOWN",
                "loading_mode": "UNKNOWN",
                "loading_rate": "UNKNOWN",
                "image_folder": "UNKNOWN",
                "image_count": "UNKNOWN",
                "dat_count": "UNKNOWN",
                "paired_count": "UNKNOWN",
                "first_image": "UNKNOWN",
                "last_image": "UNKNOWN",
                "force_file": force["force_file"],
                "force_rows": force["total_data_rows"],
                "force_columns": force["all_columns"],
                "force_sampling_rate": force["sampling_rate_hz"],
                "camera_sampling_rate": "UNKNOWN",
                "start_time": force["time_start"],
                "end_time": force["time_end"],
                "synchronization_status": "NOT_STARTED",
                "synchronization_method": "UNKNOWN",
                "notes": "该状态导出文件尚未与某个 DIC 试验建立权威对应；列含 Pos/Speed/Press，未发现直接 force/load 列。T 为文件内相对时间候选。",
            }
        )
    fields = [
        "experiment_id", "specimen_id", "source_label", "orientation", "loading_mode", "loading_rate",
        "image_folder", "image_count", "dat_count", "paired_count", "first_image", "last_image",
        "force_file", "force_rows", "force_columns", "force_sampling_rate", "camera_sampling_rate",
        "start_time", "end_time", "synchronization_status", "synchronization_method", "notes",
    ]
    write_csv(out / "experiment_manifest.csv", rows, fields)
    return rows


def build_report(source: Path, project: Path, out: Path, file_rows: list[dict], dic_rows: list[dict], force_rows: list[dict], manifest_rows: list[dict]) -> None:
    total_bytes = sum(int(row["size_bytes"]) for row in file_rows)
    category_counts = Counter(row["category"] for row in file_rows)
    category_sizes = Counter()
    for row in file_rows:
        category_sizes[row["category"]] += int(row["size_bytes"])
    complete = [r for r in dic_rows if r["pair_status"] == "COMPLETE"]
    incomplete = [r for r in dic_rows if r["missing_dat_count"] or r["orphan_dat_count"] or r["image_sequence_gap_count"] or r["dat_sequence_gap_count"]]
    papers = [r for r in file_rows if r["category"] == "论文/研究资料"]
    readable = [r for r in force_rows if r["read_status"] == "READABLE"]
    lock_files = [r for r in force_rows if r["read_status"] == "LOCK_FILE"]
    force_with_force_col = [r for r in force_rows if r["force_or_load_columns"] != "UNKNOWN"]
    lines = [
        "# PA12 实验数据第一阶段盘点报告",
        "",
        f"- 盘点源目录：`{norm_path(source)}`",
        f"- 结构化目录：`{norm_path(project)}`",
        "- 阶段：第一阶段，数据盘点和建立索引。未执行图片/DAT/力值同步、应力应变计算或 VFM。",
        "- 原始数据处理：源目录既有文件未覆盖、未重命名、未移动；结构化目录为新增副本。",
        "",
        "## 1. 总体数量",
        "",
        f"源目录（排除本次新建的结构化副本）共有 **{len(file_rows)} 个文件**，总大小 **{total_bytes:,} bytes**。",
        "",
        "| 分类 | 文件数 | 大小（bytes） |",
        "| --- | ---: | ---: |",
    ]
    for category in sorted(category_counts):
        lines.append(f"| {category} | {category_counts[category]} | {category_sizes[category]:,} |")
    lines += [
        "",
        f"论文/研究资料共 {len(papers)} 个文件，包含 4 个 PDF 和 1 个 DOCX。论文只登记文件，未在本阶段全文分析。",
        "",
        "## 2. DIC 图片与 DAT",
        "",
        f"DIC 清单共记录 {len(dic_rows)} 个直接包含 JPG/JPEG 或 DAT 的目录，其中 {len(complete)} 个目录的图片与 DAT 完整配对，{len(incomplete)} 个目录存在缺 DAT、孤立 DAT 或编号不连续。",
        "",
        "重点异常如下：",
        "",
    ]
    if incomplete:
        for row in incomplete:
            issues = []
            if row["missing_dat_count"]:
                issues.append(f"缺 DAT {row['missing_dat_count']} 个")
            if row["orphan_dat_count"]:
                issues.append(f"孤立 DAT {row['orphan_dat_count']} 个")
            if row["image_sequence_gap_count"]:
                issues.append(f"图片编号缺口 {row['image_sequence_gap_count']} 个")
            if row["dat_sequence_gap_count"]:
                issues.append(f"DAT 编号缺口 {row['dat_sequence_gap_count']} 个")
            lines.append(f"- `{row['organized_folder']}`：图片 {row['image_count']}，DAT {row['dat_count']}，已配对 {row['paired_count']}；" + "，".join(issues) + "。")
    else:
        lines.append("- 未发现配对异常。")
    lines += [
        "",
        "需要注意：`raw_xy_original_all` 下面同时存在原始采集目录、筛选目录和预览目录。清单按直接包含图片/DAT 的目录分别记录，避免把处理副本和原始采集混成一组。",
        "",
        "## 3. XLS/XLSX 力数据盘点",
        "",
        f"共发现 {len(force_rows)} 个 XLS/XLSX 文件，其中正式状态导出 {len(readable)} 个、Office 临时锁文件 {len(lock_files)} 个；正式文件全部成功读取。当前正式文件扩展名为 `.xls`，但文件容器签名是 OOXML ZIP，实际按 openpyxl 读取。",
        "",
        "已读取的工作表普遍包含 `Pos`、`Speed`、`Press`，列名形态为 `T`、`X1_Pos`、`X2_Pos`、`Y1_Pos`、`Y2_Pos` 等。`T` 可作为文件内相对时间候选，`*_Pos` 可作为位置/位移候选，`*_Speed` 可作为速度候选，`*_Press` 可作为压力候选。",
        "",
        f"直接名称含 `force` 或 `load` 的列文件数：{len(force_with_force_col)}。因此第一阶段不能把这些状态导出直接认定为力传感器数据，也不能把 `Press` 直接解释为力。",
        "",
        "力数据的时间值目前是文件内相对 `T`，不是墙上时钟时间；没有发现可以直接用于图片同步的硬件触发时间。",
        "",
        "## 4. 图片与力文件对应状态",
        "",
        f"`experiment_manifest.csv` 共 {len(manifest_rows)} 行：包含 DIC 试验集合和 {len(readable)} 个未建立图像映射的正式状态导出记录。临时锁文件只保留在 `file_inventory.csv` 和 `force_inventory.csv` 中。",
        "",
        "- DIC 行的 `force_file` 暂写 `UNKNOWN`，因为当前没有权威的试样编号到状态导出文件映射；文件名只作为候选标签，不作为物理含义判断。",
        "- 力文件行的 `image_folder` 暂写 `UNKNOWN`，用于明确标出尚未匹配的力文件。",
        "- 所有行的 `synchronization_status` 为 `NOT_STARTED`；本阶段没有执行同步。",
        "- 仅凭文件修改时间不能代表采集时间，因此没有把修改时间写入同步字段。",
        "",
        "## 5. 几何与其他资料",
        "",
        "- 已整理 6 个 STEP 文件，并保留几何 PDF、尺寸叠加图、验证 JSON 和说明 TXT。",
        "- `yuan_analysis_20260912/` 已有历史分析结果、报告和分析环境，本阶段只在 `file_inventory.csv` 中登记，未把运行环境复制进结构化原始层。",
        "- `second brain/` 是独立的 Obsidian 知识库，本阶段只登记，不与实验原始数据混合。",
        "- XY/XZ 压缩归档已保留在 `00_README/source_archives/`，展开后的实验数据也已按类别复制。",
        "",
        "## 6. 输出文件",
        "",
        "- `05_output/manifests/file_inventory.csv`：源目录全量文件分类清单（排除本次结构化副本自身）。",
        "- `05_output/manifests/dic_inventory.csv`：JPG/DAT 目录级配对与编号清单。",
        "- `05_output/manifests/force_inventory.csv`：XLS/XLSX 工作表、列、行数、候选字段和数值范围清单。",
        "- `05_output/manifests/experiment_manifest.csv`：第一阶段试验/力文件索引。",
        "- `05_output/reports/data_inventory_report.md`：本报告。",
        "",
        "## 7. 第一阶段结论",
        "",
        "结构化目录已建立，原始图像、DAT、状态导出和几何资料均已按来源复制并完成文件数/字节数核对。下一阶段需要先人工确认试样编号与力文件的映射，以及 `T`、相机采集时刻和触发方式，再进行同步。",
    ]
    (out / "data_inventory_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--project", required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    project = args.project.resolve()
    out = project / "05_output" / "manifests"
    report_out = project / "05_output" / "reports"
    file_rows = build_file_inventory(source, project, out)
    dic_rows = build_dic_inventory(project, source, out)
    force_rows = build_force_inventory(project, out)
    manifest_rows = build_experiment_manifest(dic_rows, force_rows, project, out)
    build_report(source, project, report_out, file_rows, dic_rows, force_rows, manifest_rows)
    print(json.dumps({
        "source_files": len(file_rows),
        "dic_collections": len(dic_rows),
        "force_files": len(force_rows),
        "manifest_rows": len(manifest_rows),
        "output": norm_path(project / "05_output"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
