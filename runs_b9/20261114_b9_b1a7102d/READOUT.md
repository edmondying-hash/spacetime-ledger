# B9 clock-factor check — run read-out

Run folder: `/workspace/runs_b9/20261114_b9_b1a7102d/`. Machine: the box (Linux, CPU only, affinity CPU 0, thread env vars = 1, CUDA_VISIBLE_DEVICES empty). Not bigbang, not a user machine. Run 14 Nov 2026, 9:20–9:21 PM EST.

Design `B9_CLOCK_DESIGN.md` sha256 `b1a7102db33df9769a97c0495c710a9bf494fd26d7c4d498d0e5e648c34af728` (folder `/workspace/B9_clock_design_spacetime_20261113/`). Sidecar `B9_OPEN_DECISIONS.md` sha256 `f5ce6f447a9e19d89be2a379a11a72fc7738a0724d57169a505167ade55f607e`. PDF sha256 `630cfa93e497b4ebd5563a11c9d9fce13d539511aef5b4de49cb4bb620071756`. Approval: Edmond Ying, 9:18 PM EST 14 Nov 2026, "let's run hash b1a7102db33df9769a97c0495c710a9bf494fd26d7c4d498d0e5e648c34af728 , no change". K1–K11 at design defaults: I3, I4, I5 computed, none adopted; I2 a control, I6 not scored (no `--include-I6`); C1, C2 and the analytic table run; targets K4–K6 defaults; box; caps as K8; no paper/plan/repo/Sheets edit; `field.py` not rerun.

One attempt per step. No retry, no re-score, no parameter change.

## Pre-flight hashes

- Design folder `SHA256SUMS`: all four files OK (`logs/design_hashcheck.txt`).
- Harness `harness/b9_measure.py` sha256 `651ec6bcbe68f9f9934eed112a763be94dc0d0824de5224eb25a6094f8eee940` (same bytes as design folder).
- Paper `space-ledger-v2.md` via `git show fdf3e72a958bdc0e3ed95f06530b0a96d0a45d61:space-ledger-v2.md` (read-only, local clone `/workspace/spacetime-ledger`): sha256 `ce22701ca6e5e2dfa143ab43a6062e80025c1afeba5137f7e271c239bc75555c`, equal to the design's. Commit `5a00f03e6dd0849a77f189ff3f4836d3dd216e16` is an ancestor. Recorded: remote `main` is now `8a6a0b1ec46e5f3f6737b26c970018273f97721c`; the design pins `fdf3e72a…`, which was used.
- `/workspace/mercury/` RESULTS.md, field.py, orbit.py, orbit.json, beta.json, results.json, run.log: all seven sha256 equal to §1 (`out/sources.json`).

## Resources (external meter `harness/run_meter.py`; caps 512 MiB RSS, 120 s per step, 600 s total)

| Process | Wall s | CPU s | Peak RSS MiB (polled / ru_maxrss) | Exit | Cap kill |
|---|---|---|---|---|---|
| P0 source hashes | 0.061 | 0.055 | 16.2 / 16.9 | 0 | none |
| b9_measure.py `--step all` (S0–S5) | 23.689 | 23.296 | 88.6 / 88.5 | 0 | none |
| Supplement §7 gates | 2.690 | 2.689 | 84.0 / 86.8 | 0 | none |
| Total | 26.44 | 26.04 | 88.6 max | | |

Per step, from the harness's internal meter (peak RSS is process-wide maximum so far, cumulative):

| Step | Wall s | CPU s | Peak RSS MiB | Harness status |
|---|---|---|---|---|
| S0 | 0.931 | 0.607 | 76.3 | PASS |
| S1 | 5.994 | 5.969 | 87.0 | PASS |
| S2 | 5.448 | 5.431 | 88.3 | PASS |
| S3 | 0.000035 | 0.000035 | 88.3 | PASS |
| S4 | 11.145 | 11.143 | 88.5 | PASS |
| S5 | 0.000005 | 0.000004 | 88.5 | RECORDED |

Output folder size before this file: 55,646 bytes (cap 32 MiB).

## S0

Imports: NumPy 2.5.4, SciPy 1.18.1, `solve_ivp` DOP853 present; Python 3.13.5. Formula recomputation: I1 42.98069352502894, I2 46.333187619981196, I3 14.326897841676312, relative difference 0.0 for each (tolerance 1e-9). 5-year GR cost probe: 0.208 s wall, value 44.1617892068795 ″/cy (not a result).

## Controls (§7)

