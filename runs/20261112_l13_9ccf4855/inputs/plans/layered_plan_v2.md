# Layered test program for the §9 open problems — v2

**Draft for Edmond's review. Nothing in the paper, repo, Sheet or production has been changed, and no simulation was run to make this version.**
Revision of Edmond's v1 proposal (2026-11-09; copy kept unchanged at `ref/layered_plan_v1_original.md`). Every edit is listed with its reason in `CHANGES.md`. Nothing from v1 has been deleted: items moved out of the main line are in Appendix A, and targets that were not measured numbers are kept as labelled *reference values* (§0.3).

Paper checked against: `space-ledger-v2.md` / `.pdf` on `main` at commit `9d39338` (2026-11-09 08:50 EST), §8 and §9 (PDF pp. 68–71). Open-problem numbers **OP1–OP19** and server-side items **S1–S7** are the paper's own numbers and are not renumbered here.

Target: open problems 1–19 and server-side items S1–S7, plus the three objectives in §8 (8.1 read-out, 8.2 radiative Lorentz invariance, 8.3 chiral gauge theory).

The approach is bottom-up. Each layer is a software milestone with a frozen interface, an entry gate and an exit gate. A later layer may not change a lower layer's conventions. If it must, the lower layer is re-run. This is the only way to keep toy results comparable across the paper's tables.

---

## 0. Standing rules (apply to every layer and every run)

### 0.1 Physics rules

1. **Congestion is always ON**, including in vacuum. Congestion OFF is allowed only as a labelled diagnostic and never counts toward a gate. Current factors are s = (1+load)^(−1/2), F = s² and the lock-queue ρ = 1 − f.
2. **Whole ticks only.** No fractional ticks and no sub-tick interpolation in the rule. Rounding, if needed, is to whole ticks and is declared in advance.
3. **No self-load.** A packet never loads the nodes it is being propagated through by its own presence unless a written rule says so and Edmond has approved that rule.
4. **No fitting.** No model parameter, exponent, coefficient or source profile is tuned to hit a target. Rules and coefficients are written down and hashed before any comparison. Fitting the *size of a measured effect* (e.g. a leak coefficient from a run) is allowed and must be labelled as such.
5. **Unbiased comparison.** Model and reference are run under the same conditions (same geometry, grid, source, boundary, read-out), with the same uncertainty treatment on both sides. Fluctuations come only from a specified mechanism with an explicit seed.
6. **Measured targets only** (§0.3).
7. **Preserve failed runs.** Originals and failed or partial runs are kept unchanged with their logs and hashes. A failure is a result.

### 0.2 Run governance

- Every run needs Edmond's own approval, with stated caps (memory, CPU seconds, wall time, output size, one attempt, stop on any failed check). Designs can be written without a run.
- Every result records code version, seed, grid, boundary condition, units, caps and resources used, and lives in `runs/<date>_<id>/result.json` (v1 §9 rule 4).

### 0.3 Targets

A **target** is a measured number with its published uncertainty and citation. A model value is scored against it with the same uncertainty treatment on both sides. If only a limit exists, the item is scored against the limit.

