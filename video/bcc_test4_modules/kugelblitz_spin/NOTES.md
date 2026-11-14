# bcc_kugelblitz_spin: v6 preview notes (Nov 14, 2026, America/New_York). Preview only, not committed or uploaded.

**Deliverable:** `bcc_kugelblitz_spin.mp4`, 45.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz. Audio −16.0 LUFS, true peak −3.0 dBTP, sample peak −2.99 dBFS, no clipping.
sha256 `45b21d730bb1ee177b0ad6698ae97605bab855c1fd93a6925455e2f8db9ece67`.

Source: `../kugelblitz_src/` = bigbang `~/bcc_test4/bcc_kugelblitz_spin.py` (mtime 00:47:30, sha256 f0d701f3…900a) and `test_bcc_kugelblitz_spin.py` (00:47:46, eb0d57b9…bd5). Module imported unchanged. `run_output.txt` and `test_output.txt` (4/4 OK) are there too.

## Storyboard
1. Title 4.5 s: "Kugelblitz: action and reaction (toy model)". The stars sit at random distances.
2. Pile-up 10.5 s: stars at random distances (seed 7, r from 3.6 to 9.8), with W(0) = 36 / 80 / 120 (deadlocked) / 216. Caption: "In the code, the load does not depend on star distance."
3. Action and reaction 24 s, 24 stars × 5 ticks:
   - bias 0: L = 0 and nothing turns.
   - bias +0.20: core +14.4 CCW, stars −14.4 CW, sum 0.
   - bias −0.08: core −5.76 CW, stars +5.76 CCW, sum 0.
4. Closer 6 s, "Toy model":
   - The sum is 0 by construction.
   - The spin direction is set by the chosen ray tilt.
   - The star distances are drawn only.
   - The per-star split and the orbit speeds are display choices.

## Display choices (on screen)
- The star distances are random (seed 7). The module puts every star on a single ring, and W, L_core and L_stars don't depend on distance. This is asserted by re-running with ring_radius 4.
- The per-star recoil share is −flux_k·b_k, the module's own per-star terms. The renderer asserts that the shares sum to recoil_stars_lz.
- The orbit rate is share / r² with unit star mass, drawn ×15. The ray tilt is drawn ×8 and the core swirl ×200 (the swirl uses frame_drag_omega).
- Part 3 of the module (the 1/r³ frame-drag profile) is not shown.
