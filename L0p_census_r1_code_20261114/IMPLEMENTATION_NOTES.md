# L0' census r1 implementation notes

Written against L0P_CENSUS_DESIGN_r1.md, sha256 c2673a6426ca5728738c7e7e63871bd26577e8475e9b2819d9980aeccb642fd1. Every entry point (census.py, census_steps.py) checks that sha256 before doing anything.

## Files
- census.py: the driver. It runs one attempt: S0, S1, S2, S4, S3, S5a, S5b, S6, S7, then the repair round (S0, S1, S2b, S4, S3, S5a, S6, S7 for R-C3) only if the census S7 records C3's F1 cell as NOT MET. Each step is a separate process with RLIMIT_CPU = the step's CPU cap and RLIMIT_FSIZE = the step's output cap. The driver polls VmRSS, wall time and output bytes, and kills the step's process group on any overrun. Each step's CPU, wall and peak RSS come from wait4 rusage, recorded in steps/<round>_<step>.json. The run folder is created with an exclusive mkdir, so a second attempt refuses to start. At the end the driver writes DONE or STOPPED with the reason, then SHA256SUMS over the run folder.
- census_steps.py: the step implementations. The run order is S4 before S3, because S3 needs c̄₀ from S4 (r1 S3 "Order").
- census_core.py: the layer lists, symbols and real-space engines. Each candidate is one list of layers, used for both the symbol and real-space evolution.
- dirac4_cycle_symbol.py: an unchanged copy of main's file (sha256 cc4bb988e81e5e93937184ce89cb14f7cbb847c058551fd0b5406b4ccd8f77d6), used by the S0 K-checks.
- watcher.sh: the memory-gated launcher. It checks MemAvailable immediately, then every 300 s, and launches once when MemAvailable ≥ 3,670,016 kB. A mkdir marker at /workspace/runs_l0p/.launched_c2673a64 ensures a single launch.

## Choices the design leaves to the implementation
1. Threads: BLAS/OMP are set to 1 thread (r1 allows at most 4). FFTs use scipy.fft with workers = 1.
2. Run folder: /workspace/runs_l0p/<YYYYMMDD>_l0p_census_r1_c2673a64/<candidate>/<step>/result.json, per the run instruction, instead of r1's `runs/<date>_L0p_census`. Lattice-level and rule-independent items (S0, S2a, the S3 control, the S4 control and thresholds, S5b, S7) are under `_global/`.
3. S4 bands: the bands with |ω(Γ)| ≤ 10⁻⁶, sorted at each κ. c₀(n̂,b) is taken as |a₁|, so that c̄₀ (the mean over D26 and bands) and |c₀/c̄₀ − 1| are defined for negative-ω bands. ξ₁ = a₂/a₁ and ξ₂ = a₃/a₁ keep their signs. The fit uses the scaled variable κ/0.2 with lstsq. If any ray has |ω| > 3.0, that knob value is UNINFORMATIVE (branch-wrap guard). If the S4 control is invalid, candidate fits still run to record c̄₀ for S3 and S5, and F4 is UNINFORMATIVE.
4. S3 refinement: at most 100 grid local minima per function (g₀, g_π) per knob value, lowest first, plus all high-symmetry points:
   - SC: the 8 points with k_i ∈ {0, π}.
   - C2: the 8 points with k_i ∈ {0, π/2}.
   - BCC: k_i ∈ {0, π}, the N points (±π/2, ±π/2, 0) and permutations, and the P points (±π/2)³.

   Minima beyond the 100 are listed. If any of them has a grid value below max(2·0.01·c̄₀, 10⁻⁶), the F1 conditions at that knob value that would otherwise be MET become UNINFORMATIVE. The NM result is replaced by the start point if the start point is lower. Plateaus are grouped by 26-connected labelling.
5. S3 conditions: NOT MET in any of conditions 1–3 gives NOT MET. Otherwise, any UNINFORMATIVE condition gives UNINFORMATIVE. Without c̄₀, conditions 2–3 are UNINFORMATIVE, except that a π-touching gives condition 3 NOT MET. Line test: the zero set counts as not isolated if count₁₂₉ > 2·count₆₅, or if count₆₅ = 0 and count₁₂₉ > 2.
6. S3 taste table: the "velocity tensor" entry records, per axis, ω/h at k₀ ± h·e_a for the degenerate bands (h = 10⁻⁵), plus the tilt. Chirality is "not computed".
7. F5 slopes: least-squares log–log slope with |values| clamped below at 10⁻¹⁰.
8. S5a boxes are even and FFT-friendly: SC (and C2) 48, 90 and 180; B0 80, 160 and 320 (a/2 units). Q₂ uses the second-moment tensor Σ_W ρ x_a x_b. The wrap region is sites with max_i |x_i| > N/2 − 2σ (in ℓ). C2 is evolved through the 2×2×2-cell FFT with the operator D M(q/2) D†, D = diag(e^{ik·s}).
9. S6: δE = |E(t) − E(0)| / E_abs(0), δn = max over k and bands of |n(t) − n(0)| / Q(0), with the Schur basis taken at t = 0. B0's k-space uses the a/2 grid with the orbit embedded in ℤ³. The Gaussian state is σ = 2ℓ (B0: 2√3 grid units).
10. S1: C2's light cone starts from each of the 8 sites of cell 0 (Manhattan distance from that site). C2's time-reversal record uses M = diag((−1)^{a·s}), a ∈ {0,1}³.
11. S2(a) leapfrog:
    - The field is a complex planar packet, so the |u|² centroid is smooth.
    - The box is 4096 × 4 × 4 with sheared identifications (x, y+4, z) ≡ (x+4, y, z) when n_y ≠ 0, and the same for z.
    - The previous time level comes from the exact discrete dispersion.
    - The centroid is measured on the line y = z = 0, and speed/c = Δp / (Δt·√m·λ).

    The B0 record uses the BCC 8-corner scalar rule with k per a/2: ω = k(1 − k²[Σn⁴/24 + Σ_{i<j} n_i²n_j²/4] + …).
12. S7:
    - V1 is the S1 label. V2 combines S2(a) and S2(b). V3 is MET iff the S3 scan completed at every K7 value and the S3 control is valid. V4 is the S6 label (UNINFORMATIVE if the cross-check fails).
    - Knob rule:
      - NOT MET if any per-knob label is NOT MET or the zero-class count changes across K7.
      - MET if all per-knob labels are MET.
      - Otherwise UNINFORMATIVE.
      - For C4 it is "not applicable (no knob)" and does not block.
    - F2 follows r1 S7.
13. S0 K5: the C3 p-odd value is the max-abs entry of U − 1 and must reproduce 0.631 to within 5×10⁻⁴. All other K and implementation checks must be ≤ 10⁻¹². S0 also checks layer counts against the r1 table and recomputes every code hash against SHA256SUMS.
14. Peak RSS: each step records wait4 maxrss. Per-candidate records add VmHWM after a clear_refs reset.
15. Smoke tests use `--mode smoke` (tiny sizes, outputs marked NOT CENSUS, memory value recorded but not enforced). They refuse to write under /workspace/runs_l0p.
