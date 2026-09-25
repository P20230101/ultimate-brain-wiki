from __future__ import annotations

import csv
import math
import re
import zlib
from pathlib import Path


REQUIRED_FIELDS = ("x", "y", "u", "v", "exx", "eyy", "exy")
_DAT_RECORD_TOKENS = ("<18>=<", "<53>=<")


class MatchIDExportError(ValueError):
    """Raised when a MatchID export cannot satisfy the declared input contract."""


def _first_tag(text: str, tag: str) -> str | None:
    match = re.search(rf"<{re.escape(tag)}>=<([^>]*)>", text)
    return None if match is None else match.group(1)


def inspect_dat_file(dat_path: Path) -> dict:
    """Inspect a compressed MatchID DAT without loading the full field into memory."""

    header = ""
    counts = {"18": 0, "53": 0}
    carry = ""
    carry_length = max(len(token) for token in _DAT_RECORD_TOKENS) - 1
    decompressor = zlib.decompressobj(wbits=31)
    with dat_path.open("rb") as handle:
        while not decompressor.eof:
            compressed = handle.read(1024 * 1024)
            if not compressed:
                output = decompressor.flush()
                if not output:
                    break
            else:
                output = decompressor.decompress(compressed)
            chunk = output.decode("latin1", errors="replace")
            if len(header) < 200_000:
                header += chunk[: 200_000 - len(header)]
            combined = carry + chunk
            for key, token in (("18", "<18>=<"), ("53", "<53>=<")):
                counts[key] += combined.count(token)
            carry = combined[-carry_length:]

    version_match = re.search(r"\*\*\*MatchID 2D-Version\s+([0-9.]+)", header)
    point_count_raw = _first_tag(header, "55")
    point_count = int(point_count_raw) if point_count_raw is not None else None
    if counts["18"] == 0 and counts["53"] == 0:
        status = "NO_DIC_RECORDS"
    elif counts["53"] == 0:
        status = "NO_STRAIN_RECORDS"
    elif counts["18"] == 0:
        status = "NO_DISPLACEMENT_RECORDS"
    else:
        status = "DIC_FIELDS_AVAILABLE"
    return {
        "path": str(dat_path),
        "version": None if version_match is None else version_match.group(1),
        "conversion_mm_per_pixel": (
            None if _first_tag(header, "11") is None else float(_first_tag(header, "11"))
        ),
        "roi_raw": _first_tag(header, "16"),
        "point_count": point_count,
        "record_counts": counts,
        "status": status,
    }


def classify_dat_point_count_anomalies(
    audits: list[dict], *, min_fraction: float = 0.2
) -> list[dict]:
    """Mark usable-looking frames whose DAT field is probably truncated."""

    if not 0.0 < min_fraction <= 1.0:
        raise ValueError("min_fraction 必须在 0 和 1 之间")
    point_counts = sorted(
        int(row["point_count"])
        for row in audits
        if row.get("status") == "DIC_FIELDS_AVAILABLE"
        and row.get("point_count") is not None
    )
    if not point_counts:
        return [dict(row) for row in audits]
    middle = len(point_counts) // 2
    reference = (
        point_counts[middle]
        if len(point_counts) % 2
        else int(round((point_counts[middle - 1] + point_counts[middle]) / 2.0))
    )
    classified: list[dict] = []
    for audit in audits:
        row = dict(audit)
        row["point_count_reference"] = reference
        point_count = row.get("point_count")
        if (
            row.get("status") == "DIC_FIELDS_AVAILABLE"
            and point_count is not None
            and int(point_count) < reference * min_fraction
        ):
            row["status"] = "DAT_POINT_COUNT_ANOMALY"
            row["point_count_fraction"] = float(int(point_count) / reference)
            row["error"] = (
                f"DAT 点数 {point_count} 仅为实验参考点数 {reference} 的 "
                f"{int(point_count) / reference:.3f}，疑似截断帧"
            )
        classified.append(row)
    return classified


def _read_dat_text(dat_path: Path) -> str:
    compressed = dat_path.read_bytes()
    decompressor = zlib.decompressobj(wbits=31)
    payload = decompressor.decompress(compressed) + decompressor.flush()
    return payload.decode("latin1", errors="replace")


def _finite_dat_number(value: str, field: str, dat_path: Path) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise MatchIDExportError(
            f"{dat_path} 的 DAT {field} 字段不是数值：{value!r}"
        ) from error
    if not math.isfinite(number):
        raise MatchIDExportError(
            f"{dat_path} 的 DAT {field} 字段包含 NaN 或无穷值"
        )
    return number


