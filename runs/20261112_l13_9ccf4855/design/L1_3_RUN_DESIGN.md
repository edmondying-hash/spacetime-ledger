# L1.3 design: is ν = cτ/a fixed by the rule or by φ? (one BCC orbit, `dirac4`)

Quantized Space-Ledger. Draft of 12 November 2026 (America/New_York), for Edmond Ying's approval. **This document is a design with a hand derivation and a proposed run. It runs nothing, and it edits no paper, plan, Sheet or archived record.** Nothing in it is approved until Edmond approves it (§9).

## 0. What L1.3 asks, and a naming trap

Plan `layered_plan_v3.3.md` §3, L1.3:

> The paper leaves open whether `ν = cτ/a = 0.989` is fixed by the rule or by φ. **Test:** scan φ and the layer weights; determine whether any local normalisation forces `ν = 0.98911`. Pass: a derivation or a proof that φ is a genuine free parameter. This matters because `ν` sets the tick and therefore every quoted rate. (A scan of φ to *understand* the rule is allowed; choosing φ to hit a number is not.)

**Naming trap.** The symbol ν means two different things in the paper.
- In the hop layers, `S^ε_k` has `ν² + m² = 1` (§6.2). **At m = 0 this ν is exactly 1.** It is a mass-mixing weight, not the speed.
- In the definition of c (paper line 381 and §6.1), `c = ν a/τ`, with `ν = 0.989` at φ = 1.4. This is the **low-energy light speed in units of the hop rate**, written c₀ in the §6.2 low-energy limit.

This design calls the second one **c₀(φ)** throughout, and it is what L1.3 is about. The first is called ν_S and is 1 at m = 0.

## 1. Hand derivation (done before any run; the run must confirm or refute it)

This is a pencil derivation from the boxed update rule in §6.2 on `main`. It is not a simulation. It is stated here so the run has a prediction to test, and so the verdict rule can be written before data.

**Setting.** m = 0, so ν_S = 1 and the hop layers are `S^ε = diag(A^ε, A^{ε†})`. Small k, first order in k. From the hop symbols, `u ≈ 1`, `n ≈ k` (the ε-dependent terms are second order), so `A^ε ≈ 1 − i k·σ`.

1. Hop layers: `S^± ≈ 1 − i τ_z (k·σ)` (the R block gets `A`, the L block gets `A†`).
2. Wilson layers: `X^ε ≈ τ_x + τ_y (k·σ)`, and `X² = 1` exactly, so `e^{−iφX} = cos φ − i sin φ X`. At k = 0, `X = τ_x`, so `V = 1`. To first order,
   `V^± ≈ 1 − i sin φ (cos φ τ_y + sin φ τ_z)(k·σ)`.
3. One cycle `U = V⁻ S⁻ V⁺ S⁺`, first order: the terms add, so
   `U ≈ 1 − 2i (k·σ) [ (1 + sin²φ) τ_z + sin φ cos φ τ_y ]`.
4. The matrix in brackets has eigenvalues `± √((1 + sin²φ)² + sin²φ cos²φ) = ± √(1 + 3 sin²φ)`. With `U = e^{−4iω}` per cycle, ω per layer, so
   **c₀(φ) = ω/|k| = ½ √(1 + 3 sin²φ)**,
   direction independent at first order (only `k·σ` appears).

**Arithmetic check against recorded numbers** (a calculator check of the formula, not a run of the rule):

| φ | ½√(1+3 sin²φ) | Table `dirac4` (paper) |
|---|---|---|
| 0.5 | 0.649913 | 0.650 |
| 0.8 | 0.797465 | 0.797 |
| 1.0 | 0.883773 | 0.884 |
| 1.2 | 0.949485 | 0.949 |
| 1.4 | 0.989107 | 0.989 |
| 1.5 | 0.998122 | 0.998 |
| π/2 | 1.000000 | 1.000 |

