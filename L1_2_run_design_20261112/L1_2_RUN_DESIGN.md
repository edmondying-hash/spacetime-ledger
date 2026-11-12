# L1.2 run design: chirality chain and doubler gap (Table `dw`), one BCC orbit

Quantized Space-Ledger. Draft of 12 November 2026 (America/New_York), for Edmond Ying's approval. **This document is a design and a cap proposal. It runs nothing, and it edits no paper, plan, Sheet or archived record.** Nothing in it is approved until Edmond approves it (§9).

## 0. Scope and what this design could not see

L1.2 in the live plan (`layered_plan_v3_3_r2_20261111/layered_plan_v3.3.md`, §3) reads:

> Reproduce Table `dw`: residual mass vs Ns, `|γ5|`, localisation length, smallest gap vs b. Pass: within 5%, and `b ≤ 0.25` boundary confirmed independently. Then test the *end-mode* dispersion against the physical-mode dispersion: the chiral mode's speed is 0.9855 of the hop rate; a difference would be a species-dependent `c`.

Reference values are those on `main` (`space-ledger-v2.md`, §6.2 "Chiral modes from internal component chains", Table `tab:dw`, after the one-BCC edit at 66ee62f).

**Not available to the author of this design.** The generating code (`qca/dw.py`, `dirac4s.py`, `dirac4.py`, `sym.py`, `dw_gscan.py`, `dw_final.py`, frozen `dirac4.py`) and the L1.2 pre-registration (`/tmp/l12_prereg_stage/PREREGISTRATION.md`, sha256 `733752444dfdbaab68654e583b15fdc97619883224fc30357f8ecba998747239`) are on Edmond's machines and not in this repository. This design was therefore written from the plan, the paper and the L1.1 reason note (`L1_1_one_bcc_reason_r2_20261112/REASON_L1_1_one_BCC_r2.md`, §2 and §7) only. Consequences:

- **The pre-registration governs.** Before any run, the executing agent diffs this design against `PREREGISTRATION.md` and writes `DESIGN_vs_PREREG.md`. Where they conflict, the pre-registration wins unless Edmond rules otherwise. This design adds nothing to the pre-registration that loosens a gate.
- Definitions of `|γ5|` and "localisation length" are quoted verbatim from `dw.py` into `result.json` and are not re-invented. Section 5 says what an independent check of each would be.

## 1. Frozen inputs (verify before running; stop on any mismatch)

| Item | Expected sha256 |
|---|---|
| `qca/dw.py` | `769833f0393dc1599d5944f6a2837c6ff5ac207ce6ca169eaa2ba9b2ca5fd651` |
| `qca/dirac4s.py` | `4db41fe71ce2844f58f1c61c3c84a768b37b82de1bd546a468d3980c3f0627b4` |
| `qca/dirac4.py` (scan script, `dist_gamma`) | `9f01ea8f10947eb6a30506e1499de22e373fc7e1a25fa2689e38c873e2b5aedd` |
| `qca/sym.py` | `7b1bbafd4b01464c8f4d4643582c60994f34ed3e119c4167625f2e5905131764` |
| `qca/dw_gscan.py` | `5bf6af5d089fd17dbe922f335855e9bf961dc731be4025b591e3e0ff16bf938e` |
| frozen symbol module `dirac4.py` | `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff` |
| `qca/dirac4_checks.py` | `4e316d9895f035966bb0aa269216dcc38c3986c50c5118907ab609af8e519c05` |
| `space-ledger-v2.md` (paper reference values) | record the sha256 of the commit actually used; main at `cc2cc5c` or later |
| `PREREGISTRATION.md` | `733752444dfdbaab68654e583b15fdc97619883224fc30357f8ecba998747239` |

The chain stack to run is `dw.py` → `dirac4s.py` → `qca/dirac4.py` → `sym.py`, with `r = 0` (no Wilson term). The sum-form Wilson term is not part of the one-orbit rule and is **not run** (L1.1 reason note, §7).

## 2. Conditions declared before the run (plan §0.1 and §0.4)

