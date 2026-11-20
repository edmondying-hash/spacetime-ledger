#!/usr/bin/env python3
"""Client-Server Spacetime Architecture: Entangled Spin Correlations & Bell CHSH Test.

Demonstrates:
1. Client Layer: Distant Alice & Bob detectors bounded by c = 1 BCC hop/tick.
2. Server Layer: Shared non-local singlet state pointer updating instantaneously.
3. No-Signaling Compliance: Local click marginals stay 50/50 random while joint
   correlations violate the classical Bell CHSH limit (S > 2.0, approaching 2*sqrt(2)).
"""

# ---- Fixed-copy label (Nov 19, 2026) ---------------------------------------
# INSERTED, NOT EMERGENT: the singlet correlation P(opposite) = cos^2(delta/2) is written into a
# non-local server table (by design). The toy shows this bookkeeping reproduces QM statistics and
# keeps marginals at 50/50; it does not derive them. Non-locality vs the 'local cells' checklist item: OD4.
# ---------------------------------------------------------------------------


import argparse
from dataclasses import dataclass
import math
from typing import Dict, List, Tuple
import numpy as np


@dataclass
class ServerSingletState:
    """Backend server memory object shared by two entangled client particles."""

    pair_id: int
    collapsed: bool = False
    first_angle_rad: float = 0.0
    first_outcome: int = 0  # +1 or -1


class SpacetimeServerBus:
    """Server-side state registry managing non-local entanglement pointers."""

    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)
        self._records: Dict[int, ServerSingletState] = {}

    def allocate_singlet_pair(self, pair_id: int) -> int:
        self._records[pair_id] = ServerSingletState(pair_id=pair_id)
        return pair_id

    def query_spin_measurement(self, pair_id: int, detector_angle_rad: float) -> int:
        """Resolve a client detector click against the shared server state record."""
        rec = self._records[pair_id]
        if not rec.collapsed:
            # First detector to trigger resolves 50/50 and locks server state
            outcome = 1 if self.rng.random() < 0.5 else -1
            rec.collapsed = True
            rec.first_angle_rad = detector_angle_rad
            rec.first_outcome = outcome
            return outcome

        # Second detector queries the already-updated server record:
        # P(same) = sin^2((theta_B - theta_A)/2), P(opposite) = cos^2((theta_B - theta_A)/2)
        delta_theta = detector_angle_rad - rec.first_angle_rad
        # INSERTED quantum rule (cos^2 of half-angle) in a NON-LOCAL server table, by design.
        prob_opposite = math.cos(delta_theta / 2.0) ** 2
        if self.rng.random() < prob_opposite:
            return -rec.first_outcome
        return rec.first_outcome


def run_bell_chsh_experiment(
    num_pairs: int = 10000,
    station_distance_hops: int = 48,
    seed: int = 42,
) -> Dict[str, float]:
    """Run simultaneous client-space measurements across 4 CHSH angle settings."""
    server = SpacetimeServerBus(seed=seed)

    # Optimal Bell CHSH detector angles (in degrees)
    # A0 = 0°, A1 = 45°, B0 = 22.5°, B1 = 67.5°
    angles_a = (0.0, 45.0)
    angles_b = (22.5, 67.5)

    correlations: Dict[Tuple[float, float], float] = {}
    alice_up_counts: List[int] = []
    bob_up_counts: List[int] = []

    pair_counter = 0
    for deg_a in angles_a:
        for deg_b in angles_b:
            rad_a = math.radians(deg_a)
            rad_b = math.radians(deg_b)
            prod_sum = 0
            a_ups = 0
            b_ups = 0

            for _ in range(num_pairs):
                pid = server.allocate_singlet_pair(pair_counter)
                pair_counter += 1

                # Both client stations trigger at the exact same tick (dt = 0 < 48 ticks)
                res_a = server.query_spin_measurement(pid, rad_a)
                res_b = server.query_spin_measurement(pid, rad_b)

                prod_sum += res_a * res_b
                if res_a == 1:
                    a_ups += 1
                if res_b == 1:
                    b_ups += 1

            correlations[(deg_a, deg_b)] = prod_sum / num_pairs
            alice_up_counts.append(a_ups / num_pairs)
            bob_up_counts.append(b_ups / num_pairs)

    e_00 = correlations[(0.0, 22.5)]
    e_01 = correlations[(0.0, 67.5)]
    e_10 = correlations[(45.0, 22.5)]
    e_11 = correlations[(45.0, 67.5)]

    # CHSH Bell parameter S = |E(A0, B0) - E(A0, B1) + E(A1, B0) + E(A1, B1)|
    chsh_s = abs(e_00 - e_01 + e_10 + e_11)

    print("=" * 74)
    print("SERVERSIDE MODULE 1: Client-Server Entanglement & Bell CHSH Benchmark")
    print("=" * 74)
    print(f"Client Separation : {station_distance_hops} BCC hops (Min light transit = {station_distance_hops} ticks)")
    print("Measurement Sync  : Simultaneous (dt = 0 ticks; client signaling impossible)")
    print("-" * 74)
    print("Detector Angles (A, B) | Measured E(A,B) | Theory -cos(A-B) | Error")
    print("-" * 74)
    for (da, db), val in correlations.items():
        theory = -math.cos(math.radians(da - db))
        err = abs(val - theory)
        print(f"  A={da:>4.1f}°, B={db:>4.1f}°     | {val:>15.4f} | {theory:>16.4f} | {err:.4f}")

    print("-" * 74)
    print(f"Alice Marginal P(+1)  : {sum(alice_up_counts)/len(alice_up_counts):.4f} (No-signaling 0.5000 check)")
    print(f"Bob Marginal   P(+1)  : {sum(bob_up_counts)/len(bob_up_counts):.4f} (No-signaling 0.5000 check)")
    print(f"Bell CHSH Parameter S : {chsh_s:.4f} (Classical Limit <= 2.0000 | Quantum Max = 2.8284)")
    print("=" * 74)

    return {"chsh_S": round(chsh_s, 4), "alice_marginal": round(sum(alice_up_counts) / 4.0, 4)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Client-Server Entangled Spin Correlation Test")
    parser.add_argument("--pairs", type=int, default=10000, help="Entangled pairs per angle setting")
    parser.add_argument("--distance", type=int, default=48, help="BCC hop separation between stations")
    args = parser.parse_args()
    run_bell_chsh_experiment(num_pairs=args.pairs, station_distance_hops=args.distance)


if __name__ == "__main__":
    main()
