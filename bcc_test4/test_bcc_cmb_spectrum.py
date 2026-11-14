#!/usr/bin/env python3
"""Unit tests for CMB blackbody spectrum and acoustic peak on the 6-face Planck lattice."""

import unittest
from bcc_cmb_spectrum import BCCCMBSpectrumSim


class TestBCCCMBSpectrum(unittest.TestCase):
    def test_recombination_redshift_cools_to_2_725_kelvin_and_411_photons_cm3(self):
        """Stretching T_recomb = 2994.775 K by 1 + z = 1099 yields T_0 = 2.725 K and ~410.7 cm^-3."""
        sim = BCCCMBSpectrumSim(t_recomb_k=2994.775, z_recomb=1098.0, eta_baryon=6.10e-10)
        dens = sim.photon_and_baryon_densities()
        self.assertAlmostEqual(dens["t0_k"], 2.725, places=3)
        self.assertAlmostEqual(dens["n_gamma_cm3"], 410.7, delta=1.0)

    def test_planck_blackbody_peaks_at_160_2_ghz(self):
        """Planck spectral radiance at T_0 = 2.725 K reaches its maximum at 160.2 GHz."""
        sim = BCCCMBSpectrumSim()
        spec = sim.planck_blackbody_spectrum([80.0, 120.0, 160.2, 220.0, 300.0])
        peak_row = max(spec, key=lambda r: r["b_nu_si"])
        self.assertEqual(peak_row["freq_ghz"], 160.2)
        self.assertEqual(peak_row["norm_radiance"], 1.0)

    def test_three_axis_sound_speed_yields_first_acoustic_peak_at_ell_220(self):
        """3D orthogonal plasma c_s = c/sqrt(3) gives first CMB acoustic peak at l_1 ~ 220."""
        sim = BCCCMBSpectrumSim()
        ac = sim.acoustic_peak_multipole()
        self.assertAlmostEqual(ac["c_s_over_c"], 3.0 ** -0.5, places=6)
        self.assertAlmostEqual(ac["ell_1_grid"], 220.0, delta=2.0)


if __name__ == "__main__":
    unittest.main()
