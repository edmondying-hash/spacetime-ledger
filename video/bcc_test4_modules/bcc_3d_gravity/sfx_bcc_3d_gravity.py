#!/usr/bin/env python3
"""Synthesized SFX for bcc_3d_gravity.mp4 (numpy only). Reads timeline.json from the renderer."""
import os, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *
OUT = os.path.dirname(os.path.abspath(__file__)); T = load(OUT); m = Mix(T["total"])
m.add(pad(T["title"][1] + 0.5, (73.42, 110, 146.83)), 0)
e = T["end"] - T["title"][1]
m.add(hum(e + 1, 41.2, 0.035, level_pts=[(0, 0), (1.5, 1), (e - 0.5, 1), (e + 1, 0)]), T["title"][1])  # deep bed
for k, t in enumerate(T["profile_pts"]): m.add(tick(1760 - 90 * k, 0.035), t, pan=-0.5 + 0.12 * k)    # W(r) falls
m.add(rising_tone(2.0, 330, -0.5, 0.04), T["rw"] - 0.2)                                              # r*W falls
for k, t in enumerate(T["ray_ticks"]): m.add(click(1800, 0.035, m.rng), t, pan=-0.6 + 1.2 * k / 22)   # rays step
m.add(chime(880, 2.5, 0.11), T["lag"] + 0.1)
for k, t in enumerate(T["zig"]): m.add(click(2400 if k % 2 == 0 else 1600, 0.06, m.rng), t, pan=0.4 if k % 2 else -0.4)
p0, p1 = T["pascal"]; m.add(pad(p1 - p0, (196, 246.94, 293.66), 0.035), p0)
m.add(whoosh(1.2, 400, 3000, 0.06, m.rng), T["centroid"] - 0.2)
for i, (t, lag) in enumerate(T["coupler"]): m.add(thump(50 + 3 * lag, 0.27, m.rng), t, pan=-0.45 + 0.3 * i)
m.add(chime(660, 3.5, 0.09), T["end"] + 0.2)
m.write(os.path.join(OUT, "bcc_3d_gravity_sfx.wav")); print("wrote sfx")
