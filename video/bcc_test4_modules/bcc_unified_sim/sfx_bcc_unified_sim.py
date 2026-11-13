#!/usr/bin/env python3
"""Synthesized SFX for bcc_unified_sim.mp4 (v4, 6-face; numpy only). Reads timeline.json."""
import os, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *
OUT = os.path.dirname(os.path.abspath(__file__)); T = load(OUT); m = Mix(T["total"])
m.add(pad(T["title"][1] + 0.5, (110, 164.81, 220)), 0)
g0 = T["title"][1]; e = T["end"] - g0
m.add(hum(e + 1, 55, 0.03, level_pts=[(0, 0), (1.5, 1), (e - 0.5, 1), (e + 1, 0)]), g0)
for t, links in T["hops"]: m.add(click(1400 + 90 * links, 0.05, m.rng), t, pan=float(m.rng.uniform(-0.5, 0.5)))
m.add(whoosh(1.8, 200, 2200, 0.09, m.rng), T["fam_bars"])
m.add(tick(990, 0.04), T["formula1"])
for i, val in enumerate(T["gb_vals"]): m.add(thump(48 + 0.008 * val, 0.27, m.rng), T["gb_rise"] + 0.5 + 0.45 * i, pan=-0.3 + 0.3 * i)
m.add(chime(880, 2.0, 0.08), T["gb_formula"])
l0, l1 = T["lens"]
for k in range(24): m.add(click(2000, 0.03, m.rng), l0 + (l1 - l0) * (k + 1) / 24, pan=-0.6 + 1.2 * k / 24)
m.add(chime(880, 2.5, 0.11), T["lens_lag"] + 0.1)
for t in T["packets"]: m.add(click(2600, 0.022, m.rng), t, pan=float(m.rng.uniform(-0.6, 0.6)))
for i, t in enumerate(T["grow"]): m.add(thump(55 + 3 * i, 0.22, m.rng), t)
m.add(chime(1046.5, 2.2, 0.10), T["cap"] + 0.1)
m.add(chime(660, 3.5, 0.09), T["end"] + 0.2)
m.write(os.path.join(OUT, "bcc_unified_sim_sfx.wav")); print("wrote sfx")
