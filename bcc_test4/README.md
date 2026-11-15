# Quantized Space-Ledger (`spacetime-ledger`) — 6-Face Planck-Cube Grid Suite

A zero-dependency Python 3 computational physics and toy-model simulation suite exploring how hadron spectroscopy, Dirac spinors, gauge force carriers, electromagnetic link-flux recoil, quantum wave interference, Special Relativity, General Relativity, dark matter halos, CMB blackbody cooling, congestion-gated dark energy, and black-hole storage horizons can be modeled on a single discrete **3D space-filling cubic lattice**.

> **Scientific Framing:** Every module in this repository is a self-contained, unit-tested computational toy model (`74/74` passing tests in the master suite, plus `4/4` tests in the standalone stencil benchmark). Numerical outputs come directly from executing the deterministic lattice routing and ledger conservation rules below; they are consistency checks and discrete analogies rather than claims that established continuous physics emerges ab initio without calibration knobs.

---

## Core Lattice Architecture

* **Fundamental Cell (`1.0 l_P^3`):** Rigid 3D cubic grid of Planck-scale cells with **6 orthogonal faces** (`±x, ±y, ±z`), eliminating diagonal shortcuts (`1 orthogonal face hop per tick`).
* **Why 6-Face Cubic Over 8-Link BCC (`bcc_lattice_comparison.py`):** A standalone side-by-side benchmark (`4/4` unit tests) proves that an 8-link body-centered cubic stencil `(±1, ±1, ±1)` splits 3D space into disconnected checkerboard parity sublattices (blocking adjacent cubes like `(1, 0, 0)` and breaking `Dirac4` spatial gradients), whereas the **6-face simple cubic stencil** visits `100%` of its light cone, yields tighter 3D Poisson isotropy (`18.64%` vs. `26.16%`), and produces exact zero-amplitude dark nodal planes (`36/36` exact dark nodes).
* **Mass vs. Charge on the Ledger (`bcc_em_recoil.py`):**
  * **Mass (`BareT + RouteT`):** The positive scalar tick workload required to redraw and sustain a particle's internal closed loop each cycle—explaining inertia (`a = F / m`) as the routing overhead of shifting a busier pattern across cube faces.
  * **Electric Charge (`Q_EM = +1, -1, 0`):** Net boundary link-flux polarity across the 6 cube faces. Opposite polarities (`+` source, `-` sink) relieve routing tension along shared links (attraction), matching polarities pile up link congestion (repulsion), and balanced internal quark loops (`Q_EM = 0`) carry mass without EM coupling.
* **Universal Routing Speed (`c = 1.0 l_P / t_P`):** Every fundamental packet advances by at most 1 orthogonal face hop per universal clock tick (`1.0 t_P`).
* **Node Throughput Cap (`C_cap = 100 ticks/cycle`):** Each cell enforces a finite processing ceiling (`100 ticks/cycle`). When local routing workload saturates `W(r) >= 100`, outbound gates lock (`0` escape), forming a **zero-leak horizon storage tank** and preventing unphysical `1/r -> infinity` singularities.
* **Global Ledger Conservation:** Total routing ticks, charge flux, spinor norm (`|psi|^2 = 1`), and linear/angular momentum (`p_1 + p_2 = 0`, `L_core + L_stars = 0`) are strictly conserved across every step.

---

## Quick Start

```sh
# 1. Run all 74 unit tests + 19 simulation modules and export JSON report
python3 run_bcc_suite.py --json-out benchmark_report.json

# 2. Render the complete 24-panel (4x6) master benchmark dashboard
python3 plot_bcc_benchmarks.py --json benchmark_report.json --out bcc_benchmark_dashboard.png

# 3. Run the standalone 6-face cubic vs. 8-link BCC architectural comparison
python3 -m unittest test_bcc_lattice_comparison.py -v && python3 bcc_lattice_comparison.py
```

---

## Simulation Modules (19 Master Scripts + 1 Standalone Benchmark)

