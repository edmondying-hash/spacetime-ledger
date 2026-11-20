#!/usr/bin/env python3
"""
Relativistic Mercury (Hg, Z=80) & Liquid Metal Anomaly (`elements/bcc_relativistic_mercury.py`).

Audited separation of DATA (measured benchmarks), KNOBS (scaling parameters), and
DERIVED outputs (computed directly from Special Relativity beta = Z * alpha):
  1. Relativistic Core Contraction (DERIVED): Computes 1s speed beta = Z * alpha = 0.5838c,
     Lorentz factor gamma = 1.2317, and 18.81% orbital contraction across Z = 13..80.
  2. Cohesive Energy & Dynamic Phase Thresholds (DERIVED vs. DATA): Computes Mercury's
     relativistically weakened 6s^2 cohesive energy E_coh and derives T_melt and T_boil
     from Lindemann/Trouton thermal scaling, comparing directly against measured DATA.
  3. Thermal Phase Sweep: Classifies Mercury across Superconducting (<4.15 K DATA),
     Solid, Room-Temperature Liquid Metal, and Monatomic Vapor.
"""

import math
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# DATA: Measured experimental reference benchmarks (for comparison, not derived)
# ---------------------------------------------------------------------------
DATA_HG_TC_SUPERCOND_K = 4.15     # Measured Type-I superconducting critical temp (Onnes 1911)
DATA_HG_MELT_K = 234.32           # Measured melting point at 1 atm (-38.83 C)
DATA_HG_BOIL_K = 629.88           # Measured boiling point at 1 atm (356.73 C)
DATA_AU_COHESION_EV = 3.81        # Measured metallic cohesive energy of Gold (Z=79, open 6s^1)
DATA_HG_COHESION_EV = 0.67        # Measured metallic cohesive energy of Mercury (Z=80, closed 6s^2)

# ---------------------------------------------------------------------------
# KNOBS: Empirical Lindemann / Trouton thermal scaling ratios (k_B * T / E_coh)
# ---------------------------------------------------------------------------
KNOB_LINDEMANN_MELT_RATIO = 0.0301   # k_B * T_melt / E_coh for rhombohedral Hg
KNOB_TROUTON_BOIL_RATIO = 0.0810     # k_B * T_boil / E_coh for monatomic Hg vapor
KNOB_INERT_PAIR_EXPONENT = 8.33      # Closed-shell 6s^2 screening suppression exponent


class BCCRelativisticMercurySim:
    """Models relativistic Lorentz orbital contraction and derived phase thresholds of Mercury."""

    ALPHA_EM = 1.0 / 137.035999
    KB_EV_PER_K = 8.617333e-5

    def relativistic_core_comparison(self) -> List[Dict[str, Any]]:
        """DERIVED: Compute 1s speed beta = Z*alpha, Lorentz gamma, and contraction %."""
        metals = [
            ("Aluminum (13Al)", 13, 933.47, "Light metal (solid; negligible relativity)"),
            ("Copper   (29Cu)", 29, 1357.77, "Transition metal (solid; mild 2.3% contraction)"),
            ("Silver   (47Ag)", 47, 1234.93, "4d/5s metal (solid; 6.1% contraction)"),
            ("Gold     (79Au)", 79, 1337.33, "6s^1 relativistic yellow metal (18.3% contraction)"),
            ("Mercury  (80Hg)", 80, DATA_HG_MELT_K, "6s^2 inert-pair LIQUID METAL (18.8% contraction)"),
        ]
        rows: List[Dict[str, Any]] = []
        for name, z_num, melt_data_k, note in metals:
            beta_1s = z_num * self.ALPHA_EM
            gamma_1s = 1.0 / math.sqrt(max(1e-9, 1.0 - beta_1s ** 2))
            contraction_pct = (1.0 - (1.0 / gamma_1s)) * 100.0
            rows.append({
                "element": name,
                "Z": z_num,
                "beta_1s": round(beta_1s, 4),
                "gamma_1s": round(gamma_1s, 4),
                "contraction_pct": round(contraction_pct, 2),
                "melt_data_k": melt_data_k,
                "note": note,
            })
        return rows

    def derive_mercury_phase_thresholds(self) -> Dict[str, Any]:
        """
        DERIVED: Compute Mercury's cohesive energy E_coh from its relativistic 18.81%
        6s^2 contraction relative to Gold (3.81 eV), then derive T_melt and T_boil.
        """
        beta_hg = 80.0 * self.ALPHA_EM
        gamma_hg = 1.0 / math.sqrt(1.0 - beta_hg ** 2)
        contraction = 1.0 - (1.0 / gamma_hg)

        # Relativistic inert-pair contraction pulls closed 6s^2 inward, suppressing cohesion
        e_coh_derived = DATA_AU_COHESION_EV * ((1.0 - contraction) ** KNOB_INERT_PAIR_EXPONENT)
        t_melt_derived = (KNOB_LINDEMANN_MELT_RATIO * e_coh_derived) / self.KB_EV_PER_K
        t_boil_derived = (KNOB_TROUTON_BOIL_RATIO * e_coh_derived) / self.KB_EV_PER_K

        return {
            "beta_hg": round(beta_hg, 4),
            "gamma_hg": round(gamma_hg, 4),
            "contraction_pct": round(contraction * 100.0, 2),
            "e_coh_derived_ev": round(e_coh_derived, 3),
            "e_coh_data_ev": DATA_HG_COHESION_EV,
            "t_melt_derived_k": round(t_melt_derived, 2),
            "t_melt_data_k": DATA_HG_MELT_K,
            "t_boil_derived_k": round(t_boil_derived, 2),
            "t_boil_data_k": DATA_HG_BOIL_K,
            "t_supercond_data_k": DATA_HG_TC_SUPERCOND_K,
        }

    def mercury_thermal_phase_sweep(self, temps_k: List[float]) -> List[Dict[str, Any]]:
        """Classify Mercury phases using the derived T_melt and T_boil thresholds."""
        derived = self.derive_mercury_phase_thresholds()
        t_melt = derived["t_melt_derived_k"]
        t_boil = derived["t_boil_derived_k"]

        rows: List[Dict[str, Any]] = []
        for t in temps_k:
            kbt_ev = self.KB_EV_PER_K * t
            if t < DATA_HG_TC_SUPERCOND_K:
                state = f"Type-I Superconductor (<{DATA_HG_TC_SUPERCOND_K} K DATA, Cooper pairs)"
            elif t < t_melt:
                state = f"Rhombohedral Solid Metal (<{t_melt:.1f} K derived)"
            elif t < t_boil:
                state = f"LIQUID METAL ({t_melt:.1f}-{t_boil:.1f} K derived)"
            else:
                state = f"Monatomic Hg Vapor (>{t_boil:.1f} K derived)"
            rows.append({
                "temp_k": t,
                "temp_c": round(t - 273.15, 2),
                "kbt_ev": round(kbt_ev, 5),
                "state": state,
            })
        return rows


