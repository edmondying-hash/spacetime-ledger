# L2.0-C5(a): interface audit of every read primitive

Quantized Space-Ledger. Written 13 November 2026 (America/New_York) by `spacetime` (the Grok bot) at Edmond Ying's request (messages of 13 November, asking for the L2.0 design and for this audit to start while B9 waits). This is a read-only audit: no scored run was performed, and no paper, plan or repository file was edited.

**Question.** Residual assumption R-d2 (plan v3.4, gap G-7; fuller argument in `born_fixes/D2_NOTE.md`, sha256 `a799a24ec34bd4103841f60cdfb9429b31a7fd842c9a6ba0df79ecab2191c61e`) says: every read, including one that resolves only the τ factor or only the σ factor, is a unitary of the rule followed by a read of exclusive link channels. C5(a) asks whether each read primitive, in the paper's §5.5 pointer API, in the code that produced the paper's CHSH 2.828 / I₃≈0 / no-signalling numbers, and in the canonical L1 harness, is written that way.

**Verdict, in one line.** No audited primitive is written as rule unitary + exclusive link-channel read. The §5.5 API is a two-outcome attribute read with `cos²` inserted by hand, which is the finding the plan already expected. The 2.828 / I₃≈0 / no-signalling numbers were not produced by a link-channel read of `dirac4` on a pair made by a client-side split. The canonical L1 harness has no client-side outcome-read primitive at all, so R-d2 is not implemented there either.

A primitive is scored "meets R-d2" only if all four hold, with file:line evidence: (1) a unitary of the canonical rule (`dirac4` cycle, 8 corner hops, φ = 1.4) is applied; (2) outcomes are exclusive sets of links or of node components after that unitary; (3) the weight is the conserved charge in those sets, not an inserted `cos²` or a hand-coded `|a|²` of an abstract qubit; (4) the server ledger is left unchanged. Anything else is "does not meet R-d2".

---

## 0. Sources

- **Paper.** `space-ledger-v2.md` on `origin/main` at `7edcdc3a5bc4e566b45cdfb1d88ef8bbdefe0700` (the tip after `git fetch`; the paper bytes are identical to `fdf3e72`), sha256 `ce22701ca6e5e2dfa143ab43a6062e80025c1afeba5137f7e271c239bc75555c`. The stale `/workspace/whitepaper` copy was not read.
- **Plan.** `layered_plan_v3.4.md`, sha256 `a50dd0a0d5c9304e782d8482905167d797f4973106d9a27326c69572a1e846cf`, §4 lines 209–259.
- **Canonical rule module.** Hashed `dirac4.py` used in the L1.2 / L1.3 / L1.5 / L1.4 runs, sha256 `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff` (box copy `/workspace/runs_l12/20261112_l12_7e09b7c4/frozen/f71c782e/dirac4.py`; also copied to `frozen/dirac4.py` in this folder).
- **Code folders on the box, as they stood on 13 November 2026.** Paths below are absolute on the box. Hashes are sha256 of the named file.

---

## 1. Paper §5.5 pointer API

Paper lines 355–363 describe a toy-tested interface, with two numerical CHSH figures that are *not* the §8.1 value 2.828.

**Primitives named in the paper text**

| Primitive | Paper lines | What it does | Meets R-d2? |
|---|---|---|---|
| `a = entangle(x1, x2)` | 357 | Opens one shared server record. Each daughter carries a pointer, and the pump's energy and momentum are split. No outcome is stored. | Not a read. The call does not apply a `dirac4` unitary and does not read links. |
| `read(a, i, basis, setting)` | 357 | "computes the odds and returns ±1"; the client locks that value. A later read on another basis is conditioned on the earlier result. | **No.** Two-outcome attribute read. The paper's own caveat (line 357, last two sentences) says the read uses the `cos²(θ_A − θ_B)` odds by hand, so the interface is consistent but does not derive the Born rule. No rule unitary, no exclusive link channels. |
| `spread(x, version, Δticks)` | 363 | Lazy jump to the state Δt ticks after `entangle()` or the last lock, "like a counter-based random-number generator". Phase drift is proportional to energy times Δt. | Not a read. No `dirac4` hop is performed (the paper compares it with a per-tick update and says the cost stays flat). |
| The "collapse" draw at read time | 363 | "one weighted draw from the odds, using both detectors' settings together; it never looks up a stored value." | **No.** Same hand-coded odds. An energy–time (Franson-type) variant "follows `cos²(Δφ/2)`" (line 363), also inserted. |

