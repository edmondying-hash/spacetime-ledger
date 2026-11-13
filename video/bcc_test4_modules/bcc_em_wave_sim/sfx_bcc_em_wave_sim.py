#!/usr/bin/env python3
"""Synthesized SFX for bcc_em_wave_sim.mp4 (numpy only). Reads timeline.json from the renderer."""
import os, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *
OUT = os.path.dirname(os.path.abspath(__file__)); T = load(OUT); m = Mix(T["total"])
m.add(pad(T["title"][1] + 0.5, (110, 138.59, 164.81)), 0)
g0 = T["title"][1]; s0, s1 = T["slit"]
m.add(hum(s0 - g0 + 1, 55, 0.035, level_pts=[(0, 0), (1.2, 1), (s0 - g0 - 0.5, 1), (s0 - g0 + 1, 0)]), g0)
for i, t in enumerate(T["residuals"]): m.add(chime(1318.5 + 120 * i, 1.6, 0.07), t)    # residual bars land
m.add(tick(880, 0.04), T["built_in"])
# double slit: a soft tone pulsed at the source period (6 ticks of 120 over ~10.5 s ~ 1.7 Hz)
d = s1 - s0; t = tt(d); trem = 0.5 + 0.5 * np.sin(2 * np.pi * (120 / 6) / 10.5 * t)
wave_tone = 0.04 * (np.sin(2 * np.pi * 220 * t) + 0.3 * np.sin(2 * np.pi * 330 * t)) * trem * edge(len(t), 1.0, 1.0)
m.add(wave_tone, s0, pan=-0.2)
k0 = T["sensor"] - s0; n = len(t)                           # scrambled channel joins after the sensor caption
scr = m.rng.standard_normal(n); scr = lowpass(scr, 900) * trem * np.clip((t - k0) / 0.8, 0, 1) * edge(n, 0.1, 1.0)
m.add(0.6 * 0.04 * scr / (np.abs(scr).max() + 1e-9) * 4, s0, pan=0.35)
m.add(whoosh(1.2, 300, 2400, 0.07, m.rng), T["screen_sum"] - 0.2)
for i, t0 in enumerate(T["screen_bars"]): m.add(thump(64 + 10 * i, 0.28, m.rng), t0, pan=-0.3 + 0.6 * i)
m.add(chime(660, 3.5, 0.09), T["end"] + 0.2)
m.write(os.path.join(OUT, "bcc_em_wave_sim_sfx.wav")); print("wrote sfx")
