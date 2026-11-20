# relativistic_mercury.mp4 — Mercury, 0 K and up (toy model)

Source: `spacetime/elements/bcc_relativistic_mercury.py`, main @ 2276456040a8036c77f6499f2de915f819c52402
(sha256 f61ef7f02666ff6d957382f7c22e2e09b5d15681ae214df47276479dea48f755, matches GitHub raw). The render was made from an unmodified copy; the program itself lives at `spacetime/elements/bcc_relativistic_mercury.py` and is not duplicated here.

Video: 1920x1080, 30 fps, 39.5 s, H.264 + AAC 192k. Audio -16.0 LUFS integrated, -3.0 dBTP true peak.
Structure: title 3 s · sweep 31.5 s (0 → 800 K) · end card 5 s.

## What the program computes
- `mercury_thermal_phase_sweep(temps)`: for each T it returns °C = T − 273.15 and kT = 8.617333e-5·T eV (computed),
  plus a state string chosen by fixed `if` thresholds: < 4.15 K superconductor, < 234.32 K rhombohedral solid,
  < 629.88 K liquid metal, otherwise vapor. The thresholds are measured Hg values typed into the code, not derived.
  Nothing in the program uses kT, the cohesion energy or the relativistic numbers to decide the phase.
- `relativistic_core_comparison()`: β = Z·α, γ = 1/√(1−β²), contraction = 1 − 1/γ. For Hg: 0.5838, 1.2317, 18.81 %.
  These do not depend on temperature.
- `gold_vs_mercury_valence()`: hand-entered table (ionisation 10.44 eV, cohesion 0.67 eV, melt 234.32 K, boil 629.88 K).

## On-screen numbers and where they come from
| On screen | Source |
|---|---|
| T (K), °C, kT (eV) | `mercury_thermal_phase_sweep([T])` called every frame |
| State headline + bracket text | the state string the same call returns, verbatim (split at " (") |
| Phase strip tick values 4.15 / 234.32 / 629.88 | 4.15 is the literal in the sweep function; 234.32 and 629.88 read from `gold_vs_mercury_valence()`; the script asserts the returned state flips exactly at each |
| Hg 1s v/c, γ, contraction | `relativistic_core_comparison()` (labelled constant in T) |
| 800 K end point | chosen for display (the program's own demo stops at 700 K) |

## Display-only (not from the program)
- The atom picture is a small Langevin illustration. Its regime is switched by the program's state string:
  springs to an oblique lattice (solid/SC), cohesive pool under gravity (liquid), free flight (vapor).
  Jitter size, pool shape, speeds and the cyan "pairs" drifting through the lattice in the superconducting range
  are drawn for effect. Labelled "Hg atoms (illustration only)".
- Temperature pacing: piecewise-linear in time with short holds at 4.15, 234.32 and 629.88 K so each phase gets
  screen time. The phase strip uses four equal-width segments (labelled "segments not to scale").
- Sound: synthesized (hum, a tone whose pitch follows position on the strip, chimes when the state string flips,
  a whoosh at boiling). No samples.

## Honesty caveats
- The phase changes are true by construction: they happen at hard-coded measured temperatures, so the video
  shows a lookup table, not a prediction. Nothing is called "predicted".
- °C and kT are the only temperature-dependent computed quantities, and they are simple unit conversions.
- The words in the state strings ("server Cooper pairs", "relativistically decoupled 6s^2") are the program's own
  labels, shown verbatim. The video doesn't add any physics claims of its own.
- At exactly 4.15 / 234.32 / 629.88 K the program already reports the higher phase (strict `<` tests), and the holds show this.

Files: `render_relativistic_mercury.py`, `sfx_relativistic_mercury.py`, `timeline.json`, `audio_levels.json`,
`thumbnail.png` (t = 21 s, liquid), `contact_sheet.jpg`.
The scripts were run on a build box: they import the program from a local `src/` copy and shared helpers (`bccvid.py`, `sfxlib.py`) from that box, so paths at the top of each script need adjusting to re-run.
