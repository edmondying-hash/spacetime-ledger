#!/usr/bin/env python3
"""Unit tests for emergent Special Relativity on the 6-face Planck-cube grid."""

import unittest
from bcc_sr_emergence import BCCSREmergenceSim


class TestBCCSREmergence(unittest.TestCase):
    def test_time_dilation_and_length_contraction_at_point_eight_c(self):
        """At beta = 0.8c, gamma = 5/3 = 1.666667, clock rate = 0.6, and L = 6.0 l_P."""
        sim = BCCSREmergenceSim(c_grid=1.0)
        rows = {r["beta"]: r for r in sim.kinematics_profile([0.0, 0.8], rest_length_lp=10.0)}
        at_rest = rows.get(0.0)
        moving = rows.get(0.8)
        self.assertEqual(at_rest["gamma"], 1.0)
        self.assertAlmostEqual(moving["gamma"], 5.0 / 3.0, places=6)
        self.assertAlmostEqual(moving["clock_rate"], 0.6, places=6)
        self.assertAlmostEqual(moving["contracted_length"], 6.0, places=4)

    def test_energy_momentum_dispersion_relation_exact(self):
        """Orthogonal rest-mass and momentum ticks satisfy E = gamma*m0 = sqrt((pc)^2 + m0^2)."""
        sim = BCCSREmergenceSim(rest_mass_mev=938.92)
        for row in sim.energy_momentum_table([0.0, 0.5, 0.9, 0.99]):
            self.assertLess(row["residual_mev"], 1e-8)

    def test_velocity_addition_caps_at_c_and_preserves_photon_speed(self):
        """Composing 0.8c + 0.8c gives 0.975610c < c, and photon speed c + 0.8c stays 1.0c."""
        sim = BCCSREmergenceSim()
        sub = sim.compose_velocities(0.8, 0.8)
        photon = sim.compose_velocities(1.0, 0.8)
        self.assertAlmostEqual(sub["grid_relativistic"], 40.0 / 41.0, places=6)
        self.assertTrue(sub["respects_c_cap"])
        self.assertEqual(photon["grid_relativistic"], 1.0)


if __name__ == "__main__":
    unittest.main()
