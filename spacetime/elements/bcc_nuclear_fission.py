#!/usr/bin/env python3
"""
Nuclear Fission & Chain Reaction Kinetics on the 3D BCC Lattice (`elements/bcc_nuclear_fission.py`).

Models heavy-nucleus Coulomb-vs.-Strong instability, zero-barrier thermal neutron capture,
mass-defect workload release, and neutron multiplication factor k_eff:
  1. Nuclear Binding Curve (H-2 -> He-4 -> Fe-56 Peak -> U-235): Shows short-range
     pion/gluon saturation vs. long-range Z^2 virtual-photon repulsion driving heavy
     nuclei past Iron-56 toward fission instability.
  2. Thermal Neutron Capture & Split (n + U-235 -> Ba-141 + Kr-92 + 3n + 202.5 MeV):
     Quantifies the 0.025 eV zero-Coulomb neutron trigger, barrier clearance, and
     freed BCC routing ticks (~40.5 ticks per split).
  3. Chain Reaction Multiplication Sweep (k_eff): Tracks neutron population across
     subcritical (k=0.85), critical steady-state (k=1.00), and supercritical (k=1.15) grids.
"""

from typing import Any, Dict, List


class BCCNuclearFissionSim:
    """Models heavy-core Coulomb instability and neutron-induced fission on the 3D BCC grid."""

    TICK_TO_MEV = 5.0

    def binding_curve_comparison(self) -> List[Dict[str, Any]]:
        """
        Compare binding energy per nucleon across the nuclear stability curve from
        light fusion fuel up to the Fe-56 peak and heavy fissile U-235.
        """
        isotopes = [
            ("Deuterium (2H)", 2, 1, 2.22, "Fusion fuel (climbs toward Fe-56)"),
            ("Helium-4 (4He)", 4, 2, 28.30, "Alpha magic core (tight light cluster)"),
            ("Carbon-12 (12C)", 12, 6, 92.16, "Triple-alpha core"),
            ("Iron-56 (56Fe)", 56, 26, 492.26, "PEAK STABILITY (8.79 MeV/nucleon)"),
            ("Krypton-92 (92Kr)", 92, 36, 783.18, "Fission daughter fragment (~8.51 MeV/nuc)"),
            ("Barium-141 (141Ba)", 141, 56, 1173.98, "Fission daughter fragment (~8.33 MeV/nuc)"),
            ("Uranium-235 (235U)", 235, 92, 1783.87, "Over-charged Z=92 core (fissile cliff)"),
        ]
        rows: List[Dict[str, Any]] = []
        for name, a_num, z_num, b_tot, role in isotopes:
            b_per_nuc = b_tot / a_num
            # Relative long-range Z(Z-1) Coulomb stress per nucleon
            coulomb_stress = (z_num * (z_num - 1)) / float(a_num)
            rows.append({
                "isotope": name,
                "A": a_num,
                "Z": z_num,
                "binding_per_nuc": round(b_per_nuc, 3),
                "coulomb_stress": round(coulomb_stress, 2),
                "role": role,
            })
        return rows

    def simulate_u235_split(self) -> Dict[str, Any]:
        """
        Compute exact routing workload release when a 0.025 eV thermal neutron splits
        U-235 into Ba-141 + Kr-92 + 3 prompt neutrons.
        """
        b_u235 = 1783.87
        b_ba141 = 1173.98
        b_kr92 = 783.18
        # Binding energy after split minus before split = freed kinetic + radiation energy
        q_total_mev = (b_ba141 + b_kr92) - b_u235
        # Typical fission energy budget breakdown (MeV)
        breakdown = [
            ("Fission Fragments (Ba-141 + Kr-92)", 168.0, "Coulomb snap recoil of daughter cores"),
            ("Prompt Neutrons (avg 2.43 n/split)", 4.8, "Uncharged Q_EM=0 chain-reaction carriers"),
            ("Prompt Gamma Photons", 7.2, "De-excitation virtual-to-real photon burst"),
            ("Beta Decay + Neutrinos (delayed)", 22.5, "Weak W- quark flips toward stability"),
        ]
        items: List[Dict[str, Any]] = []
        for label, mev, desc in breakdown:
            items.append({
                "channel": label,
                "energy_mev": round(mev, 2),
                "bcc_ticks": round(mev / self.TICK_TO_MEV, 3),
                "mechanism": desc,
            })
        return {
            "reaction": "n (0.025 eV) + U-235 -> U-236* -> Ba-141 + Kr-92 + 3n",
            "capture_excitation_mev": 6.54,
            "fission_barrier_mev": 5.70,
            "q_total_mev": round(q_total_mev, 2),
            "freed_bcc_ticks": round(q_total_mev / self.TICK_TO_MEV, 2),
            "channels": items,
        }

    def chain_reaction_generations(
        self, generations: int = 8, initial_neutrons: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Track neutron population N_g = N_0 * (k_eff)^g across subcritical (0.85),
        critical power-plant steady state (1.00), and supercritical (1.18) regimes.
        """
        rows: List[Dict[str, Any]] = []
        for g in range(generations + 1):
            n_sub = initial_neutrons * (0.85 ** g)
            n_crit = initial_neutrons * (1.00 ** g)
            n_super = initial_neutrons * (1.18 ** g)
            power_mw = (n_crit / initial_neutrons) * 1000.0  # 1,000 MW steady baseline at k=1.00
            rows.append({
                "gen": g,
                "subcritical_k085": round(n_sub, 1),
                "critical_k100": round(n_crit, 1),
                "supercritical_k118": round(n_super, 1),
                "steady_power_mw": round(power_mw, 1),
            })
        return rows


def run_fission_demo() -> None:
    sim = BCCNuclearFissionSim()

    print("=" * 92)
    print("PART 1: Nuclear Binding Curve (Fusion Climb -> Fe-56 Peak -> U-235 Fission Cliff)")
    print("=" * 92)
    print("Isotope              Mass A   Charge Z   Bind/Nuc (MeV)   Z^2/A Stress   3D BCC Regime")
    print("-" * 92)
    for r in sim.binding_curve_comparison():
        print(
            f"{r['isotope']:<20} {r['A']:>6} {r['Z']:>10} {r['binding_per_nuc']:>16.3f} "
            f"{r['coulomb_stress']:>14.2f}   {r['role']}"
        )

    split = sim.simulate_u235_split()
    print("\n" + "=" * 92)
    print(f"PART 2: Thermal Neutron Split ({split['reaction']})")
    print(
        f"Capture Excitation = +{split['capture_excitation_mev']:.2f} MeV > "
        f"Barrier ({split['fission_barrier_mev']:.2f} MeV) -> "
        f"Released = {split['q_total_mev']:.2f} MeV ({split['freed_bcc_ticks']:.2f} BCC ticks)"
    )
    print("=" * 92)
    print("Energy Release Channel               Energy (MeV)   BCC Ticks   Lattice Mechanism")
    print("-" * 92)
    for ch in split["channels"]:
        print(
            f"{ch['channel']:<36} {ch['energy_mev']:>12.2f} {ch['bcc_ticks']:>11.3f}   {ch['mechanism']}"
        )

    print("\n" + "=" * 92)
    print("PART 3: Neutron Chain-Reaction Multiplication (k_eff = 0.85 vs. 1.00 vs. 1.18)")
    print("=" * 92)
    print("Generation   Subcritical (k=0.85)   Critical Reactor (k=1.00)   Supercritical (k=1.18)")
    print("-" * 92)
    for g in sim.chain_reaction_generations(generations=8, initial_neutrons=100):
        print(
            f"{g['gen']:>10} {g['subcritical_k085']:>22.1f} {g['critical_k100']:>27.1f} "
            f"{g['supercritical_k118']:>24.1f}"
        )


if __name__ == "__main__":
    run_fission_demo()
