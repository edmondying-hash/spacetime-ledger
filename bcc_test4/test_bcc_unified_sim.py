#!/usr/bin/env python3
"""Unit tests for bcc_unified_sim.py (tick accounting, mass gap, lensing lag, and strict 2D/3D horizon)."""
import unittest
from bcc_unified_sim import (
    bcc_step_distance,
    steiner_y_links,
    BCCUnifiedGrid,
    BCCNetworkCongestion,
)


class BCCUnifiedTests(unittest.TestCase):
    def test_bcc_distance_and_steiner_links(self):
        self.assertEqual(bcc_step_distance((0, 0, 0), (1, 1, 1), L=8), 1)
        self.assertEqual(bcc_step_distance((0, 0, 0), (7, 7, 7), L=8), 1)
        self.assertEqual(steiner_y_links([(0, 0, 0), (0, 0, 0), (0, 0, 0)], L=8), 0)
        self.assertEqual(steiner_y_links([(0, 0, 0), (1, 1, 1), (7, 7, 7)], L=8), 2)

    def test_strange_quark_redraw_lag_and_mass_ordering(self):
        grid = BCCUnifiedGrid(seed=7)
        n_res = grid.run_baryon_subroutine(('l', 'l', 'l'), (-0.75, 0.0, 0.0), total_cycles=1500)
        delta_res = grid.run_baryon_subroutine(('l', 'l', 'l'), (0.25, 0.25, 0.25), total_cycles=1500)
        omega_res = grid.run_baryon_subroutine(('s', 's', 's'), (0.25, 0.25, 0.25), total_cycles=1500)

        self.assertGreater(n_res['redraws_per_cycle'], omega_res['redraws_per_cycle'])
        self.assertLess(n_res['mass_MeV'], delta_res['mass_MeV'])
        self.assertLess(delta_res['mass_MeV'], omega_res['mass_MeV'])
        self.assertGreater(n_res['active_load_pct'], 95.0)

    def test_pure_gluon_glueball_mass_gap(self):
        grid = BCCUnifiedGrid(seed=42)
        gb4 = grid.run_glueball_loop(loop_links=4, vertex_self_coupling=280, total_cycles=1500)
        gb6 = grid.run_glueball_loop(loop_links=6, vertex_self_coupling=280, total_cycles=1500)
        gb8 = grid.run_glueball_loop(loop_links=8, vertex_self_coupling=280, total_cycles=1500)

        self.assertEqual(gb4['bare_ticks'], 0.0)
        self.assertEqual(gb4['active_load_pct'], 100.0)
        self.assertGreater(gb4['mass_MeV'], 1800.0)
        self.assertLess(gb4['mass_MeV'], gb6['mass_MeV'])
        self.assertLess(gb6['mass_MeV'], gb8['mass_MeV'])

        with self.assertRaises(ValueError):
            grid.run_glueball_loop(loop_links=3)

    def test_congestion_lensing_lag(self):
        net = BCCNetworkCongestion(size=25, max_node_ticks=100)
        net.place_mass_cluster_2d(cx=12, cy=12, core_load=85, falloff=3.0)
        packets = net.trace_light_wavefront((2, 12, 22), total_ticks=24)
        self.assertGreater(packets[2]['x'], packets[12]['x'])
        self.assertEqual(packets[2]['x'], packets[22]['x'])

    def test_2d_core_3d_shell_strict_lock(self):
        net = BCCNetworkCongestion(size=15, max_node_ticks=100, seed=42)
        net.seed_flat_2d_core(cx=7, cy=7, cz=7, radius=2)
        initial_core = len(net.deadlocked_3d)
        initial_shell = len(net.get_3d_boundary_shell())
        self.assertEqual(initial_core, 13)
        self.assertEqual(initial_shell, 66)

        stats = net.simulate_3d_infall_strict_lock(incoming_packets=220, packet_load=20)
        self.assertGreater(stats['total_deadlocked'], initial_core)
        self.assertGreater(stats['exposed_3d_shell'], initial_shell)
        self.assertGreater(stats['active_edge_nodes_hit'], 0)
        self.assertEqual(stats['escaped_packets'], 0)
        self.assertGreater(stats['span_xyz'][2], 1)


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

