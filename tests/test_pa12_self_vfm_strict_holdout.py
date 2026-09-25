import unittest

from tools.audit_pa12_self_vfm_strict_holdout import _hardening_indices, _holdout_status, _machine_axis_strains


class StrictHoldoutTests(unittest.TestCase):
    def test_machine_axis_strains_follow_experiment_dic_mapping(self):
        row = {"平均exx": "0.01", "平均eyy": "0.03"}

        self.assertEqual(
            _machine_axis_strains(row, {"machine_x_dic_axis": "x", "machine_y_dic_axis": "y"}),
            (0.01, 0.03),
        )
        self.assertEqual(
            _machine_axis_strains(row, {"machine_x_dic_axis": "y", "machine_y_dic_axis": "x"}),
            (0.03, 0.01),
        )

    def test_stage_two_candidates_match_runner_peak_and_threshold_rules(self):
        rows = [
            {"等效应力/MPa": "0.1"},
            {"等效应力/MPa": "4.0"},
            {"等效应力/MPa": "10.0"},
            {"等效应力/MPa": "8.0"},
        ]
        plastic_strains = [0.002, 0.0005, 0.002, 0.002]
        config = {"minimum_force_n": 5.0, "minimum_plastic_strain": 0.001}

        self.assertEqual(_hardening_indices(rows, plastic_strains, config, (10.0, 20.0)), [2])

    def test_single_test_point_is_not_a_holdout_validation_pass(self):
        self.assertEqual(_holdout_status(1, 20), "INSUFFICIENT_TEST_POINTS")
        self.assertEqual(_holdout_status(20, 20), "PASS")


if __name__ == "__main__":
    unittest.main()
