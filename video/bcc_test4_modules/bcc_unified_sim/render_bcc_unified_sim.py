#!/usr/bin/env python3
"""v2_sound: explainer video for the v4 (6-face) bcc_unified_sim.py, with synthesized SFX.

Edmond's module is imported unchanged. Two loops are copied only to record
per-cycle / per-packet state (quark positions, core growth); each copy is
asserted to reproduce the module's own returned numbers.
"""
import sys, random
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from bccvid import *
import_src()
import numpy as np
from matplotlib.patches import Patch
import bcc_unified_sim as us

OUT = "/workspace/bcc_test4_videos/v2_sound/bcc_unified_sim"
sim = us.BCCUnifiedGridSim(size=8)
assert len(us.FACES_6) == 6 and sim.directions == us.FACES_6
FAMS = us.BARYON_FAMILIES
RES = {fam: sim.simulate_baryon_family(flv, sp, cycles=3000, seed=42 + i) for i, (fam, flv, sp) in enumerate(FAMS)}
PRINTED = {'N': 720.94, 'Delta': 722.29, 'Lambda': 814.80, 'Sigma': 835.02, 'Xi': 917.67,
           'SigmaStar': 839.12, 'XiStar': 928.14, 'Omega': 1006.39}
assert {k: RES[k]['GridMass'] for k in PRINTED} == PRINTED

# --- copy of simulate_baryon_family loop for N (seed 42) with position recording ---
def trace_family(flavors, spin_factor, cycles=3000, seed=42, keep=200):
    rng = random.Random(seed)
    pos = [(1, 1, 1), (4, 4, 4), (6, 2, 5)]
    probs = {"u": 0.72, "d": 0.72, "s": 0.40}
    tl = tr = 0; rec = []
    for _ in range(cycles):
        new = []; hops = 0
        for idx, flv in enumerate(flavors):
            px, py, pz = pos[idx]
            if rng.random() < probs[flv]:
                dx, dy, dz = sim.directions[rng.randrange(6)]
                px, py, pz = (px + dx) % sim.size, (py + dy) % sim.size, (pz + dz) % sim.size
                tr += 1; hops += 1
            new.append((px, py, pz))
        pos = new; links = us.steiner_3q_links(*pos, sim.size); tl += links
        if len(rec) < keep: rec.append((list(pos), links, hops))
    avg = tl / cycles; ns = sum(f == "s" for f in flavors)
    bare = 12.0 + 91.0 * ns; route = avg * 95.0; spin = spin_factor * (6.5 - 1.4 * ns)
    return rec, round(bare + route + spin, 2)
TRACE, chk = trace_family(("u", "u", "d"), -1.0)
assert chk == RES['N']['GridMass']

GB = {n: sim.simulate_glueball(n)['glueball_mass_mev'] for n in (0, 4, 6, 8)}
assert [GB[n] for n in (0, 4, 6, 8)] == [0.0, 2001.19, 2851.47, 3701.75]
LENS = sim.simulate_wavefront_lensing()
assert [r['lag'] for r in LENS] == [0, 0, 5, 10, 5, 0, 0]

# --- copy of simulate_2d_to_3d_deadlock loop with per-packet recording ---
core = {(x, y, 4) for x in range(3, 6) for y in range(2, 6)}; core.add((4, 6, 4))
CORE0 = frozenset(core); shell = set()
for cx, cy, cz in core:
    for dx, dy, dz in sim.directions:
        nb = (cx + dx, cy + dy, cz + dz)
        if nb not in core: shell.add(nb)
SHELL0 = len(shell); rng = random.Random(19); DL = []
for _ in range(220):
    target = sorted(shell)[rng.randrange(len(shell))]
    grew = False
    if len(core) < 23 and rng.random() < 0.08:
        core.add(target); grew = True
        for dx, dy, dz in sim.directions:
            nb = (target[0] + dx, target[1] + dy, target[2] + dz)
            if nb not in core: shell.add(nb)
    DL.append((frozenset(core), target, len(shell), grew))
dl = sim.simulate_2d_to_3d_deadlock()
assert len(CORE0) == 13 and dl['deadlocked_nodes'] == len(core) == 23 and dl['shell_nodes'] == len(shell) == 73
GROW_AT = next(i for i, d in enumerate(DL) if len(d[0]) == 23)   # packet index where the cap is reached

v = Video(OUT, "_silent", "bcc_test4 · bcc_unified_sim.py  (v4, 6-face)",
          "Toy model on a 6-face cubic grid · several terms are hard-coded formulas · numbers from the actual run")
v.add(4, title_card("Unified grid sim, 6 faces", "Baryon routing · gluon loops · lag rule · deadlock pile-up"))

