# GR geometry vs proposed fixed-BCC lensing (38 s)

Approved release **v2**. A v1 preview (`lensing_comparison_preview.mp4`) was not released. Approved 9 Nov 2026, 8:46 AM ET: "Let's commit and publish on YouTube, thanks."

[`lensing_comparison_v2.mp4`](lensing_comparison_v2.mp4) is that file, stored unchanged.

## What the picture shows

Conceptual side-by-side illustration. Silent, 1920×1080, H.264, 30 fps, 38.000 s.

- **LEFT** illustrates established GR geometric lensing. It is not a newly integrated geodesic.
- **RIGHT** is the proposed fixed-BCC congestion hypothesis on a rigid body-centred-cubic network. Active links are nearest-eight only (body center to the eight corners): 91 nodes, 216 links. The dashed path is a hypothetical deflection, not a calculated prediction.
- Equivalence is not demonstrated. There is no quantitative validation and no accuracy claim.

Footer on screen: "Conceptual illustration — not quantitative validation."

| File | Role |
|---|---|
| [`lensing_comparison_v2.mp4`](lensing_comparison_v2.mp4) | Approved release |
| [`lensing_comparison_v2.mp4.sha256`](lensing_comparison_v2.mp4.sha256) | SHA-256 of that file |
| [`thumbnail.png`](thumbnail.png) | Decoded frame at t = 30 s |
| [`contact_sheet_v2.jpg`](contact_sheet_v2.jpg) | Sample frames |
| [`storyboard.md`](storyboard.md) | Approved 38 s board |
| [`SCIENTIFIC_NOTES_v2.md`](SCIENTIFIC_NOTES_v2.md) | Scope and evidential status |
| [`render_lensing_comparison_v2.py`](render_lensing_comparison_v2.py) | Portable renderer |
| [`bcc_geometry_v2.json`](bcc_geometry_v2.json) | Fixed node and link record |
| [`validation_v2.json`](validation_v2.json) | Probe and path checks from the review render |

From this directory:

```bash
sha256sum -c lensing_comparison_v2.mp4.sha256
```

## Regenerate (optional)

Python 3, `Pillow` (`PIL`), `ffmpeg`, `ffprobe`, and DejaVu Sans at `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` and `DejaVuSans-Bold.ttf`.

```bash
python3 render_lensing_comparison_v2.py
```

Outputs land in this folder: `lensing_comparison_v2.mp4`, `frames_v2/`, `contact_sheet_v2.jpg`, `SCIENTIFIC_NOTES_v2.md`, `validation_v2.json`, `bcc_geometry_v2.json`.

Path edit, not a drawing change: `OUT_DIR` is the directory of the script. The supplied renderer used `/workspace/lensing_storyboard`. Recorded filenames in the notes and validation writer are basenames. A re-run replaces the local MP4 and does not reproduce the reviewed bytes. The committed file and the `.sha256` sidecar are the release.