Not targets: values produced by theory or simulation (GR predictions, simulation profiles, RGE extrapolations, the paper's own toy outputs). These may still be listed as **reference values**, labelled as such, and never used as a pass/fail gate. Items for which no measured number exists yet are **mechanism-first**: the gate is a written mechanism with a stated physical reason, not a number.

| Quantity | Measured target | Source |
|---|---|---|
| Linear photon dispersion | E_QG,1 > 7.6 E_Pl (95%, subluminal) | Fermi-LAT GRB 090510; Vasileiou et al., PRD 87, 122001 (2013). Most conservative Abdo et al., Nature 462, 331 (2009): > 1.2 E_Pl |
| Linear photon dispersion | E_QG,1 > 10 E_Pl, i.e. > 1.0×10²⁰ GeV subluminal (> 1.1×10²⁰ GeV superluminal), 95% | LHAASO GRB 221009A; Cao et al., PRL 133, 071501 (2024) |
| Quadratic photon dispersion | E_QG,2 > 6.9×10¹¹ GeV subluminal (7.0×10¹¹ superluminal), 95% | LHAASO, same paper (supersedes Vasileiou's 1.3×10¹¹ GeV) |
| PPN γ | γ − 1 = (2.1 ± 2.3)×10⁻⁵ | Cassini; Bertotti, Iess & Tortora, Nature 425, 374 (2003) |
| PPN β | \|β − 1\| < 8×10⁻⁵ (perihelion shift) | Will, Living Rev. Relativ. 17, 4 (2014), Table 4 |
| Equivalence principle | η(Ti,Pt) = [−1.5 ± 2.3(stat) ± 1.5(syst)]×10⁻¹⁵ | MICROSCOPE; Touboul et al., PRL 129, 121102 (2022) |
| GP-B | geodetic −6601.8 ± 18.3 mas/yr; frame-dragging −37.2 ± 7.2 mas/yr | Everitt et al., PRL 106, 221101 (2011) |
| Lepton masses | mₑ = 0.51099895000(15) MeV, m_μ = 105.6583755(23) MeV, m_τ = 1776.93(9) MeV; m_μ/mₑ = 206.768283(5), m_τ/mₑ = 3477.37(18) | PDG 2024 (Navas et al., PRD 110, 030001) |
| Koide ratio of measured masses | Q = 0.6666645 ± 0.0000051 (from the PDG masses above; 2/3 is the empirical relation, not a target for the model to "derive" beyond what the masses show) | computed here from PDG 2024 |
| Higgs and top masses | m_H = 125.20 ± 0.11 GeV; m_t = 172.57 ± 0.29 GeV | PDG 2024 |
| Scalar tilt | n_s = 0.9649 ± 0.0042 (68%) | Planck 2018 X, A&A 641, A10 (2020) |
| Tensor-to-scalar ratio | r₀.₀₅ < 0.036 (95%), upper limit only | BICEP/Keck + Planck + WMAP (BK18), PRL 127, 151301 (2021) |
| Vacuum energy (S5 size) | ρ_Λ/ρ_Planck ≈ 1.1×10⁻¹²³ (from Planck 2018 H₀ = 67.4 ± 0.5, Ω_Λ = 0.685 ± 0.007) | Planck 2018 VI, A&A 641, A6 (2020); derived arithmetic |

---

## 1. Layer map

| Layer | Content | Open problems | Exit gate |
|---|---|---|---|
| **L0** | Substrate, conventions, exactness harness; **choice of canonical rule** | OP1 (foundation) | V1–V5 pass; units frozen; one canonical node rule named |
| **L1** | Free spectrum: doublers, chirality, dispersion, ν, **linear-term test** | OP3 (spectrum), OP15, OP16 | zero modes and extra nodes classified with a repair-or-reason decision; gap table reproduced; linear term measured and compared with GRB limits; ν from the rule or declared free |
| **L2** | Read-out and statistics | S1, S7, OP2, S2, OP3 (shared records) | Born weights without insertion; κ bound; exchange phase −1; order independence |
| **L3** | Gravity | OP4–OP11, OP17 | γ, β, η and GP-B from the rule compared with Cassini, perihelion, MICROSCOPE, GP-B; **current γ status recorded honestly (≈3% short of GR in bending)**; 1-loop anisotropy suppressed |
| **L4** | Matter spectrum | OP12–OP14 (OP18 moved to Appendix A) | κ_c scaling; OP12 needs a new mechanism with a stated reason (the existing-rule route is a recorded no-go) |
| **L5** | Cosmology | OP19, S3, S5, S6 (S4 moved to Appendix A) | halo slope against a measured profile; n_s against Planck and r against the BK18 upper limit; vacuum-energy mechanism or no-go |

Parallel tracks: OP13 (Higgs) and OP19 (halo) do not depend on L2 and can start after L1.

---

## 2. Layer 0 — substrate and harness

**Frozen conventions.** BCC links `h = (±1,±1,±1)/2`, `ℓ = a√3/2`, `c = ℏ = 1`, tick `τ = 0.989 t_P` (0.9855 with the chirality chain). Coefficients are quoted in `(kℓ)²`. Every result records code version, seed, grid, boundary condition and units. The standing rules in §0 are part of the frozen conventions.

**Canonical rule (new decision).** Two different node rules are in use. The paper's §6.2 four-component rule with a Wilson layer is the one in Table `dirac4`. The OP4 local rule (`prod/op4_local_gpu.py`, a product of three 1D walks with ν² + m² = 1 per tick) is the one used for the recent gravity, photon and spectrum work. They have different doubler content (L1.1) and possibly different linear terms (L1.5). L0 must name which one is canonical, or carry both as labelled branches through L1.

**Tests.** V1 unitarity, reversal and light cone; V2 scalar dispersion; V3 independent dense BZ scan; V4 energy drift over 10⁵ ticks; V5 regenerate the paper's tables.

**Exit gate.** All pass; the result schema is fixed; the canonical rule is named.

**Status (2026-11-09):** V1, V2 pass. V3 partially run and already returned a finding (§10). V4/V5 not yet automated. Canonical rule: not yet chosen.

---

## 3. Layer 1 — free spectrum (OP3, OP15, OP16)

### L1.1 Doubler census — OP3 (both rules)

**Setup.** For each rule in use, take the explicit symbols: the 4×4 symbols of §6.2, and the OP4 generator Q(k) = [[ν n·σ, −m], [−m, −ν n·σ]]. Scan the cube `[-π,π]³` densely (≥129³) and include every high-symmetry point. Refine candidates with a local minimiser. Report the minimum over the *interior* and over the *closure*, separately, and report each zero's location, chirality and tilt.

**Pass.** For each rule, either no zero except Γ in the closure, or a documented statement that the extra zeros are excluded from the physical state space, and why. **The same decision rule applies to both findings below:** repair it, or give a reason it is unphysical that survives a finite lattice with even L.

**Current result, §6.2 Wilson symbol.** Interior minima match Table `dirac4` (0.084 vs 0.082 at φ=1.4; 0.201 vs 0.217 at φ=0.5; coarse-grid error). But there are **12 exact massless zero modes** at the face centres `(±π,±π,0)` and permutations, independent of φ, with the Wilson layer present (U = I to 7e−16). They gap only when `m>0` (ω=0.050 at m=0.1). Random starts never hit them because they are measure-zero. See §10.

**Current result, OP4 rule** (`/workspace/bcc_staggered_design_20261109/`, symbolic checks). OP4 has **4 isolated Weyl nodes per chirality block**: Γ, H = (π,0,0), P = (π/2,π/2,π/2) and P′ = −P, i.e. **3 extra nodes (doublers)**. Chiralities are (+,−,+,−) for (Γ,H,P,P′) and sum to zero (Nielsen–Ninomiya). They are isolated points, not lines. Uniform congestion load only rescales velocity and leaves the node count unchanged.

**Naive BCC operator and staggering.** The naive nearest-neighbour BCC Dirac operator has **zero lines** at k_i = k_j = π/2 (a count that grows with L). **Kogut–Susskind spin diagonalisation is frustrated on BCC**: the four body-diagonal hops cannot all anticommute for any U(1) phases, so exact KS staggering does not exist on this lattice, and staggering does **not** remove the zero lines. The best Z₂-flux pattern gives about 2 Dirac tastes but with over-tilted (type-II) cones.

**Decision needed (one decision, applied to both rules).** Either (a) show these points are not in the physical spectrum (hard: they are allowed k on an even finite lattice), or (b) repair the rule so that the extra zeros or nodes are lifted while Γ stays massless, and re-run the census. Candidate repairs: the face-centre `g(k)` patch (§10); a Wilson-type term on OP4's three isolated doublers; domain wall or overlap (exact chirality, highest cost). A design for one CPU-only free-spectrum check exists; it is **not approved or run**.

**Link to OP12.** Using the four OP4 nodes as the three generations is a recorded no-go under existing rules (L4, M3).

### L1.2 Chirality chain and doubler gap — OP3

Reproduce Table `dw`: residual mass vs Ns, `|γ5|`, localisation length, smallest gap vs b. Pass: within 5%, and `b ≤ 0.25` boundary confirmed independently. Then test the *end-mode* dispersion against the physical-mode dispersion: the chiral mode's speed is 0.9855 of the hop rate; a difference would be a species-dependent `c`.

### L1.3 ν from the rule — OP3

The paper leaves open whether `ν = cτ/a = 0.989` is fixed by the rule or by φ. **Test:** scan φ and the layer weights; determine whether any local normalisation forces `ν = 0.98911`. Pass: a derivation or a proof that φ is a genuine free parameter. This matters because `ν` sets the tick and therefore every quoted rate. (A scan of φ to *understand* the rule is allowed; choosing φ to hit a number is not.)

### L1.4 Dispersion and diffusion vs data — OP15

Produce, from the rule, a sky-direction table of `1−v/c` at 1 GeV, 1 TeV, 31 GeV, 100 TeV, 3e20 eV, both subluminal and superluminal signs. Compare with the measured limits in §0.3: Fermi GRB 090510 (E_QG,1 > 7.6 E_Pl, Vasileiou 2013; conservative 1.2 E_Pl, Abdo 2009), LHAASO GRB 221009A (E_QG,1 > 1.0×10²⁰ GeV subluminal; E_QG,2 > 6.9×10¹¹ GeV). Also compute a diffusion signature (arrival-time blur) for a random (Poisson) control, which the model excludes (Sec. 7.3). Pass: no bound violated; the anisotropic term is stated with its search template, not just its magnitude.

### L1.5 Vector and tensor fields; linear-term test — OP16

Repeat L1.4 with a photon-like vector field and the actual canonical rule (4-component §6.2 and/or OP4), along at least 13 directions including [100], [110], [111] and [11−1].

**Why this is a test, not an assumed pass.** The paper's "no linear term, leading effect quadratic" statement (Sec. 6.4 Test 1, Sec. 7.8) comes from the scalar link-only toy. For the OP4 rule, a leading-order analysis predicts a **possible linear, direction-odd massless light-speed leak along [111]**, v_g ≈ 1 + (2/(3√3))κ ≈ 1 + 0.385κ (κ = kℓ), which flips sign along [11−1]; along [100] and [110] the leading term is quadratic (1 − κ²/2, 1 − 5κ²/8) (`/workspace/lorentz_tick_budget_design_20261109/DESIGN.md`). Whether it survives the exact whole-tick macrostep is exactly what the run measures.

**Measure.** Massless v_g(κ, direction) from the exact whole-tick evolution, congestion ON (uniform vacuum load) with OFF as a labelled diagnostic; fit only the leak coefficients ξ₁ (linear) and ξ₂ (quadratic) per direction, with the same uncertainty treatment as the data.

**Pass.** The implied E_QG,1 in every direction exceeds both the Fermi (7.6 E_Pl) and the LHAASO (10 E_Pl) limits, and E_QG,2 exceeds the LHAASO quadratic limit. A direction-odd term is reported with its sky template, since the bound weakens for bursts with small k_x k_y k_z.

**Falsifier.** A linear term that applies to photons and violates the limits. For scale: if the [111] leak of 0.385κ applied to photons at full size, LHAASO would require a ≲ ℓ_P/(0.385×10) ≈ 0.26 ℓ_P. That would conflict with the paper's Planck-scale spacing and with the Sec. 7.8 wording.

**Status.** Tick-budget / light-speed run (`lorentz_tick_budget_design_20261109`) is **designed and held pending Edmond's approval** (25 clock fixtures, 10 light-speed runs, 2 controls; proposed caps 1 thread, 1 GiB, 180 CPU s, 240 s wall, 16 MiB, one attempt). Until it runs, L1.5 is **open**, and the Sec. 6.4 / 7.8 "no linear term" wording should be read as scalar-toy only.

This closes the largest tree-level Lorentz hole and is a prerequisite for L3.

**L1 exit gate.** L1.1 decision made and census re-run for the chosen rule; L1.2 reproduced; L1.3 settled; L1.4 and L1.5 measured against the §0.3 limits.

---

## 4. Layer 2 — read-out and statistics (S1, S7, OP2, S2)

Targets in this layer are reproduction of quantum-mechanical predictions for the same state and geometry (an internal consistency gate), anchored to measurement where a measured bound exists: three-slit Sorkin parameter |κ| ≲ 10⁻² (Sinha et al., Science 329, 418 (2010)); loophole-free Bell tests agree with QM for their own states (e.g. Hensen et al., Nature 526, 682 (2015); Storz et al., Nature 617, 265 (2023)). The Tsirelson value 2√2 is the QM prediction for an ideal state, i.e. a reference value, not a measured target.

### L2.1 Born weights from energy share — S1/S7

The paper already reports CHSH 2.828, I₃≈0, no signalling, with cos² not coded. **What is missing is a harness that makes the claim auditable:** the read must use only the conserved link energy, and the entangled pair must be produced by a client-side split, not inserted. Pass: `S=2.828±0.005` (QM reference for the ideal state), `|κ|<1e−3`, marginal shift `<2σ`. Controls: |a| and |a|⁴ must fail (S≈1.66, 3.77). **Falsifier:** energy share does not reproduce the square.

### L2.2 Three-slit κ — S7

Same rule, three-slit geometry, two intensities. Pass `|κ|<1e−3` at both (internal precision gate; the measured bound is |κ| ≲ 10⁻²). This is the sharpest tabletop-adjacent test in the paper.

### L2.3 Order independence of spacelike reads — S2, OP3

Enumerate server read orders in the delayed-choice geometry. Pass: max |ΔP| < 3σ. Falsifier: any client-visible order dependence.

### L2.4 Exchange phase and exclusion — OP2

Two identical excitations on the BCC patch, exchanged along two paths; measure the two-particle phase. Pass: −1 for the fermionic sector, +1 for the bosonic, with the spin-statistics link arising from the rule rather than assigned. This is a hard, honest test: a toy that only re-labels antisymmetry will fail the "not imported" criterion.

### L2.5 Shared records — OP3

Many-particle joint states held as single-writer records: pass if a 3-particle GHZ-style record reproduces the quantum marginals and no-signalling, and if the single-writer constraint does not serialise independent pairs.

---

## 5. Layer 3 — gravity (OP4–OP11, OP17)

Ordered by increasing difficulty; each item names what would count as failure. All runs congestion ON; no self-load unless an approved rule supplies it.

| Test | OP | Setup | Measured target | Pass | Falsifier | Status (2026-11-09) |
|---|---|---|---|---|---|---|
| G1 load-first γ | 7 | 3D BCC, load diffusion, wave probe, 13 directions; bending and Shapiro | Cassini γ−1 = (2.1±2.3)×10⁻⁵ | γ from the rule within Cassini's error, isotropy ≤0.5%, no residual floor under refinement | residual floor | **Open, not passing.** Current OP4 congestion-continuum comparison is ≈3% short of GR in bending (ledger/GR steering 0.970–0.971 at h=0.5; gap persists under h=1→0.5 refinement). Edmond chose to carry this as the current result. |
| G2 compounding β | 8 | neighbour clock relay, Mercury orbit | \|β−1\| < 8×10⁻⁵ (Will 2014) | β from the rule within that bound | β→0.5 | Toy-level β=1 reported in the paper (OP7/8); conditional on G1 |
| G3 EP for composites | 4,7,8 | strongly bound pair, h, h/2, h/4 | MICROSCOPE η ~ 10⁻¹⁵ | η → 0 with refinement as h²; extrapolated η compared with MICROSCOPE | η flat at ~1% | paper reports ~1% for strong binding; finer-grid run pending |
| G4 tensor source | 8 | rotating + pressure source | GP-B geodetic and frame-dragging (Everitt 2011) | coupling 2 from rule, not inserted; GP-B within errors | scalar-only result | not started |
| G5 Planck-mass node | 6 | single node at m_P, then spread | none (mechanism-first) | GR recovered when load spread; finite core | divergent / no crossover | not started |
| G6 1-loop anisotropy | 17 | canonical rule + Wilson, self-energy | Lorentz-violation bounds (Kostelecký & Russell, *Data Tables for Lorentz and CPT Violation*, arXiv:0801.0287, current edition) | anisotropic part ≤ C(E/E_P)² and within the tabulated bounds | unsuppressed term | not started |
| G7 core dynamics | 9–11 | collapsing shell on the load rule | none (mechanism-first) | stable finite core; inner horizon stated | mass inflation / no cap | horizon design: existing rules give **no horizon** (s, F, ρ never reach 0), whereas GR's isotropic lapse reaches 0 at r = M/2; design only |

**G1, stated honestly.** v1's gate (`γ−1 → 0` as h→0) cannot pass as written with the current rule: the gap to GR has a known size (≈3% in bending in the strong-field toy) and did not shrink under grid refinement. G1 therefore stays open with that size recorded; it is *not* claimed as GR agreement. The paper's OP7 text ("γ = 0.999 ± 0.001") came from an earlier load-first link rule, a different mechanism, and itself notes toy precision about 40× short of the Cassini bound. Both results are kept; neither is deleted. G2 and G4 can proceed but are labelled "conditional on G1 open". Reopening G1 needs a new mechanism with a stated reason, not tuning.

G3 is the cleanest: the paper already reports ~1% for strong binding and says the finer-grid run is pending. G6 is the decisive one and the paper's own top risk.

Reference values (not targets): GR's 42.98″/cy for Mercury and 4GM/(bc²) for bending are GR predictions; the gates above use the measured PPN bounds instead.

---

## 6. Layer 4 — matter spectrum (OP12–OP14)

| Test | OP | Question | Measured target | Status / realistic outcome |
|---|---|---|---|---|
| M1 Higgs critical point | 13 | Does homing lock to κ_c as L→∞? | none (internal lattice criterion) | Simulation-ready; the +0.006 bias must shrink |
| M2 λ(M_Pl) and m_H/M_Pl | 14 | Two-loop RGE rerun; is λ(M_Pl)≈0 stable? | m_H, m_t (PDG 2024); m_H/M_Pl ≈ 1.0×10⁻¹⁷ | Analysis, not lattice; λ(M_Pl)≈0 is an SM extrapolation (reference value), so the gate is the measured inputs |
| M3 three generations | 12 | A rule with a stated physical reason that gives three light modes with the measured ratios | m_μ/mₑ = 206.768, m_τ/mₑ = 3477.37 (PDG 2024); Koide Q of measured masses | **No-go for existing rules recorded (2026-11-09).** Needs a new mechanism. |

**M3, current result (2026-11-09; design `/workspace/bcc_generation_split_design_20261109/`, run `/workspace/bcc_generation_split_run_20261109/`).**
- Under the existing OP4 rule the four nodes Γ, H, P, P′ all have the **same mass** (exactly 1:1:1:1); uniform congestion scales all four by the same factor, so the ratios are load-independent.
- The predeclared corner-mass terms (on-site; one-tick and two-tick BCC Wilson-type terms; the OP4 tick scalar) give node-mass ratios of only **1 or 2** (232/232 checks passed; none meets the count, ratio or handedness criteria).
- A **wrong-handed node is always among the light ones**: relative to Γ, H and P′ have reversed handedness, so any three survivors include a V+A "generation", while all three measured generations are V−A.
- **20 preregistered nested-loop counting rules** (balls, shells, 8ⁿ walks, neighbour checks, nested trees; electron at level 0 or 1; with or without whole-tick rounding; PREREG hash frozen before the run) give m_μ/mₑ between **1 and 9** and m_τ/mₑ up to 73, against 206.77 and 3477.37: 0 pass, 0 partial, 20 fail. Reaching 207 with 8ⁿ would need a non-integer depth of about 2.56.
- Side result: per-generation masses can stay unitary if they enter through the tick budget (ν² + m² = 1), provided the electron's lattice mass is below about 3×10⁻⁴; heavier generations would then have a very slightly lower top speed.
- The paper's Sec. 6.8 already records an earlier failed doubler-as-generation version (four species, Koide 0.33–0.50).

**M3 entry gate (new).** A written mechanism with its physical reason ("each level costs X because of Y"), hashed before comparison, with no free coefficients chosen to hit the targets. **Koide** is used only as a test of the measured masses (Q = 0.666664 ± 0.000005 from PDG 2024), not as a separate target to be fitted. M3 is time-boxed; a further no-go is a valid result.

M1 is the only one that is a normal simulation.

(v1's M4, dark-matter identity, OP18, is moved to Appendix A.)

---

## 7. Layer 5 — cosmology (OP19, S3, S5, S6)

| Test | OP | Measured target | Pass | Note / status |
|---|---|---|---|---|
| C1 halo outer slope | 19 | **to be chosen**: a measured stacked halo profile (e.g. weak-lensing). v1's r⁻³ is the NFW form from simulations, kept as a reference value | slope within the measured profile's errors | current −2.3; expanding grid + infall |
| C2 soliton core | — | none measured; v1's "3–6% vs Schive" compares with a simulation (Schive et al. 2014), kept as a reference value, not a gate | — | already matches the reference |
| C3 n_s, r | S6 | n_s = 0.9649 ± 0.0042 (Planck 2018); r < 0.036 (95%, BK18) | n_s within Planck's errors; r below the BK18 limit | Paper's toy values n_s = 0.9658, r = 0.0022 (b=1) are *model outputs*, not targets. Against the measured numbers they currently pass (n_s within 0.2σ; r below the limit), but log-load counting and b are chosen, not derived (S6), and it is QFT on a background, not a lattice |
| C4 vacuum energy | S3, S5 | none for S3 (**mechanism-first**); S5's size ρ_Λ/ρ_P ≈ 1.1×10⁻¹²³ is derived from measured Λ | a written suppression mechanism with a stated reason; S5 derived without a horizon input | no simulation yet |

C1 is ready and cheap. C4 is not a simulation problem yet; it needs a mechanism first. S5 (per-node fee ~1e−123) and S6 (log-load counting) are derivation targets, not fits.

(v1's C5, CP bias, S4, is moved to Appendix A and made mechanism-first with no numerical target.)

---

## 8. Traceability: open problem → layer → first action

| OP | Layer | First action | Cost | Status |
|---|---|---|---|---|
| 1 | all | freezes with L0–L2; L0 names the canonical rule | — | open |
| 2 | L2 | exchange-phase toy | 1–2 wk | open |
| 3 | L1 | one repair-or-reason decision for the 12 face-centre zeros (§6.2) **and** OP4's 3 extra nodes; then rerun census | 3–5 d | open; design only |
| 4 | L3 | EP composite (G3) | 3–5 d | open |
| 5 | L3 | workload→metric map; start with G1 | 2 wk | open |
| 6 | L3 | single-node m_P toy | 1 wk | open |
| 7 | L3 | G1: carry ≈3% bending gap as current result; any reopening needs a new stated mechanism | 2 wk | open, gate not passing |
| 8 | L3 | G2 + tensor source (G4), labelled conditional on G1 | 2 wk | open |
| 9–11 | L3 | G5–G7; horizon design (no horizon from existing rules) | 3–6 wk | design only |
| 12 | L4 | new mechanism with stated reason, preregistered; existing-rule no-go recorded | 2 wk | no-go for existing rules |
| 13 | L4 | L-scan Binder + homing | 1–2 wk | open |
| 14 | L4 | RGE rerun (analysis) against measured m_H, m_t | 3 d | open |
| 15 | L1 | sky table + diffusion control against Fermi/LHAASO | 1 wk | open |
| 16 | L1 | linear-term test along [111]/[11−1] (tick-budget run) | 1 wk | designed; held for approval |
| 17 | L3 | 1-loop anisotropy | 2–4 wk | open |
| 18 | App. A | candidate-field definition (side item, Edmond to decide) | open | — |
| 19 | L5 | expanding-grid halo; choose a measured profile | 1–2 wk | open |
| S1 | L2 | auditable energy-share read | 1–2 wk | open |
| S2 | L2 | read-order permutation | 3 d | open |
| S3 | L5 | mechanism first | open | open |
| S4 | App. A | mechanism first, no numerical target (side item, Edmond to decide) | open | — |
| S5 | L5 | derivation, no fit | open | open |
| S6 | L5 | derive log-load counting; score n_s and r against Planck and BK18 | open | open |
| S7 | L2 | already passes; make reproducible | 3 d | toy-tested |

---

## 9. Interface contract (so layers do not rewrite each other)

```
ledger/
  bcc.py       links, dispersion, directions                [frozen]
  qwalk.py     1D/2D Dirac walk, exact checks               [frozen]
  dirac4.py    4-component symbols, gap, chirality           [L1, may change if repaired]
  op4.py       OP4 product-walk symbol and nodes (read-only wrapper of prod/op4_local_gpu.py)  [L1]
  readout.py   energy-share read, CHSH, kappa                [L2]
  workload.py  load, clock relay, link priority              [L3]
  matter.py    phi^4 / Higgs lattice                         [L4]
  cosmo.py     Schrodinger-Poisson halo                      [L5]
```

Rules:
1. A layer adds modules; it does not edit lower-layer numbers.
2. Every module exposes a pure function `observables(config) -> dict`.
3. All stochastic runs take an explicit seed and return a spread over ≥5 seeds.
4. A result is not reported unless `runs/<date>_<id>/result.json` exists and the table can be regenerated from it.
5. `config` carries `congestion: "ON"` by default; `"OFF"` is accepted only with `diagnostic: true` and is excluded from gates.
6. Failed and partial runs are kept in `runs/` unchanged, with their logs and hashes.

---

## 10. First results (2026-11-09)

**V2 — scalar dispersion.** Confirmed the Table in §6.15: coefficients 1/24, 1/12, 7/72 in `(kℓ)²`, axis–body gap 1/18, to 1.8e−9. (Scalar link-only rule; does not settle the linear term for the Dirac/OP4 rule, see L1.5.)

**V1 — 1D checkerboard.** Unitarity 1.1e−17, dispersion exact, zero probability outside the cone over 300 ticks, reversal 2.8e−16. Harness trap found: open boundaries plus on-site mass mixing break unitarity at the edges (norm loss 0.09); use periodic for unitarity, open for the cone.

**V3 — OP3 doubler census (partial).** The interior gap table is reproduced within coarse-grid error:

| φ | paper | this scan (interior) |
|---|---|---|
| 0.5 | 0.217 | 0.201 |
| 0.8 | 0.262 | 0.247 |
| 1.0 | 0.232 | 0.236 |
| 1.2 | 0.167 | 0.168 |
| 1.4 | 0.082 | 0.084 |
| 1.5 | 0.035 | 0.035 |

But the closure has **12 exact zero modes** at the face centres `(±π,±π,0)` and permutations, with the Wilson layer present and `m=0`; `U = I` to 7e−16. They are independent of φ and vanish for `m>0`. The paper's random search cannot hit them (measure-zero set), so the statement "no zero-frequency point other than the physical one" needs the qualifier "in the interior" or a repair.

**Why it happens.** At `(π,π,0)`, `u = cos kx cos ky cos kz = +1` and `n = 0`, so the Wilson symbol reduces to `e^{−iφτx} e^{+iφτx} = 1`, exactly as at Γ. The layer does not distinguish Γ from the face centres. That is the defect.

**Candidate repair (tested, mixed).** Replace `u` in `X` by `u + g(k)` with `g(Γ)=0` and `g` order one at the face centres, for example `g = (1/3)Σ(1−cos k_i)`; keep the second factor `e^{+iφτx}` so the cancellation at Γ survives, and use a matrix exponential if `X²≠1`. Result at φ=1.4: the 12 zeros lift (ω=0.637), Γ stays massless, and the smallest interior gap rises from 0.082 to 0.221. But `g` is O(k²) near Γ, so it also changes the low-energy dispersion; the light speed and the `(E/E_P)²` coefficient must be re-measured before this patch can be accepted. This is a concrete, falsifiable next step, not a rewrite. (The chosen `g` must be written down with its reason before re-measuring; it is not tuned to the dispersion targets.)

**Caveat.** If these boundary modes are declared unphysical, the model owes a reason that survives a finite lattice with even L, where `k=(π,π,0)` is an allowed momentum. That is a model decision, not a numerical one.

**OP4 nodes (symbolic, 2026-11-09).** 4 Weyl nodes per block (Γ, H, P, P′), chiralities (+,−,+,−); KS staggering frustrated on BCC; naive BCC zero lines at k_i = k_j = π/2 persist under staggering. Source: `/workspace/bcc_staggered_design_20261109/`.

**Generation split (run once, 2026-11-09).** No-go for existing rules (see M3). Source: `/workspace/bcc_generation_split_run_20261109/`.

**Photon bending (2026-11-08).** Congestion-ON OP4 continuum comparison: ≈3% short of GR, unchanged under field refinement h=1→0.5 (138/138 checks). Source: `/workspace/gpu/op4_bcc_local/curved_reference_design/photon_field_refinement_20261108/`.

---

## 11. Recommended first sprint (2 weeks)

1. **L0 canonical-rule decision** — 0.5 d. Needed before L1.1 can be closed.
2. **L1.1 repair-or-reason decision + full census** (OP3, both rules) — 3–5 d. Highest information; already productive.
3. **L1.5 linear-term test** (OP16) — the tick-budget run is designed; needs Edmond's approval of caps. Closes or confirms the tree-level Lorentz hole.
4. **G3 EP composite** (OP4/7/8) — 3–5 d. Explicit pending run; clean go/no-go. Labelled conditional on G1 open.
5. **L1.3 ν derivation** (OP3) — 2 d. Cheap; fixes a free parameter.

Do not start L2/L3 until L1's exit gate is met. The face-centre issue and the OP4 nodes show why: a repair at L1 changes the symbol that every later layer uses.

---

## Appendix A — Possible side items (Edmond to decide)

Edmond has said the open-problems list should be kept strictly to what upholds the theory. The items below are **not deleted**. They are taken out of the main layer line until Edmond decides whether they stay.

| Item | Paper ref | v1 location | Why it may be a side item | If kept |
|---|---|---|---|---|
| M4 dark-matter identity | OP18 (Sec. 6.20) | L4 | Asks *which* excitation dark matter is; the halo tests (OP19, C1–C2) do not depend on the answer | L4, mechanism-first: a candidate field with a stated reason, no fit |
| C5 CP bias / baryon asymmetry | S4 (Sec. 3.6) | L5 | Server-side; the paper has no model; needs three generations, which are a no-go under existing rules (M3) | L5, **mechanism-first with no numerical target** (the measured baryon-to-photon ratio, η ≈ 6.1×10⁻¹⁰, is recorded for later use only) |

Other candidates Edmond may want to look at with the same question (left in the main line for now): C2 soliton core (no open-problem number, no measured target), and the neutrino parts of OP12 (splittings, PMNS, absolute scale).
