#!/usr/bin/env python3
"""v2_sound: YouTube version of Edmond's animate_uds_mass.py on the v4 (6-face) suite (his script is not modified).

Numbers: the unrounded Lambda / N / Omega tick values come from running
the v4 bcc_unified_sim.py unchanged (grid_values.py -> grid_values.json). The only
MeV conversion is ONE scale calibrated so the grid Lambda total equals PDG
Lambda0 (1115.683 MeV, the value baryon_calculator.py uses). The v4 code sets no
MeV scale for baryons (its glueball printout labels ticks as MeV 1:1). Quark hop motion is illustrative (seeded random), like his.

Pipeline: render silent video -> sfx_uds_mass.py builds the wav from events.json
-> ffmpeg muxes AAC audio normalised to about -16 LUFS.
"""
import sys, json, math, subprocess, os
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from bccvid import *
import numpy as np
from matplotlib.patches import Patch

OUT = "/workspace/bcc_test4_videos/v2_sound/uds_mass"
G = json.load(open(os.path.join(OUT, "grid_values.json")))
LAM, NUC, OME = G['Lambda'], G['N'], G['Omega']
PDG_L = G['_pdg']['Lambda']; PDG_P = G['_pdg']['p']; PDG_O = G['_pdg']['Omega-']
BARE, ROUTE, SPIN, TOT = LAM['BareT'], LAM['RouteT'], LAM['SpinT'], LAM['GridMass']
SCALE = PDG_L / TOT                     # MeV per tick, calibrated to PDG Lambda0
# sanity vs printed bcc_unified_sim output
assert (round(BARE, 1), round(ROUTE, 1), round(SPIN, 1), round(TOT, 2)) == (103.0, 716.9, -5.1, 814.80)
assert (NUC['GridMass'], OME['GridMass'], NUC['BareT'], OME['BareT']) == (720.94, 1006.39, 12.0, 285.0)
for d in (NUC, LAM, OME):
    d['mass_MeV'], d['bare_ticks'], d['route_ticks'] = d['GridMass'], d['BareT'], d['RouteT']

# ---------------- timeline (seconds) ----------------
T_TITLE, T_A1, T_A2, T_A3, T_END = 4.0, 9.0, 17.0, 12.0, 6.0
A1 = T_TITLE; A2 = A1 + T_A1; A3 = A2 + T_A2; END = A3 + T_A3; TOTAL = END + T_END
LINK_ON = (0.3, 1.8)        # act-2 local: links fade in
CLIMB = (1.8, 12.0)         # act-2 local: mass climbs
HOP_DT = 0.6

def climb(tl):
    return ease((tl - CLIMB[0]) / (CLIMB[1] - CLIMB[0]))

# ---------------- illustrative quark hops (seeded, like his script) ----------------
rng = np.random.default_rng(7)
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
pos = {'u': (2, 5), 'd': (5, 5), 's': (3.5, 2)}
start = dict(pos)
HOPS = []   # (act2-local time, quark, from, to)
t = 1.0; k = 0
while t < T_A2 - 0.8:
    for q in ('u', 'd') + (('s',) if k % 2 == 0 else ()):
        x, y = pos[q]; dx, dy = DIRS[int(rng.integers(0, 4))]
        nx, ny = float(np.clip(x + dx, 1, 6)), float(np.clip(y + dy, 1, 6))
        if (nx, ny) != (x, y):
            HOPS.append((t + 0.07 * "uds".index(q), q, (x, y), (nx, ny))); pos[q] = (nx, ny)
    t += HOP_DT; k += 1

def qpos(q, tl):
    p = start[q]
    for th, qq, a, b in HOPS:
        if qq != q or th > tl: continue
        f = ease((tl - th) / 0.25)
        p = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
    return p

QCOL = {'u': CYAN, 'd': YELLOW, 's': RED}
QSIZE = {'u': 900, 'd': 900, 's': 1250}

