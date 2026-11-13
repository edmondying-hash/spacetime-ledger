#!/usr/bin/env python3
"""v2_sound (v4 suite, synthesized SFX): explainer video for bcc_3d_gravity.py (module imported unchanged; ray tracing
and the 3D Pascal step are copied only to record per-tick state, and asserted
to reproduce the module's printed numbers)."""
import sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
from bccvid import *
import_src()
import numpy as np
import bcc_3d_gravity as gm

OUT = "/workspace/bcc_test4_videos/v2_sound/bcc_3d_gravity"
sim = gm.BCC3DGravityGrid(size=25, max_node_ticks=100)
sim.inject_3d_mass_core(12, 12, 12, total_workload=1100.0, radius=1)
sim.solve_3d_poisson_congestion(iterations=250)
WK = np.array(sim.workload)  # [z][y][x]
RW = [(r, WK[12][12][12 + r]) for r in range(1, 9)]
assert [round(w, 2) for _, w in RW] == [86.85, 39.41, 22.58, 14.68, 10.16, 7.25, 5.22, 3.72]
ROWS = (2, 6, 8, 10, 12, 14, 16, 18, 22)
pk = {y: {'x': 1, 'wait': 0, 'hops': 0, 'captured': False} for y in ROWS}
HIST = [{y: 1 for y in ROWS}]
for _ in range(22):  # copy of trace_3d_light_rays loop + recording
    for y, s in pk.items():
        if s['captured'] or s['x'] >= sim.size - 2: continue
        if s['wait'] > 0: s['wait'] -= 1; continue
        d = sim.tick_delay_at(s['x'] + 1, y, 12)
        if d is None: s['captured'] = True; continue
        s['x'] += 1; s['wait'] = d; s['hops'] += 1
    HIST.append({y: s['x'] for y, s in pk.items()})
ref = sim.trace_3d_light_rays(ROWS, z_plane=12, total_ticks=22)
assert all(ref[y]['x'] == pk[y]['x'] for y in ROWS)
LAG = {y: pk[2]['x'] - pk[y]['x'] for y in ROWS}
assert [LAG[y] for y in ROWS] == [0, 0, 0, 3, 12, 3, 0, 0, 0]
ZZ = sim.trace_6face_zigzag_wave(start=(2, 12, 12), ticks=8)
assert ZZ[-1]['pos'] == (6, 12, 12)

def pascal_state(momentum, n_ticks=6):  # copy of evolve_biased_3d_pascal_wave core, returns state
    px, py, pz = momentum
    rules = [((1, 0, 0), 1 + max(0, px), True), ((-1, 0, 0), 1 + max(0, -px), False),
             ((0, 1, 0), 1 + max(0, py), True), ((0, -1, 0), 1 + max(0, -py), False),
             ((0, 0, 1), 1 + max(0, pz), True), ((0, 0, -1), 1 + max(0, -pz), False)]
    st = {(0, 0, 0): (1, 0)}
    for tick in range(1, n_ticks + 1):
        ev = tick % 2 == 0; nx = {}
        for (x, y, z), (p, n) in st.items():
            for (dx, dy, dz), w, pf in rules:
                k = (x + dx, y + dy, z + dz); cp, cn = nx.get(k, (0, 0))
                nx[k] = (cp + w * n, cn + w * p) if (ev and pf) else (cp + w * p, cn + w * n)
        st = nx
    return st
PAS = {}
for p in ((0, 0, 0), (2, 1, 0)):
    st = pascal_state(p); res = sim.evolve_biased_3d_pascal_wave(momentum=p, n_ticks=6)
    assert len(st) == res['active_3d_nodes'] == 231 and sum(a == b for a, b in st.values()) == res['dark_nodes'] == 103
    PAS[p] = (st, res)
CPL = []
cg = gm.BCC3DGravityGrid(size=25, max_node_ticks=100)
for p in ((0, 0, 0), (2, 0, 0), (2, 1, 0), (3, 2, 1)):
    CPL.append(cg.couple_pascal_momentum_to_gravity(momentum=p, tick_scale=110.0))
assert [(c['lag_b0_pixels'], c['lag_b2_pixels']) for c in CPL] == [(6, 0), (9, 1), (12, 3), (13, 5)]
assert [round(c['peak_core_W'], 2) for c in CPL] == [67.36, 89.81, 101.03, 134.71]

