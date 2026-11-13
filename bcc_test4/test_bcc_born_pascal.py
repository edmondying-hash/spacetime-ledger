#!/usr/bin/env python3
"""Unit tests for bcc_born_pascal.py (integer dual-Pascal cancellation & wave convergence)."""
import unittest
from bcc_born_pascal import compute_dual_pascal_distribution


class TestBCCBornPascal(unittest.TestCase):
    def test_pascal_conservation_and_dark_nodes(self):
        res = compute_dual_pascal_distribution(n_ticks=12)
        rows = {r['x']: r for r in res['rows']}

        total_paths = sum(r['pos'] + r['neg'] for r in res['rows'])
        self.assertEqual(total_paths, 4096)
        self.assertAlmostEqual(sum(r['p_born'] for r in res['rows']), 1.0, places=12)

        for dark_x in (-10, -6, -2, 2, 6, 10):
            self.assertEqual(rows[dark_x]['net_psi'], 0)
            self.assertEqual(rows[dark_x]['p_born'], 0.0)
            self.assertAlmostEqual(rows[dark_x]['p_wave'], 0.0, places=12)

    def test_convergence_to_continuous_wave_equation(self):
        err_12 = compute_dual_pascal_distribution(n_ticks=12)['max_abs_diff']
        err_100 = compute_dual_pascal_distribution(n_ticks=100)['max_abs_diff']
        self.assertLess(err_100, err_12 * 0.5)


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
