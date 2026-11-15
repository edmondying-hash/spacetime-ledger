# L2.0 run design: S1 derivation attempt, C1–C5 on `dirac4` (one BCC orbit, φ = 1.4)

Quantized Space-Ledger. Written 13 November 2026 (America/New_York) by `spacetime` (the Grok bot) at Edmond Ying's request (13 November: write the L2.0 design and start the read-only C5(a) audit while B9 waits on the K1–K3 calls). This document is a design for Edmond's review. It scores no check, and it edits no paper, plan, repository, Sheet or archived record. Nothing in it may be run as a scored check until Edmond names its sha256 in his own words. Open decisions are numbered D1–D16 and listed in the sidecar `L2_0_OPEN_DECISIONS.md` in this folder; this document decides none of them. Where a default is written below, it is a proposal that applies only if Edmond gives no other value.

C5(a) is the read-only interface audit in `L2_0_C5A_AUDIT.md` in this folder. It is part of this design drop and does not wait on a scored run.

## 0. Sources

All hashes are sha256.

- **Paper.** `space-ledger-v2.md` on `origin/main` at `7edcdc3a5bc4e566b45cdfb1d88ef8bbdefe0700` (fetched 13 November 2026; paper bytes identical to `fdf3e72a958bdc0e3ed95f06530b0a96d0a45d61`), sha256 `ce22701ca6e5e2dfa143ab43a6062e80025c1afeba5137f7e271c239bc75555c`. Sections used: 3.3 (read-out postulate and the "Why the Read-out Is the Square" table), 5.5 (pointer API), 6.2 (four-component rule), 8.1 (Born-rule tests). The stale `/workspace/whitepaper` copy was not read.
- **Plan.** `layered_plan_v3.4.md` (plan v3.4 folder on the same `origin/main`), sha256 `a50dd0a0d5c9304e782d8482905167d797f4973106d9a27326c69572a1e846cf`, §4 lines 209–259 (L2.0 and the L2.1 sentence that defines what would later count).
- **R-d2 note.** `/workspace/layered_open_problems_20261109/born_fixes/D2_NOTE.md`, sha256 `a799a24ec34bd4103841f60cdfb9429b31a7fd842c9a6ba0df79ecab2191c61e`.
- **Canonical rule.** Frozen `dirac4.py` of the L1.2 / L1.3 / L1.5 / L1.4 runs, sha256 `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff`, copied to `frozen/dirac4.py` in this folder (byte-identical to `/workspace/runs_l12/20261112_l12_7e09b7c4/frozen/f71c782e/dirac4.py`). Cycle `U_k = V^- S^- V^+ S^+`, 8 corner hops `h = (±1,±1,±1)` in units of a/2, k in radians per a/2, default φ = 1.4, m = 0, Wilson layer on, Wilson mass 0, no face-centre patch. The older D'Ariano–Perinotti module `/workspace/qca/bcc.py` is a seed only and is not used for any C1–C5 procedure.
- **Seeds of the argument, old rule.** `/workspace/born3`, `/workspace/born4`, `/workspace/born5`, `/workspace/born6`, `/workspace/tn`, `/workspace/entangle_spdc`, `/workspace/readout`. Their hashes and the C5(a) line evidence are in the audit. They do not gate this design.
- **Unscored timing probe.** `L2_0_PROBE_TIMING.json` in this folder, produced by `l20_measure.py --probe` on the agent's box at 15:30:09 EST on 13 November 2026. Peak RSS 91 MiB, 11.4 s wall, 21.4 s CPU. No number in that file is a C1–C5 result; cost figures in §8 are taken from it.

## 1. What L2.0 is, and what it is not

Plan line 211: L2.0 comes first inside Layer 2. L2.1–L2.2 assume the energy-share read and do not test S1.

