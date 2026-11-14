#!/usr/bin/env python3
"""Synthesized SFX for bcc_halo_solver.mp4 (numpy only). Reads timeline.json from the renderer."""
import os, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *
OUT = os.path.dirname(os.path.abspath(__file__)); T = load(OUT); m = Mix(T["total"])
m.add(pad(T["title"][1] + 0.5, (73.42, 110, 146.83)), 0)
m.add(whoosh(1.4, 200, 2200, 0.07, m.rng), 0.3)
e = T["end"] - T["title"][1]
m.add(hum(e + 1, 49.0, 0.032, level_pts=[(0, 0), (1.5, 1), (e - 0.5, 1), (e + 1, 0)]), T["title"][1])
# v_baryon stroke: falling ticks, then a descending tone
b0, b1 = T["vbar"]
m.add(rising_tone(b1 - b0 + 0.3, 392, -0.85, 0.045), b0)
for k, t in enumerate(T["vbar_pts"]):
    m.add(tick(1760 - 120 * k, 0.04), t, pan=-0.55 + 0.12 * k)
# v_total: flatter sustained tone + ticks
t0, t1 = T["vtot"]
m.add(pad(t1 - t0 + 0.4, (196, 246.94, 293.66), 0.04), t0)
for k, t in enumerate(T["vtot_pts"]):
    m.add(tick(1320, 0.035), t, pan=-0.2 + 0.12 * k)
m.add(whoosh(1.5, 180, 2600, 0.10, m.rng), T["gap"] - 0.15)
# halo build-up: ticks at tabulated r, rising tone as the ratio climbs
h0, h1 = T["halo"]
m.add(rising_tone(T["ratio_final"] - h0 + 0.2, 196, 1.15, 0.05), h0 + 0.2)
for k, t in enumerate(T["halo_pts"]):
    m.add(tick(990 + 80 * k, 0.045), t, pan=-0.4 + 0.18 * k)
m.add(chime(784, 2.2, 0.10), T["ratio_final"] + 0.05)
# cusp vs core: a rising tone as the 1/r cusp climbs inward
c0, c1 = T["cusp_draw"]
m.add(rising_tone(c1 - c0 + 0.2, 220, 1.4, 0.055), c0)
m.add(pad(T["cusp"][1] - T["cusp"][0], (110, 164.81), 0.03), T["cusp"][0])
m.add(tick(880, 0.05), T["cusp_ann"])
m.add(chime(660, 3.4, 0.10), T["end"] + 0.15)
m.write(os.path.join(OUT, "bcc_halo_solver_sfx.wav")); print("wrote sfx")
