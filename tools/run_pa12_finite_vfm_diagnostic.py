from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.affinity import translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

if __package__:
    from .matchid_dic import parse_matchid_dat, read_matchid_export
    from .pa12_finite_kinematics import align_displacement_fields, common_reference_point_indices, matchid_grid_triangles, plane_stress_virtual_work_residuals, profile_elastic_parameters, triangle_polygon_overlap_areas
    from .run_pa12_self_vfm import _geometry, _read_index
else:
    from matchid_dic import parse_matchid_dat, read_matchid_export
    from pa12_finite_kinematics import align_displacement_fields, common_reference_point_indices, matchid_grid_triangles, plane_stress_virtual_work_residuals, profile_elastic_parameters, triangle_polygon_overlap_areas
    from run_pa12_self_vfm import _geometry, _read_index


def _analysis_domains(
    reference_coordinates: np.ndarray,
    job_geometry: dict,
    machine_axes: dict,
    triangles: np.ndarray,
    operation_window: dict | None = None,
) -> list[dict]:
    dic_lengths = {
        "x": float(job_geometry["length_x_mm"]),
        "y": float(job_geometry["length_y_mm"]),
    }
    job_lengths = tuple(
        dic_lengths[machine_axes[axis]["coordinate"]] for axis in ("X", "Y")
    )
    dic_axis_index = {"x": 0, "y": 1}
    roi_polygons_mm = job_geometry.get("roi_polygons_mm") or [
        job_geometry["roi_polygon_mm"]
    ]
    roi_polygons_machine = [
        np.asarray(polygon, dtype=float)[
            :,
            [dic_axis_index[machine_axes[axis]["coordinate"]] for axis in ("X", "Y")],
        ]
        for polygon in roi_polygons_mm
    ]
    roi_shapes = [Polygon(polygon) for polygon in roi_polygons_machine]
    roi_polygon = unary_union(roi_shapes)
    field_polygon_machine = max(
        roi_polygons_machine, key=lambda polygon: Polygon(polygon).area
    )
    boundary_virtual_fields = _job_roi_boundary_virtual_fields(
        reference_coordinates, field_polygon_machine
    )
    job_roi_triangle_areas = np.zeros(len(triangles), dtype=float)
    for polygon in roi_polygons_machine:
        job_roi_triangle_areas += triangle_polygon_overlap_areas(
            reference_coordinates, triangles, polygon
        )
    job_supported_area = float(job_roi_triangle_areas.sum())
    subset_size_px = int(job_geometry["subset_size_px"])
    subset_offsets_px = np.arange(subset_size_px) - (subset_size_px - 1) / 2.0
    subset_offsets_mm = subset_offsets_px * float(
        job_geometry["conversion_mm_per_pixel"]
    )
    inset_center_region = roi_polygon
    for offset_x in subset_offsets_mm:
        for offset_y in subset_offsets_mm:
            inset_center_region = inset_center_region.intersection(
                translate(roi_polygon, xoff=-offset_x, yoff=-offset_y)
            )
    inset_polygons = [
        component
        for component in getattr(inset_center_region, "geoms", [inset_center_region])
        if component.geom_type == "Polygon"
    ]
    inset_triangle_areas = np.zeros(len(triangles), dtype=float)
    for inset_polygon in inset_polygons:
        inset_triangle_areas += triangle_polygon_overlap_areas(
            reference_coordinates,
            triangles,
            np.asarray(inset_polygon.exterior.coords[:-1], dtype=float),
        )
    inset_supported_area = float(inset_triangle_areas.sum())
    domains = [
        {
            "id": "full_job_roi",
            "label": "Job ROI 交叠面积积分",
            "virtual_field_lengths_mm": job_lengths,
            "roi_area_mm2": float(job_geometry["area_mm2"]),
            "measured_mesh_area_mm2": job_supported_area,
            "triangle_integration_areas_mm2": job_roi_triangle_areas,
            "virtual_field_values": boundary_virtual_fields,
        },
        {
            "id": "dic_subset_inset_sensitivity",
            "label": "DIC subset 内缩域独立敏感性",
            "virtual_field_lengths_mm": job_lengths,
            "subset_size_px": subset_size_px,
            "subset_support_half_width_px": (subset_size_px - 1) / 2.0,
            "roi_area_mm2": float(inset_center_region.area),
            "measured_mesh_area_mm2": inset_supported_area,
            "triangle_integration_areas_mm2": inset_triangle_areas,
            "virtual_field_values": boundary_virtual_fields,
        },
    ]
    if operation_window is not None:
        center = np.asarray(operation_window["center_machine_mm"], dtype=float)
        axis = np.asarray(operation_window["axis_unit_machine"], dtype=float)
        transverse = np.array([-axis[1], axis[0]])
        length = float(operation_window["length_mm"])
        width = float(operation_window["width_mm"])
        corners = np.asarray(
            [
                center - axis * length / 2 - transverse * width / 2,
                center + axis * length / 2 - transverse * width / 2,
                center + axis * length / 2 + transverse * width / 2,
                center - axis * length / 2 + transverse * width / 2,
            ]
        )
        operation_areas = triangle_polygon_overlap_areas(
            reference_coordinates, triangles, corners
        )
        relative_coordinates = np.asarray(reference_coordinates) - center
        longitudinal_coordinate = relative_coordinates @ axis
        transverse_coordinate = relative_coordinates @ transverse
        operation_virtual_fields = np.zeros(
            (2, len(reference_coordinates), 2), dtype=float
        )
        operation_virtual_fields[0, :, 0] = (
            longitudinal_coordinate + length / 2
        ) / length
        operation_virtual_fields[1, :, 1] = (
            transverse_coordinate + width / 2
        ) / width
        domains.append(
            {
                "id": "operation_window",
                "label": f"{length:g}×{width:g} mm 操作窗",
                "virtual_field_lengths_mm": (length, width),
                "roi_area_mm2": float(length * width),
                "measured_mesh_area_mm2": float(operation_areas.sum()),
                "triangle_integration_areas_mm2": operation_areas,
                "virtual_field_values": operation_virtual_fields,
                "operation_window_definition": dict(operation_window),
            }
        )
    return domains


