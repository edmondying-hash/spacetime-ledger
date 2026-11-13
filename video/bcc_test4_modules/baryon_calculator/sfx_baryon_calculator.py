#!/usr/bin/env python3
"""Synthesized SFX for baryon_calculator.mp4 (numpy only). Reads timeline.json from the renderer."""
import os, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *
OUT = os.path.dirname(os.path.abspath(__file__)); T = load(OUT); m = Mix(T["total"])
m.add(pad(T["title"][1] + 0.5), 0)                                              # title pad
m.add(hum(T["end"] - T["title"][1] + 1, f0=55, amp=0.03,
          level_pts=[(0, 0), (1.5, 1), (T["end"] - T["title"][1] - 0.5, 1), (T["end"] - T["title"][1] + 1, 0)]),
      T["title"][1])                                                             # soft bed
for i, t in enumerate(T["inputs"]): m.add(tick(1320 + 110 * i, 0.05), t, pan=-0.4)   # PDG inputs appear
m.add(whoosh(1.0, 300, 2500, 0.08, m.rng), T["fit_arrow"] - 0.2)                 # "fit ->"
for i, t in enumerate(T["outputs"]): m.add(tick(1760 + 110 * i, 0.05), t, pan=0.4)    # fitted params appear
b0, b1 = T["baseline"]; m.add(whoosh(b1 - b0 + 0.4, 150, 1800, 0.10, m.rng), b0)    # baselines rise
s0, s1 = T["spin"]; m.add(rising_tone(s1 - s0 + 0.8, 262, 0.5, 0.05), s0)        # spin shifts
m.add(chime(880, 2.5, 0.12), T["pdg"])                                           # PDG markers land
m.add(tick(990, 0.04), T["split"])
for i, (t, sg) in enumerate(zip(T["diff_bars"], T["diff_signs"])):
    m.add(thump(62 + (8 if sg > 0 else -6) + 2 * i, 0.26, m.rng), t, pan=(i - 2.5) * 0.15)
m.add(chime(660, 3.5, 0.09), T["end"] + 0.2)
m.write(os.path.join(OUT, "baryon_calculator_sfx.wav"))
print("wrote sfx")
