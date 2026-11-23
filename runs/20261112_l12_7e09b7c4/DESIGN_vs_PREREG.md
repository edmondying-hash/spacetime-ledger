# DESIGN_vs_PREREG — L1.2 run 20261112_l12_7e09b7c4

Written 2026-11-12, about 6:50 PM America/New_York, before any L1.2 computation.

Documents compared:
- Design `L1_2_RUN_DESIGN.md`, sha256 `7e09b7c42bf0b0b44db0057bc7a23c25add9503c441c163f47defabbe93f679b` (copied unchanged to `design/`).
- Decisions record `L1_2_DECISIONS.txt`, sha256 `c3225f353a1ad68956e2d39443814586b8c6e62ce862dced70e9c1f5aa17cf4e` (D1 load-free; D2 as revised in its section 3; D3 accepted; D4 yes).
- Pre-registration `PREREGISTRATION.md`, sha256 `733752444dfdbaab68654e583b15fdc97619883224fc30357f8ecba998747239`.
- Paper `space-ledger-v2.md` at main `cc2cc5c8c9b572c68bd1a1f074fdfacbfac4fe32`, sha256 `8cbb94ec481b3332f074ea028505478dd2d576a8b5d60915f072b653ab6aad70`.

Rule applied (D4): where the two conflict, `PREREGISTRATION.md` governs. Where the pre-registration is silent, the design applies. Where the design adds a measurement the pre-registration does not have, it is run and reported under the design's own rule, and it never loosens a pre-registration gate.

## Edmond's ruling on location and caps

The pre-registration names the box (one thread, 1 GiB, 300 CPU s, 360 s wall, 16 MiB). Edmond approved design `7e09b7c4` at 4:56 PM ET ("Approve 7e09b7c4") with the design §6 caps, and gave the go in this chat at 6:41 PM ET ("yes, start") for S0–S5 on **bigbang** (`/home/eying/spacetime_files/runs/20261112_l12_7e09b7c4/`). This is recorded as **Edmond's ruling at 6:41 PM ET**: location bigbang, caps = design §6 soft ceilings (96 GiB, 20 threads, 8 h total, 2 h/step, 1 GiB output). The pre-registration's box caps do not apply. BLAS/OpenMP threads are pinned to 1 in every process (standing rule); where a step uses parallel worker processes, there are at most 20, each single-threaded.

## Path redirect (pre-registered deviation, pre-reg decision 3)

The frozen generators `exec(open('/workspace/qca/….py'))` and `open('sym.py')`. On bigbang the harness replaces `builtins.open` for reads of `/workspace/qca/<name>` and of the bare name `sym.py` with `frozen/qca/<name>` in this folder. No frozen byte is edited. Frozen hashes are checked at the start (S0) and at the end (after S5). The box copies under `/workspace/qca/` were hashed read-only before staging and matched every pin.

## Conflicts and how they are settled

| # | Item | Design | Pre-registration | Applied (D4) |
|---|---|---|---|---|
| C1 | `N_s=24` residual cell | floor test vs `f24` (m0=0), pass/fail | UNINFORMATIVE; report raw residual, log10, and `N_s=22` as floor diagnostic; does not block PASS; `r[:,1]>1e-15` cut not applied to the cell | Pre-reg. Design `f24` is computed and reported as a record only, not a verdict. |
| C2 | R4a / E2 seeding | `default_rng(20261112)`, per-task `+index` | exact `dw_gscan.py` protocol: fresh `default_rng(1)` per (b,N_s), 60 starts, NM `xatol=1e-7, fatol=1e-12, maxiter=1500`, `dist_gamma>0.3` | Pre-reg. The frozen `dw_gscan.py` is executed unchanged (via the redirect). |
| C3 | b ladder / N_s for the boundary | R5: b∈{0.10…0.40}, N_s∈{8,16,24,32,48}, D3 verdict rules | E1 b∈{0.10…0.35} at N_s∈{8,12,16,24}; E2 at N_s∈{8,16}; three-part pass (i)(ii)(iii) | Pre-reg three-part clause is THE boundary gate. E1 is evaluated on the union ladder b∈{0.10,…,0.40}, N_s∈{8,12,16,24,32,48}; clause (ii)/(iii) use only the pre-reg subset. Design R5 verdicts (allowed/excluded/unresolved) are computed with D3 thresholds and reported beside it. |
| C4 | Residual decay fits | fit over N_s=2…12 | as `dw_final.py` (N_s=2…24 even, with its `>1e-15` cut), reference only, not in 5% PASS | Pre-reg (run `dw_final.py` unchanged). The design's N_s=2…12 fit is also reported, with the design's dual 5% rule, as a record. |
| C5 | |γ5| / loc. length direction | 13 directions, gate on all | direction (1,2,3)/√14; cells from `walls[0]` (V5 D18) | Pre-reg for the gate. 13-direction spread reported as a record. |
| C6 | Speed estimator | group velocity, Richardson, `N_s=1` chain as physical reference | phase velocity |ω_min|/κ, 13 dirs of `dw_final.py`, κ∈{0.0125,0.025,0.05}; bulk = `periodS` (m=0, φ=1.4); speed_mean at κ=0.0125 | Pre-reg estimator governs. Note: `floq(k,N_s=1,φ,b,m0=0)` has `Wmat=I` and is algebraically `periodS(k,0,φ)`; the run verifies this numerically, so the pre-reg bulk control and the design's "same code path, N_s=1" are the same matrix. Design's group-velocity extrapolation reported as a record (method: central difference h=1e-5 along each direction at |k|=0.01…0.05, quadratic fit v(k)=v0+a k², v0 reported). |
| C7 | Speed gate | 1e-6 relative = species-independent; else recorded difference | measurement, not scored vs 0.9855 | D2 (revised, Edmond 4:51 PM) defines the R6 clause verdict: pass iff (a) both measured by the same code path over 13 directions, 6 s.f., difference + relative, and (b) end-mode speed within 5% of 0.9855. This is a separate clause; it is not added to the pre-reg Table-dw 5% PASS. |
| C8 | Pre-flight | P0–P4 | G0, G0b, G1 | Union. All must pass; any failure stops the run. |
| C9 | Caps / location | design §6 | box caps | Edmond's ruling 6:41 PM ET (above). |
| C10 | |γ5| and localisation definitions "from dw.py" | quote verbatim from `dw.py` | method is `dw_final.py` | `dw.py` contains neither definition; they are in `dw_final.py` (lines quoted verbatim into result.json). |

