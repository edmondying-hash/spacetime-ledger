#!/usr/bin/env python3
"""
3-Generation Baryogenesis on the 3D 6-Face Planck-Cube Grid.

Compares side-by-side:
  1. Toy Bias (eps_3d = 0.015): Macroscopic view of Gen 3 -> 2 -> 1 chiral asymmetry.
  2. Cosmic Tuned (eps_3d = 1.002e-9): Reproduces the observed Big Bang baryon-to-photon
     ratio eta = n_B / n_gamma ~ 6.10e-10 while N_gen = 1, 2 still annihilate to 0.
"""

import math
from typing import Any, Dict, List


class BCCBaryogenesisSim:
    """3D lattice cascade simulator comparing toy and cosmic-tuned chiral biases."""

    def __init__(
        self,
        initial_per_gen: int = 10000,
        chiral_phase_rad: float = 1.15,
        eps_toy: float = 0.015,
        eps_cosmic: float = 1.002e-9,
    ):
        self.initial_per_gen = initial_per_gen
        self.chiral_phase_rad = chiral_phase_rad
        self.eps_toy = eps_toy
        self.eps_cosmic = eps_cosmic

    def _jarlskog_3d_invariant(self, n_gen: int) -> float:
        """Irreducible 3D chiral phase vanishes for N_gen < 3 and activates at N_gen == 3."""
        return 0.0 if n_gen < 3 else math.sin(self.chiral_phase_rad)

    def simulate_universe(self, n_gen: int, eps_3d: float = None) -> Dict[str, Any]:
        """Evolve an exact 50/50 matter/antimatter population through Gen 3 -> 2 -> 1 cascade."""
        if n_gen not in (1, 2, 3):
            raise ValueError("3D lattice supports 1, 2, or 3 orthogonal generations.")
        if eps_3d is None:
            eps_3d = self.eps_toy

        j_cp = self._jarlskog_3d_invariant(n_gen)
        matter = {g: float(self.initial_per_gen) for g in range(1, n_gen + 1)}
        anti = {g: float(self.initial_per_gen) for g in range(1, n_gen + 1)}
        total_initial = sum(matter.values()) + sum(anti.values())

        if n_gen == 3:
            bias_32 = eps_3d * j_cp
            matter[2] += matter[3] * (1.0 + bias_32)
            anti[2] += anti[3] * (1.0 - bias_32)
            matter[3], anti[3] = 0.0, 0.0

        if n_gen >= 2:
            bias_21 = 0.5 * eps_3d * j_cp
            matter[1] += matter[2] * (1.0 + bias_21)
            anti[1] += anti[2] * (1.0 - bias_21)
            matter[2], anti[2] = 0.0, 0.0

        annihilated_pairs = min(matter[1], anti[1])
        em_photons = 2.0 * annihilated_pairs
        surviving_matter = matter[1] - annihilated_pairs
        surviving_anti = anti[1] - annihilated_pairs
        eta_baryon = surviving_matter / em_photons if em_photons > 0 else 0.0

        return {
            "n_gen": n_gen,
            "j_cp": round(j_cp, 4),
            "initial_total": int(total_initial),
            "em_photons": round(em_photons, 1),
            "surviving_matter": round(surviving_matter, 6),
            "surviving_anti": round(surviving_anti, 6),
            "baryon_to_photon": eta_baryon,
        }

    def generation_node_loads(self, node_cap: float = 100.0) -> List[Dict[str, Any]]:
        """Check why 3 orthogonal axes allow 3 stable generations under the 100-tick node cap."""
        modes = [
            ("Gen 1 (u, d, e)", "1D Linear Hop", 18.0),
            ("Gen 2 (c, s, mu)", "2D Planar Turn", 44.0),
            ("Gen 3 (t, b, tau)", "3D Volumetric Twist", 82.0),
            ("Gen 4 (Hypothetical)", "Over-Cap Multi-Loop", 128.0),
        ]
        rows: List[Dict[str, Any]] = []
        for label, geom, ticks in modes:
            allowed = ticks <= node_cap
            rows.append({
                "generation": label,
                "geometry": geom,
                "ticks": ticks,
                "allowed": allowed,
                "status": "Allowed (< 100 cap)" if allowed else "BLOCKED / Fractures (> 100 cap)",
            })
        return rows


def run_baryogenesis_demo() -> None:
    sim = BCCBaryogenesisSim()
    print("=== PART 1: 50/50 Big Bang Cascade (Untuned Toy vs. Cosmic-Tuned eta ~ 6.1e-10) ===")
    print("N_gen  J_cp    Untuned Matter   Untuned eta   Cosmic Matter    Cosmic eta (PDG ~6.1e-10)")
    print("-" * 88)
    for n in (1, 2, 3):
        toy = sim.simulate_universe(n, eps_3d=sim.eps_toy)
        cos = sim.simulate_universe(n, eps_3d=sim.eps_cosmic)
        print(
            f"{n:>5} {toy['j_cp']:>6.4f} {toy['surviving_matter']:>17.2f} "
            f"{toy['baryon_to_photon']:>13.4e} {cos['surviving_matter']:>15.6f} "
            f"{cos['baryon_to_photon']:>16.4e}"
        )

    print("\n=== PART 2: 3D Orthogonal Axis Capacity & 100-Tick Node Cutoff ===")
    print("Generation             3D Routing Geometry     Tick Load   Lattice Status")
    print("-" * 78)
    for row in sim.generation_node_loads():
        print(f"{row['generation']:<22} {row['geometry']:<23} {row['ticks']:>9.1f}   {row['status']}")


if __name__ == "__main__":
    run_baryogenesis_demo()

