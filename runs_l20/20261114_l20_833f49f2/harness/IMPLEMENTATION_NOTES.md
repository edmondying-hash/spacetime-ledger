# L2.0 scored run: implementation choices (written before the run, 14 Nov 2026 America/New_York)

Design: L2_0_RUN_DESIGN.md sha256 833f49f26418b2267cc0a9b389a46220078b453eebe92cf149145af330077ed9, all D1-D16 defaults.
Design folder /workspace/L2_0_design_spacetime_20261113/ is imported read-only and never written (bytecode writing disabled).

## Code
- l20_measure.py's `--check` entry points are stubs (they return 2 without scoring). The scored procedures of §§4-9 are
  implemented in harness/l20_score.py, which imports l20_measure.py (and frozen/dirac4.py through it) unchanged and uses
  its primitives: U_cycle, precompute_U, fft_cycle, orbit_mask, random_orbit_state, localized_packet, half_displacements,
  n_params, constraint_matrix_fast, identity_params, apply_params_to_symbol, charges, charges_power, lock_to_channel,
  projector_sigma/tau, factor_expect, spin_dependent_shift. l20_measure.nullspace_svd is NOT used for the official search
  (full_matrices=True on a 27,760 x 560 matrix would need ~6 GB); see C1.
- harness/meter.py is byte-identical to the L1.5 meter (sha256 29b968b434ed45b141824d80be96684ebc413bde77e3aa6dd55a2f099552eff1):
  wall, CPU (user+sys of child), sampled tree RSS every 0.2 s, kill on wall ceiling or RSS > cap, threads pinned to 1.
- harness/run_all.py runs each check once under the meter; ceiling = min(per-check cap, remaining of 2,400 s); RSS cap
  512 MiB; output size checked after each check (64 MiB); S0 failure stops the run. No retries.
- RNG: one numpy Generator default_rng(seed) per (check, seed), used in a fixed order inside each check. C5 uses one
  Generator per seed for the whole check (S4 spinor drawn first, then all shots). S0 uses default_rng(20261113).
- Shots: rng.choice over channels with the rule's normalised weights, N = 100,000 per read (the design's minimum).
  sigma is the exact binomial shot-noise sd from the sampling weight w: Q*sqrt(w(1-w)/N); for differences of two
  independent reads the variances add. A comparison "within k sigma" is |diff| <= k*sigma + 1e-12 (floating floor, only
  matters when w is 0 or 1).
- Labels: PASS / FAIL / UNINFORMATIVE per check; sub-gates recorded separately.

## S0
- P0: sha256 of every file in the design SHA256SUMS, of SHA256SUMS itself (ae005712...), and of the imported modules.
- P1: 64 k-points = origin + six axis mid-points (+-pi/2 e_i) + 32 random + 25 further random (uniform in [-pi,pi)^3);
  max |entry| of U^dag U - I <= 1e-14.
- P2: at L = 16 and L = 32, six on-grid plane waves k = 2 pi n / L restricted to the orbit, random unit spinor,
  amplitude-1 per site; one FFT cycle vs U_cycle(k) chi; max |entry| difference <= 1e-12.
- P3: at L = 16 and 32, random orbit state, 10 cycles, max off-orbit |a| <= 1e-14.
- P4: thread env = 1, process has 1 OS thread, CUDA_VISIBLE_DEVICES empty, meter flag set. (threadpoolctl absent.)

## C1
- 5.1: Sigma|a|^p summed over orbit sites only (off-orbit amplitudes are exactly zero in exact arithmetic).
  S1: width-2 packet at (L/2)^3, random spinor. S2: random_orbit_state. S3: two width-2 packets at (L/4,L/2,L/2) and
  (3L/4,L/2,L/2), the same random spinor, equal charge, second packet times e^{0.7i}, renormalised.
  "Within two hops of the periodic edge" = any coordinate in {0,1,L-2,L-1}. Edge fraction checked at every recorded cycle;
  if > 1e-6 for S1 or S3, that state (same spinor) is rerun once at L = 32 (S3 separation L/2 = 16); if it still exceeds
  1e-6 it is labelled UNINFORMATIVE; the L = 16 S1/S2 cells gate. The S3 p = 2 bound is part of PASS.
- Diagnostics (not gated), seed 20261113, S1, L = 16, 1,000 cycles: m = 0.3; uniform load ON with rule B
  (each of S+, V+, S-, V- to the principal 0.81 power via complex Schur, as in the L1.5 harness), phi = 1.4, m = 0.
- 5.2: official k-set = 12^3 grid (k_i = -pi + 2 pi n/12) + origin + six axis mid-points (+-pi/2 e_i), 1,735 points.
  Constraint matrix from l20_measure.constraint_matrix_fast, built in chunks of 128 k and reduced by block Householder QR
  (numpy qr mode='r'); singular values and right singular vectors are those of R (equal to those of A in exact
  arithmetic). Nullspace: s < 1e-8; grey: 1e-8 <= s < 1e-4. On-site nested search: QR of the first 16 columns.