def parse_matchid_dat(dat_path: Path) -> dict:
    """Parse the confirmed MatchID 2D 19.x DAT field layout.

    The layout is established by comparing raw ``<18>/<53>`` records with a
    Results Viewer CSV from the same MatchID job/version.  Invalid ``<53>``
    records are excluded using their explicit validity flag; values are never
    imputed.
    """

    text = _read_dat_text(dat_path)
    displacement_records = [
        record.split(";") for record in re.findall(r"<18>=<([^>]*)>", text)
    ]
    strain_records = [
        record.split(";") for record in re.findall(r"<53>=<([^>]*)>", text)
    ]
    if not displacement_records or not strain_records:
        raise MatchIDExportError(f"{dat_path} 不含完整的 <18>/<53> 记录")

    displacement_by_id = {
        int(record[0]): record for record in displacement_records
    }
    strain_by_id = {int(record[0]): record for record in strain_records}
    if set(displacement_by_id) != set(strain_by_id):
        raise MatchIDExportError(f"{dat_path} 的 <18>/<53> 点编号不一致")

    scale_raw = _first_tag(text[:200_000], "11")
    if scale_raw is None:
        raise MatchIDExportError(f"{dat_path} 缺少 <11> 标定值")
    scale = _finite_dat_number(scale_raw, "scale", dat_path)

    rows: list[dict[str, float | int]] = []
    excluded_invalid_count = 0
    for point_id in sorted(displacement_by_id):
        displacement = displacement_by_id[point_id]
        strain = strain_by_id[point_id]
        if len(displacement) < 15 or len(strain) < 8:
            raise MatchIDExportError(f"{dat_path} 的点 {point_id} 字段数量不足")
        valid = strain[1].strip().lower()
        if valid not in {"true", "false"}:
            raise MatchIDExportError(
                f"{dat_path} 的点 {point_id} <53> 有效标记无法解析：{strain[1]!r}"
            )
        if valid == "false":
            excluded_invalid_count += 1
            continue
        rows.append(
            {
                "point_id": point_id,
                "x_pixels": _finite_dat_number(displacement[1], "x_base_pixels", dat_path)
                + _finite_dat_number(displacement[5], "x_offset_pixels", dat_path),
                "y_pixels": _finite_dat_number(displacement[2], "y_base_pixels", dat_path)
                + _finite_dat_number(displacement[6], "y_offset_pixels", dat_path),
                "x": (
                    _finite_dat_number(displacement[1], "x_base_pixels", dat_path)
                    + _finite_dat_number(displacement[5], "x_offset_pixels", dat_path)
                )
                * scale,
                "y": (
                    _finite_dat_number(displacement[2], "y_base_pixels", dat_path)
                    + _finite_dat_number(displacement[6], "y_offset_pixels", dat_path)
                )
                * scale,
                "u": _finite_dat_number(displacement[7], "u_pixels", dat_path) * scale,
                "v": _finite_dat_number(displacement[8], "v_pixels", dat_path) * scale,
                "exx": _finite_dat_number(strain[2], "exx", dat_path),
                "eyy": _finite_dat_number(strain[3], "eyy", dat_path),
                "exy": _finite_dat_number(strain[4], "exy", dat_path),
                "e1": _finite_dat_number(strain[5], "e1", dat_path),
                "e2": _finite_dat_number(strain[6], "e2", dat_path),
                "gamma": _finite_dat_number(strain[7], "gamma", dat_path),
                "r": _finite_dat_number(displacement[13], "r", dat_path),
                "sigma": _finite_dat_number(displacement[14], "sigma", dat_path),
            }
        )
    return {
        "version": _first_tag(text[:200_000], "0"),
        "scale_mm_per_pixel": scale,
        "point_count": len(displacement_records),
        "valid_point_count": len(rows),
        "excluded_invalid_count": excluded_invalid_count,
        "rows": rows,
    }


