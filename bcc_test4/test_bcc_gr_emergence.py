#!/usr/bin/env python3
"""Unit tests for emergent weak-field General Relativity on the 6-face Planck lattice."""

import unittest
from bcc_gr_emergence import BCCGREmergenceSim


class TestBCCGREmergence(unittest.TestCase):
    def test_time_dilation_matches_schwarzschild_and_locks_at_horizon(self):
        """Clock rate sqrt(1 - W(r)/C_cap) matches Schwarzschild g_00 and hits 0 at r = r_s."""
        sim = BCCGREmergenceSim(node_cap=100.0, r_s=3.0)
        rows = {r["r"]: r for r in sim.time_dilation_profile([3.0, 6.0, 12.0])}
        self.assertEqual(rows.get(3.0)["grid_dtau_dt"], 0.0)
        self.assertAlmostEqual(rows.get(6.0)["grid_dtau_dt"], rows.get(6.0)["gr_dtau_dt"], places=6)
        self.assertAlmostEqual(rows.get(12.0)["grid_dtau_dt"], rows.get(12.0)["gr_dtau_dt"], places=6)

    def test_light_deflection_recovers_exact_2x_einstein_factor(self):
        """Temporal queue wait (g_00) + spatial orthogonal detour (g_rr) gives 2.0x Newton."""
        sim = BCCGREmergenceSim(node_cap=100.0, r_s=3.0)
        rows = sim.light_deflection_2x_test([6.0, 15.0, 25.0])
        for row in rows:
            self.assertAlmostEqual(row["ratio_to_newton"], 2.0, places=4)
            self.assertAlmostEqual(row["grid_rad"], row["einstein_rad"], places=6)

    def test_perihelion_precession_matches_einstein_formula(self):
        """Post-Newtonian 1/r^3 congestion shift matches 3*pi*r_s / (a*(1-e^2)) within 1%."""
        sim = BCCGREmergenceSim(node_cap=100.0, r_s=3.0)
        res = sim.perihelion_precession(semi_major_a=1200.0, eccentricity=0.5)
        self.assertLess(res["rel_error_pct"], 1.0)


if __name__ == "__main__":
    unittest.main()
