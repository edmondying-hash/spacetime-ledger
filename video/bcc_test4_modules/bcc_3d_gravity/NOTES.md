# bcc_3d_gravity: v2_sound notes (Nov 13, 2026)

**Deliverable:** `bcc_3d_gravity.mp4`, 60.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz stereo. Audio: -16.1 LUFS integrated, true peak -2.1 dBTP, sample peak -2.61 dBFS, no clipping.

Source: v4 `bcc_3d_gravity.py` (unchanged module).
## Changes vs the published version
- Numbers: none. Rerun on v4; all values asserted and unchanged (r·W 86.85 → 29.76, lags 6 / 9 / 12 / 13). The v4 README still says "1/r"; the video keeps "falls faster than 1/r here".
- Captions: unchanged.
- New: a synthesized soundtrack. The first master clipped (+4.1 dBTP); it is fixed by the new limiter.

## Sound (sfx_bcc_3d_gravity.py, numpy synthesis, original)
A deep 41 Hz bed, descending ticks as W(r) falls, a falling tone for r·W, ray-step clicks panned across, and thumps and chimes in the momentum and Pascal scenes.

## Pipeline (same for all 8 v2_sound videos)
- `python3 render_<name>.py` renders matplotlib frames into ffmpeg (libx264 crf 18, yuv420p, 1920x1080, 30 fps), writes `timeline.json`, runs the sfx script (numpy synthesis, 48 kHz stereo wav), then masters and muxes AAC 192k.
- Mastering (`_common/bccvid.py: loudnorm_mux`): gain to −16 LUFS, then a 4×-oversampled look-ahead limiter at −3 dBFS, re-measured up to 3 times so the result stays on −16 LUFS. This replaced plain ffmpeg loudnorm, which left born and gravity at +1.7 / +4.1 dBTP (clipping) on their first pass.
- `python3 render_<name>.py --audio-only` reuses the finished video stream and only redoes the sound.
- Each folder has the MP4, `.mp4.sha256`, `contact_sheet.jpg`, `thumbnail.png`, the renderer, the sfx script, `timeline.json`, the sfx wav and `audio_levels.json`.
- The published version (in `/workspace/bcc_test4_videos/<name>/`) is left untouched. Edmond's files are not modified.
