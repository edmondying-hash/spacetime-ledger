# L1.1 — the three edge momenta — r9: identification note

**Status: draft for Edmond's review. Not hashed, not approved, nothing run under it. No simulation, census, grid, scan or script was run to write it.**

**r9 (2026-11-12):** r8 is kept unchanged as `REPAIR_SPEC_L1_1_r8.md` (sha256 `ad02c20147677e527fc81f5f3b6e27a0dd2f1b300cf8dcde4152cc8fdab63afc`; folder `L1_1_repair_spec_r8_20261111/`, sign-off sidecar `L1_1_repair_spec_r8_20261111_SIGNOFF.txt`). r9 is a new document in a new folder. It does not edit, re-encode or re-line-end r8, its diff, its `SHA256SUMS`, the sign-off sidecar, layered plan v3.3 r2 (`layered_plan_v3.3.md` sha256 `89b3972a0af418bfcb260b978842e79dc73945c61ec2bd85fe3a5e7d1785aa39`), `space-ledger-v2.md` (sha256 `e86ef5c3f1ad9331d61c6033e300dfd37232f4836ce39a55b206bf3985335dc8`) or `space-ledger-v2.pdf`.

What changed relative to r8:

- r8 treated the twelve edge zeros as a defect of one rule that needs a repair, and recorded that no candidate passes §3.4. r9 records an identification instead: on the paper's own ledger space `ℓ²(BCC) ⊗ ℂ⁴` the twelve edge labels are Γ, so there is nothing to repair.
- R3 is reworded (§3). R4–R7 become vacuous. R1 and R2 stand.
- The §3.4 floor table is not touched, re-decided or lowered. No route of r8 §6 is adopted: route 3 (chain + Wilson `r = 0.05`) is not adopted, and the composition route is not a candidate (§7).
- r8 §7's block ("a repair that clears §3.4, or a re-decision of the floor") is not carried into r9's reading (§5).
- One follow-up is recorded as design only, not approved and not run (§6).

Checked against: `space-ledger-v2.md` §6.2 (hop symbols `A^ε`, the cycle `U_k`, the Doublers bullet, "Doublers and bulk"), `layered_plan_v3.3.md` §2 (V3 status line), §3 (L1.1), §8 (traceability) and §10, and `REPAIR_SPEC_L1_1_r8.md`. Every number below that is not marked otherwise is read from those files or is closed-form algebra on the paper's symbol. Where a number in the handoff disagreed with a file, the file is quoted (§9).

## 1. The rule is unchanged

`U_k = V⁻ S⁻ V⁺ S⁺`, as boxed in paper §6.2. Corner hops `h ∈ {(±1,±1,±1)}` in units of `a/2`, `T_hψ(x) = ψ(x − h)`, hop symbols `A^ε_k = u^ε σ₀ − i n^ε·σ` with `u^ε = c_x c_y c_z − ε s_x s_y s_z`, Wilson layers `V^ε = e^{−iφX^ε} e^{+iφτ_x}`, `X^ε = u^ε τ_x + τ_y ⊗ (n^ε·σ)`, `ν² + m² = 1`. r9 changes nothing in it, adds no parameter, and changes no code.

## 2. The identification

**The paper's state space is one BCC grid.** Paper §6.2 ("Formal update rule"): "Each core x on the BCC grid carries ψ(x) = (ψ_R(x), ψ_L(x))ᵀ ∈ ℂ² ⊕ ℂ². The ledger Hilbert space is ℋ = ℓ²(BCC) ⊗ ℂ⁴." The four-taste ℤ³ reading is a property of a computation that runs on all of ℤ³. The same section's Doublers bullet describes that computation ("the grid is ℤ³, the diagonal hops … split it into four decoupled BCC orbits … the Γ cone on the other three tastes"). r9 adopts the `ℓ²(BCC)` definition as the physical model, one orbit `x ≡ y ≡ z (mod 2)`.

**Every layer is diagonal-hop or on-site.** `S^±` and `V^±` consist of the eight corner hops `(±1,±1,±1)` plus on-site matrices; each hop flips the parity of all three coordinates together, so it maps an orbit to itself. The mass mixing is on-site. In the chain (Table `dw`) the internal rotation `R(b)` mixes `L_s` with `R_{s+1}` on the same node, and "no hop ever changes `s`" (paper, chiral modes from internal component chains). None of these connects one parity orbit to another.