def _job_roi_boundary_virtual_fields(
    reference_coordinates: np.ndarray,
    roi_polygon_machine: np.ndarray,
) -> np.ndarray:
    coordinates = np.asarray(reference_coordinates, dtype=float)
    polygon = np.asarray(roi_polygon_machine, dtype=float)
    virtual_fields = np.zeros((2, len(coordinates), 2), dtype=float)

    for axis_index in range(2):
        transverse_index = 1 - axis_index
        next_vertices = np.roll(polygon, -1, axis=0)
        transverse_spans = np.abs(
            next_vertices[:, transverse_index] - polygon[:, transverse_index]
        )
        cut_edges = np.argsort(transverse_spans)[-2:]
        edge_lines = []
        for edge_index in cut_edges:
            start = polygon[edge_index]
            end = next_vertices[edge_index]
            slope = (end[axis_index] - start[axis_index]) / (
                end[transverse_index] - start[transverse_index]
            )
            intercept = start[axis_index] - slope * start[transverse_index]
            edge_lines.append(
                (0.5 * (start[axis_index] + end[axis_index]), slope, intercept)
            )
        low_edge, high_edge = sorted(edge_lines, key=lambda line: line[0])
        transverse_limits = np.min(polygon[:, transverse_index]), np.max(
            polygon[:, transverse_index]
        )
        low_values = np.array(
            [low_edge[1] * value + low_edge[2] for value in transverse_limits]
        )
        high_values = np.array(
            [high_edge[1] * value + high_edge[2] for value in transverse_limits]
        )
        if np.any(high_values - low_values <= 0.0):
            raise ValueError("Job ROI 两条轴向切边的虚场归一化宽度不为正")
        transverse_coordinates = coordinates[:, transverse_index]
        low_values = low_edge[1] * transverse_coordinates + low_edge[2]
        high_values = high_edge[1] * transverse_coordinates + high_edge[2]
        virtual_fields[axis_index, :, axis_index] = (
            coordinates[:, axis_index] - low_values
        ) / (high_values - low_values)

    return virtual_fields


