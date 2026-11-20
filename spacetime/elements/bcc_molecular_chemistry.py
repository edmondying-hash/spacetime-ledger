#!/usr/bin/env python3
"""
Molecular Chemistry on the 3D BCC Lattice: Methane (CH4), Water (H2O) & CO2.

Models covalent electron-pair sharing, sp^3 tetrahedral BCC body-diagonal geometry,
lone-pair bond angle compression (109.5° -> 104.5°), electric dipole moments, and
intermolecular hydrogen bonding vs. boiling points:
  1. Covalent Bond Workload & Geometry: Compares CH4 (4 symmetric C-H bonds along
     tetrahedral BCC diagonals), H2O (2 O-H bonds + 2 lone pairs), and CO2 (linear O=C=O).
  2. Dipole Moment & Intermolecular Cohesion: Shows how lone-pair asymmetry gives H2O
     a 1.85 D dipole and 0.21 eV hydrogen bonds vs. non-polar CH4 (0.00 D, 0.011 eV).
  3. Thermal Phase Sweep (80 K -> 450 K): Tracks Solid, Liquid, and Gas states for
     Methane vs. Water under ambient thermal vibration k_B * T.
"""

import math
from typing import Any, Dict, List


class BCCMolecularChemistrySim:
    """Models covalent electron-pair routing and intermolecular phases on the 3D BCC grid."""

    KB_EV_PER_K = 8.617333e-5

    def molecular_geometry_table(self) -> List[Dict[str, Any]]:
        """Compare valence electron pairs, BCC sp^3 bond angles, bond energies, and dipoles."""
        molecules = [
            {
                "formula": "Methane (CH4)",
                "bonding_pairs": 4,
                "lone_pairs": 0,
                "bond_angle_deg": 109.47,  # Exact 3D BCC tetrahedral diagonal angle acos(-1/3)
                "bond_len_ang": 1.09,
                "bond_energy_ev": 4.25,    # Per C-H covalent pair
                "dipole_debye": 0.00,
                "symmetry": "Tetrahedral (4 BCC diagonals)",
            },
            {
                "formula": "Water (H2O)",
                "bonding_pairs": 2,
                "lone_pairs": 2,
                "bond_angle_deg": 104.45,  # Compressed by 2 lone-pair lobes (~2.5° per lone pair)
                "bond_len_ang": 0.96,
                "bond_energy_ev": 4.80,    # Per O-H covalent pair
                "dipole_debye": 1.85,
                "symmetry": "Bent V-shape (2 lone pairs)",
            },
            {
                "formula": "Carbon Dioxide (CO2)",
                "bonding_pairs": 4,        # Two double bonds (O=C=O)
                "lone_pairs": 0,           # On central Carbon
                "bond_angle_deg": 180.00,
                "bond_len_ang": 1.16,
                "bond_energy_ev": 8.28,    # Per C=O double bond
                "dipole_debye": 0.00,
                "symmetry": "Linear Opposing (dipoles cancel)",
            },
        ]
        for m in molecules:
            total_covalent_ev = m["bonding_pairs"] * m["bond_energy_ev"]
            if m["formula"] == "Carbon Dioxide (CO2)":
                total_covalent_ev = 2.0 * m["bond_energy_ev"]
            m["total_bond_ev"] = round(total_covalent_ev, 2)
        return molecules

    def intermolecular_cohesion_table(self) -> List[Dict[str, Any]]:
        """Compare intermolecular attraction energy, melting point, and boiling point."""
        return [
            {
                "molecule": "Methane (CH4)",
                "dipole_d": 0.00,
                "inter_force": "Weak London dispersion (0.011 eV)",
                "melt_k": 90.7,
                "boil_k": 111.7,
                "state_at_300k": "Gas (cryogenic liquid only)",
            },
            {
                "molecule": "Carbon Dioxide (CO2)",
                "dipole_d": 0.00,
                "inter_force": "Quadrupole dispersion (0.17 eV)",
                "melt_k": 216.6,   # At 5.1 atm triple point (sublimes at 194.7 K at 1 atm)
                "boil_k": 194.7,   # Sublimation point at 1 atm
                "state_at_300k": "Gas (sublimes dry ice at 194.7 K)",
            },
            {
                "molecule": "Water (H2O)",
                "dipole_d": 1.85,
                "inter_force": "Strong H-bond network (0.21 eV)",
                "melt_k": 273.15,
                "boil_k": 373.15,
                "state_at_300k": "Liquid (life-supporting ocean window)",
            },
        ]

    def phase_sweep_comparison(self, temps_k: List[float]) -> List[Dict[str, Any]]:
        """Compare physical phase of CH4 vs. H2O from 80 K to 420 K."""
        rows: List[Dict[str, Any]] = []
        for t in temps_k:
            kbt_ev = self.KB_EV_PER_K * t
            ch4_state = "Solid" if t < 90.7 else ("Liquid" if t < 111.7 else "Gas")
            h2o_state = "Solid (Ice)" if t < 273.15 else ("Liquid (Water)" if t < 373.15 else "Gas (Steam)")
            rows.append({
                "temp_k": t,
                "temp_c": round(t - 273.15, 1),
                "kbt_ev": round(kbt_ev, 5),
                "ch4_phase": ch4_state,
                "h2o_phase": h2o_state,
            })
        return rows


def run_molecular_demo() -> None:
    sim = BCCMolecularChemistrySim()

    print("=" * 92)
    print("PART 1: Covalent Electron-Pair Geometry on the 3D BCC Lattice (CH4 vs. H2O vs. CO2)")
    print("=" * 92)
    print("Molecule             Bonds  LonePairs  Angle (deg)  Bond (Ang)  Total Bond   Dipole (D)")
    print("-" * 92)
    for m in sim.molecular_geometry_table():
        print(
            f"{m['formula']:<20} {m['bonding_pairs']:>5} {m['lone_pairs']:>10} "
            f"{m['bond_angle_deg']:>12.2f} {m['bond_len_ang']:>11.2f} "
            f"{m['total_bond_ev']:>9.2f} eV {m['dipole_debye']:>10.2f}"
        )

    print("\n" + "=" * 92)
    print("PART 2: Intermolecular Cohesion & Why Water Is Liquid at 300 K (27°C)")
    print("=" * 92)
    print("Molecule             Dipole   Intermolecular Link               Melt (K)   Boil (K)")
    print("-" * 92)
    for c in sim.intermolecular_cohesion_table():
        print(
            f"{c['molecule']:<20} {c['dipole_d']:>5.2f}D   {c['inter_force']:<33} "
            f"{c['melt_k']:>8.2f} {c['boil_k']:>10.2f}"
        )

    print("\n" + "=" * 92)
    print("PART 3: Thermal Vibration Phase Sweep (80 K Cryogenic -> 420 K Steam)")
    print("=" * 92)
    print("Temp (K)   Temp (°C)   Thermal kT (eV)   Methane (CH4)   Water (H2O)")
    print("-" * 92)
    for p in sim.phase_sweep_comparison([80.0, 100.0, 200.0, 260.0, 300.0, 350.0, 420.0]):
        print(
            f"{p['temp_k']:>8.1f} {p['temp_c']:>11.1f} {p['kbt_ev']:>17.5f}   "
            f"{p['ch4_phase']:<15} {p['h2o_phase']}"
        )


if __name__ == "__main__":
    run_molecular_demo()

