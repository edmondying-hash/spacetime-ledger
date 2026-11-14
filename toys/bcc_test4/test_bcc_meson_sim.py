#!/usr/bin/env python3
"""Unit tests for bcc_meson_sim.py (meson spectrum, 3:1 hyperfine ratio, and string breaking)."""
import unittest
from bcc_meson_sim import BCCMesonSim


class TestBCCMesonSim(unittest.TestCase):
    def test_ground_state_meson_spectrum_ordering(self):
        sim = BCCMesonSim()
        rows = {r['name']: r for r in sim.run_spectrum()}

        self.assertLess(rows['pi']['ModelMeV'], rows['K']['ModelMeV'])
        self.assertLess(rows['K']['ModelMeV'], rows['rho']['ModelMeV'])
        self.assertLess(rows['rho']['ModelMeV'], rows['K*']['ModelMeV'])
        self.assertLess(rows['K*']['ModelMeV'], rows['phi']['ModelMeV'])
        self.assertLess(rows['phi']['ModelMeV'], rows['D']['ModelMeV'])
        self.assertLess(rows['D']['ModelMeV'], rows['D*']['ModelMeV'])
        self.assertLess(rows['D*']['ModelMeV'], rows['J/psi']['ModelMeV'])

    def test_hyperfine_3_to_1_ratio_and_heavy_quark_suppression(self):
        sim = BCCMesonSim()
        rows = {r['name']: r for r in sim.run_spectrum()}

        # Exact 3:1 pseudoscalar (J=0) vs vector (J=1) hyperfine splitting ratio
        pi_res = rows['pi']
        rho_res = rows['rho']
        self.assertAlmostEqual(abs(pi_res['SpinT']) / abs(rho_res['SpinT']), 3.0, places=6)

        # Heavy-quark 1/(m_i m_j) hyperfine suppression: (rho - pi) > (K* - K) > (D* - D)
        split_light = rows['rho']['ModelMeV'] - rows['pi']['ModelMeV']
        split_strange = rows['K*']['ModelMeV'] - rows['K']['ModelMeV']
        split_charm = rows['D*']['ModelMeV'] - rows['D']['ModelMeV']
        self.assertGreater(split_light, split_strange)
        self.assertGreater(split_strange, split_charm)

    def test_color_confinement_string_breaking(self):
        sim = BCCMesonSim()
        stretch = sim.simulate_flux_tube_stretch(max_hops=9)

        self.assertEqual(stretch['snapped_at_hop'], 7)
        self.assertFalse(stretch['steps'][6]['broken'])
        self.assertTrue(stretch['steps'][7]['broken'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