The circularity trap is stated first (plan line 219). If "energy" is defined as \|a\|², then "read by energy share" is the Born rule with extra steps. L2.0 takes the conservation route: (a) Q = Σ\|a\|² is the charge the dynamics conserves, a property of the rule; (b) a read must not bias where that charge sits, a stated postulate (i), in per-channel form (gap G-1).

**Claim (plan Step 3).** The only weights satisfying (i) per-channel conservation of Q in expectation, (ii) immediate repeatability (lock), and (iii) additivity over exclusive outcomes, are w_k = Q_k / Q.

If C1–C5 pass and every assumption is listed, S1 is narrowed to postulate (i), or to (i) plus R-d2 if a two-dimensional read primitive is kept. Under neither outcome is S1 recorded as closed. This design does not authorise an L2.1 run, a paper edit, or a change to §5.5.

**Entry.** The plan's L2.0 entry is the L1 exit gate (line 253). L1.1–L1.4 are closed on `main`. L1.5 has been run; B9 and the B_m record are still open decisions of Edmond's. When a scored C1–C5 run may start is open decision D15. C5(a) is already done.

## 2. Setting, rule, and the client record

**Lattice and rule.** One BCC orbit of an L-cell: the all-even and all-odd integer sites, with hops `h = (±1,±1,±1)` between them. The state is a 4-component amplitude ψ_α(x) ∈ ℂ⁴ at each occupied site, in the frozen module's ordering (R, L) ⊗ (σ). One *cycle* is the paper's U_k at every k, applied as a Fourier multiplier (equivalently the real-space hop form of the L1.5 harness, which that harness already compared with `U_k`). Default L, m, φ, Wilson flags and congestion are D6, D5, D9, D1.

**Channels.** A detector setting is a unitary U_det, then a partition of the (site, component) pairs after that unitary into exclusive sets k = 1…K, and possibly an unassigned remainder R. Q_k = Σ_{i ∈ k} |a_i|², Q = Σ_k Q_k, Q_R = Σ_{i ∈ R} |a_i|². A cell is UNINFORMATIVE if Q_R / (Q + Q_R) > 10⁻⁶, or if two channels share a pair, or if Q < 10⁻¹².

**A read (default D3).** The server array is never written by a read. The client holds a copy. With weight w_k the client is told "k" and its copy is replaced by the channel-k content carrying the full charge Q (the lock). A Q-share read uses w_k = Q_k / Q. Controls use w_k ∝ Σ_{i ∈ k} |a_i|^p for p = 1 and p = 4, and the d = 2 controls of C5(d).

**Server identity.** After every read, the server array is bit-identical to its pre-read bytes (C3). Any difference is a fail, not UNINFORMATIVE.

## 3. C5(a) — already performed, read only

See `L2_0_C5A_AUDIT.md`. Short statement, not a substitute for the audit:

- Paper §5.5 `read(a, i, basis, setting)` and the lazy / Franson collapse use `cos²` by hand. They do not meet R-d2. The numerical figures 2.822 ± 0.007, 2.837 ± 0.010 and 2.821 ± 0.010 come from `/workspace/entangle_spdc/sim.py` and `v11/v11.py` and are a different test from §8.1.
- The paper's §8.1 figures CHSH = 2.828, I₃ ≈ 0, no signalling, and the 1.66 / 3.77 controls, come from `/workspace/born3` and `/workspace/tn`. In `born3` the CHSH block never calls the BCC step: a singlet is inserted at line 61 and the weight is \|amp\|² of a 2-qubit pointer. In `tn` a Bell pair is inserted and the square enters as a double-layer contraction of decoh2 qubit tensors. Neither uses hashed `dirac4`. Those figures would not count for L2.1 as written.
- The canonical L1 harness has no client-side outcome-read primitive. R-d2 is not implemented there.

C5(a), as the plan wrote the gate, does not pass. How that interacts with C5(b)–(d) and with the L2.0 exit is D10 (default: record the finding; still run (b)–(d) as labelled measurements of the new interface; do not treat C5 as passed while §5.5 stays a two-outcome primitive).

