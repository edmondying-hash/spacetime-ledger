# bcc_virtual_carriers: v5 preview notes (Nov 13, 2026, America/New_York)

**Deliverable (preview only — not committed or uploaded):** `bcc_virtual_carriers.mp4`, 40.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz stereo. Audio: −16.0 LUFS integrated, true peak −2.8 dBTP, sample peak −2.82 dBFS, no clipping.

Source: snapshot of Edmond's `bcc_virtual_carriers.py` at `/workspace/bcc_test4_videos/v5/carriers_src` (copied from `v5/bcc_test4`, itself from bigbang), imported unchanged. sha256 of the preview MP4: `12c11bf0fb8151b2dddda2d58dd88ccc98258613a7282f7be006b76491677b58`.

## Storyboard
1. Title (5 s) on a slowly turning 6-face (axis-aligned) Planck-cube lattice, with three short traces leaving the centre: "Virtual force carriers on the lattice (toy model)". Subtitle: "One hop per tick on a 6-face grid".
2. Three panels side by side (29 s), hops 1..8 at 3 s each (from t = 5.5 s):
   - **Photon** (m = 0): Manhattan (diamond) shells spread on a 2D slice of the 6-face grid. Official `simulate_carrier_range(mass_mev=0)`: V = 1, 0.5, 0.333333, 0.25, 0.2, 0.166667, 0.142857, 0.125 (shown to 3 decimals); **shell flux stays 1.000 every hop**.
   - **W boson** (m = 80,379 MeV, r₀ = 1.5 hops): the same shells fade with `decay_factor`. Official survival: **0.513417** at hop 1, **0.069483** at hop 4, **0.004828** at hop 8 (captions use the 3-decimal readouts 0.513, 0.069, 0.005). Labelled short-range from hop 4.
   - **Gluon**: a 1D tube grows at **+45 MeV/hop**. Hop 6 = 270 MeV (intact); **hop 7 = 315 MeV > 275 MeV snaps**, and a new q q̄ pair appears. The tube visual is frozen at the snap (the code's hop-8 row is still snapped at 360 MeV and is not drawn as further stretch).
3. Closing (6 s): "The 1/r and decay laws are set in the code" / "W range (1.5 hops) is a set parameter" / "Snap threshold 275 MeV is chosen."

`weak_flavor_transition_rate` is unused by the demo and is not shown.

## Honest framing (on screen)
- Title, footer, and closer say toy model. Nothing is called a prediction.
- The closer states that the 1/r and Yukawa laws are set in the code, that the W range (1.5 hops) is a set parameter, and that the 275 MeV snap threshold is chosen.
- On-screen table values are asserted in the renderer against the official rounded outputs of `BCCVirtualCarrierSim`.

## Sound
`sfx_bcc_virtual_carriers.py`, numpy synthesis, original. Title pad; a shared hop-clock tick each hop; a constant-bright photon ding (left); a W ding that fades with survival; a climbing gluon tick; a thump and chime at the hop-7 snap; a closing chime.

## Pipeline
Same as the halo and GR previews and the v2_sound suite: matplotlib frames → ffmpeg libx264 crf 18 → `timeline.json` → sfx wav → `loudnorm_mux` in `_common/bccvid.py` (target −16 LUFS, limiter at −3 dBFS, true peak ≤ −2 dBTP) → contact sheet, thumbnail, sha256, `audio_levels.json`. Tooling reused from `/workspace/bcc_test4_videos/v2_sound/_common/`.
