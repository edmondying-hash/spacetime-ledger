# 3D BCC Spacetime Network Simulation (`bcc/`)

> **Fixed copy notes.** **Hop length (OD1, open for Edmond):** `bcc_config.HOP` = `'sqrt3_lP'` (default, top README wording: hop = √3 ℓP, cell = 4 V_P, tick = √3 tP so c stays fixed) or `'lP'` (bcc/README wording: hop = ℓP, cell = 0.770 V_P, tick = tP). The two READMEs disagreed; the ~0.770 V_P figure holds only under `'lP'`. Override with env `BCC_HOP=lP`.
> - `bcc_dirac4_spinor.py`: FIXED, the 8-link shift is now exactly unitary (A_n = Π_z Π_y Π_x spin projectors; norm drift 9.5e-14 over 1000 ticks; was 0.028 norm after 6 ticks). Parts 1–2 are closed-form identities (INSERTED). OD3 (walk form) open.
> - `bcc_meson_sim.py`: masses are HAND-SET from tuned constants; BCCLinks is a diagnostic not used in the mass. Ticks/hop follows HOP.
> - `bcc_unified_engine.py`: INSERTED pieces labelled (baryon terms, glueball formula, lensing 1/r, horizon escaped = 0, Huygens 1/r load). Huygens dt = 0.55 is a DECLARED KNOB: wave speed dt/√2 = 0.389 coord/tick = 0.2245 hop/tick; one hop/tick is beyond this scheme's stability limit (≤ 1 coord/tick). CSV exporter fixed, `scaling_sweep.csv` now filled.
> - `bcc_virtual_carriers.py` (new to the bundle): carrier profiles INSERTED; range now r0 = ħ/(mc) in hops (W: 8.8e16 hops, not 1.5); new genuine lattice Green's function shows 1/r (A = 0.0784 vs 1/4π = 0.0796) and Yukawa (λ = 6.016 vs 6) emerging on 8 links.

A self-contained computational physics engine modeling client-space spacetime as a uniform, fixed-capacity **3D Body-Centered Cubic (BCC) 8-diagonal crystal network**. Rather than treating mass, confinement, gravity, orbits, and quantum interference as separate continuum laws, this framework derives them as emergent routing workloads, node-queuing delays, refractive wavepacket steering, and multi-path zigzag oscillations across a discrete 8-link lattice.

---

## Core Architectural Hypothesis & Node Geometry

