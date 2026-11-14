#!/usr/bin/env python3
"""Unit tests for 3-generation chiral baryogenesis (untuned toy vs. cosmic-tuned)."""

import unittest
from bcc_baryogenesis import BCCBaryogenesisSim


class TestBCCBaryogenesis(unittest.TestCase):
    def test_one_and_two_generations_annihilate_completely(self):
        """With 1 or 2 generations, J_cp = 0 so both toy and cosmic cascades leave 0 matter."""
        sim = BCCBaryogenesisSim(initial_per_gen=10000)
        for n in (1, 2):
            for eps in (sim.eps_toy, sim.eps_cosmic):
                res = sim.simulate_universe(n, eps_3d=eps)
                self.assertEqual(res["j_cp"], 0.0)
                self.assertEqual(res["surviving_matter"], 0.0)
                self.assertEqual(res["surviving_anti"], 0.0)

    def test_three_generations_untuned_and_cosmic_tuned_surplus(self):
        """3D chiral cascade produces positive Gen 1 matter; cosmic bias matches eta ~ 6.1e-10."""
        sim = BCCBaryogenesisSim(initial_per_gen=10000)
        toy = sim.simulate_universe(3, eps_3d=sim.eps_toy)
        cos = sim.simulate_universe(3, eps_3d=sim.eps_cosmic)
        self.assertGreater(toy["surviving_matter"], 500.0)
        self.assertEqual(toy["surviving_anti"], 0.0)
        self.assertAlmostEqual(cos["baryon_to_photon"], 6.10e-10, delta=0.05e-10)
        self.assertEqual(cos["surviving_anti"], 0.0)

    def test_three_generations_fit_under_100_tick_node_cap(self):
        """Gen 1..3 fit under the 100-tick node throughput cap while Gen 4 exceeds it."""
        sim = BCCBaryogenesisSim()
        loads = sim.generation_node_loads(node_cap=100.0)
        self.assertTrue(all(row["allowed"] for row in loads[:3]))
        self.assertFalse(loads[3]["allowed"])


if __name__ == "__main__":
    unittest.main()
