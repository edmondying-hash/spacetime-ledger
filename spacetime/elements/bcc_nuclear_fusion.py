#!/usr/bin/env python3
"""
Nuclear Fusion on the 3D BCC (8-Diagonal) Lattice (`elements/bcc_nuclear_fusion.py`).

Unifies virtual-photon Coulomb repulsion, short-range pion/gluon Steiner tree merging,
Dirac-4 quantum barrier tunneling, and the D-T vs. p-p weak-bottleneck rate gap:
  1. Approach Potential Profile (12.0 fm -> 0.8 fm): Plots repulsive 1/r virtual-photon
     Coulomb energy against attractive short-range Yukawa pion + gluon Steiner merge.
  2. Thermal Tunneling Sweep (10M K -> 200M K): Computes thermal kinetic energy k_B*T,
     Gamow quantum tunneling probability, and relative fusion reactivity across stellar
     core (15M K) and tokamak reactor (150M K) temperatures.
  3. Reaction Channel Comparison (p-p vs. D-D vs. D-T): Quantifies the mass-defect
     workload release (Q-value in MeV & BCC ticks) and shows why D-T fuses ~10^25x
     faster than pure Hydrogen by avoiding a virtual W+ weak boson transition.
"""

import math
from typing import Any, Dict, List


class BCCNuclearFusionSim:
    """Models nuclear barrier tunneling and gluon Steiner tree fusion on the 3D BCC grid."""

    KB_KEV_PER_K = 8.617333e-8   # Boltzmann constant (keV / K)
    E2_4PI_EPS0_MEV_FM = 1.43996 # Coulomb constant e^2 / (4 * pi * eps0) in MeV * fm
    TICK_TO_MEV = 5.0

    def barrier_potential_profile(self, radii_fm: List[float]) -> List[Dict[str, Any]]:
        """
        Compute net interaction potential V(r) = V_coulomb(r) + V_strong(r) in MeV
        for two singly-charged nuclei (Z1 = Z2 = 1) approaching from 12 fm to 0.8 fm.
        """
        rows: List[Dict[str, Any]] = []
        # Strong nuclear potential: attractive Yukawa pion well (r_pi = 1.41 fm) + hard-core repulsion
        v0_pion_mev = -42.0
        r_pi_fm = 1.41

        for r in radii_fm:
            v_coul = self.E2_4PI_EPS0_MEV_FM / max(0.5, r)
            if r > 2.2:
                # Outside strong-force range: pure 1/r virtual-photon repulsion
                v_strong = v0_pion_mev * math.exp(-(r - 1.5) / r_pi_fm) * 0.25
            else:
                # Inside 2.2 fm: virtual pion overlap & gluon Steiner tree merge into He-4 well
                well = v0_pion_mev * math.exp(-((r - 1.1) ** 2) / 0.85)
                core_repel = 18.0 * math.exp(-(r - 0.5) / 0.25) if r < 0.9 else 0.0
                v_strong = well + core_repel

            v_net = v_coul + v_strong
            regime = (
                "FUSED He-4 Gluon Core (Bound)"
                if v_net < -5.0
                else ("Coulomb Barrier Peak (Tunneling Zone)" if v_net > 0.35 else "1/r Virtual-Photon Repulsion")
            )
            rows.append({
                "r_fm": r,
                "v_coulomb_mev": round(v_coul, 4),
                "v_strong_mev": round(v_strong, 4),
                "v_net_mev": round(v_net, 4),
                "regime": regime,
            })
        return rows

    def thermal_tunneling_sweep(self, temps_million_k: List[float]) -> List[Dict[str, Any]]:
        """
        Compute thermal energy k_B*T, Gamow quantum tunneling factor, and relative D-T
        reactivity across 10M K (red dwarf) -> 15M K (Sun) -> 150M K (tokamak).
        """
        # Gamow energy for D-T: E_G = 1183 keV (reduced mass mu = 1.2 u)
        e_gamow_kev = 1183.0
        rows: List[Dict[str, Any]] = []

        raw_rates: List[float] = []
        temp_data: List[Dict[str, Any]] = []

        for t_mk in temps_million_k:
            t_k = t_mk * 1.0e6
            kbt_kev = self.KB_KEV_PER_K * t_k
            # Optimal Gamow peak collision energy E_0 = (E_G * (kT)^2 / 4)^(1/3)
            e0_kev = ((e_gamow_kev * (kbt_kev ** 2)) / 4.0) ** (1.0 / 3.0)
            # Tunneling exponent tau = 3 * E_0 / kT
            tau = (3.0 * e0_kev) / max(1e-9, kbt_kev)
            tunnel_prob = math.exp(-tau)
            # Bosch-Hale style relative reactivity proxy ~ tau^2 * exp(-tau)
            rel_rate = (tau ** 2) * tunnel_prob
            raw_rates.append(rel_rate)
            temp_data.append({
                "temp_mk": t_mk,
                "kbt_kev": round(kbt_kev, 3),
                "gamow_peak_kev": round(e0_kev, 2),
                "tunnel_prob": tunnel_prob,
                "raw_rate": rel_rate,
            })

        max_rate = max(raw_rates) if raw_rates else 1.0
        for item in temp_data:
            norm_rate = item["raw_rate"] / max_rate
            if item["temp_mk"] < 20.0:
                env = "Solar Core (15M K — slow stellar burn)"
            elif item["temp_mk"] < 80.0:
                env = "Sub-Ignition Plasma (heating regime)"
            elif item["temp_mk"] <= 180.0:
                env = "Tokamak Peak Ignition (100-150M K)"
            else:
                env = "Over-Heated Plasma (thermal spread)"

            rows.append({
                "temp_mk": item["temp_mk"],
                "kbt_kev": item["kbt_kev"],
                "gamow_peak_kev": item["gamow_peak_kev"],
                "tunnel_prob": item["tunnel_prob"],
                "norm_reactivity": round(norm_rate, 4),
                "environment": env,
            })
        return rows

    def reaction_channels(self) -> List[Dict[str, Any]]:
        """
        Compare p-p, D-D, and D-T fusion channels in terms of mass-defect Q-value (MeV),
        freed BCC routing ticks, and weak-force bottleneck factor.
        """
        channels = [
            {
                "reaction": "p + p -> D + e+ + nu_e",
                "q_mev": 0.42,
                "weak_step": "YES (W+ quark flip)",
                "rel_cross_section": "1.0e-25 (Solar bottleneck)",
                "products": "Deuteron + Positron + Neutrino",
            },
            {
                "reaction": "D + D -> He-3 + n (50%)",
                "q_mev": 3.27,
                "weak_step": "No (Pure strong merge)",
                "rel_cross_section": "1.5e-2  (Needs ~400M K)",
                "products": "Helium-3 (0.82) + Neutron (2.45)",
            },
            {
                "reaction": "D + D -> T + p (50%)",
                "q_mev": 4.03,
                "weak_step": "No (Pure strong merge)",
                "rel_cross_section": "1.5e-2  (Needs ~400M K)",
                "products": "Triton (1.01) + Proton (3.02)",
            },
            {
                "reaction": "D + T -> He-4 + n",
                "q_mev": 17.59,
                "weak_step": "No (Direct He-4 core)",
                "rel_cross_section": "1.00    (Optimal 150M K fuel)",
                "products": "Alpha He-4 (3.52) + Neutron (14.07)",
            },
        ]
        for ch in channels:
            ch["freed_bcc_ticks"] = round(ch["q_mev"] / self.TICK_TO_MEV, 3)
        return channels


