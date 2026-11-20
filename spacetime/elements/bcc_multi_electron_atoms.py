#!/usr/bin/env python3
"""
Multi-Electron Atoms on the 3D BCC Lattice: Helium (He) & Carbon (C) vs. Hydrogen (H).

Models nuclear pion-exchange binding, Pauli-exclusion electron shell filling (1s^2 vs.
1s^2 2s^2 2p^2), Slater nuclear charge screening (Z_eff), and macroscopic phase behavior:
  1. Nuclear Core & Mass Defect: Compares H-1 (unpaired p+), He-4 (28.30 MeV alpha core),
     and C-12 (92.16 MeV triple-alpha core) in MeV and freed BCC routing ticks.
  2. Pauli Shell Stacking & Screening (Z_eff): Computes inner-shell shielding, effective
     nuclear charge Z_eff, atomic radius (Angstroms), and first ionization energy (eV).
  3. Valence Connectivity & Phase Extremes: Explains why 0-valence closed-shell He-4 boils
     at 4.22 K (and turns superfluid below 2.17 K) while 4-valence tetrahedral Carbon stays
     solid up to 3,915 K.
"""

from typing import Any, Dict, List


class BCCMultiElectronSim:
    """Models multi-nucleon binding and Pauli-excluded electron shells on the 3D BCC grid."""

    TICK_TO_MEV = 5.0
    BOHR_ANG = 0.529177
    RYDBERG_EV = 13.605693
    PROTON_MEV = 938.272
    NEUTRON_MEV = 939.565
    ELECTRON_MEV = 0.511

    def nuclear_core_table(self) -> List[Dict[str, Any]]:
        """Compare nucleon count, pion-exchange binding defect, and BCC tick savings."""
        nuclei = [
            {"element": "Hydrogen (1H)", "Z": 1, "N": 0, "binding_mev": 0.00},
            {"element": "Helium-4 (4He)", "Z": 2, "N": 2, "binding_mev": 28.30},
            {"element": "Carbon-12 (12C)", "Z": 6, "N": 6, "binding_mev": 92.16},
        ]
        rows: List[Dict[str, Any]] = []
        for nuc in nuclei:
            a_mass = nuc["Z"] + nuc["N"]
            raw_mev = (
                nuc["Z"] * (self.PROTON_MEV + self.ELECTRON_MEV)
                + nuc["N"] * self.NEUTRON_MEV
            )
            bound_mev = raw_mev - nuc["binding_mev"]
            bind_per_nuc = nuc["binding_mev"] / a_mass
            saved_ticks = nuc["binding_mev"] / self.TICK_TO_MEV
            rows.append({
                "element": nuc["element"],
                "nucleons": a_mass,
                "binding_mev": round(nuc["binding_mev"], 2),
                "mev_per_nucleon": round(bind_per_nuc, 3),
                "saved_bcc_ticks": round(saved_ticks, 3),
                "bound_mass_mev": round(bound_mev, 2),
            })
        return rows

    def electron_shell_screening(self) -> List[Dict[str, Any]]:
        """
        Compute Pauli shell occupancy, inner-electron Slater screening sigma, effective
        nuclear charge Z_eff = Z - sigma, valence radius, and 1st ionization energy.
        """
        atoms = [
            {
                "symbol": "H  (Z=1)",
                "config": "1s^1 (1 unpaired)",
                "n_outer": 1,
                "z": 1.0,
                "sigma": 0.00,       # Single electron: zero screening
                "open_bonds": 1,
                "ion_ev": 13.61,
            },
            {
                "symbol": "He (Z=2)",
                "config": "1s^2 (closed pair)",
                "n_outer": 1,
                "z": 2.0,
                "sigma": 0.31,       # Same-shell 1s partner screens ~0.31e
                "open_bonds": 0,
                "ion_ev": 24.59,
            },
            {
                "symbol": "C  (Z=6)",
                "config": "1s^2 2s^2 2p^2",
                "n_outer": 2,
                "z": 6.0,
                "sigma": 2.75,       # 2 inner 1s electrons (~1.70) + 3 outer 2s/2p (~1.05)
                "open_bonds": 4,
                "ion_ev": 11.26,
            },
        ]
        rows: List[Dict[str, Any]] = []
        for a in atoms:
            z_eff = a["z"] - a["sigma"]
            # Valence orbital radius r = (n^2 / Z_eff) * a_0
            r_ang = ((a["n_outer"] ** 2) / z_eff) * self.BOHR_ANG
            rows.append({
                "symbol": a["symbol"],
                "config": a["config"],
                "z_eff": round(z_eff, 2),
                "radius_ang": round(r_ang, 3),
                "ion_ev": a["ion_ev"],
                "open_bonds": a["open_bonds"],
            })
        return rows

    def macroscopic_phase_comparison(self) -> List[Dict[str, Any]]:
        """Contrast bond energy, boiling/sublimation point, and quantum phase behavior."""
        return [
            {
                "element": "Hydrogen (H2)",
                "bond_type": "Diatomic 1s^2 pair (4.52 eV)",
                "inter_bond_ev": 0.0009,
                "phase_transition": "Boils at 20.28 K",
                "lattice_behavior": "Insulating cryogenic liquid; 1-bond pairs",
            },
            {
                "element": "Helium (4He)",
                "bond_type": "Closed 1s^2 noble shell (0 bonds)",
                "inter_bond_ev": 0.0002,
                "phase_transition": "Boils at 4.22 K | Superfluid < 2.17 K",
                "lattice_behavior": "Bosonic He-4 pairs condense into 0-viscosity flow",
            },
            {
                "element": "Carbon (12C)",
                "bond_type": "4 sp^3 covalent bonds (3.60 eV/bond)",
                "inter_bond_ev": 3.6000,
                "phase_transition": "Sublimes at 3,915 K",
                "lattice_behavior": "3D tetrahedral network (Diamond insulator / Graphene conductor)",
            },
        ]


