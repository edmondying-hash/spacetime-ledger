# L1.3b design: corrected two-angle test and the unrun checks of L1.3 (one BCC orbit, `dirac4`)

Quantized Space-Ledger. Draft of 12 November 2026 (America/New_York), for Edmond Ying's approval. **This document is a design. It runs nothing, and it edits no paper, plan, Sheet or archived record.** Nothing in it is approved until Edmond approves its sha256 (§9).

## 0. Why L1.3b exists

Run `9ccf4855` (results PR #8, branch `grok/l1-3-run-20261112`, commit `f4e45728`, SHA256SUMS `17f5e19944dd36a7b257854951e5a4c594515d71dedd8e4a0d43da6f139e6157`) ended **FAIL / OPEN** and stays in the record unchanged:

- **R1 PASSED**: `c₀(φ) = ½√(1+3 sin²φ)` against the exact symbol at 16 φ and 13 directions, to 4.3e-14.
- **R2 FAILED** for two design faults, both mine: (a) the printed two-angle formula had a ½ prefactor where ¼ is correct; (b) the measurement protocol extrapolated in κ² and so assumed no term odd in κ, which is false for φ₂ ≠ φ₄. The run fixed reading (a) before computing and recorded it as DEV-1.
- **S3 was not run** (stop rule), so N1 to N5 are unscored.

Edmond's decision (2026-11-12, 7:55 PM America/New_York): R2 is recorded as open as written, and a corrected L1.3b is approved **to be designed**. This file is that design. A run needs approval of this file's hash (§9).

## 1. Corrected derivation (pencil algebra, checked at its special cases)

Setting, as in the L1.3 design §1: m = 0 (so ν_S = 1), first order in k, `A^ε ≈ 1 − i k·σ`, `S^± ≈ 1 − iτ_z(k·σ)`, and for a Wilson layer with angle φ, `V ≈ 1 − i sin φ (cos φ τ_y + sin φ τ_z)(k·σ)`.

With angle φ₂ on `V⁺` (step 2) and φ₄ on `V⁻` (step 4), one cycle `U = V⁻ S⁻ V⁺ S⁺` is, to first order,
`U ≈ 1 − i (k·σ) [ (2 + sin²φ₂ + sin²φ₄) τ_z + (sin φ₂ cos φ₂ + sin φ₄ cos φ₄) τ_y ]`.
The bracket has eigenvalues `± √((2 + sin²φ₂ + sin²φ₄)² + (sin φ₂ cos φ₂ + sin φ₄ cos φ₄)²)`. With `U = e^{−4iω}` per cycle (ω per layer), so ω = |k| × that root / 4:

**c₀(φ₂, φ₄) = ¼ √( (2 + sin²φ₂ + sin²φ₄)² + (sin φ₂ cos φ₂ + sin φ₄ cos φ₄)² )**

Special cases evaluated before approval (by arithmetic and by the dry-run in §10): at φ₂ = φ₄ = φ it equals `½√(1+3 sin²φ)` (the case run `9ccf4855` confirmed); `c₀(0,0) = 0.5`; `c₀(π/2, π/2) = 1`; it is symmetric under φ₂ ↔ φ₄ (difference 0.0 at (0.5, 1.3)). The printed ½ version would give 2c₀ at φ₂ = φ₄, which contradicts the line above it; that is how the error shows.

**What first order does not give.** The formula is the |k| → 0 speed. Second-order terms in `n^ε` (`n_x ≈ k_x + ε k_y k_z`) enter the cycle with ε alternating, and with φ₂ ≠ φ₄ they do not cancel, so v(κ) = c₀ + b κ + O(κ²) with b direction dependent. At φ₂ = φ₄ the first-order cancellation holds in the exact symbol (§10). **No expression for b is derived here.** b is measured and recorded (R2c), not predicted.

## 2. Declared conditions (plan §0.1; unchanged from L1.3)

- **Rule and lattice.** `dirac4`, canonical, one BCC orbit, integer hops, `k` in radians per `a/2`, 2π-periodic. Free spectrum, **m = 0**.
- **Load rule.** None, the §6.2 vacuum symbol (plan §0.1 exception for L1.1–L1.3, Edmond B3).
- **Whole ticks.** The cycle eigenvalue only; no sub-tick interpolation.
- **No fitting to targets.** φ, φ₂, φ₄ are scanned, not chosen. Verdict rules are fixed and hashed before the first comparison.
- **Out of scope.** Massive case, L1.4, L1.5, the doubler gap, the chain. A closed form for b.

## 3. Pre-flight (stop on any failure)

| Id | Check | Stop if |
|---|---|---|
| P0 | Hash of this design; of `space-ledger-v2.md` (record the commit); of the U-builder (lines 51 to 96 of `harness/l13_primary.py`, whole-file sha256 `5e606a0631b0124992d65f22dd15ffb90e9ad388706c73a9b7739cb388870d8e`, copied from PR #8 and used **unchanged**) and of any frozen module imported | any mismatch |
| P1 to P4 | As in the L1.3 design §3: unitarity of `A`, `S`, `V` at 50 random k; `(u^ε)² + |n^ε|² = 1` and `(X^ε)² = 1`; `V = 1` and `U = 1` at k = 0; periodicity `U_k = U_{k+π(1,1,0)}` at φ = 1.4 | the L1.3 residual limits |
| P5 (new) | The closed forms in §1 evaluated in code at the special cases: `c₀(φ,φ) = ½√(1+3 sin²φ)` for 7 φ; `c₀(0,0) = 0.5`; `c₀(π/2,π/2) = 1`; `c₀(φ₂,φ₄) = c₀(φ₄,φ₂)` for 5 pairs | any difference `> 1e-13` |

## 4. Steps, measurement and verdict rules

**Measurement protocol (changed from L1.3).** For each angle pair and each of the **13 directions** (3 `[100]`, 6 `[110]`, 4 `[111]`, as in L1.2): `|k| = κ` for `κ ∈ {0.001, 0.002, 0.004, 0.008, 0.016}`; `v(κ) = ω_min(κ)/κ`, with ω_min the smallest `|ω|` over the four eigenvalues of `U_k` and ω = arg λ / (−4). **v₀ is the Neville extrapolation to κ = 0 in κ (all powers), through all five κ (degree 4).** Degree 3 (four smallest κ) is recorded as a diagnostic. The linear coefficient b and quadratic coefficient c of the degree-4 interpolating polynomial are recorded per direction.

### R1′. Consistency of R1 under the new protocol (φ = φ₂ = φ₄)

- Grid: `{0.1, 0.2, …, 1.5}`, the paper's table values `{0.5, 0.8, 1.0, 1.2, 1.4, 1.5}`, and π/2 (16 values, as in L1.3).
- **Pass:** `|v₀ − ½√(1+3 sin²φ)| ≤ 1e-6` for every φ and direction, and the spread of v₀ over the 13 directions `≤ 1e-6`; v₀ rounds to the printed value at the tabulated φ. The R1 result of `9ccf4855` stands as recorded; R1′ is a consistency check that the protocol change does not disturb it.

### R2b. Layer weights φ₂ ≠ φ₄ (the corrected R2)

- 7 × 7 grid of `(φ₂, φ₄) ∈ {0.2, 0.5, 0.8, 1.0, 1.2, 1.4, π/2}²` (49 pairs, the 7 diagonal pairs included).
- **Pass:** `|v₀ − c₀(φ₂, φ₄)| ≤ 1e-6` against the **¼ formula of §1** for every pair and direction, and the spread of v₀ over the 13 directions `≤ 1e-6` for every pair.

### R2c. Linear and quadratic coefficients (record only, not in the verdict)

b and c per pair and direction, as a table. Two observations are listed in advance **as replications, not predictions**, because they were seen in an unscored diagnostic before this design was written (§10): (Q1) `|b| ≤ 1e-6` on the three `[100]` directions for every pair; (Q2) `|b| ≤ 1e-6` at every diagonal pair φ₂ = φ₄. They are reported pass or fail but do not decide the verdict. No symmetry of b under φ₂ ↔ φ₄ or under direction sign is assumed or claimed; the diagnostic shows b is neither symmetric nor antisymmetric under the exchange.

### R3. Does any local normalisation select φ? (the L1.3 question; first run)

Unchanged from the L1.3 design §4:

| Id | Candidate normalisation | Check | Pre-declared outcome that supports "φ is free" |
|---|---|---|---|
| N1 | Unitarity / SU(2) | Each layer exactly unitary for φ, φ₂, φ₄ over a dense grid on `[0, π]`; `U` unitary at 200 random k for each | unitary to `1e-12` at every tested φ, so unitarity selects nothing |
| N2 | Stationarity | `dc₀/dφ` at φ = 1.4, by finite differences on the R1′ values, against the closed form (0.127) | nonzero, so 1.4 is not an extremum of c₀ |
| N3 | Range | `v₀(φ)` strictly monotone on `[0, π/2]` and spanning `[0.5, 1]`, extended to `φ ∈ {0.0, 0.05}` | every target value in `[0.5, 1]` is hit by exactly one φ |
| N4 | Doubler return | The V5 v2 census value at φ = π/2 (`results.json` `ca6793ea…`) and `c₀(π/2) = 1` (cited, not re-run) | speed 1 needs φ = π/2, where the doublers return: a trade-off, not a selection of 1.4 |
| N5 | A search of the record | Search `space-ledger-v2.md` §6.2, the plan and the L1.1 notes for any statement that fixes φ = 1.4 other than "default" | each hit recorded verbatim; no hit that derives φ from the rule |

N3 strict monotonicity requires a gap `> 1e-6` between consecutive φ in the grid, over all directions; N2's "nonzero" threshold is `1e-4` (as set in the pre-run `PROTOCOL_NOTES.md` of `9ccf4855`).

### Verdict for L1.3b

- **PASS** iff R1′ passes, R2b passes, N1 holds, and N2 and N3 hold as pre-declared.
- **FAIL / OPEN** if R1′ or R2b fails, if N1 finds a φ where a layer is not unitary, or if N5 finds a derivation of φ = 1.4 from the rule.
- R2c, N4, N5 (absent a derivation) and the cross-check below are recorded evidence and do not by themselves decide pass or fail.
- **What a PASS does to L1.3.** The R2 of `9ccf4855` remains FAIL as written, in the record, unaltered. If L1.3b passes, Edmond may record L1.3 closed on L1.3b (R1 of `9ccf4855` and R1′, R2b and R3 of L1.3b) in a closure record, naming the original R2 failure and its two design causes. That is his decision, taken after the run.

## 5. Independence of the implementation

The U-builder is the one used in `9ccf4855` (hash in P0), written from the §6.2 text of the paper and importing no frozen module. Only the measurement code is new, and its source is hashed before any comparison and published. As a labelled cross-check, after the primary results are written, the same pair grid at 13 directions is also evaluated through the frozen `U_cycle` (`dirac4.py` sha256 `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff`); the maximum difference between the two implementations' `U_k` is recorded (expected at rounding level). In `9ccf4855` this cross-check was never reached.

## 6. Resource estimate and cap proposal (plan §0.2)

About 49 pairs + 16 φ + extension, times 13 directions times 5 κ, each a 4×4 eigenproblem: of the order of 10⁴ eigensolves. `9ccf4855` measured 5e-5 s per single eigensolve, so seconds. These are estimates; S0 restates them.

| Cap | Proposed ceiling |
|---|---|
| Memory | 2 GiB |
| CPU | 1 thread (pinned), no GPU |
| Wall time | 30 min total, 10 min per step |
| Output | 64 MiB under `runs/<date>_<id>/` |
| Attempts | **one per step.** A corrected re-run is a new run with its own id and approval |
| Stop rules | stop on any failed pre-flight (P0 to P5); stop and report on any failed step; do not edit the measurement code after seeing a comparison; do not silently retry. Steps not run are recorded as "not run" |

As with L1.2 and L1.3, the caps are soft ceilings with these hard rules. Raising a ceiling is a note in `result.json` and a ping to Edmond.

## 7. What `result.json` must contain

Code version (design hash, U-builder and measurement-code hashes, frozen-module hash, paper commit and sha256), seed (none random in R1′/R2b; the 50 and 200 random k use `numpy.random.default_rng(20261112)`, per-task `+ index`), grid, boundary condition (periodic, one orbit; no real-space run), units (ω per layer, speeds in hop-rate units), load rule ("none, §6.2 vacuum symbol"), caps and resources per step, every R1′ and R2b value (v₀, closed form, difference, per direction, degree-3 and degree-4), the R2c table, the N1 to N5 records, the cross-check, raw logs, the sha256 of the frozen design, and a pointer to `9ccf4855`. The table must be regenerable from `result.json`.

## 8. Decisions for Edmond

- **D1: who runs it.** Proposed: the Grok bot on `bigbang`, as with L1.2 and `9ccf4855`.
- **D2: tolerance.** `1e-6` absolute on v₀, unchanged from the L1.3 design. Accept or change now; it freezes when this file is hashed.
- **D3: the disclosed order of events.** The κ set, the degree-4 extrapolation and the R2c replications were chosen after an unscored diagnostic (§10) showed the odd term. The closed form was **not** adjusted to data: the ¼ comes from the algebra at φ₂ = φ₄. Say whether you accept a design written under that disclosure.
- **D4: closure rule.** As in §4: a PASS lets you record L1.3 closed on L1.3b, with the R2 failure kept. Confirm, or say what you want instead.
- **D5: the closed forms and the paper.** If L1.3b passes, `c₀(φ) = ½√(1+3 sin²φ)` (and the two-angle form) could go into the paper §6.2. **This design does not authorise any paper edit.**

## 9. Approval and freezing

1. A one-line approval naming the sha256 of this file (see `SHA256SUMS` beside it) is the approval required by plan §0.2 for steps S0 to S3, under §6.
2. The executing agent copies this file unchanged into the run directory, hashes it, and writes `expected.json` (the closed forms and the paper's table values) before any computation.
3. Steps: **S0** pre-flight P0 to P5 and one timed eigensolve; **S1** R1′; **S2** R2b and R2c; **S3** R3 (N1 to N3), the N4 and N5 records, the cross-check, and `result.json`.
4. Nothing is authorised beyond S0 to S3. No paper, plan, repo or archived-record edit is authorised by this design.
5. After the run, Edmond is pinged with the verdict table; results go on a separate branch and PR; a closure record follows only after Edmond's decision.

## 10. Design dry-run (unscored, written before this design was hashed)

`design_dryrun_unscored.py` and its output `design_dryrun_unscored_output.txt` sit beside this file and are hashed in `SHA256SUMS`. They import the U-builder of `9ccf4855` (PR #8) read-only and apply the §4 protocol, on the Cursor VM, not on `bigbang`. Findings: worst `|v₀ − c₀|` over 49 pairs × 13 directions is 3.9e-13; R1′ worst 2.3e-13; `|b|` on `[100]` and at φ₂ = φ₄ is at most 2.1e-10; v₀ is symmetric under φ₂ ↔ φ₄ to 4.2e-13, while b is neither symmetric nor antisymmetric. A first diagnostic (a different κ set, 5e-4 to 8e-3, least-squares in κ) is recorded in the store note `l1-3-r2-diagnostic-unscored.md`. **Neither is a result of this design and neither is an input to its verdict.** Their purpose is to ensure the verdict rules can pass for a correct reason and cannot fail for a design reason again; the pass margin (1e-13 against 1e-6) is large enough that the tolerance is not tuned to it.
