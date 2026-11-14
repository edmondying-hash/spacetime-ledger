#!/usr/bin/env python3
"""Unit tests for converging starlight black holes, recoil conservation, and frame-dragging."""

import unittest
from bcc_kugelblitz_spin import BCCKugelblitzSpinSim


class TestBCCKugelblitzSpin(unittest.TestCase):
    def test_converging_light_web_deadlocks_above_100_tick_cap(self):
        """Sparse star ring stays transparent (W < 100), dense ring deadlocks into a BH."""
        sim = BCCKugelblitzSpinSim(node_cap=100.0)
        sparse = sim.simulate_star_ring(num_stars=12, ray_ticks=3.0, asymmetry_bias=0.0)
        dense = sim.simulate_star_ring(num_stars=24, ray_ticks=5.0, asymmetry_bias=0.0)
        self.assertFalse(sparse["deadlocked_bh"])
        self.assertTrue(dense["deadlocked_bh"])
        self.assertGreaterEqual(dense["central_workload"], 100.0)

    def test_symmetric_ring_produces_zero_net_rotation(self):
        """Mirror-symmetric star distribution cancels radial momentum with zero net spin."""
        sim = BCCKugelblitzSpinSim()
        sym = sim.simulate_star_ring(num_stars=24, ray_ticks=5.0, asymmetry_bias=0.0)
        self.assertAlmostEqual(sym["net_lz"], 0.0, places=6)
        self.assertEqual(sym["frame_drag_omega"], 0.0)

    def test_opposite_ring_asymmetries_drive_opposite_galactic_spin(self):
        """Positive vs. negative ring asymmetry induces CCW vs. CW frame-dragging spin."""
        sim = BCCKugelblitzSpinSim()
        ccw = sim.simulate_star_ring(num_stars=24, ray_ticks=5.0, asymmetry_bias=0.10)
        cw = sim.simulate_star_ring(num_stars=24, ray_ticks=5.0, asymmetry_bias=-0.10)
        self.assertGreater(ccw["frame_drag_omega"], 0.0)
        self.assertLess(cw["frame_drag_omega"], 0.0)
        self.assertAlmostEqual(ccw["frame_drag_omega"], -cw["frame_drag_omega"], places=6)

    def test_action_reaction_recoil_and_inverse_r3_frame_dragging(self):
        """Isolated emission conserves L_core + L_stars = 0; core drag decays as 1/r^3."""
        sim = BCCKugelblitzSpinSim()
        res = sim.simulate_star_ring(num_stars=24, ray_ticks=5.0, asymmetry_bias=0.15)
        self.assertAlmostEqual(res["net_lz"] + res["recoil_stars_lz"], 0.0, places=8)
        drag = {r["r"]: r for r in sim.frame_dragging_radial_profile(core_lz=14.4, radii=[2.0, 4.0])}
        # Doubling r reduces 1/r^3 frame-dragging rate by a factor of 8
        self.assertAlmostEqual(drag.get(2.0)["omega_drag"] / drag.get(4.0)["omega_drag"], 8.0, places=5)


if __name__ == "__main__":
    unittest.main()
