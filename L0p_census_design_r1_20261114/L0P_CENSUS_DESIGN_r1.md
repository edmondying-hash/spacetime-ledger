---
title: "L0′ census design, revision r1: simple cubic (6-face) grid, with BCC/dirac4 as baseline"
subtitle: "Pre-registered design for the Quantized Space-Ledger restart, carrying Edmond Ying's answers to OD1–OD18. Prepared by spacetime, 2026-11-14 (America/New_York)."
geometry: margin=2.2cm
mainfont: DejaVu Serif
monofont: DejaVu Sans Mono
fontsize: 10pt
---

# 0. What this document is

This is revision r1 of the L0′ census design. It carries Edmond's answers to all 18 open decisions of the original design (Section 0.1), and it is the text the census runs on. Nothing in it has been run. The only computations behind it are the definition checks and the random-matrix timing proxy of the original folder (Appendix A, Section 7). Neither evaluates a gate, scans a spectrum or scores a candidate, and neither is part of the census. No launcher or code is part of this design; the implementation is written against this file's sha256 (Section 1.3).

**Inputs (all read on 2026-11-14):**

| Input | Identifier |
|---|---|
| Repository `edmondying-hash/spacetime-ledger`, fresh clone of `main` | HEAD `8a6a0b1ec46e5f3f6737b26c970018273f97721c` |
| `space-ledger-v2.md` on that HEAD | sha256 `ce22701ca6e5e2dfa143ab43a6062e80025c1afeba5137f7e271c239bc75555c` |
| Plan v3.4, `layered_plan_v3_4_draft_20261112/layered_plan_v3.4.md` (L0 §2, standing rules §0) | sha256 `a50dd0a0d5c9304e782d8482905167d797f4973106d9a27326c69572a1e846cf` |
| Real-problem definition, `/workspace/L0p_real_problem_final_20261114/REAL_PROBLEM_DEFINITION.md` | sha256 `6bf2f171779e57fab083836c444bb798820556af5d224a51118473b2e39a2534` |
| Six-face paper revision, `/workspace/paper_six_face_20261114/space-ledger-v2_sixface_draft.md` / `.pdf` | sha256 `c2ef2e7bd875ecdeb11918c707f13189b2d384917211202a10562e169ba4c36e` / `44b13059840c891787c6554b292ad0dab9106d4502854fd933e87cec7ab67b93` |
| Reopened-items list, `/workspace/paper_six_face_20261114/CHANGES_AND_REOPENED.md` | sha256 `552db0892fa5b7dbe1eee41d00c92f8d315e31d207375485c23025286f79dee9` |
| `dirac4` symbol extract on main, `toys/bcc_test4/dirac4_cycle_symbol.py` (cites frozen `dirac4.py` sha256 `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff`) | sha256 `cc4bb988e81e5e93937184ce89cb14f7cbb847c058551fd0b5406b4ccd8f77d6` |
| L0 V4 pre-registration (drift band convention reused in S6), `/workspace/L0_V4V5_prereg_20261111/PREREG_L0_V4_V5.md` | as hashed in that folder |

## 0.1 Revision r1: source documents and Edmond's answers

**Superseded text (kept unchanged in `/workspace/L0p_census_design_20261114/`):**

- `L0P_CENSUS_DESIGN.md`, sha256 `44e02b9712bae14b300fb053df471545339d38a4739d80a11a3b9e53b6189683`
- `OPEN_DECISIONS.md`, sha256 `6398dc2be1ca186876323f632516eb695be73c1fac86697b83d259a99bd95741`
- that folder's `SHA256SUMS`, sha256 `6bdc887ec141bf054d910911f33c379a4d18bdc5d4a10dfbdf2c647b3c2046f6`; its `checks/` files are cited in Appendix A by their sha256 values, unchanged.

**Source of the answers.** Edmond Ying's reply in helper's chat, 2026-11-14 at 11:33 AM EST, relayed to spacetime by helper: "Go with all your recommendations for OD1 to OD18". The answers below are as relayed. Every option not listed here is removed from this revision.

| OD | Question | Answer (option) | Where it takes effect |
|---|---|---|---|
| OD1 | Knob range for φ (B0, C1, C3) | (a) φ ∈ [0.5, 1.5] | §4 knob grids; §3.2, §3.3, §3.5; Appendix R |
| OD2 | Knob range for θ (C2) | (a) θ ∈ [π/16, π/4] | §4 knob grids; §3.4 |
| OD3 | Quasi-energy-π touchings in F1 | (a) counted as light species; any π-touching gives F1 NOT MET | S3 |
| OD4 | Planck-scale gap floor g_P | (a) g_P = 0.01 in Δ̂ | S3 |
| OD5 | KS phases under F2 | (a) allowed, with the same standing as a checkerboard | §3.4; S7 |
| OD6 | Fixed layer order under F2 | (a) not a fixed direction, provided F4 and F5 (including ΔQ₂) are within their thresholds | §3.7; S7 |
| OD7 | Static load field for F5b | (a) lattice Green function of the face-graph Laplacian | S5b |
| OD8 | Length unit for B0 | (a) ℓ = a√3/2, kℓ = √3 k_grid | §2; S4; S5 |
| OD9 | Form of B0 | (a) unrepaired one-orbit `dirac4`, φ the only knob | §3.2; S7 |
| OD10 | Repair round | (a) Appendix R families frozen in this revision with exact forms and ranges | §8; Appendix R |
| OD11 | Stop rule | (a) full census: every candidate on every step | §4 |
| OD12 | F5 sizes and thresholds | (a) σ ∈ {1.5, 3, 6}, r ∈ {3, 6, 12}, magnitudes ≤ 10⁻² (leakage ≤ 10⁻³), slopes ≤ −1.5 | S5 |
| OD13 | Machine | (a) the box, CPU, 3 GiB peak RSS, 15,540 CPU s census caps | §7; S0 |
| OD14 | C4 definition | (a) coinless palindromic product of 1D Weyl walks, no knob | §3.6 |
| OD15 | F4 numeric-zero thresholds | (b) 100× the scalar control's measured floor, frozen by the control before any candidate is fitted | S4 (exact procedure there) |
| OD16 | C1 definition | (a) as written: per-axis face Wilson layers, all at angle φ | §3.3 |
| OD17 | Congestion | (a) free-rule carve-out, "load rule: none" | §1.4 |
| OD18 | Run decision | (b) one run on a new hashed revision carrying these answers (this file) | §1.3; §7 |

**What r1 adds beyond replacing options** (specification required by the answers, not new choices of option):

1. The exact OD15(b) procedure (S4).
2. The exact frozen repair families and ranges (Appendix R). Two specification points in Appendix R were not options in `OPEN_DECISIONS.md`. They are marked "r1 specification" there: R-C3 uses φ_F = φ (no added knob, checklist item 1), and R-C2 has no frozen form.
3. Caps for the repair round, listed separately from the OD13 census caps (§7).
4. A memory preflight on the box: under OD13(a) the run stops at S0 if free memory is below 3.5 GiB. It does not move to another machine (S0, §7).

# 1. Fixed inputs

## 1.1 The gates (quoted verbatim from the hashed definition, sha256 6bf2f171…2534)

