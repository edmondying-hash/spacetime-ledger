# Current status supplement, 2026-11-15

Recorded 2026-11-15 (UTC), when the 2026-11-14 records were copied onto `main`. The decisions below are Edmond Ying's of 2026-11-14 (America/New_York), as approved for this sync. This file is progress tracking. It does not edit layered plan v3.4, `space-ledger-v2.md`, `space-ledger-v2.pdf`, or any file copied from the archive. Where it disagrees with a status line inside the hashed plan, it supersedes that line only as a record of what has been run or closed. It does not change the scientific design.

The copies are the archive `records_20261114.tar.gz`, sha256 `ead82e32b13380f88d3d9958aacd43993352d092886bd93f2c5d2c6ad159aec0`. Each of the eleven folder `SHA256SUMS` manifests was checked read-only after extraction (`sha256sum -c`: every listed file OK). No supplied file was edited. `__pycache__` was not in the archive.

Paper and plan, unchanged by this sync (same bytes as `main` at `3f29cc90c927b1518cea73c5ba796718029b1cdf` before the copy):

- `space-ledger-v2.md` sha256 `ce22701ca6e5e2dfa143ab43a6062e80025c1afeba5137f7e271c239bc75555c`
- `space-ledger-v2.pdf` sha256 `1036664bff90fb6d96f64e07b6e6f06bcf28a0382a370f7e0bba8f3f5f1b07f5`
- `layered_plan_v3_4_draft_20261112/layered_plan_v3.4.md` sha256 `a50dd0a0d5c9304e782d8482905167d797f4973106d9a27326c69572a1e846cf`

The plan's own status lines stay as signed off. In particular, L1.5 is still "open" at plan line 201, the B2 scope reading is still marked pending at plan line 136, and L2.0 is still "Design only" at plan line 255. Those sentences sit inside the hash.

## L0′ simple-cubic census r1

Design [`L0p_census_design_r1_20261114/L0P_CENSUS_DESIGN_r1.md`](L0p_census_design_r1_20261114/L0P_CENSUS_DESIGN_r1.md), sha256 `c2673a6426ca5728738c7e7e63871bd26577e8475e9b2819d9980aeccb642fd1`. The design's trigger is: fall back to BCC/`dirac4` if no simple cubic candidate passes F1–F5, the knob rule, and the simplicity test, and read that outcome alongside the BCC baseline row.

Run [`runs_l0p/20261114_l0p_census_r1_c2673a64/`](runs_l0p/20261114_l0p_census_r1_c2673a64/). The repair-round table [`_global/S7_repair/READOUT.md`](runs_l0p/20261114_l0p_census_r1_c2673a64/_global/S7_repair/READOUT.md) (sha256 `5d1764c36f4a4194a2fcd6e4b9041b2be323ace523f47973de1b87f111456218`) labels no simple cubic candidate (C1–C4, RC3) MET in every column. The trigger condition holds in that round. The BCC baseline row B0 is also not MET in every column; the fallback is the fork rule, not a claim that B0 passed the census. Code and the problem statement, copied unchanged: [`L0p_census_r1_code_20261114/`](L0p_census_r1_code_20261114/), [`L0p_real_problem_final_20261114/`](L0p_real_problem_final_20261114/).

On 2026-11-14 at 6:59 PM ET, Edmond chose the BCC/`dirac4` fallback under that fork rule, with no census rerun, and resumed at L1.5 (B9, then the L1.5 closure, then L2.0). That choice is recorded in the L1.5 closure, section 5. No census rerun is in this archive.

## L1.1–L1.5

L1.1, L1.2, and L1.3 were already closed on `main`. L1.4 is closed by [`L1_4_CLOSURE_20261113.txt`](L1_4_CLOSURE_20261113.txt), already on `main` before this sync.

L1.5 closure text [`L1_5_closure_draft_20261114/L1_5_CLOSURE_20261114.txt`](L1_5_closure_draft_20261114/L1_5_CLOSURE_20261114.txt), sha256 `6c42a3956592d1dd01c847173e11a38e46c1e4355f0e4a92e36084fc7eb1b09e`. Edmond accepted that text at 9:54 PM ET on 2026-11-14. The file is copied unchanged. It still says, inside the hash, that it takes effect when accepted and that it had not been pushed; this supplement is the later record of the acceptance and of the copy onto `main`. The closure authorises no paper edit and no plan edit. The L1.5a / L1.5b verdict run and the B_m comparison run are not in this repository; the closure cites them by hash.

Open items the closure carries forward, and does not decide, include B9 K1 (the gravity map) and B9 K2. The list is section 6 of the closure.

## B9

B9, the clock-factor check, was run once. Design [`B9_clock_design_spacetime_20261113/B9_CLOCK_DESIGN.md`](B9_clock_design_spacetime_20261113/B9_CLOCK_DESIGN.md), sha256 `b1a7102db33df9769a97c0495c710a9bf494fd26d7c4d498d0e5e648c34af728`. Run [`runs_b9/20261114_b9_b1a7102d/`](runs_b9/20261114_b9_b1a7102d/), read-out [`READOUT.md`](runs_b9/20261114_b9_b1a7102d/READOUT.md). Harness status S0–S4 PASS, S5 RECORDED. I3, I4, and I5 were computed and reported. None was adopted. K1, which gravity map to use (I3, I4, I5, a combination, or another), stays open for the gravity layer. B9 is not a derivation of a gravity map and is not a selection of one.

