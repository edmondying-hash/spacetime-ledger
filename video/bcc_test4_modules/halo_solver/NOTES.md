# bcc_halo_solver: v5 preview notes (Nov 13, 2026, America/New_York)

**Deliverable (preview only — not committed or uploaded):** `bcc_halo_solver.mp4`, 40.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz stereo. Audio: −16.0 LUFS integrated, true peak −3.0 dBTP, sample peak −2.99 dBFS, no clipping.

Source: Edmond's `bcc_test4` copied from bigbang (machine 425d727e-5e8a-489d-99e1-0e1697dfb5ee), including `bcc_halo_solver.py` and `bcc_dark_matter.py` unchanged. sha256 of the preview MP4: `e9c7661141f025c5929ff02cbde393c98e9451e515963e5a914e8ebeead5fe78`.

## Storyboard
1. Title (5 s) on a slowly turning 6-face (axis-aligned) Planck-cube lattice: "Dark-matter halo solver (toy model)".
2. Rotation curve (10 s): `v_baryon` falls off, then `v_total` stays flat, then the gap fills as the halo. Tabulated points from `BCCDarkMatterSim().rotation_curve([2,4,8,14,20])`: 20.06 / 21.26, 16.36 / 19.88, 12.18 / 19.43, 9.26 / 19.58, 7.75 / 19.76.
3. Halo build-up (11 s): stylized Q_EM=0 loops fill a ring around a bright baryon core; enclosed `M_halo` grows. Official invert rows: dark:baryon 0.12 → 0.48 → 1.54 → 3.47 → **5.50 : 1 at r = 20 (84.6% dark)**; M_halo 99.17, 510.26, 1833.38, 4166.80, 6607.90.
4. Cusp vs core (8 s): NFW 1/r cusp climbs inward to **1062.50** at r=0.2; lattice core levels at **84.46**; dashed **100-tick cap** (not reached). ρ₀ = 85, core radius = 2.5 (the profile's core radius; the input halo in `bcc_dark_matter.py` uses r_core = 3.0).
5. Closing (6 s): toy-model framing — the halo is put into the input curve; the solver recovers it (consistency check, not a prediction). Core height set by ρ₀ = 85; the 100-tick cap is not reached.

## Honest framing (on screen)
- Title and footer say toy model. The closer states the halo is an input, the run is a consistency check, not a prediction.
- Smooth strokes evaluate the same `enclosed_loads` / `sqrt(W/r)`, `invert_rotation_curve`, and `cored_vs_cusp_profile` functions at dense radii; markers and labels use the official rounded table values (asserted in the renderer).

## Sound
`sfx_bcc_halo_solver.py`, numpy synthesis, original. Title pad, a falling tone as `v_baryon` drops, a flatter pad as `v_total` holds, a whoosh when the gap fills, a rising tone plus ticks as the dark:baryon ratio climbs, a rising tone as the cusp draws inward, and a closing chime.

## Pipeline
Same as the v2_sound suite: matplotlib frames → ffmpeg libx264 crf 18 → `timeline.json` → sfx wav → `loudnorm_mux` in `_common/bccvid.py` (target −16 LUFS, limiter at −3 dBFS, true peak ≤ −2 dBTP) → contact sheet, thumbnail, sha256, `audio_levels.json`. Tooling reused from `/workspace/bcc_test4_videos/v2_sound/_common/`.