- Positivity: the nullspace is split into the identity ray and an orthonormal basis of its complement (nullspace vectors
  orthogonal, in parameter space, to the identity vector). Each complement basis vector is tested: positive if min
  eigenvalue of m(k) >= -1e-10 for +v or -v on the official grid and on the 16^3 diagnostic grid. Note recorded before
  the run: the complement is orthogonal to I, i.e. its BZ-averaged trace is zero, so a complement vector can only be PSD
  if it is zero; and I + eps*J is positive for small eps whenever the nullspace has dimension > 1. The design's basis-ray
  test is implemented as written on this basis; the nullspace dimension and basis are recorded in full.
- SDP realisation: no SDP solver on the box (cvxpy absent; not installed). Fallback m(k) >= 0 test used, labelled.
  (A vector with a negative m(k) eigenvalue cannot be realised by any K >= 0.)
- Controls: (1) unit identity vector residual max|A v| <= 1e-10 and projection residual onto the nullspace <= 1e-10;
  (2) sigma_z on the spin factor (on-site diag (1,-1,1,-1)), max|A v| >= 1e-3; (3) 6^3 and 8^3 grids (+ origin + axis
  mid-points) must give n_grey = 0 and the same n_clear as 12^3.
- C1 overall: FAIL if either sub-gate FAILs; PASS if both PASS; otherwise UNINFORMATIVE.

## C2 / C3 (L = 16)
- Five states per seed, built in this order: P1 width-2 packet at centre, spinor (1,0,0,0); P2 the same with a seeded
  random spinor; SPLIT random orbit state rescaled to charges 2/3 (x < 8) and 1/3 (x >= 8), channels the two x-halves;
  EQ4 random orbit state rescaled to 1/4 per (x,y) quadrant; RANDQ random orbit state. Channels for P1, P2, EQ4, RANDQ:
  the four (x,y) quadrants split at 8. Detector unitary = identity.
- C2: the server is evolved 0, 10, 100 cycles; each read is on a client copy; E[Q_j after] estimated from shot counts
  times the locked copy's channel charges (lock verified). Control requirement applied to every (seed, state) at t = 0
  whose kept Q_k differ by more than 1e-12 (P1, P2, SPLIT, RANDQ as built).
- C3: time 0, Q-share. The client read is deterministic given the outcome, so the locked copy and its weights are
  computed once per outcome channel with the real lock/read functions, and the second read and second-client read are
  sampled per shot from those weights. Server bytes compared with the snapshot (numpy.array_equal) after every shot,
  plus sha256 before/after; the server array is also flagged read-only.

## C4 (L = 16)
- Partitions: (x,y) quadrants; four x-slabs of width 4; 2x2 chequer of period L/2 (blocks of 4 in x and y).
  A,B,C,D as listed; merge B and C.
- States: seeds 1-4 random orbit state rescaled to 0.4/0.3/0.2/0.1 on A/B/C/D; seed 5 a width-2 packet at centre with
  a seeded random spinor (the "residual packet state").
- Unmerged and merged reads are independent shot sets. Controls use w_k proportional to sum_{i in k}|a_i|^p as written
  in design §2. Control counted as shifting if, on any official partition/seed cell, A or D moves by > 5 sigma.

## C5 (b)-(d)
- No dirac4 cycle in C5: the read is the discrete Stern-Gerlach embedding (l20_measure.spin_dependent_shift) then
  channels. L = 32, d = 8; packet width 1.5 at (L/2)^3; S5 second centre +16 along y.
- Channels: Voronoi cells (minimum image) of the plus images and minus images of every packet centre; a site is in the
  mid-band if its distance to the bisector of its nearest plus and nearest minus image is <= 1 (this covers both periodic
  bisectors). Mid-band fraction > 1e-6 (or coincident images) -> retry once at L = 64, d = 16 (S5 separation stays 16);
  still > 1e-6 -> UNINFORMATIVE.
- C5(b): 50 Fibonacci directions official, 6 axis directions reporting only; sigma and tau factors; 5 seeds (S4 spinor
  seeded per seed; other states identical across seeds, shots differ).
- C5(c): S2, S3, S5; directions with even index 0..38 (20); both factors; fine-grainings FG1 = halves perpendicular to the
  axis after the shift axis (a+1 mod 3) split at L/2; FG2 = quadrants in the two axes perpendicular to the shift axis;
  FG3 = unread factor split by components (tau_z: comps {0,1}/{2,3} for a sigma read; sigma_z: {0,2}/{1,3} for a tau read).
  Coarse and fine reads are independent shot sets.
- C5(d): S2, S3; same 20 directions, both factors, three fine-grainings. g3: w+ = [1 + x^3]/2 with x = n.r =
  (Q+ - Q-)/Q per pair; g_p: w+ = Q+^{p/2} / (Q+^{p/2} + Q-^{p/2}) per pair (D2_NOTE definition), fine weights
  q_j/Q times the pair rule. Tests: the embedding identity (coarse vs summed fine) and the C2 per-channel drift on the
  coarse read. A control counts as rejected if some (state, direction, factor, test) is beyond 5 sigma on all five seeds.
- C5 overall per D10: C5(a) stands as already done (does not pass); C5 is not treated as passed.
