# From Quantum Loops to Cosmic Horizons: Finite-Scope Coarse-Graining on the 6-Face Planck-Cube Ledger

## 1. Executive Summary: One Unified Accounting System Without a Quantum–Macro Split

In standard physics, microscopic quantum field theory and macroscopic General Relativity are treated as two separate frameworks that clash whenever length scales shrink toward zero (`r -> 0`), producing infinities (`1/r -> infinity`) in point-charge self-energy, black-hole singularities, and dark-matter NFW cusps.

In the **Quantized Space-Ledger (`spacetime-ledger`)** architecture, both regimes run on **one finite, discrete 3D cubic ledger** (`1.0 l_P^3` cells with **6 orthogonal faces**, `±x, ±y, ±z`). Every physical quantity has an explicit **scope** and a **hard finite ceiling**, allowing microscopic quark–gluon workloads to coarse-grain seamlessly into macroscopic mass, charge, gravity, and cosmic expansion without changing rules or hitting mathematical singularities.

---

## 2. Internal Component Accounting vs. External Coarse-Graining

A core principle of this ledger is **boundary encapsulation**: external cells do not need to inspect the internal quark and gluon routing inside a confined particle once its color loop closes.

| Scale & Scope | Active Ledger Variables | Physical Role | Corresponding Modules |
| :--- | :--- | :--- | :--- |
| **Internal Loop Scope** (`< 1 fm`, Sub-Hadronic) | `BareT` (flavor redraw lag), `RouteT` (6-face Steiner links), `SpinT` (pair-spin coupling), `45 MeV/hop` flux tubes | Determines hadron mass spectrum, glueball mass gap (`2,001 MeV`), and string breaking (`> 275 MeV`) | `baryon_calculator.py`, `bcc_unified_sim.py`, `bcc_meson_sim.py`, `bcc_virtual_carriers.py` |
| **Boundary Interface** (`1.0 l_P^3` Cell Surface) | Total Tick Budget `M = BareT + RouteT + SpinT`, Net Link Polarity `Q_EM ∈ {+1, 0, -1}`, Spinor Phase `Dirac4` | Summarizes internal complexity into three conserved exterior handles: Mass, Electric Charge, and Spin | `bcc_dirac4_spinor.py`, `bcc_em_recoil.py`, `bcc_em_wave_sim.py`, `bcc_born_pascal.py` |
| **Macroscopic & Cosmic Scope** (`1 fm` to `Gpc`) | Radial Workload `W(r)`, Idle Capacity `C_cap - W(r)`, Horizon Lock `W(r) >= 100`, `Q_EM = 0` Halo Loops | Drives `1/r` gravity, `g_00` time dilation, `2.0x` light bending, flat galaxy curves, CMB cooling, and void expansion | `bcc_3d_gravity.py`, `bcc3dhorizonsim.py`, `bcc_sr_emergence.py`, `bcc_gr_emergence.py`, `bcc_dark_matter.py`, `bcc_halo_solver.py`, `bcc_cmb_spectrum.py`, `bcc_dark_energy.py`, `bcc_kugelblitz_spin.py` |

### Why External Cells Only Need the Total Tick Budget (`M`)
1. **Color Confinement Closes the Internal Ledger:** Inside a proton (`uud`) or meson (`q qbar`), color flux tubes bind quarks with linear tension (`45 MeV/hop`) that snaps into new hadrons above `275 MeV`. Because zero net color charge leaks outside the loop, neighboring Planck cubes never compute individual quark-to-quark Steiner trees.
2. **Inertia as Loop Shifting Overhead (`a = F / m`):** From the outside, a particle's total internal tick count `M` acts as its inertial mass. Delivering a link-flux impulse `Δp` must shift all `M` internal ticks together across cube faces—explaining why a light electron (`0.511 MeV`) moves `1,836.15×` farther than a proton (`938.27 MeV`), while a proton moves `1.41×` farther than a heavier `Ξ⁻` (`1321.71 MeV`).
3. **Charge as Boundary Link Polarity (`Q_EM`):** Independent of scalar tick mass `M`, net outbound (`+1`) or inbound (`-1`) link flux across the 6 cube faces governs electromagnetic attraction (flux relief) and repulsion (flux pile-up), while balanced internal loops (`Q_EM = 0`, such as neutrons or dark-matter loops) carry full gravitational workload `M` with zero EM drag.

---

## 3. Finite Scopes & Hard Ceilings That Prevent Singularities

Every divergence in continuous physics is blocked on the 6-face ledger by four built-in architectural limits:

1. **Minimum Spatial Quantum (`1.0 l_P^3` Space-Filling Cube):** Eliminates `r = 0` point-particle infinities and avoids the checkerboard parity blind spots of 8-link BCC stencils (`bcc_lattice_comparison.py`).
2. **Maximum Signal Speed (`1 Orthogonal Face Hop / Tick = c`):** Enforces exact Lorentz time dilation (`gamma`), length contraction (`1/gamma`), relativistic dispersion `E^2 = (pc)^2 + (m0 c^2)^2`, and bounded velocity addition (`u + v <= c`).
3. **Maximum Flux-Tube Tension (`275 MeV` String-Breaking Threshold):** Prevents infinite linear quark separation energy by snapping stretched tubes into confined hadron pairs at hop 7 (`315 MeV > 275 MeV`).
4. **Maximum Node Throughput (`C_cap = 100 ticks/cycle`):**
   * **Black-Hole Storage Tank:** When central workload reaches `W(r) >= 100` (from matter infall or converging starlight *Kugelblitz* webs), outbound routing gates lock (`0` escape). Instead of collapsing to a singular point, excess workload expands the deadlocked boundary shell outward (`19 -> 105` nodes) as a zero-leak storage tank.
   * **Cusp-Free Dark Matter Halos:** Pseudo-isothermal `Q_EM = 0` loop halos level off below the `100-tick` ceiling (`84.46 < 100`), avoiding the unphysical `1/r` NFW central cusp.
   * **Congestion-Gated Dark Energy:** Vacuum expansion ticks only fire on idle nodes (`W < 20`), keeping high-load bound galaxies fixed in size while empty intergalactic voids expand and accelerate (`z_acc = 0.632`).

---

## 4. Reproducibility & Verification

All claims in this architectural summary map directly to executable, zero-dependency Python 3 modules (`74/74` master unit tests + `4/4` stencil comparison tests):