- **Lattice.** One BCC orbit through the origin, integer hops `(±1,±1,±1)`, `k` in radians per `a/2`, `2π`-periodic. Exclusion set for global searches: radius 0.3 around every `πg`, `g` an integer triple of even sum (the Γ images of one orbit).
- **Rule.** `dirac4` canonical, with the domain-wall chain, at `φ = 1.4`, `b` as per table, `m = 0` in the hop layers (`S±` at `m = 0`), on-site chain mass `m0` as per table.
- **Load rule.** The §6.2 symbol has no load term, and every L0 and L1.1 symbol result (V5 v2 census) was computed load-free. This run is the same: **load-free symbol, declared.** Plan §0.1 rule 1 says congestion is always ON and OFF is a labelled diagnostic that never counts toward a gate. Under that wording a load-free run could not count. L1.1 closed on a load-free census, so this design follows that precedent. **Decision D1 for Edmond** (§8). A uniform-load invariance check is listed as an optional labelled diagnostic (step X3), not a gate.
- **Whole ticks.** Everything is evaluated at the four-layer cycle eigenvalue `e^{-4iω}`. No sub-tick interpolation. `ω` is per layer, the convention of the paper's Table `dirac4`.
- **No fitting to targets (rule 4).** The tolerances and verdict rules in §4 are fixed and hashed before the first comparison. The paper's values are written into `expected.json` before any run output exists. Fitting a decay rate or a speed from a run is allowed and is labelled "measured".
- **Seeds.** Any random start uses `numpy.random.default_rng(20261112)`, with per-task seeds derived as `20261112 + task index`, all recorded.
- **Failed runs.** Kept unchanged with logs and hashes (rule 7). A failure is a result.

## 3. Pre-flight (stop everything on any failure)

| Id | Check | Stop if |
|---|---|---|
| P0 | Every §1 file hash matches | any mismatch |
| P1 | Chain cycle `floq(k, N_s, 1.4, b)` is unitary at 50 random `k`, for `N_s ∈ {2, 8, 16, 32}` and `b ∈ {0.1, 0.2, 0.25}` | `‖U†U − I‖∞ > 1e-12` |
| P2 | One-orbit periodicity: chain cycle equal at `k` and `k + π(1,1,0)` (and the other two generators) for 20 random `k`, `N_s = 4`, `b = 0.2`, `r = 0` | max difference `> 1e-13` (the L1.1 check C3 gave 1.1e-15) |
| P3 | `dist_gamma((π,π,0)) = 0` (the L1.1 check gave 0.0), and `dist_gamma((π/2,π/2,π/2)) > 0.3` so that point is not excluded by the search | otherwise |
| P4 | Re-run the L1.1 sum-form diagnostic at `r = 0` only: shift difference at the twelve edge labels `≤ 1e-13` | otherwise |

## 4. Cells, reference values and pre-declared verdict rules

All "within 5%" tests are relative to the paper's printed value: `|measured − paper| / |paper| ≤ 0.05`. A cell passes if it meets that, or if the measured value rounds to the paper's printed digits. Each cell is also reported with the measured value to six significant figures.

### R1. Residual end-mode mass (`φ = 1.4`, `b = 0.2`, `m0 = 0.05`, units `E_P` per tick)

| `N_s` | Components | Paper | Rule |
|---|---|---|---|
| 2 | 8 | 2.9e-3 | within 5% |
| 4 | 16 | 1.8e-4 | within 5% |
| 8 | 32 | 7.0e-7 | within 5% |
| 12 | 48 | 2.7e-9 | within 5% |
| 24 | 96 | ~1e-16 ("at the roundoff floor") | **floor cell, see below** |

- **Floor cell (`N_s = 24`).** The generator's own cut (`dw_final.py:9`, `r[:,1]>1e-15`) is why this cell cannot reproduce by construction (plan §2 status line). This run **does not apply that cut.** Declared rule: compute the same quantity at `m0 = 0` and `N_s = 24`, which is exactly massless, and call that the empirical roundoff floor `f24`. The cell passes if `|value at m0 = 0.05| ≤ max(10·f24, 1e-14)`. This is a pass/fail on "at the floor", not a 5% test.
- Also fit and report the decay rate per copy at `m0 = 0.05` over `N_s = 2…12` and at `m0 = 0.1`. Paper: −1.390 against predicted `ln(tan m0 / tan b) = −1.399` (and −0.698 against −0.703 at `m0 = 0.1`). Rule: measured rate within 5% of the paper's fitted rate **and** within 5% of `ln(tan m0/tan b)`. For orientation, the author computed from the paper's printed residual masses that the per-copy rate between adjacent printed `N_s` is −1.390, −1.387, −1.389, and that the printed `N_s = 12` value extrapolated by the predicted rate gives 1.4e-16 at `N_s = 24`. So the printed values are self-consistent. This does not substitute for the run.
- Also confirm `m0 = 0` gives end modes exactly massless: value `≤ 10·f` at each tabulated `N_s`.

