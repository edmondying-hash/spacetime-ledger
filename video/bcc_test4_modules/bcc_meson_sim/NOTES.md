# bcc_meson_sim: v2_sound notes (Nov 13, 2026)

**Deliverable:** `bcc_meson_sim.mp4`, 51.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz stereo. Audio: -16.1 LUFS integrated, true peak -2.5 dBTP, sample peak -2.68 dBFS, no clipping.

Source: v4 `bcc_meson_sim.py` (unchanged module).
## Changes vs the published version
- Numbers: none. Rerun on v4; all values asserted and unchanged.
- Captions: unchanged; rechecked against the v4 README.
- New: a synthesized soundtrack.

## Sound (sfx_bcc_meson_sim.py, numpy synthesis, original)
Ticks for the PDG diamonds, two low thumps for the D / D* misses, up/down tones for the spin splitting, per-hop clicks as the flux tube stretches with a rising tension tone, then a thump and bright chime at the string snap.

## Pipeline (same for all 8 v2_sound videos)
- `python3 render_<name>.py` renders matplotlib frames into ffmpeg (libx264 crf 18, yuv420p, 1920x1080, 30 fps), writes `timeline.json`, runs the sfx script (numpy synthesis, 48 kHz stereo wav), then masters and muxes AAC 192k.
- Mastering (`_common/bccvid.py: loudnorm_mux`): gain to −16 LUFS, then a 4×-oversampled look-ahead limiter at −3 dBFS, re-measured up to 3 times so the result stays on −16 LUFS. This replaced plain ffmpeg loudnorm, which left born and gravity at +1.7 / +4.1 dBTP (clipping) on their first pass.
- `python3 render_<name>.py --audio-only` reuses the finished video stream and only redoes the sound.
- Each folder has the MP4, `.mp4.sha256`, `contact_sheet.jpg`, `thumbnail.png`, the renderer, the sfx script, `timeline.json`, the sfx wav and `audio_levels.json`.
- The published version (in `/workspace/bcc_test4_videos/<name>/`) is left untouched. Edmond's files are not modified.
