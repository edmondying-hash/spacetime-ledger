# bcc_test4 module videos

1080p30 H.264 visualisations for the [toy-model simulation suite](../../bcc_test4/), each with synthesized AAC sound, drawn from the current suite. YouTube links will be added later.

| Module | Video | Length |
| --- | --- | --- |
| `baryon_calculator` | [baryon_calculator.mp4](baryon_calculator/baryon_calculator.mp4) | 44 s |
| `bcc_unified_sim` | [bcc_unified_sim.mp4](bcc_unified_sim/bcc_unified_sim.mp4) | 59 s |
| `bcc_meson_sim` | [bcc_meson_sim.mp4](bcc_meson_sim/bcc_meson_sim.mp4) | 51 s |
| `bcc_em_wave_sim` | [bcc_em_wave_sim.mp4](bcc_em_wave_sim/bcc_em_wave_sim.mp4) | 47 s |
| `bcc_born_pascal` | [bcc_born_pascal.mp4](bcc_born_pascal/bcc_born_pascal.mp4) | 49 s |
| `bcc_3d_gravity` | [bcc_3d_gravity.mp4](bcc_3d_gravity/bcc_3d_gravity.mp4) | 60 s |
| `bcc3dhorizonsim` | [bcc3dhorizonsim.mp4](bcc3dhorizonsim/bcc3dhorizonsim.mp4) | 46 s |
| `uds_mass` | [uds_mass.mp4](uds_mass/uds_mass.mp4) | 48 s |

[`uds_mass`](uds_mass/uds_mass.mp4) is a toy-model visualisation of Λ⁰ (uds). Bare quarks sit at 103 ticks and rise to 814.80 ticks once gluon routing switches on. The MeV scale is calibrated to PDG Λ⁰. The soundtrack is synthesized. [Notes](uds_mass/NOTES.md).

Each module folder holds the MP4, a `.sha256` sidecar, a contact sheet, a thumbnail, `render_<module>.py`, `sfx_<module>.py`, `timeline.json`, `audio_levels.json`, and its own `NOTES.md`. Shared helpers are in [`_common/`](_common/) (`bccvid.py`, `sfxlib.py`). Run logs: [suite_output_v4.txt](suite_output_v4.txt), [unified_output_v4.txt](unified_output_v4.txt), [horizon_cli_v4.txt](horizon_cli_v4.txt). [NOTES.md](NOTES.md) is the earlier first-pass note.

## Render

From the repository root, one module at a time (needs matplotlib, numpy, and ffmpeg; the suite itself does not):

```bash
python3 video/bcc_test4_modules/<module>/render_<module>.py
```

`<module>` is one of the folders above. Check a video from its folder:

```bash
sha256sum -c baryon_calculator.mp4.sha256
```
