import gzip
import json

import numpy as np
import pandas as pd
import pytest

from tools.pa12_finite_kinematics import (
    plane_stress_virtual_work_residuals,
    profile_elastic_parameters,
)
import tools.run_pa12_finite_vfm_diagnostic as diagnostic
from tools.run_pa12_finite_vfm_diagnostic import (
    _analysis_domains,
    _analyze_domain,
    _deformation_quality,
    _read_reference_frame,
    _reference_field_source,
)
from tools.run_pa12_self_vfm import _geometry


def test_geometry_reads_subset_size_from_job_metadata(tmp_path):
    job_path = tmp_path / "Job.m2inp"
    job_path.write_text(
        "<Reference$image>=<000000.jpg>"
        "<Conversion>=<0.5>"
        "<Shape>=<2;0;False;4;0;0;10;0;10;8;0;8>"
        "<Step$size>=<3>"
        "<Subset$size>=<15>",
        encoding="utf-8",
    )

    geometry = _geometry(job_path)

    assert geometry["subset_size_px"] == 15


def test_read_index_accepts_s16_manual_mapping_headers(tmp_path):
    from tools.run_pa12_self_vfm import _read_index

    index_path = tmp_path / "manual_index.csv"
    index_path.write_text(
        '"DIC_File","照片","时间_s","X向力_N","Y向力_N"\n'
        '"0","000000.jpg","0.001484375","0.32","-0.24"\n'
        '"1","000001.jpg","0.1020","4.82","4.26"\n',
        encoding="utf-8-sig",
    )

    rows = _read_index(index_path)

    assert [row["照片"] for row in rows] == ["000000.jpg", "000001.jpg"]
    assert [row["时间/s"] for row in rows] == ["0.001484375", "0.1020"]
    assert [row["X向力/N"] for row in rows] == ["0.32", "4.82"]
    assert [row["Y向力/N"] for row in rows] == ["-0.24", "4.26"]


def test_reference_frame_reads_job_dat_without_a_force_index_row(tmp_path):
    dat_path = tmp_path / "000000.jpg.dat"
    payload = (
        "<11>=<0.5>"
        "<18>=<0;100;200;0;0;3;4;1;2;0;0;0;0;0.9;0.1;0;1;0>"
        "<53>=<0;True;1;2;3;4;5;6;0.9;1;2;3>"
        "<18>=<1;110;210;0;0;5;6;7;8;0;0;0;0;0.8;0.2;0;1;0>"
        "<53>=<1;True;2;3;4;5;6;7;0.9;1;2;3>"
    )
    with gzip.open(dat_path, "wb") as handle:
        handle.write(payload.encode("latin1"))
    config = {
        "reference_photo": "000000.jpg",
        "reference_dat_file": str(dat_path),
    }

    assert _reference_field_source(config, tmp_path) == dat_path
    reference = _read_reference_frame(config, tmp_path)

    np.testing.assert_allclose(reference["x"], [51.5, 57.5])
    np.testing.assert_allclose(reference["y"], [102.0, 108.0])
    np.testing.assert_allclose(reference["u"], [0.5, 3.5])
    np.testing.assert_allclose(reference["v"], [1.0, 4.0])


def test_analysis_domains_keep_job_roi_and_dic_inset_geometry_separate():
    reference = np.array([[2.0, 1.0], [2.0, 7.0], [6.0, 7.0], [6.0, 1.0]])
    job_geometry = {
        "length_x_mm": 10.0,
        "length_y_mm": 8.0,
        "area_mm2": 80.0,
        "roi_polygon_mm": [(0.0, 0.0), (10.0, 0.0), (10.0, 8.0), (0.0, 8.0)],
        "conversion_mm_per_pixel": 1.0,
        "subset_size_px": 3,
    }
    machine_axes = {
        "X": {"coordinate": "y"},
        "Y": {"coordinate": "x"},
    }

    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    domains = _analysis_domains(reference, job_geometry, machine_axes, triangles)

    assert [domain["id"] for domain in domains] == [
        "full_job_roi",
        "dic_subset_inset_sensitivity",
    ]
    assert domains[0]["virtual_field_lengths_mm"] == (8.0, 10.0)
    assert domains[0]["roi_area_mm2"] == 80.0
    assert domains[0]["label"] == "Job ROI 交叠面积积分"
    assert domains[0]["measured_mesh_area_mm2"] == pytest.approx(24.0)
    assert domains[0]["triangle_integration_areas_mm2"].sum() == pytest.approx(24.0)
    assert domains[1]["virtual_field_lengths_mm"] == (8.0, 10.0)
    assert domains[1]["roi_area_mm2"] == 48.0
    assert domains[1]["measured_mesh_area_mm2"] == pytest.approx(24.0)
    assert domains[1]["triangle_integration_areas_mm2"].sum() == pytest.approx(24.0)
    assert domains[1]["label"] == "DIC subset 内缩域独立敏感性"


