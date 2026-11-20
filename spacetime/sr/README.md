# Emergent Special Relativity (`sr/`)

This directory derives **Lorentz kinematics, relativistic energy-momentum dispersion, and bounded velocity addition** directly from the finite **1-hop-per-tick routing budget ($c = 1.0\text{ BCC diagonal hop/tick} = \sqrt{3}\,\ell_P / t_P$)** of the 3D Body-Centered Cubic (BCC) spacetime network.

---

## Core SR Mechanisms on the 3D BCC Lattice

1. **Finite Tick-Budget Split ($\gamma = 1/\sqrt{1 - \beta^2}$):**
   - Every node hop advances by a fixed diagonal distance ($c = 1$). When a bound hadron or clock translates across the grid at speed fraction $\beta = v/c$, a fraction $\beta$ of its hop budget goes into forward translation, leaving $\sqrt{1 - \beta^2}$ for internal transverse zigzag bounces.
   - This mechanically dilates internal clock ticks ($T_{\text{moving}} / T_{\text{rest}} = \gamma$) and contracts spatial wavelengths ($L = L_0 / \gamma$) without postulating continuous Minkowski spacetime as an axiom.
2. **Orthogonal Dispersion ($E^2 = (pc)^2 + (m_0 c^2)^2$):**
   - Internal gluon/quark routing workload ($m_0 = 927.3\text{ MeV}$ for the 3D BCC Nucleon) and translational momentum ticks ($p c = \gamma m_0 \beta c^2$) occupy orthogonal components of the node processing budget, satisfying the Pythagorean dispersion relation and preserving invariant rest mass $m_0$ across all boost frames.
3. **Bounded Velocity Addition & Invariance of $c$:**
   - Composing two collinear lattice drift rates obeys $(u + v)/(1 + uv/c^2) < c$, preventing any massive cluster from breaching the 1-hop/tick throughput limit while keeping massless BCC waves ($u = c$) strictly invariant at $c$.

---

## Quick Start & Benchmark Highlights (`bcc_sr_emergence.py`)

```bash
python3 bcc_sr_emergence.py
```

| Speed Fraction ($\beta = v/c$) | BCC Zigzag $\gamma$ | Clock Rate ($1/\gamma$) | Contracted Length ($L_0=10$) | Momentum $pc$ (MeV) | Total Energy $E$ (MeV) | Invariant $m_0$ (MeV) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`0.00`** | `1.000000` | `1.000000` | `10.0000` | `0.00` | `927.30` | **`927.3000`** |
| **`0.50`** | `1.154701` | `0.866025` | `8.6603` | `535.38` | `1070.75` | **`927.3000`** |
| **`0.80`** | `1.666667` | `0.600000` | `6.0000` | `1236.40` | `1545.50` | **`927.3000`** |
| **`0.95`** | `3.202563` | `0.312250` | `3.1225` | `2821.25` | `2969.74` | **`927.3000`** |
| **`0.99`** | `7.088812` | `0.141067` | `1.4107` | `6507.72` | `6573.46` | **`927.3000`** |

