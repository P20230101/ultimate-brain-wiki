from __future__ import annotations

import math
from collections.abc import Sequence

from matplotlib.tri import Triangulation


def plane_stress_virtual_work_coefficients(
    *,
    exx: float,
    eyy: float,
    nu: float,
    area_mm2: float,
    thickness_mm: float,
    length_x_mm: float,
    length_y_mm: float,
) -> tuple[float, float]:
    """Return the X/Y internal virtual-work coefficients per MPa.

    The virtual fields are unit extensions: ``u*=x/Lx`` and ``v*=y/Ly``.
    ``exy`` is a tensor shear strain in the DIC convention and is not used by
    these two constant normal virtual fields.
    """

    if not -1.0 < nu < 0.5:
        raise ValueError("平面应力泊松比必须位于 (-1, 0.5) 内")
    if area_mm2 <= 0 or thickness_mm <= 0 or length_x_mm <= 0 or length_y_mm <= 0:
        raise ValueError("面积、厚度和虚场长度必须为正")
    factor = thickness_mm * area_mm2 / (1.0 - nu * nu)
    coefficient_x = factor / length_x_mm * (exx + nu * eyy)
    coefficient_y = factor / length_y_mm * (eyy + nu * exx)
    return coefficient_x, coefficient_y


def integrate_plane_stress_virtual_work_coefficients(
    *,
    points: Sequence[dict[str, float]],
    nu: float,
    thickness_mm: float,
    length_x_mm: float,
    length_y_mm: float,
    roi_bounds: tuple[float, float, float, float],
) -> dict[str, float | int]:
    """Integrate unit-modulus virtual-work coefficients over valid ROI triangles."""

    if not -1.0 < nu < 0.5:
        raise ValueError("平面应力泊松比必须位于 (-1, 0.5) 内")
    if thickness_mm <= 0 or length_x_mm <= 0 or length_y_mm <= 0:
        raise ValueError("厚度和虚场长度必须为正")
    x_min, x_max, y_min, y_max = roi_bounds
    if x_min >= x_max or y_min >= y_max:
        raise ValueError("ROI边界必须具有正面积")

    valid_points: list[dict[str, float]] = []
    excluded_point_count = 0
    for point in points:
        x = float(point["x"])
        y = float(point["y"])
        exx = float(point["exx"])
        eyy = float(point["eyy"])
        if not all(math.isfinite(value) for value in (x, y, exx, eyy)):
            excluded_point_count += 1
            continue
        if x_min <= x <= x_max and y_min <= y <= y_max:
            valid_points.append({"x": x, "y": y, "exx": exx, "eyy": eyy})
        else:
            excluded_point_count += 1

    if len(valid_points) < 3:
        raise ValueError("ROI内有效点不足以建立三角剖分")

    triangulation = Triangulation(
        [point["x"] for point in valid_points],
        [point["y"] for point in valid_points],
    )
    integrated_area = 0.0
    integrated_x = 0.0
    integrated_y = 0.0
    valid_triangle_count = 0
    for triangle in triangulation.triangles:
        vertices = [valid_points[index] for index in triangle]
        centroid_x = sum(point["x"] for point in vertices) / 3.0
        centroid_y = sum(point["y"] for point in vertices) / 3.0
        if not (x_min <= centroid_x <= x_max and y_min <= centroid_y <= y_max):
            continue
        first, second, third = vertices
        area = abs(
            (
                (second["x"] - first["x"]) * (third["y"] - first["y"])
                - (third["x"] - first["x"]) * (second["y"] - first["y"])
            )
            / 2.0
        )
        if area == 0.0:
            continue
        integrated_area += area
        integrated_x += area * sum(point["exx"] + nu * point["eyy"] for point in vertices) / 3.0
        integrated_y += area * sum(point["eyy"] + nu * point["exx"] for point in vertices) / 3.0
        valid_triangle_count += 1

    if valid_triangle_count == 0:
        raise ValueError("ROI内没有有效三角形")

    factor = thickness_mm / (1.0 - nu * nu)
    rectangle_area = (x_max - x_min) * (y_max - y_min)
    return {
        "coefficient_x": factor * integrated_x / length_x_mm,
        "coefficient_y": factor * integrated_y / length_y_mm,
        "integrated_area_mm2": integrated_area,
        "valid_point_count": len(valid_points),
        "excluded_point_count": excluded_point_count,
        "valid_triangle_count": valid_triangle_count,
        "rectangle_area_mm2": rectangle_area,
        "area_ratio": integrated_area / rectangle_area,
    }


def rotated_machine_axes(
    *,
    exx: float,
    eyy: float,
    length_x_mm: float,
    length_y_mm: float,
) -> dict[str, float]:
    """Map rotated-DIC normal fields and lengths to machine X/Y.

    The project calibration fixes machine X at the rotated top/bottom pair
    and machine Y at the rotated left/right pair.  The helper keeps this
    physical mapping separate from the generic mathematical x/y formulas.
    """

    return {
        "machine_x_strain": eyy,
        "machine_y_strain": exx,
        "machine_x_virtual_length_mm": length_y_mm,
        "machine_y_virtual_length_mm": length_x_mm,
        "machine_x_edge_length_mm": length_x_mm,
        "machine_y_edge_length_mm": length_y_mm,
    }


