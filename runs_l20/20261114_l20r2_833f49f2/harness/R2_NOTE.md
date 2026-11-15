# L2.0 r2: code-only fixes to the run-folder glue code (14 Nov 2026, America/New_York)

Design: /workspace/L2_0_design_spacetime_20261113/L2_0_RUN_DESIGN.md, sha256
833f49f26418b2267cc0a9b389a46220078b453eebe92cf149145af330077ed9, all D1-D16 defaults. The design folder is not modified.
First run: /workspace/runs_l20/20261114_l20_833f49f2/ (SHA256SUMS sha256
355899be68345e063a9923280001325778fc1b7580dc35eeb9206c5245b850b2), not modified.
Request: Edmond Ying, 14 Nov 2026 10:27 PM ET, "ok, can you fix those and rerun?", replying to the offer to fix the C5
memory leak and the C4 seeding as code-only changes and rerun only C4 and C5.

## Files in this folder
- l20_score.py: the first run's harness/l20_score.py (sha256 e6dbb36eb0e59562c3366a9780a364e03848f8dd511edb755e1e992fb14b492f)
  with the two fixes below.
- run_all.py: the first run's harness/run_all.py (sha256 91287a1b9c8eb6842c5a869cdc453c52865474fbe9cf66b9a4ffb52718452edf)
  with the check list reduced to S0, C4, C5 (orchestration only; caps, meter, env and order unchanged).
- meter.py: byte-identical to the first run's meter (sha256 29b968b434ed45b141824d80be96684ebc413bde77e3aa6dd55a2f099552eff1).

## Fix 1: C5 memory
Cause (first run DISCLOSURES item 1): check_C5 kept every post-hop array `moved` (4 x 32^3 complex128, 2 MiB at L = 32)
in its geometry cache `geo` for all 1,008 (state, direction, factor[, S4 seed]) cells, about 2 GiB in total.
Change: right after prepare_cell builds a cell's geometry, the C5(c)/(d) fine-graining charges are computed for the
cells C5(c)/(d) use (S2, S3, S5; fib directions with even index 0..38; both factors) with the same masks and arithmetic as
the first run's inline code (moved into a helper `fine_charges`), stored as 3-element/4-element/2-element vectors, and
`moved`, `plus`, `minus` are dropped from the cache. C5(c)/(d) then read the stored charges instead of recomputing them
from `moved`. The FGS and cdirs definitions were moved earlier in check_C5 (same values) so the (b) loop can use them.
Unchanged: states, spinors, directions, factors, geometry (L = 32, d = 8, retry at L = 64, d = 16), Voronoi channels and
mid-band, fine-grainings, shots (N = 100,000), seeds, the per-seed Generators and the order in which they are drawn
(no draws happen in the moved code), sigma, gates and labels.

## Fix 2: C4 seeding
Cause (first run DISCLOSURES item 2): every (partition, seed) cell drew its shots from a fresh default_rng(seed); for
seeds 1-4 the channel weights are the same 0.4/0.3/0.2/0.1 on all three partitions, so the three partitions shared one
draw set.
Change: the state is still built from default_rng(seed) exactly as before (same random orbit states, same seed-5 packet
spinor); all shots of the cell (Q-share, p = 1, p = 4, unmerged and merged, in the same order) are drawn from a second
Generator default_rng([seed, partition_index]), partition_index 0 = quadrants, 1 = slabs_x, 2 = chequer. The cell record
also stores partition_index and the shot-RNG entropy [seed, partition_index].
Unchanged: partitions, states, rules, N, sigma, the 3-sigma and 5-sigma gates, and the control weights. The controls still
use w_k proportional to sum_{i in k}|a_i|^p as written in design section 2; first-run DISCLOSURES item 3 (that weight is
additive under merging) applies to this rerun unchanged.

## Rerun plan
One attempt of S0 (preflight), C4 and C5 under the first run's caps (D8: 1 thread, no GPU, 512 MiB sampled tree RSS,
600 s wall for S0 and C4, 900 s for C5, 2,400 s total, 64 MiB output), same seeds 20261113-20261117, same meter, in
/workspace/runs_l20/20261114_l20r2_833f49f2/. The design's larger-L geometry retry is part of the same attempt. C1, C2
and C3 are not rerun; their records stay those of the first run. A memory-only check of C5's geometry stage, with no
shots and no gate, is kept separately in /workspace/L2_0_r2_smoke_NOT_SCORED_20261114/.