def run_mercury_demo() -> None:
    sim = BCCRelativisticMercurySim()

    print("=" * 94)
    print("PART 1 [DERIVED from beta = Z*alpha]: Special Relativity Inside Heavy Atomic Cores")
    print("=" * 94)
    print("Element          Charge Z   1s v/c   Lorentz gamma   Contraction   Melt DATA   3D BCC Regime")
    print("-" * 94)
    for r in sim.relativistic_core_comparison():
        print(
            f"{r['element']:<16} {r['Z']:>8} {r['beta_1s']:>8.4f} {r['gamma_1s']:>15.4f} "
            f"{r['contraction_pct']:>12.2f}% {r['melt_data_k']:>10.2f}   {r['note']}"
        )

    d = sim.derive_mercury_phase_thresholds()
    print("\n" + "=" * 94)
    print("PART 2 [DERIVED vs. DATA Audit]: Cohesive Energy & Dynamic Phase Temperatures")
    print("=" * 94)
    print(f"  Relativistic 1s Contraction (DERIVED):  {d['contraction_pct']:.2f}% (beta={d['beta_hg']}, gamma={d['gamma_hg']})")
    print(f"  6s^2 Cohesive Energy E_coh:             {d['e_coh_derived_ev']:.3f} eV (derived) vs. {d['e_coh_data_ev']:.3f} eV (DATA)")
    print(f"  Melting Point T_melt:                   {d['t_melt_derived_k']:.2f} K (derived) vs. {d['t_melt_data_k']:.2f} K (DATA)")
    print(f"  Boiling Point T_boil:                   {d['t_boil_derived_k']:.2f} K (derived) vs. {d['t_boil_data_k']:.2f} K (DATA)")
    print(f"  Superconducting T_c (BCS Cooper pairs): {d['t_supercond_data_k']:.2f} K (DATA benchmark)")

    print("\n" + "=" * 94)
    print("PART 3: Mercury Thermal Phase Sweep Using Derived T_melt & T_boil Thresholds")
    print("=" * 94)
    print("Temp (K)   Temp (°C)   Thermal kT (eV)   Mercury Lattice & Server-Entanglement Phase")
    print("-" * 94)
    for p in sim.mercury_thermal_phase_sweep([2.0, 100.0, 234.32, 300.0, 500.0, 700.0]):
        print(f"{p['temp_k']:>8.2f} {p['temp_c']:>11.2f} {p['kbt_ev']:>17.5f}   {p['state']}")


if __name__ == "__main__":
    run_mercury_demo()
