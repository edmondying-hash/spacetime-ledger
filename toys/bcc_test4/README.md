# 6-Face Space-Filling Planck-Cube Lattice & Hadron Physics Suite

A self-contained computational physics repository modeling hadron spectroscopy,
color confinement, pure-gluon mass gaps, Maxwell link conservation, Born-Pascal
quantum interference, network-deadlocked horizons, relativistic lensing,
3-body gravitational orbits, EM-neutral dark matter halos, and 3-generation
baryogenesis on a single discrete lattice architecture.

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
# 1. Run all 43 unit tests + all 10 simulation modules + export JSON report
python3 run_bcc_suite.py --json-out benchmark_report.json

# 2. Run simulations only (skip unit tests)
python3 run_bcc_suite.py --skip-tests --json-out benchmark_report.json

# 3. Generate the 9-panel benchmark dashboard PNG
python3 plot_bcc_benchmarks.py --json benchmark_report.json --out bcc_benchmark_dashboard.png
```

## Simulation Modules (10)

1. **`baryon_calculator.py`** — Effective pair-spin mass calculator calibrated
   on `p/n`, `Delta(1232)`, and `Lambda` (`938.92`, `1232.00`, `1115.68 MeV`),
   predicting out-of-calibration octet/decuplet states (`Sigma0 = 1179.81 MeV`,
   `Xi0 = 1329.77 MeV`, `Omega- = 1681.89 MeV`) against PDG 2024.
2. **`bcc_unified_sim.py`** — Four-part unified 6-face grid simulation:
   - *Part 1:* 3-quark (`3q`) orthogonal 6-face routing workload & Manhattan
     Steiner tree load across all 8 baryon families (`N` through `Omega`).
   - *Part 2:* Closed pure-gluon loops (`BareT = 0`) yielding a
     **`2,001.19 MeV` mass gap** for 4-link loops above the `0.00 MeV` vacuum.
   - *Part 3:* Wavefront gravitational lensing (`10`, `5`, `0` px delay) around
     a congestion cluster.
   - *Part 4:* 2D-to-3D network-deadlocked core growth (`13 -> 23` deadlocked
     nodes, `0` escaped packets).
3. **`bcc_meson_sim.py`** — Ground-state quark-antiquark (`q qbar`) meson
   spectrum (`pi = 140.00 MeV`, `rho = 780.00 MeV`, `K = 493.01 MeV`,
   `K* = 902.08 MeV`, `phi = 1035.37 MeV`, `D = 1867.33 MeV` (`+0.13` vs
   PDG `1867.20`), `D* = 1995.33 MeV` (`−13.22` vs PDG `2008.55`),
   `J/psi = 3106.40 MeV`, `B = 5493.07 MeV` (`+213.41` vs PDG `5279.66`),
   `B* = 5535.02 MeV` (`+210.31` vs PDG `5324.71`),
   `Upsilon = 9460.69 MeV` (`+0.29` vs PDG `9460.40`)) with `3:1`
   hyperfine splitting and linear flux-tube stretching (`45 MeV/hop`) that
   snaps at **7 orthogonal hops (`315.00 MeV`)** above the `275.0 MeV`
   threshold.
   - *Reduced-mass route correction:* Unequal-flavour pairs pick up an
     extra routing delay `ΔRouteT = b̄ − 2μ = (b1−b2)²/(2(b1+b2))` ticks,
     added once (`1×`) after the baseline `3·BareT` term. The term is zero
     when `b1 = b2` (`pi`, `rho`, `phi`, `J/psi`, `Upsilon`). It is `+0.963` ticks (`4.82 MeV`)
     for K/K* and `62/3` ticks (`103.33 MeV`) for D/D*.

     An additive quark-mass rule must miss D. Spin-averaged PDG 2024 masses
     of the symmetric light and charm systems, `(616 + 3069)/2 = 1842 MeV`,
     sit well below the real spin-averaged D/D* mass of `1973 MeV`. The
     reduced-mass term is what closes most of that gap.
   - *Caveats:* `κ = 1` is a choice, not a derived factor. Putting the
     correction inside the `3·BareT` term (`κ = 3`) would shift D by
     `+310 MeV` instead of `+103.33 MeV`. The form and `κ` were chosen
     with D in view, so D and D* are not blind predictions. The meson
     unit tests check only mass ordering, the `3:1` spin ratio, and the
     7-hop string break; they do not test this term.
   - *Bottom quarks (B, B\*, Upsilon):* The bottom bare cost is `b = 236.50`
     ticks. The source comments that value as anchored solely on the
     symmetric `Upsilon(1S)` (`b bbar`); the model then sits `+0.29 MeV`
     from the PDG 2024 mass (`9460.69` vs `9460.40`). With that cost held
     fixed, B and B* are the resulting predictions. They overshoot the
     PDG 2024 masses by about `+210 MeV` (`B = 5493.07` vs `5279.66`,
     `B* = 5535.02` vs `5324.71`). The hyperfine splitting itself still
     tracks the `1/(b1 b2)` rule: `B*−B = 41.95 MeV` vs PDG `45.05 MeV`
     (within about `3 MeV`), continuing the sequence
     `640 → 409.07 → 128 → 41.95 MeV`.

     The correction grows linearly with the heavy mass. Its heavy-quark
     asymptote is `½b₂ − (3/2)b₁`, not `½b₂ − 2b₁`. For B it is already
     `+96.91` ticks. In the HQET limit the light quark's orbit saturates
     instead, so this linear term overshoots for bottom. B is a blind
     prediction only if that `b` cost was fixed from Upsilon before looking at
     B; the source comment says that this is how it was set.
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
9. **`bcc_dark_matter.py`** — EM-neutral closed-loop halos (`Q_EM = 0`,
   `Load > 0`) separating gravitational routing load from photon link flux:
   - *Invisible Gravitational Lensing:* `0.0%` photon attenuation alongside
     `12 px` central gravitational wavefront delay (`b = 0`).
   - *Flat Galaxy Rotation Curves:* Replaces Keplerian `1/sqrt(r)` falloff
     (`20.06 -> 7.75`) with a flat outer halo plateau (`19.43–21.26`).
   - *Bullet-Cluster Offset:* Collisionless `Q_EM = 0` halos pass through each
     other (`4.0 l_P` separation) while EM-coupled baryons shock and stall
     (`1.1 l_P` separation, `+1.45 l_P` lensing offset).
10. **`bcc_baryogenesis.py`** — This module is Edmond's conjecture about the
    three-generation link to CP violation; its parameters (e.g. eps_3d =
    0.015) are hand-set guesses, not derived results. Side-by-side 3-generation
    cascade starting from an exact 50/50 matter/antimatter population. An
    irreducible 3D chiral phase (`J_cp = sin(1.15 rad)`) is zero for
    `N_gen < 3` and turns on at `N_gen = 3`. Two biases are compared: an
    untuned toy (`eps_3d = 0.015`) and a cosmic-tuned value
    (`eps_3d = 1.002e-9`) aimed at the observed baryon-to-photon ratio
    `eta ~ 6.10e-10`. In the suite run, `N_gen = 1` and `2` annihilate to
    zero surviving matter; `N_gen = 3` leaves a surplus (`J_cp = 0.9128`,
    untuned `eta = 9.2114e-03`, cosmic `eta = 6.0973e-10`). A second part
    assigns tick loads to four generation geometries (`18`, `44`, `82`,
    `128`) against the `100`-tick node cap, so Gen 1–3 fit and a hypothetical
    Gen 4 does not.

## Unit Test Suite (43 Tests Across 10 Modules)

| Test Module | Tests | Coverage |
| :--- | :---: | :--- |
| `test_baryon_calculator.py` | 12 | Anchors, permutations, Pauli states, pair-spin rule |
| `test_bcc_unified_sim.py` | 5 | 6-face Manhattan Steiner links, strange lag, glueball gap, lensing, 3D lock |
| `test_bcc_meson_sim.py` | 3 | Meson ordering, `3:1` hyperfine split, `7`-hop string break |
| `test_bcc_em_wave_sim.py` | 2 | Gauss's law (`10^-16`), double-slit vs. detector collapse |
| `test_bcc_born_pascal.py` | 2 | Pascal dark nodes, continuous wave equation convergence |
| `test_bcc_3d_gravity.py` | 7 | `1/r` decay, spherical horizon, zigzag, momentum lensing |
| `test_bcc3dhorizonsim.py` | 3 | 6-face stencil, 3D accretion growth, radial horizon profile |
| `test_bcc_3body_orbits.py` | 3 | Figure-8 stability, 3-4-5 smoothing split, finite-`c` shift |
| `test_bcc_dark_matter.py` | 3 | Invisible `Q_EM=0` lensing, flat rotation curve, Bullet-Cluster offset |
| `test_bcc_baryogenesis.py` | 3 | 1–2 gen annihilation, 3-gen cosmic `eta ~ 6.10e-10`, 100-tick cap |
| **Total** | **43** | **All passing (`OK`)** |

## Visualizations

- **`plot_bcc_benchmarks.py`** reads `benchmark_report.json` and renders
  `bcc_benchmark_dashboard.png` (9 panels covering baryons, mesons, flux-tube
  breaking, pure-gluon mass gap, momentum-coupled lensing, 3D horizon profile,
  3-body Figure-8, zoomed Pythagorean 3-4-5, and dark-matter rotation curves).
- **`animate_uds_mass.py`** renders a 3-act animation (`uds_gluon_mass_jump.gif`)
  illustrating how `uds` (Lambda^0) jumps from bare valence quarks to full
  gluon-dressed baryon mass.

## PDF

Convert this file with Pandoc:

```sh
pandoc README.md -o readme.pdf
```