**Code that produced the §5.5 numbers**

The line-357 figures match `/workspace/entangle_spdc/sim.py` (sha256 `8fb1ed1f94535bfde3e0642c9da646f116e72232819a5dc12c4e5289151cf110`) and `results.json` / `log.txt` in that folder, one for one:

- Shared record, 40,000 pairs per setting, seed 1: S = 2.82245 ± 0.00709, written in the paper as 2.822 ± 0.007.
- Copied-record control: S = 0.01275 ± 0.010, written as 0.01 ± 0.01.
- 80% efficiency and 1% dark counts: S = 2.7998 ± 0.0089, written as 2.800 ± 0.009.
- Basis-switch correlation: 0.00375 ± 0.005, written as 0.003 ± 0.005.
- No-signalling z on A's marginal, all well under 2σ (largest \|z\| in the `v1` run is 0.42).

Evidence that this `read` is not R-d2:

- `entangle` (lines 6–10) writes a record with members, a split of pump energy and momentum, and an empty `locked` map. It does not call `dirac4`.
- `probability` (lines 11–14) returns `None` on a first read (then 50/50) and `np.cos(th-thj)**2` once the partner has locked. That is the inserted `cos²`.
- `read` (lines 20–26) draws ±1 from that probability and calls `decohere` (lines 15–19), which stores the lock and drops other bases. No link, no component mask, no conserved charge.
- `transport` (lines 27–30) is a classical hop of a pointer payload along `sign(k)` and is used only every 500 shots; it does not evolve a 4-component BCC amplitude.

The line-363 lazy / Franson figures match `/workspace/entangle_spdc/v11/v11.py` (sha256 `33c57416dcc145ffc5ebe30678239f6803969602cfa1b1d3d433bfa726503ff7`):

- `odds` (lines 17–22) sets the four joint weights to `(1 ± cos 2(θ_A−θ_B))/4` for polarisation and `(1 ± cos(θ_A+θ_B))/4` for Franson. Those are `cos²` weights.
- `collapse` (lines 24–32) draws once from those weights with a Philox counter RNG.
- Reported: polarisation lazy S = 2.837 ± 0.010 (paper: 2.837 ± 0.010); Franson S = 2.821 ± 0.010 (paper: 2.821 ± 0.010); phase difference lazy vs per-tick 3.6×10⁻¹³ rad in the paper, `phase_maxdiff` in the code's `results.json`.

**Finding.** Every §5.5 read primitive fails R-d2. This is the finding the plan (line 251) and `D2_NOTE.md` (section 5) already expected: the API is justified only as shorthand for a link-channel read, and as written it is a two-dimensional primitive with `cos²` inserted. These CHSH numbers therefore do not count for L2.1 either (L2.1 forbids a coded `cos²` and requires an energy-share read of conserved link charge).

---

## 2. Code that produced the paper's §8.1 numbers (CHSH 2.828, I₃≈0, no signalling)

Paper line 1269 (and the same claim at lines 145, 1341, 1347): "the toy runs give CHSH = 2.828, three-slit I₃ ≈ 0, 50/50 splits and no signaling, with no cos² or Born weight coded in." Reading by \|amp\| or amp⁴ "fails (CHSH 1.66 and 3.77, and it signals)." "The entangled pair is made on the client side, as a crystal splits a photon." A "small tensor-network ledger (3×3 PEPS, exact contraction)" is said to give the same results, "even with an unequal entangled pair, though there the square enters through the read rather than emerging from it."

Two box folders produce those numbers. Neither uses `dirac4`.

### 2.1 `born3` — energy-share on a hand-inserted singlet, and a BCC three-slit

Folder `/workspace/born3/`. Main file `born3.py`, sha256 `821d92bdb202b2f99869e1bdf00872ad39abdeb6cac2ddc2afc4f95ec0fbd801`. Controls `controls.py`, sha256 `a813bb6462dc488d212ee5eb635ab4394e2d7ef182f2b2674f91361857678b9c`. Rule imported from `/workspace/qca/bcc.py` (sha256 `2ec73dcbd16145d33c9947cafeb9f7976b65ea8ae9c941a9210fd7b97cb20af8`), the D'Ariano–Perinotti Dirac automaton, m = 0.3, 16³ grid, 4 components per node. This is the older rule named in the plan as a seed, not the canonical `dirac4` rule.

