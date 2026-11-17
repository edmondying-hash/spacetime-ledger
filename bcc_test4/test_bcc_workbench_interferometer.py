#!/usr/bin/env python3
"""Unit tests for the BCC Workbench Torsion + 976 nm Laser Interferometer module."""

import unittest
from bcc_workbench_interferometer import BCCWorkbenchInterferometerSim


class TestBCCWorkbenchInterferometer(unittest.TestCase):
    def test_open_exhaust_produces_measurable_interferometer_fringes(self):
        sim = BCCWorkbenchInterferometerSim(laser_optical_watts=5.0)
        res = sim.run_workbench_trial(open_exhaust=True, wall_distance_m=4.0)
        self.assertGreater(res["thrust_nn"], 16.0)
        self.assertGreater(res["interferometer_fringes"], 1.0)
        self.assertGreater(res["wall_spot_shift_mm"], 1.0)
        self.assertTrue(res["below_mirror_damage"])

    def test_closed_absorber_yields_exact_zero_deflection(self):
        sim = BCCWorkbenchInterferometerSim(laser_optical_watts=5.0)
        null_res = sim.run_workbench_trial(open_exhaust=False)
        self.assertEqual(null_res["thrust_nn"], 0.0)
        self.assertEqual(null_res["interferometer_fringes"], 0.0)
        self.assertEqual(null_res["wall_spot_shift_mm"], 0.0)

    def test_workbench_intensity_stays_orders_of_magnitude_below_planck_saturation(self):
        sim = BCCWorkbenchInterferometerSim(laser_optical_watts=5.0)
        res = sim.run_workbench_trial(open_exhaust=True)
        self.assertLess(res["planck_congestion_ratio"], 1e-100)


if __name__ == "__main__":
    unittest.main()
