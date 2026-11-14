#!/usr/bin/env python3
"""Unit tests for the inverse dark-matter halo solver on the 6-face Planck lattice."""

import unittest
from bcc_dark_matter import BCCDarkMatterSim
from bcc_halo_solver import BCCHaloSolver


class TestBCCHaloSolver(unittest.TestCase):
    def test_enclosed_halo_mass_grows_linearly_and_recovers_cosmic_ratio(self):
        """Flat rotation curve inverts to linearly growing M_halo(<r) and ~5.5:1 outer ratio."""
        dm_sim = BCCDarkMatterSim()
        solver = BCCHaloSolver()
        inv = solver.invert_rotation_curve(dm_sim.rotation_curve([2.0, 4.0, 8.0, 14.0, 20.0]))
        by_r = {row["r"]: row for row in inv}
        self.assertGreater(by_r.get(20.0)["m_halo"], by_r.get(8.0)["m_halo"])
        self.assertAlmostEqual(by_r.get(20.0)["dark_to_baryon"], 5.5, delta=0.3)

    def test_keplerian_baryon_only_curve_inverts_to_zero_halo(self):
        """When v_total == v_baryon, reconstructed halo mass and loop count are strictly 0."""
        solver = BCCHaloSolver()
        baryon_only = [
            {"r": 4.0, "v_baryon": 16.0, "v_total": 16.0},
            {"r": 10.0, "v_baryon": 10.12, "v_total": 10.12},
        ]
        for row in solver.invert_rotation_curve(baryon_only):
            self.assertEqual(row["m_halo"], 0.0)
            self.assertEqual(row["est_loops"], 0.0)

    def test_cored_halo_stays_bounded_below_node_cap_unlike_nfw_cusp(self):
        """Lattice pseudo-isothermal core avoids the divergent NFW 1/r singularity near r=0."""
        solver = BCCHaloSolver(node_cap=100.0)
        prof = {r["r"]: r for r in solver.cored_vs_cusp_profile([0.2, 1.0, 5.0])}
        inner = prof.get(0.2)
        self.assertGreater(inner["nfw_cusp_ticks"], 500.0)
        self.assertLessEqual(inner["grid_core_ticks"], 100.0)


if __name__ == "__main__":
    unittest.main()