**What uses the BCC rule, and what does not.**

- Check 1, conservation of Σ\|a\|^p (lines 19–25 of `born3.py`): the BCC `step` (lines 15–16) is applied for 300 ticks. Σ\|a\|² drifts 5.57×10⁻¹⁴; Σ\|a\| grows by a factor 22; Σ\|a\|⁴ falls 99.7%. This is the "6×10⁻¹⁴ over 300 ticks" cited in the paper and in plan C1. **Not a client read.**
- Check 3, fine-graining (lines 44–57): two packets are split by the same `step`. Branch weight at q = 2 stays at 2/3; q = 1 and q = 4 drift. **Not a client read of exclusive channels in the R-d2 sense**; it is a diagnostic of which p-norm is stable.
- Check 4, Sorkin I₃ (lines 71–84): three slit sources are placed on the 16³ grid, propagated 6 ticks by `step`, and a screen plane is read as Σ\|a\|^q. For q = 2, relative I₃ = 5.00×10⁻¹⁶; for q = 1, 0.329; for q = 4, 0.016 (`results.json`). This is the paper's I₃≈0. The "read" here is a sum of \|a\|^q over a screen plane of nodes and components, i.e. a region sum, but the dynamics are the old rule, and there is no preceding detector-setting unitary of `dirac4`, no lock, and no server/client split. **Does not meet R-d2 as a canonical-rule primitive.** It is a region-sum of the old rule, which is closer in spirit than the CHSH part, and it still is not the canonical harness.
- Check 4, CHSH (lines 58–70): **the BCC `step` is not called.** The entangled pair is a hard-coded singlet, line 61: `singlet=np.array([[0,1],[-1,0]])/np.sqrt(2)`. The pointer is a 2×2 rotation `proj(theta)` (lines 59–60). `read_pair` (lines 62–65) multiplies the singlet by the two rotations, takes `(np.abs(amp)**2).ravel()`, normalises, and samples. Sampled CHSH = 2.82967 at 2×10⁵ shots (`results.json`); the exact q = 2 value in `controls.py` lines 7–14 is 2.8284271247461903 = 2√2. Controls: q = 1 gives 1.6568542494923801; q = 4 gives 3.7712361663282534. No-signalling on a non-maximal state: q = 2 is 2.2×10⁻¹⁶; q = 1 is 0.132; q = 4 is 0.077. Singlet marginals stay at 1/2 for all three q.

**Meets R-d2?** **No**, for the CHSH / no-signalling half that supplies the 2.828 and the 1.66 / 3.77 controls. There is no `dirac4` (and in the CHSH block, no BCC step either), no exclusive link channels, and the pair is inserted, not produced by a split. The weight is the squared modulus of a two-qubit amplitude after a pointer rotation. The authors are careful not to write `cos²` as a formula; the square is still the read, applied to a hand-made singlet. That is why the exact q = 2 value is exactly Tsirelson's 2√2.

`/workspace/entangle_spdc/v2/sim.py` (sha256 `66230eb9793ce23468d7a870967d7d9deb409e1c45817f9006c0036b828d601f`) is an earlier OP27/OP1 attempt. Its VERDICT records that a linear threshold gives S = 1.66, and that getting `cos²` required thresholding \|proj\|², "the square is inserted (S=2.825)". It is not the §8.1 source, and it does not meet R-d2.

`/workspace/born5/born5.py` and `born5b.py` fit a free weight under additivity and then apply it to CHSH (2.827 / 2.8278). They are plan seeds for the Gleason-style route (G-3), not the source of the paper's 2.828 sentence. The weight is a function of \|a\| on abstract pieces, not a link-channel read of `dirac4`. **Does not meet R-d2.**

`/workspace/born4/` and `/workspace/born6/` are the Zurek equal-piece route, both recorded as FAIL in their VERDICT files, and they do not supply the paper's 2.828.

### 2.2 `tn` — 3×3 PEPS, double-layer read

Folder `/workspace/tn/`. `tn.py` sha256 `180edb8217552bc66cd1b838411ee55d1c31ac0b774fe8f6126b0c8e4136d2b5`; `tn_controls.py` sha256 `7e748d20549f599cf7b7022d52f44f7896034a6c7c9e30fb0618d7ab4171ce94`. This is the "small tensor-network ledger" of paper line 1269.

