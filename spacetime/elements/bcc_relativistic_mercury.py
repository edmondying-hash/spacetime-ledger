#!/usr/bin/env python3
"""
Relativistic Mercury (Hg, Z=80) & Liquid Metal Anomaly (`elements/bcc_relativistic_mercury.py`).

Unifies Special Relativity (sr/ Lorentz contraction gamma = 1/sqrt(1 - beta^2)) with
multi-electron atomic shells (elements/):
  1. Relativistic Inner-Shell Velocity (beta = Z * alpha): Shows how Mercury's Z=80
     nuclear charge accelerates 1s electrons to 0.584c (gamma = 1.232), contracting
     orbital radii by 18.8% compared to non-relativistic Bohr scaling.
  2. Relativistic 6s^2 Inert-Pair Stabilization: Compares Z=47 Silver (Ag), Z=79 Gold (Au),
     and Z=80 Mercury (Hg) to show why relativistic contraction pulls Hg's closed 6s^2
     shell inward (10.44 eV ionization), starving metallic bond cohesion.
  3. Room-Temperature Liquid Metal & 4.15 K Superconductivity: Tracks Solid (<234.3 K),
     Liquid Metal (234.3-629.9 K), Gas (>629.9 K), and Cooper-pair Superconductor (<4.15 K).
"""

import math
from typing import Any, Dict, List


class BCCRelativisticMercurySim:
    """Models relativistic Lorentz orbital contraction and liquid-metal phases of Mercury."""

    ALPHA_EM = 1.0 / 137.035999
    KB_EV_PER_K = 8.617333e-5

    def relativistic_core_comparison(self) -> List[Dict[str, Any]]:
        """
        Compare 1s orbital speed fraction beta = Z * alpha, Lorentz factor gamma,
        and relativistic orbital contraction (1 - 1/gamma) across light vs. heavy metals.
        """
        metals = [
            ("Aluminum (13Al)", 13, 933.47, "Light metal (solid; negligible relativity)"),
            ("Copper   (29Cu)", 29, 1357.77, "Transition metal (solid; mild 2.3% contraction)"),
            ("Silver   (47Ag)", 47, 1234.93, "4d/5s metal (solid; 6.1% contraction)"),
            ("Gold     (79Au)", 79, 1337.33, "6s^1 relativistic yellow metal (18.3% contraction)"),
            ("Mercury  (80Hg)", 80, 234.32, "6s^2 inert-pair LIQUID METAL (18.8% contraction)"),
        ]
        rows: List[Dict[str, Any]] = []
        for name, z_num, melt_k, note in metals:
            beta_1s = z_num * self.ALPHA_EM
            gamma_1s = 1.0 / math.sqrt(max(1e-9, 1.0 - beta_1s ** 2))
            contraction_pct = (1.0 - (1.0 / gamma_1s)) * 100.0
            rows.append({
                "element": name,
                "Z": z_num,
                "beta_1s": round(beta_1s, 4),
                "gamma_1s": round(gamma_1s, 4),
                "contraction_pct": round(contraction_pct, 2),
                "melt_k": melt_k,
                "note": note,
            })
        return rows

    def gold_vs_mercury_valence(self) -> List[Dict[str, Any]]:
        """
        Contrast Z=79 Gold (half-filled 6s^1 -> strong covalent-metallic bond, melts 1337 K)
        against Z=80 Mercury (closed relativistic 6s^2 -> weak van der Waals metal, melts 234 K).
        """
        return [
            {
                "element": "Gold (79Au)",
                "valence": "[Xe] 4f^14 5d^10 6s^1",
                "first_ion_ev": 9.23,
                "cohesion_ev_atom": 3.81,
                "melt_k": 1337.33,
                "boil_k": 3129.00,
                "mechanism": "Unpaired 6s^1 + expanded 5d form strong Au-Au bonds",
            },
            {
                "element": "Mercury (80Hg)",
                "valence": "[Xe] 4f^14 5d^10 6s^2",
                "first_ion_ev": 10.44,
                "cohesion_ev_atom": 0.67,
                "melt_k": 234.32,
                "boil_k": 629.88,
                "mechanism": "Relativistically contracted closed 6s^2 acts like pseudo-noble gas",
            },
        ]

    def mercury_thermal_phase_sweep(self, temps_k: List[float]) -> List[Dict[str, Any]]:
        """Track Mercury across Superconducting (<4.15 K), Solid, Liquid Metal (300 K), and Gas."""
        rows: List[Dict[str, Any]] = []
        for t in temps_k:
            kbt_ev = self.KB_EV_PER_K * t
            if t < 4.15:
                state = "Type-I Superconductor (server Cooper pairs, R=0)"
            elif t < 234.32:
                state = "Rhombohedral Solid Metal (weak 6s^2 crystal)"
            elif t < 629.88:
                state = "LIQUID METAL (relativistically decoupled 6s^2)"
            else:
                state = "Monatomic Hg Vapor (free neutral atoms)"
            rows.append({
                "temp_k": t,
                "temp_c": round(t - 273.15, 2),
                "kbt_ev": round(kbt_ev, 5),
                "state": state,
            })
        return rows


def run_mercury_demo() -> None:
    sim = BCCRelativisticMercurySim()

    print("=" * 92)
    print("PART 1: Special Relativity Inside Heavy Atoms (beta = Z*alpha -> Lorentz Contraction)")
    print("=" * 92)
    print("Element          Charge Z   1s v/c   Lorentz gamma   Contraction   Melt (K)   3D BCC Regime")
    print("-" * 92)
    for r in sim.relativistic_core_comparison():
        print(
            f"{r['element']:<16} {r['Z']:>8} {r['beta_1s']:>8.4f} {r['gamma_1s']:>15.4f} "
            f"{r['contraction_pct']:>12.2f}% {r['melt_k']:>10.2f}   {r['note']}"
        )

    print("\n" + "=" * 92)
    print("PART 2: Why Gold (Z=79) Melts at 1,337 K While Neighbor Mercury (Z=80) Melts at 234 K")
    print("=" * 92)
    print("Element         Valence Shell          Ioniz (eV)   Cohesion   Melt (K)   BCC Bonding Behavior")
    print("-" * 92)
    for g in sim.gold_vs_mercury_valence():
        print(
            f"{g['element']:<15} {g['valence']:<22} {g['first_ion_ev']:>10.2f} "
            f"{g['cohesion_ev_atom']:>8.2f}eV {g['melt_k']:>10.2f}   {g['mechanism']}"
        )

    print("\n" + "=" * 92)
    print("PART 3: Mercury Thermal Phase Sweep (2 K Superconductor -> 300 K Liquid -> 700 K Gas)")
    print("=" * 92)
    print("Temp (K)   Temp (°C)   Thermal kT (eV)   Mercury Lattice & Server-Entanglement Phase")
    print("-" * 92)
    for p in sim.mercury_thermal_phase_sweep([2.0, 100.0, 234.32, 300.0, 500.0, 700.0]):
        print(f"{p['temp_k']:>8.2f} {p['temp_c']:>11.2f} {p['kbt_ev']:>17.5f}   {p['state']}")


if __name__ == "__main__":
    run_mercury_demo()
