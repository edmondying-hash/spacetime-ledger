#!/usr/bin/env python3
"""Unit tests for the 6-face Planck-cube unified baryon, glueball, lensing, and horizon sim."""

import unittest
from bcc_unified_sim import (
    BCCUnifiedGridSim,
    FACES_6,
    face_distance,
    steiner_3q_links,
)


class BCCUnifiedTests(unittest.TestCase):
    def test_6face_distance_and_steiner_links(self):
        """6-face stencil has 6 orthogonal neighbors and exact 3D Manhattan Steiner links."""
        self.assertEqual(len(FACES_6), 6)
        self.assertEqual(face_distance((1, 1, 1), (3, 2, 1), size=8), 3)
        self.assertEqual(steiner_3q_links((1, 1, 1), (3, 1, 1), (1, 4, 1), size=8), 5)

    def test_strange_quark_redraw_lag_and_mass_ordering(self):
        """Strange quarks redraw slower and increase baryon mass ordering N < Lambda < Xi < Omega."""
        sim = BCCUnifiedGridSim(size=8)
        n_res = sim.simulate_baryon_family(("u", "u", "d"), -1.0, cycles=2000, seed=10)
        l_res = sim.simulate_baryon_family(("u", "d", "s"), -1.0, cycles=2000, seed=11)
        x_res = sim.simulate_baryon_family(("u", "s", "s"), -0.66, cycles=2000, seed=12)
        o_res = sim.simulate_baryon_family(("s", "s", "s"), 0.34, cycles=2000, seed=13)

        self.assertGreater(n_res["Redraw/c"], l_res["Redraw/c"])
        self.assertGreater(l_res["Redraw/c"], o_res["Redraw/c"])
        self.assertLess(n_res["GridMass"], l_res["GridMass"])
        self.assertLess(l_res["GridMass"], x_res["GridMass"])
        self.assertLess(x_res["GridMass"], o_res["GridMass"])

    def test_pure_gluon_glueball_mass_gap(self):
        """Closed 4-link gluon loop generates a positive mass gap above the 0 MeV vacuum."""
        sim = BCCUnifiedGridSim(size=8)
        vac = sim.simulate_glueball(0)
        gb4 = sim.simulate_glueball(4)
        self.assertEqual(vac["glueball_mass_mev"], 0.0)
        self.assertGreater(gb4["glueball_mass_mev"], 1500.0)

    def test_congestion_lensing_lag(self):
        """Wavefront rows passing through the core experience higher lag than distant rows."""
        sim = BCCUnifiedGridSim(size=8)
        rows = sim.simulate_wavefront_lensing()
        core_row = next(r for r in rows if r["dist"] == 0)
        edge_row = next(r for r in rows if r["dist"] == 8)
        self.assertGreater(core_row["lag"], edge_row["lag"])
        self.assertEqual(edge_row["lag"], 0)

    def test_2d_core_3d_shell_strict_lock(self):
        """2D saturated core expands into a 3D boundary shell with zero escaped packets."""
        sim = BCCUnifiedGridSim(size=8)
        res = sim.simulate_2d_to_3d_deadlock(packets=220)
        self.assertGreater(res["deadlocked_nodes"], res["initial_core"])
        self.assertEqual(res["escaped_packets"], 0)


if __name__ == "__main__":
    unittest.main()