## Unified diffs against the first run's harness files
```diff
--- first_run/harness/l20_score.py
+++ r2/l20_score.py
@@ -4,6 +4,8 @@
 Glue code written 14 Nov 2026 (America/New_York) in the run folder; it imports the design folder's
 l20_measure.py (and through it frozen/dirac4.py) unchanged and read-only. Implementation choices are
 listed in IMPLEMENTATION_NOTES.md beside this file.
+r2 code fix (14 Nov 2026, America/New_York; see R2_NOTE.md): (1) C5 no longer keeps post-hop arrays in its
+geometry cache; (2) C4 Q-share/control shots use an RNG derived from (seed, partition index). Nothing else changed.
 usage: l20_score.py S0|C1|C2|C3|C4|C5   (env L20_SCORE=1, L20_OUT=<out dir>)"""
 import sys
 sys.dont_write_bytecode = True
@@ -685,9 +687,10 @@
     L = 16
     parts = c4_partitions(L)
     cells = []
-    for pname, masks in parts.items():
+    for pidx, (pname, masks) in enumerate(parts.items()):
         for si, seed in enumerate(SEEDS):
-            rng = np.random.default_rng(seed)
+            rng = np.random.default_rng(seed)  # state construction: unchanged from the first run
+            rng_shot = np.random.default_rng([seed, pidx])  # r2 fix 2: shots independent per (seed, partition)
             if si < 4:
                 psi = rescale(H.random_orbit_state(L, rng), masks, [0.4, 0.3, 0.2, 0.1]); sname = "random_0.4/0.3/0.2/0.1"
             else:
@@ -695,13 +698,14 @@
             Qj = H.charges(psi, masks)
             merged = [masks[0], masks[1] | masks[2], masks[3]]
             QR = 1.0 - float(Qj.sum()) / norm2(psi)
-            cell = dict(partition=pname, seed=seed, state=sname, Q=Qj, merge_QR_over_Q=QR)
+            cell = dict(partition=pname, partition_index=pidx, shot_rng_entropy=[seed, pidx], seed=seed, state=sname,
+                        Q=Qj, merge_QR_over_Q=QR)
             if (Qj < 1e-12).any() or QR > 1e-6:
                 cell["label"] = "UNINFORMATIVE"; cells.append(cell); continue
             rules = {}
             for rname, p in (("Qshare", 2.0), ("p1", 1.0), ("p4", 4.0)):
-                cu, wu, _ = draw(rng, H.charges_power(psi, masks, p))
-                cm, wm, _ = draw(rng, H.charges_power(psi, merged, p))
+                cu, wu, _ = draw(rng_shot, H.charges_power(psi, masks, p))
+                cm, wm, _ = draw(rng_shot, H.charges_power(psi, merged, p))
                 fu, fm = cu / NSHOT, cm / NSHOT
                 sA = math.sqrt(wu[0] * (1 - wu[0]) / NSHOT + wm[0] * (1 - wm[0]) / NSHOT)
                 sD = math.sqrt(wu[3] * (1 - wu[3]) / NSHOT + wm[2] * (1 - wm[2]) / NSHOT)
@@ -836,6 +840,23 @@
     return dict(ok=False, tries=tries)
 
 
+def fine_charges(g, fac, FGS):
+    """r2 fix 1: the C5(c)/(d) fine-graining charges, computed from g["moved"] once, so moved can be discarded.
+    Same masks and arithmetic as the first run's inline code."""
+    out = {}
+    for fg in FGS:
+        fm = fine_masks(g["L"], g["axis"], fg, fac)
+        qpj, qmj = [], []
+        for (sm, comps) in fm:
+            mp_ = g["plus"] if sm is None else (g["plus"] & sm)
+            mm_ = g["minus"] if sm is None else (g["minus"] & sm)
+            qpj.append(chg(g["moved"], mp_, comps)); qmj.append(chg(g["moved"], mm_, comps))
+        qpj, qmj = np.array(qpj), np.array(qmj)
+        Q = g["Qp"] + g["Qm"]
+        out[fg] = (qpj, qmj, 1.0 - (qpj.sum() + qmj.sum()) / Q)
+    return out
+
+
 def check_C5():
     sph = fib_dirs(50)
     dirs = [("fib", i, v) for i, v in enumerate(sph)] + [("axis", i, v) for i, v in enumerate(AXIS_DIRS)]
@@ -844,6 +865,9 @@
     rngs = {s: np.random.default_rng(s) for s in SEEDS}
     spin4 = {s: rand_spin(rngs[s]) for s in SEEDS}
     geo = {}
+    FGS = ["FG1_halves", "FG2_quadrants", "FG3_unread_factor"]
+    cdirs = [(i, sph[i]) for i in range(0, 40, 2)]
+    need_fine = {(st, "fib", i, fac, None) for st in ["S2", "S3", "S5"] for (i, _) in cdirs for fac in factors}
     b_cells = []
     for st in states:
         for (kind, i, n) in dirs:
@@ -852,6 +876,13 @@
                     gkey = (st, kind, i, fac, seed if st == "S4" else None)
                     if gkey not in geo:
                         geo[gkey] = prepare_cell(st, n, fac, spin4[seed] if st == "S4" else None)
+                        # r2 fix 1: keep only scalars and (for C5(c)/(d) cells) the fine charges; drop the arrays
+                        gg = geo[gkey]
+                        if gg["ok"]:
+                            if gkey in need_fine:
+                                gg["fine"] = fine_charges(gg, fac, FGS)
+                            for k in ("moved", "plus", "minus"):
+                                gg.pop(k, None)
                     g = geo[gkey]
                     cell = dict(state=st, dir_kind=kind, dir_index=i, n=n, factor=fac, seed=seed,
                                 official=(kind == "fib"), tries=g["tries"])
@@ -871,8 +902,6 @@
     lab_b = "UNINFORMATIVE" if not sc_b else ("FAIL" if fail_b else "PASS")
     zb = [c["z"] for c in sc_b]
     # C5(c) and C5(d)
-    FGS = ["FG1_halves", "FG2_quadrants", "FG3_unread_factor"]
-    cdirs = [(i, sph[i]) for i in range(0, 40, 2)]
     c_cells, d_cells = [], []
     for st in ["S2", "S3", "S5"]:
         for (i, n) in cdirs:
@@ -880,15 +909,8 @@
                 g = geo[(st, "fib", i, fac, None)]
                 for fg in FGS:
                     if g["ok"]:
-                        fm = fine_masks(g["L"], g["axis"], fg, fac)
-                        qpj, qmj = [], []
-                        for (sm, comps) in fm:
-                            mp_ = g["plus"] if sm is None else (g["plus"] & sm)
-                            mm_ = g["minus"] if sm is None else (g["minus"] & sm)
-                            qpj.append(chg(g["moved"], mp_, comps)); qmj.append(chg(g["moved"], mm_, comps))
-                        qpj, qmj = np.array(qpj), np.array(qmj)
+                        qpj, qmj, fine_res = g["fine"][fg]  # r2 fix 1: precomputed in the (b) loop
                         Q = g["Qp"] + g["Qm"]
-                        fine_res = 1.0 - (qpj.sum() + qmj.sum()) / Q
                     for seed in SEEDS:
                         rng = rngs[seed]
                         base = dict(state=st, dir_index=i, factor=fac, fine_graining=fg, seed=seed)

--- first_run/harness/run_all.py
+++ r2/run_all.py
@@ -1,5 +1,6 @@
 #!/usr/bin/env python3
-"""Orchestrator: runs S0, C1, C2, C3, C4, C5 once each under meter.py (no retries). Caps D8: 1 thread, no GPU,
+"""Orchestrator (r2 rerun, see R2_NOTE.md): runs S0, C4, C5 only, once each under meter.py (no retries); C1-C3 stand
+from the first run /workspace/runs_l20/20261114_l20_833f49f2/. Caps D8: 1 thread, no GPU,
 512 MiB sampled tree RSS (meter kill), 600 s wall each for S0 and C1-C4, 900 s for C5, 2400 s total wall
 (each ceiling = min(per-check cap, remaining total)), 64 MiB output (checked after each check). S0 failure stops the run."""
 import sys
@@ -8,7 +9,7 @@
 RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 HD = os.path.join(RUN, "harness")
 OUTD, LOGD = os.path.join(RUN, "out"), os.path.join(RUN, "logs")
-CHECKS = [("S0", 600), ("C1", 600), ("C2", 600), ("C3", 600), ("C4", 600), ("C5", 900)]
+CHECKS = [("S0", 600), ("C4", 600), ("C5", 900)]  # r2: C1-C3 not rerun
 TOTAL, RSS = 2400.0, 512 * 2 ** 20
 OUTCAP = 64 * 2 ** 20
 
```