## 4. Pre-flight S0 (not a physics gate)

Before C1–C5, in the same run folder:

- **P0.** sha256 of `frozen/dirac4.py` equals `f71c782e…8aff`; sha256 of `L2_0_RUN_DESIGN.md`, `l20_measure.py` and this folder's `SHA256SUMS` match the values Edmond named; `L20_SCORE=1` is set only after that naming.
- **P1.** `U_cycle(k)` is unitary to 10⁻¹⁴ on a 64-point k-set including 0, the axis mid-points and 32 random points (the unscored probe saw 1.25×10⁻¹⁵ on 35 points; that number is not reused as a result).
- **P2.** A plane-wave on the L-cell, evolved one cycle by the FFT stepper, agrees with `U_cycle(k)` to 10⁻¹² (the same check the L1.5 hop form used).
- **P3.** The orbit mask is preserved: mixed-parity sites stay at amplitude 0 to 10⁻¹⁴ after 10 cycles.
- **P4.** Resource meter on, one thread, the caps of §8 installed. Threads pinned to 1.

If any of P0–P4 fails, the run stops and no physics check is scored.

## 5. Check C1 — only Q is conserved among \|a\|^p, plus a local-density search

**What it tests.** Plan Step 1 and gap G-2, on the canonical rule.

### 5.1 p-norm drift

**Procedure.** For each of the five seeds (D12) and each of three states — (S1) a normalised Gaussian packet of width 2.0 at the cell centre with a random internal spinor; (S2) a Haar-random state on the orbit; (S3) two packets of width 2.0, centres separated by L/2 along x, equal charge, a relative phase 0.7 — evolve 1,000 full cycles (D13) with the FFT stepper at L = 16 (D6). Record Σ\|a\|^p at every cycle for p ∈ {0.5, 1, 1.5, 2, 2.5, 3, 4}. Relative drift of a series h is max_t |h_t / h_0 − 1|.

**Pass.** On every (seed, S1 or S2) cell, the p = 2 drift is ≤ 10⁻¹² and each of the six other p drifts by more than 10⁻³. S3 is recorded; it must meet the same p = 2 bound; if a p ≠ 2 on S3 drifts by ≤ 10⁻³ the cell is reported and does not by itself fail the check (two coherent packets can make a single p accidentally quiet).

**Fail.** Any (seed, S1 or S2) cell with p = 2 drift > 10⁻¹², or with some p ≠ 2 drifting by ≤ 10⁻³.

**UNINFORMATIVE.** If p = 2 already drifts by > 10⁻¹² at cycle 1 (stepper fault), stop and do not score C1. If more than 10⁻⁶ of Q on S1 or S3 sits within two hops of the periodic edge at any recorded cycle, rerun that state at L = 32 once, inside the cap; if it still wraps, that state is UNINFORMATIVE and S1/S2 at L = 16 still gate.

A labelled diagnostic at m = 0.3 (D5) and a uniform-load ON diagnostic (D1) are recorded on one seed, one state S1, and do not gate.

### 5.2 Local positive quadratic densities on a node plus its 8 neighbours

**Search space, stated concretely.** Let N(x) be x together with its 8 corner neighbours x + h, h ∈ {(±1,±1,±1)}. A translation-invariant quadratic density supported on that stencil is

ρ(x) = Ψ(x)† K Ψ(x),

where Ψ(x) is the 36-component vector of amplitudes (4 components on each of the 9 sites) and K is a 36×36 Hermitian matrix. The total charge Q_K = Σ_x ρ(x) is a translation-invariant quadratic form whose kernel M(h) is a 4×4 matrix for each displacement h in the 35-element difference set

D = { y − z : y, z ∈ {0} ∪ {(±1,±1,±1)} }

