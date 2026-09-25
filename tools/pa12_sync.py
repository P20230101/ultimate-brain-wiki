from __future__ import annotations

import argparse
import csv
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

if __package__:
    from .pa12_mechanics import build_nominal_stress_strain_table
else:
    from pa12_mechanics import build_nominal_stress_strain_table

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


class VFMOutputBlocked(RuntimeError):
    """Raised when formal VFM output would violate the row-count contract."""


@dataclass(frozen=True)
class ForceEvents:
    start_index: int
    peak_index: int
    fracture_index: int
    baseline_x: float
    baseline_y: float
    load_polarity: float
    peak_magnitude: float
    fracture_magnitude: float


@dataclass(frozen=True)
class InterpolatedForces:
    photo_time: np.ndarray
    x: np.ndarray
    y: np.ndarray


@dataclass(frozen=True)
class FrameRecord:
    number: int
    image_name: str
    dat_name: str


@dataclass(frozen=True)
class FrameInventory:
    images: tuple[Path, ...]
    dats: tuple[Path, ...]
    paired: tuple[FrameRecord, ...]
    missing_dat: tuple[str, ...]
    orphan_dat: tuple[str, ...]
    image_numbers: tuple[int, ...]
    dat_numbers: tuple[int, ...]
    image_sequence_gaps: tuple[int, ...]
    dat_sequence_gaps: tuple[int, ...]


def average_press_channels(
    frame: pd.DataFrame,
    x_columns: list[str] | tuple[str, ...],
    y_columns: list[str] | tuple[str, ...],
) -> tuple[np.ndarray, np.ndarray]:
    x_values = frame[list(x_columns)].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    y_values = frame[list(y_columns)].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    return np.mean(x_values, axis=1), np.mean(y_values, axis=1)


def _require_numeric_array(name: str, values: np.ndarray) -> None:
    if values.ndim != 1:
        raise ValueError(f"{name} 必须是一维数组")
    if not np.isfinite(values).all():
        raise ValueError(f"{name} 包含 NaN 或无穷值")


def _require_strictly_increasing(name: str, values: np.ndarray) -> None:
    _require_numeric_array(name, values)
    if len(values) < 2 or not np.all(np.diff(values) > 0):
        raise ValueError(f"{name} 必须严格递增")


def _odd_window(window: int) -> int:
    value = max(3, int(window))
    return value if value % 2 else value + 1


def _moving_average(values: np.ndarray, window: int) -> np.ndarray:
    return (
        pd.Series(values)
        .rolling(window=_odd_window(window), center=True, min_periods=1)
        .mean()
        .to_numpy(dtype=float)
    )


def _first_sustained(mask: np.ndarray, persistence: int, start: int) -> int | None:
    for index in range(start, len(mask) - persistence + 1):
        if bool(np.all(mask[index : index + persistence])):
            return index
    return None


def detect_force_events(
    time: np.ndarray,
    x_raw: np.ndarray,
    y_raw: np.ndarray,
    *,
    baseline_window_s: float = 0.05,
    start_threshold_n: float = 5.0,
    persistence_s: float = 0.05,
    fracture_fraction: float = 0.2,
    smoothing_window_s: float = 0.05,
    manual_start_index: int | None = None,
    manual_fracture_index: int | None = None,
) -> ForceEvents:
    time = np.asarray(time, dtype=float)
    x_raw = np.asarray(x_raw, dtype=float)
    y_raw = np.asarray(y_raw, dtype=float)
    if not (len(time) == len(x_raw) == len(y_raw)):
        raise ValueError("时间、X 力、Y 力长度必须相同")
    _require_strictly_increasing("力时间", time)
    _require_numeric_array("X 力", x_raw)
    _require_numeric_array("Y 力", y_raw)
    if not 0.0 < fracture_fraction < 1.0:
        raise ValueError("fracture_fraction 必须在 0 和 1 之间")
    if (manual_start_index is None) != (manual_fracture_index is None):
        raise ValueError("人工力数据覆盖必须同时提供 start_index 和 fracture_index")

    dt = float(np.median(np.diff(time)))
    baseline_count = max(3, int(round(baseline_window_s / dt)))
    if baseline_count >= len(time):
        raise ValueError("基线窗口覆盖了全部力数据")
    baseline_x = float(np.mean(x_raw[:baseline_count]))
    baseline_y = float(np.mean(y_raw[:baseline_count]))
    centered = ((x_raw - baseline_x) + (y_raw - baseline_y)) / 2.0

    noise = float(np.median(np.abs(centered[:baseline_count] - np.median(centered[:baseline_count]))))
    noise_sigma = max(1.4826 * noise, 0.5)
    threshold = max(float(start_threshold_n), 6.0 * noise_sigma)
    smoothing_window = max(3, int(round(smoothing_window_s / dt)))
    smoothed = _moving_average(centered, smoothing_window)

    if manual_start_index is not None:
        if not 0 <= manual_start_index < manual_fracture_index < len(time):
            raise ValueError("人工力数据区间无效")
        direction_index = manual_start_index + int(
            np.argmax(np.abs(smoothed[manual_start_index : manual_fracture_index + 1]))
        )
    else:
        direction_index = baseline_count + int(np.argmax(np.abs(smoothed[baseline_count:])))
    load_polarity = float(np.sign(smoothed[direction_index]))
    if load_polarity == 0.0:
        raise ValueError("无法确定加载方向")
    magnitude = load_polarity * smoothed

    persistence = max(2, int(round(persistence_s / dt)))
    if manual_start_index is not None:
        start_index = manual_start_index
    else:
        start_index = _first_sustained(magnitude >= threshold, persistence, baseline_count)
        if start_index is None:
            raise ValueError("未检测到持续离开基线的加载起点")

    peak_end = manual_fracture_index + 1 if manual_fracture_index is not None else len(magnitude)
    peak_index = start_index + int(np.argmax(magnitude[start_index:peak_end]))
    peak_magnitude = float(magnitude[peak_index])
    if peak_magnitude <= threshold:
        raise ValueError("加载峰值没有明显高于基线")

    if manual_fracture_index is not None:
        fracture_index = manual_fracture_index
    else:
        fracture_threshold = peak_magnitude * fracture_fraction
        fracture_index = _first_sustained(
            magnitude <= fracture_threshold,
            persistence,
            peak_index + 1,
        )
        if fracture_index is None:
            raise ValueError("峰值之后未检测到持续掉载，不能确定断裂点")

    return ForceEvents(
        start_index=start_index,
        peak_index=peak_index,
        fracture_index=fracture_index,
        baseline_x=baseline_x,
        baseline_y=baseline_y,
        load_polarity=load_polarity,
        peak_magnitude=peak_magnitude,
        fracture_magnitude=float(magnitude[fracture_index]),
    )