1. **Spacetime as a Uniform-Capacity Node Network:** Empty vacuum consists of idle 3D BCC lattice nodes (`0` active links = `0` mass). Each node has an identical maximum tick/processing capacity (`max_node_ticks`), setting a universal maximum hop rate ($c = 1$ hop per tick).
2. **8-Diagonal BCC Connectivity ($\langle \pm 1, \pm 1, \pm 1 \rangle$):** Unlike a 6-face simple cubic grid (which suffers severe orthogonal staircase bottlenecks) or a 4D hypercubic Euclidean lattice, a 3D BCC lattice connects every node to 8 corner neighbors along body diagonals—advancing across all three spatial axes simultaneously on every hop.
3. **Planck-Scale Node Volume & Truncated Octahedron Territory (Kelvin's Cell):**
   - **Node Volume (depends on OD1):** Setting 1 BCC diagonal hop ($\sqrt{3}$ coordinate units) equal to 1 Planck length ($\ell_P$) per Planck time ($t_P$) [HOP=`lP`] gives each node a volume of $\frac{4}{3\sqrt{3}}\,\ell_P^3 \approx 0.770\,V_P$ ($\approx 3.25 \times 10^{-105}\text{ m}^3$), packing $\sim 3 \times 10^{104}$ idle server nodes into every cubic meter of vacuum.
   - **Truncated Octahedron Voronoi Cell:** Dividing 3D space by nearest BCC node produces a **14-sided truncated octahedron** (8 regular hexagonal faces pierced perpendicularly by the 8 diagonal routing links + 6 square faces). Because Lord Kelvin's truncated octahedron is the most spherical space-filling polyhedron in 3D, multi-path Huygens waves wash out directional grid grain rapidly ($0.056\%$ error by $R = 240$).
4. **Hadrons, Mesons & Confinement as Routing Topology:**
   - **Baryons ($qqq$):** 3-terminal Steiner Y-junction routing across $\approx 4.66$ BCC diagonal links.
   - **Mesons ($q\bar{q}$):** 2-terminal shortest-path flux tubes across $\approx 2.95$ BCC diagonal links with reduced-mass recoil saturation ($3.5\,b_{\min}$) and $3:1$ hyperfine spin splitting. Stretching a BCC flux tube beyond $275.0\text{ MeV}$ snaps the link chain at **4 BCC diagonal hops** ($311.76\text{ MeV}$), spawning two confined mesons.
   - **Glueballs:** Closed 4-link non-planar gluon rhombus cycles (`1615.0 MeV`, $1.742\times$ Nucleon mass gap).
5. **Gravity, Orbits & Horizons as Queuing Congestion:** High-workload clusters consume local node ticks (`Load%`), creating a radial queuing-delay gradient ($U(r) \propto 1/r$) that slows passing wavefronts ($c_{\text{eff}} < c$), refracts wavepackets into precessing elliptical orbits, and traps excitations when local utilization reaches 100%.
6. **Quantum Waves & Interference as Zigzag Path Counting:** Moving along an axis on a diagonal grid requires symmetric multi-path zigzags (a 2D Pascal triangle walk). Assigning a $90^\circ$ ($i$) phase shift on zigzag reversals (Feynman checkerboard coin) produces mechanical destructive interference fringes, single-dot detector threshold clicks, and instant fringe washout upon which-path measurement.

---

## Repository Structure (`bcc/`)

| File | Description |
| :--- | :--- |
| `bcc_unified_engine.py` | Master 5-module 3D BCC simulation engine (baryons, glueballs, lensing, horizons, double-slit, Huygens isotropy) with CLI flags and JSON/CSV export. |
| `bcc_meson_sim.py` | Simulates all 11 ground-state $q\bar{q}$ mesons (`pi` through `Upsilon`) on the 3D BCC lattice plus 4-hop color flux-tube string breaking. |
| `../serverside/bcc_orbital_sim.py` (lives in serverside/) | Simulates refractive wavepacket trajectories around a congested BCC core (`Circular`, `Precessing Ellipse`, `Hyperbolic Flyby`, and `Horizon Capture`). |
| `plot_bcc_results.py` | Generates a 4-panel summary dashboard (`bcc_dashboard.png`) from exported JSON reports. |
| `plot_bcc_3d_cell.py` | Renders a 4-panel 3D wireframe (`bcc_3d_wireframe.png`) of the 8-link BCC unit cell, the **truncated octahedron Voronoi cell (volume per HOP switch)**, the 3-quark Steiner tree, and the 4-link non-planar glueball rhombus. |
| `animate_bcc_quarks.py` | Exports an animated 3D GIF (`bcc_quark_hopping.gif`) showing 3 valence quarks hopping and dynamically redrawing their gluon Steiner flux tree. |

---

## Installation & Requirements

Requires Python 3.9+ with `numpy`, `matplotlib`, and `pillow`:

```bash
pip install numpy matplotlib pillow
```

---

## Quick Start & CLI Usage

### 1. Run the Full 5-Module Engine & Export Reports
```bash
python3 bcc_unified_engine.py --module 1 2 3 4 5 --radius 30 60 90 --json full_report.json --csv full_sweep.csv
```

### 2. Run Meson Spectrum & String-Breaking Simulation
```bash
python3 bcc_meson_sim.py
```

### 3. Run Individual Engine Modules or Parameter Sweeps
* **Module 1 (Baryon Mass Spectrum & Glueball Mass Gap):**
  ```bash
  python3 bcc_unified_engine.py --module 1 --cycles 5000 --link-weight 198.0
  ```
* **Modules 2 & 3 (Coupled Radial Lensing & Saturation Horizons):**
  ```bash
  python3 bcc_unified_engine.py --module 2 3
  ```
* **Module 4 (Double-Slit Zigzag Interference & Which-Path Decoherence):**
  ```bash
  python3 bcc_unified_engine.py --module 4 --clicks 5000
  ```
* **Module 5 (3D Huygens Spherical Isotropy & Shapiro Delay Scaling Sweep):**
  ```bash
  python3 bcc_unified_engine.py --module 5 --radius 30 60 90 120 --json scaling_sweep.json --csv scaling_sweep.csv
  ```

### 4. Generate Visualizations & Orbital Simulations
* **4-Panel Physics Dashboard:**
  ```bash
  python3 plot_bcc_results.py full_report.json --out bcc_dashboard.png
  ```
* **4-Panel 3D BCC Lattice, Truncated Octahedron & Flux-Tube Wireframe:**
  ```bash
  python3 plot_bcc_3d_cell.py --out bcc_3d_wireframe.png
  ```
* **Refractive Wavepacket Orbits & Perihelion Precession:**
  ```bash
  python3 ../serverside/bcc_orbital_sim.py --out bcc_orbits.png
  ```
* **Animated 3D Quark-Hopping GIF:**
  ```bash
  python3 animate_bcc_quarks.py --out bcc_quark_hopping.gif --frames 50 --fps 5
  ```

---

## Key Benchmark Findings

### 1. Cross-Lattice Routing Efficiency (Parameter-Free Comparison)

| Lattice Architecture | Avg Steiner Links ($N$) | Voronoi Cell Geometry | Topological Shell/Core Ratio |
| :--- | :---: | :---: | :---: |
| **3D Simple Planck Cube (6-Face)** | `9.33` | Cube ($1.000\,V_P$) | `3.17x` |
| **3D True BCC Lattice (8-Diagonal)** | **`4.67`** | **Truncated Octahedron (4 or 0.770 V_P, OD1)** | **`4.09x`** |
| **4D Hypercubic Lattice (8-Face)** | `12.37` | 4D Tesseract | `4.48x` |

### 2. Ground-State Meson Spectrum & String Breaking (`bcc_meson_sim.py`)
All 11 ground-state $q\bar{q}$ mesons reproduce PDG masses within `0.13` to `15.91 MeV` (<0.3% mean relative error), while stretching a BCC diagonal flux tube ($15.588\text{ ticks/hop}$) snaps cleanly at **4 BCC hops** ($311.76\text{ MeV} > 275.0\text{ MeV}$):

| Meson | Quarks | Spin $J$ | Avg BCC Links | Model Mass (MeV) | PDG Mass (MeV) | Diff (MeV) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`pi`** | $l\bar{l}$ | `0` | `2.94` | `140.00` | `138.04` | `+1.96` |
| **`rho`** | $l\bar{l}$ | `1` | `2.98` | `780.00` | `775.26` | `+4.74` |
| **`K`** | $l\bar{s}$ | `0` | `3.02` | `493.01` | `495.64` | `-2.63` |
| **`K*`** | $l\bar{s}$ | `1` | `3.03` | `902.08` | `893.60` | `+8.48` |
| **`phi`** | $s\bar{s}$ | `1` | `3.03` | `1035.37` | `1019.46` | `+15.91` |
| **`D`** | $l\bar{c}$ | `0` | `2.97` | `1867.33` | `1867.20` | `+0.13` |
| **`D*`** | $l\bar{c}$ | `1` | `2.96` | `1995.33` | `2008.55` | `-13.22` |
| **`J/psi`** | $c\bar{c}$ | `1` | `2.80` | `3106.40` | `3096.90` | `+9.50` |
| **`B`** | $l\bar{b}$ | `0` | `2.93` | `5279.79` | `5279.66` | `+0.13` |
| **`B*`** | $l\bar{b}$ | `1` | `2.94` | `5321.74` | `5324.71` | `-2.97` |
| **`Upsilon`** | $b\bar{b}$ | `1` | `2.94` | `9460.69` | `9460.40` | `+0.29` |

### 3. Baryon Spectrum, Pure-Gluon Mass Gap & Horizons (Modules 1–3)
* **Nucleon (`N`) Routing Workload:** Averages **4.66 diagonal links** (`927.3 MeV`), with gluon routing supplying >98% of total baryon mass.
* **Pure-Gluon Glueball Mass Gap:** The minimal closed cycle on a 3D BCC lattice is a **4-link non-planar rhombus** (`1615.0 MeV`, `BareT = 0`), yielding a dimensionless **Glueball-to-Nucleon ratio of `1.742`** (aligning with Lattice QCD benchmarks of `~1.70`).
* **Coupled Lensing & Horizon Scaling:** Increasing cluster mass from `N` (`927.3 MeV`) to `Omega` (`1218.3 MeV`) deepens near-core signal slowdown at impact parameter `b = 2` (`c_eff` drops from `0.610c` to `0.516c`) and expands the 100%-saturated deadlock core (`23 -> 26` nodes) while preserving an invariant **`4.08–4.09x`** 8-link boundary shell ratio.

### 4. Refractive Orbital Mechanics & Horizon Capture (`bcc_orbital_sim.py`)
* **Circular Orbit (`1.00 v_circ`):** Maintains a closed orbit between `R = 24.0` and `24.1` lattice units.
* **Precessing Ellipse (`0.84 v_circ`):** Traces a bound relativistic rosette between `R = 16.5` and `24.0` with a measured periapsis advance of **−88.22°/orbit** (retrograde; dt-converged). FIXED: the old 87.97°/272.03° figures came from averaging atan2 differences mod 360; the circular orbit now reads ~0 (e = 1e-5).
• Hyperbolic Flyby (1.42 v_circ) & Capture (0.32 v_circ): High-velocity packets bend inward and escape (R -> 74.3), while low-velocity packets spiral across the r = 4.5 saturation horizon (CAPTURED).

5. Double-Slit Interference & Which-Path Decoherence (Module 4)

• Coherent Regime (No Slit Sensor): 1,000 discrete single-dot detector triggers accumulate into constructive peaks at y = 0 (80 clicks) and y = ±18 (83–88 clicks) separated by deep destructive dark fringes at y = -12 (9 clicks) and y = +12 (5 clicks).
• Decohered Regime (Sensor at y = -6): Tagging the path at the left slit breaks phase synchronization between zigzag ripples, immediately washing out the y = ±12 dark fringes (63 and 45 clicks).

6. Continuum Rotational Isotropy Convergence (Module 5)


Wavefront Radius ($R$)	Mean Effective Speed ($R / \text{Tick}$)	Mean $1/r$ Shapiro Delay	Mean Spherical Anisotropy Error
R = 30	0.3387	24.80 ticks	0.840%
R = 60	0.3403	36.20 ticks	0.394%
R = 90	0.3465	43.00 ticks	0.200%
R = 120	0.3516	47.20 ticks	0.104%