### R2. Chirality `|γ5|` ($N_s = 16$, `m0 = 0`)

| `|k|` | 0.01 | 0.05 | 0.1 | 0.15 | 0.2 |
|---|---|---|---|---|---|
| Paper `|γ5|` | 1.0000 | 0.9999 | 0.9993 | 0.9953 | 0.954 |

- Rule: within 5% (plan wording). Reported additionally to four decimals, because 5% is loose near 1.
- Chirality sign: the `s = 1` end mode is right-handed and the `s = N_s` end mode left-handed (paper). Pass requires the signs to match on every `k`.
- At `|k| ≈ 0.3` the paper says `|γ5| ≈ 0.47`. Record, not a gate (the paper gives one rounded value, no printed table cell).
- **Direction.** The paper does not state the direction of `k` for this table. The run takes the 13 directions of R5 and reports the spread. The gate is passed only if every direction is within 5%, and the direction dependence is part of the record.

### R3. Localisation length (components, `N_s = 16`, `m0 = 0`)

| `|k|` | 0.01 | 0.05 | 0.1 | 0.15 | 0.2 |
|---|---|---|---|---|---|
| Paper | 0.12 | 0.20 | 0.29 | 0.40 | 0.64 |

- Rule: within 5%, with the definition quoted from `dw.py` verbatim into `result.json`. If the definition cannot be identified from the code, this cell is reported as "definition not identified" and does not pass or fail. It is not replaced by a guess. The paper's table prints two significant figures, so the 5% rule is applied after the code's own rounding.

### R4. Smallest doubler gap versus `b` (`N_s = 16`, units `E_P` per tick, `r = 0`)

| `b` | 0.10 | 0.15 | 0.20 | 0.25 |
|---|---|---|---|---|
| Paper | 0.058 | 0.046 | 0.034 | 0.022 |

The paper's four values come from 60 random starts each and are stated not to be a proof of the minimum. This run therefore has two searches:

- **R4a (reproduction).** `dw_gscan.py` as hashed, 60 random starts, seeds as in §2, same exclusion. Rule: within 5%, or rounds to the printed value.
- **R4b (independent).** A deterministic dense search, not sharing R4a's random starts: a 129³ boundary-inclusive grid on `[-π,π]³`, every grid local minimum refined by Nelder–Mead, exclusion radius 0.3 around every Γ image, argmin and its distance to the nearest Γ image recorded. This is the method of the official V5 v2 census (`results.json` `ca6793ea…`), applied to the chain. Rule: R4b within 5% of the paper. In addition, a **two-sided classification** is recorded in advance:
  - R4b within 5% of the paper: the paper's value stands.
  - R4b below the paper by more than 5%: the paper's value is **not** the minimum. This is a finding, not a pass. Report the argmin.
  - R4b above the paper by more than 5%: R4a's random search found a point the grid refinement did not. Report both argmins.
- The paper's bulk (interior-component) gap at `b = 0.2` is 0.033 `E_P`. Compute it, report it, and apply the 5% rule.

### R5. The `b ≤ 0.25` boundary, confirmed independently

The paper (one-BCC edit) says that for `b ≥ 0.3` a doubler end mode survives near `k = (π/2, π/2, ±π/2)` with a gap that falls exponentially with `N_s`; that point differs from Γ by a vector that is not a reciprocal lattice vector; so the construction needs `b ≲ 0.25`.

Independent means: not through `dw_gscan.py`'s random starts and not through the `qca/RESULTS.md` line cited by the edit set.

- **Procedure.** For `b ∈ {0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40}` and `N_s ∈ {8, 16, 24, 32, 48}`, at `m0 = 0`:
  1. At each of the eight points `(±π/2, ±π/2, ±π/2)`, record which are equivalent modulo the reciprocal lattice of the orbit, then take the smallest `|ω|` and the weight of that eigenvector on the two end copies `s = 1` and `s = N_s`.
  2. Fit `ln(gap)` versus `N_s` over `N_s = 24, 32, 48`.
- **Declared verdict rules (frozen at hash time).**
  - A doubler end mode **survives at `(b, N_s)`** if the eigenvector's end-copy weight is `≥ 0.5` and the smallest `|ω|` is below the R4 gap for the same `b`.
  - `b` **is allowed** if no such end mode survives at `N_s = 48` and the fitted gap does not decay: fitted slope `> −0.05` per copy, i.e. the gap converges.
  - `b` **is excluded** if an end mode survives and the fitted slope is `≤ −0.1` per copy.
  - Anything between those is reported as "unresolved" and the table keeps the `b = 0.3` and `b = 0.25` rows open. The thresholds 0.5, −0.05 and −0.1 are proposals made here without having seen the data. They are fixed when this design is hashed and are not changed afterwards.
