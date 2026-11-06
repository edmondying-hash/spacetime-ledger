# OP2 star collapse — Quantized Space-Ledger toy model (educational video)

Illustration of a proposed model for The Quantized Space-Ledger explainer series.

## Latest approved release: v3

[`op2_collapse_v3.mp4`](op2_collapse_v3.mp4) is the approved release (Intuition, 6 Nov 2026, 9:08 AM ET: "looks good, please go ahead and commit and publish"). This commit stores that file unchanged. It is the release, not a preview.

Two changes from v2, and nothing else:

1. The dashed outer halo ring stays visible, drawn last at the same scene `r_out`. That ring is the illustrative blast-extent boundary, not a new fitted radius. Grid motion and advection match v2.
2. Captions state that the smooth motion is an illustrative interpolation between separate mass states, not measured collapse dynamics (`Illustrative transitions between separate mass states.` / `Not measured collapse dynamics.`).

Timing stays 38 s. The numeric states, 8-direction inward beads, and model caveats are the same as v2.

| File | Role |
|---|---|
| [`op2_collapse_v3.mp4`](op2_collapse_v3.mp4) | Approved release video |
| [`op2_collapse_v3.mp4.sha256`](op2_collapse_v3.mp4.sha256) | SHA-256 of that file |
| [`thumbnail_v3.png`](thumbnail_v3.png) | Frame at t = 29 s from the v3 MP4 (inward-collapse scene) |
| [`render_op2_v3.py`](render_op2_v3.py) | Portable renderer for a local regeneration |

Check the stored video from this directory:

```bash
sha256sum -c op2_collapse_v3.mp4.sha256
```

## Earlier release: v2

v2 stays in this folder. v3 does not replace those bytes.

| File | Role |
|---|---|
| [`op2_collapse_v2.mp4`](op2_collapse_v2.mp4) | Reviewed v2 video |
| [`op2_collapse_v2.mp4.sha256`](op2_collapse_v2.mp4.sha256) | SHA-256 of that file |
| [`thumbnail.png`](thumbnail.png) | Frame at t = 29 s from the v2 MP4 |
| [`storyboard.md`](storyboard.md) / [`storyboard.pdf`](storyboard.pdf) | Approved v2 board and approval history |
| [`render_op2_v2.py`](render_op2_v2.py) | v2 renderer |
| [`make_storyboard.py`](make_storyboard.py) | Board stills and PDF only; does not encode either MP4 |

```bash
sha256sum -c op2_collapse_v2.mp4.sha256
```

## Spec

| Field | Value |
|---|---|
| Resolution | 1920×1080 |
| Codec | H.264, yuv420p |
| Frame rate | 30 fps |
| Duration | 38.000 s |
| Audio | none |
| Style | dark cyan/gold; corner + toy-model framing; ≥28 pt captions |

## What the picture shows

Radial-shell mean-field toy (Pauli v4) at **G = 0.01** in model units. The labels are **separate added-mass states**, not snapshots of one dynamical run. On-screen motion, timing, and radii are **illustrative interpolation** between those states. The support cap is a **chosen** reading of the model (LCAP = 7: 8-neighbour spill). Equilibrium rows at and past that cap sit on the **grid floor** (R_half = 1). The post-cap state on screen (N = 46127) keeps an **extended halo** (R_out = 18).

| Label | N | half-mass density ρ_half | Equilibrium radii in the excerpts |
|---|---|---|---|
| A supported | 141 | ≈ 1.93 (exact 1.925…) | R_half ≈ 2.06, R_out = 3 |
| B near collapse | 3853 | ≈ 8.1 (exact 8.066…) | R_half ≈ 3.85, R_out = 8; core ~4× A |
| Chosen cap | **4738** | — | `collapse_N`. That row is already R_half = 1, R_out = 6 |
| C post (~10× N_c) | 46127 | ≈ 5500 (exact 5506…) | R_half = 1 (grid floor), R_out = 18 (extended halo) |

ρ_half = (N/2) / (4/3 π R_half³). Outer density stays ~1–2 because a thin ground-level envelope remains.

Local excerpts and the toy-run notes:

- [`provenance/pauli_deg4_SUMMARY.md`](provenance/pauli_deg4_SUMMARY.md)
- [`provenance/pauli_massdens_SUMMARY.md`](provenance/pauli_massdens_SUMMARY.md)
- [`data/pauli_massdens_G0.01_excerpt.json`](data/pauli_massdens_G0.01_excerpt.json)
- [`data/pauli_deg4_G0.01_excerpt.json`](data/pauli_deg4_G0.01_excerpt.json)

The summaries also mention neighboring G values from the same scan. The video uses the G = 0.01 rows. Full runs originally lived on a workstation under `gpu/pauli_deg4/` and `gpu/pauli_massdens/`; those directories are not in this repository. The JSON files here are the small verified excerpts.

## Scope

Kept in line with the on-screen lines.

- Blast-spill is a load-packing rule for the outer radius.
- The cap LCAP = 7 is a disclosed model choice.
- R = 1 is the lattice floor.
- Timing on screen is illustrative.
- Supernova, ejecta, bounce, nuclear burning, a neutron-star phase, a black hole or horizon, and empirical stellar validation are outside this illustration. The toy's planet-to-dense gap is about 4–5× at G = 0.01, and the scan has no sustained white-dwarf R ∝ M⁻¹/³ branch.

## Regenerate (optional)

Python 3 dependencies:

- `numpy`
- `matplotlib`
- `ffmpeg` on `PATH` (H.264 encode)

From this directory, the v3 renderer:

```bash
python3 render_op2_v3.py
```

That writes `./op2_collapse_v3.mp4`, `./frames_v3/`, and `./qa_stills_v3/`. Set `OP2_OUT` to write somewhere else:

```bash
OP2_OUT=/path/to/dir python3 render_op2_v3.py
```

The v2 renderer is the same command with [`render_op2_v2.py`](render_op2_v2.py). It writes `./op2_collapse_v2.mp4`, `./frames_v2/`, and `./qa_stills_v2/`.

Re-running replaces a local MP4. It does not reproduce the reviewed file byte for byte. The committed MP4 and its `.sha256` sidecar are the release.

Storyboard stills and PDF only (no video). Also needs `pillow` (imported as `PIL`) to check that each still is 1920×1080:

```bash
python3 make_storyboard.py
```

Outputs `storyboard.pdf` and `sb_01_setup.png` … `sb_06_after.png` in this directory.
