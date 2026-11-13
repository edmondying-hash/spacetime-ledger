# Layered test program for the §9 open problems — v3.4 (DRAFT, not signed off)

**Status (2026-11-12): DRAFT v3.4, awaiting Edmond's sign-off. It supersedes v3.3 r2 only when signed off; until then `layered_plan_v3_3_r2_20261111/` stays the live plan. This draft changes no paper, Sheet or production file, and no simulation was run to make it.**

**v3.4 (2026-11-12, after Edmond's answers B1–B4 to the plan review):** v3.3 r2 is kept unchanged at `layered_plan_v3_3_r2_20261111/layered_plan_v3.3.md` (sha256 `89b3972a0af418bfcb260b978842e79dc73945c61ec2bd85fe3a5e7d1785aa39`). Paths beginning `/workspace` refer to the earlier working machine and are not in this repository; paths without a leading slash are relative to the repository root. v3.4 (1) applies the one-orbit closure of L1.1 and removes the repair text it made stale; (2) records Edmond's decisions B1 (the canonical rule `dirac4` gates L1.1; OP4's three extra nodes are a diagnostic finding), B2 (every OP4-rule or OP4-bridge result is to be redone on `dirac4` before it counts), B3 (load-free carve-out for L1.1–L1.3) and B4 (the official V5 v2 census is accepted as the L1.1 census on the canonical rule; nothing is re-run); (3) records L1.2 closed and L1.3 closed on L1.3b (run `9ccf4855`: R1 PASS, R2 FAIL / OPEN, kept as written; run `20261112_l13b_dc90fd23`: PASS); (4) adds §0.5–§0.7, of which §0.5 and §0.6 are **proposals awaiting Edmond's confirmation** and §0.7 is a decision log. The full list of edits is `CHANGES_v3.4.md`; the exact diff is `plan_diff_v3.3_to_v3.4.txt`.

**v3.3 (2026-11-11, after Edmond t2400u):** v3.2 is kept unchanged at `/workspace/layered_plan_v3_2b_20261111/layered_plan_v3.2.md` (sha256 `5e5891bb55fc5449965f7efba8482bfecd135c30172f770d7dc65564db4902dd`). v3.3 changes only the V3 clause of the §2 L0 status line: V3 is closed with a finding, citing the official V5 v2 census (`results.json` sha256 `ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708`) and the 9 November `scan_gap.py` (script sha256 `821be234e6508aa9c6fe3cb3f8e996643697c66397b711f0fb0a7330b70dfd28`). To match, it also updates the title and the status line at the top. Relative paths in this document still refer to the v3.1 folder `/workspace/layered_open_problems_20261109/`.
**v3.2 (2026-11-11, after Edmond pt2369u):** v3.1 is kept unchanged at `/workspace/layered_open_problems_20261109/layered_plan_v3.1.md` (sha256 `dac6a260659f0ed2c69c8440aa3e0a6585ddfcd587b02053071946008f11cbda`). v3.2 changes the L0 exit gate (§1 table row L0 and §2 **Exit gate**): V1–V4 must still pass, and V5's criterion becomes that V5 ran and its result is recorded; to match, it also updates the title, the status line at the top and the §2 L0 status line. Reason: table 6's N_s=24 cell sits below the generating script's own resolution cut (`qca/dw_final.py:9`, `r[:,1]>1e-15`), so it cannot reproduce by construction; see the erratum `ERRATUM_PAPER_V5.md` (sha256 `1f770a8680bdbf7f253c2065b9b00e1c0da16d76223bd9f5cdfa3643941bd5ce`) and the V5 r2 `results.json` (sha256 `f755182c0fedf92e904b7a3c54ee63834dccf46add931762f0528a4702c60771`); relative paths in this document refer to the v3.1 folder `/workspace/layered_open_problems_20261109/`. This file supersedes the withdrawn first cut of v3.2 (`/workspace/layered_plan_v3_2_20261111/layered_plan_v3.2.md`, sha256 `af01013537f980c23aa71f6c2f63ddc40bab30660bf76c32083aca69f11f0872`), which was never pinned.
**v3.1 (2026-11-09, after Edmond t1964u):** v3 is kept unchanged at `layered_plan_v3.md`. v3.1 changes only L2.0: a new gap **G-7 (the d = 2 loophole)**, a new check **L2.0-C5 (link-channel reads)**, and matching updates to the L2.0 exit gate, status, traceability row and sprint item. See `CHANGES_v3.1.md`, `born_fixes/D2_NOTE.md` and `born_fixes/PROPOSAL.md`.
Revision of v2 after Edmond's review (2026-11-09). v1 is kept unchanged at `ref/layered_plan_v1_original.md` and v2 at `layered_plan_v2.md`. v1→v2 edits are in `CHANGES.md`; v2→v3 edits are in `CHANGES_v3.md`. Nothing from v1 has been deleted: items moved out of the main line are in Appendix A, and targets that were not measured numbers are kept as labelled *reference values* (§0.3).

Paper checked against: `space-ledger-v2.md` / `.pdf` on `main` at commit `9d39338` (2026-11-09 08:50 EST), §8 and §9 (PDF pp. 68–71). (v3.4: the L1.1 to L1.3 items refer to `main` at `cc2cc5c`, paper sha256 `8cbb94ec481b3332f074ea028505478dd2d576a8b5d60915f072b653ab6aad70`; §8 and §9 were not re-checked beyond the L1 items.) Open-problem numbers **OP1–OP19** and server-side items **S1–S7** are the paper's own numbers and are not renumbered here.

Target: open problems 1–19 and server-side items S1–S7, plus the three objectives in §8 (8.1 read-out, 8.2 radiative Lorentz invariance, 8.3 chiral gauge theory).

The approach is bottom-up. Each layer is a software milestone with a frozen interface, an entry gate and an exit gate. A later layer may not change a lower layer's conventions. If it must, the lower layer is re-run. This is the only way to keep toy results comparable across the paper's tables.

---

## 0. Standing rules (apply to every layer and every run)

### 0.1 Physics rules

1. **Congestion is always ON**, including in vacuum. Congestion OFF is allowed only as a labelled diagnostic and never counts toward a gate. Which load rule is meant (the paper's load-first rule or the OP4 local rule and its continuum bridge) is fixed per run; the symbols are listed, one rule each, in §0.4. **Exception (v3.4, Edmond B3, 2026-11-12):** the Layer 1 free-spectrum gates L1.1–L1.3 are evaluated on the §6.2 vacuum symbol, which has no load term (uniform load only rescales velocity). Each such run declares "load rule: none, §6.2 vacuum symbol". L1.4 and L1.5 declare their own load rule and keep congestion ON.
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
| Three-slit interference | \|κ\| < 10⁻² (Sinha et al., Science 329, 418 (2010)); κ̃₃ = (0.6 ± 1.8)×10⁻³ single photons (Kauten et al., NJP 19, 033017 (2017)) | as cited |
| Isotropic photon–electron speed difference (G6) | −5.8×10⁻¹² ≤ κ̃_tr − (4/3)c_e^{00} ≤ 1.2×10⁻¹¹ | Hohensee et al., PRL 102, 170402 (2009) |
| Strong-field photon test (not a G1 comparator) | Sgr A* shadow δ = −0.08 ± 0.09 (VLTI), −0.04 (+0.09/−0.10) (Keck) | EHT Collaboration, ApJL 930, L17 (2022) |
| Cluster halo profile (C1, pre-registered) | stacked Σ(R) of 16 X-ray-selected CLASH clusters, published bins and covariance | Umetsu et al., ApJ 821, 116 (2016) |
| Lepton masses | mₑ = 0.51099895000(15) MeV, m_μ = 105.6583755(23) MeV, m_τ = 1776.93(9) MeV; m_μ/mₑ = 206.768283(5), m_τ/mₑ = 3477.37(18) | PDG 2024 (Navas et al., PRD 110, 030001) |
| Koide ratio of measured masses | Q = 0.6666645 ± 0.0000051 (from the PDG masses above; 2/3 is the empirical relation, not a target for the model to "derive" beyond what the masses show) | computed here from PDG 2024 |
| Higgs and top masses | m_H = 125.20 ± 0.11 GeV; m_t = 172.57 ± 0.29 GeV | PDG 2024 |
| Scalar tilt | n_s = 0.9649 ± 0.0042 (68%) | Planck 2018 X, A&A 641, A10 (2020) |
| Tensor-to-scalar ratio | r₀.₀₅ < 0.036 (95%), upper limit only | BICEP/Keck + Planck + WMAP (BK18), PRL 127, 151301 (2021) |
| Vacuum energy (S5 size) | ρ_Λ/ρ_Planck ≈ 1.1×10⁻¹²³ (from Planck 2018 H₀ = 67.4 ± 0.5, Ω_Λ = 0.685 ± 0.007) | Planck 2018 VI, A&A 641, A6 (2020); derived arithmetic |

### 0.4 Symbols and which rule they belong to

Two load conventions are in use. They are **not** the same rule and must not be mixed in one comparison without a declared bridge. One line per symbol:

| Symbol | Rule it belongs to | Definition | Source |
|---|---|---|---|
| U | Paper, load-first link priority | clock potential, U = −ln f | paper Sec. 6.12 ("Load-first link priority"); `/workspace/op15load/VERDICT.md` |
| f | Paper, load-first link priority | light's free-tick share of a link, f = e^{−U} (Poisson tick claiming) | paper Sec. 6.12 and OP7; `/workspace/op15load/VERDICT.md` §2 |
| ρ | Paper, load-first link priority | load share of a link, ρ = 1 − e^{−U} | paper Sec. 6.12 |
| per-link light cost | Paper, load-first link priority | 1/(1−ρ)² = 1/f² = e^{2U} | paper Sec. 6.12, OP7 |
| ℓ | OP4 local rule | node load (dimensionless; not the link length ℓ of §2) | `prod/op4_local_gpu.py` lines 2–5 |
| s | OP4 local rule | s = (1+ℓ)^{−1/2}; loaded generator H = √s Q_fwd √s, bond angle ∝ √s_i √s_j, on-site clock phase ∝ s | `prod/op4_local_gpu.py` lines 2–5, 51–64 (quoted in `/workspace/gpu/op4_bcc_local/curved_reference_design/congestion_history_audit_20261108/REPORT.md`) |
| V | OP4 photon continuum work (clock) | V = s | `.../photon_comparison_20261108/REPORT.md`; `.../photon_field_refinement_20261108/results.json` ("bridge") |
| f = s | OP4 photon continuum **bridge** (assumed, user-adopted) | identifies the old free-tick share with the OP4 clock factor | `.../photon_priority_comparison_20261108/REPORT.md`; `.../photon_field_refinement_20261108/METHOD.md` |
| F | OP4 photon continuum bridge | photon speed F = s² (mean cost 1/f² with f = s) | same |
| W | OP4 photon continuum bridge | optical spatial factor W = 1/s in isotropic-metric bookkeeping (lapse-only benchmark uses W = 1) | same; congestion audit REPORT |
| ρ = 1 − f | OP4 photon continuum bridge (lock-queue) | the paper's ρ carried over with f = s; **not** the paper's e^{−U} form | congestion audit REPORT |

"Congestion ON" in §0.1 means whichever of these load rules the test declares, always active including in vacuum. Each run must name its rule (paper load-first rule, OP4 local rule, or OP4 continuum bridge).

### 0.5 Reproduction conventions (PROPOSED in v3.4, awaiting Edmond's confirmation)

Motivation: the L1.2 reproduction used "within 5%", which is a loose tool near 1, at floors and for two-digit entries.
- A reproduction of a printed table cell passes if it rounds to the printed digits, or lies within a relative tolerance stated in the design, whichever the design names in advance.
- A cell at or below the generating script's own resolution floor is declared **uninformative in advance**, with its raw value reported (as V5 did for table 6, N_s = 24).
- For any direction-dependent quantity the design names the direction of k (the paper does not for Table `dw`).

### 0.6 Run-design practice (PROPOSED in v3.4, awaiting Edmond's confirmation)

Motivation: L1.2 R5 failed as written because its thresholds were guesses made without data, and L1.3 R2 failed because a prefactor was wrong and the measurement protocol assumed no term odd in k. Under §0.1 rule 4 neither can be retuned after the data.
- **Pilot, then freeze.** If a threshold cannot be set from theory or from the paper, run a labelled calibration pilot on a separate grid or seed, hash its result, and freeze the threshold before the gate run. The pilot never counts toward a gate.
- **Design dry-run.** Before approval, evaluate every closed form in the design at its stated special cases (for example "reduces to X at φ₂ = φ₄"), and state in the design which terms the measurement protocol assumes absent (for example odd powers of k). Also exercise every record-keeping read (lookups of values that are only cited, not measured) on the actual input files, because the L1.3b run lost its N4 lookup to a key-type error that a dry-run would have caught.
- **Approval packet.** A run is handed over as: design folder with sha256; decisions sidecar outside the hashed folder; Edmond's approval naming the hash; caps; runner; results on a separate branch and pull request; review; closure record; then any paper edit.
- **Stop rule.** A run stops on the first failed gated step. Unrun steps are recorded as "not run". Running them later is a new, separately approved run, not a retry of the failed step.
- **Pre-registration governs on conflict** between a design and the pre-registration it cites (L1.2 decision D4).

### 0.7 Decision log (Edmond's decisions; dates America/New_York)

| Date | Decision | Where recorded |
|---|---|---|
| before 2026-11-12 (in v3.3) | Canonical rule: `dirac4`; OP4 a labelled diagnostic branch | §2 |
| 2026-11-12 | L1.1 closed by adopting a single BCC orbit of the integer cubic grid; the twelve edge zeros are Γ images; the sum-form r = 0.05 Wilson repair is withdrawn | paper commits `66ee62f`, `cc2cc5c`; `L1_1_one_bcc_reason_r2_20261112/` |
| 2026-11-12 | L1.2: D1 load-free; D2 revised (pass when the end-versus-bulk speed difference is measured and recorded); D3 thresholds accepted; D4 `PREREGISTRATION.md` governs; design `7e09b7c4` approved 4:56 PM | `L1_2_run_design_20261112_DECISIONS.txt` (sha256 `c3225f353a1ad68956e2d39443814586b8c6e62ce862dced70e9c1f5aa17cf4e`) |
| 2026-11-12 | L1.2 closed; paper wording "from b ≈ 0.35" | `L1_2_CLOSURE_20261112.txt` (branch `cursor/l1-2-closure-paper-wording-a445`, PR #6, not yet merged) |
| 2026-11-12 | L1.3 design `9ccf4855` approved 7:33 PM, run by the Grok bot on bigbang; "layer weights" = two Wilson angles φ₂, φ₄; tolerance 1e-6; massless only; same pipeline for the paper edit | `L1_3_run_design_20261112_DECISIONS.txt` (sha256 `2dc1bb8e94e16c727bc2bc978d5ee904044e3e1a7566878d33a0c1960b158072`) |
| 2026-11-12 | L1.3: R2 of run `9ccf4855` recorded as open as written; corrected L1.3b approved to be designed (7:55 PM) and approved to run (8:12 PM, "L1.3b approved") | `L1_3b_run_design_20261112_DECISIONS.txt` (sha256 `c2081f1852847777e3acf931442890a1d80dcc7768b582af6da423029c995e9c`, PR #10) |
| 2026-11-12 | L1.3 closed on L1.3b (run PASS, PR #12); paper edit under D5 prepared: closed form `c₀(φ)` and φ is a free parameter (8:32 PM) | `L1_3_CLOSURE_20261112.txt` (PR #13) |
| 2026-11-12 | Plan review answers: B1 `dirac4` gates L1.1 and OP4's three extra nodes are a diagnostic finding; B2 "all to be redone" (scope read as OP4-rule and OP4-bridge results; reading pending confirmation); B3 load-free carve-out for L1.1–L1.3; B4 the official V5 v2 census is accepted as the L1.1 census of `dirac4`, no re-run (Edmond, 8:11 PM: "B4 is accepted, no rerun"; his earlier words at 7:48 PM and 7:51 PM are in the sidecar) | `layered_plan_v3_4_draft_20261112_DECISIONS.txt` (verbatim words and times) |


---

## 1. Layer map

| Layer | Content | Open problems | Exit gate |
|---|---|---|---|
| **L0** | Substrate, conventions, exactness harness; **choice of canonical rule** | OP1 (foundation) | V1–V4 pass; V5 ran and its result is recorded (V5 cannot pass in full: table 6's N_s=24 cell sits below the generating script's own resolution cut (`qca/dw_final.py:9`, `r[:,1]>1e-15`), so it cannot reproduce by construction); units frozen; one canonical node rule named, the other a labelled diagnostic branch |
| **L1** | Free spectrum: doublers, chirality, dispersion, ν, **linear-term test** | OP3 (spectrum), OP15, OP16 | zero modes and extra nodes of the canonical rule classified (reason: one BCC orbit; the V5 v2 census accepted as the census of that rule); OP4's extra nodes recorded as a diagnostic finding; gap table reproduced; linear term measured and compared with GRB limits; ν from the rule or declared free |
| **L2** | Read-out and statistics | S1 (L2.0 derivation attempt), S7, OP2, S2, OP3 (shared records) | per item: L2.0 S1 attempt recorded as narrowed or open; S7 reproduction; κ bound; exchange phase −1; order independence |
| **L3** | Gravity | OP4–OP11, OP17 | **per item** (§5): each of G1–G7 passes or fails on its own gate. G1 is open: the strong-field toy is 3% short in finite-screen steering, and a weak-field γ has not been measured |
| **L4** | Matter spectrum | OP12–OP14 (OP18 moved to Appendix A) | κ_c scaling; OP12 needs a new mechanism with a stated reason (the existing-rule route is a recorded no-go, established on the OP4 rule: diagnostic branch) |
| **L5** | Cosmology | OP19, S3, S5, S6 (S4 moved to Appendix A) | halo slope against a measured profile; n_s against Planck and r against the BK18 upper limit; vacuum-energy mechanism or no-go |

Parallel tracks: OP13 (Higgs) and OP19 (halo) do not depend on L2 and can start after L1.

---

## 2. Layer 0 — substrate and harness

**Frozen conventions.** One BCC orbit of ℤ³ (all-even or all-odd integer coordinates); integer hops `h = (±1,±1,±1)` in units of a/2, so `ℓ = |h|·a/2 = a√3/2` and k is in radians per a/2; which of a and a√3/2 is identified with ℓ_P is an open paper item (`PAPER_EDITS_one_BCC.md`), not settled here, and `τ = 0.989 t_P` assumes a ≈ ℓ_P; "hop rate" (one layer or one cycle, and which length) depends on the same item; κ is |k| in radians per a/2 in the L1.3 and L1.3b runs, whereas L1.5 and earlier plan text use κ = kℓ, so kℓ = √3 κ; `c = ℏ = 1`, tick `τ = 0.989 t_P` (0.9855 with the chirality chain). Coefficients are quoted in `(kℓ)²`. Every result records code version, seed, grid, boundary condition, units and load rule (§0.4). The standing rules in §0 are part of the frozen conventions.

**Canonical rule (decision).** Two node rules are in use: the paper's §6.2 four-component rule with a Wilson layer (Table `dirac4`), and the OP4 local rule (`prod/op4_local_gpu.py`, a product of three 1D walks with ν² + m² = 1 per tick) used for the recent gravity, photon and spectrum work. They have different doubler content (L1.1) and possibly different linear terms (L1.5). **v3 picks one option: at the L0 exit, exactly one canonical rule is named; the other is kept as a labelled diagnostic branch** that may be run for comparison but never counts toward a gate. **Decision (Edmond): `dirac4` is canonical; OP4 is the diagnostic branch.**

**Consequence of the decision (v3.4, Edmond B1 and B2, 2026-11-12).** Every result whose harness uses the OP4 rule or its continuum bridge is a diagnostic-branch result and **is to be redone on `dirac4` before it counts toward a gate**. That covers: G1's finite-screen steering 0.970 and the photon-bending runs (§5, §10); the M3 generation split on OP4's nodes (§6); the OP4 node findings (L1.1, §10); and the held L1.5 tick-budget design (§3). **Scope reading pending Edmond's confirmation:** "all to be redone" is read as the results just listed, applied the same way in §1 (L4 row), §5 (G1, G7), §6, §8 (row 12) and Appendix A. Each redo needs its own design and Edmond's approval; none is designed yet. Items whose harness uses neither OP4 nor the §6.2 node symbol (G3's 1D zigzag walk with the paper's f = e^{−U} rule, M1, M2, C1–C4) are not changed by this decision, and the existing rule stays: anything that uses the L1 3D node symbol waits for L1's exit gate.

**Tests.** V1 unitarity, reversal and light cone; V2 scalar dispersion; V3 independent dense BZ scan; V4 energy drift over 10⁵ ticks; V5 regenerate the paper's tables.

**Exit gate.** V1–V4 pass; V5 ran and its result is recorded (V5 cannot pass in full: table 6's N_s=24 cell sits below the generating script's own resolution cut (`qca/dw_final.py:9`, `r[:,1]>1e-15`), so it cannot reproduce by construction); the result schema is fixed; one canonical rule named, the other labelled diagnostic.

**Status (2026-11-11):** V1, V2 pass. V3 closed with a finding (§10): the official V5 v2 census (`results.json` sha256 `ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708`) is V3's dense-scan object — unrepaired `dirac4` at m=0, 129³ boundary-inclusive grid, local minima refined by Nelder–Mead, exclusion 0.3 around every Γ image, argmins with distances — and reproduced all 18 numeric cells of Table `dirac4`; it agrees with the 9 November `scan_gap.py` (25³ interior and exact evaluation of the twelve edge-point zeros; script sha256 `821be234e6508aa9c6fe3cb3f8e996643697c66397b711f0fb0a7330b70dfd28`) on the interior table, and those twelve points are Γ images under the even-parity lattice and lie in the V5 exclusion set. V4 PASS (`results.json` sha256 `1aa2130cebf03232f1c04a9f7e67e7228344d3a45803a85d2d7c22b2aae43e0a`). V5 recorded as FAIL: V5 r2 verdict "V5 FAIL (tables not reproduced: 2, 6)" (`results.json` sha256 `f755182c0fedf92e904b7a3c54ee63834dccf46add931762f0528a4702c60771`); table 2 was a paper typo, corrected by erratum on main@393f4493; table 6 is below the generator's resolution cut and is expected to fail in V5 v2. Canonical rule: `dirac4` (OP4 a labelled diagnostic branch).

---

## 3. Layer 1 — free spectrum (OP3, OP15, OP16)

### L1.1 Doubler census — OP3 (canonical rule gates; OP4 diagnostic)

**Status (v3.4, 2026-11-12).** The reason decision is made: on one BCC orbit the twelve edge zeros are Γ images, and the sum-form repair is withdrawn (Edmond; paper commits `66ee62f`, `cc2cc5c`). **L1.1 is CLOSED (Edmond B4, confirmed 2026-11-12, 8:11 PM: "B4 is accepted, no rerun"): the official V5 v2 census is accepted as the L1.1 census of the canonical rule `dirac4`, and no re-run is needed.** That census (`results.json` sha256 `ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708`) is unrepaired `dirac4` at m = 0 on a 129³ boundary-inclusive grid with local minima refined, exclusion 0.3 around every Γ image, and it reproduced all 18 numeric cells of Table `dirac4`; the 9 November `scan_gap.py` evaluated the twelve edge points exactly and found ω = 0 there, which the one-orbit reason identifies as Γ. OP4's three extra nodes (H, P, P′) are a **diagnostic finding**, recorded here, with no repair required by the gate (Edmond B1). **r8 stays signed off; under one orbit it is no longer the required L1.1 path for `dirac4`; nothing in r8 is withdrawn.**

**Setup.** Take the explicit 4×4 symbols of §6.2 of the canonical rule on the one-orbit lattice (the OP4 generator Q(k) = [[ν n·σ, −m], [−m, −ν n·σ]] is scanned only as a labelled diagnostic). Scan the cube `[-π,π]³` densely (≥129³) and include every high-symmetry point. A zero at πg with g an integer triple of even coordinate sum is Γ on the one-orbit lattice and is reported as a Γ image, not as a doubler. Refine candidates with a local minimiser. Report the minimum over the *interior* and over the *closure*, separately, and report each zero's location, chirality and tilt.

**Pass.** For the canonical rule, no zero except Γ and its images in the closure (a Γ image being a reciprocal-lattice class on the one-orbit lattice), with the interior gap table reproduced (met by the V5 v2 census). OP4's nodes are reported but do not enter the gate.

**[Superseded 2026-11-12 by the one-orbit decision; kept as history. The twelve points are Γ images, not defects.]** **Current result, §6.2 Wilson symbol.** Interior minima match Table `dirac4` (0.084 vs 0.082 at φ=1.4; 0.201 vs 0.217 at φ=0.5; coarse-grid error). But there are **12 exact massless zero modes** at the edge labels `(±π,±π,0)` and permutations, independent of φ, with the Wilson layer present (U = I to 7e−16). They gap only when `m>0` (ω=0.050 at m=0.1). Random starts never hit them because they are measure-zero. See §10.

**[Diagnostic branch; recorded finding, not a gate.]** **Current result, OP4 rule** (`/workspace/bcc_staggered_design_20261109/`, symbolic checks). OP4 has **4 isolated Weyl nodes per chirality block**: Γ, H = (π,0,0), P = (π/2,π/2,π/2) and P′ = −P, i.e. **3 extra nodes (doublers)**. Chiralities are (+,−,+,−) for (Γ,H,P,P′) and sum to zero (Nielsen–Ninomiya). They are isolated points, not lines. Uniform congestion load only rescales velocity and leaves the node count unchanged.

**Naive BCC operator and staggering.** The naive nearest-neighbour BCC Dirac operator has **zero lines** at k_i = k_j = π/2 (a count that grows with L). **Kogut–Susskind spin diagonalisation is frustrated on BCC**: the four body-diagonal hops cannot all anticommute for any U(1) phases, so exact KS staggering does not exist on this lattice, and staggering does **not** remove the zero lines. The best Z₂-flux pattern gives about 2 Dirac tastes but with over-tilted (type-II) cones.

**Decision (Edmond, 2026-11-12).** Option (a), a reason: the single BCC orbit. The sum-form `g(k)` repair is withdrawn (it is not periodic under π(1,1,0)), and no repair of OP4's three extra nodes is required by the gate. The V5 v2 census is accepted as the census (B4, confirmed 8:11 PM).

**Link to OP12.** Using the four OP4 nodes as the three generations is a recorded no-go under existing rules (L4, M3).

### L1.2 Chirality chain and doubler gap — OP3

Reproduce Table `dw`: residual mass vs Ns, `|γ5|`, localisation length, smallest gap vs b. Pass: within 5%, and `b ≤ 0.25` boundary confirmed independently. Then test the *end-mode* dispersion against the physical-mode dispersion: the chiral mode's speed is 0.9855 of the hop rate; a difference would be a species-dependent `c`.

**Status (v3.4): CLOSED 2026-11-12.** Run `7e09b7c4` (results PR #5, branch `grok/l1-2-run-20261112`); closure record `L1_2_CLOSURE_20261112.txt` (branch `cursor/l1-2-closure-paper-wording-a445`, PR #6, not yet merged). Table `dw`: 14 of 14 scored cells pass; the pre-registered three-part boundary clause passes; the end-mode speed is 0.985529 against the unchained 0.989084, a difference of −0.00355526 or −0.359% (against the paper's 0.98911 it would be −0.362%), recorded as a species-dependent `c` (D2 revised: (a) both speeds measured by one code path with the difference recorded, and (b) the end mode within the 5% rule of the paper's 0.9855). Design item R5 failed as written (its 0.5 end-copy-weight threshold was a guess, and the weight at (π/2)³ never exceeds 0.353); it was not retuned. PR #6, when merged, changes paper §6.2 (main still says "For b≥0.3") to "from b ≈ 0.35".

### L1.3 ν from the rule — OP3

The paper leaves open whether `ν = cτ/a = 0.989` is fixed by the rule or by φ. **Test:** scan φ and the layer weights; determine whether any local normalisation forces `ν = 0.98911`. Pass: a derivation or a proof that φ is a genuine free parameter. This matters because `ν` sets the tick and therefore every quoted rate. (A scan of φ to *understand* the rule is allowed; choosing φ to hit a number is not.)

**Naming (v3.4).** The hop weight ν_S (ν_S² + m² = 1, so ν_S = 1 at m = 0) is a different quantity from ν = cτ/a, which is the light speed c₀ in units of the hop rate.

**Status (v3.4): CLOSED on L1.3b (Edmond, 2026-11-12, 8:32 PM: "let's close L1.3 on L1.3b"; closure record `L1_3_CLOSURE_20261112.txt`, branch `cursor/l1-3-closure-paper-edit-a445`, PR #13, not yet merged).** The original run `9ccf4855` keeps its verdict FAIL / OPEN as written.
- **Run `9ccf4855`** (design sha256 `9ccf48559c099289b24af638164ca64b95195872b1e4a0d8966ed44ca800d098`; results PR #8, branch `grok/l1-3-run-20261112`, commit `f4e45728`, SHA256SUMS `17f5e19944dd36a7b257854951e5a4c594515d71dedd8e4a0d43da6f139e6157`): stopped after S2. **R1 PASS:** `c₀(φ) = ½√(1 + 3 sin²φ)` matches the exact symbol at all 16 values of φ in all 13 directions to 4.3e-14. **R2 FAIL:** all 42 pairs with φ₂ ≠ φ₄ miss the 1e-6 tolerance (worst 1.6e-4 at (0.5, π/2)); the design's printed formula had the wrong prefactor (¼, not ½; the run fixed the reading before computing and recorded it, DEV-1), and its κ² extrapolation assumed no odd term, which exists for φ₂ ≠ φ₄ along [110] and [111]. **S3 not run** (stop rule), so N1–N5 were not reached.
- **Run `20261112_l13b_dc90fd23`** (L1.3b design sha256 `dc90fd231d9a92602187f61dc68bded2891b3ece5274290ba18b75f86d604a8d`, PR #10, approved 8:12 PM; results PR #12, branch `grok/l1-3b-run-20261112`, commit `3d6075b791ce1bd089a1fbd95196ee31327911fb`, SHA256SUMS `5ab7cdd2b7e5a4af7d0d385cff0cd2ffd5308775b7d9479938cc5fdfe27dbf0b`, 42 of 42 verify): **verdict PASS.** R1′ (equal angles, 16 φ × 13 directions) max 1.69e-13; R2b (49 angle pairs × 13 directions, factor-¼ form, all powers of κ fitted) max 4.10e-13; N1 unitarity 3.0e-15; N2 slope of c₀ at φ = 1.4 is 0.1266, so 1.4 is not stationary; N3 c₀ strictly monotone from 0.5 to 1 over φ ∈ [0, π/2]; N5 26 hits for φ = 1.4 in the record, none a derivation. R2c (record only): linear coefficient at most 1.7e-10 on [100] and at equal angles; nonzero for φ₂ ≠ φ₄ on [110] and [111] (up to 0.104).
- **What this settles.** The low-energy light speed of `dirac4` on one BCC orbit is `c₀(φ) = ½√(1 + 3 sin²φ)` for equal Wilson angles, and φ is a free parameter: unitarity and the tested local structure select no value. The tick `τ = 0.989 t_P` corresponds to the paper's choice φ = 1.4 (a gap-versus-speed choice) and inherits it.
- **Disclosed, not affecting the verdict:** the approval did not quote the design hash (the run notes record the 8:12 PM message and a DM to the bot); S3's N4 record lookup raised KeyError and was not re-run (post-run read from the hashed census: gap 1.37e-17, speed 0.99993, `post/N4_CITED_READ.json`); SHA256SUMS was regenerated once; the S3 cross-check against the frozen `dirac4` module differs by exactly 0.0.
- **Paper edit (design D5, Edmond 8:32 PM).** Prepared in PR #13: the closed form and the statement that φ is a free parameter, in §6.2 "Low-energy limit". Takes effect only on merge. The two-angle form and the linear-term remark are not added.

### L1.4 Dispersion and diffusion vs data — OP15

Produce, from the rule, a sky-direction table of `1−v/c` at 1 GeV, 1 TeV, 31 GeV, 100 TeV, 3e20 eV, both subluminal and superluminal signs. Compare with the measured limits in §0.3: Fermi GRB 090510 (E_QG,1 > 7.6 E_Pl, Vasileiou 2013; conservative 1.2 E_Pl, Abdo 2009), LHAASO GRB 221009A (E_QG,1 > 1.0×10²⁰ GeV subluminal; E_QG,2 > 6.9×10¹¹ GeV). Also compute a diffusion signature (arrival-time blur) for a random (Poisson) control, which the model excludes (Sec. 7.3). Pass: no bound violated; the anisotropic term is stated with its search template, not just its magnitude.

### L1.5 Vector and tensor fields; linear-term test — OP16

Repeat L1.4 with a photon-like vector field and the canonical rule (4-component §6.2; OP4 only as a labelled diagnostic), along at least 13 directions including [100], [110], [111] and [11−1].

**Why this is a test, not an assumed pass.** The paper's "no linear term, leading effect quadratic" statement (Sec. 6.4 Test 1, Sec. 7.8) comes from the scalar link-only toy. For the OP4 rule (diagnostic branch; no corresponding prediction has been derived for `dirac4`), a leading-order analysis predicts a **possible linear, direction-odd massless light-speed leak along [111]**, v_g ≈ 1 + (2/(3√3))κ ≈ 1 + 0.385κ (κ = kℓ here; the L1.3 and L1.3b runs use κ = |k| in radians per a/2, so kℓ = √3 κ, and the 0.385 figure comes from a design written under the older h/2 convention: restate it in the current convention before any L1.5 design), which flips sign along [11−1]; along [100] and [110] the leading term is quadratic (1 − κ²/2, 1 − 5κ²/8) (`/workspace/lorentz_tick_budget_design_20261109/DESIGN.md`). Whether it survives the exact whole-tick macrostep is exactly what the run measures. *Hypothesis to pre-register, not a result:* the L1.3b run recorded (R2c, record only) no term linear in |k| in the `dirac4` massless light speed at equal Wilson angles (|b| ≤ 1.7e-10 at the equal-angle pairs, 13 directions, PR #12), whereas unequal angles produce one on [110] and [111]; this is a measured observation on the canonical rule, but it was not a gated result and says nothing about the L1.5 whole-tick macrostep; a hand derivation for `dirac4` in the style of L1.3 should come before any L1.5 run.

**Measure.** Massless v_g(κ, direction) from the exact whole-tick evolution, congestion ON (uniform vacuum load) with OFF as a labelled diagnostic; fit only the leak coefficients ξ₁ (linear) and ξ₂ (quadratic) per direction, with the same uncertainty treatment as the data.

**Pass.** The implied E_QG,1 in every direction exceeds both the Fermi (7.6 E_Pl) and the LHAASO (10 E_Pl) limits, and E_QG,2 exceeds the LHAASO quadratic limit. A direction-odd term is reported with its sky template, since the bound weakens for bursts with small k_x k_y k_z.

**Falsifier.** A linear term that applies to photons and violates the limits. For scale: if the [111] leak of 0.385κ applied to photons at full size, LHAASO would require ℓ ≲ 0.26 ℓ_P (with κ = kℓ), i.e. a ≲ 0.30 ℓ_P (ℓ = a√3/2). That would conflict with the paper's Planck-scale spacing and with the Sec. 7.8 wording.

**Status.** Tick-budget / light-speed run (`lorentz_tick_budget_design_20261109`) is **designed and held pending Edmond's approval** (25 clock fixtures, 10 light-speed runs, 2 controls; proposed caps 1 thread, 1 GiB, 180 CPU s, 240 s wall, 16 MiB, one attempt). Until it runs, L1.5 is **open**, and the Sec. 6.4 / 7.8 "no linear term" wording should be read as scalar-toy only. **v3.4:** that held design is for the OP4 rule, a diagnostic branch, so it does not gate; a `dirac4` design is needed and has not been written.

This closes the largest tree-level Lorentz hole and is a prerequisite for L3.

**L1 exit gate.** L1.1 closed (V5 v2 census accepted for the canonical rule on one BCC orbit, Γ images classified, OP4's nodes recorded as a diagnostic finding); L1.2 reproduced (closed 2026-11-12); L1.3 closed (2026-11-12, on L1.3b); L1.4 and L1.5 measured against the §0.3 limits. (L1.5 needs a `dirac4` design first: the held tick-budget design is OP4-only and diagnostic; see §11.)

---

## 4. Layer 2 — read-out and statistics (S1, S7, OP2, S2)

Order inside L2: **L2.0 (S1 derivation attempt) comes first.** L2.1–L2.2 are S7 reproduction tests that *assume* the energy-share read. They do not test S1.

Targets in L2.1–L2.2 are reproduction of the quantum-mechanical prediction for the same state and geometry (an internal consistency gate), anchored to measured bounds where they exist: three-slit Sorkin parameter |κ| < 10⁻² (Sinha et al., Science 329, 418 (2010)) and κ̃₃ = (0.6 ± 1.8)×10⁻³ for single photons (Kauten et al., New J. Phys. 19, 033017 (2017)); loophole-free Bell tests agree with QM for their own states (e.g. Hensen et al., Nature 526, 682 (2015); Storz et al., Nature 617, 265 (2023)). The Tsirelson value 2√2 is the QM prediction for an ideal state, i.e. a reference value.

### L2.0 S1 derivation attempt: the read weights from conservation of Q (design only)

Built on Edmond's conservation argument (2026-11-09). Seed material: `/workspace/born3` (conservation and fine-graining), `/workspace/born5` (constraint-only weight fit), `/workspace/born4` and `/workspace/born6` (Zurek equal-piece route, both FAIL), paper Sec. 3.3 ("Why the Read-out Is the Square", detector-merging table) and Sec. 8.1. **No run is proposed in this revision.**

**The circularity trap (stated first).** If "energy" is *defined* as |a|², then "read by energy share" is the Born rule with extra steps; the paper says as much (Sec. 3.3: the square "is an input here"). A derivation therefore needs either an independent notion of load or energy, or a conservation argument that *forces* the weights. L2.0 takes the conservation route. Its content is not "energy = |a|²" but two separate facts: (a) Q = Σ|a|² is the charge the dynamics conserves, which is a property of the rule and is not chosen; (b) a read must not bias where that charge sits, which is a stated postulate.

**Setting.** Channels k = 1…K are exclusive outcome regions (disjoint sets of links/components; a detector setting is a unitary applied before the read). Q_k = Σ_{i∈k}|a_i|², Q = Σ_k Q_k. A read is a stochastic map on the *client's conditional state*: with probability w_k it returns k and the conditional state becomes the channel-k content carrying the full charge Q (lock). The server ledger itself is unchanged (paper Sec. 3.3 read-out postulate); see gap G-4.

**Step 1 (property of the rule).** The BCC update conserves Q exactly (unitarity), and among the family Σ|a_i|^p only p = 2 is conserved. Seed: born3 on the D'Ariano–Perinotti rule (`/workspace/qca/bcc.py`, 16³, m = 0.3): Σ|a|² drifts 6×10⁻¹⁴ over 300 ticks while Σ|a| grows ×20 and Σ|a|⁴ falls 99.7%.

**Step 2 (what a read is).** A read (i) conserves Q in expectation **per channel**: E[Q_j after the read] = Q_j before, for every channel j (no wipes, no creation, no bias); (ii) is repeatable: an immediate re-read returns the same k with certainty (lock); (iii) is additive over exclusive outcomes: merging channels k and l gives w_{k∪l} = w_k + w_l (detector merging).

**Step 3 (claim).** The only weights satisfying (i)–(iii) are w_k = Q_k/Q.

*Sketch.* After a read that returns k, channel k holds all the charge Q and every other channel holds 0 (lock). So E[Q_j after] = w_j·Q. Condition (i) requires this to equal Q_j, hence w_j = Q_j/Q for every j. (ii) is then automatic: the conditional state has Q_k = Q, so a re-read returns k with weight 1, i.e. the read is idempotent. (iii) is also automatic, since Q_{k∪l} = Q_k + Q_l. A read by |a| share or |a|⁴ share gives E[Q_j after] ≠ Q_j for generic states, so (i) excludes it. Born then follows from unitarity (Step 1) plus no-wipe (i).

**Where the remaining postulate sits.** Exactly in **(i), read per channel**: a client read is a coarse-graining that neither creates nor destroys Q and does not bias its expected location (the server's "no wipes" rule). Everything else is either a property of the rule (Step 1) or follows from (i). The honest residue of S1 is the physical question: *why is a client read a charge-respecting coarse-graining?* L2.0 does not answer that. If it passes, S1 is **narrowed to postulate (i)**, not closed.

**Gaps in the logic (stated now, to be resolved or carried):**

- **G-1. (i) must be per channel; total-Q conservation is not enough.** If (i) only asks that the total Q be conserved in expectation, any weights w_k work, because the lock already puts the full Q into the chosen channel on every shot. It is the per-channel (martingale) form that forces w_k = Q_k/Q. That is a stronger postulate than "no wipes" read loosely, and it should be stated as such. (It is the same martingale property that gives Born in dynamical-collapse models.)
- **G-2. Step 1's uniqueness holds only within a stated class.** born3 tested only the family Σ|a|^p. Beyond it: (a) any function of Q (Q², √Q) is conserved trivially, so uniqueness is "up to functions of Q", which is harmless; (b) a free, translation-invariant walk conserves many more quadratic charges, e.g. each momentum-mode occupation |ã(k)|² and the quasi-energy expectation ⟨ψ|H|ψ⟩. These are non-local, so a *locality* requirement (a channel's weight depends only on the amplitudes in that channel's links) is needed to exclude them. Locality is an extra assumption and must be listed. (c) Local, positive, conserved quadratic densities other than |a|² may exist for a given rule (for example an energy-current density of the walk). Whether OP4 or the §6.2 rule has any is **not checked**; check C1 adds that search. If one exists, it is an alternative weight, and (i) alone does not choose between them.
- **G-3. (iii) alone does not give Gleason or Busch.** Additivity over one fixed set of channels (one basis) allows any additive weight Σ_{i∈k} g(|a_i|). Gleason's theorem needs additivity for every orthogonal decomposition (non-contextual across detector settings) and dimension ≥ 3; Busch needs additivity over generalised (POVM) effects. A second, independent route to w = Q_k/Q exists without (i): (iii) + locality + "total weight 1 for every state the dynamics produces" forces g(x) = x² (Cauchy-type argument on g(√t); born5's constraint-only fit gives power 2.00 ± 0.01 where weight is carried). That route replaces (i) by non-contextual additivity and so moves the postulate rather than removing it. In the main route, (iii) is a consequence of (i) and is not needed as an input.
- **G-4. What object does (i) act on?** The paper's read-out postulate says a read does not alter the server ledger. If the server state is unchanged, Q is trivially conserved and (i) is empty. So (i) must be about the client's conditional record (relative state), and the plan must state that explicitly. Whether a per-channel martingale on a client-side record can be grounded in server dynamics is part of the S1 residue.
- **G-5. Repeatability selects sharp reads, not weights.** (ii) makes the read idempotent (projective). It does not discriminate |a| from |a|² by itself. It is still a required consistency check.
- **G-6. Entangled pairs.** In born3 the entangled pair is set client-side by hand (paper Sec. 8.1). L2.0 does not change that.
- **G-7. The d = 2 loophole (added v3.1).** Gleason needs dimension ≥ 3. The node space is ℂ²_τ ⊗ ℂ²_σ (paper Sec. 6.2), so a read that resolved only τ or only σ, *as its own two-outcome measure*, would be two-dimensional. There non-quadratic rules survive, e.g. [1 + (n·r)³]/2, the per-pair-normalised \|a\|^p rules, or Bell's 1966 sign model. Embedding (ℓ²(BCC) ⊗ ℂ⁴, dimension ≥ 4) closes it only if the factor read is the same measure as the full-space read. Busch's POVM theorem needs additivity over all effects, which is stronger, and reduces to embedding via Naimark. The main route (Step 3) is dimension-free for any K ≥ 2, but its channels are link sets, so it applies to a factor read only if that read is carried by link channels. **Residual assumption R-d2:** every read, including one of τ or σ alone, is a rule unitary followed by an exclusive link-channel read. As written, the paper's §5.5 pointer API (`read()` returns ±1 with cos² by hand) does not meet R-d2. Tested by L2.0-C5. Full argument: `born_fixes/D2_NOTE.md`.

**Checks (mapped to Edmond's four; each needs Edmond's approval and caps before any run; canonical L0 rule, congestion ON with OFF as a labelled diagnostic; seeds explicit):**

| # | Check | What it tests | Pass | Fail | Seed result (old rule, not the canonical one) |
|---|---|---|---|---|---|
| C1 | Only Q conserved among \|a\|^p, plus a local-density search | Step 1; gap G-2 | Over ≥10³ ticks, relative drift of Σ\|a\|² ≤ 10⁻¹² while Σ\|a\|^p for p ∈ {0.5, 1, 1.5, 2.5, 3, 4} drifts > 10⁻³; the search over positive quadratic densities supported on one node plus its 8 neighbours finds only the \|a\|² density (and functions of Q) conserved | any other positive local conserved density, or p ≠ 2 conserved | born3: p=2 drift 6×10⁻¹⁴ / 300 ticks; Σ\|a\| ×20, Σ\|a\|⁴ −99.7% |
| C2 | Read-channel drift | (i) per channel | For the Q-share read, E[Q_j after] − Q_j = 0 within 3σ for every channel, over ≥10⁵ shots and ≥5 seeds, also after the record evolves further; \|a\|- and \|a\|⁴-share reads show a nonzero per-channel bias at > 5σ | Q-share shows a bias, or the controls do not | born3 check 3: q=2 branch weight stays 0.6667 over 772 sub-links / 60 ticks; q=1 drifts 0.50→0.55, q=4 0.889→0.887 |
| C3 | Lock / repeatability | (ii), G-5 | Immediate re-read agrees on every shot (0 disagreements in ≥10⁵); a second client correlated with the first agrees on every shot; the server state is bit-identical before and after the read | any disagreement, or any change to the server state | none (new) |
| C4 | Detector merging | (iii) | Merging two channels leaves every untouched outcome's weight unchanged within 3σ and gives w_{k∪l} = w_k + w_l, on link channels of the canonical rule; \|a\|^p controls (p ≠ 2) shift by > 5σ | Q-share shifts, or controls do not | paper Sec. 3.3 table (Fraunhofer, illustrative): \|a\|² 0.360/0.360; \|a\| 0.349/0.429; \|a\|³ 0.367/0.297 |
| C5 (L2.0-C5, added v3.1) | d = 2 / link-channel reads | R-d2; gap G-7 | (a) interface audit: every read primitive (canonical harness and §5.5 pointer API) is written as rule unitary + exclusive link-channel read; (b) σ-only and τ-only reads done by a factor-dependent hop then link channels give \|w_n − ⟨Π_n⟩\| ≤ 3σ over ≥ 50 directions n, ≥ 5 states (including entangled τ–σ–position), ≥ 10⁵ shots, ≥ 5 seeds; (c) embedding consistency w(1⊗P_n) = Σ_j w(Π_j⊗P_n) within 3σ for ≥ 3 fine-grainings; (d) controls [1+(n·r)³]/2 and per-pair-normalised \|a\|^p (p = 1, 4) rejected at > 5σ | any read primitive that is not unitary + link channels (R-d2 stays an open assumption carried by S1), or any 3σ deviation in (b)/(c), or a control not rejected | none; (a) is expected to fail for the §5.5 API as written (a finding, not a run) |

**L2.0 entry gate.** L1 exit gate (the canonical rule is fixed, so Step 1 is tested on the rule that will be used).
**L2.0 exit gate.** Either (a) the sketch is written out with every assumption listed (per-channel (i), locality, the client-record object of G-4) and C1–C5 pass, in which case S1 is recorded as **narrowed to postulate (i)**. If C1–C4 pass but C5(a) finds a two-dimensional read primitive that is kept, S1 is recorded as **narrowed to (i) plus assumption R-d2**; or (b) a gap is confirmed (for example C1 finds another local conserved density), in which case S1 stays open and the failure is kept as a result. Under neither outcome is S1 recorded as closed; closing it requires deriving (i) from T and Û_net.
**Status.** Design only. C1 and C2 have seeds on an older rule; C3 has none; C4 has only the illustrative Fraunhofer check; C5 has none (its part (a) is a read-only audit and can be done before L1 closes). **d = 2 status:** not closed unconditionally; closed given R-d2 (by Step 3 under (i), or by Gleason on ℓ²(BCC) ⊗ ℂ⁴ under non-contextuality).

### L2.1 Born odds and CHSH with the energy-share read assumed — S7

The paper already reports CHSH 2.828, I₃≈0, no signalling, with cos² not coded. **This is a reproduction test of S7, not a test of S1:** it assumes the energy-share read. What is missing is a harness that makes the claim auditable: the read must use only the conserved link charge, and the entangled pair must be produced by a client-side split, not inserted. Pass: `S=2.828±0.005` (QM reference for the ideal state), `|κ|<1e−3`, marginal shift `<2σ`. Controls: |a| and |a|⁴ must fail (S≈1.66, 3.77). **Falsifier:** energy share does not reproduce the square. Entry gate: L1 exit gate (may run in parallel with L2.0).

### L2.2 Three-slit κ — S7

Same rule, three-slit geometry, two intensities. Pass `|κ|<1e−3` at both (internal precision gate; measured bounds above). This is the sharpest tabletop-adjacent test in the paper.

### L2.3 Order independence of spacelike reads — S2, OP3

Enumerate server read orders in the delayed-choice geometry. Pass: max |ΔP| < 3σ. Falsifier: any client-visible order dependence.

### L2.4 Exchange phase and exclusion — OP2

Two identical excitations on the BCC patch, exchanged along two paths; measure the two-particle phase. Pass: −1 for the fermionic sector, +1 for the bosonic, with the spin-statistics link arising from the rule rather than assigned. This is a hard, honest test: a toy that only re-labels antisymmetry will fail the "not imported" criterion.

### L2.5 Shared records — OP3

Many-particle joint states held as single-writer records: pass if a 3-particle GHZ-style record reproduces the quantum marginals and no-signalling, and if the single-writer constraint does not serialise independent pairs.

**L2 exit gate (per item).** L2.0 exit (a) or (b) recorded; L2.1–L2.5 each pass or fail on its own gate. Higher layers rely only on the items they use.

---

## 5. Layer 3 — gravity (OP4–OP11, OP17)

Ordered by increasing difficulty; each item names what would count as failure. Each run names its load rule (§0.4); congestion ON; no self-load unless an approved rule supplies it. **L3 gates are per item:** each Gi passes or fails on its own row, and a downstream item may use only the items it depends on that have passed (or must carry the label "conditional on Gi open"). L3 as a whole is closed only when every row has passed; with G1 open it cannot close.

**Diagnostic-branch note (v3.4, Edmond B2).** The G1 finite-screen numbers (§5 G1 note), the photon-bending runs (§10) and any other L3 result that rests on the OP4 rule or its continuum bridge are diagnostic-branch results. They are kept, and they do not count toward a gate until redone on `dirac4`.

**Entry rule.** An L3 item that uses the L1 3D node symbol may not start until L1's exit gate is met. Items whose harness does not use that symbol (G1's continuum ray solver, G3's 1D zigzag walk) may run earlier as labelled *pre-L1 pilots*; their results are reported but do not count toward the L3 gate until repeated on the canonical 3D rule.

| Test | OP | Setup (rule) | Measured target | Gate (this item only) | Falsifier | Status (2026-11-09) |
|---|---|---|---|---|---|---|
| G1 light bending, γ | 7 | weak-field sequence, same source and boundary on both sides; bending and Shapiro (rule declared per §0.4) | Cassini γ−1 = (2.1±2.3)×10⁻⁵, valid only in the weak field | γ extracted from the ε → 0 limit within Cassini's error, isotropic to 0.5%, no floor under refinement | residual floor | **Open, not passing; weak-field γ not yet measured** (see G1 note) |
| G2 compounding β | 8 | neighbour clock relay, Mercury orbit (paper load-first rule) | \|β−1\| < 8×10⁻⁵ (Will 2014, Table 4) | β from the rule within that bound | β→0.5 | toy-level β = 1 (paper OP7/8); conditional on G1 open |
| G3 EP for composites | 4,7,8 | 1D Dirac zigzag apps, H = f²·hop + f·(mass+binding), paper f = e^{−U} rule (`/workspace/op15ep/ep2.py`, GPU port `/workspace/gpu/equalfall/`); pre-L1 pilot | MICROSCOPE η(Ti,Pt) = [−1.5 ± 2.3(stat) ± 1.5(syst)]×10⁻¹⁵ | η falls with refinement (h² or faster) and its extrapolation is compatible with MICROSCOPE | η flat with refinement | **PARTIAL (corrected from v2):** refinement to s = 8 was run (Nov 1); lattice artifacts gone, but bound-vs-free plateaus at ~6×10⁻⁴ (weak/medium binding) and 5.8×10⁻³ (internally turning case), floors set by the harness readout; EP is an input (all terms on one tick clock); MICROSCOPE far out of reach |
| G4 tensor source | 8 | rotating + pressure source | GP-B geodetic −6601.8 ± 18.3, frame-dragging −37.2 ± 7.2 mas/yr (Everitt et al., PRL 106, 221101 (2011)) | coupling 2 from rule, not inserted; GP-B within errors | scalar-only result | not started; conditional on G1 open |
| G5 Planck-mass node | 6 | single node at m_P, then spread | none (mechanism-first) | GR recovered when load spread; finite core | divergent / no crossover | not started |
| G6 1-loop anisotropy | 17 | canonical rule + Wilson, self-energy | **named coefficient:** isotropic photon–electron speed difference, SME combination κ̃_tr − (4/3)c_e^{00}, measured −5.8×10⁻¹² ≤ κ̃_tr − (4/3)c_e^{00} ≤ 1.2×10⁻¹¹ (Hohensee et al., PRL 102, 170402 (2009)); see note | induced value inside that interval with no fine tuning; anisotropic part ≤ C(E/E_P)² | unsuppressed term | not started |
| G7 core dynamics | 9–11 | collapsing shell on the load rule | none (mechanism-first) | stable finite core; inner horizon stated | mass inflation / no cap | horizon design: existing rules give **no horizon** (s, F, ρ never reach 0; these are OP4 symbols per §0.4, so this is a diagnostic-branch result), whereas GR's isotropic lapse reaches 0 at r = M/2; design only |

**G1 note: what 0.970 is, and why Cassini is not its comparator.** Verified against `/workspace/gpu/op4_bcc_local/curved_reference_design/photon_field_refinement_20261108/results.json` and `../photon_priority_comparison_20261108/REPORT.md`:

- *Quantity.* 0.970 is the ratio of **finite-screen exit-direction ("parallel steering") angles** of continuum null rays: ledger (OP4 continuum bridge, V = s, F = s², W = 1/s) versus an exact Schwarzschild ray from the same initial data, read at the domain exit (isotropic radius ≈ 31). It is **not** the asymptotic infinity-to-infinity deflection; the run's own report says not to compare it with 4M/b or call it a factor-2 test.
- *Numbers.* Geometry A: ledger 0.19812 vs GR 0.20427 rad, ratio 0.9699 at h = 0.5 (0.9680 at h = 1). Geometry B: 0.19828 vs 0.20427, ratio 0.9707 (0.9709 at h = 1). Under field refinement h = 1 → 0.5 the gap moves in opposite directions: A closes from 6.532 to 6.149 mrad, B opens from 5.941 to 5.988 mrad. Stable to about 0.4 mrad, but two grids cannot separate a residual floor from slow convergence; an h = 0.25 run is needed. Out-of-plane component at h = 0.5: A 9.06e−4 rad (0.46% of in-plane; 0.65% at h = 1), B 1.06e−5 rad (0.005%). Method: two geometries (A, B), Poisson field solve on the BCC grid, continuum ray integration; not a 13-direction test.
- *Field strength.* M = 40/(8π) ≈ 1.59, b_∞ ≈ 26.6, so ε = M/b ≈ 0.060. Cassini's ray had ε ≈ 1.3×10⁻⁶ (b ≈ 1.6 R_⊙), about 4.5×10⁴ times weaker. This is a **strong-field** toy.
- *Naive conversion, stated plainly.* If the ratio were a weak-field total deflection, (1+γ)/2 = r would give γ ≈ 0.940 (A) / 0.941 (B), i.e. **γ − 1 ≈ −0.060 / −0.059**, about **2,600σ** (2,618σ A, 2,550σ B) from Cassini's (2.1 ± 2.3)×10⁻⁵. That is a gap of thousands of σ, not "3%".
- *Why that conversion is not legitimate here.* (1) At ε ≈ 0.06 the second-order GR term is about (15π/16)ε ≈ 18% of the asymptotic deflection, six times the gap, so the gap cannot be assigned to γ alone. (2) The two sides do not share a source: the ledger field comes from 27 point emitters with U = 0 at r = 38.5, whereas GR uses a point mass in unbounded space. (3) The run's own linear (Born) control shows the bridge gives exactly twice the lapse-only value, i.e. γ = 1 at linear order. That is **by construction** of the adopted bridge F = s², W = 1/s, not derived. The full ledger value is 6.8% above its own linear value, so the 3% gap sits in nonlinear and source/boundary terms.
- *Comparator.* Cassini is the right comparator only for a weak-field γ, which has **not been measured** for this rule. No measured light deflection exists at ε ≈ 0.06. The nearest measured strong-field photon test is the EHT shadow size of Sgr A*, δ = −0.08 ± 0.09 (VLTI) / −0.04 (+0.09, −0.10) (Keck) (EHT Collaboration, ApJL 930, L17 (2022)). That is a different observable (photon-ring size, ε ≈ 0.19), so it is not a direct comparator either.
- *Required next step (needs a design and Edmond's approval).* A weak-field sequence (ε from 10⁻² down to ≤ 10⁻⁴) with the same source and boundary on both sides (or GR evaluated on the ledger's own potential), extracting γ from the ε → 0 slope. Only that number goes against Cassini.

The paper's OP7 text (γ = 0.999 ± 0.001) came from an earlier load-first link rule (the paper's f = e^{−U} convention), a different mechanism, with weak-field extrapolation, and itself notes toy precision about 40× short of the Cassini bound. Both results are kept.

**G6 note: why that coefficient.** A cubic (BCC) lattice cannot produce a direction-dependent dimension-4 photon term: the anisotropic coefficients κ̃_e− form a symmetric traceless rank-2 tensor, and cubic symmetry forbids any nonzero one. The radiative danger at dimension 4 (Collins et al. 2004) is therefore an **isotropic, species-dependent** limiting speed, which is the combination κ̃_tr − (4/3)c_e^{00} bounded above. Lattice-frame anisotropy first appears at rank 4 (dimension ≥ 6), which is covered by the L1.4/L1.5 GRB limits. For reference, κ̃_e− is bounded at the 10⁻¹⁸ level (Nagel et al., Nat. Commun. 6, 8174 (2015)); a nonzero κ̃_e− would indicate broken cubic symmetry in the rule.

G3 is the cleanest available pilot; G6 is the decisive item and the paper's own top risk.

Reference values (not targets): GR's 42.98″/cy for Mercury and 4GM/(bc²) for bending are GR predictions; the gates above use measured PPN bounds instead.

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

**v3.4 note (Edmond B2).** The no-go above was established on OP4's four nodes and OP4's corner-mass terms, so it is a diagnostic-branch result; it is to be redone on `dirac4`. The M3 entry gate below is unchanged.

**M3 entry gate (new).** A written mechanism with its physical reason ("each level costs X because of Y"), hashed before comparison, with no free coefficients chosen to hit the targets. **Koide** is used only as a test of the measured masses (Q = 0.666664 ± 0.000005 from PDG 2024), not as a separate target to be fitted. M3 is time-boxed; a further no-go is a valid result.

M1 is the only one that is a normal simulation.

(v1's M4, dark-matter identity, OP18, is moved to Appendix A.)

---

## 7. Layer 5 — cosmology (OP19, S3, S5, S6)

| Test | OP | Measured target | Pass | Note / status |
|---|---|---|---|---|
| C1 halo outer slope | 19 | **pre-registered below**: CLASH stacked Σ(R), Umetsu et al. 2016. v1's r⁻³ is the NFW form from simulations, kept as a reference value | χ² p ≥ 0.05 against the pre-registered data, no free shape parameters | current toy slope −2.3; expanding grid + infall |
| C2 soliton core | — | none measured; v1's "3–6% vs Schive" compares with a simulation (Schive et al. 2014), kept as a reference value, not a gate | — | already matches the reference |
| C3 n_s, r | S6 | n_s = 0.9649 ± 0.0042 (Planck 2018); r < 0.036 (95%, BK18) | n_s within Planck's errors; r below the BK18 limit | Paper's toy values n_s = 0.9658, r = 0.0022 (b=1) are *model outputs*, not targets. Against the measured numbers they currently pass (n_s within 0.2σ; r below the limit), but log-load counting and b are chosen, not derived (S6), and it is QFT on a background, not a lattice |
| C4 vacuum energy | S3, S5 | none for S3 (**mechanism-first**); S5's size ρ_Λ/ρ_P ≈ 1.1×10⁻¹²³ is derived from measured Λ | a written suppression mechanism with a stated reason; S5 derived without a horizon input | no simulation yet |

**C1 pre-registration (fixed now, before any run; changing it after seeing a result is fitting under §0.1).**
- *Dataset:* the stacked projected surface-mass-density profile Σ(R) of the 16 X-ray-selected CLASH clusters from the joint strong-lensing, weak-lensing shear and magnification analysis of Umetsu et al., ApJ 821, 116 (2016), with its published radial bins and full covariance, used unchanged. That stack is fitted well by NFW, Einasto and DARKexp and disfavours power-law, cored isothermal and Burkert profiles; its NFW fit gives c₂₀₀c = 3.79 (+0.30, −0.28) at M₂₀₀c = 14.1×10¹⁴ M_⊙.
- *Radial range:* published bins with R ≥ 0.2 r₂₀₀c and R ≤ 2 Mpc/h (one-halo regime; no two-halo term is added to the model, so the outer bins beyond that are excluded in advance).
- *Model mapping:* the toy's radius is scaled by its own r₂₀₀c (computed from the toy's density against the toy background), and its mass normalisation is set by the measured M₂₀₀c. There are no free shape parameters. Σ_model(R) is the line-of-sight projection of the toy's 3D density out to 2 r₂₀₀c.
- *Statistic:* χ² of Σ_model against the data with the published covariance; dof = number of bins in range. Pass if p ≥ 0.05. The outer log-slope d ln Σ/d ln R over the same range is also reported, for information only.
- *Caveat (declared):* the toy is a light-scalar halo; outside the soliton core it behaves like cold dark matter, so a cluster-scale outer profile is a fair test of the outer slope, but not of the core. Edmond may replace the dataset **only before** any C1 run.

C1 is ready and cheap. C4 is not a simulation problem yet; it needs a mechanism first. S5 (per-node fee ~1e−123) and S6 (log-load counting) are derivation targets, not fits.

(v1's C5, CP bias, S4, is moved to Appendix A and made mechanism-first with no numerical target.)

---

## 8. Traceability: open problem → layer → first action

| OP | Layer | First action | Cost | Status |
|---|---|---|---|---|
| 1 | all | freezes with L0–L2; L0 names the canonical rule | — | open |
| 2 | L2 | exchange-phase toy | 1–2 wk | open |
| 3 | L1 | reason decision made (one BCC orbit; the 12 edge zeros are Γ images); OP4's 3 extra nodes recorded as a diagnostic finding; V5 v2 census accepted as the `dirac4` census | — | L1.1 closed; L1.2 closed; L1.3 closed |
| 4 | L3 | EP composite (G3), pre-L1 pilot: readout fix | 3–5 d | PARTIAL (s = 8 floors) |
| 5 | L3 | workload→metric map; start with G1 | 2 wk | open |
| 6 | L3 | single-node m_P toy | 1 wk | open |
| 7 | L3 | G1: design a weak-field ε → 0 sequence with matched source and boundary; the strong-field 0.970 is not a γ measurement | 2 wk | open; weak-field γ not measured |
| 8 | L3 | G2 + tensor source (G4), labelled conditional on G1 | 2 wk | open |
| 9–11 | L3 | G5–G7; horizon design (no horizon from existing rules) | 3–6 wk | design only |
| 12 | L4 | new mechanism with stated reason, preregistered; existing-rule no-go recorded (OP4 rule: diagnostic branch) | 2 wk | no-go for existing rules (OP4: diagnostic branch) |
| 13 | L4 | L-scan Binder + homing | 1–2 wk | open |
| 14 | L4 | RGE rerun (analysis) against measured m_H, m_t | 3 d | open |
| 15 | L1 | sky table + diffusion control against Fermi/LHAASO | 1 wk | open |
| 16 | L1 | linear-term test along [111]/[11−1] (tick-budget run) | 1 wk | OP4-rule design held (diagnostic); `dirac4` hand derivation and design needed |
| 17 | L3 | 1-loop induced κ̃_tr − (4/3)c_e^{00} | 2–4 wk | open |
| 18 | App. A | candidate-field definition (side item, Edmond to decide) | open | — |
| 19 | L5 | expanding-grid halo against the pre-registered CLASH stack | 1–2 wk | open |
| S1 | L2 (L2.0) | conservation-route derivation attempt: theorem sketch, gaps G-1 to G-7, checks C1–C5 | 1–2 wk | design only |
| S2 | L2 | read-order permutation | 3 d | open |
| S3 | L5 | mechanism first | open | open |
| S4 | App. A | mechanism first, no numerical target (side item, Edmond to decide) | open | — |
| S5 | L5 | derivation, no fit | open | open |
| S6 | L5 | derive log-load counting; score n_s and r against Planck and BK18 | open | open |
| S7 | L2 (L2.1–L2.2) | auditable energy-share read (reproduction; read rule assumed) | 3 d | toy-tested |

---

## 9. Interface contract (so layers do not rewrite each other)

```
ledger/
  bcc.py       links, dispersion, directions                [frozen]
  qwalk.py     1D/2D Dirac walk, exact checks               [frozen]
  dirac4.py    4-component symbols, gap, chirality           [L1; no repair applied]
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
5. `config` carries `congestion: "ON"` by default; `"OFF"` is accepted only with `diagnostic: true` and is excluded from gates. Exception: L1.1–L1.3 run on the load-free vacuum symbol (§0.1).
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

**[Superseded 2026-11-12: the twelve points are Γ images on the one-orbit lattice; kept as history.]** But the closure has **12 exact zero modes** at the edge labels `(±π,±π,0)` and permutations, with the Wilson layer present and `m=0`; `U = I` to 7e−16. They are independent of φ and vanish for `m>0`. The paper's random search cannot hit them (measure-zero set), so the statement "no zero-frequency point other than the physical one" needs the qualifier "in the interior" or a repair.

**[Superseded 2026-11-12: at (π,π,0) the symbol equals Γ because it is Γ on the one-orbit lattice; kept as history.]** **Why it happens.** At `(π,π,0)`, `u = cos kx cos ky cos kz = +1` and `n = 0`, so the Wilson symbol reduces to `e^{−iφτx} e^{+iφτx} = 1`, exactly as at Γ. The layer does not distinguish Γ from the edge labels. That is the defect.

**[Withdrawn 2026-11-12: not periodic under π(1,1,0); the one-orbit decision replaces it.]** **Candidate repair (tested, mixed).** Replace `u` in `X` by `u + g(k)` with `g(Γ)=0` and `g` order one at the edge labels, for example `g = (1/3)Σ(1−cos k_i)`; keep the second factor `e^{+iφτx}` so the cancellation at Γ survives, and use a matrix exponential if `X²≠1`. Result at φ=1.4: the 12 zeros lift (ω=0.637), Γ stays massless, and the smallest interior gap rises from 0.082 to 0.221. But `g` is O(k²) near Γ, so it also changes the low-energy dispersion; the light speed and the `(E/E_P)²` coefficient must be re-measured before this patch can be accepted. This is a concrete, falsifiable next step, not a rewrite. (The chosen `g` must be written down with its reason before re-measuring; it is not tuned to the dispersion targets.)

**[Answered 2026-11-12 by the one-orbit reason: k = (π,π,0) is Γ on the one-orbit lattice, so the reason survives an even-L finite lattice.]** **Caveat.** If these boundary modes are declared unphysical, the model owes a reason that survives a finite lattice with even L, where `k=(π,π,0)` is an allowed momentum. That is a model decision, not a numerical one.

**[Diagnostic branch.]** **OP4 nodes (symbolic, 2026-11-09).** 4 Weyl nodes per block (Γ, H, P, P′), chiralities (+,−,+,−); KS staggering frustrated on BCC; naive BCC zero lines at k_i = k_j = π/2 persist under staggering. Source: `/workspace/bcc_staggered_design_20261109/`.

**[Diagnostic branch (OP4 nodes); to be redone on `dirac4`.]** **Generation split (run once, 2026-11-09).** No-go for existing rules (see M3). Source: `/workspace/bcc_generation_split_run_20261109/`.

**[Diagnostic branch (OP4 bridge); to be redone on `dirac4`.]** **Photon bending (2026-11-08).** Congestion-ON OP4 continuum bridge: finite-screen steering 0.970–0.971 of the exact Schwarzschild value at ε = M/b ≈ 0.060 (strong field), stable to about 0.4 mrad under field refinement h=1→0.5 but moving in opposite directions (A gap closing, B opening), so floor vs convergence is unresolved until h=0.25 (138/138 checks). Not a weak-field γ measurement; read naively as (1+γ)/2 it would mean γ−1 ≈ −0.06 (≈2,600σ from Cassini). See the G1 note in §5. Source: `/workspace/gpu/op4_bcc_local/curved_reference_design/photon_field_refinement_20261108/`.

**EP composites (2026-11-01).** G3 refinement to s = 8 completed: PARTIAL, floors ~6×10⁻⁴ and 5.8×10⁻³ set by the readout. Source: `/workspace/gpu/equalfall/SUMMARY.md`.

---

## 11. Recommended first sprint (2 weeks) and realistic L1 timeline

**Consistency rule (resolves v2's contradiction).** L2/L3 work that uses the L1 3D node symbol does not start before L1's exit gate. Work whose harness does not use that symbol may run as a labelled pre-L1 pilot (§5 entry rule). G3 qualifies: its harness is the 1D Dirac zigzag walk of `/workspace/op15ep/ep2.py` with the paper's f = e^{−U} weights, not the §6.2 or OP4 3D symbol. Its result counts toward L3 only after a repeat on the canonical 3D rule.

Sprint (2 weeks):
1. **L0 canonical-rule decision** (Edmond) — 0.5 d. **Done: `dirac4`.**
2. **L1.1 doubler census** (OP3). **Done 2026-11-12 (closed):** one-orbit reason decision plus the V5 v2 census accepted as the census (Edmond B4, 8:11 PM). The OP4 branch is a diagnostic finding only.
3. **L1.2 chirality chain reproduction** (Table `dw`) — 2–3 d. Required by the L1 exit gate; omitted in v2's sprint. **Done 2026-11-12 (closed).**
4. **L1.3 ν derivation** (OP3). Run `9ccf4855`: R1 PASS, R2 FAIL / OPEN, S3 not run; R2 recorded as open as written; L1.3b (PR #10, run PR #12) PASS; **L1.3 closed on L1.3b** (Edmond, 8:32 PM).
5. **L1.5 linear-term test** (OP16). The held design is for the diagnostic OP4 rule; a `dirac4` hand derivation and design come first, then Edmond's approval of caps.
6. **G3 pre-L1 pilot** — a readout fix (longer fit window or a different readout), since more refinement will not move the floors. Labelled pilot.
7. **L2.0 design review** (no run) — Edmond reviews the theorem sketch, gaps G-1 to G-7 and the C5 audit (part (a), read-only).

**Realistic L1 close.** L1 cannot close inside this sprint. L1.3 is closed; L1.4 and L1.5 need designs and approvals. A repair-induced re-measure of L1.4 and L1.5 is no longer needed, because no repair is applied. The earlier "4–6 weeks" estimate is withdrawn and is to be re-estimated once the L1.4 and L1.5 designs exist. Until L1 closes, L2.0–L2.5 and every L3 item except the labelled pilots wait.

---

## Appendix A — Possible side items (Edmond to decide)

Edmond has said the open-problems list should be kept strictly to what upholds the theory. The items below are **not deleted**. They are taken out of the main layer line until Edmond decides whether they stay.

| Item | Paper ref | v1 location | Why it may be a side item | If kept |
|---|---|---|---|---|
| M4 dark-matter identity | OP18 (Sec. 6.20) | L4 | Asks *which* excitation dark matter is; the halo tests (OP19, C1–C2) do not depend on the answer | L4, mechanism-first: a candidate field with a stated reason, no fit |
| C5 CP bias / baryon asymmetry | S4 (Sec. 3.6) | L5 | Server-side; the paper has no model; needs three generations, which are a no-go under existing rules (M3; established on the OP4 rule, a diagnostic branch) | L5, **mechanism-first with no numerical target** (the measured baryon-to-photon ratio, η ≈ 6.1×10⁻¹⁰, is recorded for later use only) |

**Coverage, for Edmond to confirm.** With OP18 and S4 in this appendix, the main layer line covers **18 of the 19 open problems** (all but OP18) and **6 of the 7 server-side items** (all but S4). Neither is deleted from the paper. If that is not intended, both return to L4/L5 as mechanism-first items.

Other candidates Edmond may want to look at with the same question (left in the main line for now): C2 soliton core (no open-problem number, no measured target), and the neutrino parts of OP12 (splittings, PMNS, absolute scale).