v = Video(OUT, "_silent", "bcc_test4 · bcc_3d_gravity.py",
          "Toy model on a 6-face cubic grid · numbers from the actual run of bcc_3d_gravity.py")
v.add(4, title_card("Congestion 'gravity' on a 3D grid", "Load spreads out · rays queue · momentum adds load"))

def p1(fig, t, T):
    ax = fig.add_axes([0.04, 0.17, 0.40, 0.68])
    ax.imshow(np.log10(WK[12] + 1e-3), origin="lower", cmap="magma", vmin=-1, vmax=2.5)
    ax.plot([13, 20], [12, 12], color=CYAN, lw=2)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title("workload W, slice z = 12 (log colour, 25³ grid)", fontsize=16, color=DIM)
    b = style_ax(fig.add_axes([0.53, 0.20, 0.43, 0.62]))
    k = min(int(t / 0.5), 8)
    rs = [r for r, _ in RW][:k]; ws = [w for _, w in RW][:k]
    b.plot(rs, ws, "o-", color=CYAN, lw=3, ms=10, label="W(r)")
    gk = ramp(t, 5.0, 1.0)
    if gk > 0:
        b.plot([r for r, _ in RW], [r * w for r, w in RW], "s-", color=ORANGE, lw=3, ms=10, alpha=gk, label="r · W(r)  (flat if 1/r)")
        b.text(1.1, 92, "86.85", color=ORANGE, fontsize=17, alpha=gk); b.text(7.4, 33, "29.76", color=ORANGE, fontsize=17, alpha=gk)
    b.set_xlim(0.5, 8.5); b.set_ylim(0, 105); b.set_xlabel("distance r from core (cells)", fontsize=16)
    b.legend(loc="upper right", frameon=False, fontsize=17)

v.add(11, p1, [(0.3, "Load injected at the centre relaxes outward"),
               (5.0, "r·W(r) falls 86.85 → 29.76: steeper than 1/r on this box")], "1 · Load profile")

def p2(fig, t, T):
    ax = fig.add_axes([0.22, 0.17, 0.56, 0.68])
    ax.imshow(np.minimum(WK[12], 100), origin="lower", cmap="inferno", vmin=0, vmax=100)
    k = min(int(t / 8.0 * 22), 22)
    for y in ROWS:
        ax.plot([1, HIST[k][y]], [y, y], color=CYAN, lw=2, alpha=0.5)
        ax.plot(HIST[k][y], y, "o", ms=13, color=CYAN, mec=FG)
        if k == 22:
            ax.text(24.2, y, f"lag {LAG[y]}", va="center", fontsize=17, color=YELLOW if LAG[y] else DIM)
    ax.set_xlim(-.5, 28.5); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"tick {k} / 22 · rays move +x one face per tick", fontsize=16, color=DIM)

v.add(11, p2, [(0.3, "Each step waits longer where load is high"),
               (8.2, "Ray through the core: 12 behind; 2 cells off: 3 behind")], "2 · Ray lag")

def p3(fig, t, T):
    ax = fig.add_axes([0.10, 0.15, 0.50, 0.75], projection="3d"); ax.set_facecolor(BG)
    k = min(int(t / 0.45), 8)
    pts = [e['pos'] for e in ZZ[:k + 1]]
    ax.plot(*zip(*pts), "-o", color=CYAN, lw=4, ms=9)
    ax.plot([2, 6], [12, 12], [12, 12], "--", color=DIM, lw=1.5)
    ax.set_xlim(1.5, 6.5); ax.set_ylim(11, 14); ax.set_zlim(11, 14); ax.view_init(elev=25, azim=-60 + 20 * t / T)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis): a.set_pane_color((0.07, 0.08, 0.13, 1))
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    fig.text(0.64, 0.62, f"tick {k}", fontsize=30)
    fig.text(0.64, 0.54, f"step {ZZ[k]['step']}", fontsize=24, color=CYAN)
    fig.text(0.64, 0.47, f"position {ZZ[k]['pos']}", fontsize=24, color=FG)

v.add(6, p3, [(0.3, "One face per tick: 8 steps, 4 along x, back to the axis")], "3 · Face-step path")

