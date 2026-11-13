#!/usr/bin/env python3
"""Synthesized SFX for bcc3dhorizonsim.mp4 (numpy only). Reads timeline.json from the renderer."""
import os, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *
OUT = os.path.dirname(os.path.abspath(__file__)); T = load(OUT); m = Mix(T["total"])
m.add(pad(T["title"][1] + 0.5, (82.41, 123.47, 164.81)), 0)
g0 = T["title"][1]; e = T["end"] - g0
m.add(hum(e + 1, 41.2, 0.03, level_pts=[(0, 0), (1.5, 1), (e - 0.5, 1), (e + 1, 0)]), g0)
m.add(whoosh(1.4, 1500, 200, 0.08, m.rng, falling=True), T["contour"] - 0.3)      # core locks: falling whoosh
m.add(thump(46, 0.28, m.rng), T["core"])
# pile-up: a low drone that deepens and swells as the deadlocked count grows
p0, p1 = T["pile"]; t = tt(p1 - p0)
cnt = np.interp(t + p0, [x[0] for x in T["packets"]], [x[1] for x in T["packets"]])
c01 = (cnt - cnt.min()) / (cnt.max() - cnt.min() + 1e-9)
freq = 98 * 2 ** (-0.8 * c01); ph = 2 * np.pi * np.cumsum(freq) / SR
m.add(0.05 * (np.sin(ph) + 0.3 * np.sin(2 * ph)) * (0.4 + 0.6 * c01) * edge(len(t), 0.8, 1.0), p0)
for tp, n in T["packets"]: m.add(click(2600, 0.025, m.rng), tp, pan=float(m.rng.uniform(-0.6, 0.6)))
for tl in T["locks"]: m.add(click(900, 0.05, m.rng), tl, pan=float(m.rng.uniform(-0.4, 0.4)))
for i, tc in enumerate(T["checkpoints"]): m.add(chime(784 * 2 ** (-i / 12 * 3), 1.6, 0.07), tc)
for i, (tr, blocked) in enumerate(T["radial"]): m.add(thump(44 if blocked else 80, 0.26, m.rng), tr, pan=-0.45 + 0.15 * i)
m.add(chime(660, 3.5, 0.09), T["end"] + 0.2)
m.write(os.path.join(OUT, "bcc3dhorizonsim_sfx.wav")); print("wrote sfx")
