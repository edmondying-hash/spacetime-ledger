#!/usr/bin/env python3
"""Synthesized SFX for bcc_meson_sim.mp4 (numpy only). Reads timeline.json from the renderer."""
import os, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *
OUT = os.path.dirname(os.path.abspath(__file__)); T = load(OUT); m = Mix(T["total"])
m.add(pad(T["title"][1] + 0.5, (98, 146.83, 196)), 0)
e = T["end"] - T["title"][1]
m.add(hum(e + 1, 49, 0.03, level_pts=[(0, 0), (1.5, 1), (e - 0.5, 1), (e + 1, 0)]), T["title"][1])
r0, r1 = T["spec_rise"]; m.add(whoosh(r1 - r0 + 0.4, 150, 2200, 0.10, m.rng), r0)
for k in range(8): m.add(tick(1500 + 60 * k, 0.03), T["pdg"] + 0.08 * k, pan=-0.6 + 0.17 * k)   # PDG diamonds
m.add(chime(880, 2.0, 0.07), T["diffs"])
m.add(thump(52, 0.25, m.rng), T["bad"]); m.add(thump(48, 0.22, m.rng), T["bad"] + 0.35)       # D, D* misses
for t, sp in T["hyper"]:                                                                    # spin down / up
    m.add(thump(50 if sp < 0 else 85, 0.22, m.rng), t, pan=-0.3 if sp < 0 else 0.3)
for i, (t, en) in enumerate(zip(T["hops"], T["energies"])):                                 # tube stretches
    m.add(click(1400 + 4 * en, 0.07, m.rng), t, pan=-0.5 + 0.15 * i)
m.add(rising_tone(T["snap"] - T["hops"][0] + 0.4, 147, 1.0, 0.045), T["hops"][0] - 0.8)       # tension builds
m.add(thump(90, 0.3, m.rng), T["snap"]); m.add(chime(1046.5, 2.8, 0.14), T["snap"] + 0.05)     # SNAP
m.add(chime(660, 3.5, 0.09), T["end"] + 0.2)
m.write(os.path.join(OUT, "bcc_meson_sim_sfx.wav")); print("wrote sfx")