- **Pass:** `b ≤ 0.25` all "allowed" and `b ≥ 0.3` "excluded". If the transition falls at a different `b`, the result is recorded as measured, the plan's "`b ≤ 0.25`" statement is recorded as **not confirmed**, and the paper line is flagged. No `b` value is adjusted to make it pass.
- **Cross-check with R4b.** For each `b`, the R4b argmin location and the point found in step 1 should agree (distance `≤ 0.3`) wherever the end mode survives. If they disagree, report it.

### R6. End-mode speed versus physical-mode speed (the "species-dependent `c`" test)

- **End mode.** For each of the 13 direction classes (3 axes `[100]`, 6 face diagonals `[110]`, 4 body diagonals `[111]`, including `[11−1]` as a body diagonal), at `N_s = 16`, `m0 = 0`, `b = 0.2`, `φ = 1.4`: group velocity `v_g = dω/d|k|` of the end mode at `|k| = 0.01, 0.02, 0.03, 0.04, 0.05`, extrapolated to `|k| → 0` (Richardson, as `VERIFY.md` did). Report in units of the hop rate. Paper: 0.9855. Also report the direction spread against `|k|` and its fitted exponent (paper: `k^{2.00}`, about `5e-4` at `k = 0.05`).
- **Physical mode (reference).** The unchained §6.2 rule at `φ = 1.4`: the paper's `c0 = 0.98911`, and the Richardson value `0.98910736` of `VERIFY.md`. Re-measured here by the same code path with `N_s = 1` and no chain, so both numbers come from one code version.
- **Verdict rule.** Species-independent `c` requires `|v_end − v_phys| / v_phys ≤ 1e-6` (the paper's own stated direction-independence level of the low-energy light speed). Anything larger is recorded as **a measured species-dependent difference**, with its value.
- **Expected outcome, stated in advance so it cannot be adjusted afterwards.** The paper's own two numbers differ: 0.98911 and 0.9855 differ by 0.00361, or 0.365%. The run is expected to confirm a difference of about that size rather than agreement. The plan's wording says "a difference would be a species-dependent `c`". The paper treats 0.9855 as the tick of the chained rule (`τ = 0.9855 t_P`), so the question for Edmond is what the gate should say about it. **Decision D2** (§8). The run measures and reports. It does not decide.
- Also report the end mode against any gapped bulk chain mode at the lowest `k` (reference only), and the end mode's `ω`-versus-`k` curve to `|k| = 0.25` (the paper's stated limit of the chiral mode).

### X. Report-only extras (not gates)

| Id | What | Reason |
|---|---|---|
| X1 | Real-space exactness at `N_s = 8`: periodic `40³` cubic grid, point source (one orbit of `40³/4` nodes), 24 ticks. Unitarity, probability outside the one-hop light cone, probability conservation, reversal. Paper: `9e-16`, 0, `2e-15`, `2e-15` | The paper prints them in the same section; cheap |
| X2 | Reproduce the Table `dw` printed component counts (`4 N_s`) and the paper's Cost sentence (32 and 64 components at `N_s = 8, 16`) | Trivial bookkeeping check |
| X3 | Uniform-load invariance (labelled diagnostic, congestion on by a uniform load): confirm that a uniform load only rescales the end-mode speed and leaves residual mass and `|γ5|` unchanged | Plan §3 L1.1 says uniform load only rescales velocity. Only relevant if Edmond rules D1 the other way. The rule used must be named per §0.4. Skip unless D1 requires it |

## 5. Independent checks of the definitions (no new physics)

- `|γ5|`: also compute `⟨ψ|γ5|ψ⟩` directly from the end-mode eigenvector of the cycle matrix with `γ5 = τ_z ⊗ 1` on the (R, L) label, and report it next to the code's value. A mismatch is a finding about the definition, not about the physics.
- Residual mass: also compute it two ways, the smallest `|ω|` at `|k| = 0` and the Dirac-fit `ω_0` from the low-`k` dispersion. They should agree to rounding.

## 6. Order of work, resource estimate and cap proposal