def test_analysis_domains_integrate_authorized_repaired_polygon_components():
    main_polygon = np.array(
        [[0.0, 0.0], [4.0, 0.0], [4.0, 4.0], [0.0, 4.0]]
    )
    fragment_polygon = np.array(
        [[5.0, 0.0], [5.5, 0.0], [5.0, 0.5]]
    )
    reference = np.vstack((main_polygon[:3], fragment_polygon))
    triangles = np.array([[0, 1, 2], [3, 4, 5]])
    job_geometry = {
        "length_x_mm": 5.5,
        "length_y_mm": 4.0,
        "area_mm2": 16.125,
        "roi_polygon_mm": main_polygon.tolist(),
        "roi_polygons_mm": [main_polygon.tolist(), fragment_polygon.tolist()],
        "conversion_mm_per_pixel": 1.0,
        "subset_size_px": 1,
    }
    machine_axes = {"X": {"coordinate": "x"}, "Y": {"coordinate": "y"}}

    domains = _analysis_domains(reference, job_geometry, machine_axes, triangles)

    assert domains[0]["measured_mesh_area_mm2"] == pytest.approx(8.125)


def test_analysis_domains_erode_job_roi_by_exact_15_by_15_pixel_center_support():
    reference = np.array(
        [[0.0, 0.0], [30.0, 0.0], [30.0, 20.0], [0.0, 20.0], [15.0, 10.0]]
    )
    job_geometry = {
        "length_x_mm": 30.0,
        "length_y_mm": 20.0,
        "area_mm2": 600.0,
        "roi_polygon_mm": [
            (0.0, 0.0),
            (30.0, 0.0),
            (30.0, 20.0),
            (0.0, 20.0),
        ],
        "conversion_mm_per_pixel": 0.1,
        "subset_size_px": 15,
    }
    machine_axes = {"X": {"coordinate": "x"}, "Y": {"coordinate": "y"}}
    triangles = np.array(
        [[4, 0, 1], [4, 1, 2], [4, 2, 3], [4, 3, 0]], dtype=int
    )

    full_job, dic_inset = _analysis_domains(
        reference, job_geometry, machine_axes, triangles
    )

    assert dic_inset["subset_size_px"] == 15
    assert dic_inset["subset_support_half_width_px"] == 7.0
    assert full_job["roi_area_mm2"] == pytest.approx(600.0)
    assert dic_inset["roi_area_mm2"] == pytest.approx(28.6 * 18.6)
    assert dic_inset["measured_mesh_area_mm2"] == pytest.approx(28.6 * 18.6)


def test_analysis_domains_share_job_defined_boundary_fields_with_inset_sensitivity():
    polygon = np.array(
        [[0.0, 0.0], [10.0, 0.0], [10.5, 8.0], [1.5, 8.0], [0.2, 0.15]]
    )
    reference = np.vstack((polygon, [5.0, 4.0]))
    triangles = np.array(
        [[5, index, (index + 1) % len(polygon)] for index in range(len(polygon))]
    )
    job_geometry = {
        "length_x_mm": float(np.ptp(polygon[:, 0])),
        "length_y_mm": float(np.ptp(polygon[:, 1])),
        "area_mm2": 76.0,
        "roi_polygon_mm": polygon.tolist(),
        "conversion_mm_per_pixel": 1.0,
        "subset_size_px": 3,
    }
    machine_axes = {"X": {"coordinate": "x"}, "Y": {"coordinate": "y"}}

    full_job, dic_inset = _analysis_domains(
        reference, job_geometry, machine_axes, triangles
    )

    fields = full_job["virtual_field_values"]
    assert dic_inset["virtual_field_values"] is fields
    assert 0.0 < dic_inset["roi_area_mm2"] < full_job["roi_area_mm2"]
    assert dic_inset["triangle_integration_areas_mm2"].sum() == pytest.approx(
        dic_inset["measured_mesh_area_mm2"]
    )
    np.testing.assert_allclose(fields[0, [3, 4], 0], 0.0, atol=1e-14)
    np.testing.assert_allclose(fields[0, [1, 2], 0], 1.0, atol=1e-14)
    np.testing.assert_allclose(fields[1, [0, 1], 1], 0.0, atol=1e-14)
    np.testing.assert_allclose(fields[1, [2, 3], 1], 1.0, atol=1e-14)