def interpolate_force_values(
    force_time: np.ndarray,
    x_raw: np.ndarray,
    y_raw: np.ndarray,
    photo_time: np.ndarray,
    *,
    baseline_x: float,
    baseline_y: float,
    force_sign: float = -1.0,
) -> InterpolatedForces:
    force_time = np.asarray(force_time, dtype=float)
    x_raw = np.asarray(x_raw, dtype=float)
    y_raw = np.asarray(y_raw, dtype=float)
    photo_time = np.asarray(photo_time, dtype=float)
    if not (len(force_time) == len(x_raw) == len(y_raw)):
        raise ValueError("力时间、X 力、Y 力长度必须相同")
    _require_strictly_increasing("力时间", force_time)
    _require_strictly_increasing("照片时间", photo_time)
    if photo_time[0] < force_time[0] or photo_time[-1] > force_time[-1]:
        raise ValueError("照片时间超出力数据时间范围")
    if not np.isfinite(force_sign) or force_sign == 0.0:
        raise ValueError("force_sign 必须是非零有限数")

    x = (np.interp(photo_time, force_time, x_raw) - baseline_x) * force_sign
    y = (np.interp(photo_time, force_time, y_raw) - baseline_y) * force_sign
    x[0] = 0.0
    y[0] = 0.0
    return InterpolatedForces(photo_time=photo_time, x=x, y=y)


def shared_photo_time_axis(
    x_photo_time: np.ndarray, y_photo_time: np.ndarray
) -> bool:
    return bool(np.array_equal(x_photo_time, y_photo_time))


def select_frame_numbers(
    frame_numbers: list[int] | tuple[int, ...],
    *,
    load_start_time: float,
    fracture_time: float,
    camera_setting_fps: float,
) -> list[int]:
    if not frame_numbers:
        raise ValueError("没有可用照片")
    if camera_setting_fps <= 0.0:
        raise ValueError("相机设置频率必须大于 0")
    if fracture_time <= load_start_time:
        raise ValueError("断裂时间必须晚于加载起点")
    numbers = sorted(frame_numbers)
    expected_start = numbers[0] + math.floor(load_start_time * camera_setting_fps + 0.5)
    expected_end = numbers[0] + math.floor(fracture_time * camera_setting_fps + 0.5)
    start = max(numbers[0], expected_start)
    end = min(numbers[-1], expected_end)
    if start > end:
        raise ValueError("自动检测到的有效实验区间没有覆盖任何照片")
    selected = [number for number in numbers if start <= number <= end]
    if not selected:
        raise ValueError("自动检测到的有效实验区间没有覆盖任何照片")
    return selected


def photo_time_from_frame_numbers(
    frame_numbers: list[int] | tuple[int, ...],
    *,
    start_time: float,
    fracture_time: float,
    camera_setting_fps: float,
) -> np.ndarray:
    numbers = np.asarray(frame_numbers, dtype=float)
    if len(numbers) < 2 or not np.isfinite(numbers).all() or not np.all(np.diff(numbers) > 0):
        raise ValueError("照片帧号必须至少包含两个严格递增的有效帧")
    if camera_setting_fps <= 0.0:
        raise ValueError("相机设置频率必须大于 0")
    if fracture_time <= start_time:
        raise ValueError("断裂时间必须晚于加载起点")
    capture_offsets = (numbers - numbers[0]) / camera_setting_fps
    normalized = capture_offsets / capture_offsets[-1]
    return start_time + normalized * (fracture_time - start_time)


def validate_vfm_lengths(photo_count: int, x_count: int, y_count: int) -> None:
    if not (photo_count == x_count == y_count):
        raise VFMOutputBlocked(
            f"禁止生成正式 VFM：照片={photo_count}，X CSV={x_count}，Y CSV={y_count}"
        )


def validate_nonnegative_vfm_forces(x: np.ndarray, y: np.ndarray) -> None:
    x_values = np.asarray(x, dtype=float)
    y_values = np.asarray(y, dtype=float)
    if (
        x_values[0] < -1e-12
        or y_values[0] < -1e-12
        or np.any(x_values[1:] <= 0.0)
        or np.any(y_values[1:] <= 0.0)
    ):
        raise VFMOutputBlocked("禁止生成正式 VFM：首行外的校正后拉伸力必须严格大于 0")


def validate_active_vfm_forces(
    x: np.ndarray,
    y: np.ndarray,
    active_axes: list[str] | tuple[str, ...],
) -> None:
    values = {"X": np.asarray(x, dtype=float), "Y": np.asarray(y, dtype=float)}
    for axis in active_axes:
        axis_values = values[axis]
        if (
            len(axis_values) == 0
            or not np.isfinite(axis_values).all()
            or axis_values[0] < -1e-12
            or np.any(axis_values[1:] <= 0.0)
        ):
            raise VFMOutputBlocked(f"禁止生成正式 VFM：{axis}方向首行外的校正后拉伸力必须严格大于 0")


def frame_sequence_gaps(numbers: list[int] | tuple[int, ...]) -> list[int]:
    if not numbers:
        return []
    values = sorted(set(numbers))
    return [number for number in range(values[0], values[-1] + 1) if number not in values]


def summarize_frame_numbers(numbers: list[int] | tuple[int, ...], max_ranges: int = 12) -> str:
    values = sorted(set(int(number) for number in numbers))
    if not values:
        return "[]"
    ranges: list[tuple[int, int]] = []
    start = previous = values[0]
    for value in values[1:]:
        if value == previous + 1:
            previous = value
            continue
        ranges.append((start, previous))
        start = previous = value
    ranges.append((start, previous))
    labels = [str(start) if start == end else f"{start}-{end}" for start, end in ranges]
    if len(labels) > max_ranges:
        return ", ".join(labels[:max_ranges]) + f", …（共 {len(values)} 个，{len(labels)} 段）"
    return ", ".join(labels)


def select_frames_from_capture_offsets(
    frame_numbers: list[int] | tuple[int, ...],
    capture_offsets_s: np.ndarray,
    *,
    load_start_time: float,
    fracture_time: float,
) -> tuple[list[int], np.ndarray] | None:
    offsets = np.asarray(capture_offsets_s, dtype=float)
    if len(frame_numbers) != len(offsets):
        raise ValueError("照片帧号和照片时间数量必须相同")
    if len(offsets) < 2 or not np.isfinite(offsets).all() or not np.all(np.diff(offsets) > 0):
        return None
    effective_time = fracture_time - load_start_time
    if effective_time <= 0.0:
        raise ValueError("断裂时间必须晚于加载起点")
    start_index = int(np.argmin(np.abs(offsets - load_start_time)))
    target_end_offset = offsets[start_index] + effective_time
    end_index = int(np.argmin(np.abs(offsets - target_end_offset)))
    if end_index <= start_index:
        return None
    selected_offsets = offsets[start_index : end_index + 1]
    normalized = (selected_offsets - selected_offsets[0]) / (selected_offsets[-1] - selected_offsets[0])
    photo_time = load_start_time + normalized * effective_time
    return list(frame_numbers[start_index : end_index + 1]), photo_time