def run_multi_electron_demo() -> None:
    sim = BCCMultiElectronSim()

    print("=" * 88)
    print("PART 1: Nuclear Core Pion-Exchange Binding (H-1 vs. He-4 Alpha vs. C-12)")
    print("=" * 88)
    print("Nucleus           Nucleons   Binding (MeV)   MeV/Nucleon   Saved BCC Ticks   Total Mass")
    print("-" * 88)
    for r in sim.nuclear_core_table():
        print(
            f"{r['element']:<17} {r['nucleons']:>8} {r['binding_mev']:>15.2f} "
            f"{r['mev_per_nucleon']:>13.3f} {r['saved_bcc_ticks']:>17.3f} {r['bound_mass_mev']:>12.2f}"
        )

    print("\n" + "=" * 88)
    print("PART 2: Pauli Exclusion Electron Shells & Effective Nuclear Screening (Z_eff)")
    print("=" * 88)
    print("Atom       Electron Shell       Z_eff   Radius (Ang)   1st Ioniz (eV)   Covalent Bonds")
    print("-" * 88)
    for s in sim.electron_shell_screening():
        print(
            f"{s['symbol']:<10} {s['config']:<20} {s['z_eff']:>5.2f} {s['radius_ang']:>14.3f} "
            f"{s['ion_ev']:>16.2f} {s['open_bonds']:>16}"
        )

    print("\n" + "=" * 88)
    print("PART 3: How Valence Connectivity Controls Macroscopic Temperature & Quantum Phases")
    print("=" * 88)
    print("Element         Valence Routing                 Thermal Limit              3D Lattice Phase")
    print("-" * 88)
    for p in sim.macroscopic_phase_comparison():
        print(
            f"{p['element']:<15} {p['bond_type']:<31} {p['phase_transition']:<26} {p['lattice_behavior']}"
        )


if __name__ == "__main__":
    run_multi_electron_demo()

