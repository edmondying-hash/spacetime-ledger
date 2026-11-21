# Repair specification for L1.1 — the three edge momenta — r8

**Status: draft for Edmond's review. Not hashed, not approved, nothing run under it.**

**r8 (2026-11-11):** r7 is kept unchanged as `REPAIR_SPEC_L1_1_r7.md` (sha256 `aeca56e4a60bf57a929bb48b1651a23863651e97b41ebeb1b87a06663380ebbb`). r8 replaces route 3 in §6: the chain + Wilson `r = 0.05` term is not missing. It is implemented in the frozen chain source and reproduces the paper's `2.663e−2` (`0.0266255` at `N_s = 32`, 41³, exactly unitary, Γ = 0, the twelve edge zeros lifted). The gate still rejects it: at `φ = 1.4` the repaired minimum is `32%` of the §3.4 floor, a factor `3.08` below it. §7 now records that no candidate passes §3, so L1.1 is blocked on a decision — find a repair that clears §3.4, or re-decide the floor — not on a missing term. §8 records the route 3 provenance. §3.4 is unchanged. This version changes no paper, repo, Sheet or production file; no new simulation was run, the route 3 numbers are read from the existing 2026-11-09 run and its frozen source.

**r7 (2026-11-11):** r6 is kept unchanged as `REPAIR_SPEC_L1_1_r6.md` (sha256 `b02fddd5e1848ed5202c6d2676395876340e2a718e6499280c453d1f461ba604`). r7 replaces one sentence in §4: the unitarity defect is not "0.12–0.84 depending on k" (those are the three probe-point values, and 0.84 was not measured); it is `0.12`, `0.42` and `0.72` at the probe point for the three rows, and across a 41³ sample the median is `1e1`–`1e2` with largest values `8×10²`, `6×10³` and `3×10⁴`. Nothing else is changed. This version changes no paper, repo, Sheet or production file, and no simulation was run to make it.

**r6 (2026-11-11):** r5 is kept unchanged as `REPAIR_SPEC_L1_1_r5.md` (sha256 `9dab86441c6236fd4d065bb11cdc8d65f41672acda23da00a51d4c26f18043cd`). r6 records that the §4 table — which reproduces — is the phase of a non-unitary operator: with `g` added to `u` and `n` untouched, the step is not unitary (R1). Exact unitarity forces `Δ ∈ {0, −2u}` at every k, which closes every additive potential on `u` before any floor, grid or census. §4 gains the unitarity column and the 27-point counts; §5 is rewritten as that branch condition, and the coefficient-exclusion list that stood in r5 is not restated as a constraint; §6 strikes route 1 and records that route 2 is closed by the same argument; §8 records that `periodS` was unmodified only for the baseline, that the candidates modified `A/E` and `Xh`, and that on bigbang `dirac4s.py` cannot be imported as it stands. A companion erratum to plan v3.2 line 391 is sent with this file. The §3.4 floor and the "no worse" rule are unchanged. This version changes no paper, repo, Sheet or production file, and no simulation was run to make it.

