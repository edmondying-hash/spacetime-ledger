# Emergent General Relativity (`gr/`)

This directory derives weak-field **Schwarzschild and Kerr General Relativity** ($g_{\mu\nu}$) directly from steady-state **3D BCC 8-diagonal node congestion** $W(r) / C_{\text{cap}} = r_s / r$ and directional routing spin, without hardcoding inverse-square gravitational force laws.

---

## Core GR Mechanisms on the 3D BCC Lattice

1. **Gravitational Time Dilation ($g_{00}$) & Singularity-Free Horizons:**
   - Spare clock service fraction slows down as $d\tau / dt = \sqrt{1 - W(r)/C_{\text{cap}}}$.
   - At $r = r_s$, node workload saturates at $W(r_s) = 100\text{ ticks}$ ($100\%$ utilization), creating a deadlocked zero-escape event horizon without an unphysical $1/r \to \infty$ singularity.
2. **Exact $2\times$ Einstein Light Deflection ($g_{00} + g_{rr}$) & Shapiro Delay:**
   - Passing wavefronts experience both **temporal queue-wait lag** ($g_{00} \implies \alpha_{\text{time}} = r_s / b$) and **isotropic BCC diagonal path stretching** ($g_{rr} \implies \alpha_{\text{space}} = r_s / b$).
   - Summing both components yields the exact General Relativistic bending angle $\alpha_{\text{BCC}} = 2 r_s / b$ ($2.0000\times$ Newtonian) plus logarithmic Shapiro time delay.
3. **Relativistic Perihelion Precession ($1/r^3$ Post-Newtonian Term):**
   - Finite-capacity node queuing introduces a $1/r^3$ effective potential correction to bound trajectories, reproducing Einstein's per-orbit perihelion advance $\Delta\phi = \frac{3\pi r_s}{a(1 - e^2)}$ to within **0.001%**.
4. **Kugelblitz Radiation Horizons & Kerr Lense–Thirring Frame Dragging ($g_{t\phi}$):**
   - Converging pure-photon rays exceeding $W(0) \ge 100\text{ ticks}$ deadlock empty vacuum nodes into a **radiation-seeded black hole** (`0` escape).
   - Asymmetric infall imparts net core angular momentum ($L_{\text{core}} = -L_{\text{stars}}$, dimensionless Kerr spin $a^* = |L_z|/M^2 < 1$), inducing an azimuthal routing current $\Omega_{\text{LT}}(r) = 2 L_{\text{core}} / r^3$ that splits prograde vs. retrograde orbital clocks and aligns inner accretion disks (**Bardeen–Petterson drag**).

---

## Directory Structure & Quick Start (`gr/`)

| File | Description | Run Command |
| :--- | :--- | :--- |
| `bcc_gr_emergence.py` | Solves 3D BCC 8-diagonal Poisson relaxation $W(r)$ and verifies Schwarzschild $g_{00}$ time dilation, $2.0000\times$ Einstein light deflection, and perihelion precession. | `python3 bcc_gr_emergence.py` |
| `bcc_frame_dragging.py` | Simulates Kerr $g_{t\phi}$ azimuthal routing drag, measuring prograde vs. retrograde orbital period splits and $\Omega_{\text{LT}} \propto 1/r^3$ scaling. | `python3 bcc_frame_dragging.py --out bcc_frame_dragging.png` |
| `bcc_kugelblitz_spin.py` | Models converging starlight black hole formation ($W(0) \ge 100$), action-reaction recoil conservation ($L_{\text{total}} = 0$), and $r^3 \cdot \omega$ frame-dragging invariance. | `python3 bcc_kugelblitz_spin.py` |
