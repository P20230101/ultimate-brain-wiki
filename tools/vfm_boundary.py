from __future__ import annotations

import gzip
import json
import math
import re
from pathlib import Path


EXPECTED_ROTATED_MAPPING = {
    "顶部": "X2",
    "底部": "X1",
    "左侧": "Y2",
    "右侧": "Y1",
}


class VfmBoundaryError(ValueError):
    """Raised when a VFM boundary contract cannot be established."""


def load_vfm_boundary_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_vfm_boundary_config(config: dict) -> None:
    geometry = config["geometry"]
    for name in ("center_roi_thickness_mm", "overall_thickness_mm"):
        value = float(geometry[name])
        if not math.isfinite(value) or value <= 0.0:
            raise VfmBoundaryError(f"几何参数 {name} 必须是正数")

    mapping = config["rotated_boundary_mapping"]
    if mapping != EXPECTED_ROTATED_MAPPING:
        raise VfmBoundaryError(
            f"旋转后边界映射不符合已确认方向：{mapping!r}"
        )

    modes = config["loading_modes"]
    if modes["双轴"]["positive_sides"] != {
        "X": ["顶部", "底部"],
        "Y": ["左侧", "右侧"],
    }:
        raise VfmBoundaryError("双轴边界必须使用 X 顶/底、Y 左/右")
    if modes["单轴 X"]["positive_sides"] != {"X": ["顶部", "底部"]}:
        raise VfmBoundaryError("单轴 X 必须只使用顶部/底部")
    if modes["单轴 Y"]["positive_sides"] != {"Y": ["左侧", "右侧"]}:
        raise VfmBoundaryError("单轴 Y 必须只使用左侧/右侧")


def _tag_values(text: str, tag: str) -> list[str]:
    return re.findall(rf"<{re.escape(tag)}>=<([^>]*)>", text)


def _number(value: str, field: str, path: Path) -> float:
    try:
        number = float(value)
    except ValueError as error:
        raise VfmBoundaryError(f"{path} 的 {field} 不是数值：{value!r}") from error
    if not math.isfinite(number):
        raise VfmBoundaryError(f"{path} 的 {field} 不是有限数值")
    return number


def _parse_boundary(payload: str, path: Path) -> dict:
    fields = payload.split(";")
    if len(fields) < 1:
        raise VfmBoundaryError(f"{path} 的 Boundary 记录为空")
    try:
        boundary_id = int(fields[0])
    except ValueError as error:
        raise VfmBoundaryError(f"{path} 的 Boundary 编号无法解析") from error
    return {"id": boundary_id, "fields": fields}


def _parse_force_series(payload: str, path: Path) -> dict:
    fields = payload.split(";")
    if len(fields) < 2:
        raise VfmBoundaryError(f"{path} 的 Forces 记录字段不足")
    try:
        series_id = int(fields[0])
        declared_count = int(fields[1])
    except ValueError as error:
        raise VfmBoundaryError(f"{path} 的 Forces 编号或数量无法解析") from error
    entries = fields[2:]
    if len(entries) % 2 != 0:
        raise VfmBoundaryError(f"{path} 的 Forces 图像—力序列不成对")
    frame_names = entries[::2]
    values = [
        _number(value, f"Forces[{series_id}]", path)
        for value in entries[1::2]
    ]
    if declared_count != len(values):
        raise VfmBoundaryError(
            f"{path} 的 Forces[{series_id}] 声明 {declared_count} 帧，实际 {len(values)} 帧"
        )
    return {
        "id": series_id,
        "declared_count": declared_count,
        "frame_names": frame_names,
        "values": values,
    }


def parse_matchid_vfm_metadata(vfm_path: Path) -> dict:
    with gzip.open(vfm_path, "rt", encoding="utf-8", errors="replace") as handle:
        text = handle.read()

    thickness_values = _tag_values(text, "Thickness")
    conversion_values = _tag_values(text, "Conversion")
    if not thickness_values:
        raise VfmBoundaryError(f"{vfm_path} 缺少 Thickness")
    if not conversion_values:
        raise VfmBoundaryError(f"{vfm_path} 缺少 Conversion")

    boundaries = [_parse_boundary(value, vfm_path) for value in _tag_values(text, "Boundary")]
    force_series = [
        _parse_force_series(value, vfm_path)
        for value in _tag_values(text, "Forces")
    ]
    if not boundaries or not force_series:
        raise VfmBoundaryError(f"{vfm_path} 缺少 Boundary 或 Forces 记录")
    force_values = [value for series in force_series for value in series["values"]]
    first_force_samples = [series["values"][0] for series in force_series if series["values"]]
    later_force_values = [value for series in force_series for value in series["values"][1:]]
    frame_counts = sorted({series["declared_count"] for series in force_series})
    return {
        "path": str(vfm_path),
        "thickness_mm": _number(thickness_values[0], "Thickness", vfm_path),
        "conversion_mm_per_pixel": _number(
            conversion_values[0], "Conversion", vfm_path
        ),
        "boundary_count": len(boundaries),
        "boundary_ids": [boundary["id"] for boundary in boundaries],
        "boundaries": boundaries,
        "force_series_count": len(force_series),
        "force_frame_counts": frame_counts,
        "force_series": force_series,
        "all_force_values_nonnegative": all(value >= -1e-12 for value in force_values),
        "first_force_samples_zero": all(abs(value) <= 1e-12 for value in first_force_samples),
        "later_force_values_positive": all(value > 0.0 for value in later_force_values),
    }