def test_analysis_domains_use_triangulated_dic_support_not_bounding_rectangle():
    reference = np.array([[0.0, 0.0], [4.0, 0.0], [3.0, 4.0], [1.0, 4.0]])
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    job_geometry = {
        "length_x_mm": 4.0,
        "length_y_mm": 4.0,
        "area_mm2": 12.0,
        "bounding_area_mm2": 16.0,
        "roi_polygon_mm": [(0.0, 0.0), (0.0, 4.0), (4.0, 3.0), (4.0, 1.0)],
        "conversion_mm_per_pixel": 1.0,
        "subset_size_px": 3,
    }
    machine_axes = {
        "X": {"coordinate": "y"},
        "Y": {"coordinate": "x"},
    }

    full_job, dic_inset = _analysis_domains(
        reference, job_geometry, machine_axes, triangles
    )

    assert full_job["roi_area_mm2"] == pytest.approx(12.0)
    assert full_job["measured_mesh_area_mm2"] == pytest.approx(12.0)
    assert 0.0 < dic_inset["roi_area_mm2"] < 12.0
    assert 0.0 < dic_inset["measured_mesh_area_mm2"] < 12.0
    assert full_job["triangle_integration_areas_mm2"].sum() == pytest.approx(12.0)
    assert dic_inset["triangle_integration_areas_mm2"].sum() == pytest.approx(
        dic_inset["measured_mesh_area_mm2"]
    )
    fields = full_job["virtual_field_values"]
    np.testing.assert_allclose(fields[0, [0, 3], 0], 0.0, atol=1e-14)
    np.testing.assert_allclose(fields[0, [1, 2], 0], 1.0, atol=1e-14)
    np.testing.assert_allclose(fields[1, [0, 1], 1], 0.0, atol=1e-14)
    np.testing.assert_allclose(fields[1, [2, 3], 1], 1.0, atol=1e-14)


def test_elastic_modulus_profile_uses_the_same_general_nodal_virtual_fields():
    coordinates = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 1.0]])
    triangles = np.array([[0, 1, 2]])
    displacements = np.array(
        [[[0.0, 0.0], [0.03, 0.01], [-0.01, 0.02]]]
    )
    virtual_fields = np.array(
        [
            [[0.0, 0.0], [1.0, 0.0], [0.25, 0.0]],
            [[0.0, 0.5], [0.0, 0.25], [0.0, 1.0]],
        ]
    )
    expected_modulus = 2500.0
    poisson_ratio = 0.34
    resultants = plane_stress_virtual_work_residuals(
        coordinates,
        triangles,
        displacements,
        np.zeros((1, 2)),
        1.2,
        expected_modulus,
        poisson_ratio,
        virtual_field_lengths_mm=(2.0, 1.0),
        virtual_field_values=virtual_fields,
    )

    fitted = profile_elastic_parameters(
        coordinates,
        triangles,
        displacements,
        resultants,
        1.2,
        np.array([poisson_ratio]),
        virtual_field_lengths_mm=(2.0, 1.0),
        virtual_field_values=virtual_fields,
    )[0]

    assert fitted["youngs_modulus_mpa"] == pytest.approx(expected_modulus, rel=1e-12)
    assert fitted["residual_rms_n"] < 1e-10


def test_analysis_fits_uniaxial_modulus_from_selected_loading_axis_only():
    reference = np.array([[0.0, 0.0], [2.0, 0.0], [2.0, 1.0], [0.0, 1.0]])
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    displacement = reference @ np.diag([1.02, 0.99]).T - reference
    displacements = displacement[None, :, :]
    thickness, true_modulus, nu = 1.0, 1500.0, 0.33
    internal_resultants = plane_stress_virtual_work_residuals(
        reference,
        triangles,
        displacements,
        np.zeros((1, 2)),
        thickness,
        true_modulus,
        nu,
        virtual_field_lengths_mm=(2.0, 1.0),
    )
    uniaxial_resultants = internal_resultants.copy()
    uniaxial_resultants[:, 1] = 0.0
    domain = {
        "id": "full_job_roi",
        "virtual_field_lengths_mm": (2.0, 1.0),
        "triangle_integration_areas_mm2": np.array([1.0, 1.0]),
    }

    result = _analyze_domain(
        domain,
        reference,
        triangles,
        displacements,
        uniaxial_resultants,
        [0],
        thickness,
        nu,
        np.array([nu]),
        fit_axis_indices=(0,),
    )

    assert result["youngs_modulus_mpa"] == pytest.approx(true_modulus)
    assert result["fit_axis_indices"] == [0]
    assert result["fit_residual_rms_n"] < 1e-10
    assert result["all_axis_fit_residual_rms_n"] > 1.0


