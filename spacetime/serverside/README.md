# Client-Server Spacetime Layer (`serverside/`)

> **Fixed copy notes.** The Bell/GHZ/eraser correlations are INSERTED by design: P(opposite) = cos²(Δ/2) and |amp|² weights live in a non-local server table (checklist "local cells" tension, OD4). `entangled_bell_server.py` uses angles 0/45 vs 22.5/67.5 and gives S ≈ 2.41 (correct for those angles; 2√2 needs 0/90 vs 45/135 as in the API sweep). `bcc_orbital_sim.py`: FIXED periapsis-advance measurement (−88.22°/orbit for the 0.84 v_circ ellipse; circular ~0), tilt now rotates rather than adds speed; field c_eff = 1/(1+k/r) is INSERTED. `octant_huygens_fast.py`: dt = 0.55 is a declared knob.

This directory implements the **non-local backend state architecture**, **zero-metadata client encapsulation**, and **8-fold octant symmetry acceleration** complementing the 3D BCC spatial lattice (`bcc/`).

---

## Architectural Separation: Client Space vs. Server Space

| Layer | Physical Role | Visibility & Locality Rules |
| :--- | :--- | :--- |
| **Client Space (`bcc/`)** | Observable 3D BCC crystal lattice where opaque packets (`ClientParticle`), waves, and detectors reside. | Strictly bounded by $c = 1$ BCC diagonal hop per tick. Clients hold **zero entanglement metadata**, enforcing the no-signaling theorem ($P(+1) = 0.500$). |
| **Server Space (`serverside/`)** | Private kernel binding tables (`_packet_to_eid`, `_resolved_values`) carried during `redraw()`. | Updates linked correlation records instantaneously on `read()` or ambient vacuum `decohere()`, reproducing Bell/GHZ non-locality and quantum erasure without FTL client signaling. |

---

## The 4-Primitive Server Instruction Set (`spacetime_server_api.py`)

1. **`x = entangle(a, a2, a3, ...)`** — Binds $N$ opaque client packets into a private server correlation group `x`.
2. **`redraw(a, vector)`** — Server advances packet `a` along a 3D BCC diagonal $\langle \pm 1, \pm 1, \pm 1 \rangle$ while checking its private binding table for ambient vacuum noise.
3. **`read(a, basis)`** — Triggered when packet `a` strikes a detector; resolves the shared server record against the measurement basis and updates all linked members.
4. **`decohere()`** — Spontaneous no-argument vacuum fluctuation collapse (`random()`), severing shared server pointers under thermal noise.

---

## Scripts & Quick Start

| File | Description | Run Command |
| :--- | :--- | :--- |
| `entangled_bell_server.py` | Simultaneous Alice & Bob measurements across 48 BCC hops verifying Bell CHSH violation (`S > 2.0`) with 50/50 local marginals. | `python3 entangled_bell_server.py --pairs 10000 --distance 48` |
| `spacetime_server_api.py` | Zero-metadata client benchmark testing **2-particle Bell (`|S|`)** and **3-particle GHZ (`Mermin M`)** states across a thermal vacuum noise sweep. | `python3 spacetime_server_api.py` |
| `quantum_eraser_server.py` | Delayed-choice quantum eraser sorting raw `D0` clicks into `Z`-basis which-path clumps vs. complementary `|+>` fringes and `|->` anti-fringes. | `python3 quantum_eraser_server.py` |
| `octant_huygens_fast.py` | Uses 8-fold octant reflection symmetry ($x,y,z \ge 0$) to accelerate large-radius ($R = 60 \to 240$) 3D BCC wavefront sweeps by **8×**. | `python3 octant_huygens_fast.py --radius 60 120 180 240` |

---

## Key Benchmark Findings

### 1. Bell CHSH & 3-Particle GHZ Decoherence Sweep (`spacetime_server_api.py`)

| Vacuum Noise / Hop | 2-Particle Bell `|S|` (Classical $\le 2.0$) | 3-Particle GHZ Mermin `M` (Classical $\le 2.0$) | Regime |
| :---: | :---: | :---: | :--- |
| **`0.000`** | **`2.8544`** | **`4.0000`** | Full Quantum Non-Locality |
| **`0.005`** | **`2.4912`** | **`3.4496`** | Non-Local (Weak Thermal Noise) |
| **`0.015`** | `1.9712` | **`2.5768`** | Bell Decohered / GHZ Still Non-Local |
| **`0.030`** | `1.3488` | `1.6272` | Classical / Decohered |
| **`0.060`** | `0.6120` | `0.6416` | High-Noise Classical Limit |

### 2. Ultra-Large Radius Continuum Convergence (`octant_huygens_fast.py`)

| Target Radius ($R$) | Octant Runtime | Mean Speed ($R / \text{Tick}$) | Mean $1/r$ Shapiro Lag | Mean Spherical Isotropy Error |
| :---: | :---: | :---: | :---: | :---: |
| **`R = 60`** | `2.40s` | `0.3403` | `36.20` ticks | **`0.394%`** |
| **`R = 120`** | `47.11s` | `0.3516` | `47.20` ticks | **`0.104%`** |
| **`R = 180`** | `267.77s` | `0.3586` | `52.80` ticks | **`0.092%`** |
| **`R = 240`** | `833.43s` | `0.3635` | `56.40` ticks | **`0.056%`** |
