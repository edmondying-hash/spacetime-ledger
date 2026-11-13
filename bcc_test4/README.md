# 6-Face Space-Filling Planck-Cube Lattice & Hadron Physics Suite

A self-contained computational physics repository modeling hadron spectroscopy,
color confinement, pure-gluon mass gaps, Maxwell link conservation, Born-Pascal
quantum interference, network-deadlocked horizons, relativistic lensing, and
3-body gravitational orbits on a single discrete lattice architecture.

## Core Architecture

- **Space-Filling Lattice:** Rigid 3D cubic lattice where every cell is a
  Planck cube of volume `1.0 l_P^3` connected across **6 orthogonal faces**
  (`±x, ±y, ±z`).
- **Universal Tick Clock:** Discrete routing step of `1.0 t_P` (`1` orthogonal
  face hop per tick at `c`).
- **Node Congestion Cap:** Each cube processes up to `100 ticks/cycle`;
  overloaded regions network-deadlock (`0 escape`) without central
  singularities.

## Quick Start

```sh
# 1. Run all 37 unit tests + all 8 simulation modules + export JSON report
python3 run_bcc_suite.py --json-out benchmark_report.json

# 2. Run simulations only (skip unit tests)
python3 run_bcc_suite.py --skip-tests --json-out benchmark_report.json

# 3. Generate the 6-panel benchmark dashboard PNG
python3 plot_bcc_benchmarks.py --json benchmark_report.json --out bcc_benchmark_dashboard.png
```

## Simulation Modules (8)

1. **`baryon_calculator.py`** — Effective pair-spin mass calculator calibrated
   on `p/n`, `Delta(1232)`, and `Lambda` (`938.92`, `1232.00`, `1115.68 MeV`),
   predicting out-of-calibration octet/decuplet states (`Sigma0 = 1179.81 MeV`,
   `Xi0 = 1329.77 MeV`, `Omega- = 1681.89 MeV`) against PDG 2024.
2. **`bcc_unified_sim.py`** — Four-part unified grid simulation:
   - *Part 1:* 3-quark (`3q`) routing workload vs. pair-spin mass rule.
   - *Part 2:* Closed pure-gluon loops (`BareT = 0`) yielding a
     **`2,001.18 MeV` mass gap** for 4-link loops above the `0.00 MeV` vacuum.
   - *Part 3:* Wavefront gravitational lensing (`10`, `7`, `0` px delay) around
     a congestion cluster.
   - *Part 4:* 2D-to-3D network-deadlocked core growth (`13 -> 23` deadlocked
     nodes, `0` escaped packets).
3. **`bcc_meson_sim.py`** — Ground-state quark-antiquark (`q qbar`) meson
   spectrum (`pi = 140.00 MeV`, `rho = 780.00 MeV`, `K = 488.20 MeV`,
   `K* = 897.27 MeV`, `phi = 1035.37 MeV`, `J/psi = 3106.40 MeV`) with `3:1`
   hyperfine splitting and linear flux-tube stretching (`45 MeV/hop`) that
   snaps at **7 orthogonal hops (`315.00 MeV`)** above the `275.0 MeV` threshold.
4. **`bcc_em_wave_sim.py`** — 3D Maxwell link-flux conservation enforcing
   Gauss's law to `~10^-16` residual, plus double-slit interference vs.
   which-slit sensor congestion collapse.
5. **`bcc_born_pascal.py`** — Dual-channel (`+/-`) Pascal random walk
   reproducing exact `0.0000` destructive dark nodes and converging toward the
   continuous wave equation as ticks increase (`N = 12 -> 100`).
6. **`bcc_3d_gravity.py`** — 3D 6-face Poisson `1/r` congestion profiles,
   impact-parameter lensing (`b = 0..10`), 3D spherical deadlocked horizons
   (`98` deadlocked nodes, `0` escape), 6-face zigzag trajectories, biased 3D
   Pascal wave packets, and **Part 6** relativistic momentum-to-gravity
   coupling (`6 -> 12` ticks/step bending central rays from `6 px` to `13 px`).
7. **`bcc3dhorizonsim.py`** — Standalone 3D horizon & network-deadlock probe
   (`19x19x19` grid) mapping radial horizon profiles (`r = 0..3 l_P` blocked
   with `0` escape; `r >= 4 l_P` active I/O).
8. **`bcc_3body_orbits.py`** — 3-body ledger-grid orbits climbing superposed
   6-face congestion gradients (no pairwise forces) vs. unsoftened Newton:
   - *Chenciner–Montgomery Figure-8:* Stays bound outside the `0.15`-unit
     grid smoothing cap (`min_sep = 0.677`) with `0.046` drift over 1 period.
   - *Burrau Pythagorean 3-4-5:* Matches Newton pre-pass (`t = 1.80`,
     `drift = 0.005`), then caps the close pass inside `0.15` units
     (`min_sep = 0.042`) without `1/r -> infinity` singularities.
   - *Finite-`c` Retardation:* Quantifies orbital phase shift (`drift = 2.884`
     at `c = 20`) when load propagates at finite wave speed instead of
     instantaneous relaxation.

## Unit Test Suite (37 Tests Across 8 Modules)

| Test Module | Tests | Coverage |
| :--- | :---: | :--- |
| `test_baryon_calculator.py` | 12 | Anchors, permutations, Pauli states, pair-spin rule |
| `test_bcc_unified_sim.py` | 5 | Steiner links, strange lag, glueball gap, lensing, 3D lock |
| `test_bcc_meson_sim.py` | 3 | Meson ordering, `3:1` hyperfine split, `7`-hop string break |
| `test_bcc_em_wave_sim.py` | 2 | Gauss's law (`10^-16`), double-slit vs. detector collapse |
| `test_bcc_born_pascal.py` | 2 | Pascal dark nodes, continuous wave equation convergence |
| `test_bcc_3d_gravity.py` | 7 | `1/r` decay, spherical horizon, zigzag, momentum lensing |
| `test_bcc3dhorizonsim.py` | 3 | 6-face stencil, 3D accretion growth, radial horizon profile |
| `test_bcc_3body_orbits.py` | 3 | Figure-8 stability, 3-4-5 smoothing split, finite-`c` shift |
| **Total** | **37** | **All passing (`OK`)** |

## Visualization

- **`plot_bcc_benchmarks.py`** reads `benchmark_report.json` and renders
  `bcc_benchmark_dashboard.png` (baryons, mesons, flux-tube breaking,
  pure-gluon mass gap, momentum-coupled lensing, and 3D horizon profile).