def test_deformation_quality_reports_jacobian_and_large_strain_distribution():
    reference = np.array([[0.0, 0.0], [2.0, 0.0], [2.0, 1.0], [0.0, 1.0]])
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    displacement = reference @ np.diag([1.1, 1.0]).T - reference

    quality = _deformation_quality(reference, triangles, displacement[None, :, :])

    assert quality["detF_min"] == pytest.approx(1.1)
    assert quality["detF_max"] == pytest.approx(1.1)
    assert quality["nonpositive_jacobian_triangle_count"] == 0
    assert quality["final_abs_almansi_component_quantiles"]["p50"] == pytest.approx(
        0.5 * (1.0 - 1.1**-2)
    )


def test_deformation_quality_preserves_per_frame_jacobian_and_strain_extremes():
    reference = np.array([[0.0, 0.0], [2.0, 0.0], [2.0, 1.0], [0.0, 1.0]])
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    stretches = [(1.1, 1.0), (0.01, 1.0), (-0.1, 1.0)]
    displacements = np.asarray(
        [reference @ np.diag(stretch).T - reference for stretch in stretches]
    )

    quality = _deformation_quality(reference, triangles, displacements)

    assert len(quality["per_frame"]) == 3
    assert quality["per_frame"][0]["detF_min"] == pytest.approx(1.1)
    assert quality["per_frame"][0]["nonpositive_jacobian_triangle_count"] == 0
    assert quality["per_frame"][1]["min_abs_detF"] == pytest.approx(0.01)
    assert quality["per_frame"][1]["max_abs_almansi_component"] == pytest.approx(4999.5)
    assert quality["per_frame"][2]["detF_min"] == pytest.approx(-0.1)
    assert quality["per_frame"][2]["nonpositive_jacobian_triangle_count"] == 2


def test_deformation_quality_keeps_exact_zero_jacobian_frame_auditable():
    reference = np.array([[0.0, 0.0], [2.0, 0.0], [2.0, 1.0], [0.0, 1.0]])
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    displacement = reference @ np.diag([0.0, 1.0]).T - reference

    quality = _deformation_quality(reference, triangles, displacement[None, :, :])

    assert quality["per_frame"][0]["nonpositive_jacobian_triangle_count"] == 2
    assert quality["per_frame"][0]["max_abs_almansi_component"] is None
    assert quality["final_abs_almansi_component_quantiles"]["max"] is None
    json.dumps(quality, allow_nan=False)


def test_virtual_work_output_blanks_physical_values_but_keeps_algebraic_diagnostics():
    forces = np.array([[10.0, 6.0], [12.0, 8.0]])
    residuals = np.array([[1.0, -2.0], [3.0, 4.0]])
    frame_quality = [
        {"nonpositive_jacobian_triangle_count": 0},
        {"nonpositive_jacobian_triangle_count": 1},
    ]

    output = diagnostic._virtual_work_output_arrays(forces, residuals, frame_quality)

    np.testing.assert_array_equal(output["physical_valid"], [True, False])
    np.testing.assert_allclose(output["internal_algebraic_n"][0], [11.0, 4.0])
    np.testing.assert_allclose(output["residual_algebraic_n"][1], [3.0, 4.0])
    assert np.isnan(output["internal_physical_n"][1]).all()
    assert np.isnan(output["external_physical_n"][1]).all()
    assert np.isnan(output["residual_physical_n"][1]).all()


