# bcc_unified_sim: v2_sound notes (Nov 13, 2026)

**Deliverable:** `bcc_unified_sim.mp4`, 59.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz stereo. Audio: -16.1 LUFS integrated, true peak -2.5 dBTP, sample peak -2.50 dBFS, no clipping.

Source: v4 `bcc_unified_sim.py`, which is a full rewrite. The renderer was written from scratch: `BCCUnifiedGridSim`, 6-face hops, `simulate_*` methods.
## Number changes vs the published version (v3 code)
| item | published | v2 (v4 code) |
|---|---|---|
| baryon grid masses N / Δ / Λ / Σ / Ξ / Σ* / Ξ* / Ω | 544.65 / 552.26 / 631.75 / 637.07 / 721.49 / 643.92 / 731.96 / 821.23 | 720.94 / 722.29 / 814.80 / 835.02 / 917.67 / 839.12 / 928.14 / 1006.39 |
| Λ terms | bare 103, route 534.9, spin −6.2 | bare 103.0, route 716.9, spin −5.1 |
| pair-spin rule comparison | refitted rule shown (A = 5.07) | removed: v4 no longer computes it (its header still says "vs. Pair-Spin Rule") |
| cycles | 6000 | 3000, seed 42 + index |
| glueball 4 / 6 / 8 links | 2001.18 / 2851.75 / 3694.67 | 2001.19 / 2851.47 / 3701.75 (closed-form: (102.58 + 145.045L) + (198.05 + 280.095L)) |
| lensing lags | 0, 0, 7, 10, 7, 0, 0 | 0, 0, 5, 10, 5, 0, 0 (v4 README still says 10 / 7 / 0) |
| deadlock | 13 → 23 core, shell 66 → 116 | 13 → 23 core, shell 40 → 73, escaped 0 |
## Caption claim changes
- Lattice: hopping is now one random face (6-face), so the title says "6-face"; the published version showed diagonal hops.
- Part 1: "Bare (12 + 91 per s quark) and spin are set by formula, not measured". Only the route term (95 × average Steiner links) comes from the hops. Load% (98 − 11·n_s) is hard-coded, so it is not shown as a result.
- Dropped "rule refitted to grid N, Δ, Λ" (no rule any more). The bars show bare + routing; the spin term (≤ 6.5) is listed and not drawn.
- Part 2: "The code computes this from a linear formula; no loop is simulated". The axis reads "printed as MeV (= ticks)" because the module labels ticks as MeV 1:1.
- Part 3: "Lag = 10 / (1 + 0.22 d²) for d ≤ 3, else 0: a formula, not a field". The cluster is drawn as schematic; there is no load field in v4.
- Part 4: "Each hit joins the core with 8% chance, capped at 23 nodes"; "Escaped = 0 is hard-coded".
- End card: "Λ grid mass 814.80 ticks; no MeV scale in the code".
- The N trace (a copied loop) is asserted to reproduce 720.94, and the deadlock copy to reproduce 23 / 73.

## Sound (sfx_bcc_unified_sim.py, numpy synthesis, original)
A title pad, a 55 Hz hum bed, a click per hop pitched by the link count, a whoosh as the family bars fill, a tick on the formula caption, glueball thumps pitched by mass, a chime on the formula, 24 lag-step clicks, a chime on the lag result, packet clicks, growth thumps, a chime at the 23-node cap, and an end chime.

## Pipeline (same for all 8 v2_sound videos)
- `python3 render_<name>.py` renders matplotlib frames into ffmpeg (libx264 crf 18, yuv420p, 1920x1080, 30 fps), writes `timeline.json`, runs the sfx script (numpy synthesis, 48 kHz stereo wav), then masters and muxes AAC 192k.
- Mastering (`_common/bccvid.py: loudnorm_mux`): gain to −16 LUFS, then a 4×-oversampled look-ahead limiter at −3 dBFS, re-measured up to 3 times so the result stays on −16 LUFS. This replaced plain ffmpeg loudnorm, which left born and gravity at +1.7 / +4.1 dBTP (clipping) on their first pass.
- `python3 render_<name>.py --audio-only` reuses the finished video stream and only redoes the sound.
- Each folder has the MP4, `.mp4.sha256`, `contact_sheet.jpg`, `thumbnail.png`, the renderer, the sfx script, `timeline.json`, the sfx wav and `audio_levels.json`.
- The published version (in `/workspace/bcc_test4_videos/<name>/`) is left untouched. Edmond's files are not modified.
