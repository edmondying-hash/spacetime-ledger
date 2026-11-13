"""Small numpy synth kit for the bcc_test4 v2_sound videos (all sounds original, no samples)."""
import json, os, wave
import numpy as np

SR = 48000


class Mix:
    def __init__(self, total, seed=2026):
        self.N = int(total * SR); self.L = np.zeros(self.N); self.R = np.zeros(self.N)
        self.rng = np.random.default_rng(seed)

    def add(self, sig, t0, pan=0.0, gain=1.0):
        i = int(t0 * SR)
        if i >= self.N or len(sig) == 0: return
        j = min(self.N, i + len(sig)); s = sig[:j - i] * gain
        gl, gr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        self.L[i:j] += s * gl * 1.414; self.R[i:j] += s * gr * 1.414

    def write(self, path, fade_out=1.0):
        n = int(fade_out * SR)
        f = np.ones(self.N); f[-n:] = np.linspace(1, 0, n)
        L, R = self.L * f, self.R * f
        g = 10 ** (-3 / 20) / max(np.abs(L).max(), np.abs(R).max(), 1e-9)
        st = np.stack([L * g, R * g], axis=1)
        with wave.open(path, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())


def tt(d):
    return np.arange(int(d * SR)) / SR


def ease(x):
    x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)


def lowpass(x, fc):
    fc = np.broadcast_to(np.asarray(fc, dtype=float), x.shape)
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y


def edge(n, a=0.01, r=0.05):
    e = np.ones(n); na, nr = min(n, int(a * SR)), min(n, int(r * SR))
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e


def pad(dur, freqs=(110, 164.81, 220), amp=0.05):
    t = tt(dur)
    s = sum(a * np.sin(2 * np.pi * f * t + k) for k, (f, a) in enumerate(zip(freqs, (1.0, 0.6, 0.4, 0.3))))
    return amp * s * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2


def hum(dur, f0=55.0, amp=0.05, lfo=0.33, level_pts=None):
    t = tt(dur)
    s = np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(4 * np.pi * f0 * t + 0.3) + 0.15 * np.sin(6 * np.pi * f0 * t)
    s *= 1 + 0.25 * np.sin(2 * np.pi * lfo * t)
    lv = np.interp(t, *zip(*level_pts)) if level_pts else edge(len(t), 1.0, 1.0)
    return amp * s * lv


def click(freq=2200, amp=0.07, rng=None):
    rng = rng or np.random.default_rng(0)
    n = int(0.03 * SR); t = np.arange(n) / SR
    noise = np.diff(rng.standard_normal(n + 1))
    return amp * (0.5 * noise + np.sin(2 * np.pi * freq * t)) * np.exp(-t / 0.006)


def whoosh(dur, f_lo=200, f_hi=4000, amp=0.12, rng=None, falling=False):
    rng = rng or np.random.default_rng(1); t = tt(dur)
    r = ease(t / dur) ** 1.5
    fc = f_lo + (f_hi - f_lo) * ((1 - r) if falling else r)
    w = lowpass(rng.standard_normal(len(t)), fc) * np.sin(np.pi * t / dur) ** 2
    return amp * w / (np.abs(w).max() + 1e-9)


def rising_tone(dur, f0=196, octaves=1.0, amp=0.06, curve=None):
    """curve: array 0..1 of length samples (progress); default eased ramp."""
    t = tt(dur)
    m = ease(t / max(dur - 0.8, 1e-3)) if curve is None else curve
    freq = f0 * 2 ** (octaves * m)
    ph = 2 * np.pi * np.cumsum(freq) / SR
    s = np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph)
    return amp * s * edge(len(t), 0.8, 0.8) * (0.6 + 0.4 * m)


def chime(f0=880, dur=3.0, amp=0.15):
    t = tt(dur)
    s = sum(a * np.sin(2 * np.pi * f0 * k * t) * np.exp(-t / (dur * dk))
            for k, a, dk in ((1, 1.0, 0.45), (2.76, 0.45, 0.25), (5.40, 0.2, 0.12), (1.5, 0.3, 0.35)))
    return amp * s * edge(len(t), 0.004, 0.05)


def thump(f=70, amp=0.3, rng=None):
    rng = rng or np.random.default_rng(3); t = tt(0.5); fr = f * np.exp(-t / 0.25)
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.12)
    tick = np.diff(rng.standard_normal(len(t) + 1)) * np.exp(-t / 0.004)
    return amp * s + 0.12 * amp * tick


def tick(freq=1760, amp=0.04):
    return chime(freq, 0.4, amp)


def load(out_dir):
    return json.load(open(os.path.join(out_dir, "timeline.json")))
