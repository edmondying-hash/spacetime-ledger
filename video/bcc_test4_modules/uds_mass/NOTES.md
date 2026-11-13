# uds_mass: v2_sound notes (Nov 13, 2026)

**Deliverable:** `uds_mass.mp4`, 48.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz stereo. Audio: -16.1 LUFS integrated, true peak -2.7 dBTP, sample peak -2.99 dBFS, no clipping.

Source: v4 `bcc_unified_sim.py` via `grid_values.py`. That file is a copy updated to the new API: `BCCUnifiedGridSim(size=8).simulate_baryon_family(..., cycles=3000, seed=42+idx)`, exactly as `run_unified_demo()` calls it. The old copy crashed because `BCCUnifiedGrid` no longer exists.
Edmond's `animate_uds_mass.py` (now also at the v4 suite root, identical) is unchanged and **still hard-codes the old numbers**: route 534.9, spin −6.2, "1 tick ≈ 1.77 MeV".
## Number changes vs the published version
| item | published (v3 code) | v2 (v4 code) |
|---|---|---|
| Λ bare / route / spin / total ticks | 103.0 / 534.9 / −6.2 / 631.75 | 103.0 / 716.9 / −5.1 / 814.80 |
| bare formula | 4 + 4 + 95 input costs | 12 + 91 per s quark |
| MeV scale (calibrated to PDG Λ⁰ 1115.683) | 1.766 MeV/tick | 1.369 MeV/tick (the code has no MeV scale for baryons; its glueball printout treats ticks as MeV 1:1) |
| bare in MeV | 181.9 | 141.0 |
| links + spin share of Λ | 83.7 % | 87.4 % ((716.9 − 5.1) / 814.8; the code's own Load% column is a hard-coded 87.0) |
| p (uud) | 544.65 ticks → 961.9 MeV (PDG 938.27, +23.6) | 720.94 → 987.2 MeV (+48.9) |
| Ω⁻ (sss) | 821.23 → 1450.3 MeV (PDG 1672.45, −222.2) | 1006.39 → 1378.0 MeV (−294.4) |
| Act 3 routing labels | ≈ 535 | 715.4 / 716.9 / 720.6 ("≈ 715–721") |
## Caption changes
- Act 1: "Bare u, d, s at rest: 12 + 91 (one s) = 103 ticks, by formula".
- Act 2: "Routing adds 716.9 ticks (95 × avg links); spin term −5.1". The meter legend says "spin term" instead of "spin pair", since v4 has no u–d pair.
- Act 3: "Routing stays near 715–721 ticks"; "Same scale: p 987 vs 938, Ω⁻ 1378 vs 1672 MeV".
- Title: "(v4, 6-face)". v4 really does hop one face at a time; the published video had dropped "6-face" because v3 used 8 diagonals. Quark motion is still labelled illustrative.
- End card: bare formula, 87.4 %, scale 1.369 (fitted to PDG Λ⁰), "Ω⁻ off by −294 MeV; not a QCD result".
- Layout: the Λ value label was lifted above the PDG line, because Λ matches PDG exactly by calibration.

## Sound (sfx_uds_mass.py, numpy synthesis, original)
Same design as the published uds video: a pad swell, a 55 Hz throbbing hum, panned hop clicks (u left, d right, s centre), a whoosh as the links switch on, a one-octave rising tone with the mass climb, a bell chime on landing (814.80 ticks / 1115.68 MeV), thumps as the bars grow, PDG ticks, and an end chime.

## Pipeline (same for all 8 v2_sound videos)
- `python3 render_<name>.py` renders matplotlib frames into ffmpeg (libx264 crf 18, yuv420p, 1920x1080, 30 fps), writes `timeline.json`, runs the sfx script (numpy synthesis, 48 kHz stereo wav), then masters and muxes AAC 192k.
- Mastering (`_common/bccvid.py: loudnorm_mux`): gain to −16 LUFS, then a 4×-oversampled look-ahead limiter at −3 dBFS, re-measured up to 3 times so the result stays on −16 LUFS. This replaced plain ffmpeg loudnorm, which left born and gravity at +1.7 / +4.1 dBTP (clipping) on their first pass.
- `python3 render_<name>.py --audio-only` reuses the finished video stream and only redoes the sound.
- Each folder has the MP4, `.mp4.sha256`, `contact_sheet.jpg`, `thumbnail.png`, the renderer, the sfx script, `timeline.json`, the sfx wav and `audio_levels.json`.
- The published version (in `/workspace/bcc_test4_videos/<name>/`) is left untouched. Edmond's files are not modified.
