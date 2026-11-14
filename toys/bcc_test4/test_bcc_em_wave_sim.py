#!/usr/bin/env python3
"""Unit tests for bcc_em_wave_sim.py (Gauss's law flux conservation and two-sublattice double-slit)."""
import unittest
from bcc_em_wave_sim import BCCMaxwellGrid, BCCDoubleSlitSim


class TestBCCEMAndSlit(unittest.TestCase):
    def test_gauss_law_and_charge_hop_conservation(self):
        grid = BCCMaxwellGrid(L=8)
        grid.place_dipole_charges((2, 3, 3), (6, 3, 3), q_mag=6.0)
        self.assertLess(grid.verify_gauss_law()['max_gauss_residual'], 1e-12)

        node = (2, 3, 3)
        for d in (0, 5, 2):
            node = grid.redraw_charge_step(node, d, dq=6.0)

        res = grid.verify_gauss_law()
        self.assertLess(res['max_gauss_residual'], 1e-12)
        self.assertAlmostEqual(res['net_global_charge'], 0.0, places=12)

    def test_two_sublattice_bins_all_rows_active_and_detector_fills_valleys(self):
        unobs = BCCDoubleSlitSim(width=36, height=45, barrier_x=10, slit_ys=(17, 27), wavelength_ticks=6)
        obs = BCCDoubleSlitSim(
            width=36, height=45, barrier_x=10, slit_ys=(17, 27), wavelength_ticks=6, detector_slit_y=17, seed=42
        )
        for t in range(120):
            unobs.step_redraw_wave(t)
            obs.step_redraw_wave(t)

        # Every screen row in the central band has nonzero signal thanks to two-sublattice binning
        for y in range(16, 29):
            self.assertGreater(unobs.detector_intensity[y], 0.0)
            self.assertGreater(obs.detector_intensity[y], 0.0)

        # Unobserved shows sharp constructive peak vs destructive valley
        max_u = max(unobs.detector_intensity)
        min_u = min(unobs.detector_intensity[y] for y in range(18, 27)) / max_u
        # Observed detector breaks phase cancellation, raising minimum valley intensity
        max_o = max(obs.detector_intensity)
        min_o = min(obs.detector_intensity[y] for y in range(18, 27)) / max_o
        self.assertGreater(min_o, min_u)


if __name__ == '__main__':
    try:
        import resource
    except ImportError:
        resource = None

    if resource is not None:
        resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
        if hasattr(resource, 'RLIMIT_AS'):
            resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))

    unittest.main(verbosity=2)