= {0} ∪ 8 corners ∪ the 6 axis vectors ±2 e_i ∪ the 12 face-diagonal vectors of length 2√2 ∪ the 8 body-diagonal vectors ±(2,2,2) (all sign combinations). That set has 35 elements; a Hermitian form is then described by a Hermitian M(0) (16 real parameters) and a general complex 4×4 M(h) for one representative of each pair {h, −h} (17 pairs, 32 real parameters each), **560 real parameters** in all. In Fourier space,

m(k) = Σ_{h ∈ D} M(h) e^{i k · h},    m(k)† = m(k),

and Q_K = Σ_k ψ̃(k)† m(k) ψ̃(k).

**Conservation condition.** The cycle acts as ψ̃(k) ↦ U_k ψ̃(k). Q_K is conserved for every state if and only if

U_k† m(k) U_k = m(k)    for every k,

i.e. m(k) lies in the commutant of U_k, and m is a trigonometric polynomial of the range D. This is a linear condition on the 560 parameters.

**Method.** Build the real constraint matrix A whose action on the 560-vector of parameters is the 16 real components of U_k† m(k) U_k − m(k) at each k of the official grid (D14: 12³ = 1,728 points, plus the origin and the six axis mid-points). Compute the SVD. The numerical nullspace is the right singular vectors whose singular values are < 10⁻⁸. Record the full singular-value list (min, max, and every value below 10⁻⁴).

**Positivity.** For each nullspace basis vector, evaluate the lowest eigenvalue of m(k) on the official k-grid and on a finer 16³ diagnostic grid. A ray is *positive* if that lowest eigenvalue is ≥ −10⁻¹⁰ after a choice of overall sign and after discarding the zero vector. Independently, try to realise the same total form by some K >= 0 (positive semidefinite) on the 36×36 stencil (a small semidefinite feasibility problem; if the solver is inconclusive, report it and fall back to the m(k) >= 0 (positive semidefinite) test, labelled as such). The \|a\|² charge is the ray m(k) = c I_4, c > 0. It must appear in the nullspace; if it does not, stop, harness fault, do not score.

A nested on-site-only search (M(h) = 0 for h ≠ 0; 16 real parameters) is reported alongside.

**Pass.** The only positive local conserved densities found in the 560-parameter search (and in the on-site nested search) are the multiples c Σ\|a\|² with c > 0. Any other nullspace vectors are recorded (dimension, a basis, a short description: for example a current or a signed component charge) and, if they are not positive, they do not fail the check (D11).

**Fail.** Any other positive local conserved density; or the identity ray absent from the nullspace after a successful SVD (that last case is a harness fault if it comes with a grey-value warning, see below).

**UNINFORMATIVE.** One or more singular values in the grey interval [10⁻⁸, 10⁻⁴) (D11). In that case the search is not scored; the p-norm half of C1 may still be scored, and is reported separately.

**Controls.** (1) The identity parameter vector lies in the numerical nullspace to 10⁻¹⁰ in residual. (2) A deliberately non-conserved on-site matrix, σ_z on the spin factor, has a residual of at least 10^{-3} at some official k (if this control is not rejected, UNINFORMATIVE). (3) The same search run on a 6³ and an 8³ grid must give the same clear nullspace dimension as 12³, or the cell is UNINFORMATIVE.

## 6. Check C2 — per-channel martingale (i)

**What it tests.** Postulate (i) per channel, and that the \|a\| and \|a\|⁴ controls are biased.

**Procedure.** L = 16. For each of the five seeds and each of five prepared states (two localized packets of different internal spinors; a two-region split with charges 2/3 and 1/3; a four-region equal split; a random-orbit state coarse-grained into four spatial quadrants), apply a detector-setting unitary that is the identity (the regions are already exclusive spatial sets of the orbit) and read with three weight rules: Q-share (p = 2), p = 1, and p = 4. Take ≥ 10⁵ shots per (seed, state, rule), vectorised. For each shot, form the client's locked copy, compute Q_j^{after} on that copy (which is Q if the outcome was j and 0 otherwise), and estimate E[Q_j after] − Q_j^{before} for every channel j, with a 3σ interval from the binomial (or multinomial) shot noise. Repeat the same reads after the *unread server* state has been evolved a further 0, 10 and 100 cycles; the Q_j against which the martingale is tested are those of the state at the read time, not of the t = 0 state.

