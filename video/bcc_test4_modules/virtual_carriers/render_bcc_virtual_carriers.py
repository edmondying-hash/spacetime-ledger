#!/usr/bin/env python3
"""v5 preview (synthesized SFX): explainer video for bcc_virtual_carriers.py (toy model).

Edmond's module is imported unchanged from a snapshot at
/workspace/bcc_test4_videos/v5/carriers_src. Tabulated on-screen numbers are
asserted against BCCVirtualCarrierSim().simulate_carrier_range (photon mass 0;
W mass 80379, range_scale_hops 1.5) and gluon_carrier_bundling() defaults.
weak_flavor_transition_rate is unused by the demo and is not shown.
"""
import sys, os, math
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
sys.path.insert(0, "/workspace/bcc_test4_videos/v5/carriers_src")
from bccvid import *
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, FancyArrowPatch
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from bcc_virtual_carriers import BCCVirtualCarrierSim

OUT = "/workspace/bcc_test4_videos/v5/virtual_carriers"
W_MASS, R0, MAX_HOPS = 80379.0, 1.5, 8
TICK_TO_MEV, TICKS_PER_HOP, BREAK_MEV = 5.0, 9.0, 275.0
MEV_PER_HOP = TICKS_PER_HOP * TICK_TO_MEV  # 45
HOP0, HOP_DT, HOP_EASE = 0.50, 3.00, 0.55  # within the three-panel scene

sim = BCCVirtualCarrierSim(tick_to_mev=TICK_TO_MEV)
EM = sim.simulate_carrier_range(max_hops=MAX_HOPS, mass_mev=0.0)
WK = sim.simulate_carrier_range(max_hops=MAX_HOPS, mass_mev=W_MASS, range_scale_hops=R0)
GL = sim.gluon_carrier_bundling(max_hops=MAX_HOPS, ticks_per_hop=TICKS_PER_HOP,
                                break_threshold_mev=BREAK_MEV)

assert [(r["hops"], r["mass_mev"], r["decay_factor"], r["potential"], r["shell_flux"]) for r in EM] == [
    (1, 0.0, 1.0, 1.0, 1.0),
    (2, 0.0, 1.0, 0.5, 1.0),
    (3, 0.0, 1.0, 0.333333, 1.0),
    (4, 0.0, 1.0, 0.25, 1.0),
    (5, 0.0, 1.0, 0.2, 1.0),
    (6, 0.0, 1.0, 0.166667, 1.0),
    (7, 0.0, 1.0, 0.142857, 1.0),
    (8, 0.0, 1.0, 0.125, 1.0),
]
assert [(r["hops"], r["mass_mev"], r["decay_factor"], r["potential"], r["shell_flux"]) for r in WK] == [
    (1, 80379.0, 0.513417, 0.513417, 0.855695),
    (2, 80379.0, 0.263597, 0.131799, 0.61506),
    (3, 80379.0, 0.135335, 0.045112, 0.406006),
    (4, 80379.0, 0.069483, 0.017371, 0.254773),
    (5, 80379.0, 0.035674, 0.007135, 0.154587),
    (6, 80379.0, 0.018316, 0.003053, 0.091578),
    (7, 80379.0, 0.009404, 0.001343, 0.053287),
    (8, 80379.0, 0.004828, 0.000603, 0.030577),
]
assert [(r["hops"], r["tube_mev"], r["snapped"], r["regime"]) for r in GL] == [
    (1, 45.0, False, "1D bundled color flux tube"),
    (2, 90.0, False, "1D bundled color flux tube"),
    (3, 135.0, False, "1D bundled color flux tube"),
    (4, 180.0, False, "1D bundled color flux tube"),
    (5, 225.0, False, "1D bundled color flux tube"),
    (6, 270.0, False, "1D bundled color flux tube"),
    (7, 315.0, True, "Snapped -> new q qbar pair"),
    (8, 360.0, True, "Snapped -> new q qbar pair"),
]
assert all(abs(r["shell_flux"] - 1.0) < 5e-7 for r in EM)
assert all(abs(r["potential"] - 1.0 / r["hops"]) < 5e-7 for r in EM)
assert GL[5]["tube_mev"] == 270.0 and not GL[5]["snapped"]
assert GL[6]["tube_mev"] == 315.0 and GL[6]["snapped"] and 315.0 > BREAK_MEV
assert MEV_PER_HOP == 45.0
# 3-decimal readout used in captions (official 6-decimal values stay on the panels)
assert round(WK[0]["decay_factor"], 3) == 0.513
assert round(WK[3]["decay_factor"], 3) == 0.069
assert round(WK[7]["decay_factor"], 3) == 0.005

