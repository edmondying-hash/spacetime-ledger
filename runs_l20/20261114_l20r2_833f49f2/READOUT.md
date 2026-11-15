# L2.0 r2 rerun read-out (S0, C4, C5 only)

Design `L2_0_RUN_DESIGN.md` sha256 `833f49f26418b2267cc0a9b389a46220078b453eebe92cf149145af330077ed9`; design folder SHA256SUMS `ae005712b98eb2263e702cdc5701abfd1fb0e9e0bef102367c40d28dab858edc` (re-verified before launch); `l20_measure.py` `08e98af5d2936474260f233f85c4b1ef06b4564d6533409f36c34a7bfa5dd516`; `frozen/dirac4.py` `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff`.
Code fix: `/workspace/L2_0_r2_codefix_20261114/` SHA256SUMS `c3157f47eac617955a7ec308badd8114823b3feb4f86541596a911efda00b275`; `R2_NOTE.md` `147971566943dfbc68e5811ac4dc16e9515210fb8fb06b5f2df1544ba170b12f`.
Harness (byte-identical copies of the code-fix folder): `harness/l20_score.py` `08d8e79fcdc7b1a84eb1d952c70b2e5286bcf34666f9ab6fc9f425537002506a`; `harness/run_all.py` `8f2fa8ef7f6671a8c0694226902d27d99338eac9675855ca91b85ace47e6244e`; `harness/meter.py` `29b968b434ed45b141824d80be96684ebc413bde77e3aa6dd55a2f099552eff1`; `harness/PRE_RUN_SHA256SUMS` `da880fc1e8e4c9cf18ccb9bc82c4787f58f636954ac45e9e5603660a5d59fba2`.
First run (not modified; C1, C2, C3 records stand from it): `/workspace/runs_l20/20261114_l20_833f49f2/` SHA256SUMS `355899be68345e063a9923280001325778fc1b7580dc35eeb9206c5245b850b2`, READOUT.md `e02398f9146b18a114212b4ab14b302d25f278472c73c1ccde1b954eb2cc2efa`.
Machine: the box. One attempt per check. Defaults D1-D16; seeds 20261113-20261117; N = 100,000 shots per read. Start 2026-11-14 22:30:03 EST, end 2026-11-14 22:30:35 EST, total wall 32.4 s.

## Resources (meter)

| Check | Ceiling s | Exit | Killed | Wall s | CPU s | Peak tree RSS MiB (sampled) | ru_maxrss MiB |
|---|---|---|---|---|---|---|---|
| S0 | 600 | 0 | no | 4.31 | 4.21 | 82.6 | 85.0 |
| C4 | 600 | 0 | no | 0.62 | 0.43 | 61.9 | 65.0 |
| C5 | 900 | 0 | no | 27.41 | 27.18 | 145.4 | 145.2 |

Run-folder size after last check: 4503716 bytes (cap 64 MiB). RSS cap 512 MiB, 1 thread, CUDA_VISIBLE_DEVICES empty.

## Gate labels

- **S0**: PASS (P0 MET, P1 MET, P2 MET, P3 MET, P4 MET). `out/S0.json` `84f9eb1033b58192d92a8dff2505d5c847a4d9d4ab5d17a090522ebc925002b9`
- **C4**: FAIL. `out/C4.json` `c9b3f6fc7cd67c7c613f298df00d7441b5abe21a3ff1ac61e9859b0abe3324eb`
  - Q-share cells outside 3 sigma: ['quadrants 20261114'] (z_A 0.76, z_D 3.05, z_BC 1.09); the other 14 (partition, seed) cells within 3 sigma. Shot draws now differ per partition (seed 20261114 unmerged counts: quadrants [40168, 29809, 20189, 9834], slabs_x [39941, 29993, 20143, 9923], chequer [40161, 29919, 19937, 9983]).
  - Control shift > 5 sigma found: p1 False, p4 False (largest control z on any cell 2.74). Controls use w_k proportional to sum_{i in k}|a_i|^p as written in design section 2 (unchanged).
  - UNINFORMATIVE cells: none.
- **C5(a)**: does not pass (read-only audit `L2_0_C5A_AUDIT.md` `423920fe845e26df1871e0e2a5ebc044c780735919c1df1af3c47ecabf683090`, not rerun).
- **C5(b)**: FAIL. `out/C5.json` `25488b6079d41468019b8c76791c2fea292e1e9a124265a177451ea81009c1b9`
  - 2,500 official cells, 2,500 scored, 0 UNINFORMATIVE; 160 official cells scored after the design's L = 64, d = 16 retry (all S5).
  - Beyond 3 sigma: 7 of 2,500; max z 4.208. S1 dir 19 sigma seed 20261114 z 4.208; S2 dir 32 sigma seed 20261115 z 3.260; S2 dir 36 tau seed 20261116 z 3.027; S3 dir 2 tau seed 20261117 z 3.586; S4 dir 40 tau seed 20261117 z 3.150; S5 dir 6 sigma seed 20261113 z 3.093; S5 dir 34 tau seed 20261113 z 3.010.
  - Axis directions (reporting only): 300 scored, 1 beyond 3 sigma.
- **C5(c)**: FAIL. 1,800 cells, 1,800 scored, 0 UNINFORMATIVE; beyond 3 sigma 3 of 1,800, max z 3.555: S2 dir 32 tau FG2_quadrants seed 20261113 z 3.028; S3 dir 4 tau FG2_quadrants seed 20261114 z 3.555; S5 dir 38 sigma FG1_halves seed 20261114 z 3.019.
- **C5(d)**: PASS. 3,600 cells. g3 rejected (117 of 480 tests beyond 5 sigma on all five seeds); g1 rejected (114 of 480); g4 rejected (116 of 480).
- **C5 overall**: not passed (D10).

## Not rerun

C1 (UNINFORMATIVE), C2 (FAIL) and C3 (PASS) stand from the first run's READOUT.md `e02398f9146b18a114212b4ab14b302d25f278472c73c1ccde1b954eb2cc2efa`.
