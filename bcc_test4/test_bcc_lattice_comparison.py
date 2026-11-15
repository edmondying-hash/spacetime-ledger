#!/usr/bin/env python3
"""Unit tests comparing 6-face simple cubic vs. 8-link BCC stencils."""

import unittest
from bcc_lattice_comparison import BCCLatticeComparisonSim


class TestBCCLatticeComparison(unittest.TestCase):
    def test_stencil_degrees_and_diagonal_vs_axial_hop_gap(self):
        """6-face has 6 links (6 hops to (2,2,2)); 8-link BCC has 8 links (2 hops to (2,2,2))."""
        sim = BCCLatticeComparisonSim()
        self.assertEqual(len(sim.STENCIL_6FACE), 6)
        self.assertEqual(len(sim.STENCIL_8BCC), 8)
        rows = {r["target"]: r for r in sim.hop_distance_comparison()}
        diag = rows.get("Body Diagonal (2, 2, 2)")
        self.assertEqual(diag["hops_6face"], 6)
        self.assertEqual(diag["hops_8bcc"], 2)

    def test_eight_link_bcc_splits_into_disconnected_parity_sublattices(self):
        """8-link BCC cannot reach odd-parity (1,0,0) from (0,0,0), whereas 6-face reaches all nodes."""
        sim = BCCLatticeComparisonSim()
        rows = {r["target"]: r for r in sim.hop_distance_comparison()}
        odd = rows.get("Odd Cardinal (1, 0, 0)")
        self.assertEqual(odd["hops_6face"], 1)
        self.assertIsNone(odd["hops_8bcc"])

    def test_both_stencils_produce_positive_3d_poisson_fields(self):
        """3D Poisson relaxation yields positive axial and diagonal r*W(r) on both stencils."""
        sim = BCCLatticeComparisonSim()
        iso = sim.isotropy_gap_benchmark()
        self.assertGreater(iso["6face_axis_rW"], 0.0)
        self.assertGreater(iso["8bcc_diag_rW"], 0.0)

    def test_six_face_pascal_walk_covers_more_space_and_forms_exact_dark_nodes(self):
        """6-face Pascal walk visits 231 cubes (vs. 85 on BCC) and cancels cleanly on x=0."""
        sim = BCCLatticeComparisonSim()
        pw = sim.pascal_walk_benchmark(ticks=6)
        self.assertEqual(pw["6face_active_cubes"], 231)
        self.assertEqual(pw["8bcc_active_cubes"], 343)
        self.assertEqual(pw["6face_max_nodal_residual"], 0)


if __name__ == "__main__":
    unittest.main()