> **Scope.** Every candidate rule is scored against the same gates, including the baseline, BCC/dirac4 (8 corner hops) as recorded on main. The simple cubic candidates are Wilson, staggered, a 4-component dirac4 analogue, and split-step.
>
> **Hard gates (failing any one disqualifies a candidate)**
>
> - F1 Species. At low energy there is exactly one light Dirac/Weyl species. Any extra species must be lifted to the Planck scale by a declared repair term, and every gated result must be insensitive to that term across a range stated before scoring.
> - F2 Bias. One species is reached without a preferred sublattice or a fixed direction, and without any position-dependent sign pattern other than a checkerboard sign. A checkerboard (staggered) sign is not counted as a bias.
> - F3 Reversibility. The rule is unitary and reversible.
> - F4 Dispersion. There is no term linear in k. Any direction-dependent term goes as (k l)^2 or smaller and stays within the Fermi/LHAASO bounds.
> - F5 Isotropy. A new pre-registered large-scale test must show anisotropy decaying as its gate requires. It measures how far a point-source front leaks outside the c0*n sphere, and the angular spread of the static load field as a function of r.
>
> **Knob rule.** A declared continuous knob is allowed only if every gated result is insensitive to it across the pre-stated range. Having to tune a knob to pass is a fail (checklist 1 and 7).
>
> **Simplicity test.** The baseline dirac4 has 4 components and 2 declared knobs (phi and the Wilson r). A simple cubic rule passes only if it has at most 4 components and at most 2 declared knobs.
>
> **Trigger.** The fallback to BCC/dirac4 applies if no simple cubic candidate passes F1-F5, the knob rule and the simplicity test. The outcome is to be read alongside how the BCC baseline itself scores on the same gates.
>
> **Timebox.** One census round over the four pre-listed candidates, plus at most one pre-registered repair round. Every failed run is kept on record.
>
> **Not a real problem.** (k l)^2 anisotropy within bounds; axis/diagonal ordering reversed relative to BCC; no prior citation for the rule; BCC numbers in the paper that need rewording.

## 1.2 Edmond's checklist (2026-11-14), applied to every design choice below

1. Less is more; anything added is a declared knob.
2. No built-in bias; any lattice bias must fade at large scales.
3. Reversible substrate, no arrow of time.
4. The network only passes state; apps carry direction, momentum and mass.
5. Local cells update from their 6 face neighbours on the tick.
6. Measured data beats principle.
7. No fitting.
8. A cheap pre-registered test comes before any foundation rewrite.

How the design uses them: item 4 sets the mass to m = 0 in every gated step (mass is an app property, not a substrate knob). Item 5 requires every hop layer of every simple cubic candidate to move amplitude by at most one face (checked in S1). Item 2 is tested by F2 (structure) and by F4/F5 (whether lattice effects fade). Item 3 is F3. Items 1 and 7 are the knob rule and the simplicity test. Item 8 is the reason this census comes before any paper rewrite.

## 1.3 Run discipline (binding on the census)

- This document and its folder are hashed before any scored computation. The implementation is written against this hash, hashed itself, and given a check-only dry run (definition checks and record reads only, no gate) before the scored run.
- One attempt per step. No retry and no re-scoring. A step that errors, trips a cap or loses a control is recorded as UNINFORMATIVE with its raw output and is not repeated inside this census.
- A result that cannot discriminate (for example a slope fitted to values all at the floating-point floor, or a control outside its band) is marked UNINFORMATIVE. It is never read as meeting or not meeting a gate.
- No fitting to targets. Fitting the size of a measured effect (a dispersion coefficient, a decay slope) is allowed and is labelled as such (plan v3.4 §0.1 rule 4).
- Like with like: every candidate, including the BCC baseline B0, is measured by the same code path, observable, grid rule (in units of its own link length ℓ), source, read-out and threshold.
- Every step records CPU seconds, wall seconds and peak RSS, together with code sha256, design sha256, seed, grid, boundary, units, knob value and load rule, in `runs/<date>_L0p_census/<candidate>/<step>/result.json`.
- Every step has caps (Section 7). A cap trip ends that step as UNINFORMATIVE.
- Every run output is kept unchanged, including failed and partial ones.
- Outcome vocabulary inside results: **MET**, **NOT MET**, **UNINFORMATIVE**. This document itself carries no outcome or status words.

## 1.4 Load rule (congestion)

The census scores free rules: every step declares "load rule: none (free rule)". Plan v3.4 §0.1 rule 1 keeps congestion ON except under declared carve-outs (V4 on 2026-11-11; B3 for L1.1–L1.3). Per OD17(a), the same free-rule carve-out covers this census.

# 2. Conventions

- **Grid (simple cubic).** Sites x ∈ ℤ³, one Planck cube of side ℓ per site, face links h ∈ {±e_x, ±e_y, ±e_z}. Spacing = link length = cube side = ℓ. With one Planck volume per site, ℓ = ℓ_P (paper reopened item D3), so kℓ = E/E_P.
- **Grid (BCC baseline B0).** One BCC orbit of the integer grid (all-even or all-odd coordinates), corner hops (±1,±1,±1) in units of a/2, as on main. Per OD8(a), ℓ = link length = a√3/2, so kℓ = √3 k_grid.
- **Fourier convention.** (T_h ψ)(x) = ψ(x − h) has symbol e^{−ik·h}. For a Hermitian involution M with projectors P^± = (1 ± M)/2, the conditional shift along axis i, (S ψ)(x) = P⁺ψ(x − e_i) + P⁻ψ(x + e_i), has symbol e^{−i k_i M}. Every such layer moves each amplitude by exactly one face.
- **Matrices.** Pauli σ_a act inside a two-component Weyl spinor. τ_a act on the (R, L) label. Chiral Dirac basis: α_i = τ_z ⊗ σ_i, β = τ_x ⊗ 1.
- **Cycle and quasi-energy.** Each candidate is a periodic sequence of layers (a cycle). U(k) is the one-cycle symbol. Its eigenvalues are e^{−iω_j(k)} with ω_j ∈ (−π, π] per cycle. Results are evaluated only at cycle boundaries.
- **Tick-convention-free energy unit.** Let c̄₀ be the direction-averaged low-energy speed of the candidate, in ℓ per cycle (from S4). A quasi-energy ω per cycle corresponds to ω/(c̄₀/ℓ) in units of E_P = ħc/ℓ_P with c the realised light speed. This is written Δ̂ = ω/c̄₀ (ℓ = 1). It does not depend on how many layers count as one tick, so candidates with different cycle lengths are compared on one scale. Paper Table `dirac4` quotes gaps per tick, so its 0.082 is not on the Δ̂ scale; B0 is re-measured on the Δ̂ scale.
- **Mass.** m = 0 in every gated step (checklist 4).
- **Directions.** D13 = {[100], [010], [001], [110], [1−10], [101], [10−1], [011], [01−1], [111], [1−11], [11−1], [−111]}, plus their negatives (D26).
- **Seeds.** Random states use numpy PCG64 with seed 20261114 + 100·(candidate index) + (state index). Candidate indices: B0 = 0, C1 = 1, C2 = 2, C3 = 3, C4 = 4, R-C3 = 5.

# 3. Candidate rules

Each SC candidate is written out exactly once below. That is the form scored in the census round. Each candidate's component count and declared knobs follow from its definition and are fixed here.

