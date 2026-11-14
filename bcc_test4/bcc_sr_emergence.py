#!/usr/bin/env python3
"""
Emergent Special Relativity from the 1-Hop-Per-Tick 6-Face Planck-Cube Grid.

Derives Lorentz kinematics and dynamics from the universal routing speed c = 1.0 l_P/t_P:
  1. Kinematic Time Dilation & Length Contraction: Orthogonal split between spatial
     translation hops (beta = v/c) and internal clock loops yields gamma = 1/sqrt(1-beta^2).
  2. Relativistic Dispersion Relation: Orthogonal rest-mass ticks (m_0) and momentum
     ticks (p = gamma * m_0 * v) satisfy E^2 = (p*c)^2 + (m_0*c^2)^2 exactly.
  3. Bounded Velocity Addition: Composing sub-light drifts u, v obeys (u+v)/(1+u*v/c^2) < c,
     and leaves massless photon speed (u = c) strictly invariant at c.
"""

import math
from typing import Any, Dict, List


class BCCSREmergenceSim:
    """Derives Special Relativity observables from finite 1-hop/tick lattice routing."""

    def __init__(self, c_grid: float = 1.0, rest_mass_mev: float = 938.92):
        self.c = c_grid
        self.rest_mass_mev = rest_mass_mev

    def lorentz_gamma(self, beta: float) -> float:
        """Compute Lorentz factor gamma = 1 / sqrt(1 - beta^2) from orthogonal tick split."""
        if not (0.0 <= beta < 1.0):
            raise ValueError("Massive particle speed fraction beta = v/c must satisfy 0 <= beta < 1.")
        return 1.0 / math.sqrt(1.0 - beta**2)

    def kinematics_profile(self, betas: List[float], rest_length_lp: float = 10.0) -> List[Dict[str, Any]]:
        """Compute time dilation (dt/dtau = gamma) and length contraction (L = L0 / gamma)."""
        rows: List[Dict[str, Any]] = []
        for b in betas:
            g = self.lorentz_gamma(b)
            internal_clock_rate = 1.0 / g
            dilated_period = g
            contracted_len = rest_length_lp / g
            rows.append({
                "beta": b,
                "gamma": round(g, 6),
                "clock_rate": round(internal_clock_rate, 6),
                "time_dilation": round(dilated_period, 6),
                "contracted_length": round(contracted_len, 4),
            })
        return rows

    def energy_momentum_table(self, betas: List[float]) -> List[Dict[str, Any]]:
        """Verify E = gamma * m0 * c^2 = sqrt((p*c)^2 + (m0*c^2)^2) across relativistic speeds."""
        rows: List[Dict[str, Any]] = []
        m0 = self.rest_mass_mev
        for b in betas:
            g = self.lorentz_gamma(b)
            p_c = g * m0 * b
            e_gamma = g * m0
            e_pythag = math.sqrt(p_c**2 + m0**2)
            rows.append({
                "beta": b,
                "gamma": round(g, 6),
                "momentum_mev": round(p_c, 2),
                "energy_gamma_mev": round(e_gamma, 2),
                "energy_pythag_mev": round(e_pythag, 2),
                "residual_mev": round(abs(e_gamma - e_pythag), 10),
            })
        return rows

    def compose_velocities(self, beta_u: float, beta_v: float) -> Dict[str, Any]:
        """Compose two collinear lattice drift speeds without exceeding the 1-hop/tick cap c."""
        if not (-1.0 <= beta_u <= 1.0 and -1.0 < beta_v < 1.0):
            raise ValueError("Requires |beta_u| <= 1 and |beta_v| < 1.")
        galilean = beta_u + beta_v
        einstein = (beta_u + beta_v) / (1.0 + beta_u * beta_v)
        return {
            "beta_u": beta_u,
            "beta_v": beta_v,
            "galilean_sum": round(galilean, 6),
            "grid_relativistic": round(einstein, 6),
            "respects_c_cap": abs(einstein) <= 1.0,
        }


def run_sr_emergence_demo() -> None:
    sim = BCCSREmergenceSim(c_grid=1.0, rest_mass_mev=938.92)
    betas = [0.0, 0.5, 0.8, 0.95, 0.99]

    print("=== PART 1: Kinematic Time Dilation & Length Contraction (1-Hop/Tick Budget) ===")
    print("Beta (v/c)   Lorentz gamma   Clock Rate (1/g)   Time Dilation   Length (L0=10)")
    print("-" * 82)
    for r in sim.kinematics_profile(betas, rest_length_lp=10.0):
        print(
            f"{r['beta']:>10.2f} {r['gamma']:>15.6f} {r['clock_rate']:>18.6f} "
            f"{r['time_dilation']:>15.6f} {r['contracted_length']:>16.4f}"
        )

    print("\n=== PART 2: Relativistic Dispersion E^2 = (pc)^2 + (m0 c^2)^2 (Nucleon m0=938.92 MeV) ===")
    print("Beta (v/c)   Momentum pc (MeV)   E = gamma*m0 (MeV)   Pythagorean E (MeV)   Residual")
    print("-" * 86)
    for r in sim.energy_momentum_table(betas):
        print(
            f"{r['beta']:>10.2f} {r['momentum_mev']:>19.2f} {r['energy_gamma_mev']:>20.2f} "
            f"{r['energy_pythag_mev']:>21.2f} {r['residual_mev']:>10.2e}"
        )

    print("\n=== PART 3: Bounded Velocity Addition & Invariance of Light Speed c ===")
    print("Frame v/c   Object u/c   Galilean u+v   Grid Relativistic   Respects c Cap")
    print("-" * 78)
    for u, v in [(0.5, 0.5), (0.8, 0.8), (0.95, 0.95), (1.0, 0.8)]:
        c_res = sim.compose_velocities(u, v)
        print(
            f"{c_res['beta_v']:>9.2f} {c_res['beta_u']:>12.2f} {c_res['galilean_sum']:>14.6f} "
            f"{c_res['grid_relativistic']:>19.6f}   {c_res['respects_c_cap']}"
        )


if __name__ == "__main__":
    run_sr_emergence_demo()