- The pair is made by hand: a Hadamard + CNOT Bell pair at one corner (lines 14 of `tn.py`), shipped along a SWAP chain (lines 15–16), then multiplied by `[[0,1],[-1,0]]` on B "to make it singlet-like" (line 17). The SUMMARY says the pair is "a server-side event set up by hand". A non-maximal `cos 0.4 / sin 0.4` pair is used in `tn_controls.py` for the no-signalling check.
- The node rule is the decoh2 qubit gate, not `dirac4` (VERDICT.md: "The 4-component BCC Dirac rule is represented here by the decoh2 qubit node gate, not by its own tensor").
- `read_double` (lines 24–29) projects A and B, contracts ket against bra, and divides by ⟨ψ\|ψ⟩. That contraction *is* Σ\|a\|². `tn_controls.py` `read_q` (lines 44–48) generalises it to Σ\|amp\|^q. Results: q = 2 gives CHSH 2.8284, I₃ 9×10⁻¹⁷, no-signalling 2×10⁻¹⁶; q = 1 gives 1.657 and signals (0.096 on the non-maximal pair); q = 4 gives 3.771 and signals (0.076).

**Meets R-d2?** **No.** The square enters through the double-layer read, as the paper itself says. There is no `dirac4` unitary, no exclusive BCC link channels, and the pair is inserted.

### 2.3 Related paper read-out: §3.3 table (not the 2.828 sentence)

`/workspace/readout/sim.py` (sha256 `d9d1ebf307c651bb93d862b72f3c7bb197e1ca2e1c9cb6af6584b067f8bad27f`) and `ext.py` produce Table `tab:readout` and Figures `fig:readout` / `fig:readoutexp` of paper §3.3 (the Fraunhofer slits, detector-merging, and an entangled-pair signalling check). Amplitudes are a continuous Fraunhofer formula (`amp`, line 5). The read-out is a pointwise rule `f(|a|)` on the screen, then a normalisation (lines 17–19). No lattice, no `dirac4`, no link channels. Plan C4 cites this table as an illustrative seed, not as a canonical-rule result. **Does not meet R-d2.**

---

## 3. Canonical L1 harness

The hashed `dirac4` modules and the L1.2, L1.3 / L1.3b, L1.4 and L1.5 measurement code live in the sealed run folders. They were read in place. Representative files:

- L1.2: `/workspace/runs_l12/20261112_l12_7e09b7c4/harness/l12.py`, frozen `dirac4.py` as above.
- L1.3: `/workspace/runs_l13/20261112_l13_9ccf4855/harness/l13_primary.py`.
- L1.4 r4: `/workspace/runs_l14/20261113_l14r4_ee137a27/harness/l14_measure.py`.
- L1.5 joint: the same L1.4 folder's `l15ab_measure.py` (also used in `runs_l15/20261112_l15ab_865660ec_56a19950/`). Real-space hop form: `HopCycle`, `apply_op`, `build_packet`, `norm2`, `centroid` at `l15ab_measure.py` lines 225–348.

**What these harnesses "measure".** Eigenvalues and eigenphases of the cycle symbol `U_k`, group and phase speeds, packet centroids, Σ\|a\|² as a unitarity / norm check (`norm2`, line 347–348 of `l15ab_measure.py`), and (in L1.5) a positive-frequency projector on the 4×4 symbol (`pos_projector`, lines 293–297). `meter.py` in each run folder is a process timer (wall, CPU, peak RSS); it is not a client read.

**Is there a client-side outcome-read primitive?** No. Nothing in these files samples an exclusive set of links, locks a client record, or returns ±1 / a detector click. The word `measure` in `measure_v0` (L1.3) and in `l15ab_measure.py` means "compute a spectral or packet observable of the rule", not "read a client outcome".

**Meets R-d2?** **Not implemented.** There is no counter-example two-outcome primitive in the canonical harness, and there is also no implementation of rule unitary + exclusive link-channel read that C5(b)–(d) could already call. R-d2 is an assumption about reads; the L1 harness never reads in that sense. C5(a) therefore cannot pass on the canonical harness as it stands: the required interface is absent, not merely mis-written. The design in this folder proposes a new L2.0 harness (`l20_measure.py`) that would implement that interface for C2–C5; that code is not yet a sealed L1 artefact and has not been scored.

---

## 4. Would the paper's CHSH 2.828 count for L2.1 as written?

