import math
import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from matplotlib.tri import Triangulation
import numpy as np

from tools.run_pa12_self_vfm import (
    _align_frame_arrays,
    _align_frame_points,
    _geometry,
    _effective_dicom_geometry,
    _geometry_quality,
    _machine_axis_strain_arrays,
    _experiment_axis_mapping,
    _read_frame_points,
    _usable_modulus,
    process_experiment,
)

from tools.pa12_self_vfm import (
    equivalent_plastic_strain_plane_stress,
    equivalent_stress_plane_stress,
    fit_elastic_modulus,
    fit_hardening_models,
    fit_linear_hardening,
    hardening_model_value,
    integrate_plane_stress_virtual_work_coefficients,
    plane_stress_virtual_work_coefficients,
    rotated_machine_axes,
)


class Pa12SelfVfmTests(unittest.TestCase):
    def test_pointwise_coefficients_use_rotated_machine_axis_strains(self):
        points = {
            "x": np.array([0.0, 2.0, 2.0, 0.0]),
            "y": np.array([0.0, 0.0, 1.0, 1.0]),
            "exx": np.full(4, 0.01),
            "eyy": np.full(4, 0.03),
        }

        result = integrate_plane_stress_virtual_work_coefficients(
            points=_machine_axis_strain_arrays(points),
            nu=0.25,
            thickness_mm=1.0,
            length_x_mm=1.0,
            length_y_mm=2.0,
            roi_bounds=(0.0, 2.0, 0.0, 1.0),
        )

        expected_machine_x = 2.0 * (0.03 + 0.25 * 0.01) / (1.0 - 0.25**2)
        expected_machine_y = 2.0 * (0.01 + 0.25 * 0.03) / (2.0 * (1.0 - 0.25**2))
        self.assertAlmostEqual(result["coefficient_x"], expected_machine_x)
        self.assertAlmostEqual(result["coefficient_y"], expected_machine_y)

    def test_effective_dicom_geometry_uses_point_bbox_without_changing_job_geometry(self):
        job_geometry = {
            "roi_bounds_mm": (0.0, 0.0, 10.0, 10.0),
            "area_mm2": 100.0,
            "length_x_mm": 10.0,
            "length_y_mm": 10.0,
        }
        effective = _effective_dicom_geometry(
            [{"x": 2.0, "y": 3.0}, {"x": 8.0, "y": 9.0}],
            job_geometry,
        )
        self.assertEqual(effective["roi_bounds_mm"], (2.0, 8.0, 3.0, 9.0))
        self.assertAlmostEqual(effective["area_mm2"], 36.0)
        self.assertEqual(job_geometry["area_mm2"], 100.0)
        self.assertTrue(effective["roi_is_axis_aligned_rectangle"])
    def test_nonpositive_elastic_fit_is_not_used_for_plastic_strain(self):
        self.assertIsNone(_usable_modulus({"modulus_mpa": -12.0}))
        self.assertIsNone(_usable_modulus({"modulus_mpa": 0.0}))
        self.assertAlmostEqual(_usable_modulus({"modulus_mpa": 1200.0}), 1200.0)

    def test_single_axis_geometry_gate_stays_in_review(self):
        quality = _geometry_quality(
            "单轴 X",
            {"area_mm2": 10.0, "bounding_area_mm2": 12.0},
            {"single_axis_geometry_gate": {"reason": "独立几何证据未完成"}},
        )

        self.assertEqual(quality["status"], "REVIEW_REQUIRED")
        self.assertEqual(quality["reason"], "独立几何证据未完成")

    def test_geometry_preserves_polygon_area_and_vertices(self):
        with TemporaryDirectory() as directory:
            job_path = Path(directory) / "Job.m2inp"
            job_path.write_text(
                "<Conversion>=<1>\n"
                "<Reference$image>=<000000.jpg>\n"
                "<Shape>=<2;0;False;4;0;0;2;0;1;1;0;1>\n",
                encoding="utf-8",
            )

            geometry = _geometry(job_path)

        self.assertAlmostEqual(geometry["area_mm2"], 1.5)
        self.assertAlmostEqual(geometry["bounding_area_mm2"], 2.0)
        self.assertEqual(len(geometry["roi_polygon_mm"]), 4)
        self.assertFalse(geometry["roi_is_axis_aligned_rectangle"])

    def test_geometry_recognizes_axis_aligned_rectangle(self):
        with TemporaryDirectory() as directory:
            job_path = Path(directory) / "Job.m2inp"
            job_path.write_text(
                "<Conversion>=<1>\n"
                "<Reference$image>=<000000.jpg>\n"
                "<Shape>=<2;0;False;4;0;0;2;0;2;1;0;1>\n",
                encoding="utf-8",
            )

            geometry = _geometry(job_path)

        self.assertTrue(geometry["roi_is_axis_aligned_rectangle"])

    def test_frame_points_are_read_with_coordinates_and_strains(self):
        from io import StringIO

        points = _read_frame_points(
            StringIO("x,y,exx,eyy,exy\n0,1,0.1,0.2,0.3\n")
        )

        self.assertEqual(points, [{"x": 0.0, "y": 1.0, "exx": 0.1, "eyy": 0.2, "exy": 0.3}])

    def test_frame_points_require_coordinate_alignment(self):
        reference = [{"x": 0.0, "y": 0.0, "exx": 0.1, "eyy": 0.2, "exy": 0.0}]
        current = [{"x": 0.1, "y": 0.0, "exx": 0.2, "eyy": 0.3, "exy": 0.0}]

        with self.assertRaises(ValueError):
            _align_frame_points(reference, current)

    def test_frame_arrays_subtract_reference_field_only_after_coordinate_check(self):
        reference = {
            "x": np.array([0.0, 1.0, 0.0]),
            "y": np.array([0.0, 0.0, 1.0]),
            "exx": np.array([0.1, 0.2, 0.3]),
            "eyy": np.array([0.2, 0.3, 0.4]),
            "exy": np.array([0.0, 0.0, 0.0]),
        }
        current = {key: value.copy() for key, value in reference.items()}
        current["exx"] += 0.01
        aligned = _align_frame_arrays(reference, current)
        np.testing.assert_allclose(aligned["exx"], [0.01, 0.01, 0.01])
        self.assertEqual(int(aligned["matched_point_count"][0]), 3)
        current["x"][0] = 0.1
        with self.assertRaises(ValueError):
            _align_frame_arrays(reference, current)

    def test_frame_arrays_join_coordinate_set_when_point_order_changes(self):
        reference = {
            "x": np.array([0.0, 1.0, 2.0, 3.0]),
            "y": np.array([0.0, 0.0, 0.0, 0.0]),
            "exx": np.array([0.1, 0.2, 0.3, 0.4]),
            "eyy": np.array([0.0, 0.0, 0.0, 0.0]),
            "exy": np.array([0.0, 0.0, 0.0, 0.0]),
        }
        current = {
            "x": np.array([2.0, 0.0, 1.0]),
            "y": np.array([0.0, 0.0, 0.0]),
            "exx": np.array([0.35, 0.11, 0.25]),
            "eyy": np.array([0.0, 0.0, 0.0]),
            "exy": np.array([0.0, 0.0, 0.0]),
        }
        aligned = _align_frame_arrays(reference, current)
        self.assertEqual(int(aligned["matched_point_count"][0]), 3)
        self.assertEqual(int(aligned["reference_missing_point_count"][0]), 1)
        self.assertEqual(int(aligned["current_extra_point_count"][0]), 0)
        np.testing.assert_allclose(aligned["exx"], [0.01, 0.05, 0.05])

    def test_pointwise_virtual_work_integrates_constant_field_over_two_triangles(self):
        points = [
            {"x": 0.0, "y": 0.0, "exx": 0.01, "eyy": 0.02},
            {"x": 2.0, "y": 0.0, "exx": 0.01, "eyy": 0.02},
            {"x": 2.0, "y": 1.0, "exx": 0.01, "eyy": 0.02},
            {"x": 0.0, "y": 1.0, "exx": 0.01, "eyy": 0.02},
        ]

        result = integrate_plane_stress_virtual_work_coefficients(
            points=points,
            nu=0.25,
            thickness_mm=1.0,
            length_x_mm=2.0,
            length_y_mm=1.0,
            roi_bounds=(0.0, 2.0, 0.0, 1.0),
        )

        expected_x = 1.0 / (1.0 - 0.25**2) * (0.01 + 0.25 * 0.02)
        expected_y = 2.0 / (1.0 - 0.25**2) * (0.02 + 0.25 * 0.01)
        self.assertAlmostEqual(result["integrated_area_mm2"], 2.0)
        self.assertAlmostEqual(result["coefficient_x"], expected_x)
        self.assertAlmostEqual(result["coefficient_y"], expected_y)
        self.assertEqual(result["valid_triangle_count"], 2)

    def test_numpy_grid_uses_pointwise_triangle_integration(self):
        grid_x, grid_y = np.meshgrid(
            np.array([0.0, 0.5, 1.0]),
            np.array([0.0, 0.5, 1.0]),
        )
        points = {
            "x": grid_x.ravel(),
            "y": grid_y.ravel(),
            "exx": np.full(9, 0.01),
            "eyy": np.full(9, 0.02),
        }

        result = integrate_plane_stress_virtual_work_coefficients(
            points=points,
            nu=0.25,
            thickness_mm=1.0,
            length_x_mm=1.0,
            length_y_mm=1.0,
            roi_bounds=(0.0, 1.0, 0.0, 1.0),
        )

        self.assertEqual(result["integration_method"], "pointwise_triangle")
        self.assertEqual(result["valid_triangle_count"], 8)
        self.assertAlmostEqual(result["integrated_area_mm2"], 1.0)

    def test_pointwise_virtual_work_excludes_points_outside_roi(self):
        points = [
            {"x": 0.0, "y": 0.0, "exx": 0.01, "eyy": 0.02},
            {"x": 2.0, "y": 0.0, "exx": 0.01, "eyy": 0.02},
            {"x": 2.0, "y": 1.0, "exx": 0.01, "eyy": 0.02},
            {"x": 0.0, "y": 1.0, "exx": 0.01, "eyy": 0.02},
            {"x": 3.0, "y": 3.0, "exx": 100.0, "eyy": 100.0},
        ]

        result = integrate_plane_stress_virtual_work_coefficients(
            points=points,
            nu=0.25,
            thickness_mm=1.0,
            length_x_mm=2.0,
            length_y_mm=1.0,
            roi_bounds=(0.0, 2.0, 0.0, 1.0),
        )

        self.assertAlmostEqual(result["integrated_area_mm2"], 2.0)
        self.assertEqual(result["excluded_point_count"], 1)

    def test_polygon_roi_uses_polygon_area_instead_of_bounding_rectangle(self):
        points = [
            {"x": 0.0, "y": 0.0, "exx": 0.01, "eyy": 0.02},
            {"x": 2.0, "y": 0.0, "exx": 0.01, "eyy": 0.02},
            {"x": 1.0, "y": 1.0, "exx": 0.01, "eyy": 0.02},
            {"x": 0.0, "y": 1.0, "exx": 0.01, "eyy": 0.02},
            {"x": 2.0, "y": 1.0, "exx": 100.0, "eyy": 100.0},
        ]

        result = integrate_plane_stress_virtual_work_coefficients(
            points=points,
            nu=0.25,
            thickness_mm=1.0,
            length_x_mm=2.0,
            length_y_mm=1.0,
            roi_bounds=(0.0, 2.0, 0.0, 1.0),
            roi_polygon=[(0.0, 0.0), (2.0, 0.0), (1.0, 1.0), (0.0, 1.0)],
        )

        self.assertAlmostEqual(result["integrated_area_mm2"], 1.5)
        self.assertAlmostEqual(result["roi_area_mm2"], 1.5)
        self.assertAlmostEqual(result["area_ratio"], 1.0)
        self.assertEqual(result["excluded_point_count"], 1)

    def test_pointwise_virtual_work_reuses_reference_triangulation(self):
        points = [
            {"x": 0.0, "y": 0.0, "exx": 0.01, "eyy": 0.02},
            {"x": 2.0, "y": 0.0, "exx": 0.01, "eyy": 0.02},
            {"x": 2.0, "y": 1.0, "exx": 0.01, "eyy": 0.02},
            {"x": 0.0, "y": 1.0, "exx": 0.01, "eyy": 0.02},
        ]
        triangulation = Triangulation(
            [point["x"] for point in points],
            [point["y"] for point in points],
        )
        result = integrate_plane_stress_virtual_work_coefficients(
            points=points,
            nu=0.25,
            thickness_mm=1.0,
            length_x_mm=2.0,
            length_y_mm=1.0,
            roi_bounds=(0.0, 2.0, 0.0, 1.0),
            triangulation=triangulation,
        )
        self.assertAlmostEqual(result["integrated_area_mm2"], 2.0)
        self.assertEqual(result["valid_triangle_count"], 2)

        moved = [dict(point, x=point["x"] + 0.1) for point in points]
        with self.assertRaises(ValueError):
            integrate_plane_stress_virtual_work_coefficients(
                points=moved,
                nu=0.25,
                thickness_mm=1.0,
                length_x_mm=2.0,
                length_y_mm=1.0,
                roi_bounds=(0.0, 2.0, 0.0, 1.0),
                triangulation=triangulation,
            )
    def test_constant_virtual_field_coefficients_are_dimensionally_consistent(self):
        bx, by = plane_stress_virtual_work_coefficients(
            exx=0.01,
            eyy=0.005,
            nu=0.25,
            area_mm2=100.0,
            thickness_mm=1.0,
            length_x_mm=10.0,
            length_y_mm=20.0,
        )

        self.assertAlmostEqual(bx, 0.12)
        self.assertAlmostEqual(by, 0.04)

    def test_elastic_modulus_is_identified_by_zero_intercept_virtual_work_fit(self):
        modulus = fit_elastic_modulus(
            coefficients=[0.1, 0.2, 0.4],
            external_forces=[20.0, 40.0, 80.0],
        )

        self.assertAlmostEqual(modulus["modulus_mpa"], 200.0)
        self.assertAlmostEqual(modulus["rmse_n"], 0.0)
        self.assertEqual(modulus["point_count"], 3)

    def test_plane_stress_equivalent_stress_uses_zero_shear_when_omitted(self):
        self.assertAlmostEqual(
            equivalent_stress_plane_stress(10.0, 4.0),
            math.sqrt(10.0**2 - 10.0 * 4.0 + 4.0**2),
        )

    def test_rotated_machine_mapping_matches_calibrated_boundaries(self):
        mapping = rotated_machine_axes(
            exx=0.02,
            eyy=0.03,
            length_x_mm=10.0,
            length_y_mm=20.0,
        )

        self.assertEqual(mapping["machine_x_strain"], 0.03)
        self.assertEqual(mapping["machine_y_strain"], 0.02)
        self.assertEqual(mapping["machine_x_virtual_length_mm"], 20.0)
        self.assertEqual(mapping["machine_y_edge_length_mm"], 20.0)

    def test_machine_axis_mapping_can_follow_vertical_single_axis_specimen(self):
        mapping = rotated_machine_axes(
            exx=0.02,
            eyy=0.03,
            length_x_mm=10.0,
            length_y_mm=20.0,
            machine_x_dic_axis="x",
            machine_y_dic_axis="y",
        )

        self.assertEqual(mapping["machine_x_strain"], 0.02)
        self.assertEqual(mapping["machine_y_strain"], 0.03)
        self.assertEqual(mapping["machine_x_virtual_length_mm"], 10.0)
        self.assertEqual(mapping["machine_x_edge_length_mm"], 20.0)
        self.assertEqual(mapping["machine_y_virtual_length_mm"], 20.0)
        self.assertEqual(mapping["machine_y_edge_length_mm"], 10.0)

    def test_machine_axis_strain_arrays_accepts_explicit_single_axis_mapping(self):
        points = {
            "x": np.array([0.0]),
            "y": np.array([0.0]),
            "exx": np.array([0.02]),
            "eyy": np.array([0.03]),
            "exy": np.array([0.0]),
        }

        mapped = _machine_axis_strain_arrays(
            points,
            machine_x_dic_axis="x",
            machine_y_dic_axis="y",
        )

        np.testing.assert_allclose(mapped["exx"], [0.02])
        np.testing.assert_allclose(mapped["eyy"], [0.03])

    def test_s22_experiment_mapping_is_explicit_and_remains_unverified(self):
        config = {
            "machine_axis_mapping_by_experiment": {
                "S22_Y_0.2": {
                    "machine_x_dic_axis": "x",
                    "machine_y_dic_axis": "y",
                    "status": "IMAGE_SUPPORTED_NEEDS_COORDINATE_CONFIRMATION",
                }
            }
        }

        mapping = _experiment_axis_mapping(
            {"experiment_id": "S22_Y_0.2", "loading_mode": "单轴 Y"},
            config,
        )

        self.assertEqual(mapping, {"machine_x_dic_axis": "x", "machine_y_dic_axis": "y"})

    def test_stage2_uses_configured_axis_for_plastic_strain_and_virtual_work(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            experiment_id = "S22_Y_0.2"
            preparation_dir = root / "Agents" / "PA12实验数据处理" / "MatchID_VFM准备" / experiment_id
            merged_dir = preparation_dir / "merged"
            merged_dir.mkdir(parents=True)
            index_path = preparation_dir / f"{experiment_id}_DIC全场—力索引.csv"
            axial_strains = [0.0, 0.001, 0.002, 0.004, 0.006, 0.008, 0.010, 0.012]
            force_y = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0]
            with index_path.open("w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.DictWriter(handle, fieldnames=["照片", "时间/s", "X向力/N", "Y向力/N"])
                writer.writeheader()
                for index, force in enumerate(force_y):
                    writer.writerow({"照片": f"{index:06d}.jpg", "时间/s": index, "X向力/N": 0.0, "Y向力/N": force})
                    with (merged_dir / f"{index:06d}_DIC全场—力.csv").open(
                        "w", newline="", encoding="utf-8-sig"
                    ) as frame_handle:
                        frame_writer = csv.DictWriter(frame_handle, fieldnames=["x", "y", "exx", "eyy", "exy"])
                        frame_writer.writeheader()
                        for x, y in ((0.0, 0.0), (10.0, 0.0), (10.0, 20.0), (0.0, 20.0)):
                            frame_writer.writerow(
                                {"x": x, "y": y, "exx": 0.0, "eyy": axial_strains[index], "exy": 0.0}
                            )

            config_path = Path(__file__).resolve().parents[1] / "configs" / "pa12_self_vfm.json"
            self_config = json.loads(config_path.read_text(encoding="utf-8"))
            self_config["eligible_loading_modes"] = ["单轴 Y"]
            self_config["machine_axis_mapping_by_experiment"] = {
                experiment_id: {"machine_x_dic_axis": "x", "machine_y_dic_axis": "y"}
            }
            self_config["nu"] = 0.0
            self_config["elastic_strain_limit"] = 0.0025
            self_config["minimum_plastic_strain"] = 0.001
            self_config["minimum_hardening_points"] = 5
            self_config["stage2_acceptance"]["minimum_points"] = 5
            geometry = {
                "roi_bounds_mm": (0.0, 10.0, 0.0, 20.0),
                "roi_polygon_mm": [(0.0, 0.0), (10.0, 0.0), (10.0, 20.0), (0.0, 20.0)],
                "roi_is_axis_aligned_rectangle": True,
                "area_mm2": 200.0,
                "bounding_area_mm2": 200.0,
                "length_x_mm": 10.0,
                "length_y_mm": 20.0,
            }
            result_directory = root / "result"
            with patch("tools.run_pa12_self_vfm._plot_experiment"):
                process_experiment(
                    {"experiment_id": experiment_id, "loading_mode": "单轴 Y", "formal_vfm_allowed": True},
                    {"output_root": str(root)},
                    self_config,
                    geometry_override=geometry,
                    result_directory=result_directory,
                )

            result = json.loads((result_directory / f"{experiment_id}_结果.json").read_text(encoding="utf-8"))
            self.assertAlmostEqual(result["阶段1"]["E_MPa"], 1000.0, places=8)
            with (result_directory / f"{experiment_id}_内外虚功.csv").open(encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))
            row = next(item for item in rows if item["照片"] == "000003.jpg")
            expected_plastic = equivalent_plastic_strain_plane_stress(
                exx=0.0,
                eyy=0.004,
                exy=0.0,
                sigma_x_mpa=0.0,
                sigma_y_mpa=3.0,
                modulus_mpa=1000.0,
                nu=0.0,
            )
            self.assertAlmostEqual(float(row["等效塑性应变"]), expected_plastic, places=9)
            expected_internal_y = float(row["阶段2模型等效应力/MPa"]) * 200.0 / 20.0
            self.assertAlmostEqual(float(row["阶段2内部虚功Y/N"]), expected_internal_y, places=7)

    def test_plastic_strain_subtracts_plane_stress_elastic_part(self):
        e_xx = (10.0 - 0.25 * 4.0) / 1000.0 + 0.01
        e_yy = (4.0 - 0.25 * 10.0) / 1000.0 - 0.005
        equivalent = equivalent_plastic_strain_plane_stress(
            exx=e_xx,
            eyy=e_yy,
            exy=0.0,
            sigma_x_mpa=10.0,
            sigma_y_mpa=4.0,
            modulus_mpa=1000.0,
            nu=0.25,
        )

        expected = math.sqrt((2.0 / 3.0) * (0.01**2 + (-0.005) ** 2 + (-0.005) ** 2))
        self.assertAlmostEqual(equivalent, expected)

    def test_linear_hardening_fit_returns_yield_and_slope(self):
        result = fit_linear_hardening(
            plastic_strains=[0.01, 0.02, 0.04],
            equivalent_stresses=[25.0, 30.0, 40.0],
        )

        self.assertAlmostEqual(result["yield_mpa"], 20.0)
        self.assertAlmostEqual(result["hardening_mpa"], 500.0)
        self.assertAlmostEqual(result["rmse_mpa"], 0.0)
        self.assertEqual(result["point_count"], 3)

    def test_generic_model_comparison_exposes_explicit_model_names(self):
        self.assertAlmostEqual(
            hardening_model_value(
                "Voce I（通用）",
                0.1,
                {"Y": 20.0, "Q": 40.0, "b": 5.0},
            ),
            20.0 + 40.0 * (1.0 - math.exp(-0.5)),
        )
        results = fit_hardening_models(
            plastic_strains=[0.01, 0.02, 0.04, 0.06],
            equivalent_stresses=[25.0, 30.0, 40.0, 50.0],
        )
        self.assertEqual(
            [row["model"] for row in results],
            ["Linear", "Ludwik", "Swift", "Voce I（通用）", "Voce II（通用）"],
        )
        self.assertTrue(all(row["point_count"] == 4 for row in results))


if __name__ == "__main__":
    unittest.main()
