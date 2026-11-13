#!/usr/bin/env python3
"""Unit tests for bcc3dhorizonsim.py (6-face 3D network-deadlock horizon & shell accretion)."""
import unittest
from bcc3dhorizonsim import FACE_DIRS_6, BCC3DHorizonSim


class TestBCC3DHorizonSim(unittest.TestCase):
    def test_six_face_stencil_and_initial_deadlock(self):
        self.assertEqual(len(FACE_DIRS_6), 6)
        sim = BCC3DHorizonSim(size=17, max_node_ticks=100, seed=42)
        sim.inject_3d_core(8, 8, 8, total_workload=2400.0, radius=1)
        sim.relax_3d_congestion(iterations=200)

        self.assertGreater(len(sim.deadlocked), 0)
        self.assertGreater(len(sim.get_3d_boundary_shell()), 0)

    def test_horizon_accretion_zero_escapes_and_3d_growth(self):
        sim = BCC3DHorizonSim(size=17, max_node_ticks=100, seed=42)
        sim.inject_3d_core(8, 8, 8, total_workload=2400.0, radius=1)
        sim.relax_3d_congestion(iterations=200)

        init_core = len(sim.deadlocked)
        init_shell = len(sim.get_3d_boundary_shell())

        stats = sim.step_accretion(incoming_packets=260, packet_load=25)
        self.assertGreater(stats['total_deadlocked'], init_core)
        self.assertGreater(stats['exposed_3d_shell'], init_shell)
        self.assertEqual(stats['escaped_packets'], 0)
        self.assertTrue(all(dim > 1 for dim in stats['span_xyz']))

    def test_radial_profile_blocks_core_and_relaxes_outside(self):
        sim = BCC3DHorizonSim(size=19, max_node_ticks=100, seed=42)
        sim.inject_3d_core(9, 9, 9, total_workload=2400.0, radius=1)
        sim.relax_3d_congestion(iterations=200)

        profile = sim.radial_horizon_profile(9, 9, 9, max_r=6)
        self.assertEqual(profile[0]['status'], 'DEADLOCKED / BLOCKED')
        self.assertIsNone(profile[0]['extra_tick_delay'])
        self.assertEqual(profile[-1]['status'], 'Active I/O')
        self.assertIsNotNone(profile[-1]['extra_tick_delay'])


if __name__ == "__main__":
    unittest.main(verbosity=2)
