# bcc3dhorizonsim: v2_sound notes (Nov 13, 2026)

**Deliverable:** `bcc3dhorizonsim.mp4`, 46.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz stereo. Audio: -16.1 LUFS integrated, true peak -2.3 dBTP, sample peak -2.31 dBFS, no clipping.

Source: v4 `bcc3dhorizonsim.py` (unchanged module).
## Changes vs the published version
- Run settings: the published video used a 17³ grid (the old README's CLI example). The v4 README and `run_bcc_suite.py` now use the defaults (19³, 2400 load, 300 packets), and that example was removed, so v2 uses the defaults.
- Numbers: core 19 / shell 38 → 105 deadlocked / shell 131 after 300 packets (published 17³: 98 / 130); escaped 0; block 7×7×7.
- Checkpoints: 50 → 37, 100 → 50, 200 → 83, 300 → 105.
- Radial profile (r 0–6): 244.33, 187.19, 108.61, 121.81, 29.42, 19.32, 12.61 (r 0–3 blocked; r = 4 adds 1 tick).
- Header: "(defaults: 19³ grid, 2400 load, 300 packets)". Slice label: "z = 9 (19³ grid)". 3D view: centre ± 4.
- Captions: "300 packets: 105 deadlocked, shell 131"; end card "Core 19 → 105 nodes after 300 packets". "Escaped = 0 is hard-coded" and "no comparison to a real black hole" are kept (checked in v4).

## Sound (sfx_bcc3dhorizonsim.py, numpy synthesis, original)
A falling whoosh when the core locks, a low drone that deepens and swells as the deadlocked count grows, rate-limited packet clicks, lock clicks for new deadlocks, chimes at the 4 checkpoints, and thumps on the radial bars.

## Pipeline (same for all 8 v2_sound videos)
- `python3 render_<name>.py` renders matplotlib frames into ffmpeg (libx264 crf 18, yuv420p, 1920x1080, 30 fps), writes `timeline.json`, runs the sfx script (numpy synthesis, 48 kHz stereo wav), then masters and muxes AAC 192k.
- Mastering (`_common/bccvid.py: loudnorm_mux`): gain to −16 LUFS, then a 4×-oversampled look-ahead limiter at −3 dBFS, re-measured up to 3 times so the result stays on −16 LUFS. This replaced plain ffmpeg loudnorm, which left born and gravity at +1.7 / +4.1 dBTP (clipping) on their first pass.
- `python3 render_<name>.py --audio-only` reuses the finished video stream and only redoes the sound.
- Each folder has the MP4, `.mp4.sha256`, `contact_sheet.jpg`, `thumbnail.png`, the renderer, the sfx script, `timeline.json`, the sfx wav and `audio_levels.json`.
- The published version (in `/workspace/bcc_test4_videos/<name>/`) is left untouched. Edmond's files are not modified.
