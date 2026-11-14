#!/usr/bin/env python3
"""Synthesized SFX for bcc_virtual_carriers.mp4 (numpy only). Reads timeline.json from the renderer."""
import os, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *
OUT = os.path.dirname(os.path.abspath(__file__)); T = load(OUT); m = Mix(T["total"])
m.add(pad(T["title"][1] + 0.5, (82.41, 123.47, 164.81)), 0)
m.add(whoosh(1.3, 220, 2400, 0.07, m.rng), 0.3)
e = T["end"] - T["title"][1]
m.add(hum(e + 1, 41.2, 0.030, level_pts=[(0, 0), (1.5, 1), (e - 0.5, 1), (e + 1, 0)]), T["title"][1])
# soft conserved-flux pad under the photon (left)
c0, c1 = T["carriers"]
m.add(pad(c1 - c0, (196.00, 246.94, 329.63), 0.028), c0, pan=-0.65)
# W decay: a mid pad that is visibly quieter after hop 4
m.add(hum(T["hop4"] - c0 + 0.4, 55.0, 0.028,
          level_pts=[(0, 0), (0.6, 1), (T["hop4"] - c0 - 0.2, 0.45), (T["hop4"] - c0 + 0.4, 0.15)]),
      c0, pan=0.0)
m.add(hum(c1 - T["hop4"] + 0.2, 49.0, 0.012,
          level_pts=[(0, 0.15), (1.0, 0.12), (c1 - T["hop4"], 0.04), (c1 - T["hop4"] + 0.2, 0)]),
      T["hop4"], pan=0.0)
# one metronome tick per hop; photon ding stays bright; W ding fades; gluon climbs
# official survival at hops 1..8 (for W ding gain only)
surv = [0.513417, 0.263597, 0.135335, 0.069483, 0.035674, 0.018316, 0.009404, 0.004828]
for k, t in enumerate(T["hops"]):
    r = k + 1
    m.add(tick(1240, 0.038), t)  # shared hop clock
    m.add(tick(1760, 0.030), t, pan=-0.7)  # photon
    m.add(tick(880, 0.028 * max(0.12, surv[k])), t, pan=0.0)  # W, fading
    if r < 7:
        m.add(tick(520 + 90 * r, 0.040), t, pan=0.7)  # gluon climbing
    if r <= 6:
        m.add(whoosh(0.45, 280, 1600 + 80 * r, 0.045, m.rng), t, pan=-0.15)
# gluon snap at hop 7, then a small chime for the new pair
m.add(thump(58, 0.28, m.rng), T["snap"], pan=0.7)
m.add(chime(988, 2.2, 0.13), T["snap"] + 0.04, pan=0.55)
m.add(chime(784, 2.0, 0.08), T["w_fade_ann"])
m.add(tick(660, 0.04), T["hop8"], pan=0.0)
m.add(chime(587, 3.4, 0.10), T["end"] + 0.15)
m.write(os.path.join(OUT, "bcc_virtual_carriers_sfx.wav")); print("wrote sfx")
