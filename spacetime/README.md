# Client-Server 3D BCC Spacetime Network

A computational physics framework modeling spacetime as a **two-tier client-server architecture** built on a uniform, fixed-capacity **3D Body-Centered Cubic (BCC) 8-diagonal crystal lattice**:

- **Client Space (`bcc/`, `sr/`, `gr/`, `cosmo/`, `elements/`):** Observable 3D BCC spatial grid composed of Planck-scale **truncated octahedron Voronoi cells** (\(\approx 0.770\,V_P\)), where matter, virtual force carriers, gluon flux trees, light waves, clocks, atoms, and galaxies operate under a strict c = 1 diagonal hop/tick throughput limit (\(\sqrt{3}\,\ell_P / t_P\)).
- **Server Space (`serverside/`):** Private kernel state-binding tables carried invisibly during `redraw()` ticks, resolving multi-particle entanglement (`Bell`, `GHZ`), delayed-choice quantum erasure, thermal vacuum decoherence, and anti-FTL scrambling without faster-than-light client signaling.

These programs are toy models built on BCC lattice logic. Matches to measured values come partly from hand-set or calibrated inputs, so they are not independent predictions.

---

## Quick Start: Root Master Report & 15-Panel Unified Dashboard

From the root `spacetime/` directory, export all six physics pillars into `master_report.json` and render the 15-panel (`5x3`) overview chart (`master_dashboard.png`):

```bash
python3 export_master_report.py
python3 plot_master_dashboard.py
```

---

## Six-Pillar Repository Structure

```text
spacetime/
├── README.md                        # Top-level unified architecture overview
├── export_master_report.py          # Unified JSON exporter across all 6 subdirectories
├── plot_master_dashboard.py         # 15-panel (5x3) master dashboard generator (master_dashboard.png)
├── bcc/                             # 1. Microscopic 3D BCC Lattice, QCD, Carriers, Spinors & Lab Bench
│   ├── README.md
│   ├── bcc_unified_engine.py        # 5-module engine (baryons, glueball gap, lensing, horizons, double-slit, isotropy)
│   ├── bcc_meson_sim.py             # 11 ground-state q-qbar mesons (pi..Upsilon) & 4-hop BCC string breaking
│   ├── bcc_virtual_carriers.py      # Virtual force-carrier waves: photon (1/r), weak (Yukawa) & gluon bundling
│   ├── bcc_dirac4_spinor.py         # 4-component Dirac spinor (720° double cover, Zitterbewegung, 3D BCC walk)
│   ├── bcc_orbital_sim.py           # Refractive wavepacket orbits, perihelion precession & horizon capture
│   ├── bcc_workbench_interferometer.py # Tabletop 976 nm diode + torsion pendulum + interferometer test
│   ├── plot_bcc_results.py          # 4-panel benchmark dashboard generator
│   ├── plot_bcc_3d_cell.py          # 4-panel 3D wireframe (unit cell, truncated octahedron ~0.77 V_P, Steiner tree, glueball)
│   └── animate_bcc_quarks.py        # Animated 3D GIF of hopping quarks & dynamic Steiner flux tree
├── serverside/                      # 2. Non-Local Server State Bus, Security Firewall & Octant Speedups
│   ├── README.md
│   ├── entangled_bell_server.py     # Spacelike-separated Bell CHSH benchmark (|S| > 2.0, 50/50 marginals)
│   ├── spacetime_server_api.py      # Zero-metadata ClientParticle + 4-primitive kernel API (Bell & GHZ sweeps)
│   ├── quantum_eraser_server.py     # Delayed-choice quantum eraser (complementary fringe / anti-fringe sorting)
│   ├── dense_coding_firewall.py     # Anti-FTL signaling firewall, mid-flight scrambling & 100% 4-state dense coding
│   └── octant_huygens_fast.py       # 8x octant-symmetry continuum convergence (R=60..240 -> 0.056% isotropy error)
├── sr/                              # 3. Special Relativity (Lorentz Kinematics & Dispersion)
│   ├── README.md
│   └── bcc_sr_emergence.py          # BCC zigzag clock gamma, E^2=(pc)^2+(m0c^2)^2 & bounded velocity addition
├── gr/                              # 4. Macroscopic General Relativity (Schwarzschild & Kerr Metrics)
│   ├── README.md
│   ├── bcc_gr_emergence.py          # 3D BCC Poisson relaxation W(r), g_00 time dilation, 2x Einstein deflection & precession
│   ├── bcc_frame_dragging.py        # Kerr g_t_phi azimuthal drag, prograde/retrograde period split & 1/r^3 scaling
│   └── bcc_kugelblitz_spin.py       # Radiation-seeded black hole (W >= 100), recoil ledger & Kerr spin parameter a*
├── cosmo/                           # 5. Emergent Cosmology (Dark Matter Halos, Dark Energy & CMB)
│   ├── README.md
│   ├── bcc_dark_matter.py           # Q_EM=0 BCC 4-link loop halos, flat rotation curves & Bullet Cluster offset
│   ├── bcc_halo_solver.py           # Inverse rotation-curve solver & 100-tick cusp-to-core density saturation
│   ├── bcc_dark_energy.py           # Congestion-gated void expansion & z_acc = 0.632 cosmic acceleration flip
│   └── bcc_cmb_spectrum.py          # CMB redshift cooling (T_0 = 2.725 K), Planck radiance & l_1 = 220.00 peak
└── elements/                        # 6. Atomic Elements, Nuclear Fusion/Fission & Molecular Chemistry
    ├── README.md
    ├── bcc_hydrogen_atom.py         # Hydrogen quark/gluon/electron breakdown, Bohr lines & 10 K->100,000 K phases
    ├── bcc_nuclear_fusion.py        # Coulomb barrier vs. gluon Steiner merge, Gamow tunneling & D-T vs. p-p fusion
    ├── bcc_nuclear_fission.py       # 2H -> 56Fe -> 235U binding curve, neutron split (202.5 MeV) & k_eff chain reaction
    ├── bcc_multi_electron_atoms.py  # 1H, 4He, and 12C pion binding, Pauli shell screening (Z_eff) & phase extremes
    └── bcc_molecular_chemistry.py   # CH4 (109.47° BCC tetrahedral), H2O (104.45° dipole) & CO2 covalent chemistry
```

