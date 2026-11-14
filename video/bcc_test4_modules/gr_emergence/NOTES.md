# bcc_gr_emergence: v5 final notes (Nov 13, 2026, America/New_York)

**Deliverable (prep only — not committed or uploaded):** `bcc_gr_emergence.mp4`, 38.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz stereo. Audio: −16.0 LUFS integrated, true peak −2.8 dBTP, sample peak −2.84 dBFS, no clipping.

Source: Edmond's `bcc_test4` copied from bigbang, `bcc_gr_emergence.py` unchanged. sha256 of the final MP4: `310e51848158e090fa5785f3e117ea5b80309c3e177a9b2ff6897688ac263a98`.

## Change vs the approved preview
Title card only: "Emergent weak-field GR (toy model)" → **"Weak-field GR on the lattice (toy model)"**. Everything else (timing, clocks, rosette, numbers, closer, soundtrack) is unchanged. Re-rendered, re-mastered, thumbnail / contact sheet / sha256 regenerated. Edmond asked for this title change when approving the preview (t267u).

## Storyboard
1. Title (4.5 s): "Weak-field GR on the lattice (toy model)" over a faint row of clocks (rightmost already ringed in red).
2. Time dilation (14 s): five clocks at r = 20, 10, 6, 4, 3 ticking at the code's `grid_dtau_dt` rates 0.921954, 0.836660, 0.707107, 0.500000, 0.000000 (W = 15.00, 30.00, 50.00, 75.00, 100.00). The r = 3 clock is frozen at the 100-tick deadlock. On-screen note: dτ/dt = √(1 − W/C) with W = C·r_s/r, same as Schwarzschild by construction.
3. Perihelion precession (13.5 s): a Keplerian ellipse (a = 1200, e = 0.50, r_s = 3) traces a 7-orbit rosette. The drawn advance is the code's grid value 0.031657 rad/orbit **exaggerated ×15 for display** (labelled on the plot and in the caption). Side panel: grid 0.031657 vs GR 0.031416 rad/orbit, diff 0.767% (`rel_error_pct` from `perihelion_precession`).
4. Closing (6 s): "Workload is set to W = C · r_s / r, so it reproduces GR's numbers" / "Emergence on the full grid is still to be tested."

Light deflection is omitted (already covered in an earlier video).

## Honest framing
- Time dilation equals Schwarzschild at these radii because W is defined as C·r_s/r, not because a grid was solved. That is stated on the clock scene and the closer.
- The rosette path is a standard precessing Keplerian ellipse using the code's grid advance; the ×15 factor is visual only and labelled.

## Sound
`sfx_bcc_gr_emergence.py`, numpy synthesis, original. Title pad; a proper-time click every 1 s of τ on each live clock (pitched and panned by radius); a thump and low drone on the deadlocked clock; a whoosh at each periapsis; a chime on the 0.767% callout and the closer.

## Pipeline
Same as the halo preview and the v2_sound suite, tooling from `/workspace/bcc_test4_videos/v2_sound/_common/`.
