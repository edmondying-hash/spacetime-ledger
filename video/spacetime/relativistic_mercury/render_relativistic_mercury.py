"""Mercury 0 K -> 800 K phase sweep video for spacetime/elements/bcc_relativistic_mercury.py.

Every on-screen number (T, deg C, kT, state string, Hg 1s v/c / gamma / contraction,
phase thresholds) comes from calls into the unmodified program copy in ./src.
The atom picture is display-only: a small Langevin toy whose regime (lattice /
pool / free flight) is switched by the state string the program returns.
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
sys.path.insert(0, os.path.join(HERE, "src"))
import bccvid as bv
from bccvid import FG, DIM, CYAN, ORANGE, RED, GREEN, VIOLET, YELLOW, GRID, PANEL, ramp
from bcc_relativistic_mercury import BCCRelativisticMercurySim

sim = BCCRelativisticMercurySim()
hg = [r for r in sim.relativistic_core_comparison() if r["Z"] == 80][0]
hgv = [r for r in sim.gold_vs_mercury_valence() if "Mercury" in r["element"]][0]
T_SC = 4.15                     # threshold literal in mercury_thermal_phase_sweep (checked below)
T_MELT, T_BOIL = hgv["melt_k"], hgv["boil_k"]   # 234.32, 629.88 from the program's data
T_MAX = 800.0

def phase_of(T):
    return sim.mercury_thermal_phase_sweep([T])[0]

# sanity: the state the program returns flips exactly at these thresholds
def _kind(s):
    return ("sc" if "Superconductor" in s else "solid" if "Solid" in s else
            "liquid" if "LIQUID" in s else "vapor")
assert _kind(phase_of(T_SC - 1e-6)["state"]) == "sc" and _kind(phase_of(T_SC)["state"]) == "solid"
assert _kind(phase_of(T_MELT - 1e-6)["state"]) == "solid" and _kind(phase_of(T_MELT)["state"]) == "liquid"
assert _kind(phase_of(T_BOIL - 1e-6)["state"]) == "liquid" and _kind(phase_of(T_BOIL)["state"]) == "vapor"

# ---------------- temperature schedule for the sweep scene (display pacing) ----------------
KEYS = [(0.0, 0.0), (1.0, 0.0), (4.5, T_SC), (5.3, T_SC), (13.3, T_MELT), (14.3, T_MELT),
        (24.3, T_BOIL), (25.3, T_BOIL), (30.5, T_MAX), (31.5, T_MAX)]
SWEEP = KEYS[-1][0]
def T_at(t):
    for (t0, T0), (t1, T1) in zip(KEYS, KEYS[1:]):
        if t <= t1:
            return T0 + (T1 - T0) * (t - t0) / (t1 - t0) if t1 > t0 else T1
    return KEYS[-1][1]

SEGS = [(0.0, T_SC), (T_SC, T_MELT), (T_MELT, T_BOIL), (T_BOIL, T_MAX)]
def strip_x(T):
    for i, (a, b) in enumerate(SEGS):
        if T <= b or i == 3:
            return (i + min(1.0, (T - a) / (b - a))) / 4
    return 1.0

# ---------------- display-only atom toy (precomputed) ----------------
BW, BH = 10.0, 7.0
a = 0.62
sites = []
for j in range(6):
    for i in range(11):
        sites.append((1.6 + i * a + j * a * 0.38, 0.35 + j * a * 0.88))
sites = np.array(sites); N = len(sites)
rng = np.random.default_rng(80)
nf = int(round(SWEEP * bv.FPS)); SUB = 10; dt = 1.0 / bv.FPS / SUB
P = np.zeros((nf, N, 2)); KIND = []
p = sites.copy(); v = np.zeros_like(p)
C_T = 0.0055   # display scale: toy "temperature" per kelvin
for f in range(nf):
    T = T_at(f / bv.FPS); k = _kind(phase_of(T)["state"]); KIND.append(k)
    teff = C_T * T
    if k in ("sc", "solid"):
        ks, g, att, gam = 200.0, 0.0, 0.0, 6.0
    elif k == "liquid":
        ks, g, att, gam = 0.0, 6.0, 14.0, 3.0; teff *= 0.35
    else:
        ks, g, att, gam = 0.0, 0.0, 0.0, 0.4; teff *= 6
    for _ in range(SUB):
        F = -ks * (p - sites)
        if ks == 0.0:
            d = p[:, None, :] - p[None, :, :]; r = np.sqrt((d ** 2).sum(-1)) + np.eye(N)
            rep = np.where(r < a, 900.0 * (a - r), 0.0)
            at = np.where((r >= a) & (r < 1.7 * a), -att * np.sin(math.pi * (r - a) / (0.7 * a)), 0.0)
            mag = (rep + at) * (1 - np.eye(N))
            F = F + (mag[..., None] * d / r[..., None]).sum(1)
            F[:, 1] -= g
        v += (F - gam * v) * dt + np.sqrt(2 * gam * teff * dt) * rng.standard_normal(p.shape)
        p += v * dt
        for ax_, hi in ((0, BW), (1, BH)):
            lo_m = p[:, ax_] < 0.15; hi_m = p[:, ax_] > hi - 0.15
            p[lo_m, ax_] = 0.15; v[lo_m, ax_] = np.abs(v[lo_m, ax_])
            p[hi_m, ax_] = hi - 0.15; v[hi_m, ax_] = -np.abs(v[hi_m, ax_])
    P[f] = p

# ---------------- scenes ----------------
def sweep(fig, t, T_scene):
    f = min(nf - 1, int(round(t * bv.FPS)))
    T = T_at(t); row = phase_of(T); kind = KIND[f]
    # left: atom box
    ax = fig.add_axes([0.035, 0.12, 0.50, 0.78]); bv.style_ax(ax, grid=False)
    ax.set_xlim(0, BW); ax.set_ylim(0, BH); ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    xy = P[f]
    sc_a = 1.0
    if kind in ("sc", "solid"):
        d = np.linalg.norm(sites[:, None] - sites[None], axis=-1)
        ii, jj = np.where((d > 0) & (d < a * 1.05))
        col = CYAN if kind == "sc" else "#6b768c"
        for i, j in zip(ii, jj):
            if i < j:
                ax.plot([xy[i, 0], xy[j, 0]], [xy[i, 1], xy[j, 1]], color=col, lw=1.0,
                        alpha=0.55 if kind == "sc" else 0.5, zorder=1)
    if kind == "sc":
        # display-only: paired carriers drifting through the lattice with zero resistance
        for m in range(5):
            yy = 0.35 + (m + 0.5) * a * 0.88
            xs = 1.6 + (m + 0.5) * a * 0.38 + a * 0.5
            span = 9 * a
            x0 = xs + (t * 0.9 + m * 0.37 * span) % span
            ax.scatter([x0, x0 + 0.17], [yy, yy], s=26, color=CYAN, alpha=0.95 * sc_a, zorder=4)
        ax.scatter(xy[:, 0], xy[:, 1], s=700, color=CYAN, alpha=0.06, zorder=2)
    alpha = 0.55 if kind == "vapor" else 1.0
    ax.scatter(xy[:, 0], xy[:, 1], s=260, color="#c7ced9", edgecolor="#eef2f8", lw=0.8, alpha=alpha, zorder=3)
    ax.scatter(xy[:, 0] - 0.05, xy[:, 1] + 0.05, s=40, color="white", alpha=0.5 * alpha, zorder=3)
    ax.text(0.15, BH - 0.25, "Hg atoms (illustration only)", fontsize=14, color=DIM, va="top")

    # right: readouts (all from mercury_thermal_phase_sweep)
    x0 = 0.585
    fig.text(x0, 0.83, f"{row['temp_k']:.2f} K", fontsize=74, weight="bold", color=FG, va="center")
    fig.text(x0, 0.735, f"{row['temp_c']:.2f} °C     kT = {row['kbt_ev']:.5f} eV", fontsize=24, color=DIM, va="center")
    st = row["state"]; head, _, tail = st.partition(" (")
    colk = {"sc": CYAN, "solid": "#c7ced9", "liquid": ORANGE, "vapor": VIOLET}[kind]
    fig.text(x0, 0.62, head, fontsize=34, color=colk, weight="bold", va="center")
    if tail:
        fig.text(x0, 0.565, "(" + tail, fontsize=21, color=DIM, va="center")
    # phase strip
    sx = fig.add_axes([x0, 0.36, 0.38, 0.05]); sx.set_xlim(0, 1); sx.set_ylim(0, 1); sx.axis("off")
    cols = [CYAN, "#8f99ab", ORANGE, VIOLET]; names = ["superconductor", "solid", "liquid", "vapor"]
    for i in range(4):
        on = i == ["sc", "solid", "liquid", "vapor"].index(kind)
        sx.add_patch(__import__("matplotlib").patches.Rectangle((i / 4 + 0.004, 0), 0.25 - 0.008, 1,
                     color=cols[i], alpha=0.85 if on else 0.22))
        fig.text(x0 + 0.38 * (i + 0.5) / 4, 0.43, names[i], fontsize=15, ha="center",
                 color=cols[i] if on else DIM)
    for Tb in (0.0, T_SC, T_MELT, T_BOIL, T_MAX):
        lab = f"{Tb:g}"
        fig.text(x0 + 0.38 * strip_x(Tb), 0.335, lab, fontsize=13, ha="center", va="top", color=DIM)
    fig.text(x0 + 0.38, 0.295, "K  (segments not to scale)", fontsize=12, ha="right", va="top", color=DIM)
    mx = strip_x(T)
    sx.plot([mx, mx], [-0.35, 1.35], color=FG, lw=3, clip_on=False)
    # constant relativistic line from relativistic_core_comparison()
    fig.text(x0, 0.20, f"Hg 1s (Z·α):  v/c {hg['beta_1s']:.4f}   γ {hg['gamma_1s']:.4f}   "
             f"contraction {hg['contraction_pct']:.2f}%", fontsize=17, color=DIM, va="center")
    fig.text(x0, 0.165, "computed by the program · same at every temperature", fontsize=13, color=DIM, va="center")

FOOT = "spacetime/elements/bcc_relativistic_mercury.py  ·  toy model  ·  phase thresholds are measured Hg values written into the code"
video = bv.Video(HERE, "relativistic_mercury_silent", "bcc_relativistic_mercury.py", FOOT)
video.add(3.0, bv.title_card("Mercury, 0 K and up", "phase state from bcc_relativistic_mercury.py"), heading="")
video.add(SWEEP, sweep, heading="TOY MODEL")
video.add(5.0, bv.end_card([
    (f"0 – {T_SC} K   superconductor", CYAN),
    (f"{T_SC} – {T_MELT} K   solid", "#c7ced9"),
    (f"{T_MELT} – {T_BOIL} K   liquid", ORANGE),
    (f"above {T_BOIL} K   vapor", VIOLET),
    ("thresholds are inputs, not outputs · only °C and kT are computed from T", DIM),
], head="What the program returns"), heading="TOY MODEL")

if __name__ == "__main__":
    st = bv.scene_starts(video)
    tl = {"scenes": st, "sweep_start": st[1]["start"], "sweep_keys": KEYS,
          "thresholds": {"sc": T_SC, "melt": T_MELT, "boil": T_BOIL, "max": T_MAX},
          "total": video.duration}
    if "--frames" in sys.argv:
        import matplotlib.pyplot as plt
        for ts in [0.5, 3.5, 6.0, 10.0, 16.0, 22.0, 27.0, 33.0, 36.5]:
            fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
            acc = 0
            for dur, fn, caps, hd in video.scenes:
                if ts < acc + dur:
                    fn(fig, ts - acc, dur); video.chrome(fig, ts - acc, dur, caps, hd); break
                acc += dur
            fig.savefig(os.path.join(HERE, f"_preview_{ts:05.1f}.png")); plt.close(fig)
    else:
        bv.finish(video, "relativistic_mercury", tl, os.path.join(HERE, "sfx_relativistic_mercury.py"), thumb_t=3.0 + 18.0)
