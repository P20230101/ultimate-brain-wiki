from __future__ import annotations

import argparse
import csv
import json
import shutil
import tempfile
import zlib
from pathlib import Path

if __package__:
    from .matchid_dic import (
        MatchIDExportError,
        REQUIRED_FIELDS,
        inspect_dat_file,
        merge_exported_frame,
        merge_reconstructed_frame,
    )
else:
    from matchid_dic import (
        MatchIDExportError,
        REQUIRED_FIELDS,
        inspect_dat_file,
        merge_exported_frame,
        merge_reconstructed_frame,
    )


INDEX_FIELDS = ["照片", "DAT", "时间/s", "X向力/N", "Y向力/N"]
MERGED_FIELDS = ["照片", "时间/s", "X向力/N", "Y向力/N", *REQUIRED_FIELDS]


def _read_index(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"帧—力索引没有表头：{path}")
        missing = [field for field in INDEX_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"帧—力索引缺少列：{', '.join(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"帧—力索引没有数据：{path}")
    return rows


def _write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _write_status(output_dir: Path, experiment_id: str, result: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{experiment_id}_DIC全场—力状态.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _resolve_dat_path(index_row: dict[str, str], dat_root: Path | None) -> Path | None:
    for field in ("DAT原始路径", "DAT"):
        raw_path = index_row.get(field)
        if not raw_path:
            continue
        path = Path(raw_path)
        if path.is_absolute() or dat_root is None:
            return path
        return dat_root / path
    return None


def _dat_point_count(quality: dict) -> int | None:
    if quality["point_count"] is not None:
        return quality["point_count"]
    count = quality["record_counts"]["18"]
    return count if count else None


def merge_experiment_exports(
    experiment_id: str,
    index_path: Path,
    export_root: Path,
    output_dir: Path,
    field_map: dict[str, str],
    units: dict[str, str],
    *,
    pattern: str = "{photo_stem}.csv",
    delimiter: str = ",",
    dat_root: Path | None = None,
) -> dict:
    """Merge Results Viewer exports, reconstructing eligible frames from DAT."""

    index_rows = _read_index(index_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    export_paths = [
        export_root
        / pattern.format(
            experiment_id=experiment_id,
            photo_name=row["照片"],
            photo_stem=Path(row["照片"]).stem,
        )
        for row in index_rows
    ]
    with tempfile.TemporaryDirectory(dir=output_dir, prefix=".merge-") as staging_root:
        staging_dir = Path(staging_root) / "merged"
        staging_dir.mkdir()
        frame_index_rows: list[dict[str, str]] = []
        missing_exports: list[str] = []
        source_counts: dict[str, int] = {}
        reconstructed_frame_count = 0
        excluded_invalid_point_count = 0
        for index_row, export_path in zip(index_rows, export_paths):
            dat_path = _resolve_dat_path(index_row, dat_root)
            dat_quality = None
            if dat_path is not None and dat_path.is_file():
                try:
                    dat_quality = inspect_dat_file(dat_path)
                except (OSError, EOFError, zlib.error) as error:
                    result = {
                        "experiment_id": experiment_id,
                        "status": "EXPORT_REQUIRED" if not export_path.is_file() else "EXPORT_INVALID",
                        "frame_count": len(index_rows),
                        "invalid_export": str(export_path) if export_path.is_file() else None,
                        "missing_exports": [str(export_path)] if not export_path.is_file() else [],
                        "reconstruction_failed_frame": index_row["照片"],
                        "reconstruction_error": str(error),
                    }
                    _write_status(output_dir, experiment_id, result)
                    return result
                if dat_quality["record_counts"]["18"] == 0 or dat_quality["record_counts"]["53"] == 0:
                    result = {
                        "experiment_id": experiment_id,
                        "status": "EXPORT_REQUIRED" if not export_path.is_file() else "EXPORT_INVALID",
                        "frame_count": len(index_rows),
                        "invalid_export": str(export_path) if export_path.is_file() else None,
                        "missing_exports": [str(export_path)] if not export_path.is_file() else [],
                        "reconstruction_failed_frame": index_row["照片"],
                        "reconstruction_error": f"{dat_path} 不含完整的 <18>/<53> 记录",
                    }
                    _write_status(output_dir, experiment_id, result)
                    return result

            rows = None
            source = None
            parsed_dat = None
            try:
                if export_path.is_file():
                    rows = merge_exported_frame(
                        index_row,
                        export_path,
                        field_map,
                        units,
                        delimiter=delimiter,
                    )
                    expected_point_count = None if dat_quality is None else _dat_point_count(dat_quality)
                    if expected_point_count is not None and len(rows) != expected_point_count:
                        raise MatchIDExportError(
                            f"{export_path} 点数 {len(rows)} 与 DAT 点数 {expected_point_count} 不一致"
                        )
                    source = "RESULTS_VIEWER_CSV"
                elif dat_path is None or not dat_path.is_file():
                    missing_exports.append(str(export_path))
            except MatchIDExportError as csv_error:
                if dat_path is None or not dat_path.is_file():
                    result = {
                        "experiment_id": experiment_id,
                        "status": "EXPORT_INVALID",
                        "frame_count": len(index_rows),
                        "invalid_export": str(export_path),
                        "error": str(csv_error),
                    }
                    _write_status(output_dir, experiment_id, result)
                    return result

            if source is None and dat_path is not None and dat_path.is_file():
                try:
                    rows, parsed_dat = merge_reconstructed_frame(index_row, dat_path, units)
                    source = "DAT_RECONSTRUCTED"
                except MatchIDExportError as dat_error:
                    result = {
                        "experiment_id": experiment_id,
                        "status": "EXPORT_REQUIRED" if not export_path.is_file() else "EXPORT_INVALID",
                        "frame_count": len(index_rows),
                        "invalid_export": str(export_path) if export_path.is_file() else None,
                        "missing_exports": [str(export_path)] if not export_path.is_file() else [],
                        "reconstruction_failed_frame": index_row["照片"],
                        "reconstruction_error": str(dat_error),
                    }
                    _write_status(output_dir, experiment_id, result)
                    return result

            if source is None:
                continue

            assert rows is not None
            source_counts[source] = source_counts.get(source, 0) + 1
            if parsed_dat is not None:
                reconstructed_frame_count += 1
                excluded_invalid_point_count += parsed_dat["excluded_invalid_count"]
            merged_path = staging_dir / f"{Path(index_row['照片']).stem}_DIC全场—力.csv"
            _write_rows(merged_path, rows, MERGED_FIELDS)
            frame_index_rows.append(
                {
                    "照片": index_row["照片"],
                    "时间/s": index_row["时间/s"],
                    "X向力/N": index_row["X向力/N"],
                    "Y向力/N": index_row["Y向力/N"],
                    "DIC导出文件": str(export_path),
                    "DIC数据来源": source,
                    "合并文件": str(output_dir / "merged" / merged_path.name),
                    "点数": str(len(rows)),
                    "DAT原始点数": "" if parsed_dat is None else str(parsed_dat["point_count"]),
                    "排除无效点数": "0" if parsed_dat is None else str(parsed_dat["excluded_invalid_count"]),
                    "状态": "READY",
                }
            )

        if missing_exports:
            result = {
                "experiment_id": experiment_id,
                "status": "EXPORT_REQUIRED",
                "frame_count": len(index_rows),
                "missing_export_count": len(missing_exports),
                "missing_exports": missing_exports,
                "source_counts": source_counts,
                "reconstructed_frame_count": reconstructed_frame_count,
                "excluded_invalid_point_count": excluded_invalid_point_count,
            }
            _write_status(output_dir, experiment_id, result)
            return result

        index_output = output_dir / f"{experiment_id}_DIC全场—力索引.csv"
        staged_index = Path(staging_root) / index_output.name
        _write_rows(
            staged_index,
            frame_index_rows,
            [
                "照片",
                "时间/s",
                "X向力/N",
                "Y向力/N",
                "DIC导出文件",
                "DIC数据来源",
                "合并文件",
                "点数",
                "DAT原始点数",
                "排除无效点数",
                "状态",
            ],
        )
        final_merged_dir = output_dir / "merged"
        final_merged_dir.mkdir(exist_ok=True)
        for staged_path in staging_dir.iterdir():
            shutil.move(str(staged_path), str(final_merged_dir / staged_path.name))
        shutil.move(str(staged_index), str(index_output))
        result = {
            "experiment_id": experiment_id,
            "status": "MATCHID_VFM_INPUT_READY",
            "frame_count": len(index_rows),
            "merged_index": str(index_output),
            "merged_directory": str(final_merged_dir),
            "field_map": field_map,
            "units": units,
            "source_counts": source_counts,
            "reconstructed_frame_count": reconstructed_frame_count,
            "excluded_invalid_point_count": excluded_invalid_point_count,
        }
        _write_status(output_dir, experiment_id, result)
        return result


def _load_entry(config_path: Path, experiment_id: str) -> tuple[dict, Path]:
    batch = json.loads(config_path.read_text(encoding="utf-8"))
    entry = next(item for item in batch["experiments"] if item["experiment_id"] == experiment_id)
    output_root = Path(batch["output_root"])
    return entry, output_root


def main() -> int:
    parser = argparse.ArgumentParser(description="合并 MatchID Results Viewer 导出的 DIC 全场 CSV")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--mapping-config", required=True, type=Path)
    parser.add_argument("--export-root", required=True, type=Path)
    args = parser.parse_args()

    entry, output_root = _load_entry(args.config, args.experiment)
    mapping = json.loads(args.mapping_config.read_text(encoding="utf-8"))
    preparation_root = output_root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备"
    index_path = preparation_root / f"{args.experiment}_帧—力—时间索引.csv"
    result = merge_experiment_exports(
        args.experiment,
        index_path,
        args.export_root,
        preparation_root / args.experiment,
        mapping["field_map"],
        mapping["units"],
        pattern=mapping.get("pattern", "{photo_stem}.csv"),
        delimiter=mapping.get("delimiter", ","),
        dat_root=Path(entry["image_folder"]) if entry.get("image_folder") else None,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "MATCHID_VFM_INPUT_READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