| Step | Work | Rough cost (author's estimate, not measured) |
|---|---|---|
| S0 | P0–P4 | seconds |
| S1 | R1, R2, R3, R6 (single `k`, or a few dozen `k`) | minutes |
| S2 | R4a (60 random starts × 4 `b`) | tens of minutes |
| S3 | R4b (129³ grid × 4 `b`; 64×64 eigenproblems for 2.15M points per `b`, then refinement) | order of an hour, multi-thread |
| S4 | R5 (7 `b` × 5 `N_s`, point evaluations and a few fits; the `N_s = 48` problem is 192×192) | minutes |
| S5 | X1, X2 (and X3 only if D1 requires it) | minutes |

I have not seen the code. These costs are guesses from matrix sizes and are not benchmarks. The first thing the executing agent does after S0 is time a single `N_s = 16` grid point and re-state the estimate in `result.json` before S3.

### Cap proposal (plan §0.2 needs stated caps)

Edmond said in chat on 12 November 2026 (about 4:15 PM America/New_York) that the Grok bot has "full access no cap" on `bigbang`. Plan §0.2 says every run has stated caps and `result.json` records them. This proposal reconciles the two: **the caps are recorded ceilings, soft, and exceeding a ceiling is logged but does not by itself kill the run.** The hard rules are the ones that cost nothing: one attempt per step, and stop on any failed check.

| Cap | Proposed ceiling |
|---|---|
| Memory | 96 GiB resident (of 128 GiB), per process 48 GiB |
| CPU | float64 on CPU, up to 20 threads, no GPU needed |
| Wall time | 8 h total, 2 h per step |
| Output | 1 GiB under `runs/<date>_<id>/`, raw eigenvalue arrays only if the step needs them |
| Attempts | **one per step**; a failed step is preserved, then a corrected re-run is a new run with its own id and its own approval |
| Stop rules | **stop on any failed pre-flight (P0–P4)**; stop and report on any check in §3 failing mid-run; no silent retry; do not edit the frozen sources to make a check pass |

If the real cost of S3 turns out to be an order of magnitude above the estimate, the ceilings are raised by a note in `result.json` stating the old and new value and the reason, and Edmond is pinged before the step that exceeds them.

## 7. What `result.json` must contain (plan §0.2)

Code version (all §1 hashes, plus `git` commit if the sources are in a repo), seed(s), grid, boundary condition (periodic, one orbit), units (`E_P` per tick, hop-rate speeds), load rule ("none, §6.2 vacuum symbol, per D1"), caps and resources used (CPU seconds, peak RSS, wall time, output size per step), the verdict for every cell with the measured value and the paper value side by side, the verbatim definitions of `|γ5|` and localisation length, `DESIGN_vs_PREREG.md`, the sha256 of this design as frozen, and the raw logs. The table must be regenerable from `result.json` (plan §9 rule 4).

## 8. Decisions for Edmond

- **D1: load rule for a free-spectrum gate.** Plan §0.1 rule 1 says congestion is always ON and a congestion-off run never counts toward a gate. L0 and L1.1 closed on a load-free symbol census. Proposed: L1.2 runs load-free, as L1.1 did, and that is declared in `result.json`. The alternative is to treat the §6.2 symbol as the vacuum rule and say so in a one-line plan note. Either is a plan wording choice, which this design does not make.
- **D2: what "species-dependent `c`" means for the gate.** The paper's own numbers give 0.98911 for the unchained cone and 0.9855 for the chained end mode, a 0.365% difference, and treat the chained value as the tick. The run will measure the difference to six figures. Whether the L1.2 gate then reads "pass, difference recorded", "fail", or "needs a statement that the chain defines the tick for chained species only" is your call. The paper's §6.1 and §7.2 wording about `τ` depends on it.
- **D3: thresholds in R5.** The 0.5, −0.05 and −0.1 thresholds are proposals made without the data. Change them now or accept them. They freeze when this file is hashed.
- **D4: `PREREGISTRATION.md`.** Confirm that it governs where it conflicts with this design (§0).

## 9. Approval and freezing

1. Edmond reviews. A one-line approval naming the sha256 of this file (see `SHA256SUMS` beside it) is the approval required by plan §0.2 for steps S0–S5, under the caps in §6.
2. The executing agent copies this file unchanged to the run directory, hashes it, and writes `expected.json` (the paper's values) before any computation.
3. Nothing is authorised beyond S0–S5. In particular, no paper, plan, repo or archived-record edit is authorised by this design, and no figure (`domainwall.png`) is regenerated.
4. After the run, Edmond is pinged with the verdict table and the two decisions D1 and D2 as they stand after the data.