def _analyze_domain(
    domain: dict,
    reference_coordinates: np.ndarray,
    triangles: np.ndarray,
    frame_displacements: np.ndarray,
    boundary_resultants: np.ndarray,
    fit_indices: list[int],
    thickness_mm: float,
    poisson_ratio_fixed: float,
    poisson_ratios: np.ndarray,
    virtual_field_values: np.ndarray | None = None,
    fit_axis_indices: tuple[int, ...] | None = None,
) -> dict:
    virtual_field_lengths = domain["virtual_field_lengths_mm"]
    integration_areas = domain["triangle_integration_areas_mm2"]
    active_triangles = np.asarray(triangles)[integration_areas > 0.0]
    frame_kinematic_quality = _deformation_quality(
        reference_coordinates, active_triangles, frame_displacements
    )["per_frame"]
    fit_frame_indices_excluded = [
        index
        for index in fit_indices
        if frame_kinematic_quality[index]["nonpositive_jacobian_triangle_count"] > 0
    ]
    fit_frame_indices_used = [
        index for index in fit_indices if index not in fit_frame_indices_excluded
    ]
    if not fit_frame_indices_used:
        raise ValueError(f"{domain['id']} 弹性拟合窗口没有物理有效帧")
    virtual_field_options = (
        {} if virtual_field_values is None else {"virtual_field_values": virtual_field_values}
    )
    fit_displacements = frame_displacements[fit_frame_indices_used]
    fit_resultants = boundary_resultants[fit_frame_indices_used]
    fixed_nu_fit = profile_elastic_parameters(
        reference_coordinates,
        triangles,
        fit_displacements,
        fit_resultants,
        thickness_mm,
        np.array([poisson_ratio_fixed]),
        virtual_field_lengths_mm=virtual_field_lengths,
        quadrature_area_weights_mm2=integration_areas,
        **virtual_field_options,
        fit_axis_indices=fit_axis_indices,
    )[0]
    modulus = fixed_nu_fit["youngs_modulus_mpa"]
    algebraically_defined_frames = np.asarray(
        [quality["min_abs_detF"] > 0.0 for quality in frame_kinematic_quality]
    )
    residuals = np.full((len(frame_displacements), boundary_resultants.shape[1]), np.nan)
    residuals[algebraically_defined_frames] = plane_stress_virtual_work_residuals(
        reference_coordinates,
        triangles,
        frame_displacements[algebraically_defined_frames],
        boundary_resultants[algebraically_defined_frames],
        thickness_mm,
        modulus,
        poisson_ratio_fixed,
        virtual_field_lengths_mm=virtual_field_lengths,
        quadrature_area_weights_mm2=integration_areas,
        **virtual_field_options,
    )
    nu_profile = profile_elastic_parameters(
        reference_coordinates,
        triangles,
        fit_displacements,
        fit_resultants,
        thickness_mm,
            poisson_ratios,
            virtual_field_lengths_mm=virtual_field_lengths,
            quadrature_area_weights_mm2=integration_areas,
            **virtual_field_options,
        fit_axis_indices=fit_axis_indices,
    )
    fit_residuals = residuals[fit_frame_indices_used]
    selected_axes = (
        np.arange(boundary_resultants.shape[1], dtype=int)
        if fit_axis_indices is None
        else np.asarray(fit_axis_indices, dtype=int)
    )
    return {
        **{
            key: value
            for key, value in domain.items()
            if key not in {"triangle_integration_areas_mm2", "virtual_field_values"}
        },
        "youngs_modulus_mpa": modulus,
        "residuals_n": residuals,
        "frame_kinematic_quality": frame_kinematic_quality,
        "fit_frame_indices_used": fit_frame_indices_used,
        "fit_frame_indices_excluded": fit_frame_indices_excluded,
        "nu_profile": nu_profile,
        "fit_axis_indices": selected_axes.tolist(),
        "fit_residual_rms_n": float(np.sqrt(np.mean(np.square(fit_residuals[:, selected_axes])))),
        "all_axis_fit_residual_rms_n": float(np.sqrt(np.mean(np.square(fit_residuals)))),
        "fit_force_rms_n": float(np.sqrt(np.mean(np.square(fit_resultants[:, selected_axes])))),
        "all_axis_fit_force_rms_n": float(np.sqrt(np.mean(np.square(fit_resultants)))),
    }


def _virtual_work_output_arrays(
    boundary_resultants_n: np.ndarray,
    residuals_n: np.ndarray,
    frame_kinematic_quality: list[dict],
) -> dict[str, np.ndarray]:
    physical_valid = np.asarray(
        [
            quality["nonpositive_jacobian_triangle_count"] == 0
            for quality in frame_kinematic_quality
        ],
        dtype=bool,
    )
    internal_algebraic = boundary_resultants_n + residuals_n
    return {
        "physical_valid": physical_valid,
        "internal_algebraic_n": internal_algebraic,
        "residual_algebraic_n": residuals_n,
        "internal_physical_n": np.where(physical_valid[:, None], internal_algebraic, np.nan),
        "external_physical_n": np.where(
            physical_valid[:, None], boundary_resultants_n, np.nan
        ),
        "residual_physical_n": np.where(physical_valid[:, None], residuals_n, np.nan),
    }


def _read_frame(path: Path) -> dict[str, np.ndarray]:
    frame = pd.read_csv(path, encoding="utf-8-sig", usecols=["x", "y", "u", "v"])
    return {key: frame[key].to_numpy(dtype=float) for key in ("x", "y", "u", "v")}


def _reference_field_source(config: dict, merged_directory: Path) -> Path:
    if "reference_field_export" in config:
        return Path(config["reference_field_export"]["path"])
    if "reference_dat_file" in config:
        return Path(config["reference_dat_file"])
    reference_stem = Path(config["reference_photo"]).stem
    return merged_directory / f"{reference_stem}_DIC全场—力.csv"