### Part A — Hadron Spectroscopy, Dirac Spinors, Quantum Interference & Force Mediation
1. **`baryon_calculator.py`** — Effective pair-spin mass calculator calibrating octet and decuplet baryons (`p/n`, `Delta+`, `Lambda`, `Sigma0`, `Xi0`, `Omega-`) against PDG 2024 masses.
2. **`bcc_unified_sim.py`** — 3D 6-face routing workload for 3-quark baryons, pure-gluon closed loops (`2,001.19 MeV` glueball mass gap above `BareT = 0` vacuum), gravitational wavefront lensing, and 2D-to-3D deadlocked core locking.
3. **`bcc_meson_sim.py`** — Ground-state `q qbar` meson spectrum (`pi`, `rho`, `K`, `K*`, `phi`, `D`, `D*`, `J/psi`, `B`, `B*`, `Upsilon`) plus linear color flux-tube stretching (`45 MeV/hop`) snapping at hop 7 (`315 MeV > 275 MeV`) into confined meson pairs.
4. **`bcc_em_wave_sim.py`** — 3D Maxwell link-flux conservation (`Gauss's law residual ~ 3.6e-16`), dipole wave propagation, and two-sublattice double-slit interference vs. which-slit sensor congestion.
5. **`bcc_born_pascal.py`** — Dual-channel (`+/-`) discrete Pascal random walk reproducing Born-rule dark interference nodes and converging toward the continuous wave equation as tick count `N` grows.
6. **`bcc_baryogenesis.py`** — 3-generation CKM Jarlskog CP-violation cascade (`J = 3.117e-5`) demonstrating why `N_gen = 1, 2` annihilate to `0` net matter while `N_gen = 3` yields `eta ~ 6.10e-10`, alongside the `100-tick` 3D axis cutoff blocking a 4th generation (`128 ticks > 100`).
7. **`bcc_virtual_carriers.py`** — Off-shell vacuum ledger loans (`Delta_E * Delta_t <= hbar/2`) unifying massless `1/r` photon/gravity flux conservation, massive `exp(-r/r0)/r` Yukawa weak-boson decay, and self-interacting `45 MeV/hop` gluon flux-tube bundling.
8. **`bcc_dirac4_spinor.py`** — 4-component Dirac spinor (`Dirac4`) on the 6-face cubic lattice (`±x, ±y, ±z` spatial faces + `gamma^0` rest-mass loop), verifying spin-1/2 `720°` double-cover sign reversal (`360° -> -psi`, `720° -> +psi`), unitary rest-mass Zitterbewegung (`P(L) <-> P(R)`), and orthogonal `+x` face wave-packet transport (`E = sqrt((pc)^2 + (m0c^2)^2)`).
9. **`bcc_em_recoil.py`** — 2-body electromagnetic link-flux attraction/repulsion and mass-gated barycenter recoil (`F_12 = -F_21`, `a = F / m`), showing how lower tick workload (mass) governs displacement regardless of charge sign (`e- vs p+`: `99.95% / 0.05%`, `p+ vs Xi-`: `58.48% / 41.52%`, `e- vs e+`: `50.00% / 50.00%`).

### Part B — Relativity, Gravity & Zero-Leak Horizons
10. **`bcc_3d_gravity.py`** — 3D 6-face Poisson `1/r` congestion profiles, wavefront lensing lag vs. impact parameter `b`, spherical deadlocked horizons, orthogonal zigzag wave trajectories, and relativistic momentum-to-gravity coupling.
11. **`bcc3dhorizonsim.py`** — Standalone `19x19x19` 3D horizon accretion probe verifying zero packet escapes (`Escaped: 0`) inside `r <= 3 l_P` (`W >= 100`) and outward horizon shell growth as a zero-leak workload storage tank.
12. **`bcc_3body_orbits.py`** — 3-body gravitational choreography comparing ledger-grid forces (`0.15`-cell smoothing cap) against unsoftened Newton for the Figure-8 periodic orbit (`min_sep = 0.677`) and Pythagorean 3-4-5 close encounter, plus finite-`c` retarded load phase shifts.
13. **`bcc_sr_emergence.py`** — Emergent Special Relativity from the `1 hop/tick` routing budget: Lorentz time dilation (`gamma = 1/sqrt(1 - beta^2)`), length contraction (`L = L0 / gamma`), exact dispersion `E^2 = (pc)^2 + (m0 c^2)^2`, and bounded relativistic velocity addition (`u + v <= c`).
14. **`bcc_gr_emergence.py`** — Emergent weak-field General Relativity from `epsilon(r) = W(r)/100 = r_s/r`: Schwarzschild `g_00` gravitational time dilation locking at `r_s = 3.0 l_P`, `2.0000x` Einstein photon deflection (`g_00` queue wait + `g_rr` orthogonal detour) with Shapiro delay, and `0.767%`-accurate relativistic perihelion precession.

### Part C — Dark Matter, CMB, Dark Energy & Galactic Core Spin
15. **`bcc_dark_matter.py`** — EM-neutral (`Q_EM = 0`) closed-loop dark-matter halos producing `0%` photon attenuation, positive gravitational lensing lag, flat galaxy rotation curves (`v ~ 19-21` vs. Keplerian `1/sqrt(r)` drop), and Bullet-Cluster collisionless halo/baryon separation (`+1.45 l_P` lensing offset).
16. **`bcc_halo_solver.py`** — Inverse rotation-curve halo solver reconstructing enclosed halo mass `M_halo(<r)`, discrete `Q_EM = 0` loop counts, outer `5.50 : 1` (`84.6%`) dark-to-baryon mass ratio, and pseudo-isothermal cored central density (`84.46 < 100 cap`) avoiding the divergent `1/r` NFW cusp.
17. **`bcc_cmb_spectrum.py`** — Cosmic Microwave Background cooling across `1 + z = 1099` (`2994.78 K -> 2.725 K`, `n_gamma = 410.50 cm^-3`), Planck blackbody radiance peaking at `160.2 GHz`, and 3D orthogonal plasma sound speed `c_s = c / sqrt(3)` placing the first acoustic peak at `l_1 = 220.0`.
18. **`bcc_dark_energy.py`** — Congestion-gated dark energy acting only on idle vacuum nodes (`W < 20`), keeping bound galaxies fixed (`10.00 l_P`) while intergalactic voids expand (`20.00 -> 32.89 l_P`) and flipping the cosmic deceleration parameter `q(z)` from positive to negative at `z_acc = 0.632`.
19. **`bcc_kugelblitz_spin.py`** — Converging star-ring photon web deadlock (`W(0) >= 100` radiation-seeded black hole vs. `W(0) < 100` bulgeless galaxies like M33), action–reaction angular momentum conservation (`L_core + L_stars = 0`), and outward `1/r^3` Lense–Thirring frame-dragging spin.

