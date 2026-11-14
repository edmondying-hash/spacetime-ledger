#!/usr/bin/env python3
"""Synthesized SFX for bcc_gr_emergence.mp4 (numpy only). Reads timeline.json from the renderer."""
import os, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *
OUT = os.path.dirname(os.path.abspath(__file__)); T = load(OUT); m = Mix(T["total"])
m.add(pad(T["title"][1] + 0.5, (65.41, 98.00, 130.81)), 0)
e = T["end"] - T["title"][1]
m.add(hum(e + 1, 36.7, 0.030, level_pts=[(0, 0), (1.5, 1), (e - 0.5, 1), (e + 1, 0)]), T["title"][1])
# clocks: a click every 1 s of proper time, pitched and panned by radius (outer = left/higher)
for ev in T["clicks"]:
    i, rate = ev["i"], ev["rate"]
    freq = 1760 - 180 * i
    m.add(tick(freq, 0.032), ev["t"], pan=-0.7 + 0.35 * i)
# deadlock: a dull thump, then a low locked drone on the rightmost clock
m.add(thump(48, 0.22, m.rng), T["deadlock"], pan=0.75)
dlen = T["clocks"][1] - T["deadlock"]
if dlen > 0.4:
    m.add(hum(dlen + 0.4, 32.0, 0.025, level_pts=[(0, 0), (0.4, 1), (dlen, 0.7), (dlen + 0.4, 0)]),
          T["deadlock"], pan=0.8)
# orbit: whoosh at each (exaggerated) periapsis
for k, t in enumerate(T["peri"]):
    m.add(whoosh(0.7, 220, 2400, 0.07, m.rng), t - 0.15, pan=-0.3 + 0.1 * (k % 3))
m.add(pad(T["orbit"][1] - T["orbit"][0], (146.83, 196.00, 220.00), 0.032), T["orbit"][0])
m.add(chime(784, 2.2, 0.09), T["prec_ann"])
m.add(chime(587, 3.4, 0.10), T["end"] + 0.15)
m.write(os.path.join(OUT, "bcc_gr_emergence_sfx.wav")); print("wrote sfx")