def test_domain_analysis_keeps_singular_jacobian_frame_without_using_it_for_fit():
    reference = np.array([[0.0, 0.0], [2.0, 0.0], [2.0, 1.0], [0.0, 1.0]])
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    displacements = np.asarray(
        [
            reference @ np.diag([1.02, 1.01]).T - reference,
            reference @ np.diag([0.0, 1.0]).T - reference,
        ]
    )
    analysis = _analyze_domain(
        {
            "id": "full_job_roi",
            "label": "Job ROI",
            "virtual_field_lengths_mm": (2.0, 1.0),
            "roi_area_mm2": 1.0,
            "measured_mesh_area_mm2": 1.0,
            "triangle_integration_areas_mm2": np.array([0.5, 0.5]),
        },
        reference,
        triangles,
        displacements,
        np.array([[1.0, 1.0], [10.0, 10.0]]),
        [0],
        1.0,
        0.3,
        np.array([0.2, 0.3, 0.4]),
    )

    assert np.isnan(analysis["residuals_n"][1]).all()
    assert analysis["frame_kinematic_quality"][1]["nonpositive_jacobian_triangle_count"] == 2


def test_domain_analysis_excludes_invalid_fit_frames_and_reports_the_used_indices():
    reference = np.array([[0.0, 0.0], [2.0, 0.0], [2.0, 1.0], [0.0, 1.0]])
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    displacements = np.asarray(
        [
            reference @ np.diag([1.02, 1.01]).T - reference,
            reference @ np.diag([-0.1, 1.0]).T - reference,
        ]
    )
    analysis = _analyze_domain(
        {
            "id": "full_job_roi",
            "label": "Job ROI",
            "virtual_field_lengths_mm": (2.0, 1.0),
            "roi_area_mm2": 1.0,
            "measured_mesh_area_mm2": 1.0,
            "triangle_integration_areas_mm2": np.array([0.5, 0.5]),
        },
        reference,
        triangles,
        displacements,
        np.array([[1.0, 1.0], [10.0, 10.0]]),
        [0, 1],
        1.0,
        0.3,
        np.array([0.2, 0.3, 0.4]),
    )

    assert analysis["fit_frame_indices_used"] == [0]
    assert analysis["fit_frame_indices_excluded"] == [1]
    assert np.isfinite(analysis["residuals_n"][1]).all()


def test_analysis_fits_elastic_modulus_independently_for_each_domain():
    reference = np.array([[0.0, 0.0], [2.0, 0.0], [2.0, 1.0], [0.0, 1.0]])
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    stretches = [(1.02, 1.0), (1.04, 0.99)]
    displacements = np.asarray(
        [
            reference @ np.diag(stretch).T - reference
            for stretch in stretches
        ]
    )
    thickness, true_modulus, nu = 1.0, 1500.0, 0.33
    full_lengths = (4.0, 2.0)
    zero_resultants = np.zeros((len(stretches), 2))
    resultants = plane_stress_virtual_work_residuals(
        reference,
        triangles,
        displacements,
        zero_resultants,
        thickness,
        true_modulus,
        nu,
        virtual_field_lengths_mm=full_lengths,
    )
    full_domain = {
        "id": "full_job_roi",
        "virtual_field_lengths_mm": full_lengths,
        "triangle_integration_areas_mm2": np.array([1.0, 1.0]),
    }
    inset_domain = {
        "id": "dic_subset_inset_sensitivity",
        "virtual_field_lengths_mm": (2.0, 1.0),
        "triangle_integration_areas_mm2": np.array([1.0, 1.0]),
    }

    full_result = _analyze_domain(
        full_domain,
        reference,
        triangles,
        displacements,
        resultants,
        [0, 1],
        thickness,
        nu,
        np.array([0.2, 0.33, 0.45]),
    )
    inset_result = _analyze_domain(
        inset_domain,
        reference,
        triangles,
        displacements,
        resultants,
        [0, 1],
        thickness,
        nu,
        np.array([0.2, 0.33, 0.45]),
    )

    assert full_result["youngs_modulus_mpa"] == pytest.approx(true_modulus)
    assert inset_result["youngs_modulus_mpa"] == pytest.approx(true_modulus / 2.0)
    assert full_result["fit_residual_rms_n"] < 1e-10
    assert inset_result["fit_residual_rms_n"] < 1e-10


