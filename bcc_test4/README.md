# 6-Face Planck-Cube Grid & Unified Hadron / Field Simulator

A zero-dependency Python simulation suite demonstrating how standard continuum physics—including **baryon and meson mass spectra**, **color confinement string breaking**, **pure-gluon mass gaps**, **Maxwell electromagnetism**, **quantum interference**, and **relativistic refractive gravity / network-deadlocked horizons**—emerges from a single local rule on a rigid 3D space-filling grid.

---

## Core Architecture: 6-Face Planck-Cube Lattice

* **Discrete Spacetime Cells (`1.0 l_P^3`, `1.0 t_P`):** Space is tiled by rigid, non-deforming cubic cells of volume `1.0 l_P^3` clocked by a global hardware tick `1.0 t_P`.
* **6 Orthogonal Face Connections (`±x, ±y, ±z`):** Every routing hop moves strictly across 1 orthogonal face (`1.0 l_P`) per tick. Diagonal or angled propagation emerges naturally as a transverse zigzag wave across orthogonal faces.
* **No Point Singularities or UV Catastrophes:** Finite cell spacing (`1.0 l_P`) imposes a hard Nyquist cutoff on momentum and wavelength, eliminating ultraviolet infinities and point singularities.
* **Network-Deadlocked Event Horizons:** When local workload (`mass + momentum`) saturates a node's per-tick I/O capacity (`W >= max_node_ticks`), routing deadlocks completely (`escaped_packets = 0`) and incoming packets pile up symmetrically across the outer 3D boundary shell.

---

## Modules & Benchmarks (`31/31` Unit Tests Passing)

| Module | Test Suite | Physics & Emergent Results |
| :--- | :--- | :--- |
| `baryon_calculator.py` | `test_baryon_calculator.py` (12 tests) | Effective pair-spin mass model calibrated to PDG 2024 (`p = 938.92 MeV`, `Delta+ = 1232.00 MeV`, `Lambda = 1115.68 MeV`, `Sigma0 = 1179.81 MeV`, `Xi0 = 1329.77 MeV`, `Omega- = 1681.89 MeV`). |
| `bcc_unified_sim.py` | `test_bcc_unified_sim.py` (5 tests) | 3-quark Y-junction workload, pure-gluon closed plaquette loops with a `~2,001.18 MeV` mass gap (`BareT = 0.0`), congestion lensing lag, and 2D core + 3D boundary shell deadlock. |
| `bcc_meson_sim.py` | `test_bcc_meson_sim.py` (3 tests) | Ground-state `q qbar` meson spectrum (`pi = 140.00 MeV`, `rho = 780.00 MeV`, `K = 488.20 MeV`, `K* = 897.27 MeV`, `phi = 1035.37 MeV`, `D = 1764.00 MeV`, `D* = 1892.00 MeV`, `J/psi = 3106.40 MeV`), exact `3:1` hyperfine spin splitting, and color-confining flux-tube string breaking at `7` orthogonal hops (`315.00 MeV > 275.0 MeV`). |
| `bcc_em_wave_sim.py` | `test_bcc_em_wave_sim.py` (2 tests) | Static and post-hop Gauss's law (`~10^-16` residual), global link flux conservation (`-1.39e-17`), and double-slit fringe collapse under which-slit sensor congestion. |
| `bcc_born_pascal.py` | `test_bcc_born_pascal.py` (2 tests) | Dual-channel (`+`/`-`) discrete Pascal walk generating exact destructive dark nodes (`0.0000`) and converging toward the continuous wave equation as ticks increase (`N = 12 -> 100`). |
| `bcc_3d_gravity.py` | `test_bcc_3d_gravity.py` (7 tests) | 6-face 3D `1/r` Poisson congestion, wavefront lensing lag vs. impact parameter `b`, spherical network-deadlocked horizons, 6-face zigzag wave trajectories, momentum-aimed 3D Pascal wave packets (`103` dark nodes), and the **Part 6 Relativistic Momentum-to-Gravity Coupler**. |
| `bcc3dhorizonsim.py` | Standalone CLI | Dedicated 3D network-deadlocked horizon & radial probe simulator with customizable grid size, core workload, and packet infall checkpoints. |

---

## Quick Start

Run all **31 unit tests** and all **6 simulation modules**:

```bash
python3 run_bcc_suite.py
```

Export a fresh JSON benchmark snapshot without re-running unit tests:

```bash
python3 run_bcc_suite.py --skip-tests --json-out benchmark_report.json
```

Run the standalone 3D horizon probe:

```bash
python3 bcc3dhorizonsim.py --size 17 --workload 2400 --packets 260
```
