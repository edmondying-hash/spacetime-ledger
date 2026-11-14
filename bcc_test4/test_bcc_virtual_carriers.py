#!/usr/bin/env python3
"""Unit tests for virtual force-carrier signals on the 3D 6-face Planck-cube grid."""

import unittest
from bcc_virtual_carriers import BCCVirtualCarrierSim


class TestBCCVirtualCarriers(unittest.TestCase):
    def test_massless_photon_conserves_shell_flux_and_follows_inverse_r(self):
        """m=0 carrier produces exact V(r) = 1/r and constant 3D shell flux = 1.0."""
        sim = BCCVirtualCarrierSim()
        rows = sim.simulate_carrier_range(max_hops=8, mass_mev=0.0)
        for row in rows:
            self.assertAlmostEqual(row["potential"], 1.0 / row["hops"], places=6)
            self.assertAlmostEqual(row["shell_flux"], 1.0, places=6)

    def test_massive_weak_carrier_exhibits_yukawa_short_range_cutoff(self):
        """m>0 weak carrier decays exponentially so flavor flips only fire at short range."""
        sim = BCCVirtualCarrierSim()
        near = sim.weak_flavor_transition_rate(separation_hops=1)
        far = sim.weak_flavor_transition_rate(separation_hops=8)
        self.assertTrue(near["transition_active"])
        self.assertFalse(far["transition_active"])
        self.assertLess(far["loan_survival"], 0.01)

    def test_gluon_carrier_bundles_linearly_and_breaks_at_seven_hops(self):
        """Self-interacting gluon carriers grow at 45 MeV/hop and snap at hop 7 (> 275 MeV)."""
        sim = BCCVirtualCarrierSim()
        by_hop = {r["hops"]: r for r in sim.gluon_carrier_bundling(max_hops=8)}
        self.assertFalse(by_hop.get(6)["snapped"])  # Hop 6 = 270 MeV (intact)
        self.assertTrue(by_hop.get(7)["snapped"])   # Hop 7 = 315 MeV (snapped)


if __name__ == "__main__":
    unittest.main()