def draw_grid(fig, tl, links, act1):
    ax = fig.add_axes([0.04, 0.17, 0.38, 0.68]); ax.set_facecolor(PANEL)
    for i in range(9):
        ax.plot([i - .5] * 2, [-.5, 7.5], color=GRID, lw=1); ax.plot([-.5, 7.5], [i - .5] * 2, color=GRID, lw=1)
    P = {q: (start[q] if act1 else qpos(q, tl)) for q in 'uds'}
    if act1:  # at rest: gentle breathing only
        br = 1 + 0.04 * math.sin(2 * math.pi * tl / 3.0)
    else:
        br = 1.0
    jx = sum(p[0] for p in P.values()) / 3; jy = sum(p[1] for p in P.values()) / 3
    if links > 0:
        for q, (x, y) in P.items():
            for lw, a in ((26, 0.05), (16, 0.10), (9, 0.22), (4, 0.9)):
                ax.plot([x, jx], [y, jy], color=VIOLET if q != 's' else "#ff7bd5", lw=lw, alpha=a * links,
                        solid_capstyle="round", zorder=2)
            for n in range(3):  # pulses travelling quark -> junction
                f = ((tl / 0.9) + n / 3.0) % 1.0
                px, py = x + (jx - x) * f, y + (jy - y) * f
                ax.scatter([px], [py], s=160, color="#f5d0fe", alpha=0.25 * links, zorder=3, lw=0)
                ax.scatter([px], [py], s=45, color="#ffffff", alpha=0.9 * links, zorder=3, lw=0)
        ax.scatter([jx], [jy], s=500, marker="D", color=VIOLET, alpha=0.25 * links, zorder=4, lw=0)
        ax.scatter([jx], [jy], s=140, marker="D", color="#e9d5ff", alpha=links, zorder=4, lw=0)
    for q, (x, y) in P.items():
        ax.scatter([x], [y], s=QSIZE[q] * 2.6 * br, color=QCOL[q], alpha=0.12, zorder=5, lw=0)
        ax.scatter([x], [y], s=QSIZE[q] * br, color=QCOL[q], edgecolor=FG, lw=1.8, zorder=6)
        ax.text(x, y, q, ha="center", va="center", fontsize=22, weight="bold", color=BG, zorder=7)
    ax.set_xlim(-.5, 7.5); ax.set_ylim(-.5, 7.5); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color(GRID)
    ax.set_title("8×8 slice of the grid", fontsize=18, color=DIM)
    ax.text(3.5, -0.25, "quark motion illustrative" if not act1 else "quarks at rest · links off",
            ha="center", va="bottom", fontsize=14, color=DIM, zorder=8)

def draw_meter(fig, m):
    ax = style_ax(fig.add_axes([0.50, 0.17, 0.12, 0.68]))
    r, s = ROUTE * m, SPIN * m
    ax.bar(0, BARE, width=0.6, color=RED, alpha=0.9)
    if r > 0:
        ax.bar(0, r + s, bottom=BARE, width=0.6, color=VIOLET, alpha=0.9)   # net top = total ticks
        ax.bar(0, -s, bottom=BARE + r + s, width=0.6, fill=False, edgecolor=GREEN, hatch="///", lw=1.5)  # spin pair removes this
    ax.set_xlim(-0.5, 0.5); ax.set_ylim(0, 900); ax.set_xticks([]); ax.set_ylabel("grid ticks per cycle", fontsize=16)
    ax.set_title("Λ⁰ (uds)", fontsize=20, color=FG)
    ax.legend(handles=[Patch(color=RED, label=f"bare  {BARE:.1f}"), Patch(color=VIOLET, label=f"gluon routing  +{ROUTE:.1f}"),
                       Patch(fill=False, edgecolor=GREEN, hatch="///", label=f"spin term  {SPIN:.1f}")],
              loc="upper left", bbox_to_anchor=(1.05, 1.0), frameon=False, fontsize=15)

def draw_readout(fig, m, landed_a):
    ticks = BARE + (ROUTE + SPIN) * m
    fig.text(0.81, 0.55, f"{ticks:.2f}", fontsize=78, weight="bold", ha="center", color=FG)
    fig.text(0.81, 0.50, "ticks per cycle", fontsize=20, ha="center", color=DIM)
    col = YELLOW if landed_a > 0 else CYAN
    fig.text(0.81, 0.36, f"≈ {ticks * SCALE:.1f} MeV", fontsize=50, weight="bold", ha="center", color=col)
    fig.text(0.81, 0.31, f"1 tick = {SCALE:.3f} MeV  (calibrated to PDG Λ⁰)", fontsize=16, ha="center", color=DIM)
    if landed_a > 0:
        fig.text(0.81, 0.22, f"= PDG Λ⁰ {PDG_L:.2f} MeV  (calibration point)", fontsize=18, ha="center", color=YELLOW, alpha=landed_a)

def act1(fig, t, T):
    draw_grid(fig, t, 0.0, True); draw_meter(fig, 0.0); draw_readout(fig, 0.0, 0)

def act2(fig, t, T):
    links = ramp(t, LINK_ON[0], LINK_ON[1] - LINK_ON[0])
    m = climb(t)
    draw_grid(fig, t, links, False); draw_meter(fig, m); draw_readout(fig, m, ramp(t, CLIMB[1], 0.4))