| Id | Rule | Lattice | Components per node | Declared knobs (census round) | Hop layers / on-site layers per cycle |
|---|---|---|---|---|---|
| B0 | `dirac4` as on main (baseline) | one BCC orbit | 4 | φ (OD9(a)) | 2 corner-hop / 2 mixed (4 layers) |
| C1 | Wilson: `dirac4` step with face-local Wilson layers | SC | 4 | φ | 18 / 12 |
| C2 | Staggered (Kogut–Susskind), brickwork | SC | 1 | θ | 12 / 0 |
| C3 | 4-component `dirac4` analogue, face sub-layers | SC | 4 | φ | 18 / 4 |
| C4 | Split-step, palindromic product of 1D Weyl walks | SC | 2 | none (OD14(a)) | 6 / 0 |

**D'Ariano–Perinotti no-go (PRA 90, 062106, 2014).** Under their assumptions (a single-step, nearest-neighbour, isotropic, two-component automaton on the Cayley graph of an Abelian group), the minimal Weyl automaton exists on BCC and not on the simple cubic lattice. None of C1–C4 is inside that assumption set. C1 and C3 have four components, C2 has an 8-site cell, and C1, C3 and C4 are multi-layer (one face per layer). So the no-go does not exclude them. It also gives no reason to expect them to meet F1–F5; the census measures that.

## 3.1 Shared building blocks

- One-axis Weyl factor: e^{−ik_iσ_i}. It is a conditional face shift along ±e_i (S1-checkable).
- A⁺(k) = e^{−ik_xσ_x} e^{−ik_yσ_y} e^{−ik_zσ_z} and A⁻(k) = e^{−ik_zσ_z} e^{−ik_yσ_y} e^{−ik_xσ_x} (reverse order).
- **Fact K1 (Appendix A).** These equal the `dirac4` matrices A^ε = u^ε − i n^ε·σ of `dirac4_cycle_symbol.py` for ε = ±, to 2.3×10⁻¹⁶. So the BCC corner hop of `dirac4` factors into three face sub-steps, and the alternation of handedness (ε = +, −) in `dirac4` is exactly a palindromic ordering of the face sub-steps.
- Step layers S^ε = diag(A^ε, A^{ε†}). The R block applies the axes in one order. The L block uses +σ shifts in the reverse order (K3b). R and L shifts act on different components, so sub-step j moves R along one axis and L along another, at most one face each.
- **Fact K2.** X^ε = u^ε τ_x + τ_y ⊗ (n^ε·σ) = τ_x diag(A^{ε†}, A^ε), and the `dirac4` Wilson layer V^ε = (cos φ − i sin φ X^ε)(cos φ + i sin φ τ_x) equals Q e^{−iφτ_x} Q† e^{iφτ_x} with Q = diag(1, A^{ε†}). So V^ε is three face sub-shifts of the L block, an on-site rotation, three face sub-shifts back, and an on-site rotation.

## 3.2 B0 — baseline: `dirac4` on one BCC orbit (as recorded on main)

U_B0(k) = V⁻ S⁻ V⁺ S⁺ at m = 0, on one BCC orbit, k per a/2, exactly the frozen `dirac4.py` (sha256 `f71c782e…aff`) / `dirac4_cycle_symbol.py` (sha256 `cc4bb988…77d6`). Γ images are πg with g an integer triple of even coordinate sum, as in V3 and the V5 v2 census. Form per OD9(a): unrepaired one-orbit `dirac4`, φ the only knob (main since 2026-11-12), with φ ∈ [0.5, 1.5] (OD1(a)). The r8 sum-form repair is not used.

## 3.3 C1 — Wilson (face-local Wilson layers)

- Face Wilson involution on axis i: X_i(k) = β e^{ik_iα_i} (Hermitian, X_i² = 1; K4). Its range is one face along e_i.
- Face Wilson layer: W_i(φ) = (cos φ − i sin φ X_i)(cos φ + i sin φ β). It is unitary (K4), equals 1 at k_i = 0 and e^{2iφβ} at k_i = π (K4). Implemented as Q_i e^{−iφτ_x} Q_i† e^{iφτ_x} with Q_i = diag(1, e^{ik_iσ_i}): two face sub-shifts of the L block and two on-site rotations.
- Mirrored Wilson blocks: V_F⁺ = W_z W_y W_x (x applied first), V_F⁻ = W_x W_y W_z.
- Cycle: **U_C1(k; φ) = V_F⁻ S⁻ V_F⁺ S⁺**, m = 0 (OD16(a)). This is the `dirac4` cycle with each corner-reach Wilson layer replaced by three per-axis face Wilson layers of the same angle φ.
- Source: Wilson's doubler-lifting term (Wilson 1977), in the unitary on-site-plus-hop form of paper §6.2. The per-axis face form is built here; no prior publication of this exact rule is known to the author ("no prior citation" is listed in the definition as not a real problem).
- **Definition-level fact (K5, closed form).** At a cube corner with p components equal to π, U_C1 = e^{4ipφβ}. Its quasi-energies are ±4pφ (mod 2π). So corner gaps close (ω = 0) at φ ∈ {π/6, π/4, π/3, π/2} in (0, π/2], and corner quasi-energy-π touchings occur at φ ∈ {π/12, π/8, π/4, 3π/8, 5π/12}. These are properties of the definition, not census results. Off-corner zeros, if any, are found only by S3. The OD1(a) range [0.5, 1.5] contains π/6, π/4 and π/3 (ω = 0) and 3π/8 and 5π/12 (ω = π); the knob rule in S7 applies as written.

## 3.4 C2 — Staggered (Kogut–Susskind phases, brickwork unitary)

- One complex amplitude per site. Kogut–Susskind phases η_x(x) = 1, η_y(x) = (−1)^{x₁}, η_z(x) = (−1)^{x₁+x₂} (Kogut & Susskind 1975; Susskind 1977). Every elementary face carries flux π: the product of η around each plaquette is −1 (K6). Per OD5(a), these phases have the same standing under F2 as a checkerboard sign.
- Bond layer B_{i,p}(θ), i ∈ {x,y,z}, p ∈ {0,1}: for every site x with x_i ≡ p (mod 2), the pair (a, b) = (ψ(x), ψ(x + e_i)) becomes (cos θ·a + η_i(x) sin θ·b, −η_i(x) sin θ·a + cos θ·b). Each layer is a set of disjoint one-face rotations (real orthogonal, hence unitary).
- Cycle (palindromic, rightmost applied first): **U_C2(θ) = B_{x,0} B_{x,1} B_{y,0} B_{y,1} B_{z,0} B_{z,1} · B_{z,1} B_{z,0} B_{y,1} B_{y,0} B_{x,1} B_{x,0}**. For small θ, U_C2 ≈ exp(−2iθ H_KS), with H_KS the Hamiltonian staggered operator.
- Symbol: 2×2×2 cell, 8 sublattices, 8×8 Bloch matrix on the reduced zone [−π/2, π/2]³ (k per ℓ). Γ images: πℤ³.
- Known background (literature, not a census result): the Hamiltonian staggered operator in three space dimensions carries two four-component tastes (Susskind 1977).

## 3.5 C3 — 4-component `dirac4` analogue on face sub-layers