def equivalent_stress_plane_stress(
    sigma_x_mpa: float,
    sigma_y_mpa: float,
    tau_xy_mpa: float = 0.0,
) -> float:
    """Return plane-stress von Mises equivalent stress in MPa."""

    value = (
        sigma_x_mpa * sigma_x_mpa
        - sigma_x_mpa * sigma_y_mpa
        + sigma_y_mpa * sigma_y_mpa
        + 3.0 * tau_xy_mpa * tau_xy_mpa
    )
    return math.sqrt(max(0.0, value))


def equivalent_plastic_strain_plane_stress(
    *,
    exx: float,
    eyy: float,
    exy: float,
    sigma_x_mpa: float,
    sigma_y_mpa: float,
    modulus_mpa: float,
    nu: float,
) -> float:
    """Estimate J2 equivalent plastic strain from total DIC strain.

    This is the declared phase-2 plane-stress reduction used by the
    self-built pipeline.  It treats the measured in-plane shear stress as
    zero because the present boundary input contains only X/Y resultants.
    Plastic incompressibility supplies ``ep_zz = -(ep_xx + ep_yy)``.
    """

    if modulus_mpa <= 0:
        raise ValueError("弹性模量必须为正")
    elastic_xx = (sigma_x_mpa - nu * sigma_y_mpa) / modulus_mpa
    elastic_yy = (sigma_y_mpa - nu * sigma_x_mpa) / modulus_mpa
    plastic_xx = exx - elastic_xx
    plastic_yy = eyy - elastic_yy
    plastic_zz = -(plastic_xx + plastic_yy)
    value = (2.0 / 3.0) * (
        plastic_xx * plastic_xx
        + plastic_yy * plastic_yy
        + plastic_zz * plastic_zz
        + 2.0 * exy * exy
    )
    return math.sqrt(max(0.0, value))


def fit_elastic_modulus(
    *,
    coefficients: Sequence[float],
    external_forces: Sequence[float],
) -> dict[str, float | int]:
    """Fit ``external_force = E * coefficient`` through the zero origin."""

    if len(coefficients) != len(external_forces) or not coefficients:
        raise ValueError("弹性虚功拟合的系数和外力数量必须相等且非空")
    denominator = sum(value * value for value in coefficients)
    if denominator <= 0:
        raise ValueError("弹性虚功系数没有可辨识的非零信息")
    modulus = sum(coefficient * force for coefficient, force in zip(coefficients, external_forces)) / denominator
    residuals = [modulus * coefficient - force for coefficient, force in zip(coefficients, external_forces)]
    rmse = math.sqrt(sum(value * value for value in residuals) / len(residuals))
    return {
        "modulus_mpa": modulus,
        "rmse_n": rmse,
        "max_abs_residual_n": max(abs(value) for value in residuals),
        "point_count": len(residuals),
    }


def fit_linear_hardening(
    *,
    plastic_strains: Sequence[float],
    equivalent_stresses: Sequence[float],
) -> dict[str, float | int]:
    """Fit ``sigma_eq = Y + H * equivalent_plastic_strain``."""

    if len(plastic_strains) != len(equivalent_stresses) or len(plastic_strains) < 2:
        raise ValueError("线性硬化拟合至少需要两个成对数据点")
    mean_p = sum(plastic_strains) / len(plastic_strains)
    mean_sigma = sum(equivalent_stresses) / len(equivalent_stresses)
    denominator = sum((value - mean_p) ** 2 for value in plastic_strains)
    if denominator <= 0:
        raise ValueError("塑性应变没有变化，无法辨识硬化斜率")
    hardening = sum(
        (plastic_strain - mean_p) * (stress - mean_sigma)
        for plastic_strain, stress in zip(plastic_strains, equivalent_stresses)
    ) / denominator
    yield_mpa = mean_sigma - hardening * mean_p
    residuals = [
        yield_mpa + hardening * plastic_strain - stress
        for plastic_strain, stress in zip(plastic_strains, equivalent_stresses)
    ]
    return {
        "yield_mpa": yield_mpa,
        "hardening_mpa": hardening,
        "rmse_mpa": math.sqrt(sum(value * value for value in residuals) / len(residuals)),
        "max_abs_residual_mpa": max(abs(value) for value in residuals),
        "point_count": len(residuals),
    }


HARDENING_MODEL_NAMES = ("Linear", "Ludwik", "Swift", "Voce I（通用）", "Voce II（通用）")