FAM = [("p (uud)", NUC, PDG_P), ("Λ⁰ (uds)", LAM, PDG_L), ("Ω⁻ (sss)", OME, PDG_O)]
BAR_T = [0.4, 1.4, 2.4]
def act3(fig, t, T):
    ax = style_ax(fig.add_axes([0.09, 0.18, 0.78, 0.64]))
    for i, (lab, d, pdg) in enumerate(FAM):
        g = ramp(t, BAR_T[i], 0.9)
        b = d['bare_ticks']; rest = d['mass_MeV'] - b
        ax.bar(i, b * g, width=0.5, color=RED, alpha=0.9)
        ax.bar(i, rest * g, bottom=b * g, width=0.5, color=VIOLET, alpha=0.9)
        if g > 0.95:
            ax.text(i, d['mass_MeV'] + (45 if d is LAM else 22), f"{d['mass_MeV']:.2f} ticks → {d['mass_MeV'] * SCALE:.1f} MeV",
                    ha="center", fontsize=18, color=FG)
            ax.text(i + 0.27, b + rest / 2 - 60, f"routing {d['route_ticks']:.1f}", fontsize=14, color=VIOLET, va="center")
        a = ramp(t, 6.5, 0.8)
        if a > 0:
            ax.plot([i - 0.32, i + 0.32], [pdg / SCALE] * 2, color=YELLOW, lw=3, alpha=a, ls="--")
            ax.text(i + 0.35, pdg / SCALE, f"PDG {pdg:.1f}", fontsize=15, color=YELLOW, alpha=a, ha="left", va="center")
    ax.set_xticks(range(3)); ax.set_xticklabels([f[0] for f in FAM], fontsize=24, color=FG)
    ax.set_xlim(-0.75, 2.75); ax.set_ylim(0, 1330); ax.set_ylabel("grid ticks per cycle", fontsize=16)
    sec = ax.secondary_yaxis("right", functions=(lambda x: x * SCALE, lambda y: y / SCALE))
    sec.set_ylabel("MeV (Λ⁰-calibrated scale)", fontsize=16); sec.tick_params(colors=DIM)
    ax.legend(handles=[Patch(color=RED, label="bare quarks"), Patch(color=VIOLET, label="gluon routing + spin"),
                       Patch(color=YELLOW, label="PDG mass (dashed)")], loc="upper left", frameon=False, fontsize=16)

v = Video(OUT, "_silent", "bcc_test4 · uds (Λ⁰) mass from grid ticks  (v4, 6-face)",
          "TOY MODEL · ticks from bcc_unified_sim.py (v4) · MeV scale calibrated to PDG Λ⁰ · quark motion illustrative")
v.add(T_TITLE, title_card("Bare quarks → baryon mass", "u, d, s at rest, then gluon flux links switch on"))
v.add(T_A1, act1, [(0.3, "Act 1 · Bare u, d, s at rest: 12 + 91 (one s) = 103 ticks, by formula"),
                   (4.5, f"On the Λ⁰ scale that is ≈ {BARE * SCALE:.0f} MeV")], "Act 1 · Bare quarks")
v.add(T_A2, act2, [(0.3, "Act 2 · Gluon flux links switch on"),
                   (3.0, f"Routing adds {ROUTE:.1f} ticks (95 × avg links); spin term {SPIN:.1f}"),
                   (7.5, f"In this toy model, links + spin are {100 * (ROUTE + SPIN) / TOT:.1f}% of the ticks"),
                   (CLIMB[1], f"{TOT:.2f} ticks → {PDG_L:.2f} MeV, by calibration")], "Act 2 · Links on")
v.add(T_A3, act3, [(0.3, "Act 3 · Same rule for p, Λ⁰ and Ω⁻"),
                   (3.5, "Routing stays near 715–721 ticks; the bare part grows with s quarks"),
                   (7.2, f"Same scale: p {NUC['mass_MeV'] * SCALE:.0f} vs {PDG_P:.0f},  Ω⁻ {OME['mass_MeV'] * SCALE:.0f} vs {PDG_O:.0f} MeV")],
      "Act 3 · Comparison")
v.add(T_END, end_card([(f"Bare uds: {BARE:.0f} ticks (formula 12 + 91 per s quark)", RED),
                       (f"Links + spin: {100 * (ROUTE + SPIN) / TOT:.1f}% of Λ⁰ ticks, in this toy model", VIOLET),
                       (f"MeV scale fitted to PDG Λ⁰: 1 tick = {SCALE:.3f} MeV", YELLOW),
                       (f"Same scale: Ω⁻ off by {OME['mass_MeV'] * SCALE - PDG_O:+.0f} MeV; not a QCD result", DIM)]))
assert abs(v.duration - TOTAL) < 1e-9

def timeline():
    return {"total": TOTAL, "act1": [A1, A2], "act2": [A2, A3], "act3": [A3, END],
            "title": [0, T_TITLE], "end": [END, TOTAL],
            "links_on": [A2 + LINK_ON[0], A2 + LINK_ON[1]], "climb": [A2 + CLIMB[0], A2 + CLIMB[1]],
            "land": A2 + CLIMB[1], "hops": [[A2 + th, q] for th, q, _, _ in HOPS],
            "bars": [A3 + b for b in BAR_T], "pdg_marks": A3 + 6.5}

if __name__ == "__main__":
    finish(v, "uds_mass", timeline(), os.path.join(OUT, "sfx_uds_mass.py"),
           thumb_t=A2 + CLIMB[1] + 1.5, audio_only="--audio-only" in sys.argv)
