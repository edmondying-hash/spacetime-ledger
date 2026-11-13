# Layered test program for the §9 open problems

Replaces the first draft (`simulation-test-plan.md`) as the working plan.
Target: **open problems 1–19 and server-side items S1–S7**, pp. 68–71 of the PDF,
plus the three objectives in §8.

The approach is bottom-up. Each layer is a software milestone with a frozen interface,
an entry gate, and an exit gate. A later layer may not change a lower layer's conventions;
if it must, the lower layer is re-run. This is the only way to keep toy results comparable
across the paper's tables.

---

## 1. Layer map

| Layer | Content | Open problems | Exit gate |
|---|---|---|---|
| **L0** | Substrate, conventions, exactness harness | OP1 (foundation) | V1–V5 pass; units frozen |
| **L1** | Free spectrum: doublers, chirality, dispersion, ν | OP3 (spectrum), OP15, OP16 | gap table reproduced; zero modes classified; vector `n=2`; ν from rule |
| **L2** | Read-out and statistics | S1, S7, OP2, S2, OP3 (shared records) | Born weights without insertion; κ bound; exchange phase −1; order independence |
| **L3** | Gravity | OP4–OP11, OP17 | γ=β=1 from rule; EP η→0; tensor source; 1-loop anisotropy suppressed |
| **L4** | Matter spectrum | OP12–OP14, OP18 | κ_c scaling; a natural 3-mode rule or a stated no-go |
| **L5** | Cosmology | OP19, S3–S6 | halo slope; n_s/r; vacuum-energy mechanism or no-go |

Parallel tracks: OP13 (Higgs) and OP19 (halo) do not depend on L2 and can start after L1.

---

## 2. Layer 0 — substrate and harness

**Frozen conventions.** BCC links `h = (±1,±1,±1)/2`, `ℓ = a√3/2`, `c = ℏ = 1`,
tick `τ = 0.989 t_P` (0.9855 with the chirality chain). Coefficients are quoted in `(kℓ)²`.
Every result records: code version, seed, grid, boundary condition, units.

**Tests.** V1 unitarity/reversal/light cone; V2 scalar dispersion; V3 independent dense BZ
scan; V4 energy drift over 10⁵ ticks; V5 regenerate the paper's tables.

**Exit gate.** All pass; the result schema is fixed.

**Status (2026-11-09):** V1, V2 pass. V3 partially run and already returned a finding
(§10). V4/V5 not yet automated.

---

## 3. Layer 1 — free spectrum (OP3, OP15, OP16)

### L1.1 Doubler census — OP3

**Setup.** The explicit 4×4 symbols of §6.2; scan the cube `[-π,π]³` densely (≥129³) and
include every high-symmetry point. Refine candidates with a local minimiser. Report the
minimum over the *interior* and over the *closure*, separately.

**Pass.** For `0<φ<π/2`, no zero except Γ **in the closure**, or a documented statement that
the boundary zeros are excluded by the physical state space and why.

**Current result.** Interior minima match Table `dirac4` (0.084 vs 0.082 at φ=1.4;
0.201 vs 0.217 at φ=0.5; coarse-grid error). But there are **12 exact massless zero modes**
at the face centres `(±π,±π,0)` and permutations, independent of φ, with the Wilson layer
present (U = I to 7e−16). They gap only when `m>0` (ω=0.050 at m=0.1). Random starts never
hit them because they are measure-zero. See §10.

**Decision needed.** Either (a) show these boundary points are not in the physical spectrum
(hard: they are allowed k on an even finite lattice), or (b) repair the Wilson layer so that
it vanishes at Γ but not at the face centres, and re-run the census. A candidate repair is
given in §10.

### L1.2 Chirality chain and doubler gap — OP3

Reproduce Table `dw`: residual mass vs Ns, `|γ5|`, localisation length, smallest gap vs b.
Pass: within 5%, and `b ≤ 0.25` boundary confirmed independently.
Then test the *end-mode* dispersion against the physical-mode dispersion: the chiral mode's
speed is 0.9855 of the hop rate; a difference would be a species-dependent `c`.