---

## Unified Physics Summary Across All Six Pillars

| Physics Domain | Directory | Network Mechanism | Key Simulation Benchmark |
| :--- | :---: | :--- | :--- |
| **QCD, Carriers & Spin-1/2** | `bcc/` | $q\bar{q}$ tubes, 3-quark Steiner trees, 4-link gluon cycles, virtual carrier waves & Dirac-4 spinors | All 11 mesons within `0.1–15.9 MeV` of PDG; Nucleon = `927.3 MeV`; Glueball/N = **`1.742`**; 4-hop gluon snap |
| **Quantum Interference** | `bcc/` | Pascal zigzag path counting with $90^\circ$ ($i$) turn phases & discrete node threshold clicks | Sharp destructive dark fringes at `y = ±12` that wash out under slit detection |
| **Continuum Isotropy** | `bcc/`, `serverside/` | Multi-path Huygens wavefront spreading across Kelvin truncated-octahedron cells ($\approx 0.770\,V_P$) | Spherical anisotropy error drops from `0.840%` (`R=30`) to **`0.056%`** (`R=240`) |
| **Entanglement & Eraser** | `serverside/` | Opaque zero-metadata `ClientParticle` + private server binding tables carried during `redraw()` | Bell **`|S| = 2.8544`**, GHZ **`M = 4.0000`**, and complementary `|+>` / `|->` eraser fringes |
| **No-Signaling Firewall** | `serverside/` | Random outcome injection on `decohere()` + one-time-pad transit scrambling | FTL exploit blocked (`0.4939` noise); 4-state superdense decoding = **`100.0%`** at $v \le c$ |
| **Special Relativity** | `sr/` | Orthogonal split of $c = 1$ hop/tick budget between translation ($\beta$) and internal BCC zigzag clocks | Exact $\gamma = 1/\sqrt{1-\beta^2}$, invariant $m_0 = 927.3000\text{ MeV}$, and bounded $u \oplus v \le c$ |
| **General Relativity** | `gr/`, `bcc/` | 3D BCC Poisson congestion $W(r)/C_{\text{cap}} = r_s/r$, horizon deadlocks, and azimuthal spin curl | Exact **`2.0000x`** Einstein deflection, rosette perihelion precession, Kugelblitz BH & $1/r^3$ Kerr drag |
| **Cosmology & CMB** | `cosmo/` | $Q_{\text{EM}}=0$ 4-link loop halos, congestion-gated void expansion ($W < 20$) & $c_s = c/\sqrt{3}$ plasma | Flat rotation curve (`84.6%` dark), Bullet Cluster offset, **$z_{\text{acc}} = 0.632$** & **$\ell_1 = 220.00$** |
| **Elements & Chemistry** | `elements/` | Gluon/pion nuclear binding curves, Gamow tunneling, Pauli shells ($Z_{\text{eff}}$) & $sp^3$ covalent bonds | **`56Fe` peak (`8.79 MeV/nuc`)**, `D-T` (`17.59 MeV`) & `235U` fission, **`656.1 nm` H-alpha**, and **`104.45°` liquid $\text{H}_2\text{O}$** |