**Pass.** For the Q-share rule, E[Q_j after] − Q_j is consistent with 0 within 3σ for every channel, every official state, every seed, and every evolution time 0, 10, 100. For the p = 1 and p = 4 rules, at least one channel on each of the unequal-charge states (the 2/3–1/3 split, and any state whose Q_k are not all equal) shows a per-channel bias at > 5σ, at evolution time 0.

**Fail.** A Q-share bias beyond 3σ on any official cell, or a control rule that does not show a > 5σ bias on the unequal-charge states.

**UNINFORMATIVE.** A channel with Q_k < 10⁻¹² is dropped; if that leaves fewer than two channels, the state is UNINFORMATIVE. If fewer than 10⁵ shots are completed, UNINFORMATIVE.

## 7. Check C3 — lock and repeatability (ii), and the server unchanged

**What it tests.** Plan (ii) and gap G-5, plus the paper's "a read does not alter the server ledger."

**Procedure.** The same states and seeds as C2, Q-share only, ≥ 10⁵ shots. After each shot: (1) an immediate second read of the same client copy, with no intervening cycle, must return the same k; (2) a second client that is given the same post-lock copy, and that reads immediately, must return the same k; (3) the server array's bytes are compared with a pre-read snapshot (`numpy.array_equal` on the complex view, or equivalent sha256 of the raw buffer) and must match.

**Pass.** Zero disagreements in (1) and (2) over all official shots, and zero server-byte differences in (3).

**Fail.** Any disagreement, or any change to the server state.

**UNINFORMATIVE.** Same shot-floor and empty-channel rule as C2. A state that is UNINFORMATIVE in C2 is skipped here.

## 8. Check C4 — detector merging (iii)

**What it tests.** Plan (iii), on link (site/component) channels of the canonical rule. The paper §3.3 table is an illustrative seed only, not a target.