def read_exif_capture_offsets(image_paths: list[Path] | tuple[Path, ...]) -> np.ndarray | None:
    capture_times: list[datetime] = []
    for path in image_paths:
        with Image.open(path) as image:
            exif = image.getexif()
            raw = exif.get(36867) or exif.get(36868) or exif.get(306)
        if raw is None:
            return None
        if isinstance(raw, bytes):
            raw = raw.decode("ascii")
        capture_times.append(datetime.strptime(str(raw).strip(), "%Y:%m:%d %H:%M:%S"))
    if len(capture_times) < 2:
        return None
    origin = capture_times[0]
    offsets = np.array([(value - origin).total_seconds() for value in capture_times], dtype=float)
    if not np.all(np.diff(offsets) > 0):
        return None
    return offsets


def _parse_frame_number(name: str) -> int:
    match = re.search(r"(\d+)$", Path(name).stem)
    if match is None:
        raise ValueError(f"照片文件名没有可识别的帧号：{name}")
    return int(match.group(1))


def discover_frames(image_folder: Path) -> FrameInventory:
    images = tuple(sorted(
        (path for path in image_folder.iterdir() if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg"}),
        key=lambda path: (_parse_frame_number(path.name), path.name.lower()),
    ))
    dats = tuple(sorted(
        (path for path in image_folder.iterdir() if path.is_file() and path.name.lower().endswith((".jpg.dat", ".jpeg.dat"))),
        key=lambda path: path.name.lower(),
    ))
    image_by_stem = {path.name.lower(): path for path in images}
    dat_by_stem = {path.name[:-4].lower(): path for path in dats}
    if len(image_by_stem) != len(images):
        raise ValueError("照片文件名重复")
    if len(dat_by_stem) != len(dats):
        raise ValueError("DAT 文件名重复")

    paired = []
    missing_dat = []
    for image in images:
        dat = dat_by_stem.get(image.name.lower())
        if dat is None:
            missing_dat.append(image.name)
        else:
            paired.append(FrameRecord(_parse_frame_number(image.name), image.name, dat.name))

    orphan_dat = sorted(set(dat_by_stem) - set(image_by_stem))
    image_numbers = tuple(_parse_frame_number(path.name) for path in images)
    dat_numbers = tuple(_parse_frame_number(path.name[:-4]) for path in dats)
    if list(image_numbers) != sorted(set(image_numbers)):
        raise ValueError("照片帧号重复或无法排序")
    if list(dat_numbers) != sorted(set(dat_numbers)):
        raise ValueError("DAT 帧号重复或无法排序")
    return FrameInventory(
        images=images,
        dats=dats,
        paired=tuple(paired),
        missing_dat=tuple(missing_dat),
        orphan_dat=tuple(orphan_dat),
        image_numbers=image_numbers,
        dat_numbers=dat_numbers,
        image_sequence_gaps=tuple(frame_sequence_gaps(image_numbers)),
        dat_sequence_gaps=tuple(frame_sequence_gaps(dat_numbers)),
    )


def _read_force_tables(config: dict) -> tuple[pd.DataFrame, pd.DataFrame | None]:
    force_file = Path(config["force_file"])
    press_sheet = config.get("press_sheet", "Press")
    position_sheet = config.get("position_sheet", "Pos")
    press = pd.read_excel(force_file, sheet_name=press_sheet, engine="openpyxl")
    try:
        position = pd.read_excel(force_file, sheet_name=position_sheet, engine="openpyxl")
    except ValueError:
        position = None
    return press, position


def _numeric_column(frame: pd.DataFrame, name: str) -> np.ndarray:
    if name not in frame.columns:
        raise ValueError(f"数据表缺少列：{name}")
    values = pd.to_numeric(frame[name], errors="coerce").to_numpy(dtype=float)
    _require_numeric_array(name, values)
    return values


def _format_number(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def _safe_filename(value: str) -> str:
    return re.sub(r"[<>:\"/\\|?*]", "_", value)


def _write_vfm(path: Path, values: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        for value in values:
            writer.writerow([_format_number(float(value))])


def _write_match_table(path: Path, frames: list[FrameRecord], interpolated: InterpolatedForces, include_time: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["照片"]
    if include_time:
        fields.append("时间/s")
    fields.extend(["X向力/N", "Y向力/N"])
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(fields)
        for index, frame in enumerate(frames):
            row = [frame.image_name]
            if include_time:
                row.append(_format_number(float(interpolated.photo_time[index]), 4))
            row.extend([
                _format_number(float(interpolated.x[index])),
                _format_number(float(interpolated.y[index])),
            ])
            writer.writerow(row)


def _write_overview(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["速度", "照片数量", "设置频率", "实际频率", "照片位移", "力数量", "力位移", "力数据时间", "力传感频率"]
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerow({field: row[field] for field in fields})


def _stress_strain_settings(config: dict) -> tuple[dict[str, float], list[str], dict[str, list[str]]]:
    geometry = {
        "specimen_width_mm": 30.0,
        "thickness_mm": 1.0,
        "overall_thickness_mm": 3.0,
        "gauge_length_mm": 30.0,
    }
    geometry.update(config.get("geometry", {}))
    orientation = str(config.get("orientation", "X")).upper()
    active_axes = list(config.get("stress_strain_axes", []))
    if not active_axes:
        active_axes = ["X", "Y"] if "XY" in orientation else ["Y"] if orientation == "Y" else ["X"]
    axis_columns = {
        axis: list(columns)
        for axis, columns in config.get("axis_position_columns", {}).items()
    }
    position_columns = list(config.get("position_columns", []))
    for axis in active_axes:
        if axis not in axis_columns:
            axis_columns[axis] = position_columns
    return geometry, active_axes, axis_columns


def _plot_stress_strain(
    path: Path,
    experiment_id: str,
    table: pd.DataFrame,
    analyses: dict,
    smoothing_window: int = 5,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(8, 6), dpi=160)
    colors = {"X": "#1f4e79", "Y": "#b45f06"}
    for direction in ("X", "Y"):
        strain_column = f"{direction}向应变"
        stress_column = f"{direction}向应力/MPa"
        if strain_column not in table or table[strain_column].isna().all():
            continue
        color = colors[direction]
        strain_values = table[strain_column].to_numpy(dtype=float)
        stress_values = table[stress_column].to_numpy(dtype=float)
        plot_window = min(_odd_window(smoothing_window), len(strain_values))
        if plot_window % 2 == 0:
            plot_window -= 1
        if plot_window >= 3:
            strain_values = _moving_average(strain_values, plot_window)
            stress_values = _moving_average(stress_values, plot_window)
        axis.plot(
            strain_values,
            stress_values,
            color=color,
            linewidth=1.3,
            label=f"{direction}方向（平滑显示）" if plot_window >= 3 else f"{direction}方向",
        )
        analysis = analyses.get(direction)
        if analysis is None:
            continue
        end = analysis.linear_end_index + 1
        axis.plot(
            table[strain_column].iloc[:end],
            analysis.linear_slope * table[strain_column].iloc[:end] + analysis.linear_intercept,
            color=color,
            linestyle="--",
            linewidth=1.0,
            label=f"{direction}线性拟合，R²={analysis.linear_r2:.3f}",
        )
        if analysis.yield_index is not None:
            axis.scatter(
                [analysis.yield_strain],
                [analysis.yield_stress],
                color=color,
                marker="o",
                s=28,
                label=f"{direction}屈服候选",
            )
    axis.set_title(f"PA12 名义应力—应变曲线：{experiment_id}")
    axis.set_xlabel("工程应变")
    axis.set_ylabel("名义应力/MPa")
    axis.grid(True, alpha=0.2)
    axis.legend(fontsize=8, loc="best")
    figure.tight_layout()
    figure.savefig(path)
    plt.close(figure)


def _write_stress_strain_analysis(
    path: Path,
    experiment_id: str,
    geometry: dict[str, float],
    analyses: dict,
) -> None:
    area = geometry["specimen_width_mm"] * geometry["thickness_mm"]
    lines = [
        f"# {experiment_id} 应力—应变分析",
        "",
        "## 计算口径",
        "",
        f"- 试样有效宽度：`{geometry['specimen_width_mm']:.3f} mm`。",
        f"- 中心测量区厚度：`{geometry['thickness_mm']:.3f} mm`（论文最终优化参数）。",
        f"- 试样总厚度：`{geometry.get('overall_thickness_mm', 'UNKNOWN'):.3f} mm`（几何图示推定值，不用于中心名义截面积）。",
        f"- 标距：`{geometry['gauge_length_mm']:.3f} mm`（论文中心测量区工作标距）。",
        f"- 名义截面积：`{area:.3f} mm²`。",
        "- 名义应力 = 同步力 / 名义截面积；工程应变 = 双侧相对位移 / 标距。",
        "- 工程应变的派生位移使用两侧相对位移的累计加载包络 `maximum.accumulate`；原始 Pos 数据不改写。该规则只适用于当前拉伸至断裂的单调加载段。",
        "- PNG 曲线使用小窗口移动平均仅改善显示连续性；CSV 和同步力值不做平滑改写。",
        "- 该结果用于曲线审核和 MatchID VFM 前置检查，不代表已完成材料参数识别。",
        "",
        "## 曲线判断",
        "",
    ]
    for direction in ("X", "Y"):
        analysis = analyses.get(direction)
        if analysis is None:
            lines.append(f"- {direction}方向：有效点数不足 5，未进行线性段和屈服候选判定。")
            continue
        lines.append(
            f"- {direction}方向：线性拟合斜率 `{analysis.linear_slope:.6g} MPa`，R²=`{analysis.linear_r2:.6f}`。"
        )
        if analysis.yield_index is None:
            lines.append(f"  - 未识别出持续偏离线性段的屈服候选点；未强行标注。")
        else:
            lines.append(
                f"  - 屈服候选：应变 `{analysis.yield_strain:.6g}`，应力 `{analysis.yield_stress:.6g} MPa`；仅作候选点。"
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _device_displacement(
    position: pd.DataFrame | None,
    force_time: np.ndarray,
    start_time: float,
    fracture_time: float,
    columns: list[str],
    *,
    displacement_definition: str = "two_grip_relative_sum",
) -> float | None:
    if position is None:
        return None
    if displacement_definition != "two_grip_relative_sum":
        raise ValueError(f"未知 displacement_definition：{displacement_definition}")
    position_time = _numeric_column(position, "T")
    _require_strictly_increasing("位移时间", position_time)
    values = np.column_stack([_numeric_column(position, column) for column in columns])
    start = np.array(
        [np.interp(start_time, position_time, values[:, i]) for i in range(values.shape[1])],
        dtype=float,
    )
    end = np.array(
        [np.interp(fracture_time, position_time, values[:, i]) for i in range(values.shape[1])],
        dtype=float,
    )
    return float(np.sum(np.abs(end - start)))


def _plot_check(
    path: Path,
    experiment_id: str,
    force_time: np.ndarray,
    raw_x: np.ndarray,
    raw_y: np.ndarray,
    corrected_x: np.ndarray,
    corrected_y: np.ndarray,
    photo_time: np.ndarray,
    photo_x: np.ndarray,
    photo_y: np.ndarray,
    start_time: float,
    peak_time: float,
    fracture_time: float,
    end_event_label: str,
    *,
    visual_fracture_time: float | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(12, 6), dpi=160)
    axis.plot(force_time, raw_x, color="#4c78a8", alpha=0.28, linewidth=0.8, label="X 原始")
    axis.plot(force_time, raw_y, color="#f58518", alpha=0.28, linewidth=0.8, label="Y 原始")
    axis.plot(force_time, corrected_x, color="#1f4e79", linewidth=1.2, label="X 校正后")
    axis.plot(force_time, corrected_y, color="#b45f06", linewidth=1.2, label="Y 校正后")
    axis.scatter(photo_time, photo_x, s=8, color="#1f4e79", alpha=0.65, label="照片时刻 X")
    axis.scatter(photo_time, photo_y, s=8, color="#b45f06", alpha=0.65, label="照片时刻 Y")
    axis.axvspan(start_time, fracture_time, color="#6aa84f", alpha=0.12, label="最终采用区间")
    axis.axvline(start_time, color="#38761d", linestyle="--", linewidth=1.0, label="加载起点")
    axis.axvline(peak_time, color="#674ea7", linestyle="--", linewidth=1.0, label="峰值")
    axis.axvline(fracture_time, color="#cc0000", linestyle="--", linewidth=1.0, label=end_event_label)
    if visual_fracture_time is not None:
        axis.axvline(
            visual_fracture_time,
            color="#990000",
            linestyle=":",
            linewidth=1.2,
            label="估算视觉断裂时刻（力值缺失）",
        )
        left = min(float(force_time[0]), visual_fracture_time)
        right = max(float(force_time[-1]), visual_fracture_time)
        padding = (right - left) * 0.02
        axis.set_xlim(left - padding, right + padding)
    axis.set_title(f"PA12 实验检查图：{experiment_id}")
    axis.set_xlabel("时间/s")
    axis.set_ylabel("力/N")
    axis.grid(True, alpha=0.2)
    axis.legend(ncol=3, fontsize=8, loc="best")
    figure.tight_layout()
    figure.savefig(path)
    plt.close(figure)


def _write_report(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    endpoint_photo_label = (
        "断裂前最后有力照片"
        if report.get("visual_fracture_confirmed")
        else "断裂照片"
        if report.get("fracture_event_confirmed")
        else "有效区间末照片（未确认断裂）"
    )
    lines = [
        f"# {report['experiment_id']} 处理报告",
        "",
        "## 结果",
        "",
        f"- 加载起始力数据索引：`{report['force_start_index']}`，时间 `{report['force_start_time']:.6f} s`。",
        f"- 峰值力数据索引：`{report['force_peak_index']}`，时间 `{report['force_peak_time']:.6f} s`。",
        f"- {report['end_event_label']}对应的力数据索引：`{report['force_fracture_index']}`，时间 `{report['force_fracture_time']:.6f} s`。",
        f"- 起始照片：`{report['first_image']}`。",
        f"- {endpoint_photo_label}：`{report['last_image']}`。",
        f"- 有效照片数量：`{report['photo_count']}`。",
        f"- 按 DIC 审计排除的照片帧：`{summarize_frame_numbers(report.get('excluded_frame_numbers', []))}`；数量 `{len(report.get('excluded_frame_numbers', []))}`。",
        f"- 排除原因：{report.get('excluded_frame_reason', '无')}。",
        f"- 实际照片频率：`{report['camera_actual_fps']:.6f} Hz`。",
        f"- 有效实验时间：`{report['effective_time']:.6f} s`。",
        f"- 照片位移（按加载速度×有效时间推算）：`{report['photo_displacement']:.6f} mm`。",
        f"- 力数据位移（Pos 设备通道）：`{report['force_displacement']:.6f} mm`。",
        f"- 应力—应变表：`{report.get('stress_strain_path', '未生成')}`。",
        f"- 应力—应变图：`{report.get('stress_strain_plot_path', '未生成')}`。",
        "",
        "## 同步方法",
        "",
        f"- 照片时间来源：{report['photo_time_method']}。",
        f"- X/Y 力值：同一组照片时间点分别插值，时间轴完全相同。",
        f"- X/Y 通道：X=`X1_Press、X2_Press` 平均，Y=`Y1_Press、Y2_Press` 平均。",
        f"- 零点：X 基线 `{report['baseline_x']:.6f}`，Y 基线 `{report['baseline_y']:.6f}`；首行校正值强制归零。",
        f"- 力符号系数：`{report['force_sign']}`；按拉伸力正值约定输出，首行校正值强制归零。",
        "",
        "## 数量门禁",
        "",
        f"- 照片数量：`{report['photo_count']}`。",
        f"- X VFM 数量：`{report['x_count']}`。",
        f"- Y VFM 数量：`{report['y_count']}`。",
        f"- 正式 VFM 输出：**{'允许' if report['vfm_allowed'] else '禁止'}**。",
        f"- 配置发布许可：{'允许' if report['formal_vfm_allowed'] else '诊断模式，禁止'}。",
        "",
        "## 自动检查",
        "",
        f"- 力时间严格递增：{'通过' if report['force_time_monotonic'] else '失败'}。",
        f"- 照片时间严格递增：{'通过' if report['photo_time_monotonic'] else '失败'}。",
        f"- X/Y 使用同一时间轴：{'通过' if report['xy_same_time_axis'] else '失败'}。",
        f"- 插值结果含 NaN：{'是' if report['interpolation_nan'] else '否'}。",
        f"- 首行接近零力：{'通过' if report['first_row_zero'] else '失败'}。",
        f"- 校正后 X/Y 力均非负（诊断）：{'通过' if report['nonnegative_forces'] else '存在负值；保留真实校正结果'}。",
        f"- 断裂/终点判定：`{report['end_event_label']}`。",
        f"- X1/X2 最大差值：`{report['x_channel_max_difference']:.6f}`。",
        f"- Y1/Y2 最大差值：`{report['y_channel_max_difference']:.6f}`。",
        f"- JPG 缺 DAT：`{report['missing_dat_count']}` 个；孤立 DAT：`{report['orphan_dat_count']}` 个。",
        f"- JPG 帧号缺口：`{summarize_frame_numbers(report['image_sequence_gaps'])}`；DAT 帧号缺口：`{summarize_frame_numbers(report['dat_sequence_gaps'])}`。",
        f"- 有效照片区间内帧号缺口：`{summarize_frame_numbers(report['selected_sequence_gaps'])}`；稀疏序列中的缺口表示未导出的帧，不表示程序补帧失败。",
        f"- 位移定义：`{report.get('displacement_definition', 'two_grip_relative_sum')}`；当前按两侧位置增量绝对值之和计算相对位移。",
        f"- 派生应力—应变位移包络：`{'启用' if report.get('monotonic_displacement_envelope') else '未启用'}`；原始 Pos 不修改。",
        f"- 非加载方向是否置零：`{'是' if report.get('inactive_force_axes_zeroed') else '否'}`；仅对单轴配置执行，主动方向仍保留校正后的真实力值。",
        f"- 应力—应变几何：宽度 `{report.get('specimen_width_mm', 'UNKNOWN')}` mm，厚度 `{report.get('thickness_mm', 'UNKNOWN')}` mm，标距 `{report.get('gauge_length_mm', 'UNKNOWN')}` mm。",
        "",
        "## 已知限制",
        "",
        "- JPG 没有可靠 EXIF 拍摄时间，本次用力数据有效区间和相机设置频率确定首尾候选帧，再按实际帧号间隔将有效区间映射到配对照片。",
        "- 原始 `Press` 通道在本批处理中的加载方向为负；VFM 输出按 `F_corrected = -(F_raw - F_baseline)` 转为拉伸正值。",
        "- 当前名义应力—应变使用 Pos 设备位移；尚未从 DAT 全场字段导出 DIC 位移，因此不能称为 DIC 位移曲线。",
        "- 本阶段已生成名义应力—应变审核结果，但尚未进入 MatchID VFM 识别或材料参数拟合。",
    ]
    if report.get("visual_fracture_confirmed"):
        lines += [
            "",
            "## 视觉断裂与力数据边界",
            "",
            f"- 视觉断裂照片：`{report.get('visual_fracture_frame', 'UNKNOWN')}`。",
            f"- 断裂前最后有力照片：`{report.get('last_force_supported_photo', 'UNKNOWN')}`。",
            f"- 视觉断裂照片时间估计：`{report.get('visual_fracture_time_estimate', 'UNKNOWN')}` s；按有效区间照片帧号和实际照片频率外推。",
            "- 视觉断裂时刻的力值：缺失；力文件在视觉断裂前结束。",
            "- 不使用末点力值、外推或人工掉载补齐断裂力；该实验不发布正式 VFM。",
        ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def process_experiment(config: dict) -> dict:
    experiment_id = str(config["experiment_id"])
    image_folder = Path(config["image_folder"])
    force_file = Path(config["force_file"])
    output_root = Path(config["output_root"])
    camera_setting_fps = float(config["camera_setting_fps"])
    loading_speed = float(config["loading_speed"])
    force_sign = float(config.get("force_sign", -1.0))
    x_columns = list(config.get("x_press_columns", ["X1_Press", "X2_Press"]))
    y_columns = list(config.get("y_press_columns", ["Y1_Press", "Y2_Press"]))

    frames = discover_frames(image_folder)
    press, position = _read_force_tables(config)
    force_time = _numeric_column(press, config.get("time_column", "T"))
    _require_strictly_increasing("力时间", force_time)
    raw_x, raw_y = average_press_channels(press, x_columns, y_columns)
    _require_numeric_array("X 原始力", raw_x)
    _require_numeric_array("Y 原始力", raw_y)

    manual = config.get("manual", {})
    manual_start_index = (
        int(manual["force_start_index"]) if "force_start_index" in manual else None
    )
    analysis_end_key = (
        "force_analysis_end_index"
        if "force_analysis_end_index" in manual
        else "force_fracture_index"
    )
    manual_fracture_index = (
        int(manual[analysis_end_key]) if analysis_end_key in manual else None
    )
    detector_config = config.get("detector", {})
    events = detect_force_events(
        force_time,
        raw_x,
        raw_y,
        baseline_window_s=float(detector_config.get("baseline_window_s", 0.05)),
        start_threshold_n=float(detector_config.get("start_threshold_n", 5.0)),
        persistence_s=float(detector_config.get("persistence_s", 0.05)),
        fracture_fraction=float(detector_config.get("fracture_fraction", 0.2)),
        smoothing_window_s=float(detector_config.get("smoothing_window_s", 0.05)),
        manual_start_index=manual_start_index,
        manual_fracture_index=manual_fracture_index,
    )

    start_index = events.start_index
    fracture_index = events.fracture_index
    if start_index < 0 or fracture_index >= len(force_time) or start_index >= fracture_index:
        raise ValueError("人工指定的力数据区间无效")
    start_time = float(force_time[start_index])
    fracture_time = float(force_time[fracture_index])

    excluded_frame_numbers = sorted({int(number) for number in config.get("excluded_frame_numbers", [])})
    excluded_frame_set = set(excluded_frame_numbers)
    paired_numbers = [frame.number for frame in frames.paired]
    exif_photo_time = read_exif_capture_offsets(
        [image_folder / frame.image_name for frame in frames.paired]
    )
    if "start_frame" in manual:
        start_frame = int(manual["start_frame"])
    else:
        start_frame = None
    if "end_frame" in manual:
        end_frame = int(manual["end_frame"])
    else:
        end_frame = None
    if start_frame is not None or end_frame is not None:
        if start_frame is None or end_frame is None:
            raise ValueError("人工照片覆盖必须同时提供 start_frame 和 end_frame")
        timeline_numbers = list(range(start_frame, end_frame + 1))
        timeline_time = photo_time_from_frame_numbers(
            timeline_numbers,
            start_time=start_time,
            fracture_time=fracture_time,
            camera_setting_fps=camera_setting_fps,
        )
        selected_numbers = [
            number for number in timeline_numbers if number not in excluded_frame_set
        ]
        time_by_number = dict(zip(timeline_numbers, timeline_time))
        photo_time = np.asarray([time_by_number[number] for number in selected_numbers], dtype=float)
        photo_time_method = "JSON 中的人工照片帧范围；时间在力数据加载起点和断裂点之间均匀分配"
    elif exif_photo_time is not None:
        exif_selection = select_frames_from_capture_offsets(
            paired_numbers,
            exif_photo_time,
            load_start_time=start_time,
            fracture_time=fracture_time,
        )
        if exif_selection is None:
            timeline_numbers = select_frame_numbers(
                paired_numbers,
                load_start_time=start_time,
                fracture_time=fracture_time,
                camera_setting_fps=camera_setting_fps,
            )
            timeline_time = photo_time_from_frame_numbers(
                timeline_numbers,
                start_time=start_time,
                fracture_time=fracture_time,
                camera_setting_fps=camera_setting_fps,
            )
            selected_numbers = [
                number for number in timeline_numbers if number not in excluded_frame_set
            ]
            time_by_number = dict(zip(timeline_numbers, timeline_time))
            photo_time = np.asarray([time_by_number[number] for number in selected_numbers], dtype=float)
            photo_time_method = "EXIF 时间不可用于有效区间；按实际帧号间隔归一化到有效力时间区间"
        else:
            timeline_numbers, timeline_time = exif_selection
            selected_mask = np.asarray(
                [number not in excluded_frame_set for number in timeline_numbers],
                dtype=bool,
            )
            selected_numbers = [
                number for number in timeline_numbers if number not in excluded_frame_set
            ]
            photo_time = timeline_time[selected_mask]
            photo_time_method = "可靠 EXIF 拍摄时间差；以力数据加载起点和断裂点归一化照片时间轴"
    else:
        timeline_numbers = select_frame_numbers(
            paired_numbers,
            load_start_time=start_time,
            fracture_time=fracture_time,
            camera_setting_fps=camera_setting_fps,
        )
        timeline_time = photo_time_from_frame_numbers(
            timeline_numbers,
            start_time=start_time,
            fracture_time=fracture_time,
            camera_setting_fps=camera_setting_fps,
        )
        selected_numbers = [
            number for number in timeline_numbers if number not in excluded_frame_set
        ]
        time_by_number = dict(zip(timeline_numbers, timeline_time))
        photo_time = np.asarray([time_by_number[number] for number in selected_numbers], dtype=float)
        photo_time_method = "无可靠 EXIF；按实际帧号间隔归一化到有效力时间区间"

    paired_by_number = {frame.number: frame for frame in frames.paired}
    missing_selected = [number for number in selected_numbers if number not in paired_by_number]
    if missing_selected:
        raise VFMOutputBlocked(f"有效照片区间内缺少 JPG/DAT 配对帧：{missing_selected[:10]}")
    selected_frames = [paired_by_number[number] for number in selected_numbers]
    if len(selected_frames) < 2:
        raise ValueError("有效照片数量少于 2，不能建立照片时间轴")

    interpolated = interpolate_force_values(
        force_time,
        raw_x,
        raw_y,
        photo_time,
        baseline_x=events.baseline_x,
        baseline_y=events.baseline_y,
        force_sign=force_sign,
    )

    geometry, active_axes, axis_position_columns = _stress_strain_settings(config)
    inactive_force_axes_zeroed = bool(config.get("zero_inactive_force_axes", False))
    if inactive_force_axes_zeroed:
        output_x = interpolated.x.copy()
        output_y = interpolated.y.copy()
        if "X" not in active_axes:
            output_x.fill(0.0)
        if "Y" not in active_axes:
            output_y.fill(0.0)
        interpolated = InterpolatedForces(
            photo_time=interpolated.photo_time,
            x=output_x,
            y=output_y,
        )

    force_corrected_x = (raw_x - events.baseline_x) * force_sign
    force_corrected_y = (raw_y - events.baseline_y) * force_sign
    force_displacement = _device_displacement(
        position,
        force_time,
        start_time,
        fracture_time,
        list(config.get("position_columns", ["X1_Pos", "X2_Pos", "Y1_Pos", "Y2_Pos"])),
        displacement_definition=str(config.get("displacement_definition", "two_grip_relative_sum")),
    )
    effective_time = fracture_time - start_time
    displacement_mode = config.get("displacement_mode", "velocity")
    if displacement_mode == "device":
        if force_displacement is None:
            raise ValueError("displacement_mode=device 但没有可用设备位移")
        photo_displacement = loading_speed * effective_time
    elif displacement_mode == "velocity":
        photo_displacement = loading_speed * effective_time
        if force_displacement is None:
            force_displacement = photo_displacement
    else:
        raise ValueError(f"未知 displacement_mode：{displacement_mode}")

    stress_strain_table = None
    curve_analyses = {}
    monotonic_displacement_envelope = bool(
        config.get("monotonic_displacement_envelope", True)
    )
    if position is not None:
        stress_strain_table, curve_analyses = build_nominal_stress_strain_table(
            [frame.image_name for frame in selected_frames],
            interpolated.photo_time,
            interpolated.x,
            interpolated.y,
            position,
            axis_position_columns,
            geometry,
            active_axes,
            monotonic_displacement_envelope=monotonic_displacement_envelope,
        )

    camera_actual_fps = (selected_numbers[-1] - selected_numbers[0]) / effective_time
    visual_fracture_frame = config.get("visual_fracture_frame")
    visual_fracture_time_estimate = None
    if visual_fracture_frame:
        visual_fracture_number = _parse_frame_number(str(visual_fracture_frame))
        visual_fracture_time_estimate = float(
            photo_time[-1]
            + (visual_fracture_number - selected_numbers[-1]) / camera_actual_fps
        )
    x_channel_values = press[x_columns].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    y_channel_values = press[y_columns].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    x_channel_difference = float(np.max(np.abs(x_channel_values[:, 0] - x_channel_values[:, 1])))
    y_channel_difference = float(np.max(np.abs(y_channel_values[:, 0] - y_channel_values[:, 1])))
    interpolation_nan = bool(np.isnan(interpolated.x).any() or np.isnan(interpolated.y).any())
    force_time_monotonic = bool(np.all(np.diff(force_time) > 0))
    photo_time_monotonic = bool(np.all(np.diff(interpolated.photo_time) > 0))
    xy_same_time_axis = shared_photo_time_axis(photo_time, interpolated.photo_time)
    first_row_zero = bool(abs(interpolated.x[0]) < 1e-12 and abs(interpolated.y[0]) < 1e-12)
    manual_event_override = manual_start_index is not None or manual_fracture_index is not None
    drop_detected = bool(
        events.peak_magnitude > 0
        and events.fracture_magnitude
        <= events.peak_magnitude * float(detector_config.get("fracture_fraction", 0.2))
    )
    manual_fracture_confirmed = bool(config.get("manual_fracture_confirmed", False))
    fracture_event_confirmed = drop_detected or manual_fracture_confirmed
    visual_fracture_confirmed = bool(config.get("visual_fracture_confirmed", False))
    force_missing_at_visual_fracture = bool(
        config.get("force_missing_at_visual_fracture", False)
    )
    end_event_label = (
        "自动掉载"
        if drop_detected and not manual_fracture_confirmed
        else "人工确认断裂"
        if manual_fracture_confirmed
        else str(config.get("end_event_label", "未确认断裂"))
    )

    selected_sequence_gaps = [
        number for number in range(selected_numbers[0], selected_numbers[-1] + 1)
        if number not in set(selected_numbers)
    ]
    formal_vfm_allowed = bool(config.get("formal_vfm_allowed", True))
    vfm_allowed = False
    vfm_error = None
    nonnegative_forces = bool(
        np.all(interpolated.x >= -1e-12) and np.all(interpolated.y >= -1e-12)
    )
    try:
        validate_vfm_lengths(len(selected_frames), len(interpolated.x), len(interpolated.y))
        if not formal_vfm_allowed:
            raise VFMOutputBlocked("当前配置为诊断模式，禁止发布正式 VFM")
        validate_active_vfm_forces(interpolated.x, interpolated.y, active_axes)
        if interpolation_nan or not force_time_monotonic or not photo_time_monotonic or not first_row_zero or not fracture_event_confirmed:
            raise VFMOutputBlocked("自动检查未全部通过")
        vfm_allowed = True
    except VFMOutputBlocked as error:
        vfm_error = str(error)

    agent_root = output_root / "Agents" / "PA12实验数据处理"
    safe_id = _safe_filename(experiment_id)
    overview_path = agent_root / "实验概览" / f"{safe_id}_实验概览.csv"
    match_path = agent_root / "照片力匹配" / f"{safe_id}_照片-力对应表.csv"
    plot_path = agent_root / "检查图" / f"{safe_id}_检查图.png"
    stress_strain_path = agent_root / "应力应变" / f"{safe_id}_应力应变.csv"
    stress_strain_plot_path = agent_root / "应力应变" / f"{safe_id}_应力应变.png"
    stress_strain_report_path = agent_root / "应力应变" / f"{safe_id}_应力应变分析.md"
    report_path = agent_root / "处理记录" / f"{safe_id}_处理报告.md"
    config_path = agent_root / "处理记录" / f"{safe_id}_配置.json"
    speed_label = str(config.get("speed_label", loading_speed))
    x_vfm_path = agent_root / "VFM专用力值" / "X方向" / f"X-{speed_label}-{len(selected_frames)}.csv"
    y_vfm_path = agent_root / "VFM专用力值" / "Y方向" / f"Y-{speed_label}-{len(selected_frames)}.csv"

    _write_match_table(match_path, selected_frames, interpolated, bool(config.get("include_time", True)))
    _write_overview(
        overview_path,
        {
            "速度": f"{loading_speed:g} mm/s",
            "照片数量": str(len(selected_frames)),
            "设置频率": f"{camera_setting_fps:g} Hz",
            "实际频率": f"{camera_actual_fps:.3f} Hz",
            "照片位移": f"{photo_displacement:.4f} mm",
            "力数量": str(len(interpolated.x)),
            "力位移": f"{force_displacement:.4f} mm",
            "力数据时间": f"{effective_time:.4f} s",
            "力传感频率": f"{1.0 / np.median(np.diff(force_time)):.3f} Hz",
        },
    )
    _plot_check(
        plot_path,
        experiment_id,
        force_time,
        raw_x,
        raw_y,
        force_corrected_x,
        force_corrected_y,
        interpolated.photo_time,
        interpolated.x,
        interpolated.y,
        start_time,
        float(force_time[events.peak_index]),
        fracture_time,
        end_event_label,
        visual_fracture_time=visual_fracture_time_estimate,
    )
    if stress_strain_table is not None:
        stress_strain_path.parent.mkdir(parents=True, exist_ok=True)
        stress_strain_table.to_csv(stress_strain_path, index=False, encoding="utf-8-sig")
        _plot_stress_strain(
            stress_strain_plot_path,
            experiment_id,
            stress_strain_table,
            curve_analyses,
            int(config.get("plot_smoothing_window", 5)),
        )
        _write_stress_strain_analysis(
            stress_strain_report_path,
            experiment_id,
            geometry,
            curve_analyses,
        )

    if vfm_allowed:
        _write_vfm(x_vfm_path, interpolated.x)
        _write_vfm(y_vfm_path, interpolated.y)

    report = {
        "experiment_id": experiment_id,
        "force_start_index": start_index,
        "force_start_time": start_time,
        "force_peak_index": events.peak_index,
        "force_peak_time": float(force_time[events.peak_index]),
        "force_fracture_index": fracture_index,
        "force_analysis_end_index": fracture_index,
        "force_fracture_time": fracture_time,
        "first_image": selected_frames[0].image_name,
        "last_image": selected_frames[-1].image_name,
        "photo_count": len(selected_frames),
        "x_count": len(interpolated.x),
        "y_count": len(interpolated.y),
        "camera_actual_fps": camera_actual_fps,
        "effective_time": effective_time,
        "photo_displacement": photo_displacement,
        "force_displacement": force_displacement,
        "photo_time_method": photo_time_method,
        "baseline_x": events.baseline_x,
        "baseline_y": events.baseline_y,
        "force_sign": force_sign,
        "formal_vfm_allowed": formal_vfm_allowed,
        "vfm_allowed": vfm_allowed,
        "vfm_error": vfm_error,
        "force_time_monotonic": force_time_monotonic,
        "photo_time_monotonic": photo_time_monotonic,
        "xy_same_time_axis": xy_same_time_axis,
        "interpolation_nan": interpolation_nan,
        "first_row_zero": first_row_zero,
        "nonnegative_forces": nonnegative_forces,
        "drop_detected": drop_detected,
        "fracture_event_confirmed": fracture_event_confirmed,
        "end_event_label": end_event_label,
        "manual_event_override": manual_event_override,
        "visual_fracture_confirmed": visual_fracture_confirmed,
        "visual_fracture_frame": config.get("visual_fracture_frame", "UNKNOWN"),
        "visual_fracture_time_estimate": visual_fracture_time_estimate,
        "last_force_supported_photo": config.get("last_force_supported_photo", "UNKNOWN"),
        "force_missing_at_visual_fracture": force_missing_at_visual_fracture,
        "monotonic_displacement_envelope": monotonic_displacement_envelope,
        "inactive_force_axes_zeroed": inactive_force_axes_zeroed,
        "x_channel_max_difference": x_channel_difference,
        "y_channel_max_difference": y_channel_difference,
        "missing_dat_count": len(frames.missing_dat),
        "orphan_dat_count": len(frames.orphan_dat),
        "image_sequence_gaps": list(frames.image_sequence_gaps),
        "dat_sequence_gaps": list(frames.dat_sequence_gaps),
        "selected_sequence_gaps": selected_sequence_gaps,
        "excluded_frame_numbers": excluded_frame_numbers,
        "excluded_frame_reason": str(config.get("excluded_frame_reason", "无")),
        "stress_strain_path": str(stress_strain_path) if stress_strain_table is not None else "未生成",
        "stress_strain_plot_path": str(stress_strain_plot_path) if stress_strain_table is not None else "未生成",
        "displacement_definition": str(config.get("displacement_definition", "two_grip_relative_sum")),
        "specimen_width_mm": geometry["specimen_width_mm"],
        "thickness_mm": geometry["thickness_mm"],
        "gauge_length_mm": geometry["gauge_length_mm"],
        "stress_strain_available": stress_strain_table is not None,
        "stress_strain_geometry": geometry,
        "stress_strain_axes": active_axes,
        "curve_analyses": curve_analyses,
    }
    _write_report(report_path, report)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "experiment_id": experiment_id,
        "first_image": selected_frames[0].image_name,
        "last_image": selected_frames[-1].image_name,
        "photo_count": len(selected_frames),
        "force_start_index": start_index,
        "force_peak_index": events.peak_index,
        "force_fracture_index": fracture_index,
        "force_analysis_end_index": fracture_index,
        "camera_actual_fps": camera_actual_fps,
        "effective_time": effective_time,
        "photo_displacement": photo_displacement,
        "force_displacement": force_displacement,
        "overview_row": {
            "速度": f"{loading_speed:g} mm/s",
            "照片数量": str(len(selected_frames)),
            "设置频率": f"{camera_setting_fps:g} Hz",
            "实际频率": f"{camera_actual_fps:.3f} Hz",
            "照片位移": f"{photo_displacement:.4f} mm",
            "力数量": str(len(interpolated.x)),
            "力位移": f"{force_displacement:.4f} mm",
            "力数据时间": f"{effective_time:.4f} s",
            "力传感频率": f"{1.0 / np.median(np.diff(force_time)):.3f} Hz",
        },
        "formal_vfm_allowed": formal_vfm_allowed,
        "vfm_allowed": vfm_allowed,
        "vfm_error": vfm_error,
        "drop_detected": drop_detected,
        "fracture_event_confirmed": fracture_event_confirmed,
        "end_event_label": end_event_label,
        "visual_fracture_confirmed": visual_fracture_confirmed,
        "visual_fracture_frame": config.get("visual_fracture_frame", "UNKNOWN"),
        "visual_fracture_time_estimate": visual_fracture_time_estimate,
        "last_force_supported_photo": config.get("last_force_supported_photo", "UNKNOWN"),
        "force_missing_at_visual_fracture": force_missing_at_visual_fracture,
        "inactive_force_axes_zeroed": inactive_force_axes_zeroed,
        "overview": str(overview_path),
        "match": str(match_path),
        "x_vfm": str(x_vfm_path) if vfm_allowed else None,
        "y_vfm": str(y_vfm_path) if vfm_allowed else None,
        "plot": str(plot_path),
        "stress_strain": str(stress_strain_path) if stress_strain_table is not None else None,
        "stress_strain_plot": str(stress_strain_plot_path) if stress_strain_table is not None else None,
        "stress_strain_report": str(stress_strain_report_path) if stress_strain_table is not None else None,
        "excluded_frame_numbers": excluded_frame_numbers,
        "excluded_frame_reason": str(config.get("excluded_frame_reason", "无")),
        "report": str(report_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="PA12 照片—力数据同步与 VFM 生成")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    result = process_experiment(config)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