- **U_C3(k; φ) = V⁻ S⁻ V⁺ S⁺**, with S^ε made of face sub-steps (Section 3.1) and V^ε = Q e^{−iφτ_x} Q† e^{iφτ_x} made of face sub-shifts (K2). As a function of k this is identical to the `dirac4` symbol (K3: 8.7×10⁻¹⁶ over 200 random (k, φ)). Every hop layer moves amplitude by at most one face.
- What changes is the lattice. All of ℤ³ is occupied, the reciprocal lattice is 2πℤ³, and the points (±π,±π,0) and permutations are no longer Γ.
- **Definition-level fact (K5).** At corners with p even, U_C3 = 1 exactly (p = 2: |U − 1| ≤ 6.8×10⁻¹⁶). At p odd, |U − 1| = 0.63 at φ = 1.4. Equivalently, the corner-hop group has index 4 in ℤ³, so U_C3 on ℤ³ is four decoupled copies of B0 (one per coset). These are definition facts; the gated count is S3's.
- Source: paper §6.2 (`dirac4`); D'Ariano & Perinotti (2014) for the Weyl pair; the face-sub-layer realisation is built here.

## 3.6 C4 — Split-step (palindromic product of 1D Weyl walks)

- Two components. **U_C4(k) = A⁻(k) A⁺(k) = e^{−ik_zσ_z}e^{−ik_yσ_y}e^{−ik_xσ_x} · e^{−ik_xσ_x}e^{−ik_yσ_y}e^{−ik_zσ_z}**: six one-face conditional shifts per cycle, no coin, no knob (OD14(a)). This is the operator-splitting Weyl walk of Bialynicki-Birula (PRD 49, 6920, 1994) and Arrighi, Nesme & Forets (J. Phys. A 47, 465302, 2014), in palindromic order.
- **Definition-level fact (K5).** U_C4 = 1 at all eight cube corners.

## 3.7 Fixed layer order

C1, C3, C4 and C2 apply axes in a fixed palindromic order (x, y, z, then z, y, x). Per OD6(a), a fixed layer order is not a fixed direction under F2, provided F4 and F5 (including ΔQ₂) are within their thresholds. B0's corner hop has no temporal order inside a layer.

# 4. Steps, observables and gates

Steps run in the order S0–S7, for every candidate (B0, C1, C2, C3, C4). Per OD11(a), every candidate is scored on every step, whatever its earlier outcomes. A cap trip or an UNINFORMATIVE control ends only that step for that candidate. The one exception is the S0 memory preflight, which stops the whole run.

**Knob grids (pre-stated).** φ ∈ [0.5, 1.5] for B0, C1, C3 (OD1(a)): K7 = {0.5, 0.6667, 0.8333, 1.0, 1.1667, 1.3333, 1.5} (exactly 0.5 + j/6, j = 0…6) and K3 = {0.5, 1.0, 1.5}. θ ∈ [π/16, π/4] for C2 (OD2(a)): K7 = π/16 + j·(3π/16)/6 = π/16 + jπ/32, j = 0…6, and K3 = {π/16, 5π/32, π/4}. C4 (OD14(a)) has no knob grid.

## S0 — Preflight (not gated)

- **Memory preflight (OD13(a)).** Read MemAvailable from `/proc/meminfo`. If it is below 3.5 GiB (3,670,016 kB), the run stops at S0: no later step runs, the whole census is recorded as UNINFORMATIVE with the measured value, and the run does not move to any other machine. A later attempt would be a new run under a new decision.
- Recompute K1–K7 (Appendix A) inside the implementation. Recompute the code sha256 and compare it with the hashed implementation manifest. Record the environment (python, numpy, scipy, BLAS, thread count). Any mismatch makes the whole census UNINFORMATIVE before any gate.

## S1 — V1 analogue and F3: unitarity, reversal, light cone (time evolution, real space)

- Grid: SC L = 24 periodic (B0: 48 in a/2 units, orbit sites only), complex128. Knob values: K3.
- (a) **Unitarity.** Random normalised state (seed above), 50 cycles. δQ = |Q(n) − 1| ≤ band C = 10·N_layers·ε₆₄ (ε₆₄ = 2.22×10⁻¹⁶; the convention of the L0 V4 pre-registration).
- (b) **Reversal.** Apply 50 cycles, then the adjoint layers in reverse order for 50 cycles. Require max_x |ψ − ψ₀| ≤ 10·(2N_layers)·ε₆₄.
- (c) **Light cone (checklist 5).** For each internal basis state e_j, start from a delta at the origin. After every layer, amplitudes outside the reach ball (Manhattan radius = number of hop layers applied so far for SC; Chebyshev radius in a/2 units = number of corner-hop layers for B0) must be exactly 0.0. Shifts are exact index moves, so any nonzero value there is an implementation or definition error.
- **F3 is MET** iff (a), (b) and (c) hold at every K3 value. **UNINFORMATIVE** if S0 found a mismatch.
- **Record only (no gate): time-reversal test for checklist 3.** For each M in the 16 matrices {τ_a ⊗ σ_b} (4 components), the 4 σ_b (2 components), or the 8 sublattice sign patterns (C2), test whether M U(k)* M⁻¹ = U(−k)† at 1000 random k to 10⁻¹². Record which M work.

## S2 — V2 analogue: scalar dispersion reference, and symbol vs time evolution

- (a) **Six-face scalar reference (paper §6.4 Test 1; substrate check, rule-independent).**
  - Analytic part: the a = l_P extrapolation table (1 GeV: 8.4×10⁻⁴⁰ [100] to 2.8×10⁻⁴⁰ [111]; 30 GeV 7.6×10⁻³⁷; 31 GeV 8.1×10⁻³⁷; 1 TeV 8.4×10⁻³⁴) and E_QG,2 ≈ 4.2–7.3×10¹⁹ GeV must be reproduced to the printed digits from (1/8)(E/E_P)²Σn_i⁴ with E_P = 1.22×10¹⁹ GeV.
  - Time-evolution part: second-order leapfrog with the 6-face Laplacian at λ = 0.5, planar Gaussian packets along [100], [110], [111] at ka ∈ {0.25, 1.0, 2.0}, in a periodic 3D box (transverse ≥ 4 sites; longitudinal 4096 plane indices; packet width 40 planes; centroid speed over ticks 200–1200). The 9 measured speeds must agree with the printed table to the printed 4 digits or within 2×10⁻⁴ (plan v3.4 §0.5; the paper states about 1×10⁻⁴ agreement).
  - For B0 (record, like with like): the BCC scalar coefficients 1/24, 1/12, 7/72 ([100], [110], [111]; paper §6.15(i)) are reproduced analytically to 10⁻¹².
- (b) **Symbol vs real-space evolution (per candidate, K3).** On an L = 24 periodic grid, for 20 plane waves e^{ik·x} u with k on the grid 2πm/L (fixed list: Γ, the 7 non-Γ corners where representable, and 12 seeded random grid momenta) and u a random internal vector, one cycle in real space must equal U(k)u to 10⁻¹² (max abs). For C2 the cycle is compared with the 8×8 Bloch symbol on the 2-cell.
- **V2 is MET** iff (a) and (b) hold. Under plan §0.5, any printed cell at or below its own resolution floor would be declared UNINFORMATIVE in advance; none is expected here.