EM_BY = {r["hops"]: r for r in EM}
WK_BY = {r["hops"]: r for r in WK}
GL_BY = {r["hops"]: r for r in GL}


def _lattice_segments(n=5):
    segs, hi = [], []
    for x in range(n):
        for y in range(n):
            for z in range(n):
                for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                    x2, y2, z2 = x + dx, y + dy, z + dz
                    if x2 >= n or y2 >= n or z2 >= n:
                        continue
                    edge = [(x, y, z), (x2, y2, z2)]
                    mid = (x + x2) / 2, (y + y2) / 2, (z + z2) / 2
                    if all(1.5 <= m <= 2.5 for m in mid):
                        hi.append(edge)
                    else:
                        segs.append(edge)
    return segs, hi


LAT_SEGS, LAT_HI = _lattice_segments(5)
LAT_NODES = [(x, y, z) for x in range(5) for y in range(5) for z in range(5)]


def hop_state(t):
    """Return current integer hop (0..8) and a 0..1 ease for the newest hop."""
    if t < HOP0:
        return 0, 0.0
    k = min(MAX_HOPS, int((t - HOP0) / HOP_DT) + 1)
    t0 = HOP0 + (k - 1) * HOP_DT
    return k, ease((t - t0) / HOP_EASE)


def title_scene(fig, t, T):
    ax = fig.add_axes([0.06, 0.10, 0.88, 0.84], projection="3d")
    ax.set_facecolor(BG)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((0.043, 0.051, 0.075, 1.0))
        axis._axinfo["grid"]["color"] = (0.12, 0.14, 0.20, 0.35)
    a = ramp(t, 0.05, 0.7)
    ax.add_collection3d(Line3DCollection(LAT_SEGS, colors=(0.28, 0.33, 0.44, 0.45 * a), linewidths=0.9))
    ax.add_collection3d(Line3DCollection(LAT_HI, colors=(0.31, 0.82, 1.0, 0.95 * a), linewidths=2.2))
    xs, ys, zs = zip(*LAT_NODES)
    ax.scatter(xs, ys, zs, s=10, c="#8b94a8", alpha=0.55 * a, depthshade=False, linewidths=0)
    # three traces leaving the cube centre along the 6-face axes
    g = ease(max(0.0, min(1.0, (t - 0.35) / 2.4)))
    c = 2.0
    reach = 2.15 * g
    if reach > 0.02:
        ax.plot([c, c + reach], [c, c], [c, c], color=CYAN, lw=2.4, alpha=0.95 * a)
        ax.plot([c, c], [c, c + reach], [c, c], color=ORANGE, lw=2.4, alpha=0.55 * a)
        ax.plot([c, c], [c, c], [c, c + reach], color=VIOLET, lw=2.8, alpha=0.95 * a)
    ax.set_xlim(-0.4, 4.4); ax.set_ylim(-0.4, 4.4); ax.set_zlim(-0.4, 4.4)
    ax.set_axis_off()
    ax.view_init(elev=18, azim=-52 + 14 * (t / max(T, 1e-6)))
    ta = ramp(t, 0.15, 0.6)
    fig.text(0.5, 0.58, "Virtual force carriers on the lattice (toy model)",
             fontsize=40, weight="bold", ha="center", va="center", alpha=ta,
             bbox=dict(boxstyle="round,pad=0.35", fc="#0b0d13", ec="none", alpha=0.66 * ta))
    fig.text(0.5, 0.455, "One hop per tick on a 6-face grid",
             fontsize=26, color=DIM, ha="center", va="center", alpha=ramp(t, 0.55, 0.6))


