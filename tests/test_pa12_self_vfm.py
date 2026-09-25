import math
import unittest

from tools.run_pa12_self_vfm import _align_frame_points, _read_frame_points

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
