#!/usr/bin/env python3
"""Unit tests for congestion-gated dark energy and void expansion on the 6-face lattice."""

import unittest
from bcc_dark_energy import BCCDarkEnergySim


class TestBCCDarkEnergy(unittest.TestCase):
    def test_bound_galaxies_do_not_expand_while_voids_stretch(self):
        """High-load bound galaxies remain fixed in width while idle void nodes expand."""
        sim = BCCDarkEnergySim(expand_thresh=20.0, h_vac_rate=0.01)
        res = sim.evolve_galaxy_void_ruler(
            galaxy_width_lp=10.0, void_width_lp=20.0, galaxy_load=85.0, void_load=0.0, steps=50
        )
        self.assertEqual(res["galaxy_gate"], 0.0)
        self.assertEqual(res["void_gate"], 1.0)
        self.assertEqual(res["galaxy_final_lp"], 10.0)
        self.assertGreater(res["void_final_lp"], 32.0)

    def test_cosmic_expansion_flips_from_deceleration_to_acceleration(self):
        """q(z) is positive in the early matter-dominated era and negative today (z=0)."""
        sim = BCCDarkEnergySim(omega_m0=0.315, omega_l0=0.685)
        hist = {r["z"]: r for r in sim.cosmic_acceleration_history([3.0, 0.0])}
        self.assertGreater(hist.get(3.0)["decel_q"], 0.3)
        self.assertLess(hist.get(0.0)["decel_q"], -0.5)

    def test_transition_redshift_occurs_near_z_0_63(self):
        """Inflection point q(z_acc) = 0 occurs at z_acc ~ 0.632 for Planck Omega_m0=0.315."""
        sim = BCCDarkEnergySim(omega_m0=0.315, omega_l0=0.685)
        z_acc = sim.transition_redshift()
        self.assertAlmostEqual(z_acc, 0.632, places=2)


if __name__ == "__main__":
    unittest.main()
