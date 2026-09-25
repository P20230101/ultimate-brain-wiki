from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CurveAnalysis:
    linear_start_index: int
    linear_end_index: int
    linear_slope: float
    linear_intercept: float
    linear_r2: float
    yield_index: int | None
    yield_strain: float | None
    yield_stress: float | None


def relative_displacement(
    position: pd.DataFrame,
    photo_time: np.ndarray,
    columns: list[str] | tuple[str, ...],
    *,
    monotonic_envelope: bool = True,
) -> np.ndarray:
    position_time = pd.to_numeric(position["T"], errors="coerce").to_numpy(dtype=float)
    values = np.column_stack(
        [pd.to_numeric(position[column], errors="coerce").to_numpy(dtype=float) for column in columns]
    )
    photo_time = np.asarray(photo_time, dtype=float)
    if len(position_time) < 2 or not np.isfinite(position_time).all() or not np.all(np.diff(position_time) > 0):
        raise ValueError("位移时间必须严格递增且为有限值")
    if not np.isfinite(values).all():
        raise ValueError("位移列包含 NaN 或无穷值")
    if len(photo_time) < 1 or not np.isfinite(photo_time).all() or not np.all(np.diff(photo_time) > 0):
        raise ValueError("照片时间必须严格递增且为有限值")
    if photo_time[0] < position_time[0] or photo_time[-1] > position_time[-1]:
        raise ValueError("照片时间超出位移数据时间范围")

    sampled = np.column_stack(
        [np.interp(photo_time, position_time, values[:, index]) for index in range(values.shape[1])]
    )
    displacement = np.sum(np.abs(sampled - sampled[0]), axis=1)
    # Pos is a measured input and is not changed. The derived curve represents
    # monotonic loading, so small measurement retraces use a loading envelope.
    return np.maximum.accumulate(displacement) if monotonic_envelope else displacement


def _r2(observed: np.ndarray, predicted: np.ndarray) -> float:
    residual = observed - predicted
    total = np.sum((observed - np.mean(observed)) ** 2)
    if total == 0.0:
        return 1.0 if np.allclose(residual, 0.0) else 0.0
    return float(1.0 - np.sum(residual**2) / total)


def analyze_curve(
    strain: np.ndarray,
    stress: np.ndarray,
    *,
    linear_fraction: float = 0.25,
    yield_deviation_fraction: float = 0.05,
    yield_persistence: int = 3,
) -> CurveAnalysis:
    strain = np.asarray(strain, dtype=float)
    stress = np.asarray(stress, dtype=float)
    if len(strain) != len(stress) or len(strain) < 5:
        raise ValueError("应变和应力必须长度相同且至少包含 5 个点")
    if not np.isfinite(strain).all() or not np.isfinite(stress).all():
        raise ValueError("应力—应变数据包含 NaN 或无穷值")
    if not 0.0 < linear_fraction < 1.0:
        raise ValueError("linear_fraction 必须在 0 和 1 之间")
    if not 0.0 < yield_deviation_fraction < 1.0:
        raise ValueError("yield_deviation_fraction 必须在 0 和 1 之间")
    if yield_persistence < 1:
        raise ValueError("yield_persistence 必须为正整数")

    peak_index = int(np.argmax(stress))
    linear_end_index = max(2, int(round(peak_index * linear_fraction)))
    linear_end_index = min(linear_end_index, len(strain) - 1)
    coefficients = np.polyfit(strain[: linear_end_index + 1], stress[: linear_end_index + 1], 1)
    predicted = np.polyval(coefficients, strain)
    linear_r2 = _r2(stress[: linear_end_index + 1], predicted[: linear_end_index + 1])

    threshold = max(abs(float(np.max(stress))) * yield_deviation_fraction, 1e-9)
    deviated = np.abs(stress - predicted) >= threshold
    yield_index: int | None = None
    for index in range(linear_end_index + 1, len(strain) - yield_persistence + 1):
        if bool(np.all(deviated[index : index + yield_persistence])):
            yield_index = index
            break

    return CurveAnalysis(
        linear_start_index=0,
        linear_end_index=linear_end_index,
        linear_slope=float(coefficients[0]),
        linear_intercept=float(coefficients[1]),
        linear_r2=linear_r2,
        yield_index=yield_index,
        yield_strain=None if yield_index is None else float(strain[yield_index]),
        yield_stress=None if yield_index is None else float(stress[yield_index]),
    )


def build_nominal_stress_strain_table(
    photo_names: list[str] | tuple[str, ...],
    photo_time: np.ndarray,
    force_x: np.ndarray,
    force_y: np.ndarray,
    position: pd.DataFrame,
    position_axes: dict[str, list[str] | tuple[str, ...]],
    geometry: dict[str, float],
    active_axes: list[str] | tuple[str, ...],
    *,
    monotonic_displacement_envelope: bool = True,
) -> tuple[pd.DataFrame, dict[str, CurveAnalysis]]:
    photo_time = np.asarray(photo_time, dtype=float)
    force_x = np.asarray(force_x, dtype=float)
    force_y = np.asarray(force_y, dtype=float)
    if not (len(photo_names) == len(photo_time) == len(force_x) == len(force_y)):
        raise ValueError("照片、时间和 X/Y 力长度必须相同")
    width = float(geometry["specimen_width_mm"])
    thickness = float(geometry["thickness_mm"])
    gauge_length = float(geometry["gauge_length_mm"])
    area = width * thickness
    if area <= 0.0 or gauge_length <= 0.0:
        raise ValueError("几何尺寸必须为正")

    table = pd.DataFrame(
        {
            "照片": list(photo_names),
            "时间/s": photo_time,
            "X向力/N": force_x,
            "Y向力/N": force_y,
        }
    )
    analyses: dict[str, CurveAnalysis] = {}
    for axis, force in (("X", force_x), ("Y", force_y)):
        if axis not in active_axes:
            table[f"{axis}向位移/mm"] = np.nan
            table[f"{axis}向应变"] = np.nan
            table[f"{axis}向应力/MPa"] = np.nan
            continue
        displacement = relative_displacement(
            position,
            photo_time,
            position_axes[axis],
            monotonic_envelope=monotonic_displacement_envelope,
        )
        strain = displacement / gauge_length
        stress = force / area
        table[f"{axis}向位移/mm"] = displacement
        table[f"{axis}向应变"] = strain
        table[f"{axis}向应力/MPa"] = stress
        if len(strain) >= 5:
            analyses[axis] = analyze_curve(strain, stress)
    return table, analyses