### L1.3 ν from the rule — OP3

The paper leaves open whether `ν = cτ/a = 0.989` is fixed by the rule or by φ.
**Test:** scan φ and the layer weights; determine whether any local normalisation forces
`ν = 0.98911`. Pass: a derivation or a proof that φ is a genuine free parameter.
This matters because `ν` sets the tick and therefore every quoted rate.

### L1.4 Dispersion and diffusion vs data — OP15

Produce, from the rule, a sky-direction table of `1−v/c` at 1 GeV, 1 TeV, 31 GeV, 100 TeV,
3e20 eV, both subluminal and superluminal signs. Compare with Fermi 090510
(`E_QG,1 > 1.2 E_P`), LHAASO 221009A (`>1.0e20 GeV`), and the quadratic bound
`E_QG,2 > 1.3e11 GeV` (Vasileiou). Also compute a diffusion signature (arrival-time blur)
for a random (Poisson) control, which the model excludes (Sec. 7.3). Pass: no bound violated;
the anisotropic term is stated with its search template, not just its magnitude.

### L1.5 Vector and tensor fields — OP16

Repeat L1.4 with a photon-like vector field and the actual 4-component rule. **Pass:** `n=2`,
no linear term in 13 directions. **Falsifier:** any `n=1` component; that is already excluded.
This closes the largest tree-level Lorentz hole and is a prerequisite for L3.

---

## 4. Layer 2 — read-out and statistics (S1, S7, OP2, S2)

### L2.1 Born weights from energy share — S1/S7

The paper already reports CHSH 2.828, I₃≈0, no signalling, with cos² not coded.
**What is missing is a harness that makes the claim auditable:** the read must use only the
conserved link energy, and the entangled pair must be produced by a client-side split, not
inserted. Pass: `S=2.828±0.005`, `|κ|<1e−3`, marginal shift `<2σ`. Controls: |a| and |a|⁴
must fail (S≈1.66, 3.77). **Falsifier:** energy share does not reproduce the square.

### L2.2 Three-slit κ — S7

Same rule, three-slit geometry, two intensities. Pass `|κ|<1e−3` at both.
This is the sharpest tabletop-adjacent test in the paper.

### L2.3 Order independence of spacelike reads — S2, OP3

Enumerate server read orders in the delayed-choice geometry. Pass: max |ΔP| < 3σ.
Falsifier: any client-visible order dependence.

### L2.4 Exchange phase and exclusion — OP2

Two identical excitations on the BCC patch, exchanged along two paths; measure the
two-particle phase. Pass: −1 for the fermionic sector, +1 for the bosonic, with the
spin-statistics link arising from the rule rather than assigned. This is a hard, honest
test: a toy that only re-labels antisymmetry will fail the "not imported" criterion.

### L2.5 Shared records — OP3

Many-particle joint states held as single-writer records: pass if a 3-particle GHZ-style
record reproduces the quantum marginals and no-signalling, and if the single-writer
constraint does not serialise independent pairs.

---

## 5. Layer 3 — gravity (OP4–OP11, OP17)

Ordered by increasing difficulty; each item names what would count as failure.

| Test | OP | Setup | Pass | Falsifier |
|---|---|---|---|---|
| G1 load-first γ | 7 | 3D BCC, load diffusion, wave probe, 13 directions | `γ−1 → 0` as h→0, isotropy ≤0.5% | residual floor |
| G2 compounding β | 8 | neighbour clock relay, Mercury orbit | `β=1.000±0.002`, 42.98″/cy | β→0.5 |
| G3 EP for composites | 4,7,8 | strongly bound pair, h, h/2, h/4 | `η ∝ h² → <1e−6` | η flat at ~1% |
| G4 tensor source | 8 | rotating + pressure source; GP-B | coupling 2 from rule, not inserted | scalar-only result |
| G5 Planck-mass node | 6 | single node at m_P, then spread | GR recovered when load spread; finite core | divergent / no crossover |
| G6 1-loop anisotropy | 17 | BCC rule + Wilson, self-energy | anisotropic part ≤ C(E/E_P)² | unsuppressed term |
| G7 core dynamics | 9–11 | collapsing shell on the load rule | stable finite core; inner horizon stated | mass inflation / no cap |