R6 vs D2-revised: no conflict found. Design R6 says a difference above 1e-6 "is recorded as a measured species-dependent difference" and that the run does not decide; D2-revised makes the clause pass when the difference is measured and recorded and 0.9855 is reproduced within 5%.

No conflict was found that D4 cannot settle.

## Choices declared before data (design left them open)

- **P4** ("L1.1 sum-form diagnostic at r=0, shift difference at the twelve edge labels ≤1e-13"): frozen `dirac4.py` (`f71c782e…`) `U_cycle(L, wilson_mass=0.0)` vs `U_cycle(0)` for the twelve labels L=(±π,±π,0) and permutations, max abs entry difference; also the chain `floq(L,4,1.4,0.2)` vs `floq(0,…)`. Both ≤1e-13.
- **G1**: chain at N_s=16, b=0.2, φ=1.4, m0=0, k=0; also reported at every N_s=2…24 (even).
- **R1 two-ways (§5)**: Dirac fit ω(k)² = ω0² + v²k² along (1,2,3)/√14 at k∈{0.002,0.004,0.006,0.008,0.01}, m0=0.05, N_s∈{2,4,8,12}; √ω0² reported beside the k=0 value.
- **|γ5| independent (§5)**: eigenvalues of Q†Γ5Q in the four-dimensional low subspace Q (Γ5 = diag(1,1,−1,−1) per copy), largest |eigenvalue| reported beside `walls[0]['gamma5']`.
- **Bulk gap 0.033**: generator of the paper line is `qca/RESULTS.md` line 175 "Bulk gap (ring, global search, b=0.2): 0.0331", produced by `dw_ring.py` (sha256 `8cbd5eb07af30663f48331bb96964c446ddf6876b3de8dd6f1a4d7c551b2b43b`, ring=True, N_s=8, 40 starts `default_rng(2)`). Executed unchanged via the redirect; 5% rule vs 0.033.
- **R4b**: 129³ boundary-inclusive grid `linspace(-π,π,129)`³ at N_s=16, m0=0, φ=1.4, b∈{0.10,0.15,0.20,0.25}; f = smallest |ω| (ω=arg λ/4). Grid local minimum = f ≤ all existing 26 neighbours in the array (no wrap). Minima with `dist_gamma>0.3` are refined by NM with the `dw_gscan.py` options; refined points with `dist_gamma≤0.3` are discarded. R4b value = min over refined points (and the grid minimum over non-excluded grid points is also recorded). Two-sided classification as design R4.
- **R5 "R4 gap for the same b"**: R4b for b≤0.25; E2 at N_s=16 for b=0.30, 0.35 (no R4b there). For b=0.40 neither design nor pre-reg defines an R4 gap; survival there is reported as "not evaluable" and the b=0.40 verdict is "unresolved (rule input missing)". Equivalence of the eight (±π/2)³ points: two points are equivalent iff their difference/π is an integer triple of even sum. Fit ln(gap) vs N_s over 24, 32, 48 by least squares. End-copy weight = Σ|v|² on copies s=1 and s=N_s of the eigenvector of the smallest |ω| (unit norm).
- **Speed (κ=0.0125)**: speed_mean end − speed_mean bulk, and relative to bulk, at 6 s.f.
- **X1**: `dw_real.py` (sha256 `276c5fdc225320ebddc8970602d03be73d56c16851cfcba04966b606e4e737f8`) executed unchanged; it writes `dw_real.json` into `out/S5/`.
- **X3** is not run (D1).
- Thread pinning: OMP/OPENBLAS/MKL/NUMEXPR/VECLIB/BLIS = 1 per process; S2, S3, S4 use up to 20 single-threaded worker processes.
