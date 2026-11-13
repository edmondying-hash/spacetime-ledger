# L1.5 design: the linear-term test on the canonical rule `dirac4` (one BCC orbit, massless excitation)

Quantized Space-Ledger. Draft of 12 November 2026 (America/New_York), revision r3 (r2 after D1, 9:47 PM: congestion ON; r3 after Edmond's 10:14 PM answers to D2 to D8, checked against the old notes), for Edmond Ying's approval. The earlier drafts (r1 `eb166966…`, r2 `ec55d22c…`) were never approved and are superseded. **This document is a design. It runs nothing for any gate, and it edits no paper, plan, Sheet or archived record.** Nothing in it is approved until Edmond approves its sha256 (§9). Plan: `layered_plan_v3.4.md` (signed off 8:38 PM, 2026-11-12), §3 L1.5. The hand derivation that precedes it, as the plan asks, is `L1_5_DERIVATION.md` in this folder.

## 0. What this replaces and what it is

The held L1.5 design (`lorentz_tick_budget_design_20261109`: 25 clock fixtures, 10 light-speed runs, 2 controls) is for the OP4 rule, a diagnostic branch (plan v3.4 §2, B1 and B2). It stays held and does not gate. This design is the `dirac4` version of the **light-speed part** of L1.5 only, called **L1.5a** below. The clock-fixture ("tick budget", moving-clock) part is **not dropped**: plan v3.4 §2 (B2) lists the held L1.5 tick-budget design among the results to be redone on `dirac4`, and the paper's Test 3 (§6.4, line 704) counts moving-clock tests as part of it. It is a separate, undesigned item, **L1.5b**, and it needs the massive case (decision D5, open).

Plan item (v3.4 §3): repeat L1.4 with a photon-like vector field and the canonical rule, along at least 13 directions including [100], [110], [111] and [11−1]; fit only ξ₁ and ξ₂ per direction; pass if the implied E_QG,1 in every direction exceeds the Fermi (7.6 E_Pl) and LHAASO (10 E_Pl) limits and E_QG,2 exceeds the LHAASO quadratic limit (6.9×10¹¹ GeV); a direction-odd term is reported with its sky template. The plan also asked for a `dirac4` hand derivation of the linear term before any L1.5 run. That derivation is `L1_5_DERIVATION.md`.

## 1. What the derivation gives, and what the run is for

From `L1_5_DERIVATION.md` (proof marks as there: [P] proved by hand and machine-checked, [C] computed, [F] found and checked):

- **[P]** Two exact identities for equal Wilson angles: `U(−k) = (T X⁻¹) U(k) (T X⁻¹)⁻¹` and `Q U(k) Q⁻¹ = U(k)*` with `Q = σ_z ⊗ σ_y`. Hence the spectrum is even in k and closed under ω → −ω, and the mean of the two lowest positive band frequencies, ω̄, is an **odd function of κ to all orders**: no term linear in the group velocity, in any direction. This is the mechanism behind the paper's "alternating handedness cancels the linear term" and it needs equal angles.
- **[C]** The one thing the symmetry leaves open (a split ±βκ² between the two branches) is zero: the O(κ²) block of the effective Hamiltonian vanishes (2.9e-15) and the branches differ only at O(κ⁵).
- **[F]** `ω̄ = c₀κ[1 + ξ₂'(n̂, φ) κ² + …]` with `ξ₂' = −(1 − q)/3 − (3/8) sin²φ cos²φ/(1 + 3 sin²φ)`, `q = n_x⁴ + n_y⁴ + n_z⁴`, found from numbers and matched at 78 points to 3e-19.

**Order of events, disclosed.** All of these were computed by me in an unscored dry-run on the same symbol the run will use (§10, `dryrun/`), before this design was written. The run is therefore a **reproduction by an independent implementation**, not a first discovery. Which statements are predictions and which are gates is fixed in §4. Under plan §0.1 rule 4 nothing here may be retuned after the run.

## 2. Declared conditions (plan §0.1)

- **Rule and lattice.** `dirac4`, canonical, equal Wilson angle φ on both Wilson layers, one BCC orbit, integer hops, k in radians per a/2 (`κ = |k|`), 2π-periodic. **m = 0.**
- **Field.** The massless `dirac4` excitation, as the proxy for the photon, exactly as the paper's §6.4 Test 3 (line 704) uses the massless Dirac walker (decision D2). No vector or tensor field is built.
- **Load rule: congestion ON (Edmond, D1, 9:47 PM).** L1.5 does not take the B3 carve-out. The paper defines no load term for the §6.2 symbol, so this design **declares** two uniform-load implementations and requires every gated number to hold under both, each at two load levels (decision D1b). Plan §0.1 rule 1 lets a run declare its own load rule; the unloaded symbol is a labelled diagnostic (OFF) and counts toward no gate.
  - **Rule A (paper load-first, uniform clock potential U₀).** The whole cycle is slowed: `U_A = U^g`, `g = f² = e^{−2U₀}` (the paper's per-link light cost 1/f²), with `g` set equal to `s` below for comparability, `U₀ = −½ ln s`.
  - **Rule B (OP4-style, uniform node load ℓ₀).** `s = (1 + ℓ₀)^(−1/2)`; bond angle ∝ √sᵢ√sⱼ and on-site clock phase ∝ s both become s for uniform load, so every rotation angle is scaled by s: each of `S⁺, V⁺, S⁻, V⁻` is replaced by its s-th power (principal branch), `U_B = (V⁻)ˢ (S⁻)ˢ (V⁺)ˢ (S⁺)ˢ`.
  - **Levels.** ℓ₀ ∈ {0.5, 2.0}, i.e. s = 0.8165 and 0.5774, for each rule: four ON conditions A.5, A2, B.5, B2. s = 1 is the unloaded diagnostic.
  - Both rules reduce to the unloaded cycle at s = 1. The rule symbols ℓ₀, s (OP4) and U₀, f (paper) are the §0.4 symbols; each rule is used with its own symbols and they are not mixed within a condition. The numerical link s = g between the two rules is a choice for comparability, not a bridge claimed by the paper.
- **Whole ticks.** The cycle eigenvalue and the whole-cycle hop evolution only; no sub-tick interpolation.
- **Energy convention (D3, accepted by Edmond 10:14 PM).** ω = c₀κ(1 + ξ₁'κ + ξ₂'κ² + …) with E/E_P = sκ, **s = 1 is the verdict convention.** Why: with s = 1 the paper's Test 3 numbers come out (dry-run F, single-handed step `V⁺S⁺`, [111]: ξ₁ = 0.192450 = 1/(3√3), independent of φ and zero along [100]; E_QG,1 = E_P/(2|ξ₁|) = 2.598 E_P; group-velocity slope 2ξ₁ = 0.385; E_QG,2 = E_P/√(2|ξ₂|) ≈ 1.8×10¹⁹ GeV). The paper does not define the convention and mixes three: lines 395 and 641 (`(E/E_P)²/18`, `(kℓ)²/18`, ℓ the link length) imply E/E_P = kℓ = √3κ; line 383 (a = ℓ_P, k·a = 2κ) implies 2κ; Test 3 itself uses κ. Results are therefore also reported for s ∈ {√3, 2}. Larger s only shrinks ξ' in E/E_P units (ξ₂ → ξ₂'/s²), so s = 1 is the least favourable of the three and cannot turn a failure into a pass. E_P = 1.22×10¹⁹ GeV. The ℓ_P identification stays an open paper item.
- **The paper's "|ξ₂| ≤ 0.23".** Dry-run F: that bound holds for φ ≥ 1.275 only. At φ = 0.5 the body-diagonal value is 0.2615 (E_QG,2 = 1.69×10¹⁹ GeV), at 0.8 it is 0.2590, at 1.0 it is 0.2470 (the design's worst cases), and at 1.4 it is 0.2249. The verdict uses the measured values, not 0.23.
- **No fitting to targets.** φ is scanned, not chosen. Verdict rules are fixed and hashed before the first comparison.
- **Out of scope.** Massive case and the moving-clock fixtures (L1.5b, D5), L1.4, vector/tensor fields, unequal Wilson angles (record only, S5), the OP4 rule itself, clock fixtures, any space-dependent load. Uniform load only; a gravitational or otherwise varying load belongs to L3.

## 3. Pre-flight (stop on any failure)

| Id | Check | Stop if |
|---|---|---|
| P0 | sha256 of this design; of `space-ledger-v2.md` (record the commit); of `frozen/dirac4.py` (`f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff`, used for the S1 consistency check only, which is not an independent check; see §5); of the executing agent's own measurement code (hashed **before** any comparison) | any mismatch |
| P1 | Unitarity of `A`, `S`, `V` and `U` at 50 random k (seed 20261112) and at k = 0 `U = 1` | residual `> 1e-12` |
| P2 | The two identities of §1 (I1 and I2 of the derivation) at 200 random (k, φ), both ε | residual `> 1e-12` (dry-run 4.5e-16) |
| P3 | `mpmath` importable at 50 digits (dry-run: mpmath 1.3.0, numpy 1.26.4, Python 3.12.3); `U` built in mp from the §6.2 symbols agrees with the double-precision build at 20 random k to `1e-12` (dry-run 5.6e-16; about 1800× headroom over round-off, loosened from `1e-14` after the 9 Nov lesson that a cut set at round-off loses a run) | not importable, or residual `> 1e-12` (no silent fallback to double precision) |
| P4 | The real-space hop weights of §4 S4 reproduce the Bloch symbols `A^ε`, `A^ε†`, `X^ε` at 20 random k | residual `> 1e-12` |
| P5 | Load conditions: at s = 1 both rules equal the unloaded `U` (residual `≤ 1e-30` at 50 digits at 5 random k); at the four ON conditions `U_A` and `U_B` are unitary (`≤ 1e-30`) and the principal-branch logarithm of every factor has all eigenphase magnitudes `< π − 0.5` at every κ used (so no branch is crossed) | any failure |

## 4. Steps, measurement and verdict rules

Grids: φ ∈ {0.5, 0.8, 1.0, 1.2, 1.4, 1.5} (the paper's table values with the doubler gap; φ = π/2 excluded because the doublers return); 13 directions (the 3 `[100]`, 6 `[110]`, 4 `[111]` classes: (1,0,0), (0,1,0), (0,0,1), (1,1,0), (1,−1,0), (1,0,1), (1,0,−1), (0,1,1), (0,1,−1), (1,1,1), (1,1,−1), (1,−1,1), (−1,1,1)), each also with n̂ → −n̂ (26 signed directions, including [11−1] and its reverse). **Every step below is evaluated under each of the four ON conditions A.5, A2, B.5, B2**; the unloaded s = 1 case is evaluated as a labelled diagnostic (OFF) and is excluded from all gates.

### S1. The symmetry, numerically (gate G1)

For each ON condition, φ, signed direction and `κ ∈ {0.05, 0.1, 0.2, 0.4}` (so that |θ| stays well below π): the four eigenphases of `U(κ n̂)` against those of `U(−κ n̂)`, sorted; and `θ_j + θ_{5−j}` for each. **G1 passes** iff both are `≤ 1e-12` everywhere (dry-run sample over the full grid: 6.7e-16 and 6.1e-16). As a labelled consistency check (not independent, §5; gates nothing) the same is evaluated through the frozen `U_cycle` (expected exact agreement of arithmetic, as in L1.3b).

### S2. Expansion at 50 digits (gate G2 and checks)

For each φ and signed direction, with `κ_j = j/500`, `j = 1…12`: ω̄(κ_j) = (|θ|₍₂₎ + |θ|₍₄₎)/8, where |θ|₍₁₎ ≤ … ≤ |θ|₍₄₎ are the four sorted eigenphase magnitudes (they come in equal pairs, so this is the mean of the two lowest positive per-layer frequencies), `ω̄/κ` interpolated exactly by a polynomial in κ with all 12 powers: `ω̄/κ = a₀ + a₁κ + a₂κ² + a₃κ³ + …`. `ξ₁' = a₁/a₀`, `ξ₂' = a₂/a₀`.

- **G2 passes** iff `|ξ₁'| ≤ 1e-12` and `|a₃|/a₀ ≤ 1e-12` for every ON condition, φ and signed direction. (Dry-run E: 4.5e-22 and 1.1e-16 over all four conditions. These are the derivation's exact-zero claims [P], extended to uniform load in the derivation §5; 1e-12 sits far above the fit's truncation error and far below any physical size.)
- **Check T1 [F]:** `|a₀ − s·½√(1 + 3 sin²φ)| ≤ 1e-12` (dry-run 2.4e-25; s = 1 for the unloaded diagnostic).
- **Check T2 [F], pre-registered prediction, rule A and the unloaded diagnostic:** `|ξ₂'(n̂, φ) − [−(1 − q)/3 − (3/8) sin²φ cos²φ/(1 + 3 sin²φ)]| ≤ 1e-12` at the 13 directions for each φ, and the same value at −n̂ (dry-run 1.5e-17: rule A multiplies ω by g and leaves ξ₂' unchanged).
- **Check T3 [F], pre-registered prediction, rule A and the unloaded diagnostic:** `ξ₂'(100) − ξ₂'(111) = 2/9` to `1e-12` for every φ.
- **Rule B is not predicted.** ξ₂' under rule B differs from the unloaded closed form by up to 0.0058 (ℓ₀ = 0.5) and 0.0116 (ℓ₀ = 2); its values are recorded and compared with the pilot values in `dryrun/expected_pilot_load.json` as a replication (tolerance `1e-10`), not as a gate.
- T1 to T3 and the rule B replication are recorded as passed or failed. A failure does not change the verdict (the physical gate is G3), but a failure of T2 or T3 means the closed form may not be quoted anywhere.

### S3. The physical gate (gate G3)

With the measured ξ₁', ξ₂' per ON condition, φ and direction, with the energy-convention factor (D3) at 1: `E_QG,1 = E_P/(2|ξ₁'|)` and `E_QG,2 = E_P/√(2|ξ₂'|)` (the paper's Test 3 convention). **G3 passes** iff, for every ON condition, φ and signed direction, `|ξ₁'| ≤ 0.05` (that is E_QG,1 ≥ 10 E_P, the LHAASO linear limit, stricter than Fermi's 7.6 and the conservative 1.2) and `E_QG,2 ≥ 6.9×10¹¹ GeV`. If `ξ₁'` is zero to the fit noise, E_QG,1 is reported as a lower bound `E_P/(2 × noise)`, not as infinity. The worst E_QG,2 over φ and direction is reported with the conversions s = √3, 2, 4. Dry-run E: worst `|ξ₂'|` over the ON conditions 0.2615 (rule A, φ = 0.5, [111]; rule B: 0.2557 and 0.2499), E_QG,2 = 1.7×10¹⁹ GeV, a factor 2.4×10⁷ above the LHAASO limit; at φ = 1.4 and rule A `|ξ₂'| = 0.2249`. Note that load enters E_QG only through ξ: the loaded speed `s c₀` is a time-scale, not a Lorentz violation.

**Sky template.** The direction dependence is reported as the cubic-harmonic form `ξ₂'(n̂) = α(φ) + (1/3) q`, with α, and the axis-to-body-diagonal difference 2/9 (in κ units: speed difference 2/3 κ²; in (kℓ)² units 2/9). No direction-odd term is expected; the table lists `ξ₂'` and its n̂ → −n̂ partner for each direction.

### S4. Real-space whole-tick check (labelled diagnostic, OFF; not in the verdict)

An independent hop implementation, to confirm that the symbol is the evolution of a local rule and that k, direction and sign mean what the symbol says. **It runs on the unloaded symbol**, because the s-th powers of rule A and rule B are not finite-range hop operators (a fractional power of a hop operator has infinite range), so a local loaded evolution does not exist for these rules. Under plan §0.1 rule 1 it is therefore a diagnostic and gates nothing; it checks the code and conventions that S1 to S3 rely on, and its thresholds below are pass/fail for that purpose only.

- **Rule in hop form (algebraic identities from the paper's `u`, `n`):** with the 8 hops `h = (±1, ±1, ±1)`, `u^ε = (1/8) Σ_h (1 − iε h_x h_y h_z) e^{ik·h}`, `n_x^ε = (1/8) Σ_h (−i h_x − ε h_y h_z) e^{ik·h}`, `n_y^ε = (1/8) Σ_h (−i h_y + ε h_x h_z) e^{ik·h}`, `n_z^ε = (1/8) Σ_h (−i h_z − ε h_x h_y) e^{ik·h}`. Then `(Oψ)(x) = Σ_h M_h ψ(x + h)` with `M_h` the 4×4 matrix of the same expression as the symbol (`A`, `A†`, or `X`). Layers applied in order `S⁺, V⁺, S⁻, V⁻`; `V = (cos φ − i sin φ X)(cos φ + i sin φ T)` applied as two operations.
- **Cell.** Periodic cell of side 104 coordinates (coordinate = a/2) on the BCC sites (all coordinates of equal parity); zero on other sites.
- **Packet.** Built in k-space: amplitude `exp(−|k − k₀|²σ²)` (σ = 9 coordinates in |ψ|²), `|k₀| = 0.6`, with Wilson angle **φ = 1.2**, on the two lowest positive-frequency eigenvectors of `U(k)` at each grid k (the spinor at k₀ projected onto that two-dimensional space), phase `e^{−ik·x₀}` with x₀ the cell centre, inverse FFT, masked to the BCC sites, normalised. 3 cycles.
- **Measurement.** Centroid velocity in coordinates per cycle, `(c₃ − c₀)/3`, with periodic minimum-image coordinates. Prediction: the weight-averaged band-resolved `∇_k(4ω_j)` over the packet's own k-grid weights (the same discrete sum as the state). Directions: (1,0,0), (−1,0,0), (1,1,1), (−1,−1,−1), (1,−1,1), (−1,1,−1), (2,1,1), (3,1,1).
- **Separate pilot and gate grids (plan §0.6, decision D6).** The dry-run D pilot that set the thresholds below used a 96-cell, φ = 1.4 and the directions (1,0,0), (−1,0,0), (1,1,1), (−1,−1,−1), (1,1,−1), (−1,−1,1), (1,1,0), (1,2,3). The gate grid above differs in cell size, in φ and in four of the eight directions (the ± pairs needed for (c) are kept); σ and |k₀| are shared. The gate grid has not been run. If the thresholds turn out too tight on it, S4 fails as a diagnostic and nothing in the verdict changes; they are not adjusted afterwards.
- **S4 is reported pass or fail on** (diagnostic): (a) the plane-wave cycle in the hop form equals the symbol at one random k on a 16-cell to `1e-12` (dry-run 2.4e-15); (b) `| ‖ψ‖² − 1 | ≤ 1e-10` after 3 cycles (dry-run 1.3e-15); (c) `|v(n̂) + v(−n̂)|_∞ ≤ 3e-3` for the pairs ±[100] and ±[111] (dry-run 3.6e-4 and 1.8e-5); (d) `|v_measured − v_predicted|_∞ ≤ 5e-3` in all eight directions (dry-run worst 9.7e-4). Thresholds (c) and (d) are about 8 to 5 times the dry-run's worst value, set from that pilot and frozen when this file is hashed (plan §0.6, pilot-then-freeze); the pilot never counts toward a gate.
- **What (c) means.** A direction-odd linear coefficient ξ₁' would show as `v(n̂) + v(−n̂) ≈ 9 ξ₁'` at these parameters, so (c) is an independent bound `|ξ₁'| ≲ 3e-4` from the unloaded evolution. By rule 1 that bound does not count toward a gate. Because loaded versions of `U` are matrix functions of the same layers, a pass of S4 is evidence that the symbol is right; it does not replace S1 to S3.

### S5. Records (not in the verdict)

- **R5a.** The eigenphase-set difference between U(k) and U(−k) at 20 random k (seed 20261112) for `(φ⁺, φ⁻) = (0.5, 1.3), (0.9, 1.0), (1.4, 1.4)`: the identity needs equal angles (dry-run 0.66, 0.086, 1.3e-15).
- **R5b.** The branch splitting (second minus lowest positive frequency) at κ = 0.006 and 0.012 on [100], [110], [111], (1,2,3), and the local exponent between them (dry-run: zero on [100] and [110], exponent 5.0 on the others).
- **R5c.** Paper comparisons, listed with values and without a verdict: the max `|ξ₂'|` over φ and direction against the paper's 0.23 (Test 3); E_QG,2 against 1.8×10¹⁹ GeV; the axis-to-body-diagonal difference against the "(E/E_P)²/18" of the paper (line 1253), in κ², (kℓ)² and (E/E_P)² units.

### Verdict for L1.5 on `dirac4`

- **PASS** iff P0 to P5, G1, G2 and G3 all hold, under every one of the four ON conditions.
- **FAIL / OPEN** if any of them fails. A failed G2 (a nonzero linear coefficient above 1e-12 that the symmetry forbids) would mean a code error or a missing hypothesis in the derivation and must be diagnosed before anything is concluded; it is not a physical finding by itself.
- T1 to T3, the rule B replication, S4, S5 and the frozen-module consistency check are recorded evidence and do not decide pass or fail. An S4 failure means the code or conventions behind S1 to S3 must be diagnosed before the verdict is read.
- **What a PASS does.** It says: for the massless `dirac4` excitation at equal Wilson angles on one BCC orbit, with congestion ON in the two declared uniform-load implementations, the linear dispersion coefficient is zero to 1e-12 in every tested direction, the quadratic coefficient is the stated cubic-harmonic form with `|ξ₂'| ≤ 0.2615`, and E_QG,2 exceeds the LHAASO limit by 2.4×10⁷. Whether that closes L1.5 for the plan item (which says "vector and tensor fields") is Edmond's decision, taken after the run in a closure record (D2, D4).
- **Stop rule.** Stop on any failed pre-flight or failed gated step. Unrun steps are recorded "not run" and are not retried within this run.

## 5. Independence of the implementation, and who runs it

**Executing agent:** `spacetime`, the Grok bot on `bigbang`, as for L1.3 and L1.3b. The reviewing agent (Cursor) runs no gate step.

The executing agent writes its own measurement code from the §6.2 text of the paper and §4 above, imports none of `dryrun/`, and hashes its code before any comparison. The folder `dryrun/` is published as the reviewing agent's reference and as the origin of the expected values; it is **not** measurement code. The frozen `dirac4.py` is **not an independent check**: in dry-run A it agrees with the reviewing agent's analytic construction exactly (0.0), so the two share a construction. S1's comparison with it is a labelled consistency check and gates nothing. The independence this design has is the executing agent's own code from the paper's text, and S4's hop-form evolution, which is a different construction from the Bloch symbols.

## 6. Resource estimate and cap proposal (plan §0.2)

Dry-run timings: A to C about 15 s together; B (50 digits, 6 φ × 26 signed directions × 12 κ, one 4×4 mp eigensolve each, 6.5 ms) about 11 s; E (the four ON conditions, same grid, matrix powers in mp) about 2 min; D (8 directions, N = 96, about 8 s each) about 1 min. The real-space arrays are 4 × 104³ complex (72 MB each, a few live copies; the 96-cell pilot used 57 MB).

| Cap | Proposed ceiling |
|---|---|
| Memory | 2 GiB |
| CPU | 1 thread (pinned: `OMP_NUM_THREADS=1`), no GPU |
| Wall time | 20 min total, 10 min per step |
| Output | 64 MiB under `runs/<date>_<id>/` |
| Attempts | **one per step.** A corrected re-run is a new run with its own id and approval |
| Stop rules | stop on any failed pre-flight; stop and report on any failed step; do not edit the measurement code after seeing a comparison; do not silently retry; steps not run are recorded as "not run" |

As with L1.2 and L1.3, the caps are soft ceilings with these hard rules.

## 7. What `result.json` must contain

Code version (design hash, measurement-code hash, frozen-module hash, paper commit and sha256, Python/numpy/mpmath versions), seed (20261112), grid, boundary condition (periodic, one orbit; S4 on a periodic 104-cell), units (ω per layer; κ per a/2; E/E_P = sκ with s = 1; velocities in coordinates per cycle, coordinate = a/2), load rule ("congestion ON: uniform load, rule A or B, s = 0.8165 or 0.5774", per condition; the unloaded diagnostic labelled OFF), caps and resource use per step, the full tables of `a₀, ξ₁', ξ₂'` per φ and signed direction, the G1 to G3 residuals against their thresholds and the S4 diagnostic values, T1 to T3, S5, and the verdict. Any record-keeping read (a lookup of a cited value) must be exercised on the actual input file in pre-flight (plan §0.6).

## 8. Decisions for Edmond

- **D1: load rule. DECIDED by Edmond (9:47 PM): "D1, L1.5 congestion is on."** L1.5 keeps congestion ON; no B3 carve-out. Recorded in `L1_5_run_design_20261112_DECISIONS.txt`.
- **D1b: which loaded rule (new, follows from D1).** The paper gives no load term for `dirac4`. Proposed: both rules of §2, A (paper load-first, uniform clock potential, `U^g`) and B (OP4-style, every rotation angle scaled by s), each at ℓ₀ = 0.5 and 2.0, all four required to pass. What the dry-run found (dry-run E, 50 digits): the symmetry argument extends to uniform load, so ξ₁' stays zero (≤ 4.5e-22) under both rules; rule A rescales ω by g and leaves ξ₂' unchanged; rule B changes ξ₂' by up to 0.012 and leaves the maximum |ξ₂'| at 0.2557 and 0.2499 (below the unloaded 0.2615). Say whether you want only one of the rules, other load levels, or a different loaded `dirac4` altogether (for example the loaded form of the paper's 1D zigzag weights `f = e^{−U}` applied to the Wilson layers). The loaded forms used here are not finite-range hop operators, which is why S4 stays on the unloaded symbol (§4).
- **D2: what "photon-like" means. CONFIRMED (10:14 PM), in part.** Confirmed: the massless `dirac4` excitation as the stand-in, as in paper §6.4 Test 3 (line 704); the paper's own caveat (line 708) says "Neither involves photons as vector fields". A PASS speaks for the massless Dirac proxy only. **Unconfirmed** (my additions, not Edmond's words): (a) that the "vector and tensor fields" part of the plan item is not carried to a separate open item; (b) that L1.5 may be closed on the stand-in. Both are open (D2b, and D4 and D5 below).
- **D2b (new).** Does the "vector and tensor fields" wording of plan v3.4 §3 L1.5 stay as an open sub-item (no rule defines such a field), or is it retired by the proxy? Proposed: record it as not testable on this lattice model, without retiring it, until you say so.
- **D3: energy convention. ACCEPTED (10:14 PM): s = 1.** See §2; the other conventions (√3, 2) are reported. Citation fixed: Test 3 is §6.4 (line 704), not §7.8.
- **D4: closure rule.** As for L1.3 and plan §0.6: a PASS lets Edmond record the item closed in a closure record, after the run. What it closes depends on D5: **L1.5a (the light-speed part) only**, with L1.5 as a whole open until L1.5b is designed, approved and run, unless you decide otherwise. Confirm.
- **D5: clock fixtures. OPEN, conflict with the old notes.** r1 and r2 proposed leaving the 25 clock fixtures out as OP4-only. That conflicts with plan v3.4 §2 (B2), which lists the held L1.5 tick-budget design among the results to be redone on `dirac4`, and with the paper (line 704), which counts moving-clock tests at v = 0 to 0.8c along five directions as part of Test 3. The fixtures need a massive walker, the same gap as the massive case out of scope here. This design therefore covers L1.5a only. Choose: (a) L1.5b gets its own `dirac4` design (massive case, moving clocks), L1.5 stays open until it closes, and this design runs first; (b) L1.5b is designed first and both run together; (c) the fixtures are retired for stated reasons (this would reverse B2 for this item). Proposed: (a).
- **D6: tolerances.** Theory-based thresholds (`1e-12`) and pilot-based thresholds (S4 (c), (d): `3e-3`, `5e-3`). Two changes after review: (1) S4's gate grid is now separate from the pilot grid (plan §0.6; §4 S4), (2) P1 to P4 thresholds are now `1e-12` and P3 is no longer `1e-14` (18× over round-off was too tight). They freeze when this file is hashed. Accept or change.
- **D7: the disclosed order of events.** The derivation, the closed forms and the pilot numbers precede this design (§1); the ξ₂' closed form was found from the pilot numbers, not derived; G2's and T2's expected values come from dry-runs on the same φ and direction grid as the gate (their thresholds are theory-based, not pilot-based). Two gaps closed: the design names the executing agent (§5), and the S1 comparison with the frozen module is labelled a consistency check, not an independent one. Accept a design written under that disclosure?
- **D8: paper edits.** This design authorises none. If the run passes, candidate edits would be offered only after closure: (i) §6.4 Test 3 gains the mechanism (the identities, the equal-angle condition); (ii) the `(E/E_P)²/18` wording for the Dirac rule (paper line 1253, §7.8) is corrected or tied to its convention: the scalar rule's value is 1/18 in (kℓ)², `dirac4`'s axis-to-diagonal gap is (2/3)κ² = (2/9)(kℓ)², which waits for the ℓ_P item and holds only if T2 and T3 pass; (iii) the ξ₂' closed form, only if T2 and T3 pass; (iv) line 704's "|ξ₂| ≤ 0.23" gains its φ range (it holds for φ ≥ 1.275; 0.2615 at φ = 0.5).

## 9. Approval and freezing

1. A one-line approval naming the sha256 of this file (see `SHA256SUMS` beside it) is the approval required by plan §0.2 for steps S1 to S5, under §6. Decisions D1b, D2b, D4 to D8 take their proposed values unless Edmond says otherwise (D1, D2 and D3 are answered); they are recorded in a sidecar outside the hashed folder.
2. The executing agent copies this file unchanged into the run directory, hashes it, and writes `expected.json` (the closed forms of §4 and the paper's table values) before any computation.
3. Steps: **S0** pre-flight P0 to P5 and the resource timing; **S1**; **S2**; **S3**; **S4**; **S5** and `result.json`.
4. Nothing is authorised beyond S0 to S5. No paper, plan, repo or archived-record edit is authorised by this design.

## 10. Dry-run (unscored; nothing in it counts toward a gate)

`dryrun/` holds six scripts and their outputs, and the shared library; `L1_5_DERIVATION.md` §3 to §6 quote them.

| Script | What it shows | Headline numbers |
|---|---|---|
| `dryrun_A_identities.py` | identities I1 and I2, spectra, the unequal-angle contrast, frozen module against the analytic construction | 4.5e-16 and 1.3e-15; frozen vs analytic exactly 0.0; unequal angles 0.66 and 0.086 |
| `dryrun_B_mp_expansion.py` | 50-digit expansion, 6 φ × 26 signed directions | `|ξ₁'|` ≤ 4.5e-22; `|a₀ − c₀|` ≤ 2.9e-25; ξ₂' closed form to 3e-19; axis−body = 2/9; splitting exponent 5.0 |
| `dryrun_C_h2_block.py` | effective-Hamiltonian block at O(κ²) | max 2.9e-15 |
| `dryrun_E_load.py` | congestion ON: rules A and B at ℓ₀ = 0.5 and 2.0, 50 digits | `|ξ₁'|` ≤ 4.5e-22 in all four; `a₀ = s c₀` to 2.4e-25; rule A ξ₂' unchanged (1.5e-17); rule B ξ₂' shifts by ≤ 0.0116, max `|ξ₂'|` 0.2557 / 0.2499 |
| `dryrun_F_test3_convention.py` | E/E_P = κ against the paper's Test 3 (single-handed step) and the φ range of "|ξ₂| ≤ 0.23" | ξ₁[111] = 0.192450 = 1/(3√3) at φ = 0.5, 1.0, 1.4; E_QG,1 = 2.598 E_P; |ξ₂'| ≤ 0.23 for φ ≥ 1.275 |
| `dryrun_D_realspace.py` | hop-form whole-tick, packet velocities | plane wave 2.4e-15; norm 1.3e-15; odd test 3.6e-4, 1.8e-5; vs prediction ≤ 9.7e-4 |

`expected_pilot.json` stores the pilot unloaded `c₀`, `α(φ)` and `ξ₂'` values at 20 digits; `expected_pilot_load.json` the ξ₂' values of the four ON conditions. Environment: Python 3.12.3, numpy 1.26.4, mpmath 1.3.0, one thread.