**r5 (2026-11-11):** r4 is kept unchanged as `REPAIR_SPEC_L1_1_r4.md` (sha256 `f10df42baa5b7712327150229ece5e3e55a5be42ebc2be4e9cf0fed2b9a48c4f`). r5 withdraws numbers that came from a cycle that applied `V(+1)` twice (`0.637463`, `0.0214`, `0.0400`, `0.0251`, and the claim that the plan's `0.221` does not reproduce); replaces §4's table with special-point values from `dirac4s.periodS`, validated against the paper's corner `0.170796 = π/2 − 1.4`; states that the interior gate runs through the census code, not a scratch script; and drops the withdrawn `0.0214` illustration from §3.4. The per-φ floor and the "no worse" rule are unchanged. This version changes no paper, repo, Sheet or production file, and no simulation was run to make it.

**r4 (2026-11-11):** r3 is kept unchanged as `REPAIR_SPEC_L1_1_r3.md` (sha256 `4f21643d37778dabb0150146e8c2bf25de21b7f68d3aa1d0eeab0f6afd877a1a`). r4 restores the status marker that r3 dropped, and notes that the plan's L1.1 text is unchanged in v3.3. §3.4 is unchanged from r3. This version changes no paper, repo, Sheet or production file, and no simulation was run to make it.

**r3 (2026-11-11):** r2 is kept unchanged as `REPAIR_SPEC_L1_1_r2.md` (sha256 `6815c4cc725dc84a5a251c05367f96851772977a51116e1460d315e5fa8c445a`). r3 changes only §3.4: the floor is "no worse than what it starts from", per φ, taken from the official V5 v2 `search_a` column (`results.json` sha256 `ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708`); φ = π/2 is reported, not gated, and is not given a floor; the paper's 2.663e−2 is not the floor. To match, it also updates the title and the status line at the top.
Written from this chat's checks against paper main@393f4493 (`e86ef5c3…`) and plan v3.2 (`5e5891bb…`) (unchanged in v3.3).

## 0. What this document is for

The unrepaired §6.2 four-component rule has three exact massless momenta
(12 sign labels) at the edge points `(±π,±π,0)` and permutations, independent of φ,
with the Wilson layer present. L1.1 requires either that Γ is the only zero, or a
reason the others are unphysical that survives a finite even lattice. We take the
**repair** branch, so this document fixes what an acceptable repair is, how it is
tested, and why the two obvious candidates fail. It does not choose a repair.

## 1. The rule a repair must preserve

`U_k = V⁻ S⁻ V⁺ S⁺`, four ticks: right step, Wilson layer, left step, mirrored
Wilson layer; corner hops `h ∈ {(±1,±1,±1)}`, `k` in radians, cubic cell 2,
symbol 2π-periodic; the Wilson layer `V± = exp(∓iφX) exp(±iφτx)` cancels exactly
at Γ because `X(Γ) = τx`. Unitary at every k. Any repair is a change to this
object, not a replacement for it.

## 2. Required properties

- **R1 Unitary by construction.** Not unitary to numerical tolerance in tests only:
  the repair must be an exponential of a Hermitian operator, or otherwise exactly
  unitary in exact arithmetic.
- **R2 Γ massless.** δ = 0 at k = 0 to within the double-precision floor,
  i.e. |ω(Γ)| ≤ 1e−15.
- **R3 No zero but Γ.** No other k in the Brillouin zone has ω = 0. Tested exactly
  at the 27 special points (§3.1) and by scan everywhere else (§3.2–3.3).
- **R4 Recovery.** The repaired rule reduces to the paper's rule as the repair
  parameter → 0, so Table `dirac4` and every earlier result are the limit, not a
  different rule. This is what makes the repair a repair and not a new model.
- **R5 Locality.** The repair is a finite-range term: the rule stays a cellular
  automaton with a small hop set, and any Fourier support beyond the corner hops
  must be stated and bounded.
- **R6 Structure preserved.** The four-tick cycle, the handedness alternation and
  the τx cancellation at Γ are unchanged; the repair enters as an addition to the
  symbol, not as a reordering of the ticks.
- **R7 Parameter fixed before measurement.** The value (or functional form) is
  written down with its reason **before** L1.4 or L1.5 is measured. A parameter
  chosen after seeing the dispersion numbers is a fit, not a repair.

## 3. The decision procedure — mandatory before any census or L1.4/L1.5 run

### 3.1 Exact enumeration of the 27 special points
Every point with `k_i ∈ {0, ±π}` — 27 of them — is evaluated **algebraically**, not
by grid: at these points `n = 0` and `u = ±1`, so the cycle collapses and ω is
exactly 0 or a closed-form value. Tabulate `u`, `u'`, `n`, ω for all 27, and name
which are zero. The corner `(π,π,π)` is one of them and has been the failure point
of a candidate already.

### 3.2 Grid scan
The interior scan is run through the official V5 v2 census code, not a scratch
script. The procedure is the one that produced the floor: find local minima,
then discard converged points inside the exclusion (`|k| < 0.3` of a Γ image).
A grid-point minimum outside the balls is a different functional and is not
the gate. Report the smallest non-excluded |ω| and its argmin in units of π
and radians, from both search (a) (300 `default_rng(0)` starts) and search (b)
(boundary-inclusive `linspace(−π, π, 129)` per axis).

### 3.3 Refinement
The 64 lowest grid points refined by Nelder–Mead (xatol 1e−9, fatol 1e−13), same
exclusion. A refined minimum below the grid minimum is a finding.

### 3.4 Acceptance
PASS requires **all** of: R2 met; no zero at any of the 26 non-Γ special points;
no zero anywhere else on the 129³ grid or after refinement; and, at every gated φ,
the repaired smallest non-excluded minimum ≥ the unrepaired minimum at the same φ.

The floor is "no worse than what it starts from", per φ, not a single threshold.
The unrepaired minima are taken from the official V5 v2 census that reproduced
Table `dirac4`: `results.json` sha256
`ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708`, column
`search_a` (the column compared to the paper). `search_b` (the 129³ grid) agrees
with these values to better than 1e−16 on every row.

| φ | unrepaired minimum (floor) |
|---|---|
| 0.5 | `0.217127955311918` |
| 0.8 | `0.26167630634482675` |
| 1.0 | `0.23202826004369173` |
| 1.2 | `0.1668769618006517` |
| 1.4 | `0.08212694658054251` |
| 1.5 | `0.034884422707531004` |
| π/2 | reported, not gated |

The six numbered rows are gated. The rule at each of them is: the repaired smallest non-excluded minimum ≥ the unrepaired minimum at the same φ.
A patch cannot be tuned at φ = 1.4 and pass elsewhere.

At φ = π/2 the unrepaired rule is itself at zero (the paper's row says "0
(doublers return)"). The "no worse" test is vacuous there and any patch would
pass, so that row is reported, not gated, and is not given a floor. The gate
is the other six.

The paper's adopted 2.663e−2 is not the floor: it belongs to the chain
construction, it is lower than 0.082, and using it would admit a patch that
drops the plain rule's bulk gap from 0.082 to 0.027 and still passes. That is
the failure mode the floor exists to catch.

The 64-point Nelder–Mead refinement (§3.3) is a post-screen acceptance step,
not part of the floor: anything the grid rejects never reaches it.

### 3.5 Record
Rule form, parameter, grid, exclusion radius, argmins, the 27-point table, and the
scan outputs, hashed. A repair that fails any clause is recorded as failed, not
tuned and re-run in place.

## 4. Why the obvious `g(k)` fails — evidence

Validated implementation: the unrepaired baseline is `dirac4s.periodS` (the
four-layer cycle as written), unmodified. At φ = 1.4 it gives Γ = 0, the
three edge momenta = `1.5e−16`, and `(π,π,π)` = `0.170796326795`, which is
`π/2 − 1.4` — the paper's own value. That agreement is what makes the
baseline column worth quoting.

The candidate rows use the same cycle with the substitution `u → u+g` in
both `A/E` and `Xh`. For those rows `periodS` is not used unmodified. The
table is the phase of the resulting operator, the unitarity defect
`|U†U−I|` at k = (0.7, 0.3, 0.11), φ = 1.4, m = 0, and the number of
zeros among the 27 special points.

| candidate at φ = 1.4 | Γ | edge momenta | corner | ‖U†U−I‖ at k=(0.7, 0.3, 0.11) | zeros of 27 |
|---|---|---|---|---|---|
| none | 0 | 1.5e−16 | `0.170796326795` = π/2−1.4 | 7.8e−16 | 13 (Γ + 12 edges) |
| `+⅓ Σ(1−cos)` | 0 | 0.04850596 | 1.9e−16 | **0.72** | 9 (Γ + 8 corners) |
| `−⅓ Σ(1−cos)` | 0 | 0.32414532 | 0.11411267 | **0.42** | 1 |
| `+⅓ Σ(1−cos)²` | 0 | 0.061895934 | 0.056683652 | **0.12** | 1 |

The baseline validation is real, and the `+⅓` corner identity is exact: at
`(π,π,π)`, `u = −1`, `n = 0`, and `g = ⅓·6 = 2`, so `u' = +1` exactly as
at Γ; every layer collapses and the cycle is the identity. The patch
moves the doubling rather than removing it.

With `g` added to `u` and `n` untouched, `a†a = (1 + 2ug + g²)I₂`, so the
step `E` is not unitary. The product is off by `0.12`, `0.42` and `0.72` at
the probe point for the three rows; across a 41³ sample the median is
`1e1`–`1e2` and the largest values are `8×10²`, `6×10³` and `3×10⁴`. R1
in §2 forbids exactly this.

Two lines of algebra close the whole route. Exact unitarity requires
`(u+Δ)² + |n|² = 1`, i.e. `Δ(2u+Δ) = 0`, so `Δ ∈ {0, −2u}` at every k.
`Δ ≡ 0` is no repair; `Δ = −2u` flips the sign at Γ, giving
`ω(Γ) = π/2 − φ ≠ 0` and breaking R2. No additive potential on `u` is
both exactly unitary and Γ-massless — before any floor, grid or census.

The only exactly-unitary reading of the same patch inverts the table's
conclusions. Renormalising `(u+g, n)` onto the unit sphere makes the rule
exactly unitary (defects ~1e−16) but changes the 27-point counts: `+⅓` →
**21 zeros** (Γ + 12 edges + 8 corners, so the edges are not lifted at
all), `+⅓ Σs²` → **27 zeros**, `−⅓` → Γ only, with all 26 remaining
points at exactly `π/2 − φ = 0.170796`. That reading divides by
`|q| = √(trig polynomial)`, which is generically an infinite Fourier
series — R5 fails. Additive-`u` is therefore either non-unitary or
non-local.

Where `0.637` came from — the plan prescribes it. Plan v3.2 line 391
(sha256 `5e5891bb55fc5449965f7efba8482bfecd135c30172f770d7dc65564db4902dd`;
the same sentence is line 392 of the live plan v3.3 r2, sha256
`89b3972a0af418bfcb260b978842e79dc73945c61ec2bd85fe3a5e7d1785aa39`) says
"use a matrix exponential if `X²≠1`". Exponentiating spectrally at the
edge gives `0.637462993 = (2π − (8/3)·1.4)/4` exactly, with
`|U†U−I| = 28.6`; the polynomial `cos φ − i sin φ X` gives `0.048506`
with defect 837. The r5 withdrawal of `0.637463` is correct, and the
plan's edge-lift number is the arithmetic fingerprint of that layer, not
a lift. The plan's `0.221` presumably reproduces on the same rule, which
would validate nothing. A companion erratum records this and is sent
with this file.

The interior column is empty by intent. A 41³ scratch scan returns `0.2034` at
φ = 0.5 where V5 has `0.2171`, because a grid point outside the exclusion balls
is a different functional from "find local minima, then discard converged
points inside". The interior gate must be run through the census code, and no
scratch number belongs here.

Withdrawn, all from a cycle that applied `V(+1)` twice: `0.637463` wherever it
appeared, `0.0214`, `0.0400`, `0.0251`, and the claim that the plan's `0.221`
does not reproduce.

## 5. Structural constraint any repair must meet

Exact unitarity forces `Δ ∈ {0, −2u}` at every k; `Δ = −2u` gives
`u(Γ) = −1` and `ω(Γ) = π/2 − φ`. The first branch (`Δ ≡ 0`) is no
repair; the second breaks R2. There is no third branch. No additive
potential on `u` is both exactly unitary and Γ-massless — before any
floor, grid or census.

## 6. Candidate routes

1. **Struck.** Additive `g` on `u`. Closed by the branch condition in §5: no
   additive potential on `u` is both exactly unitary and Γ-massless. The
   §4 table is the phase of a non-unitary operator, not a walk; the
   renormalised reading of the same patch fails R5.

2. **Closed by the same argument.** A term `h` of `s_i = 1 − cos k_i` added
   to `u` is still an additive potential on `u`. The recorded failures of
   `u² − 1` (zero at every special point) and of `Π cos k_i` (unable to
   distinguish Γ from the edges) stand as recorded. They are not a residual
   search space, and neither are the quadratic and higher members
   (`Σ s_i²` and the rest): those are the same construction and are closed
   by §5, before any floor.

3. **Chain + Wilson `r = 0.05`** — the paper's route. **Implemented, and reproduced.**
   The term is the Wilson mass in the *angle* form: the step's mass block uses
   `t = arcsin m + r·Σ(1−cos k_i)`, which is unitary for any `t`. It is `S_step` in the
   frozen chain source `chiral_rscan_20261109/src_readonly/dirac4.py` (sha256
   `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff`), driven by
   `U_slab` in `run_chiral_wall_count.py` and `omega_abs_only` in `run_rscan.py`. The
   chain is `W = R(N_s, b = 0.2)·(I ⊗ M(m₀ = 0))` on `4N_s` components, `N_s = 32`.
   At `φ = 1.4`, `r = 0.05` the 41³ zone-interior minimum is `0.0266255`
   (`results_low_r_followup.json`, `41_ns32_min_over_loci`), which is the paper's
   `2.663e−2`; `r = 0.1` gives `2.004e−2`. Re-evaluated here from the same source:
   `Γ = 0` exactly, `|λ| − 1 ≤ 1e−14`, and the 27 special points sit at `0.0504148`
   at `(±π,±π,0)`, `0.1710678` at the faces and `0.2710391` at the corner. The twelve
   edge zeros are lifted, so R1 and R2 are met. (The run's own JSON labels the
   `(±π,±π,0)` part `faces` and calls a different locus `edges`; this document keeps
   §1's naming.)

   **It fails §3.4.** At `φ = 1.4` the unrepaired floor is `0.08212694658054251` and the
   repaired minimum is `0.0266255` — `32%` of the floor, a factor `3.08` below it. The
   repair buys the twelve edge zeros with the interior gap, `0.0821 → 0.0266`; the floor
   exists to reject exactly that trade, and it does. The paper's own text calls the
   adopted gap "one third ($1/3.0$) of the $0.08\,E_P$ reference".

A construction that stays inside SU(2) by composing the symbol with a
finite-hop unit quaternion — `a(k) → a(k)·b(k)` with `b` the symbol of an
added hop — was proposed in this chat. Then `|q| = 1` and finite range hold
by construction, and the edge no longer sits at `u' = 1`, so the 12 zeros
lift generically. It is a new direction. This document does not choose it
and does not authorise a run.

## 7. What this blocks

- The L1.1 census pre-registration — nothing to census until a repair passes §3, and
  no candidate currently does: the additive family is closed by R1 (§4–§5), and the
  chain + Wilson `r = 0.05` clears R1 and R2 but lands at `32%` of the §3.4 floor at
  `φ = 1.4` (§6, route 3). L1.1 is blocked on a decision — a repair that clears §3.4,
  or a re-decision of the floor, which is a change to the gate and not to a candidate.
- L1.4 and L1.5 re-measurement — they are measured *on the repaired rule* (R7).
- The L1 exit gate, and with it L2.0 onward, per plan v3.2.

## 8. Provenance of the checks quoted here

The unrepaired baseline numbers in §4 are from `dirac4s.periodS`, the
paper's own four-layer cycle as written — `V(−1)E(−)V(+1)E(+)` —
unmodified. The unrepaired baseline at φ = 1.4 reproduces the paper's
independently known corner value `0.170796326795 = π/2 − 1.4`, and gives
Γ = 0 and the three edge momenta at `1.5e−16`. That is the validation.

The candidate rows required modifying `A/E` and `Xh` to perform
`u → u+g`; `periodS` was used unmodified only for the baseline. The
phases, unitarity defects and 27-point counts on those rows are those of
the resulting operator. They are not numbers about a unitary quantum walk.

On bigbang, `dirac4s.py` cannot be imported as it stands: it does
`exec(open('/workspace/qca/dirac4.py').read())`. A rerun needs that path
written down. The checks quoted here used a patched module path.

An earlier implementation applied `V(+1)` twice; the numbers it produced
(`0.637463`, `0.0214`, `0.0400`, `0.0251`, and the claim that the plan's
`0.221` does not reproduce) are withdrawn and must not be reused. The
plan's `0.637` is `0.637462993 = (2π − (8/3)·1.4)/4` exactly, with
`|U†U−I| = 28.6` at the edge — the arithmetic fingerprint of the
spectral exponential that plan v3.2 line 391 sanctions, not a lift. The
companion erratum records this.

The route 3 numbers are not from `periodS`. They are from the frozen chain source
`chiral_rscan_20261109/src_readonly/dirac4.py` (sha256
`f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff`), driven by
`U_slab` in `run_chiral_wall_count.py` and `omega_abs_only` in `run_rscan.py`, with
the Wilson mass in angle form `t = arcsin m + r Σ(1−cos k_i)` on `4N_s` components
(`W = R(N_s, b = 0.2)·(I ⊗ M(m₀ = 0))`). The 41³ record is `results_low_r_followup.json`:
`41_ns32_min_over_loci = 0.0266254779`, and `fits/0.05` gives `0.0304206`, `0.0295478`,
`0.0292282` at `N_s = 16, 24, 32`. The three special-point values in §6 were
re-evaluated from that source for this revision, not read from the run.

The interior gate is not measured by a scratch script; it is run through the
census code.
