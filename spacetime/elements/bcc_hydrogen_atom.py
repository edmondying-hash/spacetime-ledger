#!/usr/bin/env python3
"""
Full 3D BCC Hydrogen Atom Decomposition & Thermal Vibration Sweep (`bcc_hydrogen_atom.py`).

Pulls apart a complete Hydrogen atom across every hierarchical workload layer on the
3D BCC (8-Diagonal) Spacetime Network:
  1. Subatomic Core Breakdown: Valence quarks (u, u, d), 4.66-link gluon Steiner tree,
     virtual pion (q qbar) cloud, and Dirac-4 electron mass share (99.946% vs 0.054%).
  2. Virtual-Photon Standing-Wave Orbitals (n = 1..5): Quantizes Bohr radii r_n = n^2 * a_0,
     orbital speeds v_n = alpha * c / n, binding energies E_n = -13.606 eV / n^2, and
     Balmer/Lyman photon emission wavelengths.
  3. Thermal Vibration & Plasma Ionization Sweep (300 K -> 100,000 K): Shows ambient lattice
     vibration ionizing the 13.6 eV electron shell while leaving the 938.3 MeV quark-gluon
     proton core completely untouched (70,000,000x binding stiffness gap).
"""

import math
from typing import Any, Dict, List


class BCCHydrogenAtomSim:
    """Hierarchical 3D BCC workload decomposition of a Hydrogen atom (p+ + e-)."""

    ALPHA_EM = 1.0 / 137.035999  # Fine-structure carrier coupling probability
    BOHR_RADIUS_ANG = 0.529177   # Ground-state standing wave radius a_0 (Angstroms)
    RYDBERG_EV = 13.605693       # Ground-state binding energy (eV)
    KB_EV_PER_K = 8.617333e-5    # Boltzmann constant (eV / K)
    HC_EV_NM = 1239.84198        # Planck-c conversion (eV * nm)

    def __init__(self, tick_to_mev: float = 5.0):
        self.tick_to_mev = tick_to_mev

    def decompose_atom_workload(self) -> List[Dict[str, Any]]:
        """Break down total Hydrogen atom mass/ticks from quarks & gluons to electron shell."""
        # Proton (938.272 MeV): 3 valence quarks + ~4.66 BCC diagonal gluon Steiner links + spin
        u_bare_mev = 2.16
        d_bare_mev = 4.67
        val_quarks_mev = 2.0 * u_bare_mev + d_bare_mev  # ~8.99 MeV (~1% of proton)
        gluon_steiner_mev = 938.272 - val_quarks_mev    # ~929.28 MeV (~99% routing workload!)
        pion_virtual_mev = 138.04                       # Virtual llbar cloud dressing (off-shell)
        electron_mev = 0.511                            # Dirac-4 spinor packet
        binding_defect_mev = -self.RYDBERG_EV * 1e-6    # -0.0000136 MeV mass defect

        total_mev = val_quarks_mev + gluon_steiner_mev + electron_mev + binding_defect_mev
        components = [
            ("Valence Quarks (u, u, d)", "3 Dirac-4 spinors (BareT)", val_quarks_mev),
            ("Gluon Steiner Flux Tree", "~4.66 BCC diagonal links (RouteT)", gluon_steiner_mev),
            ("Virtual Pion Cloud (pi)", "Off-shell q-qbar vacuum dressing", 0.0),  # Virtual loan = 0 net mass
            ("Orbital Electron (e-)", "1 color-neutral Dirac-4 spinor", electron_mev),
            ("EM Binding Mass Defect", "1/r virtual-photon standing wave", binding_defect_mev),
        ]

        rows: List[Dict[str, Any]] = []
        for name, topology, mev in components:
            display_mev = pion_virtual_mev if "Pion" in name else mev
            ticks = display_mev / self.tick_to_mev
            pct = (mev / total_mev) * 100.0
            rows.append({
                "component": name,
                "topology": topology,
                "energy_mev": round(display_mev, 6),
                "bcc_ticks": round(ticks, 4),
                "mass_share_pct": round(pct, 5),
            })
        return rows

    def standing_wave_orbitals(self, max_n: int = 5) -> List[Dict[str, Any]]:
        """Compute quantized 3D BCC standing-wave shells n = 1..max_n."""
        rows: List[Dict[str, Any]] = []
        for n in range(1, max_n + 1):
            r_ang = self.BOHR_RADIUS_ANG * (n ** 2)
            v_over_c = self.ALPHA_EM / n
            e_ev = -self.RYDBERG_EV / (n ** 2)
            # Photon emitted when dropping from level n -> n-1 (or n -> 2 for Balmer)
            if n == 1:
                trans_label = "Ground state (1s)"
                photon_nm = 0.0
            elif n == 2:
                de = self.RYDBERG_EV * (1.0 - 0.25)
                photon_nm = self.HC_EV_NM / de
                trans_label = "Lyman-alpha (2->1 UV)"
            else:
                de = self.RYDBERG_EV * (0.25 - 1.0 / (n ** 2))
                photon_nm = self.HC_EV_NM / de
                trans_label = f"Balmer ({n}->2 Visible)"

            rows.append({
                "n": n,
                "radius_ang": round(r_ang, 4),
                "v_over_c": round(v_over_c, 6),
                "energy_ev": round(e_ev, 4),
                "transition": trans_label,
                "photon_nm": round(photon_nm, 2),
            })
        return rows

    def thermal_vibration_sweep(self, temps_k: List[float]) -> List[Dict[str, Any]]:
        """
        Simulate ambient thermal lattice jitter k_B * T across all phase regimes:
        Solid H2 (<14.01 K) -> Liquid H2 (14.01-20.28 K) -> H2 Gas -> Atomic H -> Plasma.
        """
        rows: List[Dict[str, Any]] = []
        proton_glue_ev = 929.28e6  # 929.28 MeV in eV
        t_melt_k = 14.01           # Solid -> Liquid H2 (1 atm)
        t_boil_k = 20.28           # Liquid -> Gas H2 (1 atm)
        h2_bond_ev = 4.52          # Covalent H-H shared electron bond

        for temp in temps_k:
            kbt_ev = self.KB_EV_PER_K * temp
            if temp < 1500.0:
                ion_frac = 0.0
            else:
                boltz = math.exp(-self.RYDBERG_EV / max(1e-9, kbt_ev))
                saha_factor = 1.0e8 * boltz
                ion_frac = saha_factor / (1.0 + saha_factor)

            glue_stress_ratio = kbt_ev / proton_glue_ev
            if temp < t_melt_k:
                state = "Solid H2 Crystal (van der Waals locked)"
            elif temp < t_boil_k:
                state = "Liquid H2 (14.0-20.3 K, sliding H2 pairs)"
            elif temp < 2500.0:
                state = "Molecular H2 Gas (4.52 eV covalent bond)"
            elif ion_frac < 0.01:
                state = "Atomic H Gas (H2 dissociated, 1s bound)"
            elif ion_frac < 0.90:
                state = "Excited / Partially Ionized H"
            else:
                state = "Ionized Plasma (e- free, p+ core intact)"

            rows.append({
                "temp_k": temp,
                "thermal_ev": kbt_ev,
                "electron_ion_pct": round(ion_frac * 100.0, 2),
                "proton_glue_stress": glue_stress_ratio,
                "atom_state": state,
            })
        return rows


