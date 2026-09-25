from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt

if __package__:
    from .matchid_prepare import parse_job_metadata
    from .pa12_self_vfm import (
        equivalent_plastic_strain_plane_stress,
        equivalent_stress_plane_stress,
        fit_elastic_modulus,
        fit_hardening_models,
        fit_linear_hardening,
        HARDENING_MODEL_NAMES,
        hardening_model_value,
        integrate_plane_stress_virtual_work_coefficients,
        plane_stress_virtual_work_coefficients,
        rotated_machine_axes,
    )
    from .pa12_vfm_check import _shape_coordinates
else:
    from matchid_prepare import parse_job_metadata
    from pa12_self_vfm import (
        equivalent_plastic_strain_plane_stress,
        equivalent_stress_plane_stress,
        fit_elastic_modulus,
        fit_hardening_models,
        fit_linear_hardening,
        HARDENING_MODEL_NAMES,
        hardening_model_value,
        integrate_plane_stress_virtual_work_coefficients,
        plane_stress_virtual_work_coefficients,
        rotated_machine_axes,
    )
    from pa12_vfm_check import _shape_coordinates


REQUIRED_INDEX_FIELDS = {"照片", "时间/s", "X向力/N", "Y向力/N"}
FRAME_FIELDS = [
    "实验编号",
    "照片",
    "时间/s",
    "点数",
    "平均exx",
    "平均eyy",
    "平均exy",
    "X向力/N",
    "Y向力/N",
    "边界σx/MPa",
    "边界σy/MPa",
    "等效应力/MPa",
    "等效塑性应变",
    "X虚场系数/N每MPa",
    "Y虚场系数/N每MPa",
    "基线X虚场系数/N每MPa",
    "基线Y虚场系数/N每MPa",
    "积分面积/mm2",
    "面积比",
    "有效三角形数",
    "排除点数",
    "阶段1内部虚功X/N",
    "阶段1外部虚功X/N",
    "阶段1残差X/N",
    "阶段1内部虚功Y/N",
    "阶段1外部虚功Y/N",
    "阶段1残差Y/N",
    "阶段2模型等效应力/MPa",
    "阶段2内部虚功X/N",
    "阶段2残差X/N",
    "阶段2内部虚功Y/N",
    "阶段2残差Y/N",
]
MODEL_COMPARISON_FIELDS = [
    "照片",
    "时间/s",
    "等效塑性应变",
    "等效应力/MPa",
    "Linear模型应力/MPa",
    "Ludwik模型应力/MPa",
    "Swift模型应力/MPa",
    "Voce I（通用）模型应力/MPa",
    "Voce II（通用）模型应力/MPa",
]


def _open_csv(path: Path):
    for encoding in ("utf-8-sig", "cp936"):
        try:
            handle = path.open("r", newline="", encoding=encoding)
            handle.read(1)
            handle.seek(0)
            return handle
        except UnicodeDecodeError:
            try:
                handle.close()
            except UnboundLocalError:
                pass
    raise UnicodeDecodeError("csv", b"", 0, 1, f"无法读取 CSV 编码：{path}")


def _finite(value: str, label: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} 不是有限数：{value!r}")
    return number


