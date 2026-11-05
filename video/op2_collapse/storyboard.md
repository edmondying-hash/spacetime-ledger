# OP2 star collapse — approved storyboard (38 s)

This file records the approved board: canvas, captions, and scene times. It is the approval record, not a stand-in for the release. The release artifact is [`op2_collapse_v2.mp4`](op2_collapse_v2.mp4), rendered by [`render_op2_v2.py`](render_op2_v2.py).

[`storyboard.pdf`](storyboard.pdf) and the stills below are written by [`make_storyboard.py`](make_storyboard.py). That generator draws the board. It does not encode the release MP4. The release renderer uses balanced 8-direction inward inflow; the board stills keep the simpler mass-added arrows from the approved layout.

**Canvas:** 1920×1080. **All on-screen text ≥38 px** (~28 pt at 100 dpi).  
**Layout bands:** header (corner row → 2-line gold framing → title) / illustration / 1–2 captions. No overlap. No tiny radius labels.

Persistent on every frame:
- Top-left own row: `Illustration of a proposed model.`
- Top center (2 gold lines): `Illustrative visualization of the` / `Quantized Space-Ledger toy model`

Dataset: **G = 0.01** (model units). Points are separate mass states of a radial-shell mean-field toy. The board bridges them by **adding mass**: A → B → chosen support cap → C. Motion, timing, and on-screen radii are illustrative interpolation, not a measured collapse time series.

## Scene table

| # | Time | Still | Shown | On-screen captions (1–2 lines) |
|---|---|---|---|---|
| F1 | 0–5 s | [sb_01_setup.png](sb_01_setup.png) | Quiet radial cyan square-node lump | `Radial-shell Pauli packing  ·  G = 0.01 (model units)` · `Motion and timing are illustrative, not measured collapse dynamics.` |
| F2 | 5–12 s | [sb_02_supported.png](sb_02_supported.png) | Supported finite lump | `N = 141   ·   half-mass density ≈ 1.93` · `Finite lump held by Pauli packing. Blast-spill sets outer extent.` |
| F3 | 12–19 s | [sb_03_add_mass.png](sb_03_add_mass.png) | Mass-added arrows; denser core | `Mass added  →  N = 3853   ·   half-mass density ≈ 8.1` · `Core denser (~4×). Different mass states, not a time series.` |
| F4 | 19–25 s | [sb_04_cap.png](sb_04_cap.png) | Mass still added; cap mark on core | `Mass added  →  N ≈ 4738` · `Chosen support cap exceeded.` |
| F5 | 25–33 s | [sb_05_collapse.png](sb_05_collapse.png) | Inward arrows; bright core; extended halo | `Core falls to the grid floor. Halo stays extended.` · `Illustrative inward pile-up.` |
| F6 | 33–38 s | [sb_06_after.png](sb_06_after.png) | Mass added again; tiny bright core + halo | `Mass added  →  N ≈ 46,127   ·   half-mass density ≈ 5,500` · `Toy model—not a stellar simulation.` |

Detailed numbers, the LCAP=7 interpretation, sources, and what the frames leave out are on the PDF notes page ([`storyboard.pdf`](storyboard.pdf)).

## Verified G = 0.01 rows

- A: N = 141, ρ_half ≈ 1.93, R_half ≈ 2.06, R_out = 3 (supported)
- B: N = 3853, ρ_half ≈ 8.1, R_half ≈ 3.85, R_out = 8 (supported, denser core)
- Chosen support cap: N = 4738 (`collapse_N`). In the equilibrium excerpt that row is already on the lattice floor (R_half = 1, R_out = 6), not a still-supported star. Scenes 4–5 illustrate the cap being exceeded and the inward pile-up.
- C: N = 46127, ρ_half ≈ 5506 (display 5,500), R_half = 1 (grid floor), R_out = 18 (extended halo)

Local copies: [`data/pauli_massdens_G0.01_excerpt.json`](data/pauli_massdens_G0.01_excerpt.json), [`data/pauli_deg4_G0.01_excerpt.json`](data/pauli_deg4_G0.01_excerpt.json), and the summaries under [`provenance/`](provenance/).

## Approval history

- Board approved (spacetime): "Yes, render this 38-second storyboard."
- An earlier render used the filenames `op2_collapse.mp4` and `render_op2.py`. Those names are history, not the file in this folder.
- Release artifact: reviewed [`op2_collapse_v2.mp4`](op2_collapse_v2.mp4) (1920×1080, H.264, yuv420p, 30 fps, 38.000 s, silent). Commit and publish approved: "Let's commit and publish on YouTube."
