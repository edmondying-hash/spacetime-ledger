#!/usr/bin/env python3
"""Unit tests for EM-neutral dark matter load halos on the 6-face Planck-cube grid."""

import unittest
from bcc_dark_matter import BCCDarkMatterSim


class TestBCCDarkMatter(unittest.TestCase):
    def test_invisible_lensing_zero_em_coupling_positive_lag(self):
        """Q_EM = 0 loop halo causes 0% photon attenuation while bending gravitational wavefronts."""
        sim = BCCDarkMatterSim()
        core = sim.invisible_lensing_probe(impact_b=0)
        far = sim.invisible_lensing_probe(impact_b=10)
        self.assertEqual(core["q_em"], 0.0)
        self.assertEqual(core["em_attenuation"], 0.0)
        self.assertGreater(core["grav_lag_px"], far["grav_lag_px"])
        self.assertEqual(far["grav_lag_px"], 0)

    def test_flat_rotation_curve_vs_keplerian_drop(self):
        """Adding an EM-neutral loop halo prevents Keplerian 1/sqrt(r) velocity decay at large r."""
        sim = BCCDarkMatterSim()
        curve = sim.rotation_curve([4.0, 12.0, 20.0])
        r4 = next(row for row in curve if row["r"] == 4.0)
        r20 = next(row for row in curve if row["r"] == 20.0)
        self.assertLess(r20["v_baryon"], 0.55 * r4["v_baryon"])
        self.assertGreater(r20["v_total"], 0.90 * r4["v_total"])

    def test_bullet_cluster_halo_baryon_separation(self):
        """Collisionless dark halos pass through each other while EM baryons shock and lag."""
        sim = BCCDarkMatterSim()
        res = sim.bullet_cluster_collision(ticks=10)
        self.assertGreater(res["dark_halo_sep"], res["baryon_sep"])
        self.assertGreater(res["lensing_offset"], 0.0)


if __name__ == "__main__":
    unittest.main()
