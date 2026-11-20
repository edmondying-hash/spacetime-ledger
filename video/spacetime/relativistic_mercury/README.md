# Relativistic mercury, 0 K and up (toy model)

`relativistic_mercury.mp4` (1920x1080, 30 fps, 39.5 s) sweeps mercury from 0 K to 800 K. The temperature, °C, kT and phase label on screen come from the program's own functions on each frame.

- **Toy model.** This is an illustration of a toy model, not a simulation of real mercury.
- **Source:** [`spacetime/elements/bcc_relativistic_mercury.py`](../../../spacetime/elements/bcc_relativistic_mercury.py) at commit 2276456.
- **Phase thresholds are measured data written into the code:** 4.15 K (superconducting), 234.32 K (melting), 629.88 K (boiling). The phase changes happen at those values by construction. They are not predictions.
- **What is computed:** only the 1s β = Z·α, γ and orbital contraction (constant in temperature: 0.5838, 1.2317, 18.81 %), and the unit conversions °C = T − 273.15 and kT = k_B·T.
- **Illustration only:** the atom motion (lattice jitter, the liquid pool, vapor flight, the cyan pairs below 4.15 K), the time pacing, the not-to-scale phase strip and the 800 K end point.
- **Sound:** synthesized, no samples.

See [NOTES.md](NOTES.md) for where each on-screen number comes from. Files: video, `thumbnail.png`, `contact_sheet.jpg`, `render_relativistic_mercury.py`, `sfx_relativistic_mercury.py`, `timeline.json`, `audio_levels.json`.
