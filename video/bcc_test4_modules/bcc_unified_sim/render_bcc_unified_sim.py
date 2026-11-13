#!/usr/bin/env python3
"""Explainer video for bcc_unified_sim.py.

Edmond's module is imported unchanged. Where the video needs per-tick state the
module does not expose, a method is copied here with recording added; every
copy is asserted to reproduce the module's own printed numbers.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # path edit: bccvid.py sits beside this script; was /workspace/bcc_test4_videos/_common
from bccvid import *
import_src()
import numpy as np
import bcc_unified_sim as us
from baryon_calculator import Parameters, calculate

OUT = os.path.dirname(os.path.abspath(__file__))  # path edit: this script's folder; was /workspace/bcc_test4_videos/<module>

# ---------- Part 1: baryon subroutine (record quark positions for N) ----------
class TracedGrid(us.BCCUnifiedGrid):
    trace = None
    def run_baryon_subroutine(self, flavors, pair_spins, total_cycles=6000):
        # copy of the module method + position/tick recording
        positions = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
        timers = [self.redraw_period[f] for f in flavors]
        total_ticks = bare_ticks_acc = route_ticks_acc = spin_ticks_acc = redraw_count = 0
        rec = []
        for _ in range(total_cycles):
            for i, flv in enumerate(flavors):
                timers[i] -= 1
                if timers[i] <= 0:
                    candidate = self.redraw_node(positions[i])
                    trial = list(positions); trial[i] = candidate
                    if us.steiner_y_links(trial, self.L) <= 4:
                        positions[i] = candidate; redraw_count += 1
                    timers[i] = self.redraw_period[flv]
            t_bare = sum(self.bare_ticks[f] for f in flavors)
            active_links = us.steiner_y_links(positions, self.L)
            t_route = active_links * self.ticks_link
            t_spin = 0
            for idx, (i, j) in enumerate(((0, 1), (0, 2), (1, 2))):
                if positions[i] == positions[j]:
                    rs = (self.redraw_period['l'] ** 2) / (self.redraw_period[flavors[i]] * self.redraw_period[flavors[j]])
                    t_spin += round(self.ticks_spin * rs * pair_spins[idx])
            total_ticks += t_bare + t_route + t_spin
            bare_ticks_acc += t_bare; route_ticks_acc += t_route; spin_ticks_acc += t_spin
            if len(rec) < 400:
                rec.append((list(positions), t_bare, t_route, t_spin, active_links))
        if self.trace is None:
            self.trace = rec
        avg = total_ticks / total_cycles
        return {'mass_MeV': avg * self.mev_per_tick, 'avg_ticks': avg,
                'bare_ticks': bare_ticks_acc / total_cycles, 'route_ticks': route_ticks_acc / total_cycles,
                'spin_ticks': spin_ticks_acc / total_cycles, 'redraws_per_cycle': redraw_count / total_cycles,
                'active_load_pct': 100.0 * (avg - bare_ticks_acc / total_cycles) / avg}

specs = {
    'N': (('l', 'l', 'l'), (-0.75, 0.00, 0.00)), 'Delta': (('l', 'l', 'l'), (+0.25, +0.25, +0.25)),
    'Lambda': (('l', 'l', 's'), (-0.75, 0.00, 0.00)), 'Sigma': (('l', 'l', 's'), (+0.25, -0.50, -0.50)),
    'Xi': (('s', 's', 'l'), (+0.25, -0.50, -0.50)), 'SigmaStar': (('l', 'l', 's'), (+0.25, +0.25, +0.25)),
    'XiStar': (('s', 's', 'l'), (+0.25, +0.25, +0.25)), 'Omega': (('s', 's', 's'), (+0.25, +0.25, +0.25)),
}
g = TracedGrid()
sim = {k: g.run_baryon_subroutine(*v) for k, v in specs.items()}
params = Parameters.from_anchors(N_MeV=sim['N']['mass_MeV'], Delta_MeV=sim['Delta']['mass_MeV'],
                                 Lambda_MeV=sim['Lambda']['mass_MeV'])
chmap = {'N': 'p', 'Delta': 'Delta+', 'Lambda': 'Lambda', 'Sigma': 'Sigma0', 'Xi': 'Xi0',
         'SigmaStar': 'SigmaStar0', 'XiStar': 'XiStar0', 'Omega': 'Omega-'}
rule = {k: calculate(c, parameters=params)['mass_MeV'] for k, c in chmap.items()}
PRINTED_GRID = {'N': 544.65, 'Delta': 552.26, 'Lambda': 631.75, 'Sigma': 637.07, 'Xi': 721.49,
                'SigmaStar': 643.92, 'XiStar': 731.96, 'Omega': 821.23}
PRINTED_RULE = {'N': 544.65, 'Delta': 552.26, 'Lambda': 631.75, 'Sigma': 633.39, 'Xi': 719.80,
                'SigmaStar': 638.54, 'XiStar': 724.95, 'Omega': 811.49}
for k in specs:
    assert round(sim[k]['mass_MeV'], 2) == PRINTED_GRID[k], k
    assert round(rule[k], 2) == PRINTED_RULE[k], k
assert (round(params.m_light, 2), round(params.m_strange, 2), round(params.A, 2)) == (182.82, 269.92, 5.07)
TRACE = g.trace

# ---------- Part 2: glueballs (module method, same RNG order as run_all) ----------
GB = {n: g.run_glueball_loop(loop_links=n, vertex_self_coupling=280) for n in (4, 6, 8)}
assert [round(GB[n]['mass_MeV'], 2) for n in (4, 6, 8)] == [2001.18, 2851.75, 3694.67]

# ---------- Part 3: congestion lensing, per-tick record ----------
lens = us.BCCNetworkCongestion(size=25, max_node_ticks=100)
lens.place_mass_cluster_2d(cx=12, cy=12, core_load=85, falloff=3.2)
ROWS = (4, 7, 10, 12, 14, 17, 20)
pk = {y: {'x': 0, 'wait': 0, 'hops': 0} for y in ROWS}
LENS_HIST = [{y: 0 for y in ROWS}]
for _ in range(24):  # copy of trace_light_wavefront loop with recording
    for y, s in pk.items():
        if s['x'] >= lens.size - 1: continue
        if s['wait'] > 0: s['wait'] -= 1; continue
        d = lens.tick_delay_at_2d(s['x'] + 1, y)
        if d is None: continue
        s['x'] += 1; s['wait'] = d; s['hops'] += 1
    LENS_HIST.append({y: s['x'] for y, s in pk.items()})
ref = us.BCCNetworkCongestion(size=25, max_node_ticks=100)
ref.place_mass_cluster_2d(cx=12, cy=12, core_load=85, falloff=3.2)
ref_pk = ref.trace_light_wavefront(ROWS, total_ticks=24)
assert all(ref_pk[y]['x'] == pk[y]['x'] for y in ROWS)
LAG = {y: pk[4]['x'] - pk[y]['x'] for y in ROWS}
assert [LAG[y] for y in ROWS] == [0, 0, 7, 10, 7, 0, 0]
LOAD = np.array(lens.load_2d, dtype=float)

# ---------- Part 4: flat 2D core + 3D shell, per-packet record ----------
bh = us.BCCNetworkCongestion(size=15, max_node_ticks=100)
bh.seed_flat_2d_core(cx=7, cy=7, cz=7, radius=2)
INIT_CORE = len(bh.deadlocked_3d); INIT_SHELL = len(bh.get_3d_boundary_shell())
core0 = set(bh.deadlocked_3d)
BH_HIST = []  # (deadlocked set snapshot, target, shell size)
for _ in range(220):  # copy of simulate_3d_infall_strict_lock loop with recording
    boundary = sorted(bh.get_3d_boundary_shell())
    if not boundary: break
    tx, ty, tz = bh.rng.choice(boundary)
    bh.load_3d[tz][ty][tx] += 20
    if bh.load_3d[tz][ty][tx] >= bh.max_ticks:
        bh.deadlocked_3d.add((tx, ty, tz))
    BH_HIST.append((frozenset(bh.deadlocked_3d), (tx, ty, tz), len(bh.get_3d_boundary_shell())))
chk = us.BCCNetworkCongestion(size=15, max_node_ticks=100)
chk.seed_flat_2d_core(cx=7, cy=7, cz=7, radius=2)
st = chk.simulate_3d_infall_strict_lock(incoming_packets=220, packet_load=20)
assert (INIT_CORE, INIT_SHELL) == (13, 66)
assert st['total_deadlocked'] == len(BH_HIST[-1][0]) == 23 and st['exposed_3d_shell'] == BH_HIST[-1][2] == 116

# ======================= video =======================
v = Video(OUT, "bcc_unified_sim", "bcc_test4 · bcc_unified_sim.py",
          "Toy model · tick costs are chosen inputs · all numbers from the actual run of bcc_unified_sim.py")
v.add(4, title_card("Unified BCC grid sim", "Baryon ticks · gluon loops · congestion lag · deadlock pile-up"))

QC = [RED, GREEN, CYAN]

def p1(fig, t, T):
    # left: quark pixels wandering on the 8x8x8 periodic grid (x-y projection)
    ax = style_ax(fig.add_axes([0.05, 0.18, 0.36, 0.64]), grid=False)
    L = 8
    for i in range(L + 1):
        ax.plot([i - .5, i - .5], [-.5, L - .5], color=GRID, lw=1); ax.plot([-.5, L - .5], [i - .5, i - .5], color=GRID, lw=1)
    k = min(int(t / 6.3 * 160), 159)
    pos, tb, tr, ts, links = TRACE[k]
    for q, (x, y, z) in enumerate(pos):
        off = (q - 1) * 0.18
        ax.plot(x + off, y + off, "o", ms=26, color=QC[q], mec=FG, mew=1.5)
    ax.set_xlim(-.5, L - .5); ax.set_ylim(-.5, L - .5); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"N (lll) · cycle {k + 1} of 6000 · x–y view of 8³ grid", fontsize=17, color=DIM)
    # middle: this cycle's ticks
    a2 = style_ax(fig.add_axes([0.45, 0.18, 0.12, 0.64]))
    a2.bar(0, tb, color=DIM, width=0.6, label="bare"); a2.bar(0, tr, bottom=tb, color=CYAN, width=0.6, label="route")
    a2.bar(0, ts, bottom=tb + tr, color=ORANGE, width=0.6, label="spin")
    a2.set_ylim(-500, 700); a2.set_xticks([]); a2.set_ylabel("ticks this cycle", fontsize=16)
    a2.set_title(f"{links} links · {tb + tr + ts} ticks", fontsize=16, color=FG)
    a2.legend(loc="lower center", frameon=False, fontsize=13, ncol=1)
    # right: averaged grid mass vs fitted rule
    a3 = style_ax(fig.add_axes([0.63, 0.18, 0.34, 0.64]))
    fams = list(specs); gr = ramp(t, 6.5, 1.8)
    for i, f in enumerate(fams):
        a3.barh(i, sim[f]['mass_MeV'] * gr, color=CYAN, alpha=0.75, height=0.6)
        if gr > 0.9:
            a3.plot(rule[f], i, "|", ms=28, mew=4, color=YELLOW)
            a3.text(sim[f]['mass_MeV'] + 8, i, f"{sim[f]['mass_MeV']:.2f}", va="center", fontsize=14)
    a3.set_yticks(range(8)); a3.set_yticklabels(['N', 'Δ', 'Λ', 'Σ', 'Ξ', 'Σ*', 'Ξ*', 'Ω'], fontsize=18, color=FG)
    a3.invert_yaxis(); a3.set_xlim(400, 900); a3.set_xlabel("ticks per cycle (1 tick := 1 MeV)", fontsize=15)
    a3.set_title("grid average  ▮   pair-spin rule  |", fontsize=16, color=DIM)

v.add(14, p1, [(0.3, "Three quark pixels hop; each cycle costs bare + routing + spin ticks"),
               (6.5, "Average over 6000 cycles = grid mass, in ticks"),
               (10.0, "Rule refitted to grid N, Δ, Λ: those three match by construction")], "1 · Baryon tick count")

def p2(fig, t, T):
    ax = style_ax(fig.add_axes([0.08, 0.20, 0.40, 0.60]), grid=False)
    ax.set_xlim(-1, 13); ax.set_ylim(-3, 3); ax.set_aspect("equal"); ax.axis("off")
    shapes = {4: [(0, 1), (1, 0), (0, -1), (-1, 0)], 6: [(0, 1.2), (1, .6), (1, -.6), (0, -1.2), (-1, -.6), (-1, .6)],
              8: [(0, 1.3), (.9, .9), (1.3, 0), (.9, -.9), (0, -1.3), (-.9, -.9), (-1.3, 0), (-.9, .9)]}
    for j, n in enumerate((4, 6, 8)):
        a = ramp(t, 0.5 + 0.6 * j); cx = 2 + 4 * j; pts = shapes[n] + [shapes[n][0]]
        ax.plot([cx + p[0] for p in pts], [p[1] for p in pts], "-o", color=VIOLET, lw=4, ms=10, alpha=a)
        ax.text(cx, -2.2, f"{n} links", ha="center", fontsize=20, alpha=a)
    b = style_ax(fig.add_axes([0.56, 0.25, 0.40, 0.57]))
    vals = [0.0] + [GB[n]['mass_MeV'] for n in (4, 6, 8)]
    gr = ramp(t, 2.5, 2.0)
    for i, val in enumerate(vals):
        b.bar(i, val * gr, color=VIOLET if i else DIM, width=0.6)
        if gr > 0.9:
            b.text(i, val + 60, f"{val:.2f}", ha="center", fontsize=17)
    b.set_xticks(range(4)); b.set_xticklabels(["0\n(vacuum)", "4", "6", "8"], fontsize=17, color=FG)
    b.set_ylim(0, 4300); b.set_ylabel("ticks (≙ MeV)", fontsize=16); b.set_xlabel("links in closed loop", fontsize=16)

v.add(11, p2, [(0.3, "Quark-free closed loops still cost ticks"),
               (4.0, "Smallest loop: 2001.18 vs 0 for empty vacuum"),
               (7.5, "Gap size follows from the chosen costs: 145 + 280 ticks per link")], "2 · Gluon loops")

def p3(fig, t, T):
    ax = fig.add_axes([0.22, 0.17, 0.56, 0.68])
    ax.imshow(LOAD, origin="lower", cmap="inferno", vmin=0, vmax=100, extent=(-.5, 24.5, -.5, 24.5))
    k = min(int(t / 8.5 * 24), 24)
    for y in ROWS:
        xs = [LENS_HIST[i][y] for i in range(k + 1)]
        ax.plot(range(len(xs)) and xs, [y] * len(xs), color=CYAN, lw=2, alpha=0.5)
        ax.plot(LENS_HIST[k][y], y, "o", ms=14, color=CYAN, mec=FG)
        if k == 24:
            ax.text(25.2, y, f"lag {LAG[y]}", va="center", fontsize=18, color=YELLOW if LAG[y] else DIM)
    ax.set_xlim(-.5, 29); ax.set_ylim(-.5, 24.5); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color(GRID)
    ax.set_title(f"tick {k} / 24 · node load (heat) from a cluster at y = 12", fontsize=17, color=DIM)

v.add(11, p3, [(0.3, "Packets step 1 pixel per tick; loaded nodes add queue delay"),
               (8.7, "Rows nearest the load fall behind: 10, 7, 0 pixels")], "3 · Congestion lag")

def p4(fig, t, T):
    ax = fig.add_axes([0.05, 0.14, 0.55, 0.76], projection="3d")
    ax.set_facecolor(BG)
    k = min(int((t - 0.8) / 8.7 * len(BH_HIST)), len(BH_HIST) - 1) if t > 0.8 else -1
    dead = BH_HIST[k][0] if k >= 0 else frozenset(core0)
    old = [p for p in dead if p in core0]; new = [p for p in dead if p not in core0]
    if old: ax.scatter(*zip(*old), s=150, c=ORANGE, depthshade=False, edgecolors=BG)
    if new: ax.scatter(*zip(*new), s=150, c=RED, depthshade=False, edgecolors=BG)
    if k >= 0:
        tgt = BH_HIST[k][1]; ax.scatter(*tgt, s=90, c=CYAN, depthshade=False)
    ax.set_xlim(3, 11); ax.set_ylim(3, 11); ax.set_zlim(3, 11)
    ax.view_init(elev=22, azim=-60 + 30 * t / T)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.set_pane_color((0.07, 0.08, 0.13, 1)); a.set_tick_params(colors=BG)
    shell = BH_HIST[k][2] if k >= 0 else INIT_SHELL
    fig.text(0.64, 0.72, f"deadlocked nodes   {len(dead)}", fontsize=30, color=RED if k >= 0 else ORANGE)
    fig.text(0.64, 0.64, f"exposed shell        {shell}", fontsize=30, color=FG)
    fig.text(0.64, 0.56, f"packets in             {k + 1}", fontsize=30, color=CYAN)
    fig.text(0.64, 0.42, "● start: flat 13-node core (z = 7)", fontsize=19, color=ORANGE)
    fig.text(0.64, 0.37, "● newly deadlocked", fontsize=19, color=RED)
    fig.text(0.64, 0.32, "● where the latest packet landed", fontsize=19, color=CYAN)

v.add(12, p4, [(0.3, "A flat saturated core; packets land on its 3D shell"),
               (6.0, "Core grows 13 → 23 nodes; shell 66 → 116"),
               (9.3, "Escaped = 0 is fixed in the code: packets only land on the shell")], "4 · Deadlock pile-up")

v.add(7, end_card([("Grid masses are tick counts; rule refitted to 3 of them", CYAN),
                   ("Loop 'gap' (2001.18) is set by chosen tick costs", VIOLET),
                   ("Congestion delays nearby rows by up to 10 pixels", YELLOW),
                   ("Zero escape is built in, not measured", RED)]))

if __name__ == "__main__":
    v.render(); print(v.extras(thumb_t=4 + 14 + 11 + 10))