def audit_dat_rows(image_folder: Path, index_rows: list[dict[str, str]]) -> list[dict]:
    """Audit the DAT paired with every photo in a force-index table."""

    audited: list[dict] = []
    for row in index_rows:
        image_name = row["照片"]
        dat_path = image_folder / f"{image_name}.dat"
        if not dat_path.is_file():
            audited.append(
                {
                    "照片": image_name,
                    "DAT": str(dat_path),
                    "status": "MISSING_DAT",
                    "record_counts": {"18": 0, "53": 0},
                    "point_count": None,
                    "version": None,
                    "conversion_mm_per_pixel": None,
                }
            )
            continue
        try:
            quality = inspect_dat_file(dat_path)
        except (OSError, EOFError, zlib.error) as error:
            audited.append(
                {
                    "照片": image_name,
                    "DAT": str(dat_path),
                    "status": "CORRUPT_DAT",
                    "error": str(error),
                    "record_counts": {"18": 0, "53": 0},
                    "point_count": None,
                    "version": None,
                    "conversion_mm_per_pixel": None,
                }
            )
            continue
        audited.append({"照片": image_name, "DAT": str(dat_path), **quality})
    return audited


def _validate_field_map(field_map: dict[str, str]) -> None:
    missing = [name for name in REQUIRED_FIELDS if not field_map.get(name)]
    if missing:
        raise MatchIDExportError(
            "MatchID 导出缺少显式字段映射：" + ", ".join(missing)
        )
    actual_names = [field_map[name] for name in REQUIRED_FIELDS]
    if len(actual_names) != len(set(actual_names)):
        raise MatchIDExportError("MatchID 导出字段映射包含重复列名")


def _number(value: str, field: str, path: Path) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise MatchIDExportError(f"{path} 的 {field} 列包含非数值：{value!r}") from error
    if not math.isfinite(number):
        raise MatchIDExportError(f"{path} 的 {field} 列包含 NaN 或无穷值")
    return number


def read_matchid_export(
    export_path: Path,
    field_map: dict[str, str],
    *,
    delimiter: str = ",",
) -> list[dict[str, float]]:
    """Read one Results Viewer CSV using an explicit canonical-field mapping."""

    _validate_field_map(field_map)
    with export_path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        if reader.fieldnames is None:
            raise MatchIDExportError(f"{export_path} 没有表头")
        missing_columns = [
            field_map[name]
            for name in REQUIRED_FIELDS
            if field_map[name] not in reader.fieldnames
        ]
        if missing_columns:
            raise MatchIDExportError(
                f"{export_path} 缺少声明的列：" + ", ".join(missing_columns)
            )
        rows: list[dict[str, float]] = []
        for row_number, row in enumerate(reader, start=2):
            if any(row.get(field_map[name]) in (None, "") for name in REQUIRED_FIELDS):
                raise MatchIDExportError(f"{export_path} 第 {row_number} 行存在空字段")
            rows.append(
                {
                    name: _number(row[field_map[name]], name, export_path)
                    for name in REQUIRED_FIELDS
                }
            )
    if not rows:
        raise MatchIDExportError(f"{export_path} 没有 DIC 点记录")
    return rows


def _require_units(units: dict[str, str]) -> None:
    missing = [name for name in REQUIRED_FIELDS if not units.get(name)]
    if missing:
        raise MatchIDExportError(
            "MatchID 导出缺少单位声明：" + ", ".join(missing)
        )


def _format_number(value: float) -> str:
    return f"{value:.12g}"


def _attach_frame_metadata(
    index_row: dict[str, str], rows: list[dict[str, float]]
) -> list[dict[str, str]]:
    metadata = {
        "照片": index_row["照片"],
        "时间/s": index_row["时间/s"],
        "X向力/N": index_row["X向力/N"],
        "Y向力/N": index_row["Y向力/N"],
    }
    return [
        {
            **metadata,
            **{name: _format_number(row[name]) for name in REQUIRED_FIELDS},
        }
        for row in rows
    ]


def merge_exported_frame(
    index_row: dict[str, str],
    export_path: Path,
    field_map: dict[str, str],
    units: dict[str, str],
    *,
    delimiter: str = ",",
) -> list[dict[str, str]]:
    """Attach one frame's time and synchronized forces to every DIC point."""

    _validate_field_map(field_map)
    _require_units(units)
    rows = read_matchid_export(export_path, field_map, delimiter=delimiter)
    return _attach_frame_metadata(index_row, rows)


def merge_reconstructed_frame(
    index_row: dict[str, str],
    dat_path: Path,
    units: dict[str, str],
) -> tuple[list[dict[str, str]], dict]:
    """Reconstruct one frame from its confirmed DAT field layout."""

    _require_units(units)
    parsed = parse_matchid_dat(dat_path)
    return _attach_frame_metadata(index_row, parsed["rows"]), parsed
