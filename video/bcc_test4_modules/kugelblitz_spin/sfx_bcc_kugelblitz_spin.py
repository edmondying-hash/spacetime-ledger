#!/usr/bin/env python3
"""Synthesized SFX for the v6 bcc_kugelblitz_spin.mp4 (numpy only). Reads timeline.json."""
import os, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *
OUT = os.path.dirname(os.path.abspath(__file__)); T = load(OUT); m = Mix(T["total"])

m.add(pad(T["title"][1] + 0.6, (73.42, 110.00, 146.83)), 0)
m.add(whoosh(1.5, 180, 2200, 0.07, m.rng), 0.35)
bed0, bed1 = T["title"][1], T["end"]
m.add(hum(bed1 - bed0 + 1.0, 38.9, 0.026,
          level_pts=[(0, 0), (1.2, 1), (bed1 - bed0 - 0.4, 0.85), (bed1 - bed0 + 1.0, 0)]), bed0)

# part 1: whoosh per ring, tick on landing, meter tone
for k, (t0, ta) in enumerate(zip(T["p_starts"], T["p_arrive"])):
    m.add(whoosh(1.0, 240, 2800 + 180 * k, 0.065, m.rng), t0 + 0.12, pan=-0.15 + 0.08 * (k % 3))
    m.add(tick(1320 + 80 * k, 0.036), ta)
    m.add(rising_tone(0.6, f0=196 + 40 * k, octaves=0.6, amp=0.035), ta - 0.12)
m.add(thump(52, 0.24, m.rng), T["deadlock"], pan=0.15)
dlen = T["w216"] - T["deadlock"]
m.add(hum(dlen + 0.6, 29.0, 0.030, level_pts=[(0, 0), (0.35, 1), (dlen, 0.75), (dlen + 0.6, 0.55)]),
      T["deadlock"], pan=0.2)
m.add(tick(420, 0.04), T["w216"]); m.add(thump(44, 0.18, m.rng), T["w216"], pan=0.1)

# part 2
for k, (t0, ta) in enumerate(zip(T["s_starts"], T["s_arrive"])):
    m.add(whoosh(0.9, 200, 2000, 0.055, m.rng), t0 + 0.10, pan=-0.25 + 0.2 * k)
    m.add(tick(1080, 0.030), ta)
m.add(pad(T["bias_ccw"] - T["bias0"], (98.00, 146.83), 0.022), T["bias0"])

def pair(t0, t1, omega, core_pan):
    """Core swirl (low, panned one way) + star recoil shimmer (higher, panned the other way)."""
    dur = t1 - t0
    lv = [(0, 0), (0.5, 1), (dur, 0.85), (dur + 0.3, 0)]
    m.add(hum(dur + 0.3, 46.0 + 80 * abs(omega) / 0.012, 0.018 + 0.022 * abs(omega) / 0.012,
              lfo=max(0.15, abs(omega) * 200 / 6.2832), level_pts=lv), t0, pan=0.5 * core_pan)
    m.add(hum(dur + 0.3, 220.0, 0.010 + 0.008 * abs(omega) / 0.012, lfo=0.6, level_pts=lv),
          t0 + 0.2, pan=-0.5 * core_pan)

pair(T["s_orbit"][1], T["bias_cw"], 0.012, +1)
pair(T["s_orbit"][2], T["end"], -0.0048, -1)
m.add(chime(988, 2.0, 0.09), T["s_orbit"][1]); m.add(chime(740, 2.0, 0.07), T["s_orbit"][1] + 0.35)
m.add(chime(659, 2.0, 0.08), T["s_orbit"][2]); m.add(chime(880, 2.0, 0.06), T["s_orbit"][2] + 0.35)
m.add(chime(587, 3.4, 0.10), T["end"] + 0.15)
m.write(os.path.join(OUT, "bcc_kugelblitz_spin_sfx.wav")); print("wrote sfx")
