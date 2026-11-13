# baryon_calculator: v2_sound notes (Nov 13, 2026)

**Deliverable:** `baryon_calculator.mp4`, 44.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz stereo. Audio: -16.0 LUFS integrated, true peak -2.6 dBTP, sample peak -2.75 dBFS, no clipping.

Source: v4 `baryon_calculator.py` (byte-identical to the published run's source).
## Changes vs the published version
- Numbers: none. The module was rerun on v4 and every on-screen value is asserted against the new output; all unchanged.
- Captions: unchanged. Rechecked against the v4 README: the calculator is a fit to PDG anchors, and the video already says so.
- New: a synthesized soundtrack.

## Sound (sfx_baryon_calculator.py, numpy synthesis, original)
Title pad, a soft hum bed, ticks as the PDG inputs and fitted parameters appear, a whoosh on the fit arrow, a rising whoosh as the baselines grow, a rising tone for the spin shifts, and a chime when the PDG markers land.

## Pipeline (same for all 8 v2_sound videos)
- `python3 render_<name>.py` renders matplotlib frames into ffmpeg (libx264 crf 18, yuv420p, 1920x1080, 30 fps), writes `timeline.json`, runs the sfx script (numpy synthesis, 48 kHz stereo wav), then masters and muxes AAC 192k.
- Mastering (`_common/bccvid.py: loudnorm_mux`): gain to −16 LUFS, then a 4×-oversampled look-ahead limiter at −3 dBFS, re-measured up to 3 times so the result stays on −16 LUFS. This replaced plain ffmpeg loudnorm, which left born and gravity at +1.7 / +4.1 dBTP (clipping) on their first pass.
- `python3 render_<name>.py --audio-only` reuses the finished video stream and only redoes the sound.
- Each folder has the MP4, `.mp4.sha256`, `contact_sheet.jpg`, `thumbnail.png`, the renderer, the sfx script, `timeline.json`, the sfx wav and `audio_levels.json`.
- The published version (in `/workspace/bcc_test4_videos/<name>/`) is left untouched. Edmond's files are not modified.