**So projection onto one orbit commutes with the cycle.** Unitarity, the one-link light cone per layer, reversibility, and the Γ cone are those of the same operator restricted to an invariant subspace. No parameter is added.

**The reciprocal lattice of the symbol.** The symbol depends on `k` only through `e^{ik·h}`. For `G = (aπ, bπ, cπ)` with `a + b + c` even, `G·h ∈ 2πℤ` for every corner hop, so the symbol is periodic under these `G` together with `2πℤ³`. On the orbit, `e^{iG·x} = e^{iπ(ax + by + cz)}`, and for `G = (π, π, 0)` with `x ≡ y (mod 2)` the exponent is `π(x + y)` with `x + y` even, so `e^{iG·x} = 1` exactly, for any even finite `L`. (Handoff note: "432 orbit sites, max |e^{iG·x} − 1| = 1.5e−15, and 2 on the other three ℤ³ orbits" is a numeric check from the previous chat; it was not re-run here, and the argument above does not depend on it. 432 = 12³/4.) `(π, π, π)` and `(π, 0, 0)` are not of this form: `a + b + c` is odd, and `e^{iG·x} = −1` on the odd-coordinate sites.

**What the 27 labels are.** The 27 points `k_i ∈ {0, ±π}` of the paper's census are 8 points on the `2π` torus, because `+π` and `−π` are the same point. Under the BCC reciprocal lattice they fall in two classes (§4).

**The twelve edge labels.** `(±π,±π,0)`, `(±π,0,±π)`, `(0,±π,±π)`: twelve sign labels, three momenta, four sign labels each, all Γ images. The paper says as much in its Doublers bullet ("three distinct momenta (twelve sign labels) — the Γ cone on the other three tastes") and in "Doublers and bulk" ("the twelve edge points … these three distinct momenta"). Plan v3.3 §2's V3 status line says "those twelve points are Γ images under the even-parity lattice and lie in the V5 exclusion set." r9 is the same statement given its own note.

## 3. The revised requirement

Relative to r8 §2:

- **R1 Unitary by construction.** Unchanged. The paper's rule is exactly unitary.
- **R2 Γ massless.** Unchanged. `|ω(Γ)| ≤ 1e−15` is the one condition that remains to be met. At Γ, `u = +1`, `n = 0`, `V = 1`, `S = I` at `m = 0`, so `U = I` and `ω = 0` exactly (§4).
- **R3 (revised).** **No zero except Γ modulo the reciprocal lattice.**
  The old clause (r8 §2 R3 and §3.4: "no zero at any of the 26 non-Γ special points") cannot be met on a single BCC orbit, because twelve of those labels are Γ itself.
- **R4–R7.** Vacuous. There is no repair parameter to recover from (R4), no added finite-range term (R5), no reordering of ticks (R6), and no parameter to fix before measurement (R7).

The §3.4 acceptance block of r8 (six floors, the π/2 row, the 2.663e−2 rejection and the post-screen note) is not modified. With no repair, the "no worse than the unrepaired rule at the same φ" comparison is the rule against itself and passes trivially. The floor is not re-decided and `φ` is not tuned.

## 4. The 8-point table on the 2π torus

Closed-form values at `m = 0`. At every point with `k_i ∈ {0, π}`, `s_i = 0`, so `n = 0` and `u = c_x c_y c_z = (−1)^{#π}`. The layers collapse: for `u = +1`, `V = 1` and `S = I`, so `U = I` and `ω = 0`. For `u = −1`, `S⁺ = S⁻ = −I` and `X = −τ_x`, so `V⁺ = V⁻ = e^{2iφτ_x}` and `U = e^{4iφτ_x}`; with `e^{−4iω}` as the eigenvalue of `U_k`, `|ω| = dist(φ, (π/2)ℤ)`, which equals `π/2 − φ` for `φ ∈ [π/4, π/2]`. At `φ = 1.4` this is `0.170796326795…`, the value r8 §4 and §8 quote for the corner and the paper's own "corner identity". (Closed-form algebra on the paper's symbol; not a census.)

