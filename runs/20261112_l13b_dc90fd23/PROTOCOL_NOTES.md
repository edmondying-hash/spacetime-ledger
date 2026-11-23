# L1.3b run 20261112_l13b_dc90fd23: protocol notes, written before any computation

Design: design/L1_3b_RUN_DESIGN.md, sha256 dc90fd231d9a92602187f61dc68bded2891b3ece5274290ba18b75f86d604a8d, copied unchanged from branch cursor/l1-3b-run-design-a445 (commit 9da63d53f354295f363801a919739177fdc9c765, PR #10).
Approval: inputs/L1_3b_run_design_20261112_DECISIONS.txt (sha256 c2081f1852847777e3acf931442890a1d80dcc7768b582af6da423029c995e9c) records Edmond Ying, 2026-11-12 8:12 PM America/New_York, "L1.3b approved", taken as approval of dc90fd23... with D1-D5 defaults; Edmond's Slack DM to the Grok bot, 2026-11-12 8:14 PM America/New_York: "approved to proceed with L1.3b". Neither message quotes the hash (design Sec. 9.1 asks for a one-line approval naming it); disclosed, not resolved here.
Scope: S0-S3 only, design Sec. 6 caps. No paper, plan, README or repo edit.

## Implementation
- U-builder: harness/l13_primary.py, copied unchanged from run 20261112_l13_9ccf4855 (identical to PR #8 commit f4e45728), sha256 5e606a0631b0124992d65f22dd15ffb90e9ad388706c73a9b7739cb388870d8e; only lines 51-96 are called. Its main() is not run.
- Measurement code (new): harness/l13b_measure.py, hashed in PRE_RUN_SHA256SUMS and MEASUREMENT_CODE_SHA256.txt before any comparison.
- Meter: harness/meter.py copied unchanged from 9ccf4855 (threads pinned to 1, 600 s per-step kill, peak tree RSS sampled every 0.2 s).
- Frozen module: frozen/dirac4.py, copied from runs/20261112_l12_7e09b7c4/frozen/f71c782e/dirac4.py, sha256 f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff; imported only in S3 after out/S3/result_S3_primary.json is written.
- N4 source: inputs/V5v2_census_results.json, copied from L0_V5v2_official_20261111/v5v2_official/results.json (sha256 ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708); read, not re-run.
- Runner: bigbang (gn100-7c00), L1.2 venv (Python 3.12.3, numpy 2.5.4) used read-only.

## Pre-declared readings (fixed before computation)
- RD-1 Gating: S1 needs S0 PASS (P0-P5); S2 needs S1 PASS (R1'); S3 needs S2 PASS (R2b). A refused step is recorded as REFUSED/"not run". R2c Q1/Q2 never gate.
- RD-2 R1' pass includes "v0 rounds to the printed value" (3 dp, every direction) at the 7 tabulated phi (0.5, 0.8, 1.0, 1.2, 1.4, 1.5, pi/2), as written inside the design's Pass bullet.
- RD-3 Spread of v0 over the 13 directions = max - min. ||.||_inf = max absolute row sum of (M^dag M - I).
- RD-4 b, c = coefficients of kappa^1, kappa^2 of the degree-4 interpolant through the five (kappa, v) points (Vandermonde solve in kappa/0.016). Its constant term is recorded beside the Neville v0.
- RD-5 Mid-run unitarity residuals of U are recorded for every measurement, not used as a gate (N1 is the unitarity test).
- RD-6 P1 uses the 16 R1' phi plus 0.0, 0.05, 0.2; P3 also checks U(k=0) = 1 for all 49 R2b pairs; P4 uses 20 random k, phi = 1.4, the 12 shifts pi(+-1,+-1,0) and permutations (L1.3 design Sec. 3 residual limits).
- RD-7 P5 phi for c0(phi,phi): 0.5, 0.8, 1.0, 1.2, 1.4, 1.5, pi/2; symmetry pairs: (0.5,1.3), (0.2,1.4), (0.8,pi/2), (1.0,1.2), (0.2,0.5).
- RD-8 N1 grids as in 9ccf4855: phi = pi*i/400 (i = 0..400) for A, S, V and U(phi,phi); pair grid pi*i/40 (41 x 41) for U(phi2,phi4); 200 random k each.
- RD-9 N2: central difference (v0(1.5) - v0(1.3))/0.2 per direction on R1' values; holds iff min |fd| > 1e-4. N3: strict monotone iff v0_min(next phi) - v0_max(previous phi) > 1e-6 on the 18 sorted phi (16 R1' + 0.0, 0.05); span iff the phi=0 and phi=pi/2 values are within 1e-6 of 0.5 and 1.
- RD-10 N5: lines containing "1.4" (not part of a longer number) and an angle word, in paper Sec. 6.2 (lines 419-626), plan v3.3 r2, the two L1.1 reason notes, the r8 repair spec and its sign-off. Every hit is recorded verbatim; hits with a keyword (derive, determine, fixed by, fixes, select, forced, required by, unique, predict) are flagged and each flagged hit is read and classified in the post-run record. Only a statement that derives phi = 1.4 from the rule counts as "a derivation".
- RD-11 Cross-check (design Sec. 5): the frozen U_cycle takes one phi, so for the 49 pairs the frozen module's own V_step/S_step are composed in U_cycle's order, V_step(-1,k,phi4) S_step(-1,k) V_step(+1,k,phi2) S_step(+1,k); diagonal pairs and the 16 R1' phi also go through frozen U_cycle(k, phi) directly. Recorded: max |U_primary - U_frozen| and max |v0 difference|.
- RD-12 Caps: address-space ulimit 2 GiB (stricter than the 2 GiB soft RSS ceiling), 1 thread, meter kill at 600 s per step, run_step.sh refuses a step once 1800 s total wall is used; output checked against 64 MiB at the end.

## Disclosures
- Before hashing, the measurement code was exercised once on the box (not bigbang) in /tmp with a MOCK U-builder (synthetic unitary, not the dirac4 symbol), a mock frozen module, dummy text files and test-only tolerance overrides, to catch crashes. One crash (index error on the mock's short file) was fixed by guarding the slice. Neville/poly_coeffs were checked on a synthetic polynomial. No value of the real symbol was computed and nothing was compared with a closed form.
- The environment check on bigbang imported numpy and ran eigvals on the 4x4 identity under ulimit -v 2 GiB (VmPeak ~105 MiB). No physics computed.