Plan v3.4, lines 257–259: L2.1 is a reproduction test of S7, not a test of S1. It assumes the energy-share read. What is missing, the plan says, is "a harness that makes the claim auditable: the read must use only the conserved link charge, and the entangled pair must be produced by a client-side split, not inserted." Pass: S = 2.828 ± 0.005, \|κ\| < 1e−3, marginal shift < 2σ; controls \|a\| and \|a\|⁴ must fail (S ≈ 1.66, 3.77). Entry gate: L1 exit (may run in parallel with L2.0).

**No, the existing 2.828 figure would not count for L2.1 as written.** Reasons, each sufficient:

1. **The pair is inserted, not produced by a client-side split.** `born3.py` line 61 hard-codes a singlet; `tn.py` lines 14–17 build a Bell pair with qubit gates and then rotate it. The paper itself (lines 1269, 1341) records this. The comparison to "a crystal splits a photon" is an analogy, not a ledger split of a `dirac4` excitation.
2. **The read is not a conserved link charge of the canonical rule.** The CHSH block of `born3` never calls the BCC step. The TN read is a double-layer contraction of decoh2 qubit tensors. Neither uses hashed `dirac4`.
3. **The rule is not the canonical one.** Conservation and I₃ in `born3` use `/workspace/qca/bcc.py`. The plan already labels those seeds "old rule, not the canonical one".
4. The §5.5 figures (2.822, 2.837, 2.821) are a different test and have `cos²` coded, which L2.1 explicitly does not allow.

What the existing runs do show, and what L2.1 can reuse as a target rather than as evidence: once a weight Σ\|a\|² is applied to a singlet (or a non-maximal pair) in a 2-qubit pointer basis, one gets 2√2, I₃ = 0 and no signalling, and the p = 1 and p = 4 weights give 1.657 and 3.771 and can signal. That is the quantum-mechanical consistency the plan wants reproduced, on `dirac4`, with a link-channel energy-share read, and with a pair that is actually split rather than inserted.

---

## 5. Summary table

| Primitive or code | Location | Kind of read | Rule | Pair / state | Weight | Meets R-d2? |
|---|---|---|---|---|---|---|
| `read(a, i, basis, setting)` | paper §5.5 line 357; `entangle_spdc/sim.py` 20–26 | two-outcome attribute, ±1 | none | `entangle()` split of a classical pump record | `cos²(θ_A−θ_B)` by hand (line 14) | No |
| lazy / Franson collapse | paper §5.5 line 363; `entangle_spdc/v11/v11.py` 17–32 | joint four-outcome draw | none | `Record` at read time | `cos 2Δθ` / `cos(θ_A+θ_B)` by hand | No |
| `born3` CHSH / no-signalling | `born3/born3.py` 58–70; `controls.py` 5–14 | 2-qubit pointer, four joint outcomes | not used in this block | hard-coded singlet, line 61 | \|amp\|² of the rotated singlet (q = 1, 4 controls) | No |
| `born3` three-slit I₃ | `born3/born3.py` 71–84 | region sum on a screen plane | old BCC `bcc.py`, m = 0.3 | three on-site sources | Σ\|a\|^q on the plane | No (old rule; no lock; no `dirac4`) |
| `tn` double-layer / `read_q` | `tn/tn.py` 24–29; `tn_controls.py` 44–48 | projected contraction | decoh2 qubit gate, 3×3 PEPS | Bell pair inserted, then shipped | Σ\|amp\|^q, q = 2 is ket·bra | No |
| §3.3 Fraunhofer table | `readout/sim.py` 17–19, 52–60 | pointwise screen rule | continuous Fraunhofer, no lattice | illustrative slits / a 2-qubit example | \|a\|^p, softmax, exponential | No |
| L1.2 / L1.3 / L1.4 / L1.5 harness | `runs_l12`, `runs_l13`, `runs_l14` `harness/*.py` | no client outcome-read | hashed `dirac4` | n/a (spectra and packets) | n/a (norm is a unitarity check) | Not implemented |
| `spread`, `entangle`, `transport`, `meter.py` | paper §5.5; `sim.py` 6–10, 27–30; L1 `meter.py` | not a read | — | — | — | n/a |

C5(a), as the plan wrote it, does not pass. The honest residue is the one already named: R-d2 remains an assumption that S1 must carry unless the §5.5 API is restated as shorthand and a link-channel interface is implemented on `dirac4`. Whether to restate §5.5, and whether C5(b)–(d) still run as labelled measurements of a new interface, are open decisions in `L2_0_OPEN_DECISIONS.md` (items D2 and D10). This audit does not decide them.
