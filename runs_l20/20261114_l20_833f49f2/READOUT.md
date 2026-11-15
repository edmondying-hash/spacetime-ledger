# L2.0 scored run read-out

Design `L2_0_RUN_DESIGN.md` sha256 `833f49f26418b2267cc0a9b389a46220078b453eebe92cf149145af330077ed9`; design folder SHA256SUMS `ae005712b98eb2263e702cdc5701abfd1fb0e9e0bef102367c40d28dab858edc`; `l20_measure.py` `08e98af5d2936474260f233f85c4b1ef06b4564d6533409f36c34a7bfa5dd516`; `frozen/dirac4.py` `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff`.
Harness: `harness/l20_score.py` `e6dbb36eb0e59562c3366a9780a364e03848f8dd511edb755e1e992fb14b492f`; `harness/run_all.py` `91287a1b9c8eb6842c5a869cdc453c52865474fbe9cf66b9a4ffb52718452edf`; `harness/meter.py` `29b968b434ed45b141824d80be96684ebc413bde77e3aa6dd55a2f099552eff1`; `harness/IMPLEMENTATION_NOTES.md` `b494b2249937c98056699e0558bd60b5180756b25e24d0751b5fed449a6ee8bf`; `harness/PRE_RUN_SHA256SUMS` `ab7ebcbac9d82afe9b9f3824fc7e7b08a17568d90ea0e460e83f6aa232ebbee8`.
Machine: the box. One attempt per check. Defaults D1-D16. Start 2026-11-14 22:09:01 EST, end 2026-11-14 22:11:56 EST, total wall 174.5 s.

## Resources (meter)

| Check | Ceiling s | Exit | Killed | Wall s | CPU s | Peak tree RSS MiB |
|---|---|---|---|---|---|---|
| S0 | 600 | 0 | no | 4.53 | 4.40 | 81.5 |
| C1 | 600 | 0 | no | 112.04 | 111.84 | 124.7 |
| C2 | 600 | 0 | no | 2.68 | 2.54 | 68.4 |
| C3 | 600 | 0 | no | 51.76 | 51.67 | 69.4 |
| C4 | 600 | 0 | no | 0.41 | 0.39 | 58.1 |
| C5 | 900 | -9 | rss_cap | 2.88 | 2.69 | 532.8 |

Run-folder size after last check: 2183875 bytes (cap 64 MiB).

## Gate labels

- **S0**: PASS (P0 MET, P1 MET, P2 MET, P3 MET, P4 MET). `out/S0.json` `25b9111e1d075db411f9d3c9e069ba255ac0cce350f5d55c6009800ea8d5db69`
- **C1**: UNINFORMATIVE. `out/C1.json` `761b8b859aa28cfa3e3952f5c63a1f9db94b76bca5c4192bddcc4bccada55a64`; `out/C1_series.npz` `262bb6452afa6f305a1da3673c7befbe65883f15c8cbb425dc2a2eb9a3e1fa41`
  - 5.1 p-norm drift: PASS. Failures: none. S3 quiet-p reported: none.
  - 5.1 L = 32 reruns (edge > 1e-6 at L = 16): 20261113 S1 UNINFORMATIVE; 20261113 S3 UNINFORMATIVE; 20261114 S1 UNINFORMATIVE; 20261114 S3 UNINFORMATIVE; 20261115 S1 UNINFORMATIVE; 20261115 S3 UNINFORMATIVE; 20261116 S1 UNINFORMATIVE; 20261116 S3 UNINFORMATIVE; 20261117 S1 UNINFORMATIVE; 20261117 S3 UNINFORMATIVE
  - 5.2 search: UNINFORMATIVE (control (3): 6^3/8^3 clear nullspace dimension differs from 12^3). n_clear 36, n_grey 0, s_min 1.450e-14, s_max 9.501e+01; on-site n_clear 1, n_grey 0.
  - Controls: (1) MET (identity residual 7.22e-16, projection residual 1.58e-15); (2) MET (sigma_z residual 0.9890); (3) NOT MET (6^3 n_clear 78 n_grey 0; 8^3 n_clear 36 n_grey 0).
  - Positivity (m(k) >= 0 fallback, no SDP solver): positive complement rays none; on-site none.
- **C2**: FAIL. `out/C2.json` `2c2efedeab50b6ba81bffeffa118097894404e85f043f240e0ec4cc17cef7eaa`
  - Q-share cells beyond 3 sigma: ['20261113 P2 t=10 Qshare z=3.1447648211732675'] (1 of 270 channel tests; max z 3.145).
  - Control (p = 1, p = 4) cells without a > 5 sigma channel at t = 0: ['20261113 RANDQ p1 max z=4.826620284604474', '20261114 RANDQ p1 max z=4.416943762508264', '20261117 RANDQ p1 max z=2.6353544909445077'].
- **C3**: PASS. Repeat disagreements 0, second-client disagreements 0, server byte differences 0. `out/C3.json` `f95681358047c384944c1ec249b86e3dc800129629d8996ba4ce8bba5da031f1`
- **C4**: FAIL. Q-share cells outside 3 sigma: ['quadrants 20261114', 'slabs_x 20261114', 'chequer 20261114']. Control shift > 5 sigma found: p1 False, p4 False. `out/C4.json` `76c56c10ea1f6edbbb0a7b2056fc079838b1827da84b2d1172d1d25f1edc8484`
- **C5(a)**: does not pass (read-only audit `L2_0_C5A_AUDIT.md` `423920fe845e26df1871e0e2a5ebc044c780735919c1df1af3c47ecabf683090`, already performed, not rerun).
- **C5(b)**: UNINFORMATIVE. **C5(c)**: UNINFORMATIVE. **C5(d)**: UNINFORMATIVE. Cap trip: meter killed C5 (`rss_cap`, exit -9) at 2.88 s wall, sampled tree RSS 532.8 MiB > 512 MiB; no `out/C5.json` was written. Log `logs/C5.log` `750495df85d6c4091dc1e22d560afe9cdda57e80e6c73699fd486824ff2a3061`; meter `logs/C5_meter.json` `5fb5765a1c2abd052e6e5ab961056f9f4bd6533aac7738641512bc07f5e5c76f`.
- **C5 overall**: not passed (D10).

## Diagnostics (not gated)

- m = 0.3, seed 20261113, S1, L = 16: drift {'0.5': 2.82, '1.0': 2.48, '1.5': 1.05, '2.0': 6.86e-14, '2.5': 0.56, '3.0': 0.818, '4.0': 0.971}; stepper fault at cycle 1: False.
- Uniform load ON, rule B, s = 0.81, phi = 1.4, m = 0, seed 20261113, S1, L = 16: p = 2 drift at cycle 1 4.772e-10 (> 1e-12, series stopped after cycle 1 by the C1 stepper-fault rule); drift over recorded cycles {'0.5': 1.39, '1.0': 1.11, '1.5': 0.51, '2.0': 4.77e-10, '2.5': 0.363, '3.0': 0.602, '4.0': 0.848}; max |factor eigenphase| 3.141592653589793; max unitarity deviation 6.33e-15.

## UNINFORMATIVE cells

- C1 5.1: L = 32 reruns of S1 and S3, all five seeds (edge fraction > 1e-6 at L = 32).
- C1 5.2: the search (control 3).
- C2, C3, C4: none.
- C5(b), C5(c), C5(d): all cells (cap trip).
