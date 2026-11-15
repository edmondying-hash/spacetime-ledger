#!/usr/bin/env python3
"""Unit tests for 2-body EM link-flux attraction, repulsion, and mass-gated recoil."""

import unittest
from bcc_em_recoil import BCCEMRecoilSim


class TestBCCEMRecoil(unittest.TestCase):
    def test_lighter_particle_moves_more_regardless_of_charge_sign(self):
        """e- moves ~1836x more than p+, while p+ moves ~1.41x more than heavier Xi-."""
        sim = BCCEMRecoilSim(k_flux=50.0)
        ep = sim.simulate_pair("e-", -1.0, 0.511, "p+", +1.0, 938.272)
        pxi = sim.simulate_pair("p+", +1.0, 938.272, "Xi-", -1.0, 1321.710)
        self.assertAlmostEqual(ep["disp_ratio_1_to_2"], 938.272 / 0.511, delta=1.0)
        self.assertAlmostEqual(pxi["disp_ratio_1_to_2"], 1321.710 / 938.272, places=2)

    def test_equal_mass_opposites_meet_symmetrically_with_zero_momentum_drift(self):
        """e- and e+ share 50%/50% displacement and conserve p_1 + p_2 = 0."""
        sim = BCCEMRecoilSim(k_flux=50.0)
        ee = sim.simulate_pair("e-", -1.0, 0.511, "e+", +1.0, 0.511)
        self.assertEqual(ee["share1_pct"], 50.0)
        self.assertEqual(ee["share2_pct"], 50.0)
        self.assertAlmostEqual(ee["momentum_residual"], 0.0, places=9)

    def test_like_charges_repel_and_increase_separation(self):
        """Matching flux signs (+1 with +1) increase final separation above initial 10.0 l_P."""
        sim = BCCEMRecoilSim(k_flux=50.0)
        pp = sim.simulate_pair("p+", +1.0, 938.272, "p+", +1.0, 938.272, sep0_lp=10.0)
        self.assertGreater(pp["final_sep_lp"], 10.0)
        self.assertAlmostEqual(pp["momentum_residual"], 0.0, places=9)


if __name__ == "__main__":
    unittest.main()