def test_indexed_reference_photo_reuses_loaded_dat_field(tmp_path, monkeypatch):
    output_root = tmp_path
    merged = output_root / "merged"
    images = output_root / "images"
    merged.mkdir()
    images.mkdir()
    for photo in ("000000.jpg", "000001.jpg"):
        (images / photo).write_bytes(b"")
        (images / f"{photo}.dat").write_bytes(b"")

    points = np.asarray(
        [(x, y) for y in range(3) for x in range(3) if (x, y) != (1, 1)],
        dtype=float,
    )
    reference = {
        "x": points[:, 0],
        "y": points[:, 1],
        "u": np.zeros(len(points)),
        "v": np.zeros(len(points)),
    }
    pd.DataFrame(
        {
            "x": points[:, 0],
            "y": points[:, 1],
            "u": points[:, 0] * 0.001,
            "v": points[:, 1] * 0.002,
        }
    ).to_csv(merged / "000001_DIC全场—力.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(
        [
            {"照片": "000000.jpg", "时间/s": 0.0, "X向力/N": 0.0, "Y向力/N": 0.0},
            {"照片": "000001.jpg", "时间/s": 0.1, "X向力/N": 10.0, "Y向力/N": 6.0},
        ]
    ).to_csv(output_root / "index.csv", index=False, encoding="cp936")

    monkeypatch.setattr(
        diagnostic, "_read_reference_frame", lambda _config, _merged: reference
    )
    read_paths = []
    read_frame = diagnostic._read_frame

    def track_merged_reads(path):
        read_paths.append(path.name)
        return read_frame(path)

    monkeypatch.setattr(diagnostic, "_read_frame", track_merged_reads)

    def fake_geometry(_job_path, repair_method=None):
        return {
            "length_x_mm": 1.0,
            "length_y_mm": 1.0,
            "area_mm2": 1.0,
            "roi_polygon_mm": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)],
            "dic_grid_spacing_mm": 1.0,
            "conversion_mm_per_pixel": 1.0,
            "subset_size_px": 1,
        }

    monkeypatch.setattr(diagnostic, "_geometry", fake_geometry)
    config = {
        "output_root": str(output_root),
        "experiment_id": "REFERENCE_REUSE_TEST",
        "merged_directory": "merged",
        "index_file": "index.csv",
        "image_folder": str(images),
        "job_file": str(output_root / "Job.m2inp"),
        "reference_photo": "000000.jpg",
        "reference_dat_file": str(images / "000000.jpg.dat"),
        "elastic_fit_photos": ["000001.jpg"],
        "machine_axes_in_dic": {
            "X": {"coordinate": "x", "displacement": "u", "force_column": "X向力/N"},
            "Y": {"coordinate": "y", "displacement": "v", "force_column": "Y向力/N"},
        },
        "poisson_ratio_fixed": 0.3,
        "thickness_mm": 1.0,
        "virtual_field_mode": "job_roi_boundary_adapted",
        "geometry_repair": "make_valid_linework",
        "output_directory": "diagnostic",
    }
    config_path = output_root / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    result = diagnostic.run(config_path)
    frame_work = pd.read_csv(
        output_root / "diagnostic" / "REFERENCE_REUSE_TEST" / "逐帧虚功诊断.csv",
        encoding="utf-8-sig",
    )

    assert result["帧数"] == 2
    assert frame_work["照片"].tolist() == ["000000.jpg", "000001.jpg"]
    assert read_paths == ["000001_DIC全场—力.csv"]