## S3 — V3 analogue, F1 and the taste census (symbol / spectrum analysis)

- **Scan.** At every K7 knob value, evaluate eig U(k) on a boundary-inclusive 129³ grid of [−π, π]³ (C2: 65³ over the reduced zone [−π/2, π/2]³, the same k spacing). The gap function is g₀(k) = min_j dist(ω_j(k), 0 mod 2π). The π-function is g_π(k) = min_j dist(ω_j(k), π mod 2π).
- **Refine.** Refine every grid local minimum (26-neighbourhood) of g₀ and of g_π with value below 0.5, plus every high-symmetry point (SC: Γ, X, M, R and images; BCC: Γ, H, N, P and images), by Nelder–Mead (xatol 10⁻¹⁰, fatol 10⁻¹⁴, maxiter 2000).
- **Classify.** A refined point with g ≤ 10⁻⁹ is a zero (ω = 0) or a π-touching (ω = π). Its degeneracy is the number of eigenvalues within 10⁻⁶ of the target. Zeros are reduced modulo the candidate's Γ-image lattice (SC 2πℤ³; C2 πℤ³; B0 πg with even-sum g). All other refined minima are gapped minima, with Δ̂ = g/c̄₀ taken at the same knob value (c̄₀ from S4).
- **Lines and surfaces.** Count the grid points with g₀ < 10⁻⁶ at 65³ and 129³ (C2: 33³ and 65³). If the count grows by more than 2× when the grid is refined, the zero set is not isolated. That is recorded and gives F1 NOT MET.
- **Taste census table (recorded for every candidate and knob value).** For each zero and π-touching: location, degeneracy, the velocity tensor (finite differences, step 10⁻⁵), tilt, and chirality where defined. Chirality is the Berry flux of the bands below the node through a cube of half-side 0.05 (Fukui–Hatsugai–Suzuki); it is record only, and "not computed" is an allowed entry. For gapped minima: location and Δ̂.
- **Species count.** N_states(0) = total degeneracy of all zeros after reduction. N_states(π) = the same for π-touchings. In Dirac units, N_D = N_states/4; a single Weyl node has N_states = 2.
- **F1 is MET** at a knob value iff all three hold:
  1. The only zero after reduction is Γ, with N_states(0) = 4 (one Dirac) or 2 (one Weyl).
  2. Every gapped minimum outside the radius-0.3 Γ neighbourhood has Δ̂ ≥ g_P = 0.01 (OD4(a)).
  3. There is no π-touching, and every π-gapped minimum has Δ̂_π ≥ 0.01 (OD3(a): π-touchings count as light species).
- F1 for the candidate is MET iff it is MET at every K7 value (knob rule).
- **Declared repair terms.** For B0, C1 and C3 the declared repair term is the Wilson layer with angle φ; its pre-stated range is φ ∈ [0.5, 1.5] (OD1(a)). C2 and C4 have none in the census round.
- **Order.** Δ̂ uses c̄₀ from S4 at the same knob value; the implementation runs S4's ray fit before S3's classification.
- **Repair.** A census-round candidate whose definition has no repair term (C2, C4) cannot use one in this round. Repairs belong to the single repair round (Section 8, Appendix R).
- **Control.** At S3 the scan is also run once on the naive SC Dirac symbol Σα_i sin k_i (as a Floquet exponential, one cycle e^{−iΣα_i sin k_i}), whose 8 species at k_i ∈ {0, π} are known (`sixface_checks_out.json`). If the scan does not report exactly 8 zero points of degeneracy 4, S3 is UNINFORMATIVE for every candidate.

## S4 — F4 dispersion (symbol analysis)

- **Rays.** For each of D26 and each K7 knob value, take k = κn̂ with κ ∈ {0.010, 0.015, …, 0.200} (39 values; κ = kℓ; B0 uses kℓ = √3 k_grid, OD8(a)). The bands b are those with ω → 0 at Γ, sorted at each κ.
- **Fit (size of a measured effect).** Least squares ω_b(κ) = Σ_{m=1}^{7} a_m κ^m, no constant term. Then c₀(n̂,b) = a₁, ξ₁ = a₂/a₁, ξ₂ = a₃/a₁, in the paper's convention ω = c₀E(1 + ξ₁E/E_P + ξ₂(E/E_P)²), with E_QG,1 = E_P/(2|ξ₁|) and E_QG,2 = E_P/√(2|ξ₂|).
- **Control and frozen thresholds (OD15(b)).** This runs once, before any candidate is fitted.
  1. Control symbols: for each matrix size d ∈ {2, 4, 8}, U_ctrl,d(k) = R_d · diag(e^{−iω_s(k)} I_{d/2}, e^{+iω_s(k)} I_{d/2}) · R_d†, with ω_s(k) = 2√(Σ_i sin²(k_i/2)) the six-face scalar symbol (paper Test 1) and R_d a fixed Haar-random d×d unitary (numpy PCG64 seed 20261114 + 900 + d, QR of a complex Gaussian matrix, with column phases fixed by the diagonal of the triangular factor). These pass through exactly the candidates' code path: same rays (D26), same 39 κ values, same eigenvalue, argument, sorting and degree-7 fit.
  2. Measured floors, for each d: F_ξ(d) = max over D26 and the d/2 bands with ω > 0 of |ξ₁|; F_c(d) = max of |c₀(n̂,b)/c̄₀ − 1| over the same set.
  3. Validity: ξ₂[100] = −1/24 and ξ₂[111] = −1/72 to 10⁻⁶, F_ξ(d) ≤ 10⁻⁹ and F_c(d) ≤ 10⁻⁹, for every d. If any of these does not hold, S4 is UNINFORMATIVE for every candidate and no threshold is formed.
  4. Frozen thresholds: T_ξ(d) = 100·max(F_ξ(d), ε₆₄) and T_c(d) = 100·max(F_c(d), ε₆₄), with ε₆₄ = 2.220446049250313×10⁻¹⁶. The ε₆₄ lower bound keeps a threshold from being zero if a control floor evaluates to exactly 0.
  5. Freezing: the six values are written to `S4_control_thresholds.json` (17 significant digits) with the control raw values. Its sha256 goes into the run log and every S4 `result.json` before the first candidate fit. Candidate fitting code loads the file, checks its sha256, and stops S4 as UNINFORMATIVE on any mismatch. The thresholds are not changed after this point.
  6. Size used per candidate: d = 4 for B0, C1, C3 and R-C3; d = 2 for C4; d = 8 for C2.
- **Thresholds.**
  - (i) No linear term: max |ξ₁| ≤ T_ξ(d) over all rays and bands.
  - (ii) Isotropic leading order: max |c₀(n̂,b)/c̄₀ − 1| ≤ T_c(d), with c̄₀ the mean over D26 and bands.
  - (iii) Bounds: |ξ₁| < 0.05 (LHAASO, E_QG,1 > 10 E_P; Fermi 7.6 E_P gives 0.066), implied by (i). |ξ₂| < 1.56×10¹⁴ (LHAASO, E_QG,2 > 6.9×10¹¹ GeV).
  - The direction dependence of ξ₂ (max − min) is recorded with its search template [100]/[110]/[111]. The axis/diagonal ordering is recorded and is not gated (the definition lists it as not a real problem).