G3 is the cleanest: the paper already reports ~1% for strong binding and says the finer-grid
run is pending. G6 is the decisive one and the paper's own top risk.

---

## 6. Layer 4 — matter spectrum (OP12–OP14, OP18)

| Test | OP | Question | Realistic outcome |
|---|---|---|---|
| M1 Higgs critical point | 13 | Does homing lock to κ_c as L→∞? | Simulation-ready; the +0.006 bias must shrink |
| M2 λ(M_Pl) and m_H/M_Pl | 14 | Two-loop RGE rerun; is λ(M_Pl)≈0 stable? | Analysis, not lattice; paper already has it |
| M3 three generations | 12 | Search for a node mode rule with 3 uneven modes and Koide 2/3 | Exploratory; a no-go is a valid result |
| M4 dark-matter identity | 18 | Which excitation loads but does not couple to EM? | Conceptual; needs a candidate field, not a fit |

M1 is the only one that is a normal simulation. M3 should be time-boxed: plain overtones
give ratios near 2, and no working mode rule exists; an exhaustive small search can settle
whether the idea has a foothold.

---

## 7. Layer 5 — cosmology (OP19, S3–S6)

| Test | OP | Pass | Note |
|---|---|---|---|
| C1 halo outer slope | 19 | `r^−3 ± 10%` | current −2.3; expanding grid + infall |
| C2 soliton core | — | 3–6% vs Schive | already passes |
| C3 n_s, r | S6 | 0.9658, 0.0022 | QFT on background, not lattice |
| C4 vacuum energy | S3, S5 | any suppression mechanism | target; no simulation yet |
| C5 CP bias | S4 | baryon/photon 1e−10 + Sakharov | server-side; no model |

C1 is ready and cheap. C4/C5 are not simulation problems yet; they need a mechanism first.
S5 (per-node fee ~1e−123) and S6 (log-load counting) are derivation targets, not fits.

---

## 8. Traceability: open problem → layer → first action

| OP | Layer | First action | Cost |
|---|---|---|---|
| 1 | all | freezes with L0–L2; no standalone test | — |
| 2 | L2 | exchange-phase toy | 1–2 wk |
| 3 | L1 | repair face-centre zeros, then rerun census | 3–5 d |
| 4 | L3 | EP composite (G3) | 3–5 d |
| 5 | L3 | workload→metric map; start with G1 | 2 wk |
| 6 | L3 | single-node m_P toy | 1 wk |
| 7 | L3 | G1 precision + priority rule derivation | 2 wk |
| 8 | L3 | G2 + tensor source (G4) | 2 wk |
| 9–11 | L3 | G5–G7 | 3–6 wk |
| 12 | L4 | time-boxed 3-mode search | 2 wk |
| 13 | L4 | L-scan Binder + homing | 1–2 wk |
| 14 | L4 | RGE rerun (analysis) | 3 d |
| 15 | L1 | sky table + diffusion control | 1 wk |
| 16 | L1 | vector dispersion | 1 wk |
| 17 | L3 | 1-loop anisotropy | 2–4 wk |
| 18 | L4 | candidate-field definition | open |
| 19 | L5 | expanding-grid halo | 1–2 wk |
| S1 | L2 | auditable energy-share read | 1–2 wk |
| S2 | L2 | read-order permutation | 3 d |
| S3 | L5 | mechanism first | open |
| S4 | L5 | mechanism first | open |
| S5 | L5 | derivation, no fit | open |
| S6 | L5 | derive log-load counting | open |
| S7 | L2 | already pass; make reproducible | 3 d |

---

## 9. Interface contract (so layers do not rewrite each other)