All seven round to the printed value. At φ = 1.4 the formula gives **0.98910736**, and `VERIFY.md` (cited in the L1.1 reason note) records a Richardson value of 0.98910736 for the same quantity, so the match is to all digits of that record. Also: `c₀(0) = 0.5`, `c₀(π/2) = 1`, `dc₀/dφ = 3 sin φ cos φ / (2√(1 + 3 sin²φ))`, which is **0.127 at φ = 1.4**, not zero, so φ = 1.4 is not a stationary point. And `c₀ = 0.98911` is reached at φ = 1.40002, which is just the default, 1.4.

**Generalisation to "layer weights".** Let the two Wilson layers have separate angles φ₂ (step 2, `V⁺`) and φ₄ (step 4, `V⁻`). The same steps give
`c₀ = ½ √( (2 + sin²φ₂ + sin²φ₄)² + (sin φ₂ cos φ₂ + sin φ₄ cos φ₄)² )`,
which reduces to the line above at φ₂ = φ₄.

**What this predicts for the question.** c₀ is a smooth, monotone function of φ on [0, π/2] that sweeps [0.5, 1]. No condition used in the derivation (SU(2) structure of A, `X² = 1`, unitarity of each layer) involves a particular φ. The only thing that pulls φ toward π/2 is the speed: `c₀ → 1` as `φ → π/2`, but the doublers return there (Table `dirac4`, gap 0 at π/2). So the rule fixes c₀ only as a function of φ, and φ is a free parameter that the paper sets to 1.4 as a gap-versus-speed choice. The tick `τ = 0.989 t_P` (paper §6.1) therefore inherits that choice. **This is a prediction. The run is there to test it.**

## 2. Declared conditions (plan §0.1)