- **F4 is MET** iff (i)–(iii) hold at every K7 value.
- Record only: c̄₀ per knob value (used by S3 and S5) and ν-type ratios. ν is not gated in L0′.

## S5 — F5 large-scale isotropy (time evolution, k-space exact)

### S5a — Point-source front

- **Source.** ψ_j(x,0) = N·exp(−|x|²/(2σ²))·e_j for each internal basis vector e_j. d = 4 for B0, C1, C3; d = 2 for C4; d = 8 for C2, with e_j the Gaussian restricted to sublattice j. B0 uses orbit sites only, with σ converted to grid units by ℓ = √3 grid units (OD8(a)). The density is the unpolarised average ρ(x,n) = (1/d)Σ_j |ψ_j(x,n)|², normalised to 1 on the candidate's site set.
- **Sizes.** σ ∈ {1.5, 3, 6} ℓ. Cycles n = round(6σ/c̄₀). Periodic box N = 30σ in ℓ (SC: 45, 90, 180; B0: 78, 156, 312 in a/2 units under OD8(a), rounded up to FFT-friendly sizes).
- **Evolution.** ψ(n) = IFFT[U(k)ⁿ ψ̂(k)]. U(k)ⁿ is formed by repeated squaring per k-plane in complex128; states are stored as complex64 and processed one internal state at a time (U(k)ⁿ is recomputed per state to bound memory). Knob values: K3.
- **Reference (like with like).** The same Gaussian on the full grid, propagated by the isotropic continuum massless rule at the measured c̄₀: ρ_ref = |C|² + Σ_i |S_i|², with C = IFFT[cos(c̄₀|k̃|n) ĝ] and S_i = IFFT[sin(c̄₀|k̃|n)(k̃_i/|k̃|) ĝ], where k̃ are the FFT momenta in [−π, π)³ per ℓ. This is the unpolarised density of a free massless Weyl or Dirac field. It is evaluated on the candidate's site set and normalised there.
- **Observables (shell W: ||x| − c̄₀n| ≤ 3σ).**
  - Leakage excess Λ = P_lat(|x| > c̄₀n + 3σ) − P_ref(same region).
  - Cubic anisotropy excess ΔA = A_lat − A_ref, with A = Σ_W ρ K₄(x̂)/Σ_W ρ and K₄(n̂) = (5/2)(n_x⁴ + n_y⁴ + n_z⁴) − 3/2 (zero mean on the sphere; 1 on [100], −2/3 on [111]).
  - Quadrupole excess ΔQ₂: the largest |eigenvalue| of the traceless second-moment tensor of ρ on W, divided by its trace, lattice minus reference. This is nonzero only if a layer order breaks cubic symmetry.
- **Wrap control.** Probability within 2σ of any box face (at least 6σ beyond the outer edge of W) must be ≤ 10⁻⁷ for both lattice and reference; otherwise that σ is UNINFORMATIVE.
- **Gate F5a (at every K3 value):**
  - |ΔA(σ=6)| ≤ 1×10⁻², |ΔQ₂(6)| ≤ 1×10⁻² and |Λ(6)| ≤ 1×10⁻³; and
  - for each of |ΔA|, |ΔQ₂| and |Λ|, the fitted log–log slope against σ over {1.5, 3, 6} is ≤ −1.5. An O((kℓ)²) effect gives −2.
  - An observable whose three values are all ≤ 1×10⁻¹⁰ is recorded as "below floor" and counts as decaying. Its slope is not fitted, since a slope through floor values would be uninformative.

### S5b — Static load field

- **Field (OD7(a)).** The steady state of local face-neighbour relaxation from a point source: the lattice Green function of the graph Laplacian. SC: L(k) = Σ_i 2(1 − cos k_i). BCC: L(k) = 8(1 − cos k_x cos k_y cos k_z) in a/2 units. It is computed by real FFT on a periodic box with the Γ-image modes removed (SC: k = 0; BCC: the four Γ images on ℤ³). This field belongs to the lattice, not to a candidate, so it is computed once for SC and once for BCC and applies to every candidate on that lattice. Knobs do not enter.
- **Shells.** Lattice sites (orbit sites for BCC) with ||x|_ℓ − r| ≤ 0.5 ℓ, for r ∈ {3, 6, 12} ℓ.
- **Observable.** A_load(r) = Σ_shell K₄(x̂)·|x|G(x) / Σ_shell |x|G(x). The reference A_ref(r) = mean of K₄(x̂) over the same shell sites (the continuum field 1/|x| sampled on the same points). ΔA_load = A_load − A_ref. The quadrupole is recorded only.
- **Boxes.** SC N ∈ {96, 192}; BCC N ∈ {168, 336} (a/2 units, the same size in ℓ under OD8(a)). Gated values use the larger box.
- **Controls.**
  - (1) Box control: ΔA_load(12) from the two boxes must agree within 10% relative or 10⁻⁶ absolute.
  - (2) Method control (SC only): the exact infinite-lattice Green function G(x) = ∫₀^∞ e^{−6t} I_{x₁}(2t) I_{x₂}(2t) I_{x₃}(2t) dt (scipy `ive`, adaptive quadrature, rtol 10⁻¹⁰) on the r = 12 shell must give ΔA_load within 10% of the FFT value.
  - If either control fails, S5b is UNINFORMATIVE for both lattices.
- **Gate F5b.** |ΔA_load(12)| ≤ 1×10⁻², and the fitted log–log slope over r ∈ {3, 6, 12} is ≤ −1.5, or all three values are ≤ 10⁻¹⁰ (below floor).
- **F5 is MET** iff F5a and F5b are both MET. Sizes and thresholds are those of OD12(a), as written above.

## S6 — V4 analogue: drift over 10⁵ layers (time evolution, real space)

- Grid: L = 16 periodic SC (B0: 32 in a/2 units, orbit), complex128, knob at the K3 midpoint.
- States: S1 random (seeded), S2 Gaussian σ = 2 at rest (e₀), S3 delta (e₀).
- Length: N = 10⁵ layers, rounded up to whole cycles.
- Observables at cycle boundaries: norm δQ; quasi-energy expectation δE (complex Schur form of U(k) at t = 0, ω_j ∈ (−π, π], normalised by E_abs(0), as in the L0 V4 pre-registration); band occupations δn.
- Checkpoints, reported only: the cycles nearest {1, 10, 100, 1000, 10⁴} and N.
- **V4 is MET** iff every drift at N is ≤ band C = 10·N·ε₆₄ = 2.22×10⁻¹⁰.
- **Cross-check (UNINFORMATIVE if it does not hold).** The real-space state at N must equal the k-space exact U(k)^{n} state to 10⁻⁹ max abs.

## S7 — Knob rule, simplicity test and trigger read-out (assembly, no new computation)