def test_diagnostic_and_report_use_adjacent_grid_support_inside_job_roi(
    tmp_path, monkeypatch
):
    output_root = tmp_path
    merged = output_root / "merged"
    images = output_root / "images"
    merged.mkdir()
    images.mkdir()
    (images / "000001.jpg").write_bytes(b"")
    (images / "000001.jpg.dat").write_bytes(b"")
    (images / "000002.jpg").write_bytes(b"")
    (images / "000002.jpg.dat").write_bytes(b"")
    points = np.asarray(
        [
            (x, y)
            for y in range(3)
            for x in range(3)
            if (x, y) != (1, 1)
        ],
        dtype=float,
    )
    reference = pd.DataFrame(
        {"x": points[:, 0], "y": points[:, 1], "u": 0.0, "v": 0.0}
    )
    current = pd.DataFrame(
        {
            "x": points[:, 0],
            "y": points[:, 1],
            "u": points[:, 0] * 0.001,
            "v": points[:, 1] * 0.002,
        }
    )
    reference.to_csv(
        merged / "000000_DIC全场—力.csv", index=False, encoding="utf-8-sig"
    )
    current.to_csv(
        merged / "000001_DIC全场—力.csv", index=False, encoding="utf-8-sig"
    )
    invalid_current = pd.DataFrame(
        {
            "x": points[:, 0],
            "y": points[:, 1],
            "u": -2.0 * points[:, 0],
            "v": points[:, 1] * 0.002,
        }
    )
    invalid_current.to_csv(
        merged / "000002_DIC全场—力.csv", index=False, encoding="utf-8-sig"
    )
    pd.DataFrame(
        [
            {"照片": "000001.jpg", "时间/s": 0.1, "X向力/N": 10.0, "Y向力/N": 6.0},
            {"照片": "000002.jpg", "时间/s": 0.2, "X向力/N": 12.0, "Y向力/N": 8.0},
        ]
    ).to_csv(output_root / "index.csv", index=False, encoding="cp936")
    config = {
        "output_root": str(output_root),
        "experiment_id": "GRID_HOLE_TEST",
        "merged_directory": "merged",
        "index_file": "index.csv",
        "image_folder": str(images),
        "job_file": str(output_root / "Job.m2inp"),
        "reference_photo": "000000.jpg",
        "elastic_fit_photos": ["000001.jpg"],
        "machine_axes_in_dic": {
            "X": {"coordinate": "x", "displacement": "u", "force_column": "X向力/N"},
            "Y": {"coordinate": "y", "displacement": "v", "force_column": "Y向力/N"},
        },
        "poisson_ratio_fixed": 0.3,
        "thickness_mm": 1.0,
        "virtual_field_mode": "job_roi_boundary_adapted",
        "geometry_repair": "make_valid_linework",
        "output_directory": "diagnostic_job_boundary",
    }
    config_path = output_root / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    captured_repair = {}

    def fake_geometry(_, repair_method=None):
        captured_repair["method"] = repair_method
        return {
            "length_x_mm": 1.0,
            "length_y_mm": 1.0,
            "area_mm2": 1.0,
            "roi_polygon_mm": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)],
            "dic_grid_spacing_mm": 1.0,
            "conversion_mm_per_pixel": 1.0,
            "subset_size_px": 1,
        }

    monkeypatch.setattr(diagnostic, "_geometry", fake_geometry)

    result = diagnostic.run(config_path)
    json.dumps(result, allow_nan=False)

    assert result["DIC网格规则"] == "Job Step size×Conversion 相邻格点三角剖分；缺失格点不跨越"
    assert result["三角形数"] == 4
    assert result["DIC三角网总面积_mm2"] == pytest.approx(2.0)
    assert result["DIC积分面积_mm2"] == pytest.approx(0.5)
    assert result["面积覆盖率"] == pytest.approx(0.5)
    assert result["虚功平衡状态"] == "BLOCKED_INCOMPLETE_DIC_SUPPORT"
    assert "不能与完整 ROI 机器合力宣称为平衡" in result["虚功平衡状态说明"]
    assert result["虚场模式"] == "job_roi_boundary_adapted"
    assert result["厚度_mm"] == pytest.approx(1.0)
    assert captured_repair["method"] == "make_valid_linework"
    output = output_root / "diagnostic_job_boundary" / "GRID_HOLE_TEST"
    frame_work = pd.read_csv(output / "逐帧虚功诊断.csv", encoding="utf-8-sig")
    assert len(frame_work) == 2
    assert frame_work["虚功物理有效"].tolist() == [True, False]
    assert pd.isna(frame_work.loc[1, "X内虚功/N"])
    assert pd.isna(frame_work.loc[1, "X外虚功/N"])
    assert pd.isna(frame_work.loc[1, "X残差/N"])
    assert frame_work.loc[1, "X向力/N"] == pytest.approx(12.0)
    assert np.isfinite(frame_work.loc[1, "X内虚功代数诊断/N"])
    assert np.isfinite(frame_work.loc[1, "X残差代数诊断/N"])
    assert result["域结果"][0]["有效帧数"] == 1
    assert result["域结果"][0]["无效帧数"] == 1
    report = (
        output / "诊断摘要.md"
    ).read_text(encoding="utf-8")
    assert "Job ROI 边界适配虚场" in report
    assert "交叠积分面积 0.500000 mm²；覆盖率 50.00%" in report
    assert "虚功平衡资格状态：BLOCKED_INCOMPLETE_DIC_SUPPORT" in report
    assert "DIC网格：Job Step size×Conversion 相邻格点三角剖分；缺失格点不跨越" in report
    assert "det(F)≤0 的帧保留在逐帧 CSV 中" in report
    assert "本次分析厚度：1.000 mm" in report