def p4(fig, t, T):
    for j, p in enumerate(((0, 0, 0), (2, 1, 0))):
        st, res = PAS[p]
        img = np.zeros((13, 13))
        for (x, y, z), (a, b) in st.items():
            if z == 0: img[y + 6, x + 6] = (a - b) ** 2
        ax = fig.add_axes([0.07 + 0.47 * j, 0.17, 0.40, 0.64])
        ax.imshow(img / img.max(), origin="lower", cmap="viridis", extent=(-6.5, 6.5, -6.5, 6.5))
        cx, cy, cz = res['born_centroid']
        ax.plot(cx, cy, "+", ms=34, mew=4, color=RED)
        ax.set_title(f"p = {p}   centroid ({cx:+.2f}, {cy:+.2f}, {cz:+.2f})", fontsize=18, color=FG)
        ax.set_xticks([]); ax.set_yticks([])
    fig.text(0.5, 0.86, "Born weight (N₊ − N₋)², slice z = 0 · 6 ticks · 231 active nodes, 103 dark", ha="center", fontsize=19, color=DIM)

v.add(11, p4, [(0.3, "Two-channel walk on 6 faces; momentum biases the face weights"),
               (5.5, "Centre shifts toward p; 103 of 231 nodes stay dark")], "4 · Aimed 3D Pascal packet")

def p5(fig, t, T):
    ax = style_ax(fig.add_axes([0.10, 0.20, 0.80, 0.60]))
    labs = [str(c['momentum']) for c in CPL]
    for i, c in enumerate(CPL):
        g = ramp(t, 0.4 + 0.5 * i, 0.8)
        ax.bar(i - 0.18, c['lag_b0_pixels'] * g, width=0.34, color=CYAN)
        ax.bar(i + 0.18, c['lag_b2_pixels'] * g, width=0.34, color=ORANGE)
        if g > 0.9:
            ax.text(i - 0.18, c['lag_b0_pixels'] + 0.25, str(c['lag_b0_pixels']), ha="center", fontsize=18)
            ax.text(i + 0.18, c['lag_b2_pixels'] + 0.25, str(c['lag_b2_pixels']), ha="center", fontsize=18)
            ax.text(i, -1.7, f"load {c['load_per_tick']}/tick", ha="center", fontsize=15, color=DIM)
    ax.set_xticks(range(4)); ax.set_xticklabels([f"p = {l}" for l in labs], fontsize=19, color=FG)
    ax.set_ylim(-2.3, 15); ax.set_ylabel("ray lag (cells)", fontsize=17)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=CYAN, label="ray through core (b = 0)"), Patch(color=ORANGE, label="ray 2 cells off (b = 2)")],
              loc="upper left", frameon=False, fontsize=17)

v.add(10, p5, [(0.3, "Feed the packet's load back in as the central mass"),
               (5.0, "Load = 6 + |p| face weights by rule → lag 6, 9, 12, 13")], "5 · Momentum → load → lag")

v.add(7, end_card([("Load decays with r, but faster than 1/r here", ORANGE),
                   ("Queueing delays rays near the core: up to 12 cells", YELLOW),
                   ("Momentum adds load by rule, so lag grows", CYAN),
                   ("A toy congestion model, not a test of GR", DIM)]))

def timeline():
    sc = scene_starts(v); a = [x["start"] for x in sc]
    return {"total": v.duration, "scenes": sc, "title": [0, a[1]],
            "profile_pts": [a[1] + 0.5 * k for k in range(1, 9)], "rw": a[1] + 5.0,
            "ray_ticks": [a[2] + 8.0 * k / 22 for k in range(1, 23)], "lag": a[2] + 8.0,
            "zig": [a[3] + 0.45 * k for k in range(1, 9)], "pascal": [a[4], a[4] + 11], "centroid": a[4] + 5.5,
            "coupler": [[a[5] + 0.4 + 0.5 * i, c['lag_b0_pixels']] for i, c in enumerate(CPL)], "end": a[6]}

if __name__ == "__main__":
    finish(v, "bcc_3d_gravity", timeline(), os.path.join(OUT, "sfx_bcc_3d_gravity.py"),
           thumb_t=4 + 11 + 10, audio_only="--audio-only" in sys.argv)