- **Knob rule.** For each knobbed candidate: MET iff F1, F3, F4, F5 and V1–V4 are each MET at every knob value at which they were evaluated (K7 or K3), with the same zero count in S3 at every K7 value. Any change of outcome across the range gives NOT MET. A result MET at some knob values and not at others means the knob would have to be tuned, which is NOT MET.
- **F2 (structural, from the definitions).** For each candidate, record every position-dependent factor and every fixed order in its definition. C2: KS phases, which have checkerboard standing (OD5(a)). C1, C2, C3, C4 and R-C3: fixed layer order, which is not a fixed direction provided F4 and F5 (including ΔQ₂) are MET (OD6(a)); if F4 or F5 is NOT MET or UNINFORMATIVE for that candidate, its F2 cell takes the same label. B0: none within a layer. F2 is MET iff no remaining factor is a preferred sublattice, a fixed direction, or a sign pattern other than a checkerboard.
- **Simplicity test.** Components ≤ 4 and declared knobs ≤ 2, taken from Section 3 (C1 4/1, C2 1/1, C3 4/1, C4 2/0, R-C3 4/1; B0 4/1 per OD9(a)). Layers per cycle are recorded and not gated.
- **Run decision.** Per OD18(b), the census runs once on this revision, cited by its sha256.
- **Read-out table (results file, not this document).** Rows B0, C1–C4, and R-C3 if the repair round runs. Columns F1, F2, F3, F4, F5a, F5b, knob rule, simplicity, V1, V2, V3 (= S3 scan), V4; then "all SC criteria MET by at least one candidate" (yes / no / UNINFORMATIVE); then B0's row for the same columns, read alongside per the definition's trigger. The trigger statement is written from this table only. Any UNINFORMATIVE cell in a candidate's row means that candidate is not counted as meeting all criteria in this round.

# 5. What the census can and cannot say

- It scores exactly five rules (B0, C1–C4) on fixed knob grids, plus R-C3 if the repair round runs. A candidate that does not meet the gates shows that this definition does not meet them, not that no simple cubic rule could.
- Under OD3(a), a π-touching gives F1 NOT MET even though it sits at quasi-energy π; the taste census records each one.
- F5b scores the lattice's own Laplacian field (OD7(a)), not a full gravity model.
- Nothing here changes the paper, the plan, main or any earlier BCC record.

# 6. Records

Every step writes `result.json` with these fields: design sha256 (this file), implementation manifest sha256, candidate, knob value, step, seeds, grid sizes, boundary condition (periodic, or infinite-lattice for the S5b control), units (ℓ and its definition per OD8(a)), load rule ("none (free rule)", per OD17(a)), caps, CPU seconds, wall seconds, peak RSS (MiB), outcome label, every raw value behind the label, and controls with their values. A top-level `SHA256SUMS` covers every output. Outputs are kept unchanged; any later analysis is a new, separately hashed file.

# 7. Cost, memory, caps and machine

**Timing proxy** (`/workspace/L0p_census_design_20261114/checks/timing_proxy.py`, sha256 `789ac89f378902e06ac56def0b5f14aa5aa5ccc811c3f43fff4036137650d634`, random matrices only, single thread, box, 2026-11-14 ~11:18 AM EST): eigvals of 129² batched 4×4 unitaries 0.082 s; 65² batched 8×8 0.071 s; complex64 FFT round trip 144³ 0.20 s and 216³ 0.84 s; one real-space 4-component layer at L = 16 0.30 ms. Proxy run: 3.7 CPU s, 537 MiB peak RSS.

| Step | Estimate (CPU) | Cap: CPU s | Cap: wall s | Cap: RSS | Cap: output |
|---|---|---|---|---|---|
| S0 preflight | < 10 s | 120 | 180 | 512 MiB | 1 MiB |
| S1 V1/F3 (5 rules × K3) | ~2 min | 600 | 900 | 1 GiB | 10 MiB |
| S2 V2 | ~2 min | 300 | 450 | 512 MiB | 5 MiB |
| S3 F1/V3 (4 knobbed × 7 + C4 + control) | ~25 min | 3600 | 4500 | 2 GiB | 50 MiB |
| S4 F4 (26 rays × 39 κ × K7) | ~2 min | 600 | 900 | 1 GiB | 10 MiB |
| S5a front (5 rules × K3 × 3 σ × d states) | ~30 min | 5400 | 7200 | 3 GiB | 50 MiB |
| S5b static field (SC, BCC; 2 boxes; Bessel control) | ~5 min | 1200 | 1800 | 2 GiB | 10 MiB |
| S6 V4 (5 rules × 3 states, 10⁵ layers) | ~25 min | 3600 | 4500 | 1 GiB | 20 MiB |
| S7 assembly | < 1 min | 120 | 180 | 512 MiB | 5 MiB |
| **Census total (OD13(a))** | **~1.5–2 h CPU** | **15,540** | **20,610** | peak 3 GiB | 161 MiB |

**Repair-round caps** (R-C3 only, and only if it runs; Section 8). S2(a), the S3 control, the S4 control and S5b are lattice-level or rule-independent. They are not repeated: the census values and the frozen `S4_control_thresholds.json` are reused.

| Repair step (R-C3) | Estimate (CPU) | Cap: CPU s | Cap: wall s | Cap: RSS | Cap: output |
|---|---|---|---|---|---|
| S0 preflight (memory rule included) | < 10 s | 60 | 90 | 512 MiB | 1 MiB |
| S1 V1/F3 (K3) | < 1 min | 120 | 180 | 1 GiB | 2 MiB |
| S2(b) symbol vs real space (K3) | < 1 min | 60 | 90 | 512 MiB | 1 MiB |
| S3 F1/V3 (K7) | ~5 min | 900 | 1200 | 2 GiB | 10 MiB |
| S4 F4 (K7) | < 1 min | 120 | 180 | 1 GiB | 2 MiB |
| S5a front (K3 × 3 σ × 4 states, SC) | ~3 min | 600 | 900 | 2 GiB | 10 MiB |
| S6 V4 (3 states, 10⁵ layers) | ~5 min | 720 | 900 | 1 GiB | 5 MiB |
| S7 assembly | < 1 min | 60 | 90 | 512 MiB | 1 MiB |
| **Repair-round total** | **~15 min CPU** | **2,640** | **3,630** | peak 2 GiB | 32 MiB |

**Combined caps (census plus repair round): 18,180 CPU s, 24,240 wall s, peak RSS 3 GiB, output 193 MiB.** The OD13(a) figure of 15,540 CPU s is the census total. The repair-round caps are additional, and are stated here so that both rounds are bounded before the run.

Peak memory is set by S5a for B0 (312³ grid, one internal state × 4 components in complex64 ≈ 0.97 GiB, plus FFT workspace and a float64 density accumulator; about 2 GiB in total).

**Machine: the box (CPU), per OD13(a)**, single process, at most 4 BLAS/FFT threads. The box has 15 GiB RAM, which other work shares; free memory was 2.5 GiB (MemAvailable 2,634,200 kB) at 11:35 AM EST on 2026-11-14, when this revision was written. The S0 memory preflight applies: if MemAvailable is below 3.5 GiB at S0, the run stops there, is recorded as UNINFORMATIVE, and does not move to sparky or any other machine. bigbang is not used, no files on ED or Pixel are touched, and no GPU is needed.

# 8. Timebox and repair round