def run_fusion_demo() -> None:
    sim = BCCNuclearFusionSim()

    print("=" * 92)
    print("PART 1: Nuclear Approach Potential (1/r Virtual-Photon Wall vs. Gluon Steiner Merge)")
    print("=" * 92)
    print("Dist (fm)   Coulomb (MeV)   Strong/Pion (MeV)   Net V(r) (MeV)   3D BCC Interaction Regime")
    print("-" * 92)
    for r in sim.barrier_potential_profile([10.0, 5.0, 3.0, 2.2, 1.8, 1.4, 1.1, 0.8]):
        print(
            f"{r['r_fm']:>9.1f} {r['v_coulomb_mev']:>+15.4f} {r['v_strong_mev']:>+19.4f} "
            f"{r['v_net_mev']:>+16.4f}   {r['regime']}"
        )

    print("\n" + "=" * 92)
    print("PART 2: Thermal Quantum Tunneling Sweep (15M K Solar Core -> 150M K Tokamak Ignition)")
    print("=" * 92)
    print("Temp (MK)   kT (keV)   Gamow Peak (keV)   Tunnel Prob   Rel Rate   Fusion Environment")
    print("-" * 92)
    for t in sim.thermal_tunneling_sweep([15.0, 30.0, 60.0, 100.0, 150.0, 200.0]):
        print(
            f"{t['temp_mk']:>9.1f} {t['kbt_kev']:>10.3f} {t['gamow_peak_kev']:>18.2f} "
            f"{t['tunnel_prob']:>13.3e} {t['norm_reactivity']:>10.4f}   {t['environment']}"
        )

    print("\n" + "=" * 92)
    print("PART 3: Hydrogen Isotope Fusion Channels (Workload Q-Value & Weak-Boson Bottleneck)")
    print("=" * 92)
    print("Reaction Channel          Q (MeV)   BCC Ticks   Weak Boson?              Relative Rate")
    print("-" * 92)
    for ch in sim.reaction_channels():
        print(
            f"{ch['reaction']:<25} {ch['q_mev']:>7.2f} {ch['freed_bcc_ticks']:>11.3f}   "
            f"{ch['weak_step']:<24} {ch['rel_cross_section']}"
        )


if __name__ == "__main__":
    run_fusion_demo()