### Architectural Appendix (Standalone Stencil Benchmark)
* **`bcc_lattice_comparison.py`** (`test_bcc_lattice_comparison.py`, 4 tests) — Side-by-side comparison of the 6-face simple cubic stencil vs. the 8-link BCC stencil across 3D hop reachability, `1/r` Poisson spherical isotropy, and 3D Pascal quantum-walk dipole mirror planes.

---

## Automated Unit Test Suite (74 / 74 Master Tests Passing)

| Test Module | Target Module | Tests | Verified Physics & Ledger Invariants |
| :--- | :--- | :---: | :--- |
| `test_baryon_calculator.py` | `baryon_calculator.py` | 12 | Pair-spin calibration, Pauli exclusion, channel permutations |
| `test_bcc_unified_sim.py` | `bcc_unified_sim.py` | 5 | 6-face Steiner links, strange redraw lag, `2001 MeV` mass gap, 3D shell lock |
| test_bcc_meson_sim.py | bcc_meson_sim.py | 3 | q qbar ordering (pi to Upsilon), 3:1 hyperfine split, hop-7 string snap |
| test_bcc_em_wave_sim.py | bcc_em_wave_sim.py | 2 | Static/post-hop Gauss's law (~1e-16), two-sublattice double-slit fringes |
| test_bcc_born_pascal.py | bcc_born_pascal.py | 2 | Dual-channel conservation, dark nodes, wave-equation convergence |
| test_bcc_3d_gravity.py | bcc_3d_gravity.py | 7 | 3D Poisson 1/r decay, lensing symmetry, momentum-to-gravity coupling |
| test_bcc3dhorizonsim.py | bcc3dhorizonsim.py | 3 | r <= 3 horizon deadlock (0 escape), zero-leak storage growth |
| test_bcc_3body_orbits.py | bcc_3body_orbits.py | 3 | Figure-8 stability, Pythagorean 0.15-cap smoothing, finite-c phase lag |
| test_bcc_dark_matter.py | bcc_dark_matter.py | 3 | Q_EM = 0 invisible lensing, flat rotation curve, Bullet-Cluster offset |
| test_bcc_baryogenesis.py | bcc_baryogenesis.py | 6 | CKM Jarlskog invariant, N_gen >= 3 CP requirement, eta = 6.1e-10 cascade |
| test_bcc_virtual_carriers.py | bcc_virtual_carriers.py | 3 | Massless 1/r flux conservation, Yukawa weak cutoff, hop-7 gluon bundling |
| test_bcc_gr_emergence.py | bcc_gr_emergence.py | 3 | Schwarzschild g_00 dilation + horizon lock, 2.0x light bending, precession |
| test_bcc_sr_emergence.py | bcc_sr_emergence.py | 3 | Lorentz gamma dilation/contraction, E^2=(pc)^2+(m0c^2)^2, u+v <= c |
| test_bcc_halo_solver.py | bcc_halo_solver.py | 3 | Inverse M_halo(<r) & 5.5:1 ratio, zero-halo check, cored <100 cap vs. NFW |
| test_bcc_cmb_spectrum.py | bcc_cmb_spectrum.py | 3 | 2.725 K redshift cooling, 160.2 GHz Planck peak, c_s=c/sqrt(3) l_1=220 |
| test_bcc_dark_energy.py | bcc_dark_energy.py | 3 | Fixed bound galaxies vs. expanding voids, q(z) acceleration flip at z=0.632 |
| test_bcc_kugelblitz_spin.py | bcc_kugelblitz_spin.py | 4 | Light-web 100-cap deadlock, L_core + L_stars = 0 recoil, 1/r^3 frame-drag |
| test_bcc_dirac4_spinor.py | bcc_dirac4_spinor.py | 3 | 720° spinor double cover, unitary Zitterbewegung, +x chiral packet walk |
| test_bcc_em_recoil.py | bcc_em_recoil.py | 3 | Link-flux attraction/repulsion, p_1+p_2=0, mass-gated barycenter recoil |
| Master Suite Total | 19 Modules | 74 | All 74 master tests pass in ~2.5s (run_bcc_suite.py in ~5.5s) |