def _panel_box(fig, x0, width, color, title, sub=""):
    ax = fig.add_axes([x0, 0.155, width, 0.725])
    ax.set_facecolor(PANEL)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(color)
        s.set_linewidth(1.8)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title(title, fontsize=22, color=color, pad=10, weight="bold")
    if sub:
        ax.text(0.5, 0.955, sub, transform=ax.transAxes, ha="center", va="top",
                fontsize=13, color=DIM)
    return ax


def _diamond(ax, r, **kw):
    ax.plot([r, 0, -r, 0, r], [0, r, 0, -r, 0], **kw)


def _shell_panel(fig, x0, width, hop, frac, rows_by, color, fade=False):
    """2D slice of the 6-face grid: Manhattan (diamond) shells around a source."""
    pad = (width - 0.36) / 2
    ax = fig.add_axes([x0 + pad, 0.36, 0.36, 0.455])
    ax.set_facecolor(PANEL)
    ax.set_xlim(-9.2, 9.2); ax.set_ylim(-9.2, 9.2)
    ax.set_aspect("equal"); ax.axis("off")
    # faint lattice dots
    for i in range(-8, 9):
        for j in range(-8, 9):
            if (abs(i) + abs(j)) <= 8:
                ax.plot(i, j, "o", ms=2.0, color=GRID, alpha=0.55, zorder=1)
    if hop <= 0:
        ax.plot(0, 0, "o", ms=16, color=YELLOW, mec=FG, zorder=6)
        return ax
    for r in range(1, hop + 1):
        row = rows_by[r]
        appear = 1.0 if r < hop else frac
        if appear <= 0:
            continue
        if fade:
            alpha = min(1.0, row["decay_factor"] * 1.35) * appear
            alpha = max(alpha, 0.04 * appear)
            lw = 1.4 + 1.2 * (r == hop)
        else:
            alpha = (0.28 + 0.72 / r) * appear
            lw = 1.6 + 1.4 * (r == hop)
        _diamond(ax, r, color=color, lw=lw, alpha=min(alpha, 1.0), zorder=3)
        # nodes on this shell
        pts = [(i, r - abs(i)) for i in range(-r, r + 1)] + [(i, -(r - abs(i))) for i in range(-r + 1, r)]
        ms = 7.0 if r == hop else 4.5
        ax.scatter([p[0] for p in pts], [p[1] for p in pts],
                   s=ms ** 2, c=color, alpha=min(alpha, 1.0), zorder=4, linewidths=0)
    ax.plot(0, 0, "o", ms=16, color=YELLOW, mec=FG, mew=0.8, zorder=6)
    return ax


