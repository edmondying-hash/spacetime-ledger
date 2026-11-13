#!/usr/bin/env python3
"""Explainer video for bcc3dhorizonsim.py, run as
`python3 bcc3dhorizonsim.py --size 17 --workload 2400 --packets 260`.
Module imported unchanged; the accretion loop is copied only to record the
deadlocked set after every packet, and asserted to match the module's output."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # path edit: bccvid.py sits beside this script; was /workspace/bcc_test4_videos/_common
from bccvid import *
import_src()
import numpy as np
import bcc3dhorizonsim as hz

OUT = os.path.dirname(os.path.abspath(__file__))  # path edit: this script's folder; was /workspace/bcc_test4_videos/<module>
SIZE, WORK, PACK = 17, 2400.0, 260
c = SIZE // 2
s = hz.BCC3DHorizonSim(size=SIZE, max_node_ticks=100, seed=42)
s.inject_3d_core(c, c, c, total_workload=WORK, radius=1)
s.relax_3d_congestion(iterations=250)
W0 = np.array(s.workload)
CORE0 = frozenset(s.deadlocked); SHELL0 = len(s.get_3d_boundary_shell())
HIST = []
for step in range(1, PACK + 1):  # copy of step_accretion loop + recording
    b = sorted(s.get_3d_boundary_shell())
    tx, ty, tz = s.rng.choice(b)
    s.workload[tz][ty][tx] += 25
    if s.workload[tz][ty][tx] >= s.max_ticks:
        s.deadlocked.add((tx, ty, tz))
    HIST.append((frozenset(s.deadlocked), (tx, ty, tz), len(s.get_3d_boundary_shell())))
PROF = s.radial_horizon_profile(c, c, c, max_r=6)
ref = hz.BCC3DHorizonSim(size=SIZE, max_node_ticks=100, seed=42)
ref.inject_3d_core(c, c, c, total_workload=WORK, radius=1); ref.relax_3d_congestion(iterations=250)
st = ref.step_accretion(incoming_packets=PACK, packet_load=25)
assert (len(CORE0), SHELL0) == (19, 38)
assert st['total_deadlocked'] == len(HIST[-1][0]) == 98 and st['exposed_3d_shell'] == HIST[-1][2] == 130
assert st['span_xyz'] == (7, 7, 7)
assert [(h['packets_absorbed'], h['deadlocked_nodes']) for h in st['checkpoints']] == [(50, 37), (100, 50), (200, 83)]
assert [p['workload'] for p in PROF] == [242.46, 185.32, 106.71, 119.87, 27.38, 17.12, 10.14]

v = Video(OUT, "bcc3dhorizonsim", "bcc_test4 · bcc3dhorizonsim.py  (--size 17 --workload 2400 --packets 260)",
          "Toy model · 6-face cubic grid · numbers from the actual CLI run of bcc3dhorizonsim.py")
v.add(4, title_card("Deadlock 'horizon' on a 3D grid", "Saturated nodes stop routing; infalling load piles up on the shell"))

def p1(fig, t, T):
    ax = fig.add_axes([0.05, 0.17, 0.45, 0.68])
    sl = W0[c]
    ax.imshow(np.minimum(sl, 250), origin="lower", cmap="inferno", vmin=0, vmax=250)
    if t > 2.5:
        ax.contour(sl, levels=[100], colors=[CYAN], linewidths=3)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title("workload, slice z = 8 (17³ grid)", fontsize=17, color=DIM)
    fig.text(0.56, 0.66, "node capacity: 100 ticks", fontsize=28, color=FG, alpha=ramp(t, 1.0))
    fig.text(0.56, 0.57, "W ≥ 100  →  deadlocked", fontsize=28, color=CYAN, alpha=ramp(t, 2.5))
    fig.text(0.56, 0.45, f"core: {len(CORE0)} nodes", fontsize=32, color=ORANGE, alpha=ramp(t, 4.0))
    fig.text(0.56, 0.37, f"shell: {SHELL0} nodes", fontsize=32, color=FG, alpha=ramp(t, 4.5))

v.add(9, p1, [(0.3, "Inject 2400 ticks of load at the centre, let it relax"),
              (4.0, "19 nodes saturate and stop routing")], "1 · Saturated core")

def p2(fig, t, T):
    ax = fig.add_axes([0.03, 0.13, 0.57, 0.78], projection="3d"); ax.set_facecolor(BG)
    k = min(int(max(t - 0.5, 0) / 13.0 * PACK), PACK - 1)
    dead = HIST[k][0]
    old = [p for p in dead if p in CORE0]; new = [p for p in dead if p not in CORE0]
    ax.scatter(*zip(*old), s=110, c=ORANGE, depthshade=False, edgecolors=BG)
    if new: ax.scatter(*zip(*new), s=110, c=RED, depthshade=False, edgecolors=BG, alpha=0.9)
    ax.scatter(*HIST[k][1], s=120, c=CYAN, depthshade=False)
    ax.set_xlim(4, 12); ax.set_ylim(4, 12); ax.set_zlim(4, 12)
    ax.view_init(elev=20, azim=-60 + 60 * t / T)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.set_pane_color((0.07, 0.08, 0.13, 1)); a.set_tick_params(colors=BG)
    fig.text(0.63, 0.74, f"packets in       {k + 1}", fontsize=30, color=CYAN)
    fig.text(0.63, 0.66, f"deadlocked       {len(dead)}", fontsize=30, color=RED)
    fig.text(0.63, 0.58, f"exposed shell   {HIST[k][2]}", fontsize=30, color=FG)
    fig.text(0.63, 0.47, "checkpoints (module output):", fontsize=19, color=DIM)
    for i, (n, d) in enumerate(((50, 37), (100, 50), (200, 83))):
        fig.text(0.63, 0.42 - 0.045 * i, f"{n} packets → {d} deadlocked", fontsize=19,
                 color=FG if k + 1 >= n else GRID)
    for i, (lab, col) in enumerate((("● initial 19-node core", ORANGE), ("● newly deadlocked", RED), ("● latest packet", CYAN))):
        fig.text(0.63, 0.25 - 0.04 * i, lab, fontsize=18, color=col)

v.add(15, p2, [(0.3, "Each packet adds 25 ticks to a random shell node"),
               (6.0, "Shell nodes that reach 100 lock too: the core grows"),
               (11.0, "260 packets: 98 deadlocked, shell 130, block 7×7×7")], "2 · Pile-up")

def p3(fig, t, T):
    ax = style_ax(fig.add_axes([0.10, 0.20, 0.80, 0.62]))
    for i, p in enumerate(PROF):
        g = ramp(t, 0.3 + 0.35 * i, 0.7)
        lock = p['extra_tick_delay'] is None
        ax.bar(p['r'], p['workload'] * g, width=0.6, color=RED if lock else CYAN)
        if g > 0.9:
            ax.text(p['r'], p['workload'] + 6, f"{p['workload']:.2f}", ha="center", fontsize=17)
            ax.text(p['r'], -24, "BLOCKED" if lock else f"+{p['extra_tick_delay']} tick", ha="center",
                    fontsize=15, color=RED if lock else FG)
    ax.axhline(100, color=YELLOW, lw=2.5, ls="--"); ax.text(6.45, 104, "capacity 100", ha="right", color=YELLOW, fontsize=17)
    ax.set_ylim(-35, 270); ax.set_xlim(-0.6, 6.6); ax.set_xticks(range(7))
    ax.set_xlabel("radius r along +x from centre", fontsize=17); ax.set_ylabel("workload (ticks)", fontsize=17)

v.add(11, p3, [(0.3, "Probe outward from the centre"),
               (4.0, "r = 0–3 blocked; just outside, +1 tick; then free")], "3 · Radial probe")

v.add(7, end_card([("Saturation threshold, not curvature, makes the 'horizon'", CYAN),
                   ("Core 19 → 98 nodes after 260 packets", RED),
                   ("Escaped = 0 is hard-coded: packets only land on the shell", YELLOW),
                   ("Toy model; no comparison to a real black hole", DIM)]))

if __name__ == "__main__":
    v.render(); print(v.extras(thumb_t=4 + 9 + 14))