def _read_index(path: Path) -> list[dict[str, str]]:
    with _open_csv(path) as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_INDEX_FIELDS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} 缺少字段：{sorted(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{path} 没有帧记录")
    return rows


def _read_frame_means(path: Path) -> dict[str, float | int]:
    with _open_csv(path) as handle:
        reader = csv.DictReader(handle)
        required = {"exx", "eyy", "exy"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} 缺少 DIC 应变字段：{sorted(missing)}")
        count = 0
        sums = {key: 0.0 for key in ("exx", "eyy", "exy")}
        for row in reader:
            count += 1
            for key in sums:
                sums[key] += _finite(row[key], f"{path}:{key}")
    if count == 0:
        raise ValueError(f"{path} 没有 DIC 点")
    return {key: value / count for key, value in sums.items()} | {"point_count": count}


def _read_frame_points(source) -> list[dict[str, float]]:
    if hasattr(source, "read"):
        reader = csv.DictReader(source)
        label = "DIC点流"
        close_handle = False
        handle = source
    else:
        path = Path(source)
        handle = _open_csv(path)
        reader = csv.DictReader(handle)
        label = str(path)
        close_handle = True
    try:
        required = {"x", "y", "exx", "eyy", "exy"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{label} 缺少 DIC逐点字段：{sorted(missing)}")
        points = [
            {
                key: _finite(row[key], f"{label}:{key}")
                for key in ("x", "y", "exx", "eyy", "exy")
            }
            for row in reader
        ]
    finally:
        if close_handle:
            handle.close()
    if not points:
        raise ValueError(f"{label} 没有 DIC 点")
    return points


def _align_frame_points(
    reference: list[dict[str, float]],
    current: list[dict[str, float]],
) -> list[dict[str, float]]:
    if len(reference) != len(current):
        raise ValueError("参考帧与当前帧 DIC 点数不一致，不能按行扣除")
    aligned: list[dict[str, float]] = []
    for index, (baseline, frame) in enumerate(zip(reference, current)):
        if not (
            math.isclose(baseline["x"], frame["x"], rel_tol=0.0, abs_tol=1e-9)
            and math.isclose(baseline["y"], frame["y"], rel_tol=0.0, abs_tol=1e-9)
        ):
            raise ValueError(f"参考帧与当前帧第 {index} 个 DIC 点坐标不一致")
        aligned.append(
            {
                "x": frame["x"],
                "y": frame["y"],
                "exx": frame["exx"] - baseline["exx"],
                "eyy": frame["eyy"] - baseline["eyy"],
                "exy": frame["exy"] - baseline["exy"],
            }
        )
    return aligned


def _geometry(job_path: Path) -> dict[str, float | str]:
    job = parse_job_metadata(job_path)
    x_pixels, y_pixels = _shape_coordinates(job["shape"])
    conversion = float(job["conversion_mm_per_pixel"])
    min_x, max_x = min(x_pixels), max(x_pixels)
    min_y, max_y = min(y_pixels), max(y_pixels)
    length_x = (max_x - min_x) * conversion
    length_y = (max_y - min_y) * conversion
    return {
        "length_x_mm": length_x,
        "length_y_mm": length_y,
        "area_mm2": length_x * length_y,
        "conversion_mm_per_pixel": conversion,
        "roi_bounds_mm": (
            min_x * conversion,
            max_x * conversion,
            min_y * conversion,
            max_y * conversion,
        ),
        "roi_bounds_px": f"x={min_x:g}–{max_x:g}, y={min_y:g}–{max_y:g} px",
        "reference_image": Path(job["reference_image"]).name,
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


def _safe_float(value: float | None) -> float | None:
    return None if value is None else float(value)


def _fit_progressive_elastic(records: list[dict], indices: list[int], active_axes: list[str]) -> list[dict]:
    output: list[dict] = []
    for end in range(2, len(indices) + 1):
        selected = indices[:end]
        coefficients: list[float] = []
        forces: list[float] = []
        for index in selected:
            for axis in active_axes:
                coefficient = records[index][f"coefficient_{axis.lower()}"]
                force = records[index][f"force_{axis.lower()}"]
                if coefficient != 0.0 and force > 0.0:
                    coefficients.append(coefficient)
                    forces.append(force)
        if len(coefficients) < 2:
            continue
        fit = fit_elastic_modulus(coefficients=coefficients, external_forces=forces)
        output.append(
            {
                "样本末帧": records[selected[-1]]["照片"],
                "E/MPa": fit["modulus_mpa"],
                "虚功均方根残差/N": fit["rmse_n"],
                "样本点数": fit["point_count"],
            }
        )
    return output


def _fit_progressive_hardening(records: list[dict], indices: list[int]) -> list[dict]:
    output: list[dict] = []
    for end in range(2, len(indices) + 1):
        selected = indices[:end]
        result = fit_linear_hardening(
            plastic_strains=[records[index]["plastic_strain"] for index in selected],
            equivalent_stresses=[records[index]["equivalent_stress"] for index in selected],
        )
        output.append(
            {
                "样本末帧": records[selected[-1]]["照片"],
                "Y/MPa": result["yield_mpa"],
                "H/MPa": result["hardening_mpa"],
                "拟合均方根残差/MPa": result["rmse_mpa"],
                "样本点数": result["point_count"],
            }
        )
    return output


def _configure_plot() -> None:
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False


def _plot_experiment(
    output_dir: Path,
    experiment_id: str,
    frame_rows: list[dict],
    elastic_progress: list[dict],
    hardening_progress: list[dict],
    model_rows: list[dict],
    geometry: dict,
) -> None:
    _configure_plot()
    times = [float(row["时间/s"]) for row in frame_rows]
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), constrained_layout=True)
    axes[0, 0].plot(times, [float(row["阶段1内部虚功X/N"]) for row in frame_rows], label="阶段1内部虚功 X")
    axes[0, 0].plot(times, [float(row["阶段1外部虚功X/N"]) for row in frame_rows], "--", label="阶段1外部虚功 X")
    axes[0, 0].plot(times, [float(row["阶段2内部虚功X/N"]) for row in frame_rows], ":", label="阶段2模型内部虚功 X")
    axes[0, 0].set_title("X方向虚功检查")
    axes[0, 0].set_xlabel("时间 / s")
    axes[0, 0].set_ylabel("虚功 / N")
    axes[0, 0].legend()
    axes[0, 1].plot(times, [float(row["阶段1内部虚功Y/N"]) for row in frame_rows], label="阶段1内部虚功 Y")
    axes[0, 1].plot(times, [float(row["阶段1外部虚功Y/N"]) for row in frame_rows], "--", label="阶段1外部虚功 Y")
    axes[0, 1].plot(times, [float(row["阶段2内部虚功Y/N"]) for row in frame_rows], ":", label="阶段2模型内部虚功 Y")
    axes[0, 1].set_title("Y方向虚功检查")
    axes[0, 1].set_xlabel("时间 / s")
    axes[0, 1].set_ylabel("虚功 / N")
    axes[0, 1].legend()
    axes[1, 0].plot(
        [float(row["等效塑性应变"]) for row in model_rows],
        [float(row["等效应力/MPa"]) for row in model_rows],
        label="DIC/边界等效应力",
    )
    model_styles = {
        "Linear模型应力/MPa": "--",
        "Ludwik模型应力/MPa": ":",
        "Swift模型应力/MPa": "-.",
        "Voce I（通用）模型应力/MPa": "--",
        "Voce II（通用）模型应力/MPa": "-",
    }
    for column, style in model_styles.items():
        model_name = column.replace("模型应力/MPa", "")
        model_rows_for_plot = [row for row in model_rows if row[column] != ""]
        if model_rows_for_plot:
            axes[1, 0].plot(
                [float(row["等效塑性应变"]) for row in model_rows_for_plot],
                [float(row[column]) for row in model_rows_for_plot],
                style,
                label=f"{model_name}模型",
            )
    axes[1, 0].set_title("等效应力—等效塑性应变")
    axes[1, 0].set_xlabel("等效塑性应变")
    axes[1, 0].set_ylabel("应力 / MPa")
    axes[1, 0].legend()
    axes[1, 1].plot(
        [float(row["边界σx/MPa"]) for row in frame_rows],
        [float(row["边界σy/MPa"]) for row in frame_rows],
        marker=".",
        label="实验应力状态",
    )
    axes[1, 1].set_title("平面应力空间")
    axes[1, 1].set_xlabel("σx / MPa")
    axes[1, 1].set_ylabel("σy / MPa")
    axes[1, 1].legend()
    fig.suptitle(f"{experiment_id} 自建 VFM：ROI {geometry['length_x_mm']:.2f}×{geometry['length_y_mm']:.2f} mm，厚度 1 mm")
    fig.savefig(output_dir / f"{experiment_id}_虚功检查.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)
    if elastic_progress:
        axes[0].plot(range(1, len(elastic_progress) + 1), [row["E/MPa"] for row in elastic_progress], marker=".")
    axes[0].set_title("E逐帧累计拟合稳定性")
    axes[0].set_xlabel("累计拟合点数")
    axes[0].set_ylabel("E / MPa")
    if hardening_progress:
        axes[1].plot(range(1, len(hardening_progress) + 1), [row["Y/MPa"] for row in hardening_progress], label="Y")
        axes[1].plot(range(1, len(hardening_progress) + 1), [row["H/MPa"] for row in hardening_progress], label="H")
    axes[1].set_title("Y/H逐帧累计拟合稳定性")
    axes[1].set_xlabel("累计拟合点数")
    axes[1].set_ylabel("参数 / MPa（对称对数刻度）")
    axes[1].set_yscale("symlog", linthresh=100.0)
    axes[1].legend()
    fig.suptitle(f"{experiment_id} 参数稳定性（不是 MatchID 迭代轨迹）")
    fig.savefig(output_dir / f"{experiment_id}_参数收敛.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 6), constrained_layout=True)
    x_values = [float(row["边界σx/MPa"]) for row in frame_rows]
    y_values = [float(row["边界σy/MPa"]) for row in frame_rows]
    ax.plot(x_values, y_values, marker=".", label="实验应力状态")
    if x_values or y_values:
        limit = max(x_values + y_values) * 1.05
        ax.plot([0.0, limit], [0.0, limit], "--", label="等双轴参考线")
    ax.set_title(f"{experiment_id} 应力空间")
    ax.set_xlabel("σx / MPa")
    ax.set_ylabel("σy / MPa")
    ax.legend()
    fig.savefig(output_dir / f"{experiment_id}_应力空间.png", dpi=160)
    plt.close(fig)


def process_experiment(entry: dict, batch: dict, self_config: dict) -> dict:
    experiment_id = entry["experiment_id"]
    output_root = Path(batch["output_root"])
    preparation_dir = output_root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备" / experiment_id
    index_path = preparation_dir / f"{experiment_id}_DIC全场—力索引.csv"
    merged_dir = preparation_dir / "merged"
    result_dir = output_root / self_config["output_directory"] / "实验结果" / experiment_id
    if entry.get("loading_mode") not in self_config.get("eligible_loading_modes", []):
        return {
            "实验编号": experiment_id,
            "状态": "跳过：单轴几何/厚度/边界待核实",
            "说明": self_config["ineligible_mode_reason"],
        }
    if not entry.get("formal_vfm_allowed", False):
        return {"实验编号": experiment_id, "状态": "跳过：配置禁止正式 VFM"}
    if not index_path.is_file() or not merged_dir.is_dir():
        return {"实验编号": experiment_id, "状态": "阻断：缺少 DIC—力合并输入"}

    index_rows = _read_index(index_path)
    geometry = _geometry(Path(entry["dic_job_file"]))
    thickness = float(self_config["geometry"]["roi_thickness_mm"])
    nu = float(self_config["nu"])
    frame_data: list[dict] = []
    baseline: dict[str, float] | None = None
    baseline_points: list[dict[str, float]] | None = None
    for row in index_rows:
        photo = row["照片"]
        frame_path = merged_dir / f"{Path(photo).stem}_DIC全场—力.csv"
        raw_points = _read_frame_points(frame_path)
        if baseline_points is None:
            baseline_points = raw_points
        points = _align_frame_points(baseline_points, raw_points)
        point_count = len(points)
        means = {
            key: sum(point[key] for point in points) / point_count
            for key in ("exx", "eyy", "exy")
        }
        exx = means["exx"]
        eyy = means["eyy"]
        exy = means["exy"]
        if baseline is None:
            baseline = {key: 0.0 for key in ("exx", "eyy", "exy")}
        force_x = _finite(row["X向力/N"], f"{experiment_id}/{photo}/X")
        force_y = _finite(row["Y向力/N"], f"{experiment_id}/{photo}/Y")
        if force_x < -1e-9 or force_y < -1e-9:
            raise ValueError(f"{experiment_id}/{photo} 存在负拉伸力")
        # 旋转后边界：顶部/底部是机器 X，左右是机器 Y。
        # 因此机器 X 对应 DIC 竖直方向 y/eyy，机器 Y 对应 DIC 水平方向 x/exx。
        axes = rotated_machine_axes(
            exx=exx,
            eyy=eyy,
            length_x_mm=float(geometry["length_x_mm"]),
            length_y_mm=float(geometry["length_y_mm"]),
        )
        machine_exx = axes["machine_x_strain"]
        machine_eyy = axes["machine_y_strain"]
        sigma_x = force_x / (thickness * axes["machine_x_edge_length_mm"])
        sigma_y = force_y / (thickness * axes["machine_y_edge_length_mm"])
        coefficient_x, coefficient_y = plane_stress_virtual_work_coefficients(
            exx=machine_exx,
            eyy=machine_eyy,
            nu=nu,
            area_mm2=float(geometry["area_mm2"]),
            thickness_mm=thickness,
            length_x_mm=axes["machine_x_virtual_length_mm"],
            length_y_mm=axes["machine_y_virtual_length_mm"],
        )
        pointwise = integrate_plane_stress_virtual_work_coefficients(
            points=points,
            nu=nu,
            thickness_mm=thickness,
            length_x_mm=axes["machine_x_virtual_length_mm"],
            length_y_mm=axes["machine_y_virtual_length_mm"],
            roi_bounds=geometry["roi_bounds_mm"],
        )
        frame_data.append(
            {
                "实验编号": experiment_id,
                "照片": photo,
                "时间/s": _finite(row["时间/s"], f"{experiment_id}/{photo}/time"),
                "point_count": point_count,
                "mean_exx": exx,
                "mean_eyy": eyy,
                "mean_exy": exy,
                "force_x": force_x,
                "force_y": force_y,
                "sigma_x": sigma_x,
                "sigma_y": sigma_y,
                "equivalent_stress": equivalent_stress_plane_stress(sigma_x, sigma_y),
                "coefficient_x": float(pointwise["coefficient_x"]),
                "coefficient_y": float(pointwise["coefficient_y"]),
                "baseline_coefficient_x": coefficient_x,
                "baseline_coefficient_y": coefficient_y,
                "integrated_area_mm2": float(pointwise["integrated_area_mm2"]),
                "area_ratio": float(pointwise["area_ratio"]),
                "valid_triangle_count": int(pointwise["valid_triangle_count"]),
                "excluded_point_count": int(pointwise["excluded_point_count"]),
                "plastic_strain": 0.0,
            }
        )

    loading_mode = entry.get("loading_mode", "")
    if loading_mode == "双轴":
        active_axes = ["X", "Y"]
    else:
        active_axes = [axis for axis in ("X", "Y") if axis in loading_mode]
    minimum_force = float(self_config["minimum_force_n"])
    strain_limit = float(self_config["elastic_strain_limit"])
    elastic_indices = [
        index
        for index, row in enumerate(frame_data)
        if max(abs(row["mean_exx"]), abs(row["mean_eyy"])) <= strain_limit
        and any(row[f"force_{axis.lower()}"] > minimum_force for axis in active_axes)
    ]
    coefficients: list[float] = []
    forces: list[float] = []
    for index in elastic_indices:
        for axis in active_axes:
            coefficient = frame_data[index][f"coefficient_{axis.lower()}"]
            force = frame_data[index][f"force_{axis.lower()}"]
            if coefficient != 0.0 and force > minimum_force:
                coefficients.append(coefficient)
                forces.append(force)
    elastic_fit = fit_elastic_modulus(coefficients=coefficients, external_forces=forces) if len(coefficients) >= 2 else None
    modulus = None if elastic_fit is None else float(elastic_fit["modulus_mpa"])
    if elastic_fit is None:
        stage1_quality = {"status": "NOT_COMPUTED"}
    else:
        maximum_active_force = max(
            frame_data[index][f"force_{axis.lower()}"]
            for index in elastic_indices
            for axis in active_axes
        )
        relative_rmse = float(elastic_fit["rmse_n"]) / maximum_active_force
        acceptance_limit = float(self_config["stage1_acceptance"]["max_relative_rmse"])
        stage1_quality = {
            "status": "PASS" if relative_rmse <= acceptance_limit else "REVIEW_REQUIRED",
            "relative_rmse": relative_rmse,
            "maximum_active_force_n": maximum_active_force,
            "acceptance_limit": acceptance_limit,
        }

    if modulus is not None and baseline is not None:
        for row in frame_data:
            row["plastic_strain"] = equivalent_plastic_strain_plane_stress(
                exx=row["mean_eyy"],
                eyy=row["mean_exx"],
                exy=row["mean_exy"],
                sigma_x_mpa=row["sigma_x"],
                sigma_y_mpa=row["sigma_y"],
                modulus_mpa=modulus,
                nu=nu,
            )
    peak_index = max(range(len(frame_data)), key=lambda index: frame_data[index]["equivalent_stress"])
    minimum_plastic_strain = float(self_config["minimum_plastic_strain"])
    hardening_indices = [
        index
        for index, row in enumerate(frame_data)
        if index <= peak_index
        and row["equivalent_stress"] > minimum_force / max(float(geometry["length_x_mm"]), float(geometry["length_y_mm"]))
        and row["plastic_strain"] >= minimum_plastic_strain
    ]
    minimum_hardening_points = int(self_config["stage2_acceptance"]["minimum_points"])
    hardening_fit = (
        fit_linear_hardening(
            plastic_strains=[frame_data[index]["plastic_strain"] for index in hardening_indices],
            equivalent_stresses=[frame_data[index]["equivalent_stress"] for index in hardening_indices],
        )
        if len(hardening_indices) >= minimum_hardening_points
        else None
    )
    model_fits = (
        fit_hardening_models(
            plastic_strains=[frame_data[index]["plastic_strain"] for index in hardening_indices],
            equivalent_stresses=[frame_data[index]["equivalent_stress"] for index in hardening_indices],
        )
        if hardening_fit is not None
        else []
    )
    model_fit_by_name = {row["model"]: row for row in model_fits}
    hardening_index_set = set(hardening_indices)
    if hardening_fit is None:
        stage2_quality = {
            "status": "NOT_COMPUTED",
            "point_count": len(hardening_indices),
            "minimum_points": minimum_hardening_points,
        }
    else:
        stress_range = max(frame_data[index]["equivalent_stress"] for index in hardening_indices)
        relative_rmse = float(hardening_fit["rmse_mpa"]) / stress_range
        acceptance_limit = float(self_config["stage2_acceptance"]["max_relative_rmse"])
        stage2_quality = {
            "status": "PASS" if relative_rmse <= acceptance_limit else "REVIEW_REQUIRED",
            "point_count": len(hardening_indices),
            "minimum_points": minimum_hardening_points,
            "relative_rmse": relative_rmse,
            "acceptance_limit": acceptance_limit,
        }

    for index, row in enumerate(frame_data):
        row["stage1_internal_x"] = 0.0 if modulus is None else modulus * row["coefficient_x"]
        row["stage1_internal_y"] = 0.0 if modulus is None else modulus * row["coefficient_y"]
        row["stage1_residual_x"] = row["stage1_internal_x"] - row["force_x"]
        row["stage1_residual_y"] = row["stage1_internal_y"] - row["force_y"]
        if hardening_fit is None or row["equivalent_stress"] <= 0.0 or index not in hardening_index_set:
            model_equivalent = None
            model_sigma_x = 0.0
            model_sigma_y = 0.0
            row["model_predictions"] = {}
        else:
            row["model_predictions"] = {
                model: hardening_model_value(model, row["plastic_strain"], fit["parameters"])
                for model, fit in model_fit_by_name.items()
            }
            model_equivalent = row["model_predictions"]["Linear"]
            scale = model_equivalent / row["equivalent_stress"]
            model_sigma_x = scale * row["sigma_x"]
            model_sigma_y = scale * row["sigma_y"]
        row["model_equivalent_stress"] = model_equivalent
        row["stage2_internal_x"] = model_sigma_x * thickness * float(geometry["area_mm2"]) / float(geometry["length_y_mm"])
        row["stage2_internal_y"] = model_sigma_y * thickness * float(geometry["area_mm2"]) / float(geometry["length_x_mm"])
        row["stage2_residual_x"] = row["stage2_internal_x"] - row["force_x"]
        row["stage2_residual_y"] = row["stage2_internal_y"] - row["force_y"]

    output_frame_rows = []
    for row in frame_data:
        output_frame_rows.append(
            {
                "实验编号": row["实验编号"],
                "照片": row["照片"],
                "时间/s": f"{row['时间/s']:.6f}",
                "点数": row["point_count"],
                "平均exx": f"{row['mean_exx']:.10g}",
                "平均eyy": f"{row['mean_eyy']:.10g}",
                "平均exy": f"{row['mean_exy']:.10g}",
                "X向力/N": f"{row['force_x']:.8f}",
                "Y向力/N": f"{row['force_y']:.8f}",
                "边界σx/MPa": f"{row['sigma_x']:.8f}",
                "边界σy/MPa": f"{row['sigma_y']:.8f}",
                "等效应力/MPa": f"{row['equivalent_stress']:.8f}",
                "等效塑性应变": f"{row['plastic_strain']:.10g}",
                "X虚场系数/N每MPa": f"{row['coefficient_x']:.10g}",
                "Y虚场系数/N每MPa": f"{row['coefficient_y']:.10g}",
                "基线X虚场系数/N每MPa": f"{row['baseline_coefficient_x']:.10g}",
                "基线Y虚场系数/N每MPa": f"{row['baseline_coefficient_y']:.10g}",
                "积分面积/mm2": f"{row['integrated_area_mm2']:.8f}",
                "面积比": f"{row['area_ratio']:.8f}",
                "有效三角形数": row["valid_triangle_count"],
                "排除点数": row["excluded_point_count"],
                "阶段1内部虚功X/N": f"{row['stage1_internal_x']:.8f}",
                "阶段1外部虚功X/N": f"{row['force_x']:.8f}",
                "阶段1残差X/N": f"{row['stage1_residual_x']:.8f}",
                "阶段1内部虚功Y/N": f"{row['stage1_internal_y']:.8f}",
                "阶段1外部虚功Y/N": f"{row['force_y']:.8f}",
                "阶段1残差Y/N": f"{row['stage1_residual_y']:.8f}",
                "阶段2模型等效应力/MPa": "" if row["model_equivalent_stress"] is None else f"{row['model_equivalent_stress']:.8f}",
                "阶段2内部虚功X/N": f"{row['stage2_internal_x']:.8f}",
                "阶段2残差X/N": f"{row['stage2_residual_x']:.8f}",
                "阶段2内部虚功Y/N": f"{row['stage2_internal_y']:.8f}",
                "阶段2残差Y/N": f"{row['stage2_residual_y']:.8f}",
            }
        )
    model_rows = []
    for row in frame_data:
        model_row = {
            "照片": row["照片"],
            "时间/s": f"{row['时间/s']:.6f}",
            "等效塑性应变": f"{row['plastic_strain']:.10g}",
            "等效应力/MPa": f"{row['equivalent_stress']:.8f}",
        }
        for model in HARDENING_MODEL_NAMES:
            value = row["model_predictions"].get(model)
            model_row[f"{model}模型应力/MPa"] = "" if value is None else f"{value:.8f}"
        model_rows.append(model_row)
    stress_rows = [
        {
            "照片": row["照片"],
            "时间/s": f"{row['时间/s']:.6f}",
            "σx/MPa": f"{row['sigma_x']:.8f}",
            "σy/MPa": f"{row['sigma_y']:.8f}",
            "等效应力/MPa": f"{row['equivalent_stress']:.8f}",
        }
        for row in frame_data
    ]
    elastic_progress = _fit_progressive_elastic(frame_data, elastic_indices, active_axes) if elastic_indices else []
    hardening_progress = _fit_progressive_hardening(frame_data, hardening_indices) if hardening_indices and len(hardening_indices) >= 2 else []
    result = {
        "实验编号": experiment_id,
        "状态": (
            "SELF_VFM_CANDIDATE"
            if (
                modulus is not None
                and hardening_fit is not None
                and stage1_quality["status"] == "PASS"
                and stage2_quality["status"] == "PASS"
            )
            else "SELF_VFM_REVIEW_REQUIRED"
            if modulus is not None
            else "SELF_VFM_PARTIAL"
        ),
        "方法": {
            "虚场": "旋转后X（顶部/底部）：u*=0, v*=y/Ly；Y（左右）：u*=x/Lx, v*=0",
            "边界力": "用户确认的外围机器力直接作为ROI边界合力",
            "厚度_mm": thickness,
            "外围整体厚度_mm": float(self_config["geometry"]["overall_thickness_mm"]),
            "nu": nu,
            "面积_mm2": geometry["area_mm2"],
            "ROI长度_mm": [geometry["length_x_mm"], geometry["length_y_mm"]],
            "DIC应变": "平均全场exx/eyy/exy；旋转后机器X=eyy、机器Y=exx；exy按张量剪切应变使用，gamma不参与",
            "阶段2": "平面应力边界应力减去弹性部分，并用塑性不可压缩估计等效塑性应变；这是自建候选算法，不是MatchID内部算法复刻",
        },
        "输入": {"照片帧数": len(frame_data), "有效DIC点数": sorted({row["point_count"] for row in frame_data}), "峰值帧": frame_data[peak_index]["照片"]},
        "阶段1": {
            "拟合帧数": len(elastic_indices),
            "首末拟合帧": None if not elastic_indices else [frame_data[elastic_indices[0]]["照片"], frame_data[elastic_indices[-1]]["照片"]],
            "E_MPa": modulus,
            "nu": nu,
            "质量": stage1_quality,
            "虚功拟合": elastic_fit,
        },
        "阶段2": {
            "拟合帧数": len(hardening_indices),
            "首末拟合帧": None if not hardening_indices else [frame_data[hardening_indices[0]]["照片"], frame_data[hardening_indices[-1]]["照片"]],
            "质量": stage2_quality,
            "Y_MPa": None if hardening_fit is None else hardening_fit["yield_mpa"],
            "H_MPa": None if hardening_fit is None else hardening_fit["hardening_mpa"],
            "线性模型拟合": hardening_fit,
            "模型比较": model_fits,
        },
        "限制": [
            "已实现Linear及通用Ludwik、Swift、经典Voce和线性+指数Voce比较；这些通用Voce名称不等同于MatchID界面同名模型。",
            "阶段2是平面应力合力—DIC约化识别，不宣称等同于MatchID内部J2/Newton求解。",
            "单组数据的候选参数须经过虚功残差、参数稳定性、边界和跨试验验证后才能作为材料参数。",
        ],
    }
    result_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(result_dir / f"{experiment_id}_内外虚功.csv", output_frame_rows, FRAME_FIELDS)
    _write_csv(result_dir / f"{experiment_id}_模型对比.csv", model_rows, MODEL_COMPARISON_FIELDS)
    _write_csv(result_dir / f"{experiment_id}_应力空间.csv", stress_rows, ["照片", "时间/s", "σx/MPa", "σy/MPa", "等效应力/MPa"])
    _write_csv(result_dir / f"{experiment_id}_参数收敛.csv", elastic_progress + hardening_progress, ["样本末帧", "E/MPa", "虚功均方根残差/N", "样本点数", "Y/MPa", "H/MPa", "拟合均方根残差/MPa"])
    _write_json(result_dir / f"{experiment_id}_结果.json", result)
    _plot_experiment(result_dir, experiment_id, output_frame_rows, elastic_progress, hardening_progress, model_rows, geometry)
    return {
        "实验编号": experiment_id,
        "状态": result["状态"],
        "帧数": len(frame_data),
        "E/MPa": modulus,
        "Y/MPa": None if hardening_fit is None else hardening_fit["yield_mpa"],
        "H/MPa": None if hardening_fit is None else hardening_fit["hardening_mpa"],
        "虚功文件": str(result_dir / f"{experiment_id}_内外虚功.csv"),
    }


def run(batch_config_path: Path, self_config_path: Path) -> dict:
    batch = json.loads(batch_config_path.read_text(encoding="utf-8"))
    self_config = json.loads(self_config_path.read_text(encoding="utf-8"))
    results = [process_experiment(entry, batch, self_config) for entry in batch["experiments"]]
    output_root = Path(batch["output_root"])
    output_dir = output_root / self_config["output_directory"] / "汇总"
    output_dir.mkdir(parents=True, exist_ok=True)
    fields = ["实验编号", "状态", "帧数", "E/MPa", "Y/MPa", "H/MPa", "虚功文件"]
    _write_csv(output_dir / "PA12自建VFM结果.csv", results, fields)
    _write_json(
        output_dir / "PA12自建VFM结果.json",
        {
            "状态": "当前为自建VFM阶段结果；未替代MatchID正式识别",
            "结果": results,
            "配置": str(self_config_path),
        },
    )
    lines = [
        "# PA12 自建 VFM 阶段报告",
        "",
        "本报告使用旋转后的 DIC 全场—力合并数据；原始 JPG、DAT、XLS 未修改。",
        "",
        "## 当前方法",
        "",
        "- 阶段1固定 ν=0.375，使用常应变单位虚场和中心 ROI 厚度 1 mm，对加载初期 DIC 全场积分并识别 E。",
        "- 阶段2固定阶段1 E 和 ν，使用边界合力换算的平面应力与 DIC 应变约化识别 Linear 等向硬化 Y/H。",
        "- 外围整体厚度 3 mm 只作几何记录；虚功和应力使用中心 ROI 厚度 1 mm。",
        "- 这是可复现的自建候选算法；它不读取 MatchID 内部的 Newton/J2 状态，也不把界面中间值写成最终材料参数。",
        "",
        "## 结果",
        "",
        "| 实验编号 | 状态 | 帧数 | E/MPa | Y/MPa | H/MPa |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in results:
        lines.append(
            f"| {row.get('实验编号','')} | {row.get('状态','')} | {row.get('帧数','')} | "
            f"{row.get('E/MPa','')} | {row.get('Y/MPa','')} | {row.get('H/MPa','')} |"
        )
    lines += [
        "",
        "## 限制",
        "",
        "- 已输出 Linear、通用 Ludwik、通用 Swift、经典 Voce I 和线性+指数 Voce II 的比较；Voce I/II 的通用名称不等同于 MatchID 界面同名模型，软件内部公式仍待核实。",
        "- Y/H 是阶段2约化识别候选，需与 MatchID 可导出的内外虚功、应力空间和参数边界逐组对照。",
        "- S23 因视觉断裂处无力数据、S24 因预载释放记录不进入本批次。",
        "",
        "## 输出目录",
        "",
        "- 每个实验的 `实验结果/<实验编号>/` 包含内外虚功、模型对比、应力空间、参数稳定性 CSV、结果 JSON 和 PNG。",
        "- `汇总/PA12自建VFM结果.csv` 和 `.json` 是总索引。",
    ]
    (output_dir / "PA12自建VFM阶段报告.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"output_directory": str(output_dir), "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description="运行 PA12 自建 VFM 阶段1/阶段2候选识别")
    parser.add_argument("--batch-config", type=Path, default=Path("configs/pa12_rotated_batch.json"))
    parser.add_argument("--config", type=Path, default=Path("configs/pa12_self_vfm.json"))
    args = parser.parse_args()
    print(json.dumps(run(args.batch_config, args.config), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