def p_carriers(fig, t, T):
    hop, frac = hop_state(t)
    # three equal panels
    gap, width, x0 = 0.015, 0.30, 0.025
    xs = [x0, x0 + width + gap, x0 + 2 * (width + gap)]

    # Photon
    _panel_box(fig, xs[0], width, CYAN, "Photon", "m = 0")
    _shell_panel(fig, xs[0], width, hop, frac, EM_BY, CYAN, fade=False)
    if hop >= 1:
        row = EM_BY[hop]
        fig.text(xs[0] + width / 2, 0.33, f"V = {row['potential']:.3f}    (1/r)",
                 fontsize=16, color=CYAN, ha="center", va="center")
        fig.text(xs[0] + width / 2, 0.275, f"shell flux  {row['shell_flux']:.3f}",
                 fontsize=18, color=GREEN, ha="center", va="center", weight="bold")
        fig.text(xs[0] + width / 2, 0.225, "conserved every hop",
                 fontsize=13, color=DIM, ha="center", va="center")
    else:
        fig.text(xs[0] + width / 2, 0.30, "V = 1/r", fontsize=16, color=DIM, ha="center")

    # W boson
    _panel_box(fig, xs[1], width, ORANGE, "W boson", "m = 80,379 MeV  ·  r₀ = 1.5 hops")
    _shell_panel(fig, xs[1], width, hop, frac, WK_BY, ORANGE, fade=True)
    if hop >= 1:
        row = WK_BY[hop]
        fig.text(xs[1] + width / 2, 0.33, f"survival  {row['decay_factor']:.6f}",
                 fontsize=17, color=ORANGE, ha="center", va="center", weight="bold")
        fig.text(xs[1] + width / 2, 0.275, "exp(−r / 1.5)",
                 fontsize=14, color=DIM, ha="center", va="center")
        if hop >= 4:
            fig.text(xs[1] + width / 2, 0.225, "short range",
                     fontsize=16, color=YELLOW, ha="center", va="center", weight="bold")
    else:
        fig.text(xs[1] + width / 2, 0.30, "Yukawa decay", fontsize=16, color=DIM, ha="center")

    # Gluon
    _panel_box(fig, xs[2], width, VIOLET, "Gluon", "+45 MeV / hop    threshold 275 MeV")
    _gluon_tube(fig, xs[2], width, hop, frac, t)
    if hop >= 1:
        # Freeze the readout at the snap (hop 7, 315 MeV); hop 8 stays snapped.
        show = 7 if hop >= 7 else hop
        row = GL_BY[show]
        col = YELLOW if row["snapped"] else VIOLET
        fig.text(xs[2] + width / 2, 0.275, f"{row['tube_mev']:.0f} MeV",
                 fontsize=20, color=col, ha="center", va="center", weight="bold")
        if row["snapped"]:
            fig.text(xs[2] + width / 2, 0.225, "315 > 275 MeV  ·  snapped",
                     fontsize=13, color=YELLOW, ha="center", va="center")
        else:
            fig.text(xs[2] + width / 2, 0.225, "1D color flux tube",
                     fontsize=13, color=DIM, ha="center", va="center")
    else:
        fig.text(xs[2] + width / 2, 0.30, "bundles, does not spread",
                 fontsize=14, color=DIM, ha="center")

    # hop counter uses the chrome heading slot (right, y=0.955)
    fig.text(0.97, 0.955, f"hop  {hop}  /  8", fontsize=20, color=FG, ha="right", va="center")