**Procedure.** L = 16, five seeds, three official partitions of the orbit into four exclusive spatial channels {A, B, C, D} (quadrants; four slabs along x; a 2×2 chequer of period L/2). For each partition, prepare a state with four unequal charges (the first four seeds' random-orbit states, projected and renormalised onto the four channels with weights 0.4, 0.3, 0.2, 0.1, plus a fifth residual packet state). Read with p = 2, 1 and 4, ≥ 10⁵ shots. Then merge B and C into one channel and repeat the read, without touching A or D.

**Pass.** For p = 2, every unmerged outcome's weight is unchanged within 3σ, and w_{B ∪ C} = w_B + w_C within 3σ, on every official partition and seed. For p = 1 and p = 4, the unmerged weight of A (or of D) shifts by > 5σ on at least one official partition, or, if a given p happens not to shift A on a symmetric partition, it shifts on the unequal 0.4/0.3/0.2/0.1 state at > 5σ.

**Fail.** A Q-share shift beyond 3σ, a Q-share failure of additivity, or both controls failing to shift at > 5σ on the unequal-charge state.

**UNINFORMATIVE.** As in C2; also if a merge leaves Q_R / Q > 10⁻⁶.

## 9. Check C5(b)–(d) — factor reads through links

**What it tests.** R-d2 in operation, gap G-7, on a new interface (the L1 harness has none; see C5(a)). C5(a) itself is the audit, already done. These parts use the factor-dependent hop of D4 (default: discrete Stern–Gerlach embedding).

**Geometry (tightened after the unscored probe).** The probe's mid-plane split at L = 16, d = 4, left a mid-plane charge of order 10⁻¹ on a mix of states that included a delocalized random field, so that split is not used as a gate geometry. Official geometry: L = 32, packet width 1.5, shift d = 8 along the nearest coordinate axis to n. After the hop, the two channels are the Voronoi cells of the two image centres (the original centre displaced by ±d ê_axis), inside the minimum-image convention; a mid-band of half-width 1 is unassigned. A cell with unassigned charge > 10⁻⁶ is UNINFORMATIVE and is retried once at L = 64, d = 16, inside the cap.

**States (five, all localized; the plan's "entangled τ–σ–position" is S5).** All centred on the L-cell, width 1.5, unless a second centre is named:

- S1. Internal spinor (1,0,0,0): τ = R, σ = ↑.
- S2. Equal superposition of σ at τ = R: (1, 1, 0, 0)/√2.
- S3. A τ–σ Bell spinor on one packet: (1, 0, 0, 1)/√2.
- S4. A random normalised spinor (seeded) on one packet.
- S5. Two packets, centres separated by 16 along y, spinors (1,0,0,0) and (0,0,0,1); this is a τ–σ–position entangled state. Channels are the unions of the Voronoi cells of each packet's two images.

**Directions.** 50 Fibonacci-sphere points, the same construction the probe used (golden-angle, i = 0…49), plus the six axis unit vectors for reporting, 56 in all; the official count for the gate is the 50 sphere points. Both σ-only and τ-only hops are run.

**C5(b).** For each (state, direction, factor, seed), apply the hop, drop UNINFORMATIVE cells, then take ≥ 10⁵ Q-share shots of the two spatial channels. Compare w_n with ⟨Π_n⟩ of the *pre-hop* state, where Π_n = 1_{orbit} ⊗ 1_{unread factor} ⊗ P_n. Pass: |w_n − ⟨Π_n⟩| ≤ 3σ on every official scored cell, five seeds. Fail: any official cell outside 3σ.

**C5(c).** For at least three fine-grainings {Π_j} that commute with 1 ⊗ P_n — (1) two position half-spaces perpendicular to a second axis; (2) four position quadrants; (3) a further split of the unread factor (τ if the read is σ, and vice versa) — check w(1 ⊗ P_n) = Σ_j w(Π_j ⊗ P_n) within 3σ, on S2, S3 and S5, 20 of the 50 directions (even index), five seeds, ≥ 10⁵ shots. Pass: every official cell within 3σ. Fail: any official cell outside 3σ.

**C5(d).** Repeat C5(c) and C2's per-channel drift, on S2 and S3, with the read rule replaced by g₃(n) = [1 + (n · r)³]/2 (r the Bloch vector of the reduced factor state) and by the per-pair-normalised g_p, p = 1 and 4. Pass: each of those three controls is rejected at > 5σ by C5(c)'s embedding identity or by C2's per-channel drift, on at least one official state and one direction, and consistently (not a single-shot fluctuation) over the five seeds. Fail: a control that is not rejected.

**UNINFORMATIVE.** Geometry as above; empty channels; fewer than 10⁵ shots; a fine-graining whose unassigned charge exceeds 10⁻⁶.

## 10. Seeds, recording, and UNINFORMATIVE (common rules)

- Seeds: D12, default 20261113–20261117.
- Every check writes a JSON result with the seed, L, m, φ, load label, the raw totals needed to recompute the quoted drifts and σ intervals, wall s, CPU s, peak RSS, and the sha256 of `dirac4.py` and of `l20_measure.py`.
- A resource meter in the same style as the L1 `meter.py` (wall, CPU self+children, peak tree RSS sampled at 0.2 s, exit code) wraps each check. One thread, no GPU.
- UNINFORMATIVE cells are named, not silently dropped. A check whose official cells are all UNINFORMATIVE is itself UNINFORMATIVE and is not a pass.
- No output of `l20_measure.py --probe` is a result. The scored path runs only with `L20_SCORE=1` after the design hash is named.

## 11. Caps, machine, and cost (from the unscored probe)

**Machine.** D7: the agent's box by default; sparky allowed; `bigbang` is not used.

**Proposed caps (D8).** 1 thread, no GPU, 512 MiB peak RSS, 10 min wall for S0 and for each of C1–C4, 15 min for C5, 40 min total wall, 64 MiB output, one attempt per check (the D6 / C5 geometry retry at a larger L counts as the same attempt).

**Probe, disclosed (box, 13 November 2026, 3:30 PM America/New_York).** File `L2_0_PROBE_TIMING.json`. Peak RSS 91 MiB. Pieces, all unscored:

| Piece | Wall | What it projects for the scored run |
|---|---|---|
| `U_cycle` unitarity, 35 k-points | 0.077 s | S0-P1 is a fraction of a second |
| FFT, L = 16, precompute + 40 cycles | 0.59 s (1.05 ms / cycle) | C1 drift, 1,000 cycles, 5 seeds × 3 states ≈ 16 s plus 0.5 s precompute |
| FFT, L = 32, precompute + 40 cycles | 4.31 s (8.2 ms / cycle) | C5 geometry at L = 32, a few seconds per state; 1,000 cycles would be ≈ 8 s |
| Commutant matrix + SVD, 40 random k | 0.94 s (560 parameters, 640 equations) | — |
| Same, 6³ = 216 k | 4.54 s build+SVD, 91 MiB | Official 12³ = 1,728 k scales about ×8 in build: ≈ 27 s build, SVD of a 27,648 × 560 matrix (about 124 MiB of A) estimated at under 2 min; well inside 10 min |
| 10⁵ four-channel shots, Python loop | 0.72 s | Vectorised sampling is faster; C2's 5 × 5 × 3 × 3 × 10⁵ draws stay under a minute |
| C5(b) geometry only, L = 16, 50 × 5 | 0.089 s | The official 50 × 5 × 2 factors at L = 32 is a fraction of a second; the mid-plane charge seen in the probe is why §9 uses Voronoi cells at L = 32, d = 8, and does not use a delocalized random field as an official C5 state |

**Expected whole scored run.** Under 10 min wall and under 256 MiB peak on the box, dominated by the C1 12³ SVD and by JSON writing. The caps are a margin.

**Run folder (scored, when authorised).** `/workspace/runs_l20/YYYYMMDD_l20_<first 8 hex of this design's sha256>/ ` on the box, or the sparky analogue under `/root/spacetime_files/`. Write-once. `bigbang` is not used. The first failed or partial attempt, if any, stays on record and is not rescored.

## 12. Harness code in this folder

`l20_measure.py` implements the FFT stepper against frozen `dirac4.py`, the 560-parameter commutant matrix, the client lock, the discrete Stern–Gerlach embedding, and the `--probe` path that produced the JSON above. The scored check entry points are present as stubs: they refuse to score unless `L20_SCORE=1` is set after the design hash is named. Filling those entry points to the letter of §§4–9 is part of the scored run's pre-flight, and any departure from this document is a P0 fail.

## 13. What this design does not authorise

- No scored C1–C5 run until Edmond names the sha256 of this file.
- No paper edit, no plan edit, no restatement of §5.5, no L1.5 closure, and no L2.1 run.
- No use of `/workspace/qca/bcc.py` as the gated rule.
- No use of `bigbang`.
- No carrying of probe numbers, born3 / tn / §5.5 numbers, or L1 spectral numbers into a C1–C5 verdict.

The L2.0 exit gate remains the plan's (lines 254–255): either the sketch is written out with every assumption listed and the checks pass, in which case S1 is narrowed to (i), or to (i) plus R-d2 in the D10 default case; or a gap is found and S1 stays open. Closing S1 is not on offer.