def _read_reference_frame(config: dict, merged_directory: Path) -> dict[str, np.ndarray]:
    if "reference_field_export" not in config:
        if "reference_dat_file" in config:
            rows = parse_matchid_dat(Path(config["reference_dat_file"]))["rows"]
            return {
                key: np.asarray([row[key] for row in rows], dtype=float)
                for key in ("x", "y", "u", "v")
            }
        return _read_frame(_reference_field_source(config, merged_directory))
    export = config["reference_field_export"]
    rows = read_matchid_export(
        Path(export["path"]), export["field_map"], delimiter=export["delimiter"]
    )
    return {
        key: np.asarray([row[key] for row in rows], dtype=float)
        for key in ("x", "y", "u", "v")
    }

def _deformation_quality(
    reference_coordinates: np.ndarray,
    triangles: np.ndarray,
    frame_displacements: np.ndarray,
) -> dict:
    element_coordinates = reference_coordinates[triangles]
    reference_edges = np.swapaxes(
        element_coordinates[:, 1:] - element_coordinates[:, :1], 1, 2
    )
    inverse_reference_edges = np.linalg.inv(reference_edges)
    min_jacobian, max_jacobian = np.inf, -np.inf
    nonpositive_jacobian_count = 0
    max_frame_p95, max_frame_p99 = None, None
    per_frame = []
    final_values = None
    final_mean_strain = None
    for displacement in frame_displacements:
        current = element_coordinates + displacement[triangles]
        current_edges = np.swapaxes(current[:, 1:] - current[:, :1], 1, 2)
        gradients = current_edges @ inverse_reference_edges
        jacobian = np.linalg.det(gradients)
        min_jacobian = min(min_jacobian, float(jacobian.min()))
        max_jacobian = max(max_jacobian, float(jacobian.max()))
        nonpositive_jacobian_count += int(np.count_nonzero(jacobian <= 0.0))
        positive_jacobian = jacobian > 0.0
        if np.any(positive_jacobian):
            positive_gradients = gradients[positive_jacobian]
            left_cauchy_green = positive_gradients @ np.swapaxes(
                positive_gradients, 1, 2
            )
            strain = 0.5 * (np.eye(2) - np.linalg.inv(left_cauchy_green))
            component_magnitude = np.max(np.abs(strain), axis=(1, 2))
            frame_p95 = float(np.quantile(component_magnitude, 0.95))
            frame_p99 = float(np.quantile(component_magnitude, 0.99))
            max_frame_p95 = (
                frame_p95 if max_frame_p95 is None else max(max_frame_p95, frame_p95)
            )
            max_frame_p99 = (
                frame_p99 if max_frame_p99 is None else max(max_frame_p99, frame_p99)
            )
            final_mean_strain = np.mean(strain, axis=0)
        else:
            component_magnitude = np.empty(0, dtype=float)
            final_mean_strain = np.full((2, 2), np.nan)
        per_frame.append({
            "detF_min": float(jacobian.min()),
            "detF_max": float(jacobian.max()),
            "nonpositive_jacobian_triangle_count": int(np.count_nonzero(jacobian <= 0.0)),
            "min_abs_detF": float(np.abs(jacobian).min()),
            "max_abs_almansi_component": (
                float(component_magnitude.max())
                if len(component_magnitude)
                else None
            ),
        })
        final_values = component_magnitude
    quantiles = (
        list(map(float, np.quantile(final_values, [0.5, 0.95, 0.99, 0.999, 1.0])))
        if len(final_values)
        else [None] * 5
    )
    return {
        "per_frame": per_frame,
        "detF_min": min_jacobian,
        "detF_max": max_jacobian,
        "nonpositive_jacobian_triangle_count": nonpositive_jacobian_count,
        "max_over_frames_p95_abs_almansi_component": max_frame_p95,
        "max_over_frames_p99_abs_almansi_component": max_frame_p99,
        "final_abs_almansi_component_quantiles": dict(zip(
            ("p50", "p95", "p99", "p99_9", "max"), quantiles
        )),
        "final_mean_almansi_strain_tensor": (
            None if final_mean_strain is None or not np.isfinite(final_mean_strain).all()
            else final_mean_strain.tolist()
        ),
    }