QC = [CYAN, YELLOW, RED]
P1_ANIM = 6.3
def p1(fig, t, T):
    ax = style_ax(fig.add_axes([0.05, 0.18, 0.36, 0.64]), grid=False)
    for i in range(9):
        ax.plot([i - .5] * 2, [-.5, 7.5], color=GRID, lw=1); ax.plot([-.5, 7.5], [i - .5] * 2, color=GRID, lw=1)
    k = min(int(t / P1_ANIM * 160), 159)
    pos, links, hops = TRACE[k]
    for q, (x, y, z) in enumerate(pos):
        ax.scatter([x], [y], s=1900, color=QC[q], alpha=0.12, lw=0)
        ax.scatter([x], [y], s=700, color=QC[q], edgecolor=FG, lw=1.5, zorder=3)
        ax.text(x, y, "uud"[q], ha="center", va="center", fontsize=18, weight="bold", color=BG, zorder=4)
    ax.set_xlim(-.5, 7.5); ax.set_ylim(-.5, 7.5); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"N (uud) · cycle {k + 1} of 3000 · x–y view of periodic 8³ grid", fontsize=16, color=DIM)
    a2 = style_ax(fig.add_axes([0.45, 0.18, 0.11, 0.64]))
    a2.bar(0, links, color=VIOLET, width=0.6); a2.set_ylim(0, 14); a2.set_xticks([])
    a2.set_ylabel("Steiner links this cycle (6-face hops)", fontsize=14)
    a2.set_title(f"{links} links → {links * 95} route ticks", fontsize=15, color=FG, pad=14)
    a3 = style_ax(fig.add_axes([0.63, 0.18, 0.34, 0.64]))
    g = ramp(t, P1_ANIM + 0.2, 1.8)
    for i, (fam, _, _) in enumerate(FAMS):
        r = RES[fam]
        a3.barh(i, r['BareT'] * g, color=RED, height=0.6)
        a3.barh(i, r['RouteT'] * g, left=r['BareT'] * g, color=VIOLET, height=0.6)
        if g > 0.9:
            a3.text(r['GridMass'] + 10, i, f"{r['GridMass']:.2f}", va="center", fontsize=14)
    a3.set_yticks(range(8)); a3.set_yticklabels(['N', 'Δ', 'Λ', 'Σ', 'Ξ', 'Σ*', 'Ξ*', 'Ω'], fontsize=18, color=FG)
    a3.invert_yaxis(); a3.set_xlim(0, 1150); a3.set_xlabel("grid mass (ticks)", fontsize=15)
    a3.legend(handles=[Patch(color=RED, label="bare (formula)"), Patch(color=VIOLET, label="routing = 95 × avg links"), Patch(color=BG, label="spin term (≤ 6.5) not drawn")],
              loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False, fontsize=13)

v.add(14, p1, [(0.3, "Quarks hop one face at a time; the links joining them are counted"),
               (6.5, "Grid mass = bare + 95 × average links + small spin term"),
               (10.0, "Bare (12 + 91 per s quark) and spin are set by formula, not measured")], "1 · Baryon routing")

def p2(fig, t, T):
    ax = style_ax(fig.add_axes([0.14, 0.24, 0.72, 0.58]))
    vals = [GB[n] for n in (0, 4, 6, 8)]; g = ramp(t, 0.5, 2.0)
    for i, val in enumerate(vals):
        ax.bar(i, val * g, color=VIOLET if i else DIM, width=0.6)
        if g > 0.9: ax.text(i, val + 60, f"{val:.2f}", ha="center", fontsize=19)
    ax.set_xticks(range(4)); ax.set_xticklabels(["0 (vacuum)", "4", "6", "8"], fontsize=19, color=FG)
    ax.set_ylim(0, 4300); ax.set_ylabel("printed as MeV (= ticks)", fontsize=15); ax.set_xlabel("links in closed loop", fontsize=16)
    ax.text(0.02, 0.93, "mass = (102.58 + 145.045·L) + (198.05 + 280.095·L)", transform=ax.transAxes,
            fontsize=18, color=YELLOW, alpha=ramp(t, 5.0))

v.add(11, p2, [(0.3, "Quark-free loops: 2001.19 for 4 links vs 0 for vacuum"),
               (5.0, "The code computes this from a linear formula; no loop is simulated")], "2 · Gluon loops")

