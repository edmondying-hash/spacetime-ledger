#!/usr/bin/env python3
"""Original synthesized sound design for uds_mass.mp4 (numpy only, no samples).
Reads timeline.json written by render_uds_mass.py and writes uds_mass_sfx.wav
(48 kHz, 16-bit stereo). Final loudness (-16 LUFS) is set by ffmpeg loudnorm."""
import json, wave, os
import numpy as np

OUT = "/workspace/bcc_test4_videos/v2_sound/uds_mass"
SR = 48000
ev = json.load(open(os.path.join(OUT, "timeline.json")))
N = int(ev["total"] * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(2026)

def tt(dur):
    return np.arange(int(dur * SR)) / SR

def add(sig, t0, pan=0.0):
    i = int(t0 * SR); j = min(N, i + len(sig)); sig = sig[:j - i]
    gl, gr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:j] += sig * gl * 1.414; R[i:j] += sig * gr * 1.414

def env_adsr(n, a, r):
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e

def lowpass(x, fc):
    """one-pole lowpass; fc may be an array (time-varying)"""
    fc = np.broadcast_to(fc, x.shape)
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y

def ease(x):
    x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

# 1) title: soft pad swell (A2, E3, A3)
t = tt(ev["title"][1] + 0.5)
pad = sum(a * np.sin(2 * np.pi * f * t) for f, a in ((110, 1.0), (164.81, 0.6), (220, 0.4)))
add(0.05 * pad * np.sin(np.pi * np.clip(t / (len(t) / SR), 0, 1)) ** 2, 0.0)

# 2) bare-state hum: act 1 full, act 2 at ~35 %, gone early in act 3
a1, a2 = ev["act1"]; a3 = ev["act3"][0]
t = tt(a3 + 1.5 - a1)
hum = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 110 * t + 0.3) + 0.15 * np.sin(2 * np.pi * 165 * t))
hum *= 1 + 0.25 * np.sin(2 * np.pi * 0.33 * t)
lvl = np.interp(t + a1, [a1, a1 + 1.2, a2, a2 + 2.0, a3, a3 + 1.5], [0, 1, 1, 0.35, 0.35, 0])
add(0.05 * hum * lvl, a1)

# 3) hop clicks (u left, d right, s centre and lower)
for th, q in ev["hops"]:
    n = int(0.03 * SR); tc = np.arange(n) / SR
    noise = np.diff(rng.standard_normal(n + 1))  # crude highpass
    f = {"u": 2400, "d": 2100, "s": 1300}[q]
    click = (0.5 * noise + np.sin(2 * np.pi * f * tc)) * np.exp(-tc / 0.006)
    add(0.07 * click, th, pan={"u": -0.45, "d": 0.45, "s": 0.0}[q])

# 4) whoosh as the links switch on (noise with rising cutoff)
l0, l1 = ev["links_on"]; d = (l1 - l0) + 0.8; t = tt(d)
fc = 200 + 3800 * ease(t / d) ** 1.5
wh = lowpass(rng.standard_normal(len(t)), fc) * np.sin(np.pi * t / d) ** 2
add(0.5 * wh / np.abs(wh).max() * 0.25, l0)

# 5) rising tone following the mass climb (one octave, 196 -> 392 Hz)
c0, c1 = ev["climb"]; t = tt(c1 - c0 + 1.2); tl = t + c0
m = ease((tl - c0) / (c1 - c0))
freq = 196 * 2 ** m
ph = 2 * np.pi * np.cumsum(freq) / SR
tone = np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph)
lv = np.interp(t, [0, 1.0, c1 - c0, c1 - c0 + 1.2], [0, 1, 1, 0]) * (0.6 + 0.4 * m)
add(0.06 * tone * lv, c0)

# 6) chime when it lands on the final mass
def chime(f0, dur, amp):
    t = tt(dur)
    s = sum(a * np.sin(2 * np.pi * f0 * k * t) * np.exp(-t / (dur * dk))
            for k, a, dk in ((1, 1.0, 0.45), (2.76, 0.45, 0.25), (5.40, 0.2, 0.12), (1.5, 0.3, 0.35)))
    return amp * s * env_adsr(len(t), 0.004, 0.05)
add(chime(880, 3.0, 0.16), ev["land"])

# 7) soft hits as the comparison bars grow
for i, tb in enumerate(ev["bars"]):
    t = tt(0.5); f = (70 + 8 * i) * np.exp(-t / 0.25)
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)
    tick = np.diff(rng.standard_normal(len(t) + 1)) * np.exp(-t / 0.004)
    add(0.32 * thump + 0.04 * tick, tb, pan=(i - 1) * 0.4)

# 8) PDG markers: two soft ticks; end card: low gentle chime
for k in range(2):
    add(chime(1760, 0.5, 0.04), ev["pdg_marks"] + 0.12 * k)
add(chime(660, 3.5, 0.09), ev["end"][0] + 0.2)

# master: fade tail, normalise peak to -3 dBFS
fade = np.ones(N); nf = int(1.0 * SR); fade[-nf:] = np.linspace(1, 0, nf)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max()); g = 10 ** (-3 / 20) / peak
st = np.stack([L * g, R * g], axis=1)
with wave.open(os.path.join(OUT, "uds_mass_sfx.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype("<i2").tobytes())
print("wrote uds_mass_sfx.wav", N / SR, "s")