def run_hydrogen_demo() -> None:
    sim = BCCHydrogenAtomSim(tick_to_mev=5.0)

    print("=" * 90)
    print("PART 1: Hierarchical 3D BCC Workload Breakdown of a Hydrogen Atom (p+ + e-)")
    print("=" * 90)
    print("Component                  BCC Network Topology                Energy (MeV)   Mass Share")
    print("-" * 90)
    for r in sim.decompose_atom_workload():
        note = " (virtual)" if "Pion" in r["component"] else f"{r['mass_share_pct']:>8.4f}%"
        print(f"{r['component']:<26} {r['topology']:<35} {r['energy_mev']:>12.6f} {note:>11}")

    print("\n" + "=" * 90)
    print("PART 2: Electron Standing-Wave Orbitals (1/r Virtual-Photon Carrier Potential)")
    print("=" * 90)
    print("Shell n   Radius (Ang)   Speed (v/c)   Binding (eV)   Spectral Transition      Photon (nm)")
    print("-" * 90)
    for o in sim.standing_wave_orbitals(max_n=5):
        ph_str = f"{o['photon_nm']:>9.2f} nm" if o["photon_nm"] > 0 else "         ---"
        print(
            f"{o['n']:>7} {o['radius_ang']:>14.4f} {o['v_over_c']:>13.6f} "
            f"{o['energy_ev']:>14.4f}   {o['transition']:<22} {ph_str}"
        )

    print("\n" + "=" * 90)
    print("PART 3: Thermal Lattice Vibration Sweep (10 K Solid -> 18 K Liquid -> 100,000 K Plasma)")
    print("=" * 90)
    print("Temp (K)   Thermal kT (eV)   e- Ionized (%)   p+ Gluon Stress   Matter Phase & Lattice State")
    print("-" * 90)
    sweep_temps = [10.0, 18.0, 300.0, 3500.0, 8000.0, 12000.0, 100000.0]
    for t in sim.thermal_vibration_sweep(sweep_temps):
        print(
            f"{t['temp_k']:>8.1f} {t['thermal_ev']:>17.5f} {t['electron_ion_pct']:>15.2f}% "
            f"{t['proton_glue_stress']:>17.2e}   {t['atom_state']}"
        )


if __name__ == "__main__":
    run_hydrogen_demo()
