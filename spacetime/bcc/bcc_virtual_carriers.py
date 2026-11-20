#!/usr/bin/env python3
"""
Virtual Force-Carrier Signals on the 3D BCC (8-Diagonal) Lattice.

Models off-shell vacuum ledger loans (Delta_E * Delta_t <= hbar/2) propagated across
the 8 BCC body diagonals (1 hop/tick, physical step = sqrt(3) l_P):
  1. Massless Carrier (gamma, m=0): Zero vacuum payback tax -> infinite-range 1/r
     potential and exact 1/r^2 shell flux conservation across BCC shells.
  2. Massive Weak Carrier (W/Z, m>0): Exponential vacuum loan decay exp(-r_bcc/r0)/r_bcc
     (Yukawa screening), limiting flavor transitions to 1-2 BCC neighbor hops.
  3. Self-Interacting Gluon Carrier (g, m=0, ColorLoad>0): Color-charged carriers
     bundle via shared link congestion into a 1D flux tube (77.94 MeV/hop, snaps at 4 hops).
"""

import math
from typing import Any, Dict, List

BCC_DIAG_SCALE = math.sqrt(3.0)
BCC_TICKS_PER_HOP = round(9.0 * BCC_DIAG_SCALE, 3)  # ~15.588 ticks / BCC diagonal hop


class BCCVirtualCarrierSim:
    """Simulates virtual gauge-boson carrier waves on the 3D BCC 8-diagonal lattice."""

    def __init__(self, tick_to_mev: float = 5.0):
        self.tick_to_mev = tick_to_mev

    def simulate_carrier_range(
        self,
        max_hops: int = 8,
        mass_mev: float = 0.0,
        range_scale_hops: float = 1.5,
    ) -> List[Dict[str, Any]]:
        """
        Propagate a virtual carrier wave from hops=1..max_hops on the 3D BCC lattice.
        Potential V(r) ~ exp(-r / r0) / r, where r0 -> inf as mass_mev -> 0.
        """
        rows: List[Dict[str, Any]] = []
        for h in range(1, max_hops + 1):
            r = float(h)
            decay = 1.0 if mass_mev <= 0.0 else math.exp(-r / range_scale_hops)
            potential = decay / r
            force = potential * ((1.0 / r) + (0.0 if mass_mev <= 0.0 else 1.0 / range_scale_hops))
            shell_flux = (r ** 2) * force
            rows.append({
                "hops": h,
                "r_bcc": round(h * BCC_DIAG_SCALE, 3),
                "mass_mev": mass_mev,
                "decay_factor": round(decay, 6),
                "potential": round(potential, 6),
                "shell_flux": round(shell_flux, 6),
            })
        return rows

    def weak_flavor_transition_rate(
        self, separation_hops: int, w_mass_mev: float = 80379.0, range_scale_hops: float = 1.2
    ) -> Dict[str, Any]:
        """Compute virtual W+- carrier loan survival for a Gen 3 -> Gen 2 / Gen 1 flavor hop."""
        loan_survival = math.exp(-separation_hops / range_scale_hops)
        allowed = loan_survival > 0.01
        return {
            "separation_hops": separation_hops,
            "w_mass_mev": w_mass_mev,
            "loan_survival": round(loan_survival, 6),
            "transition_active": allowed,
            "status": "Flavor flip active (W+- absorbed)" if allowed else "Loan expired (refunded to vacuum)",
        }

    def gluon_carrier_bundling(
        self,
        max_hops: int = 8,
        ticks_per_hop: float = BCC_TICKS_PER_HOP,
        break_threshold_mev: float = 275.0,
    ) -> List[Dict[str, Any]]:
        """
        Unlike photons (independent 1/r^2 spread), color-charged gluon carriers
        attract via shared link congestion into a 1D BCC flux tube (~77.94 MeV/hop).
        """
        rows: List[Dict[str, Any]] = []
        for h in range(1, max_hops + 1):
            tube_mev = h * ticks_per_hop * self.tick_to_mev
            snapped = tube_mev > break_threshold_mev
            rows.append({
                "hops": h,
                "tube_mev": round(tube_mev, 2),
                "snapped": snapped,
                "regime": "Snapped -> new q qbar pair" if snapped else "1D bundled BCC color flux tube",
            })
        return rows


def run_virtual_carrier_demo() -> None:
    sim = BCCVirtualCarrierSim()
    print("=== PART 1: 3D BCC Massless Photon (1/r) vs. Massive Weak Boson (Yukawa) ===")
    print("BCC Hops   Dist (l_P)   Photon V(r)   Photon Flux   Weak V(r)   Weak Survival   Force Regime")
    print("-" * 94)
    em_rows = sim.simulate_carrier_range(max_hops=8, mass_mev=0.0)
    wk_rows = sim.simulate_carrier_range(max_hops=8, mass_mev=80379.0, range_scale_hops=1.5)
    for em, wk in zip(em_rows, wk_rows):
        regime = "Long-range 1/r + short weak" if wk["decay_factor"] > 0.1 else "Pure long-range EM/Gravity"
        print(
            f"{em['hops']:>8} {em['r_bcc']:>12.3f} {em['potential']:>13.6f} {em['shell_flux']:>13.6f} "
            f"{wk['potential']:>11.6f} {wk['decay_factor']:>15.6f}   {regime}"
        )

    print("\n=== PART 2: Self-Interacting Gluon Carrier Bundling vs. Photon Spread ===")
    print("BCC Hops   Photon V(r) (1/r)   Gluon Tube (MeV)   Confinement State")
    print("-" * 76)
    gl_rows = sim.gluon_carrier_bundling(max_hops=8)
    for em, gl in zip(em_rows, gl_rows):
        print(
            f"{em['hops']:>8} {em['potential']:>19.6f} {gl['tube_mev']:>18.2f}   {gl['regime']}"
        )


if __name__ == "__main__":
    run_virtual_carrier_demo()