| # | Point on the 2π torus | Name | Class | u | ω at m = 0 | Sign labels in the 27 |
|---|---|---|---|---|---|---|
| 1 | `(0, 0, 0)` | Γ | Γ-type | +1 | 0 | 1 |
| 2 | `(π, π, 0)` | edge xy | Γ-type, a Γ image | +1 | 0 | 4: `(±π,±π,0)` |
| 3 | `(π, 0, π)` | edge xz | Γ-type, a Γ image | +1 | 0 | 4: `(±π,0,±π)` |
| 4 | `(0, π, π)` | edge yz | Γ-type, a Γ image | +1 | 0 | 4: `(0,±π,±π)` |
| 5 | `(π, 0, 0)` | face x | H-type | −1 | `π/2 − φ` (0.170796 at φ = 1.4) | 2: `(±π,0,0)` |
| 6 | `(0, π, 0)` | face y | H-type | −1 | `π/2 − φ` | 2 |
| 7 | `(0, 0, π)` | face z | H-type | −1 | `π/2 − φ` | 2 |
| 8 | `(π, π, π)` | corner | H-type | −1 | `π/2 − φ` | 8: `(±π,±π,±π)` |

Label count: `1 + 12 + 6 + 8 = 27`. Points 2–4 differ from Γ by the reciprocal-lattice vectors `(π,π,0)`, `(π,0,π)`, `(0,π,π)`: "twelve edge labels" are four sign names for each of three momenta that are Γ images. The three faces and the corner are one H-type class: same `u = −1`, same closed form, same value (r8 §4 gives the corner `0.170796326795 = π/2 − 1.4` from `dirac4s.periodS`; the paper's census finds none of the 6 face labels and none of the 8 corner labels massless).

At `φ = π/2` the H-type value is 0, which is the paper's "0 (doublers return)" row; r8 §3.4 reports that row and does not gate it.

## 5. What is no longer blocked, and what is not

**No longer blocked by the L1.1 repair-or-reason decision (this is a reading, not an approval):**

- The "repair or reason" for the twelve edge zeros is answered by identification: they are Γ on the other tastes, not extra states of one BCC orbit.
- The chain + Wilson `r = 0.05` route (r8 §6 route 3) exists only to lift those three copies. Under this reading it is not needed, and it is not adopted. r8 records that it drops the plain-rule interior gap at `φ = 1.4` from `0.08212694658054251` to `0.026625477907575197` (32% of the §3.4 floor, factor 3.08 below it); that blockage, "a repair that clears §3.4, or a re-decision of the floor", does not arise when no repair is applied. The floor is not re-decided.
- The paper's adopted headline gap `2.663e−2` is the `r = 0.05` number (paper "Doublers and bulk"; r8 §6). It is not claimed by r9. Without `r`, the same paragraph gives `0.034` (smallest doubler gap, `N_s = 16`, `b = 0.2`, global search) and `0.033` for the bulk interior-component gap at `b = 0.2`. These were read from the paper text. They were not re-run, and the paper notes its four global-search values did not evaluate the twelve edge points. On this reading those points are Γ images, so not evaluating them missed no doubler; whether the `0.034` stands is what §6 would census.

**Not settled by r9:**

- The `0.034` and `0.033` values are for the chain (Table `dw`), not for the plain rule whose floor is `0.0821` at `φ = 1.4`. r9 does not say the chain at `r = 0` meets or fails any floor. §6 is the design for finding out.
- The paper text itself still describes the ℤ³ four-taste reading in places (Doublers bullet) and still calls the twelve points "exactly massless" with `r = 0` ("while r = 0 those three distinct momenta … are exactly massless, so none of the four numbers is a global minimum"). r9 does not edit the paper. Aligning that wording is a later paper revision.
- The OP4 local rule's three extra Weyl nodes (plan §3 L1.1, second "Current result") are a different rule, and r9 does not address them.
- L1.4 and L1.5 re-measurement: no repair means the rule is unchanged, so that blocker from r8 §7 does not arise from a repair; no L1.4, L1.5 or other layer is started by r9.

## 6. What still needs a census (design only — not approved, not run)

Re-census the Table `dw` chain at `r = 0` through the official V5 v2 census code (the code that produced `results.json` sha256 `ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708`), with the exclusion balls (`|k| < 0.3`) around **every** Γ image, i.e. Γ and the three edge momenta (and sign images), and report the zone-interior minimum, with argmin in units of π and radians as in r8 §3.2. The census method (search (a), search (b), 64-point Nelder–Mead refinement, per r8 §3.2–3.3) is as r8 states it; no new method is proposed here.

- **Not approved.** Plan §0.2: every run needs Edmond's own approval, with stated caps (memory, CPU seconds, wall time, output size, one attempt, stop on any failed check). No caps are proposed or assumed by r9.
- **Not run.** Nothing in r9 depends on its result.
- The §3.4 floor is not lowered to fit whatever it returns. `φ` is not tuned. A failure is a result and is recorded, not re-run in place (plan §0.1 rules 4 and 7).

## 7. What is not pursued, and why

**The 5-and-3 composition factor `U(P)` is not the L1.1 repair.** Edmond and the previous chat set it aside for this gate.

- `P = (1+x)(1+y)(1+z)/4 − xyz`, `x = cos k_x` and cyclic, is stated by the previous chat to be the unique symmetric multilinear polynomial with the 5-and-3 vertex pattern (not re-derived here). On the four Γ-type points it takes `(+1, −1, −1, −1)`. This is checked directly: Γ gives `8/4 − 1 = +1`; each edge gives `0 − 1 = −1`. That is a taste split, not a BCC-periodic function, since a symbol periodic under the BCC reciprocal lattice takes the same value at Γ and at the three edges.
- Realising `P` needs non-BCC hops (single-axis terms from `cos k_x`), which couple the four orbits and replace "nearest-eight links on a rigid BCC grid" with a different lattice.
- A scratch composition check by the previous chat (`W = U_k U(P)` at `φ = 1.4`, matched gauge and five random SO(5) gauges, 41³ grid) reported the edges at `|ω| = π/4`, Γ at 0, and the interior minimum at about 0.003–0.007 against the 0.0821 floor; Nelder–Mead then found zeros (about 1e−14) at generic interior momenta. That was a scratch script, not the V5 census code; it is not repeated here and nothing is built on it. It is recorded only as the reason the composition route is not a candidate. r8 §6's composition paragraph ("a new direction … does not authorise a run") is not carried into r9.

The rank-3/4/5 Gram identities for `1 − P²` are math results from the other chat; they do not feed this gate and are not reopened.

## 8. A wording inconsistency in the hashed plan, recorded and not fixed

Plan v3.3 r2 is unchanged by r9 (sha256 above). Inside it:

- §2, the V3 status line (line 108), calls the twelve points "Γ images under the even-parity lattice" in the V5 exclusion set.
- §3 L1.1 ("Current result, §6.2 Wilson symbol", line 120; "Decision needed", line 126), §10 (line 388) and the §8 traceability row for OP3 (line 322) still call them "12 exact massless zero modes" / "12 face-centre zeros" needing a repair-or-reason decision.

These do not agree with each other. r9 does not edit the plan or "fix" either side. Aligning those lines is a later plan revision, not part of r9. The plan names the twelve points "face centres"; the paper and r8 name them edges (two components at `±π`). r9 follows r8's naming.

## 9. Provenance and differences from the handoff

- No simulation, census, grid, script or sweep was run for r9. Table §4 is closed-form algebra on the symbol printed in paper §6.2; the repo holds no code and none was executed. The following are read from files and not re-run: `0.08212694658054251` (r8 §3.4), `0.026625477907575197` and `32%`, factor `3.08` (r8 §6 route 3), `0.0821` and `0.0266` (r8), `0.034`, `0.033`, `2.663e−2` (paper, "Doublers and bulk").
- Not re-run and taken from the previous chat: the 432-site numeric check of `e^{iG·x}`; the scratch composition results; the uniqueness of `P`.
- Discrepancy with the handoff, in the files' favour: the closed form for H-type is `dist(φ, (π/2)ℤ)` for general `φ`, equal to `π/2 − φ` on `φ ∈ [π/4, π/2]` (which covers the gated `φ` values 0.8, 1.0, 1.2, 1.4 and 1.5; at the gated `φ = 0.5` it is `0.5`). Handoff quotes `π/2 − φ` at `φ = 1.4`, which agrees with r8 and the paper.
- The paper's Doublers bullet uses the four-taste ℤ³ description for its counts, while its formal update rule defines `ℋ = ℓ²(BCC) ⊗ ℂ⁴`. r9 relies on the latter and does not edit the paper.
- This document carries no hash and is not signed off. Sign-off, if any, is Edmond's and belongs in a sidecar outside the folder, as with r8, so the status line above is not frozen inside a hash.
