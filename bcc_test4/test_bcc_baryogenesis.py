#!/usr/bin/env python3
"""Unit tests for bcc_baryogenesis r2: checks against data and math, not against its own knobs."""

import math
import random
import unittest

import bcc_baryogenesis as bb
from bcc_baryogenesis import BCCBaryogenesisSim


class TestBCCBaryogenesis(unittest.TestCase):
    def test_ckm_jarlskog_matches_pdg_within_errors(self):
        """J from the PDG 2024 standard-parametrisation matrix lies inside the PDG 2024 fit band."""
        v = bb.ckm_standard()
        self.assertLess(bb.unitarity_defect(v), 1e-12)
        j = bb.jarlskog(v)
        self.assertGreater(j, bb.PDG2024_J - bb.PDG2024_J_ERR_DN)
        self.assertLess(j, bb.PDG2024_J + bb.PDG2024_J_ERR_UP)

    def test_unitarity_bound_holds(self):
        """|J| <= 1/(6 sqrt 3) for PDG values and for random angles/phases; bound reached at max mixing."""
        self.assertLessEqual(abs(bb.jarlskog(bb.ckm_standard())), bb.J_MAX)
        rng = random.Random(1)
        for _ in range(2000):
            s = [rng.uniform(0, 1) for _ in range(3)]
            v = bb.ckm_standard(s[0], s[1], s[2], rng.uniform(0, 2 * math.pi))
            self.assertLessEqual(abs(bb.jarlskog(v)), bb.J_MAX + 1e-12)
        s = 1 / math.sqrt(2)
        s13 = 1 / math.sqrt(3)
        self.assertAlmostEqual(bb.jarlskog(bb.ckm_standard(s, s13, s, math.pi / 2)), bb.J_MAX, places=12)

    def test_jarlskog_rephasing_invariant(self):
        v = bb.ckm_standard()
        rng = random.Random(3)
        for _ in range(20):
            rp = bb.rephase(v, [rng.uniform(0, 7) for _ in range(3)], [rng.uniform(0, 7) for _ in range(3)])
            self.assertAlmostEqual(bb.jarlskog(rp), bb.jarlskog(v), places=17)

    def test_two_generations_have_no_cp_phase(self):
        """General U(2): quartet Im is 0 and the matrix rephases to real; phase count (N-1)(N-2)/2."""
        chk = bb.two_generation_check(trials=500)
        self.assertLess(chk["max_abs_quartet"], 1e-14)
        self.assertLess(chk["max_imag_after_rephasing"], 1e-12)
        self.assertEqual([bb.physical_cp_phases(n) for n in (1, 2, 3, 4)], [0, 0, 1, 3])
        sim = BCCBaryogenesisSim()
        for n in (1, 2):
            res = sim.simulate_universe(n)
            self.assertLess(abs(res["baryon_to_photon"]), 1e-20)

    def test_degenerate_masses_kill_cp(self):
        """Jarlskog determinant = 2 J F_u F_d, and vanishes when two down-type masses are equal."""
        v = bb.ckm_standard()
        mu, md = bb.QUARK_MASSES_GEV["up"], bb.QUARK_MASSES_GEV["down"]
        d = bb.jarlskog_determinant(v, mu, md)
        expected = 2 * bb.jarlskog(v) * bb.mass_factor(mu) * bb.mass_factor(md)
        self.assertAlmostEqual(abs(d.imag) / expected, 1.0, places=6)
        d0 = bb.jarlskog_determinant(v, mu, (md[1], md[1], md[2]))
        self.assertLess(abs(d0) / expected, 1e-9)

    def test_required_epsilon_reproduces_eta(self):
        """eps from the inverted closed form, fed through the explicit cascade, gives eta = 6.1e-10."""
        j = bb.jarlskog(bb.ckm_standard())
        eps = bb.required_epsilon(bb.ETA_TARGET, j)
        res = BCCBaryogenesisSim(initial_per_gen=10000).simulate_universe(3, eps_3d=eps)
        self.assertAlmostEqual(res["baryon_to_photon"] / bb.ETA_TARGET, 1.0, places=6)
        self.assertAlmostEqual(eps / (1.5 * bb.ETA_TARGET / j), 1.0, places=6)
        self.assertEqual(res["surviving_anti"], 0.0)


if __name__ == "__main__":
    unittest.main()