```
ledger/
  bcc.py       links, dispersion, directions                [frozen]
  qwalk.py     1D/2D Dirac walk, exact checks               [frozen]
  dirac4.py    4-component symbols, gap, chirality           [L1, may change if repaired]
  readout.py   energy-share read, CHSH, kappa                [L2]
  workload.py  load, clock relay, link priority              [L3]
  matter.py    phi^4 / Higgs lattice                         [L4]
  cosmo.py     Schrodinger-Poisson halo                      [L5]
```

Rules:
1. A layer adds modules; it does not edit lower-layer numbers.
2. Every module exposes a pure function `observables(config) -> dict`.
3. All stochastic runs take an explicit seed and return a spread over ≥5 seeds.
4. A result is not reported unless `runs/<date>_<id>/result.json` exists and the table can be
   regenerated from it.

---

## 10. First results (2026-11-09)

**V2 — scalar dispersion.** Confirmed the Table in §6.15: coefficients 1/24, 1/12, 7/72 in
`(kℓ)²`, axis–body gap 1/18, to 1.8e−9.

**V1 — 1D checkerboard.** Unitarity 1.1e−17, dispersion exact, zero probability outside the
cone over 300 ticks, reversal 2.8e−16. Harness trap found: open boundaries plus on-site mass
mixing break unitarity at the edges (norm loss 0.09); use periodic for unitarity, open for the
cone.

**V3 — OP3 doubler census (partial).** The interior gap table is reproduced within coarse-grid
error:

| φ | paper | this scan (interior) |
|---|---|---|
| 0.5 | 0.217 | 0.201 |
| 0.8 | 0.262 | 0.247 |
| 1.0 | 0.232 | 0.236 |
| 1.2 | 0.167 | 0.168 |
| 1.4 | 0.082 | 0.084 |
| 1.5 | 0.035 | 0.035 |

But the closure has **12 exact zero modes** at the face centres `(±π,±π,0)` and permutations,
with the Wilson layer present and `m=0`; `U = I` to 7e−16. They are independent of φ and vanish
for `m>0`. The paper's random search cannot hit them (measure-zero set), so the statement
"no zero-frequency point other than the physical one" needs the qualifier "in the interior"
or a repair.

**Why it happens.** At `(π,π,0)`, `u = cos kx cos ky cos kz = +1` and `n = 0`, so the Wilson
symbol reduces to `e^{−iφτx} e^{+iφτx} = 1`, exactly as at Γ. The layer does not distinguish
Γ from the face centres. That is the defect.

**Candidate repair (tested, mixed).** Replace `u` in `X` by `u + g(k)` with `g(Γ)=0` and
`g` order one at the face centres, for example `g = (1/3)Σ(1−cos k_i)`; keep the second factor
`e^{+iφτx}` so the cancellation at Γ survives, and use a matrix exponential if `X²≠1`.
Result at φ=1.4: the 12 zeros lift (ω=0.637), Γ stays massless, and the smallest interior gap
rises from 0.082 to 0.221. But `g` is O(k²) near Γ, so it also changes the low-energy
dispersion; the light speed and the `(E/E_P)²` coefficient must be re-measured before this
patch can be accepted. This is a concrete, falsifiable next step, not a rewrite.

**Caveat.** If these boundary modes are declared unphysical, the model owes a reason that
survives a finite lattice with even L, where `k=(π,π,0)` is an allowed momentum. That is a
model decision, not a numerical one.

---

## 11. Recommended first sprint (2 weeks)

1. **L1.1 repair + full census** (OP3) — 3–5 d. Highest information; already productive.
2. **G3 EP composite** (OP4/7/8) — 3–5 d. Explicit pending run; clean go/no-go.
3. **L1.5 vector dispersion** (OP16) — 5 d. Closes the tree-level Lorentz hole.
4. **L1.3 ν derivation** (OP3) — 2 d. Cheap; fixes a free parameter.

Do not start L2/L3 until L1's exit gate is met. The face-centre issue shows why: a repair at
L1 changes the symbol that every later layer uses.