## L2.0

Design [`L2_0_design_spacetime_20261113/L2_0_RUN_DESIGN.md`](L2_0_design_spacetime_20261113/L2_0_RUN_DESIGN.md), sha256 `833f49f26418b2267cc0a9b389a46220078b453eebe92cf149145af330077ed9`. That design was run. L2.0 is not closed and is not passed. These records do not derive the Born rule. The design's own claim, if C1–C5 were to pass, would only narrow S1 to postulate (i), or to (i) plus R-d2. That pass did not occur.

Two run folders are kept, both under the same design hash:

- Original run [`runs_l20/20261114_l20_833f49f2/`](runs_l20/20261114_l20_833f49f2/), 2026-11-14 22:09–22:11 EST, one attempt. Read-out [`READOUT.md`](runs_l20/20261114_l20_833f49f2/READOUT.md). S0 PASS. C1 UNINFORMATIVE. C2 FAIL (one of 270 Q-share channel tests beyond 3 sigma, z = 3.145; three control cells also have no channel above 5 sigma). C3 PASS. C4 FAIL. C5(a) does not pass: the read-only audit [`L2_0_C5A_AUDIT.md`](L2_0_design_spacetime_20261113/L2_0_C5A_AUDIT.md) (sha256 `423920fe845e26df1871e0e2a5ebc044c780735919c1df1af3c47ecabf683090`) finds no audited read primitive written as a rule unitary followed by an exclusive link-channel read. C5(b), C5(c), and C5(d) are UNINFORMATIVE on this run because the meter killed C5 on the RSS cap (sampled tree RSS 532.8 MiB, cap 512 MiB); they are not a scored 3-sigma result. C5 overall not passed.
- Code-fix continuation [`runs_l20/20261114_l20r2_833f49f2/`](runs_l20/20261114_l20r2_833f49f2/), 2026-11-14 22:30 EST, S0, C4, and C5 only. The glue-code fixes are [`L2_0_r2_codefix_20261114/R2_NOTE.md`](L2_0_r2_codefix_20261114/R2_NOTE.md): C5 no longer retains the post-hop arrays, and C4 draws shots from a generator keyed by `(seed, partition index)`. C1, C2, and C3 were not rerun; their labels stand from the original run. Read-out [`READOUT.md`](runs_l20/20261114_l20r2_833f49f2/READOUT.md). S0 PASS. C4 FAIL. C5(a) does not pass (same audit, not rerun; the primitive issue remains). C5(b) FAIL: 7 of 2,500 official cells beyond 3 sigma (max z 4.208). C5(c) FAIL: 3 of 1,800 cells beyond 3 sigma (max z 3.555). Those are the design's any-cell 3-sigma gates. C5(d) PASS (g3 rejected on 117 of 480 tests, g1 on 114 of 480, g4 on 116 of 480, each beyond 5 sigma on all five seeds). C5 overall not passed.

C4, as scored on the code-fix continuation: the design's per-site controls use w_k proportional to the sum of |a_i|^p over channel k. That weight is additive under merging, so the merged and unmerged control weights match before shot noise ([`DISCLOSURES.md`](runs_l20/20261114_l20_833f49f2/DISCLOSURES.md) item 3, applied unchanged). Neither p = 1 nor p = 4 shifted by more than 5 sigma (largest control z 2.74). One Q-share cell is also outside 3 sigma (quadrants, seed 20261114, z_D = 3.05). The design's C4 fail line is a Q-share shift beyond 3 sigma, a Q-share additivity failure, or both controls failing to shift at > 5 sigma.

The name `l20r2` is this completed code-fix continuation of design `833f49f2…`. It is not a new design. A separate design revision, with channel-level Q^q controls and multiplicity-aware gates, is being prepared and reviewed elsewhere. That revision is not in this archive, is not run-authorized, and is not these folders.

## Records added

| Path | Role |
|---|---|
| `L0p_census_design_r1_20261114/` | L0′ census r1 design |
| `L0p_census_r1_code_20261114/` | census code, as run |
| `L0p_real_problem_final_20261114/` | problem statement |
| `runs_l0p/20261114_l0p_census_r1_c2673a64/` | census r1 run |
| `L1_5_closure_draft_20261114/` | L1.5 closure text and PDF |
| `B9_clock_design_spacetime_20261113/` | B9 design |
| `runs_b9/20261114_b9_b1a7102d/` | B9 run |
| `L2_0_design_spacetime_20261113/` | L2.0 design `833f49f2…` |
| `runs_l20/20261114_l20_833f49f2/` | L2.0 original run |
| `L2_0_r2_codefix_20261114/` | glue-code fix note and scripts |
| `runs_l20/20261114_l20r2_833f49f2/` | L2.0 code-fix continuation (`l20r2`) |