def run(config_path: Path) -> dict:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    virtual_field_mode = config.get("virtual_field_mode", "affine")
    if virtual_field_mode not in {"affine", "job_roi_boundary_adapted"}:
        raise ValueError(f"不支持的虚场模式：{virtual_field_mode}")
    root = Path(config["output_root"])
    experiment_id = config["experiment_id"]
    merged_dir = root / config["merged_directory"]
    index_rows = _read_index(root / config["index_file"])
    if not index_rows:
        raise ValueError("DIC—力索引没有帧记录")
    image_folder = Path(config["image_folder"])
    image_names = {path.name for path in image_folder.glob("*.jpg")}
    dat_names = {Path(path.name[:-4]).name for path in image_folder.glob("*.jpg.dat")}
    indexed_names = {row["照片"] for row in index_rows}
    unpaired_images = sorted(image_names - dat_names)
    paired_without_force_index = sorted((image_names & dat_names) - indexed_names)
    reference_source = _reference_field_source(config, merged_dir)
    reference = _read_reference_frame(config, merged_dir)
    current_fields = [
        reference
        if row["照片"] == config["reference_photo"]
        else _read_frame(merged_dir / f"{Path(row['照片']).stem}_DIC全场—力.csv")
        for row in index_rows
    ]
    common_indices = common_reference_point_indices(reference, current_fields)
    common_reference = {
        key: reference[key][common_indices] for key in ("x", "y", "u", "v")
    }
    machine_axes = config["machine_axes_in_dic"]
    fit_virtual_axes = config.get("fit_virtual_axes", ["X", "Y"])
    fit_axis_indices = tuple("XY".index(axis) for axis in fit_virtual_axes)
    machine_xy = np.column_stack([
        common_reference[machine_axes["X"]["coordinate"]],
        common_reference[machine_axes["Y"]["coordinate"]],
    ])
    geometry_repair = config.get("geometry_repair")
    job_geometry = (
        _geometry(Path(config["job_file"]), repair_method=geometry_repair)
        if geometry_repair is not None
        else _geometry(Path(config["job_file"]))
    )
    triangles = matchid_grid_triangles(
        machine_xy, float(job_geometry["dic_grid_spacing_mm"])
    )
    element_coordinates = machine_xy[triangles]
    first_edges = element_coordinates[:, 1] - element_coordinates[:, 0]
    second_edges = element_coordinates[:, 2] - element_coordinates[:, 0]
    mesh_area = float(0.5 * np.abs(
        first_edges[:, 0] * second_edges[:, 1] - first_edges[:, 1] * second_edges[:, 0]
    ).sum())
    job_area = float(job_geometry["area_mm2"])
    domains = _analysis_domains(
        machine_xy,
        job_geometry,
        machine_axes,
        triangles,
        operation_window=config.get("operation_window"),
    )
    full_job_domain = next(item for item in domains if item["id"] == "full_job_roi")
    job_supported_area = float(full_job_domain["measured_mesh_area_mm2"])
    area_ratio = job_supported_area / job_area
    names, times, displacements, forces = [], [], [], []
    for row, current in zip(index_rows, current_fields):
        aligned = align_displacement_fields(common_reference, current)
        if aligned["matched_point_count"] != len(machine_xy):
            raise ValueError(f"{row['照片']} DIC共同点不足：{aligned['matched_point_count']}/{len(machine_xy)}")
        displacements.append(np.column_stack([
            aligned[machine_axes["X"]["displacement"]],
            aligned[machine_axes["Y"]["displacement"]],
        ]))
        forces.append([float(row[machine_axes[axis]["force_column"]]) for axis in ("X", "Y")])
        names.append(row["照片"])
        times.append(float(row["时间/s"]))
    displacements, forces = np.asarray(displacements), np.asarray(forces)
    deformation_quality = _deformation_quality(machine_xy, triangles, displacements)
    fit_indices = [names.index(photo) for photo in config["elastic_fit_photos"]]
    nu = float(config["poisson_ratio_fixed"])
    thickness = float(config["thickness_mm"])
    nu_grid = np.linspace(-0.9, 0.499, 50)
    domain_results = [
        _analyze_domain(
            domain,
            machine_xy,
            triangles,
            displacements,
            forces,
            fit_indices,
            thickness,
            nu,
            nu_grid,
            virtual_field_values=(
                domain["virtual_field_values"]
                if virtual_field_mode == "job_roi_boundary_adapted"
                else None
            ),
            fit_axis_indices=fit_axis_indices,
        )
        for domain in domains
    ]
    full_job_result = next(item for item in domain_results if item["id"] == "full_job_roi")
    inset_result = next(item for item in domain_results if item["id"] == "dic_subset_inset_sensitivity")
    residual = full_job_result["residuals_n"]
    modulus = full_job_result["youngs_modulus_mpa"]
    profile = full_job_result["nu_profile"]
    best_profile_rms = min(row["residual_rms_n"] for row in profile)
    near_best = [row for row in profile if row["residual_rms_n"] <= best_profile_rms * 1.01]

    output = root / config["output_directory"] / experiment_id
    output.mkdir(parents=True, exist_ok=True)
    kinematic_quality_rows = [
        {
            "照片": photo,
            "detF最小": quality["detF_min"],
            "detF最大": quality["detF_max"],
            "非正Jacobian三角形数": quality["nonpositive_jacobian_triangle_count"],
            "最小|detF|": quality["min_abs_detF"],
            "最大|Euler-Almansi应变分量|": quality["max_abs_almansi_component"],
        }
        for photo, quality in zip(names, deformation_quality["per_frame"])
    ]
    pd.DataFrame(kinematic_quality_rows).to_csv(
        output / "逐帧运动学质量.csv", index=False, encoding="utf-8-sig"
    )
    domain_history_statistics = {}
    for analysis in domain_results:
        if analysis["id"] == "full_job_roi":
            branch_dir = output
        elif analysis["id"] == "dic_subset_inset_sensitivity":
            branch_dir = output / "DICsubset内缩域敏感性"
        else:
            branch_dir = output / analysis["id"]
        branch_dir.mkdir(parents=True, exist_ok=True)
        frame_quality = analysis["frame_kinematic_quality"]
        work_output = _virtual_work_output_arrays(
            forces, analysis["residuals_n"], frame_quality
        )
        valid_residuals = analysis["residuals_n"][work_output["physical_valid"]]
        domain_history_statistics[analysis["id"]] = {
            "有效帧数": int(np.count_nonzero(work_output["physical_valid"])),
            "无效帧数": int(np.count_nonzero(~work_output["physical_valid"])),
            "有效帧全历程残差RMS_N": float(
                np.sqrt(np.mean(np.square(valid_residuals)))
            ),
        }
        output_rows = []
        for i, photo in enumerate(names):
            quality = frame_quality[i]
            output_rows.append({
                "分析域": analysis["label"],
                "照片": photo, "时间/s": times[i],
                "虚功物理有效": bool(work_output["physical_valid"][i]),
                "detF最小": quality["detF_min"],
                "非正Jacobian三角形数": quality["nonpositive_jacobian_triangle_count"],
                "X向力/N": forces[i, 0], "Y向力/N": forces[i, 1],
                "X内虚功/N": work_output["internal_physical_n"][i, 0],
                "X外虚功/N": work_output["external_physical_n"][i, 0],
                "X残差/N": work_output["residual_physical_n"][i, 0],
                "Y内虚功/N": work_output["internal_physical_n"][i, 1],
                "Y外虚功/N": work_output["external_physical_n"][i, 1],
                "Y残差/N": work_output["residual_physical_n"][i, 1],
                "X内虚功代数诊断/N": work_output["internal_algebraic_n"][i, 0],
                "X残差代数诊断/N": work_output["residual_algebraic_n"][i, 0],
                "Y内虚功代数诊断/N": work_output["internal_algebraic_n"][i, 1],
                "Y残差代数诊断/N": work_output["residual_algebraic_n"][i, 1],
                "DIC共同点数": len(machine_xy),
                "DIC积分面积_mm2": analysis["measured_mesh_area_mm2"],
                "分析域面积_mm2": analysis["roi_area_mm2"],
                "面积覆盖率": analysis["measured_mesh_area_mm2"] / analysis["roi_area_mm2"],
            })
        pd.DataFrame(output_rows).to_csv(branch_dir / "逐帧虚功诊断.csv", index=False, encoding="utf-8-sig")
        pd.DataFrame(analysis["nu_profile"]).to_csv(branch_dir / "泊松比可辨识性剖面.csv", index=False, encoding="utf-8-sig")
        plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
        plt.rcParams["axes.unicode_minus"] = False
        fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True)
        for column_index, axis_name in enumerate(("X", "Y")):
            ax = axes[column_index]
            ax.plot(
                times,
                work_output["internal_physical_n"][:, column_index],
                label=f"{axis_name} 内虚功",
            )
            ax.plot(
                times,
                work_output["external_physical_n"][:, column_index],
                "--",
                label=f"{axis_name} 外虚功候选",
            )
            coverage = analysis["measured_mesh_area_mm2"] / analysis["roi_area_mm2"]
            ax.set_title(f"{axis_name} 方向；覆盖率 {coverage:.1%}")
            ax.set_xlabel("时间 / s")
            ax.set_ylabel("虚功 / N")
            ax.legend()
        fig.suptitle(f"{experiment_id} {analysis['label']}")
        fig.tight_layout()
        fig.savefig(branch_dir / "逐帧虚功诊断.png", dpi=160)
        plt.close(fig)
    residual_rms = full_job_result["fit_residual_rms_n"]
    force_rms = float(np.sqrt(np.mean(forces[fit_indices] ** 2)))
    result = {
        "状态": "诊断候选；Job ROI 仅积分被实测 DIC 三角形支持的交叠区域", "实验编号": experiment_id,
        "帧数": len(names), "参考照片": config["reference_photo"], "参考DIC点数": len(reference["x"]),
        "全程共同网格点数": len(machine_xy),
        "从固定网格剔除的参考坐标": [
            {"x_mm": float(reference["x"][index]), "y_mm": float(reference["y"][index])}
            for index in np.setdiff1d(np.arange(len(reference["x"])), common_indices)
        ],
        "DIC支持点数变化帧": [
            {"照片": row["照片"], "当前场点数": len(current["x"])}
            for row, current in zip(index_rows, current_fields)
            if len(current["x"]) != len(reference["x"])
        ],
        "DIC点数": len(machine_xy),
        "参考DIC场来源": str(reference_source),
        "原始JPG数": len(image_names), "原始DAT数": len(dat_names), "有效DIC力索引帧数": len(index_rows),
        "缺同名DAT的照片": unpaired_images, "有JPG和DAT但不在有效力索引的照片": paired_without_force_index,
        "三角形数": len(triangles), "DIC三角网总面积_mm2": mesh_area,
        "DIC网格规则": "Job Step size×Conversion 相邻格点三角剖分；缺失格点不跨越",
        "DIC积分面积_mm2": job_supported_area, "Job_ROI面积_mm2": job_area,
        "面积覆盖率": area_ratio, "面积门槛状态": "PASS" if area_ratio >= 0.95 else "REVIEW_REQUIRED",
        "虚功平衡状态": "BLOCKED_INCOMPLETE_DIC_SUPPORT" if area_ratio < 0.95 else "NOT_VERIFIED",
        "虚功平衡状态说明": (
            "DIC 网格未覆盖至少 95% 的完整 Job ROI；内功是部分域积分，不能与完整 ROI 机器合力宣称为平衡。"
            if area_ratio < 0.95
            else "诊断器未定义基于测量不确定度的通过容差，且不独立验证物理受力边界；残差只作诊断，不自动判为平衡。"
        ),
        "面内变形质量": deformation_quality,
        "逐帧运动学质量文件": "逐帧运动学质量.csv",
        "厚度_mm": thickness, "固定泊松比": nu, "条件弹性模量_MPa": modulus,
        "虚场模式": virtual_field_mode,
        "拟合轴": fit_virtual_axes,
        "域结果": [
            {
                "积分域": analysis["id"],
                "域名称": analysis["label"],
                "虚场长度_mm": list(analysis["virtual_field_lengths_mm"]),
                "域面积_mm2": analysis["roi_area_mm2"],
                "实测DIC面积_mm2": analysis["measured_mesh_area_mm2"],
                "DIC覆盖率": analysis["measured_mesh_area_mm2"] / analysis["roi_area_mm2"],
                "条件E_MPa": analysis["youngs_modulus_mpa"],
                "拟合帧残差RMS_N": analysis["fit_residual_rms_n"],
                "虚功平衡状态": (
                    "BLOCKED_INCOMPLETE_DIC_SUPPORT"
                    if analysis["measured_mesh_area_mm2"] / analysis["roi_area_mm2"] < 0.95
                    else "NOT_VERIFIED"
                ),
                "操作窗定义": analysis.get("operation_window_definition"),
                "实际拟合照片": [names[index] for index in analysis["fit_frame_indices_used"]],
                "拟合窗排除的非正detF照片": [names[index] for index in analysis["fit_frame_indices_excluded"]],
                **domain_history_statistics[analysis["id"]],
                "状态": "REVIEW_REQUIRED" if analysis["measured_mesh_area_mm2"] / analysis["roi_area_mm2"] < 0.95 else "DIAGNOSTIC_ONLY",
            }
            for analysis in domain_results
        ],
        "自由泊松比1pct残差带": [min(row["nu"] for row in near_best), max(row["nu"] for row in near_best)],
        "拟合帧": config["elastic_fit_photos"], "拟合帧虚功残差均方根_N": residual_rms,
        "拟合帧力均方根_N": force_rms, "残差相对力均方根": residual_rms / force_rms,
        "限制": [
            "Press 合力作为广义外功要求加载边界虚位移差为 1、其他边界外功为 0；当前未完成独立实测验证。",
            "线性 Euler–Almansi 平面应力关系仅是诊断本构，不是经验证的 PA12 有限应变塑性模型。",
            "Job ROI 分支逐三角形只积分其与原始 Job 多边形 ROI 的交叠面积；未被实测 DIC 三角形支持的 ROI 面积不外推，并继续触发 REVIEW_REQUIRED。",
            "DIC subset 内缩域是独立敏感性分析，单独输出，不与 Job ROI 主域结果合并或相互替代。",
            "30 mm 操作窗如有输出，其中心定位来自窄区中线，不是照片实测夹持标记；窗端未注册前的外虚功仅作条件诊断。",
            "det(F)≤0 的帧保留在逐帧 CSV 中；该域物理内/外虚功与残差留空，代数诊断值单列，曲线断开；全历程残差 RMS 仅统计物理有效帧。",
            "有限变形诊断只使用二维面内变形梯度；未识别厚度方向伸长和三维局部应力，因此不能称为完整三维平面应力本构识别。",
            f"本次诊断厚度按配置取 {thickness:.3f} mm；实际区域厚度与外功边界等价仍需物理证据核验。",
        ],
    }
    (output / "诊断摘要.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    virtual_field_label = (
        "Job ROI 边界适配虚场"
        if virtual_field_mode == "job_roi_boundary_adapted"
        else "仿射虚场"
    )
    lines = ["# 有限变形虚功诊断", "", f"- 实验：{experiment_id}", f"- 虚场模式：{virtual_field_label}。", f"- 位移参考场：{reference_source}（{len(reference['x'])} 点）；全程固定共同网格 {len(machine_xy)} 点。", f"- DIC支持点数变化帧：{result['DIC支持点数变化帧']}", f"- 原始 JPG/DAT：{len(image_names)}/{len(dat_names)}；有效 DIC—力帧：{len(index_rows)}", f"- 缺同名 DAT：{unpaired_images}", f"- 有 JPG/DAT 但不在有效力索引：{paired_without_force_index}", f"- Job ROI 面积 {job_area:.6f} mm²；实测 DIC 网格与 Job ROI 的交叠积分面积 {job_supported_area:.6f} mm²；覆盖率 {area_ratio:.2%}", f"- {virtual_field_label}候选（仅部分DIC积分，非完整ROI结果）：固定 ν={nu}，条件 E {modulus:.6f} MPa；拟合帧残差 RMS {residual_rms:.6f} N；力 RMS {force_rms:.6f} N；相对 RMS {residual_rms / force_rms:.2%}", f"- 该候选自由 ν 的 1% 残差带：{result['自由泊松比1pct残差带']}", "- DIC subset 内缩有效域作为独立敏感性分析，逐帧 CSV、ν 剖面和图位于 `DICsubset内缩域敏感性/`。", "", "## 双域对照", "", "| 分析域 | 虚场长度 X/Y (mm) | 区域面积 (mm²) | DIC覆盖率 | 条件 E (MPa) | 拟合残差 RMS (N) |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
    lines.insert(10, f"- 虚功平衡资格状态：{result['虚功平衡状态']}。{result['虚功平衡状态说明']}")
    lines.insert(3, f"- 本次分析厚度：{thickness:.3f} mm。")
    deformation = result["面内变形质量"]
    mean_strain = deformation["final_mean_almansi_strain_tensor"]
    mean_strain_text = (
        "N/A"
        if mean_strain is None
        else f"{mean_strain[0][0]:.4f}/{mean_strain[1][1]:.4f}"
    )
    final_quantiles = deformation["final_abs_almansi_component_quantiles"]
    final_quantiles_text = "/".join(
        "N/A" if value is None else f"{value:.4f}"
        for value in (final_quantiles["p95"], final_quantiles["p99"], final_quantiles["max"])
    )
    lines.insert(7, f"- DIC网格：{result['DIC网格规则']}；共 {result['三角形数']} 个相邻三角形。")
    lines.insert(7, f"- 面内运动学：det(F) 范围 [{deformation['detF_min']:.4f}, {deformation['detF_max']:.4f}]；最终平均 Euler–Almansi εxx/εyy={mean_strain_text}；最终 |应变分量| P95/P99/max={final_quantiles_text}。")
    lines.insert(7, "- 逐帧 det(F) 极值、非正 Jacobian 数量和应变极值见 `逐帧运动学质量.csv`。")
    for analysis in result["域结果"]:
        lines.append(f"| {analysis['域名称']} | {analysis['虚场长度_mm']} | {analysis['域面积_mm2']:.6f} | {analysis['DIC覆盖率']:.2%} | {analysis['条件E_MPa']:.6f} | {analysis['拟合帧残差RMS_N']:.6f} |")
    for analysis in result["域结果"]:
        excluded_fit_photos = analysis["拟合窗排除的非正detF照片"]
        if excluded_fit_photos:
            lines.append(f"- {analysis['域名称']}拟合窗排除非正 det(F) 帧：{excluded_fit_photos}。")
    lines.extend([
        "",
        "## 全历程物理有效帧",
        "",
        "det(F)≤0 帧保留在 CSV 中；物理虚功/残差留空，代数诊断值另列，图中断开。该 RMS 仅统计物理有效帧。",
        "",
        "| 分析域 | 有效帧数 | 无效帧数 | 有效帧全历程残差 RMS (N) |",
        "| --- | ---: | ---: | ---: |",
    ])
    for analysis in result["域结果"]:
        lines.append(f"| {analysis['域名称']} | {analysis['有效帧数']} | {analysis['无效帧数']} | {analysis['有效帧全历程残差RMS_N']:.6f} |")
    lines.extend(["", "## 限制", ""])
    lines.extend(f"- {item}" for item in result["限制"])
    (output / "诊断摘要.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="运行 PA12 有限变形 VFM 诊断")
    parser.add_argument("--config", type=Path, default=Path("configs/pa12_finite_vfm_s16.json"))
    print(json.dumps(run(parser.parse_args().config), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
