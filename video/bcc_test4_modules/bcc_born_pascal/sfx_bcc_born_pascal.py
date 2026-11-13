#!/usr/bin/env python3
"""Synthesized SFX for bcc_born_pascal.mp4 (numpy only). Reads timeline.json from the renderer."""
import os, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *
OUT = os.path.dirname(os.path.abspath(__file__)); T = load(OUT); m = Mix(T["total"])
m.add(pad(T["title"][1] + 0.5, (130.81, 196, 261.63)), 0)
e = T["end"] - T["title"][1]
m.add(hum(e + 1, 65.4, 0.025, level_pts=[(0, 0), (1.5, 1), (e - 0.5, 1), (e + 1, 0)]), T["title"][1])
for n, t in enumerate(T["ticks"], 1):                       # each tick: paired clicks (+ and - channel)
    m.add(click(1200 + 70 * n, 0.035, m.rng), t, pan=-0.35)
    m.add(click(1000 + 70 * n, 0.03, m.rng), t + 0.05, pan=0.35)
for k in range(6): m.add(tick(1568 + 0 * k, 0.035), T["dark"] + 0.25 + 0.12 * k, pan=-0.75 + 0.3 * k)  # dark nodes
m.add(chime(784, 2.5, 0.10), T["dark"] + 0.2)
b0, b1 = T["born_rise"]; m.add(whoosh(b1 - b0 + 0.5, 200, 2000, 0.09, m.rng), b0)
m.add(rising_tone(2.2, 220, 0.5, 0.04), T["ref"] - 0.3)
for i, (t, err) in enumerate(T["conv"]):                   # convergence points: thumps get softer/higher
    m.add(thump(60 + 10 * i, 0.30 * (0.5 + 2 * err), m.rng), t)
m.add(chime(660, 3.5, 0.09), T["end"] + 0.2)
m.write(os.path.join(OUT, "bcc_born_pascal_sfx.wav")); print("wrote sfx")