def hardening_model_value(model: str, plastic_strain: float, parameters: dict[str, float]) -> float:
    """Evaluate the explicitly named generic hardening laws used for comparison."""

    if plastic_strain < 0.0:
        raise ValueError("硬化模型的等效塑性应变不能为负")
    if model == "Linear":
        return parameters["Y"] + parameters["H"] * plastic_strain
    if model == "Ludwik":
        return parameters["Y"] + parameters["K"] * plastic_strain ** parameters["n"]
    if model == "Swift":
        return parameters["K"] * (parameters["p0"] + plastic_strain) ** parameters["n"]
    if model == "Voce I（通用）":
        return parameters["Y"] + parameters["Q"] * (1.0 - math.exp(-parameters["b"] * plastic_strain))
    if model == "Voce II（通用）":
        return (
            parameters["Y"]
            + parameters["R0"] * plastic_strain
            + parameters["Q"] * (1.0 - math.exp(-parameters["b"] * plastic_strain))
        )
    raise ValueError(f"未知硬化模型：{model}")


def _coordinate_fit(
    model: str,
    plastic_strains: Sequence[float],
    equivalent_stresses: Sequence[float],
    initial: dict[str, float],
    bounds: dict[str, tuple[float, float]],
) -> dict[str, float]:
    names = list(initial)
    parameters = dict(initial)

    def score(candidate: dict[str, float]) -> float:
        residuals = [
            hardening_model_value(model, plastic_strain, candidate) - stress
            for plastic_strain, stress in zip(plastic_strains, equivalent_stresses)
        ]
        return sum(value * value for value in residuals) / len(residuals)

    best_score = score(parameters)
    steps = {name: max((bounds[name][1] - bounds[name][0]) * 0.2, 1e-8) for name in names}
    for _ in range(240):
        improved = False
        for name in names:
            for direction in (-1.0, 1.0):
                candidate = dict(parameters)
                low, high = bounds[name]
                candidate[name] = min(high, max(low, parameters[name] + direction * steps[name]))
                candidate_score = score(candidate)
                if candidate_score < best_score:
                    parameters = candidate
                    best_score = candidate_score
                    improved = True
        if not improved:
            for name in names:
                steps[name] *= 0.5
            if max(steps.values()) < 1e-7:
                break
    return parameters


def fit_hardening_models(
    *,
    plastic_strains: Sequence[float],
    equivalent_stresses: Sequence[float],
) -> list[dict]:
    """Fit generic comparison laws without claiming MatchID's private naming."""

    if len(plastic_strains) != len(equivalent_stresses) or len(plastic_strains) < 2:
        raise ValueError("硬化模型比较需要成对且至少两个数据点")
    linear = fit_linear_hardening(
        plastic_strains=plastic_strains,
        equivalent_stresses=equivalent_stresses,
    )
    maximum_stress = max(equivalent_stresses)
    minimum_stress = min(equivalent_stresses)
    maximum_plastic_strain = max(plastic_strains)
    strain_scale = max(maximum_plastic_strain, 0.01)
    initial_values = {
        "Ludwik": {"Y": max(0.0, minimum_stress), "K": max(1.0, maximum_stress), "n": 0.3},
        "Swift": {"K": max(1.0, maximum_stress / (strain_scale**0.3)), "p0": 0.001, "n": 0.3},
        "Voce I（通用）": {"Y": max(0.0, minimum_stress), "Q": max(1.0, maximum_stress - minimum_stress), "b": 10.0 / strain_scale},
        "Voce II（通用）": {"Y": max(0.0, minimum_stress), "R0": max(0.0, float(linear["hardening_mpa"]) / 2.0), "Q": max(1.0, maximum_stress - minimum_stress), "b": 10.0 / strain_scale},
    }
    bounds = {
        "Y": (0.0, maximum_stress * 2.0),
        "K": (0.0, maximum_stress * 10.0),
        "n": (0.05, 2.0),
        "p0": (1e-8, strain_scale * 10.0),
        "Q": (0.0, maximum_stress * 10.0),
        "b": (1e-8, 1000.0 / strain_scale),
        "R0": (0.0, maximum_stress * 10.0),
    }
    output: list[dict] = []
    linear_parameters = {"Y": float(linear["yield_mpa"]), "H": float(linear["hardening_mpa"])}
    for model, parameters in [("Linear", linear_parameters), *initial_values.items()]:
        if model != "Linear":
            parameters = _coordinate_fit(model, plastic_strains, equivalent_stresses, parameters, bounds)
        residuals = [
            hardening_model_value(model, plastic_strain, parameters) - stress
            for plastic_strain, stress in zip(plastic_strains, equivalent_stresses)
        ]
        mean_stress = sum(equivalent_stresses) / len(equivalent_stresses)
        total_sum = sum((stress - mean_stress) ** 2 for stress in equivalent_stresses)
        residual_sum = sum(value * value for value in residuals)
        output.append(
            {
                "model": model,
                "formula_status": "通用文献形式；未宣称等同MatchID内部模型" if model != "Linear" else "本项目阶段2定义",
                "parameters": parameters,
                "rmse_mpa": math.sqrt(residual_sum / len(residuals)),
                "r2": None if total_sum == 0.0 else 1.0 - residual_sum / total_sum,
                "point_count": len(residuals),
            }
        )
    return output