def _gluon_tube(fig, x0, width, hop, frac, t):
    ax = fig.add_axes([x0 + 0.012, 0.40, width - 0.024, 0.30])
    ax.set_facecolor(PANEL)
    ax.set_xlim(-0.7, 7.7)
    ax.set_ylim(-1.15, 1.00)
    ax.axis("off")
    n_cells = 8
    for i in range(n_cells):
        ax.add_patch(Rectangle((i - 0.45, -0.38), 0.90, 0.76,
                               fc="#0e121c", ec=GRID, lw=1.0, zorder=1))
    # length grows up to hop 6; at hop 7 it snaps and we freeze (brief)
    if hop <= 0:
        ax.plot(0, 0, "o", ms=16, color=YELLOW, mec=FG, zorder=6)
        return
    if hop < 7:
        length = (hop - 1) + frac
        ax.plot([0, length], [0, 0], color=VIOLET, lw=10, alpha=0.88,
                solid_capstyle="round", zorder=3)
        ax.plot(0, 0, "o", ms=16, color=YELLOW, mec=FG, zorder=6)
        ax.plot(length, 0, "o", ms=10, color=VIOLET, mec=FG, zorder=5)
    else:
        # snap animation: gap opens during hop-7 ease, pair pops in
        snap_a = frac if hop == 7 else 1.0
        L = 7.0
        mid = L / 2.0
        gap = 0.85 * snap_a
        ax.plot([0, mid - gap], [0, 0], color=VIOLET, lw=10, alpha=0.88,
                solid_capstyle="round", zorder=3)
        ax.plot([mid + gap, L], [0, 0], color=VIOLET, lw=10, alpha=0.88,
                solid_capstyle="round", zorder=3)
        ax.plot(0, 0, "o", ms=16, color=YELLOW, mec=FG, zorder=6)
        ax.plot(L, 0, "o", ms=12, color=VIOLET, mec=FG, zorder=5)
        if snap_a > 0.35:
            pa = ease((snap_a - 0.35) / 0.65)
            # new q qbar pair in the gap
            ax.plot(mid - 0.38, 0, "o", ms=18 * (0.6 + 0.4 * pa), color=RED, mec=FG,
                    alpha=pa, zorder=7)
            ax.plot(mid + 0.38, 0, "o", ms=18 * (0.6 + 0.4 * pa), color=CYAN, mec=FG,
                    alpha=pa, zorder=7)
            ax.text(mid - 0.38, 0.62, "q", ha="center", va="bottom", fontsize=14,
                    color=RED, alpha=pa, weight="bold")
            ax.text(mid + 0.38, 0.62, "q̄", ha="center", va="bottom", fontsize=14,
                    color=CYAN, alpha=pa, weight="bold")
            ax.text(mid, -0.78, "new pair", ha="center", va="center", fontsize=13,
                    color=YELLOW, alpha=pa, weight="bold")

    # energy bar along the bottom of this axes
    # (drawn in figure coords below, via a slim axes)
    b = fig.add_axes([x0 + 0.022, 0.315, width - 0.044, 0.038])
    style_ax(b, grid=False)
    show_h = 7 if hop >= 7 else hop
    if show_h >= 1:
        mev = GL_BY[show_h]["tube_mev"]
        if hop < 7:
            mev = ((hop - 1) + frac) * MEV_PER_HOP
        col = YELLOW if show_h >= 7 else VIOLET
        b.barh(0, mev, height=0.7, color=col, alpha=0.95)
    b.axvline(BREAK_MEV, color=RED, lw=1.6, zorder=3)
    b.set_xlim(0, 360)
    b.set_yticks([]); b.set_xticks([])
    for s in b.spines.values():
        s.set_color(GRID)
    b.set_ylim(-0.55, 0.55)


v = Video(OUT, "_silent", "bcc_test4 · bcc_virtual_carriers.py",
          "Toy model on a 6-face cubic grid · numbers from the actual run of bcc_virtual_carriers.py")
v.add(5.0, title_scene)

v.add(29.0, p_carriers, [
    (0.3, "Photon: V = 1/r  ·  shell flux stays 1.000 every hop"),
    (9.5, "W boson fades:  0.513 at hop 1  ·  0.069 at hop 4"),
    (18.5, "Gluon snaps at hop 7  (315 > 275 MeV)  ·  a new q q̄ pair"),
    (21.5, "W survival 0.005 at hop 8  ·  short range"),
], "")

v.add(6.0, end_card([
    ("The 1/r and decay laws are set in the code", ORANGE),
    ("W range (1.5 hops) is a set parameter", YELLOW),
    ("Snap threshold 275 MeV is chosen", DIM),
], head="Toy model"))


def timeline():
    sc = scene_starts(v); a = [x["start"] for x in sc]
    hops = [a[1] + HOP0 + HOP_DT * (r - 1) for r in range(1, MAX_HOPS + 1)]
    return {
        "total": v.duration,
        "scenes": sc,
        "title": [0, a[1]],
        "carriers": [a[1], a[2]],
        "hops": hops,
        "hop1": hops[0],
        "hop4": hops[3],
        "hop8": hops[7],
        "snap": hops[6],  # hop 7
        "w_fade_ann": a[1] + 9.5,
        "end": a[2],
    }


if __name__ == "__main__":
    assert abs(v.duration - 40.0) < 1e-9, v.duration
    finish(v, "bcc_virtual_carriers", timeline(), os.path.join(OUT, "sfx_bcc_virtual_carriers.py"),
           thumb_t=5.0 + 19.2, audio_only="--audio-only" in sys.argv)
