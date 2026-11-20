"""Synthesized SFX for relativistic_mercury.mp4 (all original numpy synthesis, no samples)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from sfxlib import *

tl = load(HERE); total = tl["total"]; s0 = tl["sweep_start"]
keys = np.array(tl["sweep_keys"]); th = tl["thresholds"]
m = Mix(total)
# title
m.add(pad(3.2, (110, 164.81, 220), 0.05), 0.0)
m.add(chime(880, 2.0, 0.06), 0.95)
# sweep: hum under everything, pitch follows position on the (not-to-scale) phase strip
dur = keys[-1, 0]; t = tt(dur)
T = np.interp(t, keys[:, 0], keys[:, 1])
segs = [(0, th["sc"]), (th["sc"], th["melt"]), (th["melt"], th["boil"]), (th["boil"], th["max"])]
prog = np.zeros_like(T)
for i, (a, b) in enumerate(segs):
    msk = (T >= a) & (T <= b)
    prog[msk] = (i + (T[msk] - a) / (b - a)) / 4
m.add(rising_tone(dur, 98, 1.5, 0.05, curve=prog), s0)
m.add(hum(dur, 55, 0.035), s0)
# superconducting shimmer until 4.15 K
sc_end = keys[2, 0]
sh = pad(sc_end + 1.0, (1318.5, 1975.5, 2637.0), 0.012)
m.add(sh, s0 - 0.3, pan=0.2)
# phase-change chimes (moments where the program's state string flips)
for tk, f, pan in ((keys[2, 0], 1318.5, -0.3), (keys[4, 0], 880, 0.0), (keys[6, 0], 659.3, 0.3)):
    m.add(chime(f, 2.2, 0.09), s0 + tk, pan=pan)
m.add(thump(60, 0.12), s0 + keys[4, 0])
m.add(whoosh(2.4, 300, 5000, 0.07), s0 + keys[6, 0] - 0.2)
# end card
e0 = tl["scenes"][2]["start"]
m.add(pad(5.0, (98, 146.83, 196), 0.045), e0)
m.add(chime(660, 2.5, 0.05), e0 + 0.4)
m.write(os.path.join(HERE, "relativistic_mercury_sfx.wav"))
print("sfx ok")
