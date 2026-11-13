# uds (Λ⁰) mass video: notes (Nov 13, 2026)

Deliverable: `uds_mass.mp4`, 48.0 s, 1920x1080, 30 fps, H.264 + AAC 48 kHz stereo, about −16 LUFS (true-peak limit −2 dBTP).
Edmond's `animate_uds_mass.py` is unchanged. The numbers come from running `bcc_unified_sim.py`
(v3 suite, identical to the earlier copy) through `grid_values.py`, which writes `grid_values.json`.

Build: `python3 render_uds_mass.py`. It renders the silent video, writes events.json, runs `sfx_uds_mass.py`
to make the wav, then does two-pass loudnorm and muxes the AAC track.

## Number check (his hard-coded value vs. the code's output)
| his script | code output | status |
|---|---|---|
| BareT 103.0 | 103.0 (inputs 4 + 4 + 95 ticks) | ok |
| RouteT 534.9 | 534.905 | ok |
| SpinT −6.2 | −6.1525 | ok (rounded) |
| family bare 12 / 103 / 285 | 12 / 103 / 285 | ok |
| totals 544.65 / 631.75 / 821.23 | 544.654 / 631.753 / 821.225 | ok |
| "1 tick ≈ 1.77 MeV" | the code uses mev_per_tick = 1.0. 1.766 = PDG Λ⁰ 1115.683 / 631.753 | this is a calibration to Λ⁰, not code output; labelled as calibrated |
| "103 ticks (~100 MeV bare)" | 103 × 1.766 = 181.9 MeV | fixed |
| MeV readout interpolated linearly 100 → 1115.68 | ticks × 1.766 everywhere | fixed (one consistent scale) |
| "~84% of mass" from routing | Load% (routing + spin) / total = 83.7%; routing alone 84.7% | shown as 83.7% "in this toy model" |
| Act 3 labels p 938.9 / Λ⁰ 1115.7 / Ω⁻ 1681.9 MeV | these are baryon_calculator's PDG-calibrated pair-spin values, not grid values. Grid × the Λ⁰ scale gives p 961.9 and Ω⁻ 1450.3 MeV (PDG 938.27 / 1672.45: +23.6 / −222.2) | replaced with grid × scale, with PDG shown as dashed lines |
| title "6-Face Planck Grid" | the bcc_unified_sim baryon routine uses 8 diagonal BCC steps on a periodic 8³ grid | "6-face" dropped |

Quark hops are seeded random orthogonal moves, as in his script, and are labelled "quark motion illustrative".
Every frame carries the TOY MODEL footer. No claim is made about real QCD.

## Sound (all synthesized in sfx_uds_mass.py, numpy only)
- Title: a soft A2/E3/A3 sine pad swell.
- Act 1: a 55 Hz hum (plus 110 and 165 Hz) with a slow 0.33 Hz throb. It drops to about 35% in Act 2 and fades out at the start of Act 3.
- Quark hops: 30 ms clicks (high-passed noise plus a sine blip), panned u left, d right, s centre and lower.
- Links switching on: a noise whoosh with a rising low-pass cutoff.
- Mass climb: a soft tone that rises one octave (196 → 392 Hz) in step with the tick readout.
- Landing on 631.75 ticks / 1115.68 MeV: an inharmonic bell chime at 880 Hz.
- Act 3: three soft low thumps as the bars grow, two faint ticks for the PDG markers, and a low chime on the end card.
