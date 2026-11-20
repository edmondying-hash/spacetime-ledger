# Emergent Atomic Elements, Nuclear Reactions & Molecular Chemistry (`elements/`)

This directory bridges the microscopic **3D BCC Quark–Gluon Lattice (`bcc/`)** into atomic physics, nuclear fusion/fission, and molecular chemistry—demonstrating how nuclear pion binding and `Dirac-4` electron standing-wave shells build the material world.

---

## Core Atomic & Molecular Mechanisms on the 3D BCC Lattice

1. **Hierarchical Atomic Workload (`bcc_hydrogen_atom.py`):**
   - **Nuclear Core (`99.946%` of Hydrogen mass):** Three valence quarks (`u, u, d`) bound by a `~4.66`-link BCC diagonal gluon Steiner tree (`~929.3 MeV`) and dressed by an off-shell virtual pion (`q qbar`) cloud.
   - **Electronic Standing-Wave Shell (`0.054%` of Hydrogen mass):** A color-neutral `Dirac-4` electron spinor (`0.511 MeV`) trapped in the nucleus's `1/r` virtual-photon carrier field (`alpha ~ 1/137.036`), producing quantized Bohr shells ($r_n = n^2 a_0$) and spectral lines (`121.5 nm` Lyman-alpha, `656.1 nm` Balmer H-alpha).
   - **Full Phase Ladder:** Maps thermal jitter ($k_B T$) across Solid $\text{H}_2$ (`<14.01 K`), Liquid $\text{H}_2$ (`14.01–20.28 K`), Molecular $\text{H}_2$ gas, Atomic $\text{H}$ gas (`~3,500 K`), and Ionized Plasma (`~12,000 K`, where the electron strips free while the `929.3 MeV` proton core stays intact at `<10^-8` thermal stress).
2. **Nuclear Fusion & Quantum Tunneling (`bcc_nuclear_fusion.py`):**
   - Models `1/r` virtual-photon Coulomb repulsion against short-range pion/gluon Steiner tree merging (`-40.7 MeV` Helium-4 well inside `2.2 fm`).
   - Shows why `D + T -> He-4 + n + 17.59 MeV` (`3.518` freed BCC ticks) ignites at `~150M K` via Gamow tunneling while pure `p + p` fusion is bottlenecked by a virtual $W^+$ quark flip (`1.0e-25` relative rate).
3. **Nuclear Fission & Chain-Reaction Kinetics (`bcc_nuclear_fission.py`):**
   - Tracks the nuclear binding curve from `2H` (`1.11 MeV/nuc`) up to the **`56Fe` peak (`8.79 MeV/nuc`)** and down the $Z=92$ Coulomb stress cliff to **`235U` (`7.59 MeV/nuc`)**.
   - Simulates zero-Coulomb thermal neutron capture (`0.025 eV`), daughter splitting (`Ba-141 + Kr-92 + 3n`, freeing `~202.5 MeV = 40.5` BCC ticks), and neutron multiplication ($k_{\text{eff}} = 0.85$ subcritical vs. $1.00$ critical vs. $1.18$ supercritical).
4. **Multi-Electron Shells & Screening (`bcc_multi_electron_atoms.py`):**
   - Contrasts doubly-magic closed-shell **Helium (`1s^2`, `Z_eff = 1.69`, `0.313 Å`, `24.59 eV` ionization, `4.22 K` boiling / `2.17 K` superfluid)** against 4-valence **Carbon (`1s^2 2s^2 2p^2`, `Z_eff = 3.25`, `3,915 K` sublimation)**.
5. **Covalent Molecular Chemistry (`bcc_molecular_chemistry.py`):**
   - Shows **Methane (`CH4`)** locking into the exact `109.47°` tetrahedral body diagonals of the 3D BCC unit cell (`0.00 D` dipole, `111.7 K` boiling point), while **Water (`H2O`)**'s two unshared lone pairs compress its `O-H` angle to **`104.45°`** (`1.85 D` dipole, `0.21 eV` H-bonds), keeping Water liquid across **`273.15–373.15 K`**.

---

## Directory Structure & Quick Start (`elements/`)

| File | Description | Run Command |
| :--- | :--- | :--- |
| `bcc_hydrogen_atom.py` | Breaks down Hydrogen quark/gluon/electron mass shares, Bohr spectral lines, and `10 K` solid $\to$ `18 K` liquid $\to$ `100,000 K` plasma phases. | `python3 bcc_hydrogen_atom.py` |
| `bcc_nuclear_fusion.py` | Models `1/r` Coulomb barrier vs. gluon Steiner merge, Gamow tunneling (`15M–150M K`), and `D-T` (`17.59 MeV`) vs. `p-p` fusion channels. | `python3 bcc_nuclear_fusion.py` |
| `bcc_nuclear_fission.py` | Models the `2H -> 56Fe -> 235U` binding curve, thermal neutron splitting (`202.5 MeV`), and $k_{\text{eff}}$ chain-reaction generations. | `python3 bcc_nuclear_fission.py` |
| `bcc_multi_electron_atoms.py` | Compares `1H`, `4He`, and `12C` nuclear binding defects, Pauli shell screening ($Z_{\text{eff}}$), and superfluid vs. tetrahedral solid phases. | `python3 bcc_multi_electron_atoms.py` |
| `bcc_molecular_chemistry.py` | Models `CH4` (`109.47°` BCC tetrahedral), `H2O` (`104.45°` bent dipole), and `CO2` (`180°` linear) bond energies and `80–420 K` phase sweeps. | `python3 bcc_molecular_chemistry.py` |