- **Census round.** S0–S7 above, run once over B0 and C1–C4.
- **Repair round (OD10(a)).** At most one, frozen in Appendix R. It runs only for R-C3, and only if C3's F1 cell in the census round is NOT MET. If that cell is MET or UNINFORMATIVE, the repair round does not run. It runs once, directly after the census round writes its results, with no further design. It uses the same gates, the same knob grids, the same frozen S4 thresholds and the caps in Section 7. No other candidate is repaired.
- After the repair round, or after the census if the repair round does not run, the trigger is read once from the read-out table. There is no open-ended rule search, and every run is kept.

# Appendix A — Definition checks (not part of the census)

Script `/workspace/L0p_census_design_20261114/checks/definition_checks.py` (sha256 `9c1e7ddcf05d0c64a679ce2d82740d6dd5829e3cfd74a08479986983fbf631e6`). It imports `checks/dirac4_cycle_symbol.py`, an unchanged copy of main's file (sha256 `cc4bb988…77d6`). Output `checks/definition_checks_out.json` (sha256 `fc38961da70d74c42da76da6cd08b20cc529cc97f2083724a36e00857d05b8a9`). Run on the box, 2026-11-14 ~11:18 AM EST: 0.45 s wall, 2.2 s CPU, 61 MiB peak RSS. Random points use seed 20261114. No spectrum scan, no gate, no candidate scoring.

| Check | What it verifies | Max deviation |
|---|---|---|
| K1 | A^ε of `dirac4` = product of three one-axis face factors (ε = +: x,y,z; ε = −: z,y,x), 200 random k | 2.3×10⁻¹⁶ |
| K2 | X^ε = τ_x diag(A^{ε†}, A^ε); V^ε = Q e^{−iφτ_x} Q† e^{iφτ_x}, Q = diag(1, A^{ε†}) | 2.3×10⁻¹⁶; 6.7×10⁻¹⁶ |
| K3 | C3 assembled from face sub-layers = `dirac4` symbol, 200 random (k, φ) | 8.7×10⁻¹⁶ |
| K3b | L block of S⁺ = +σ face shifts in order z, y, x | 1.2×10⁻¹⁶ |
| K4 | X_i = βe^{ik_iα_i} is a Hermitian involution; W_i unitary; W_i(0) = 1; W_i(π) = e^{2iφβ} | ≤ 8.9×10⁻¹⁶ |
| K5 | Corners: U_C1 = e^{4ipφβ} (φ = 1.4); U_C3 = 1 at p even, \|U − 1\| = 0.631 at p odd (φ = 1.4); U_C4 = 1 at all 8 | 3.0×10⁻¹⁵ / 6.8×10⁻¹⁶ / 3.5×10⁻¹⁶ |
| K6 | KS phases give plaquette product −1 on every face orientation | exact |
| K7 | C1 and C3 cycle unitarity, 100 random (k, φ) | 3.6×10⁻¹⁵ |

# Appendix B — Sources

- G. M. D'Ariano and P. Perinotti, "Derivation of the Dirac equation from principles of information processing," Phys. Rev. A 90, 062106 (2014). Two-component automaton exists on BCC and not on SC, under their assumptions.
- K. G. Wilson, "Quarks and strings on a lattice," in *New Phenomena in Subnuclear Physics*, ed. A. Zichichi (Plenum, 1977). Wilson term.
- J. Kogut and L. Susskind, Phys. Rev. D 11, 395 (1975); L. Susskind, "Lattice fermions," Phys. Rev. D 16, 3031 (1977). Staggered (one-component) fermions; Hamiltonian taste count.
- H. B. Nielsen and M. Ninomiya, "Absence of neutrinos on a lattice," Nucl. Phys. B 185, 20 (1981). Doubling theorem.
- I. Bialynicki-Birula, "Weyl, Dirac, and Maxwell equations on a lattice as unitary cellular automata," Phys. Rev. D 49, 6920 (1994). Operator-splitting walks on the cubic lattice.
- P. Arrighi, V. Nesme and M. Forets, "The Dirac equation as a quantum walk: higher dimensions, observational convergence," J. Phys. A 47, 465302 (2014). Split-step Dirac walk in 3+1D.
- D. H. Adams, Phys. Rev. Lett. 104, 141602 (2010); C. Hoelbling, "Single flavor staggered fermions," Phys. Lett. B 696, 422 (2011). Staggered taste splitting (Euclidean 4D; any Hamiltonian 3D adaptation is new and would need its own definition).
- D. B. Kaplan, Phys. Lett. B 288, 342 (1992); Y. Shamir, Nucl. Phys. B 406, 90 (1993). Domain-wall chain (paper §6.2; not used in this census).
- T. Fukui, Y. Hatsugai and H. Suzuki, J. Phys. Soc. Jpn. 74, 1674 (2005). Lattice Berry flux (chirality, record only).
- Bounds: Vasileiou et al., PRD 87, 122001 (2013); Abdo et al., Nature 462, 331 (2009); Cao et al. (LHAASO), PRL 133, 071501 (2024). As listed in plan v3.4 §0.3.

# Appendix R — Frozen repair families (OD10(a))

Each family is fixed here, before the census runs. There is at most one repair round (Section 8). Nothing in this appendix runs unless its condition holds.

**R-C3 (for C3). Condition: C3's census F1 cell is NOT MET.**

- Rule: **U_RC3(k; φ) = V_F⁻(φ) V⁻(φ) S⁻ V_F⁺(φ) V⁺(φ) S⁺**, m = 0. S^ε and V^ε are exactly as in C3 (§3.5: face sub-steps, V^ε = Q e^{−iφτ_x} Q† e^{iφτ_x}, Q = diag(1, A^{ε†})). V_F⁺ = W_z W_y W_x and V_F⁻ = W_x W_y W_z are exactly as in C1 (§3.3), with W_i(φ) = (cos φ − i sin φ X_i)(cos φ + i sin φ β) and X_i = β e^{ik_iα_i}.
- r1 specification: the face Wilson angle equals φ (φ_F = φ), so the repair adds a term and no knob (checklist item 1). The two-knob variant listed in the original Appendix R is not part of this revision.
- Components 4; declared knobs 1 (φ); layers per cycle: 30 hop, 16 on-site. Every hop layer moves amplitude by at most one face.
- Pre-stated range: φ ∈ [0.5, 1.5], with the census K7 and K3 grids (§4).
- Scored on S0, S1, S2(b), S3, S4, S5a, S6 and S7, as specified for census candidates, with d = 4. The S5b result for SC and the frozen S4 thresholds (d = 4) are reused.

**R-C2 (for C2). No frozen form; C2 is not repaired.**

- r1 specification: the cited taste-splitting constructions (Adams 2010; Hoelbling 2011) are Euclidean four-dimensional operators with multi-link terms. No published Hamiltonian, one-face-per-layer form exists in those sources. Writing one now would mean trying candidate terms against the spectrum, which the timebox and checklist item 7 rule out. So this revision freezes no R-C2 form, and C2 enters no repair round. Any later C2 repair would be a new design outside this census's timebox.

**R-C4 (for C4). None.** Nielsen–Ninomiya forbids a single Weyl node, and a Dirac point needs four components, so a two-component rule keeps at least two Weyl nodes at distinct momenta and cannot reach the F1 count. Doubling to four components with face Wilson layers turns C4 into the C1 family, which is already in the census.

**R-C1 (for C1). None.** A C1 repair would be a new rule definition.

**B0. None.** It is the baseline and is scored only as written.