def p3(fig, t, T):
    ax = style_ax(fig.add_axes([0.20, 0.17, 0.60, 0.68]), grid=False)
    k = min(t / 8.0, 1.0)
    ax.scatter([12], [12], s=9000, color=ORANGE, alpha=0.10, lw=0); ax.scatter([12], [12], s=2500, color=ORANGE, alpha=0.18, lw=0)
    ax.text(12, 13.6, "cluster (schematic)", ha="center", fontsize=14, color=ORANGE)
    for r in LENS:
        x = r['x_reached'] * k
        ax.plot([0, x], [r['row_y']] * 2, color=CYAN, lw=2, alpha=0.5); ax.plot(x, r['row_y'], "o", ms=13, color=CYAN, mec=FG)
        if k >= 1:
            ax.text(25.2, r['row_y'], f"lag {r['lag']}", va="center", fontsize=18, color=YELLOW if r['lag'] else DIM)
    ax.set_xlim(-0.5, 29); ax.set_ylim(2, 22); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"tick {int(24 * k)} / 24 · rows at distance d from y = 12", fontsize=16, color=DIM)

v.add(11, p3, [(0.3, "Rows near the cluster arrive late"),
               (8.2, "Lag = 10 / (1 + 0.22 d²) for d ≤ 3, else 0: a formula, not a field")], "3 · Lag rule")

def p4(fig, t, T):
    ax = fig.add_axes([0.05, 0.14, 0.55, 0.76], projection="3d"); ax.set_facecolor(BG)
    k = min(int((t - 0.8) / 8.7 * len(DL)), len(DL) - 1) if t > 0.8 else -1
    dead = DL[k][0] if k >= 0 else CORE0
    old = [p for p in dead if p in CORE0]; new = [p for p in dead if p not in CORE0]
    ax.scatter(*zip(*old), s=160, c=ORANGE, depthshade=False, edgecolors=BG)
    if new: ax.scatter(*zip(*new), s=160, c=RED, depthshade=False, edgecolors=BG)
    if k >= 0: ax.scatter(*DL[k][1], s=90, c=CYAN, depthshade=False)
    ax.set_xlim(0, 8); ax.set_ylim(0, 8); ax.set_zlim(0, 8); ax.view_init(elev=22, azim=-60 + 30 * t / T)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.set_pane_color((0.07, 0.08, 0.13, 1)); a.set_tick_params(colors=BG)
    sh = DL[k][2] if k >= 0 else SHELL0
    fig.text(0.64, 0.72, f"deadlocked nodes   {len(dead)}", fontsize=30, color=RED if k >= 0 else ORANGE)
    fig.text(0.64, 0.64, f"3D shell               {sh}", fontsize=30, color=FG)
    fig.text(0.64, 0.56, f"packets in             {k + 1}", fontsize=30, color=CYAN)
    for i, (lab, col) in enumerate((("● start: flat 13-node core", ORANGE), ("● added to core", RED), ("● latest packet target", CYAN))):
        fig.text(0.64, 0.42 - 0.05 * i, lab, fontsize=19, color=col)

v.add(12, p4, [(0.3, "A flat 13-node core; packets hit its 6-face shell"),
               (5.0, "Each hit joins the core with 8% chance, capped at 23 nodes"),
               (9.3, "Escaped = 0 is hard-coded: nothing can leave")], "4 · Deadlock pile-up")

v.add(7, end_card([("Baryons: only the link count is simulated; bare, spin are formulas", CYAN),
                   ("Λ grid mass 814.80 ticks; no MeV scale in the code", VIOLET),
                   ("Glueball 'gap' 2001.19 and lag 10 / 5 / 0 are closed-form", YELLOW),
                   ("Core growth capped at 23; zero escape built in", RED)]))

def timeline():
    sc = scene_starts(v); a = [x["start"] for x in sc]
    hop_ev = []; last = -1
    for k in range(160):
        tk = a[1] + P1_ANIM * k / 160
        if TRACE[k][2] and tk - last > 0.11:
            hop_ev.append([tk, TRACE[k][1]]); last = tk
    pk = [a[4] + 0.8 + 8.7 * i / len(DL) for i in range(len(DL))]
    return {"total": v.duration, "scenes": sc, "title": [0, a[1]],
            "hops": hop_ev, "fam_bars": a[1] + P1_ANIM + 0.2, "formula1": a[1] + 10.0,
            "gb_rise": a[2] + 0.5, "gb_vals": [GB[n] for n in (4, 6, 8)], "gb_formula": a[2] + 5.0,
            "lens": [a[3], a[3] + 8.0], "lens_lag": a[3] + 8.0,
            "packets": pk[::3], "grow": [pk[i] for i, d in enumerate(DL) if d[3]], "cap": pk[GROW_AT],
            "end": a[5]}

if __name__ == "__main__":
    finish(v, "bcc_unified_sim", timeline(), os.path.join(OUT, "sfx_bcc_unified_sim.py"),
           thumb_t=4 + 14 + 4, audio_only="--audio-only" in sys.argv)
