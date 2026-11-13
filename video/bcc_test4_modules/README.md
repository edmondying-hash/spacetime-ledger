# bcc_test4 module videos

Silent 1080p30 H.264 visualisations of the seven modules in the [toy-model simulation suite](../../bcc_test4/). Each renderer imports that module and checks the plotted numbers against the suite's actual output. YouTube links will be added later.

| Module | Video | Length |
| --- | --- | --- |
| `baryon_calculator` | [baryon_calculator.mp4](baryon_calculator/baryon_calculator.mp4) | 44 s |
| `bcc_unified_sim` | [bcc_unified_sim.mp4](bcc_unified_sim/bcc_unified_sim.mp4) | 59 s |
| `bcc_meson_sim` | [bcc_meson_sim.mp4](bcc_meson_sim/bcc_meson_sim.mp4) | 51 s |
| `bcc_em_wave_sim` | [bcc_em_wave_sim.mp4](bcc_em_wave_sim/bcc_em_wave_sim.mp4) | 47 s |
| `bcc_born_pascal` | [bcc_born_pascal.mp4](bcc_born_pascal/bcc_born_pascal.mp4) | 49 s |
| `bcc_3d_gravity` | [bcc_3d_gravity.mp4](bcc_3d_gravity/bcc_3d_gravity.mp4) | 60 s |
| `bcc3dhorizonsim` | [bcc3dhorizonsim.mp4](bcc3dhorizonsim/bcc3dhorizonsim.mp4) | 46 s |

Each folder also holds a contact sheet, a thumbnail, `render_<module>.py`, `bccvid.py`, and a `.sha256` sidecar. [NOTES.md](NOTES.md) records where the suite README and a fresh run disagree.

## Render

From the repository root, one module at a time (needs matplotlib, numpy, and ffmpeg; the suite itself does not):

```bash
python3 video/bcc_test4_modules/<module>/render_<module>.py
```

`<module>` is one of the seven names above. The script writes the MP4 beside itself.

**Path edit.** The render scripts originally used absolute paths under `/workspace/bcc_test4_videos/`. Those were changed, and the drawing logic was not. `bccvid.py` is loaded from the script's own folder. The suite import is `../../../bcc_test4`, resolved from that same folder. The committed MP4s were not re-encoded.

Check a video from its folder:

```bash
sha256sum -c baryon_calculator.mp4.sha256
```

The sidecar keeps the archive digest and adds the filename so `sha256sum -c` can read it.
