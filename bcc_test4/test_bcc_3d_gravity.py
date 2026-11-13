#!/usr/bin/env python3
"""Unit tests for bcc_3d_gravity.py (6-face connectivity, 1/r decay, lensing, deadlock, Pascal waves, and coupler)."""
import unittest
from bcc_3d_gravity import FACE_DIRS_6, BCC3DGravityGrid


class TestBCC3DGravity(unittest.TestCase):
    def test_six_face_stencil_and_continuous_connectivity(self):
        self.assertEqual(len(FACE_DIRS_6), 6)
        grid = BCC3DGravityGrid(size=15, max_node_ticks=100)
        grid.inject_3d_mass_core(7, 7, 7, total_workload=600.0, radius=1)
        grid.solve_3d_poisson_congestion(iterations=150)

        self.assertGreater(grid.workload[7][7][7], 0.0)
        self.assertGreater(grid.workload[7][7][8], 0.0)
        self.assertGreater(grid.workload[7][7][7], grid.workload[7][7][8])

    def test_3d_poisson_monotonic_radial_decay(self):
        grid = BCC3DGravityGrid(size=25, max_node_ticks=100)
        grid.inject_3d_mass_core(12, 12, 12, total_workload=1100.0, radius=1)
        grid.solve_3d_poisson_congestion(iterations=200)

        radial_vals = [grid.workload[12][12][12 + r] for r in range(1, 9)]
        for i in range(len(radial_vals) - 1):
            self.assertGreater(radial_vals[i], radial_vals[i + 1])
        self.assertGreater(radial_vals[-1], 0.0)

    def test_3d_wavefront_lensing_symmetry(self):
        grid = BCC3DGravityGrid(size=25, max_node_ticks=100)
        grid.inject_3d_mass_core(12, 12, 12, total_workload=1100.0, radius=1)
        grid.solve_3d_poisson_congestion(iterations=200)

        rays = grid.trace_3d_light_rays((2, 10, 12, 14, 22), z_plane=12, total_ticks=22)
        self.assertGreater(rays[2]['x'], rays[12]['x'])
        self.assertGreater(rays[2]['x'], rays[10]['x'])
        self.assertEqual(rays[10]['x'], rays[14]['x'])
        self.assertEqual(rays[2]['x'], rays[22]['x'])

    def test_3d_spherical_horizon_deadlock_and_zero_escape(self):
        bh = BCC3DGravityGrid(size=17, max_node_ticks=100, seed=42)
        bh.inject_3d_mass_core(8, 8, 8, total_workload=2400.0, radius=1)
        bh.solve_3d_poisson_congestion(iterations=200)

        init_core = len(bh.deadlocked)
        init_shell = len(bh.get_3d_boundary_shell())
        self.assertGreater(init_core, 0)
        self.assertGreater(init_shell, 0)

        stats = bh.simulate_3d_horizon_accretion(incoming_packets=260, packet_load=25)
        self.assertGreater(stats['total_deadlocked'], init_core)
        self.assertGreater(stats['exposed_3d_shell'], init_shell)
        self.assertEqual(stats['escaped_packets'], 0)
        self.assertTrue(all(dim > 1 for dim in stats['span_xyz']))

    def test_6face_zigzag_wave_orthogonality_and_periodicity(self):
        grid = BCC3DGravityGrid(size=25)
        path = grid.trace_6face_zigzag_wave(start=(2, 12, 12), ticks=8)

        for entry in path[1:]:
            dx, dy, dz = entry['step']
            self.assertEqual(abs(dx) + abs(dy) + abs(dz), 1)
            self.assertIn((dx, dy, dz), FACE_DIRS_6)

        self.assertEqual(path[-1]['pos'], (6, 12, 12))
        self.assertEqual((path[-1]['dy'], path[-1]['dz']), (0, 0))

    def test_biased_3d_pascal_wave_momentum_drift(self):
        grid = BCC3DGravityGrid(size=25)
        rest = grid.evolve_biased_3d_pascal_wave(momentum=(0, 0, 0), n_ticks=6)
        aimed = grid.evolve_biased_3d_pascal_wave(momentum=(2, -1, 1), n_ticks=6)

        self.assertEqual(rest['step_budget_per_tick'], 6)
        self.assertEqual(rest['born_centroid'], (0.0, 0.0, 0.0))
        self.assertGreater(rest['dark_nodes'], 0)

        self.assertEqual(aimed['step_budget_per_tick'], 10)
        cx, cy, cz = aimed['born_centroid']
        self.assertGreater(cx, 0.0)
        self.assertLess(cy, 0.0)
        self.assertGreater(cz, 0.0)
        self.assertGreater(aimed['dark_nodes'], 0)

    def test_momentum_to_gravity_coupler_increases_lensing(self):
        grid = BCC3DGravityGrid(size=25, max_node_ticks=100)
        rest_grav = grid.couple_pascal_momentum_to_gravity(momentum=(0, 0, 0), tick_scale=110.0)
        fast_grav = grid.couple_pascal_momentum_to_gravity(momentum=(3, 2, 1), tick_scale=110.0)

        self.assertGreater(fast_grav['total_workload'], rest_grav['total_workload'])
        self.assertGreater(fast_grav['peak_core_W'], rest_grav['peak_core_W'])
        self.assertGreater(fast_grav['lag_b0_pixels'], rest_grav['lag_b0_pixels'])
        self.assertGreater(fast_grav['lag_b2_pixels'], rest_grav['lag_b2_pixels'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
