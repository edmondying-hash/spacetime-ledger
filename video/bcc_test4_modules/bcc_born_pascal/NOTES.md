# bcc_born_pascal: v2_sound notes (Nov 13, 2026)

**Deliverable:** `bcc_born_pascal.mp4`, 49.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz stereo. Audio: -16.0 LUFS integrated, true peak -2.7 dBTP, sample peak -2.83 dBFS, no clipping.

Source: v4 `bcc_born_pascal.py` (unchanged module).
## Changes vs the published version
- Numbers: none. Rerun on v4; all values asserted and unchanged.
- Captions: unchanged; rechecked against the v4 README.
- New: a synthesized soundtrack. The tick clicks were softened (0.06/0.05 → 0.035/0.03) because the first master overshot (+1.7 dBTP).

## Sound (sfx_bcc_born_pascal.py, numpy synthesis, original)
Title pad, a hum bed, paired L/R clicks on each tick (+ and − channels), ticks for the dark nodes, a chime, a whoosh as the Born curve rises, a rising reference tone, and thumps on the convergence points that get softer as the error shrinks.

## Pipeline (same for all 8 v2_sound videos)
- `python3 render_<name>.py` renders matplotlib frames into ffmpeg (libx264 crf 18, yuv420p, 1920x1080, 30 fps), writes `timeline.json`, runs the sfx script (numpy synthesis, 48 kHz stereo wav), then masters and muxes AAC 192k.
- Mastering (`_common/bccvid.py: loudnorm_mux`): gain to −16 LUFS, then a 4×-oversampled look-ahead limiter at −3 dBFS, re-measured up to 3 times so the result stays on −16 LUFS. This replaced plain ffmpeg loudnorm, which left born and gravity at +1.7 / +4.1 dBTP (clipping) on their first pass.
- `python3 render_<name>.py --audio-only` reuses the finished video stream and only redoes the sound.
- Each folder has the MP4, `.mp4.sha256`, `contact_sheet.jpg`, `thumbnail.png`, the renderer, the sfx script, `timeline.json`, the sfx wav and `audio_levels.json`.
- The published version (in `/workspace/bcc_test4_videos/<name>/`) is left untouched. Edmond's files are not modified.