| Gate | Value | Reference | Diff | Tolerance | Outcome |
|---|---|---|---|---|---|
| C1 formula | 42.98069352502894 | 42.98069352502894 | 0.0 rel | 1e-9 rel | PASS |
| C1 100-yr endpoint | 42.91229380880339 | 42.91229380880339 | 0.0 | 0.02″ | PASS |
| C1 200-orbit linear fit | 42.98224462225191 | 42.982 | 0.000245 | 0.02″ | MET |
| C2 formula | 46.333187619981196 | 46.333187619981196 | 0.0 rel | 1e-9 rel | PASS |
| C2 100-yr endpoint | 46.27759181715892 | 46.27759181715892 | 0.0 | 0.02″ | PASS |
| C2 200-orbit linear fit (recorded) | 46.33448338169987 | — | — | — | — |
| Newtonian energy drift per century, S1 / S2 / S4-I3 / S4-I5 | 3.040e-11 / 3.035e-11 / 3.034e-11 / 3.040e-11 | — | — | 1e-6 | MET (each) |
| Newtonian-only 100-yr endpoint | 0.0001485360210586517 ″/cy | 0 | 0.000149 | 0.01″ | MET |

No UNINFORMATIVE condition of §7 was triggered for the controls; B_m identifications were scored.

## S3 analytic table (default targets: perihelion [42.94, 43.02] ″/cy on the formula value; GP-A |α| ≤ 1.4e-4; Cassini γ−1 ∈ [−2e-6, 4.4e-5])

| ID | β | γ | (2+2γ−β)/3 | Perihelion formula ″/cy | Residual vs 42.98 | α | z/z_GR | Limb deflection ″ | Shapiro / GR | Perihelion | Redshift | γ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| I1 (control) | 1.0 | 1.0 | 1.0 | 42.98069352502894 | +0.000694 | 0.0 | 1.0 | 1.7512433 | 1.0 | MEETS | MEETS | MEETS |
| I2 (control) | 0.766 | 1.0 | 1.078 | 46.333187619981196 | +3.353188 | 0.0 | 1.0 | 1.7512433 | 1.0 | MISSES | MEETS | MEETS |
| I3 | 1.0 | 0.0 | 0.33333 | 14.326897841676312 | −28.653102 | 0.0 | 1.0 | 0.87562165 | 0.5 | MISSES | MEETS | MISSES (γ−1 = −1.0) |
| I4 (diagnostic) | — | — | — | — | — | 1.0 | 2.0 | — | — | UNINFORMATIVE | MISSES | UNINFORMATIVE |
| I5 | 1.0 | 1.0 | 1.0 | 42.98069352502894 | +0.000694 | 0.0 | 1.0 | 1.7512433 | 1.0 | MEETS | MEETS | MEETS |

I6: not scored (K2 default).

Recorded references, not gated (K4/K5): Clemence residual 42.56 ± 0.94 ″/cy (paper line 1002); Will 2014 |β−1| < 8e-5; Pound–Rebka / Pound–Snider; GPS ≈ 38 µs/day (paper line 898). I4's Kepler diagnostic per design §5 (linear g00 ≈ −(1−4U)) is design text; the harness records only α = 1.0 for I4.

## S4 numeric orbits (cross-check of (2+2γ−β)/3)

| ID | Formula ″/cy | 100-yr endpoint ″/cy | 200-orbit linear fit ″/cy |
|---|---|---|---|
| I3 (β,γ)=(1,0) | 14.326897841676312 | 14.278142317383175 | 14.328050101925422 |
| I5 (β,γ)=(1,1) | 42.98069352502894 | 42.91229380880339 (= I1 archived) | 42.98224462225191 |
| I4 | UNINFORMATIVE (no_consistent_1PN_orbit_until_G_retuned); α = 1.0 | | |

## Implementation choices (disclosed)

1. The harness was run once as `--step all` in one process so its own step order and S0-stop / controls-before-S4 logic apply; per-step 120 s caps were enforced externally by watching the appearance of `out/S*.json`.
2. `harness/b9_supplement.py` (sha256 `79a72dec90e7865972b8d8ca98658987c58b81dc178a65a4f5336a7c16affad1`) implements §7 items absent from the harness: the C1 linear-fit gate; the Newtonian-energy drift gate (two-point start/end relative change over the 200-orbit run, 48.169 yr, scaled to 100 yr, since only those values are recorded); the Newtonian-only check. Archived `orbit.py` records `prec(0,0)*0`, which is identically zero, and `prec(0,0)` itself keeps the 2(1+γ)(r·v)v/c² term (factor 2/3, not Newtonian); the check was therefore implemented as the archived 100-yr DOP853 endpoint (rtol 1e-13, atol 1e-3, LRL read-out) with the 1PN term removed. It also performs the source-hash pre-flight.
3. `harness/run_meter.py` (sha256 `626ceb30aa5f920447e3af42892894693693a6c6ba7ac5d733038e7971583551`): fork/exec meter, CPU-0 affinity, 20 ms VmRSS polling, kill on caps.
4. Harness hashes recorded before running in `harness/SHA256SUMS_prerun`; `harness/` made read-only before any run.
5. The harness scores the perihelion target on the formula value; orbit values are reported as cross-checks only.

Nothing was written to the repo, paper, plan, Sheets, L1.5 folders or `/workspace/mercury/`. PID 1735586 was not touched.
