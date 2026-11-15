#!/usr/bin/env python3
"""Unit tests for the 4-component Dirac spinor prototype on the 6-face lattice."""

import unittest
from bcc_dirac4_spinor import BCCDirac4SpinorSim


class TestBCCDirac4Spinor(unittest.TestCase):
    def test_spinor_720_degree_double_cover_symmetry(self):
        """360 deg rotation flips spinor sign (-1); 720 deg rotation restores +1."""
        sim = BCCDirac4SpinorSim()
        rows = {r["angle_deg"]: r for r in sim.spin_rotation_360_vs_720([0.0, 360.0, 720.0])}
        self.assertAlmostEqual(rows.get(0.0)["real_overlap"], 1.0, places=6)
        self.assertAlmostEqual(rows.get(360.0)["real_overlap"], -1.0, places=6)
        self.assertAlmostEqual(rows.get(720.0)["real_overlap"], 1.0, places=6)

    def test_rest_mass_zitterbewegung_conserves_unit_probability(self):
        """Chiral oscillation between L and R at p=0 preserves |psi|^2 = 1.000000."""
        sim = BCCDirac4SpinorSim()
        for row in sim.rest_mass_zitterbewegung(steps=8, dt=0.25):
            self.assertAlmostEqual(row["norm"], 1.0, places=6)

    def test_six_face_chiral_wavepacket_advances_forward_unitarily(self):
        """Dirac-Wilson split-step walk along +x face advances <x> > 0 with unit norm."""
        sim = BCCDirac4SpinorSim(mass_mev=0.511)
        wp = sim.propagate_6face_wavepacket(grid_len=25, ticks=6, k_mom=0.50)
        self.assertAlmostEqual(wp["total_norm"], 1.0, places=5)
        self.assertGreater(wp["mean_shift_x"], 2.0)


if __name__ == "__main__":
    unittest.main()