- **Rule and lattice.** `dirac4`, canonical, one BCC orbit, integer hops, `k` in radians per `a/2`, `2π`-periodic. Free spectrum, **m = 0**. Quantity: the massless low-energy light speed c₀, in units of the hop rate, from the lowest band of the four-layer cycle `U_k = V⁻ S⁻ V⁺ S⁺` with `ω = arg λ / (−4)` per layer.
- **Load rule.** None, the §6.2 vacuum symbol, as in L1.1 and L1.2 (Edmond's D1 on L1.2). Declared in `result.json`.
- **Whole ticks.** The cycle eigenvalue only. No sub-tick interpolation.
- **No fitting to targets (rule 4).** φ is scanned, not chosen. The target 0.98911 plays no part in the scan. The verdict rules in §4 are fixed and hashed before the first comparison. `expected.json` holds the closed form and the paper's table values before any computation.
- **Out of scope.** The massive case (m > 0, where ν_S < 1 enters), L1.4 and L1.5 (higher-order and photon-like fields), the doubler gap itself (already in the V5 v2 census), and the chain.

## 3. Pre-flight (stop on any failure)

| Id | Check | Stop if |
|---|---|---|
| P0 | Hash of this design, of `space-ledger-v2.md` (record the sha256 of the commit used) and of any frozen module imported | any mismatch |
| P1 | `A^ε`, `S^ε`, `V^ε` built from the §6.2 text are each unitary at 50 random k, for φ in the scan | `‖U†U − I‖∞ > 1e-12` |
| P2 | `(u^ε)² + |n^ε|² = 1` and `(X^ε)² = 1` at 50 random k | residual `> 1e-13` |
| P3 | At k = 0, `V = 1` and `U` equals `1` at m = 0 | residual `> 1e-13` |
| P4 | Periodicity: `U_k = U_{k+π(1,1,0)}` (and permutations) at 20 random k, φ = 1.4 | `> 1e-13` |

## 4. Steps, verdict rules and expected outcomes

### R1. Closed form against the exact symbol, φ = φ₂ = φ₄

- **φ grid.** `{0.1, 0.2, …, 1.5}`, the paper's table values `{0.5, 0.8, 1.0, 1.2, 1.4, 1.5}`, and `π/2`.
- **Measurement.** For each φ, the exact `U_k` at m = 0 along each of the **13 directions** (3 `[100]`, 6 `[110]`, 4 `[111]`, as in L1.2). `|k| = κ` for `κ ∈ {0.0025, 0.005, 0.01, 0.02}`; `v(κ) = ω_min(κ)/κ` where ω_min is the smallest `|ω|` of the lowest band; Richardson in `κ²` to `κ → 0`, giving `v₀`.
- **Pass:** `|v₀ − ½√(1 + 3 sin²φ)| ≤ 1e-6` (absolute, in hop-rate units) for every φ in the grid and every direction, and the spread of `v₀` over the 13 directions `≤ 1e-6`. This is the paper's own stated direction-independence level (`10⁻⁶`).
- **Also pass-or-record:** `v₀` rounds to the printed value of Table `dirac4` at the six tabulated φ.
- **If R1 fails** at any φ or direction, the hand derivation is wrong or incomplete. That is recorded as the result, the closed form is not used for any claim, and L1.3 does not pass on R1.

### R2. Layer weights: φ₂ ≠ φ₄

- 7 × 7 grid of `(φ₂, φ₄) ∈ {0.2, 0.5, 0.8, 1.0, 1.2, 1.4, π/2}²`, same measurement, same 13 directions.
- **Pass:** `|v₀ − c₀(φ₂, φ₄)| ≤ 1e-6` against the generalised formula in §1 for every pair and direction.
- A **different kind of "layer weight"** is not scanned: ν_S, the hop weight, is exactly 1 at m = 0 and is tied to m by `ν_S² + m² = 1`, so it is not a free layer weight at m = 0. The design records this reading of "layer weights" and asks Edmond to confirm it (D2).

### R3. Does any local normalisation select φ? (the L1.3 question)

Each of these is a recorded check, with the verdict stated in advance:

| Id | Candidate normalisation | Check | Pre-declared outcome that supports "φ is free" |
|---|---|---|---|
| N1 | Unitarity / SU(2) | Each layer is exactly unitary for φ, φ₂, φ₄ over a dense grid on `[0, π]`; `U` unitary at 200 random k for each | unitary to `1e-12` at **every** tested φ, so unitarity selects nothing |
| N2 | Stationarity | `dc₀/dφ` at φ = 1.4, by finite differences on the R1 values, against the closed form (0.127) | nonzero, so 1.4 is not an extremum of c₀ |
| N3 | Range | `v₀(φ)` is strictly monotone on `[0, π/2]` and spans `[0.5, 1]` from R1, extended to `φ ∈ {0.0, 0.05}` | every target value in `[0.5, 1]` is hit by exactly one φ, so no single number is privileged |
| N4 | Doubler return | The V5 v2 census value at φ = π/2 (1.4e-17, `results.json` `ca6793ea…`) and the closed form `c₀(π/2) = 1` (cited, not re-run) | c₀ = 1 requires φ = π/2, where the doublers return, so speed 1 is not reachable inside the allowed range; this is the gap-versus-speed trade-off, not a selection of φ = 1.4 |
| N5 | A search of the record | Search `space-ledger-v2.md` §6.2, the plan and the L1.1 notes for any statement that fixes φ = 1.4 other than "default" | record each hit verbatim; no hit that derives φ from the rule |

### Verdict for L1.3

- **PASS ("φ is a genuine free parameter; ν = c₀(φ) = ½√(1+3 sin²φ)")** iff R1 passes, R2 passes, N1 holds (unitary at every tested φ), and N2, N3 hold as pre-declared. This is the plan's second pass clause (a proof that φ is free, with the derivation as the proof and the run as its check).
- **FAIL / OPEN** if R1 or R2 fails (the derivation is not confirmed), or if N1 finds a φ where a layer is not unitary, or if N5 finds a derivation of φ = 1.4 from the rule (which would change the answer).
- N4 and N5 are recorded evidence and do not by themselves decide pass or fail.

## 5. Independence of the implementation

The primary implementation is written from the §6.2 text of the paper only. It does **not** import the frozen `dirac4.py` (`f71c782e…`) or any `qca/` module, so that agreement with the recorded numbers is a check and not a repeat. Its source is hashed before any comparison and published. As a labelled cross-check after the primary results are written, the same φ grid at 13 directions is also evaluated through the frozen `U_cycle` (`f71c782e…`), and the maximum difference between the two implementations' `U_k` is recorded (expected at rounding level). A mismatch is a finding about one of the two implementations, not about the physics.

## 6. Resource estimate and cap proposal (plan §0.2)

The matrices are 4×4. The whole job is of the order of 10⁵ eigenproblems and should take seconds to minutes on one core. These are estimates from the matrix size, not measured. The first step times one eigensolve and restates the estimate.

| Cap | Proposed ceiling |
|---|---|
| Memory | 2 GiB |
| CPU | 1 thread (pinned), up to 4 worker processes, no GPU |
| Wall time | 30 min total, 10 min per step |
| Output | 64 MiB under `runs/<date>_<id>/` |
| Attempts | **one per step.** A corrected re-run is a new run with its own id and its own approval |
| Stop rules | **stop on any failed pre-flight (P0–P4)**; stop and report on any failure mid-run; do not edit the primary implementation after seeing a comparison; do not silently retry |

As with L1.2, the caps are recorded as soft ceilings with the hard rules above. Raising a ceiling is a note in `result.json` and a ping to Edmond.

## 7. What `result.json` must contain

Code version (design hash, primary-implementation hash, any frozen module hash, paper commit and sha256), seed (none are random; the 50 and 200 random k use `numpy.random.default_rng(20261112)`, per-task `+ index`), grid, boundary condition (periodic, one orbit; not used in a real-space run here), units (`ω` per layer, speeds in hop-rate units), load rule ("none, §6.2 vacuum symbol"), caps and resources used per step, every R1 and R2 value (measured `v₀`, closed form, difference, per direction), the N1 to N5 records, the cross-check result, raw logs, and the sha256 of the design as frozen. The table must be regenerable from `result.json`.

## 8. Decisions for Edmond

- **D1: who runs it.** Proposed: the Grok bot on `bigbang`, as with L1.2, implementing from §5 without importing frozen code, with the cross-check. The job is small enough that the reviewing agent could instead implement and run it on its own machine; both are fine. This design does not choose. Say which.
- **D2: "layer weights".** The design reads this as the two Wilson angles φ₂ and φ₄ varied separately (R2), with the hop weight ν_S fixed at 1 at m = 0. Confirm, or say what else the plan meant.
- **D3: tolerance.** `1e-6` absolute on `v₀`, the paper's stated direction-independence level. Accept or change now. It freezes when this file is hashed.
- **D4: massless only.** L1.3 is scoped to the massless light speed. The massive case and any higher-order term are left to L1.4 and L1.5.
- **D5: what to do with the closed form.** If L1.3 passes, the closed form `c₀(φ) = ½√(1 + 3 sin²φ)` could be added to the paper (§6.2 low-energy limit), together with the statement that φ is a free parameter. **This design does not authorise any paper edit.** That is a separate decision after the run.

## 9. Approval and freezing

1. Edmond reviews. A one-line approval naming the sha256 of this file (see `SHA256SUMS` beside it) is the approval required by plan §0.2, for steps S0–S3 below, under §6.
2. The executing agent copies this file unchanged into the run directory, hashes it, and writes `expected.json` (the closed form and the paper's table values) before any computation.
3. Steps: **S0** pre-flight and one timed eigensolve; **S1** R1; **S2** R2; **S3** R3 (N1 to N3), the N4 and N5 records, the cross-check, and `result.json`.
4. Nothing is authorised beyond S0–S3. No paper, plan, repo or archived-record edit is authorised by this design.
5. After the run, Edmond is pinged with the verdict table, and the review follows the L1.2 pattern: results on a separate branch and PR, a closure record only after Edmond's decision.
