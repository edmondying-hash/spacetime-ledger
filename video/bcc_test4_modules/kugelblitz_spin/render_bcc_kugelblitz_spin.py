#!/usr/bin/env python3
"""v6 preview (synthesized SFX): bcc_kugelblitz_spin.py with action/reaction recoil (toy model).

Edmond's updated module (bigbang mtime Nov 14 00:47, sha256 f0d701f3...) is imported unchanged
from /workspace/bcc_test4_videos/v6/kugelblitz_src. Every on-screen number is asserted against
BCCKugelblitzSpinSim(node_cap=100, ring_radius_lp=10).simulate_star_ring as called in
run_kugelblitz_spin_demo.

Display-only choices (labelled on screen):
  * star distances from the centre are random (seed 7). The module puts every star on one ring
    and none of its outputs (W, core L, star recoil L) depend on star distance.
  * the module returns only the TOTAL star recoil (-core L). The per-star share drawn here is
    -(flux_k * b_k), i.e. each star recoils from its own rays, using the module's own per-star
    terms; the shares are asserted to sum to the module's recoil_stars_lz.
  * star orbit rate = share / r^2 with unit star mass (the module has no star mass), x15.
  * ray tilt x8, core swirl x200.
"""
import sys, os, math
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
sys.path.insert(0, "/workspace/bcc_test4_videos/v6/kugelblitz_src")
from bccvid import *
import numpy as np
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from bcc_kugelblitz_spin import BCCKugelblitzSpinSim

OUT = "/workspace/bcc_test4_videos/v6/kugelblitz_spin"
NODE_CAP, RING_R, AIM = 100.0, 10.0, 0.6
SEED, R_MIN, R_MAX = 7, 3.6, 9.8
TILT_EXAG, SWIRL_EXAG, ORBIT_EXAG = 8, 200, 15

sim = BCCKugelblitzSpinSim(node_cap=NODE_CAP, ring_radius_lp=RING_R)

P1_IN = [(12, 3.0), (16, 5.0), (24, 5.0), (36, 6.0)]
P1 = [sim.simulate_star_ring(num_stars=n, ray_ticks=rt, asymmetry_bias=0.0) for n, rt in P1_IN]
assert [(r["num_stars"], r["ray_ticks"], r["central_workload"], r["deadlocked_bh"]) for r in P1] == [
    (12, 3.0, 36.0, False), (16, 5.0, 80.0, False), (24, 5.0, 120.0, True), (36, 6.0, 216.0, True)]

P2_BIAS = [0.0, 0.20, -0.08]
P2 = [sim.simulate_star_ring(num_stars=24, ray_ticks=5.0, asymmetry_bias=b) for b in P2_BIAS]
assert [(r["asymmetry_bias"], r["net_lz"], r["recoil_stars_lz"], r["ledger_sum_lz"],
         r["frame_drag_omega"], r["rotation_dir"], r["deadlocked_bh"]) for r in P2] == [
    (0.0, 0.0, 0.0, 0.0, 0.0, "Non-Rotating (Symmetric)", True),
    (0.2, 14.4, -14.4, 0.0, 0.012, "Counter-Clockwise (CCW)", True),
    (-0.08, -5.76, 5.76, 0.0, -0.0048, "Clockwise (CW)", True),
]
# star-distance independence: the module never uses a star's distance for W or L
for b in P2_BIAS:
    alt = BCCKugelblitzSpinSim(node_cap=NODE_CAP, ring_radius_lp=4.0).simulate_star_ring(
        num_stars=24, ray_ticks=5.0, asymmetry_bias=b)
    ref = sim.simulate_star_ring(num_stars=24, ray_ticks=5.0, asymmetry_bias=b)
    assert alt["central_workload"] == ref["central_workload"] and alt["net_lz"] == ref["net_lz"]
    assert alt["recoil_stars_lz"] == ref["recoil_stars_lz"]


def radii(n):
    return np.random.default_rng([SEED, n]).uniform(R_MIN, R_MAX, n)


def _rays(n, ticks, bias):
    """Per-star terms, same formulae as simulate_star_ring; star distance is display-only."""
    out = []
    Wc = Lz = F = 0.0
    rs = radii(n)
    for k in range(n):
        theta = (2.0 * math.pi * k) / n
        weight = max(0.1, 1.0 + bias * math.sin(theta))
        flux = ticks * weight
        b_k = bias * AIM * (1.0 + 0.5 * math.cos(theta))
        overlap = math.exp(-0.5 * (b_k ** 2))
        Wc += flux * overlap
        Lz += flux * b_k
        F += flux
        r = float(rs[k])
        recoil = -flux * b_k                      # this star's share of the module's -L_core
        w_star = recoil / (r * r)                 # unit star mass (display assumption)
        c, s = math.cos(theta), math.sin(theta)
        out.append({"theta": theta, "r": r, "flux": flux, "b": b_k, "recoil": recoil,
                    "w": w_star, "x": r * c, "y": r * s, "tx": -s, "ty": c})
    omega = Lz / max(1.0, F * RING_R)
    return out, Wc, Lz, F, omega


for row in P1 + P2:
    rays, W0, Lz, F, omega = _rays(row["num_stars"], row["ray_ticks"], row["asymmetry_bias"])
    assert round(W0, 2) == row["central_workload"]
    assert round(Lz, 4) == row["net_lz"]
    assert round(sum(r["recoil"] for r in rays), 4) == row["recoil_stars_lz"]
    assert round(omega, 6) == row["frame_drag_omega"]
    # every star recoils opposite to the core (b_k never changes sign: 1 + 0.5 cos >= 0.5)
    if row["asymmetry_bias"] != 0:
        assert all(np.sign(r["recoil"]) == -np.sign(Lz) for r in rays)


def _fmt(x, nd=4):
    s = f"{x:+.{nd}f}".rstrip("0").rstrip(".")
    if s in ("+0", "-0"):
        s = "0"
    return s.replace("-", "−")


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
                    (hi if all(1.5 <= m <= 2.5 for m in mid) else segs).append(edge)
    return segs, hi


LAT_SEGS, LAT_HI = _lattice_segments(5)
LAT_NODES = [(x, y, z) for x in range(5) for y in range(5) for z in range(5)]
STAR_TH = np.linspace(0, 2 * np.pi, 24, endpoint=False)
STAR_RR = 2.4 * radii(24) / R_MAX


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
    g = ease(max(0.0, min(1.0, (t - 0.35) / 2.6)))
    z0, c = 2.0, 2.0
    sx, sy = c + STAR_RR * np.cos(STAR_TH), c + STAR_RR * np.sin(STAR_TH)
    ax.scatter(sx, sy, np.full_like(STAR_TH, z0), s=22, c=YELLOW, alpha=0.9 * a,
               depthshade=False, linewidths=0, zorder=6)
    if g > 0.02:
        reach = 1.0 - 0.88 * g
        for x, y in zip(sx, sy):
            ax.plot([x, c + (x - c) * reach], [y, c + (y - c) * reach], [z0, z0],
                    color=CYAN, lw=1.1, alpha=0.55 * a * g)
        ax.scatter([c], [c], [z0], s=80 + 220 * g, c=ORANGE, alpha=min(0.95, 0.15 + 0.55 * g) * a,
                   depthshade=False, linewidths=0, zorder=7)
    ax.set_xlim(-0.4, 4.4); ax.set_ylim(-0.4, 4.4); ax.set_zlim(-0.4, 4.4)
    ax.set_axis_off()
    ax.view_init(elev=18, azim=-52 + 14 * (t / max(T, 1e-6)))
    ta = ramp(t, 0.15, 0.6)
    fig.text(0.5, 0.58, "Kugelblitz: action and reaction (toy model)",
             fontsize=36, weight="bold", ha="center", va="center", alpha=ta,
             bbox=dict(boxstyle="round,pad=0.35", fc="#0b0d13", ec="none", alpha=0.66 * ta))
    fig.text(0.5, 0.455, "Core spin and star recoil on a 6-face grid",
             fontsize=24, color=DIM, ha="center", va="center", alpha=ramp(t, 0.55, 0.6))


CORE_R = 1.55
PLOT_LIM = 13.4


def _case_clock(t, edges):
    for i in range(len(edges) - 1):
        if t < edges[i + 1] or i == len(edges) - 2:
            return i, max(0.0, t - edges[i]), edges[i + 1] - edges[i]


def _travel(tc, travel=1.45, t0=0.20):
    return ease((tc - t0) / travel)


def _core_s(sx, sy, fx, fy):
    a2 = fx * fx + fy * fy
    b2 = 2 * (sx * fx + sy * fy)
    c2 = sx * sx + sy * sy - CORE_R * CORE_R
    disc = b2 * b2 - 4 * a2 * c2
    if disc >= 0:
        roots = [(-b2 - math.sqrt(disc)) / (2 * a2), (-b2 + math.sqrt(disc)) / (2 * a2)]
        hits = [r for r in roots if 0.0 < r < 1.0]
        if hits:
            return min(hits)
    return max(0.0, min(1.0, -b2 / (2 * a2)))


def _setup(ax):
    ax.set_facecolor(BG)
    ax.set_xlim(-PLOT_LIM, PLOT_LIM)
    ax.set_ylim(-PLOT_LIM * 0.78, PLOT_LIM * 0.78)
    ax.set_aspect("equal")
    ax.axis("off")


def _core(ax, locked, travel, core_spin, omega):
    if locked:
        ax.add_patch(Circle((0, 0), CORE_R * 1.18, fc="#2a1014", ec=RED, lw=1.6, alpha=0.95, zorder=4))
        ax.add_patch(Circle((0, 0), CORE_R, fc="#12080a", ec=RED, lw=0.8, alpha=1.0, zorder=4))
        if abs(omega) > 1e-9:
            for a in range(3):
                ts = np.linspace(0.0, 2.15 * np.pi, 70)
                rr = np.linspace(0.18 * CORE_R, 0.92 * CORE_R, 70)
                # arm shape trails the spin direction
                ph = np.sign(omega) * ts + core_spin + a * (2 * np.pi / 3)
                ax.plot(rr * np.cos(ph), rr * np.sin(ph), color=ORANGE, lw=2.3, alpha=0.9, zorder=6)
        else:
            ax.add_patch(Circle((0, 0), CORE_R * 0.62, fc="none", ec="#5a3038", lw=1.0, alpha=0.8, zorder=5))
            ax.add_patch(Circle((0, 0), CORE_R * 0.32, fc="none", ec="#5a3038", lw=0.8, alpha=0.6, zorder=5))
    else:
        ax.add_patch(Circle((0, 0), CORE_R * 1.05, fc="#1a2430", ec=CYAN, lw=1.4, alpha=0.9, zorder=4))
        ax.add_patch(Circle((0, 0), CORE_R * 0.55, fc=CYAN, ec="none",
                            alpha=min(0.85, 0.20 + 0.65 * min(1.0, max(0.0, travel))), zorder=5))


def _rays_draw(ax, rays, travel, locked, alpha=1.0):
    segs, cols, px, py = [], [], [], []
    for ray in rays:
        sx, sy = ray["x"], ray["y"]
        b_vis = ray["b"] * TILT_EXAG
        farx, fary = -sx + 2 * b_vis * ray["tx"], -sy + 2 * b_vis * ray["ty"]
        fx, fy = farx - sx, fary - sy
        s_core = _core_s(sx, sy, fx, fy)
        if travel <= 0.5:
            s_now = (travel / 0.5) * s_core
        elif locked:
            s_now = s_core
        else:
            s_now = s_core + (travel - 0.5) / 0.5 * (1.0 - s_core)
        if travel > 0.02:
            segs.append([(sx, sy), (sx + s_now * fx, sy + s_now * fy)])
            cols.append((0.31, 0.82, 1.0, (0.70 if locked else 0.50) * alpha))
            if not (locked and travel > 0.62):
                px.append(sx + s_now * fx); py.append(sy + s_now * fy)
    if segs:
        ax.add_collection(LineCollection(segs, colors=cols, linewidths=1.15, zorder=3))
    if px and alpha > 0.3:
        ax.scatter(px, py, s=18, c=YELLOW, zorder=6, linewidths=0, alpha=0.95 * alpha)


def _stars(ax, rays, phis=None, trail=None):
    xs, ys = [], []
    for k, ray in enumerate(rays):
        th = ray["theta"] + (phis[k] if phis is not None else 0.0)
        xs.append(ray["r"] * math.cos(th)); ys.append(ray["r"] * math.sin(th))
        if trail is not None and abs(trail[k]) > 1e-4:
            ta = np.linspace(th - trail[k], th, 24)
            ax.plot(ray["r"] * np.cos(ta), ray["r"] * np.sin(ta), color=YELLOW, lw=1.6, alpha=0.38, zorder=5)
    ax.scatter(xs, ys, s=42, c=YELLOW, zorder=7, linewidths=0.4, edgecolors=FG, alpha=0.95)


def _meter(fig, shown_w):
    ax = fig.add_axes([0.80, 0.18, 0.13, 0.66])
    style_ax(ax, grid=False)
    ax.set_xlim(-0.8, 1.6); ax.set_ylim(0, 240.0); ax.set_xticks([])
    ax.set_yticks([0, 50, NODE_CAP, 150, 200, 240])
    ax.set_yticklabels(["0", "50", "100", "150", "200", "240"], fontsize=12)
    ax.axhline(NODE_CAP, color=RED, ls="--", lw=1.8, zorder=3)
    ax.text(1.55, NODE_CAP, "cap", fontsize=12, color=RED, va="bottom", ha="right")
    ax.bar(0.4, shown_w, width=0.85, color=RED if shown_w >= NODE_CAP else CYAN, alpha=0.92, zorder=2)
    ax.set_title("W(0)", fontsize=16, color=DIM, pad=8)
    for s in ax.spines.values():
        s.set_color(GRID)


P_EDGES = [0.0, 2.4, 4.8, 7.6, 10.5]


def p_pileup(fig, t, T):
    i, tc, dur = _case_clock(t, P_EDGES)
    row = P1[i]
    rays, *_ = _rays(row["num_stars"], row["ray_ticks"], 0.0)
    tr = _travel(tc, travel=1.30, t0=0.15)
    shown = row["central_workload"] * ease((tr - 0.42) / 0.22)
    locked = bool(row["deadlocked_bh"]) and shown >= NODE_CAP
    ax = fig.add_axes([0.015, 0.145, 0.78, 0.72])
    _setup(ax)
    _core(ax, locked, tr, 0.0, 0.0)
    _rays_draw(ax, rays, tr, locked)
    _stars(ax, rays)
    _meter(fig, shown)
    fig.text(0.865, 0.155, f"{shown:.0f}", fontsize=28, color=RED if shown >= NODE_CAP else CYAN,
             ha="center", va="center", weight="bold")
    fig.text(0.40, 0.86, f"{row['num_stars']} stars   ·   {row['ray_ticks']:.0f} ticks   ·   random distances",
             fontsize=20, color=FG, ha="center", va="center")
    if locked:
        ax.text(0.0, -CORE_R - 0.95, "DEADLOCKED,  0 escape", fontsize=16, color=RED, ha="center",
                va="top", weight="bold", zorder=8,
                bbox=dict(boxstyle="round,pad=0.28", fc="#0b0d13", ec=RED, lw=1.0, alpha=0.88))


S_EDGES = [0.0, 4.0, 15.0, 24.0]
ORBIT_T0 = 1.55   # rays have landed (travel 0.5 at 0.15 + 0.625)
RAY_FADE = (1.30, 0.6)


def _spin_state(i, tc):
    row = P2[i]
    rays, *_ = _rays(24, 5.0, row["asymmetry_bias"])
    ts = max(0.0, tc - ORBIT_T0)
    # gentle ease-in over the first 0.6 s so the start is visible
    eff = ts - 0.3 * (1 - math.exp(-ts / 0.3)) if ts > 0 else 0.0
    phis = [r["w"] * ORBIT_EXAG * eff for r in rays]
    core = row["frame_drag_omega"] * SWIRL_EXAG * eff
    trail = [r["w"] * ORBIT_EXAG * min(eff, 0.9) for r in rays]
    return row, rays, phis, core, trail


def p_spin(fig, t, T):
    i, tc, dur = _case_clock(t, S_EDGES)
    row, rays, phis, core_ang, trail = _spin_state(i, tc)
    tr = _travel(tc, travel=1.25, t0=0.15)
    ax = fig.add_axes([0.015, 0.145, 0.78, 0.72])
    _setup(ax)
    _core(ax, True, tr, core_ang, row["frame_drag_omega"])
    ray_a = 1.0 - ramp(tc, *RAY_FADE) * (0.0 if row["asymmetry_bias"] == 0 else 0.85)
    if ray_a > 0.05:
        _rays_draw(ax, rays, tr, True, ray_a)
    _stars(ax, rays, phis, trail)

    lc, sc = row["net_lz"], row["recoil_stars_lz"]
    def dcol(v):
        return DIM if abs(v) < 1e-9 else (CYAN if v > 0 else ORANGE)
    def dlab(v):
        return "still" if abs(v) < 1e-9 else ("CCW" if v > 0 else "CW")
    x = 0.865
    fig.text(x, 0.80, "bias", fontsize=14, color=DIM, ha="center")
    fig.text(x, 0.745, f"{row['asymmetry_bias']:+.2f}".replace("-", "−"), fontsize=26, color=FG,
             ha="center", weight="bold")
    fig.text(x, 0.655, "core L_z", fontsize=14, color=DIM, ha="center")
    fig.text(x, 0.595, f"{_fmt(lc)}   {dlab(lc)}", fontsize=24, color=dcol(lc), ha="center", weight="bold")
    fig.text(x, 0.505, "stars L_z (recoil)", fontsize=14, color=DIM, ha="center")
    fig.text(x, 0.445, f"{_fmt(sc)}   {dlab(sc)}", fontsize=24, color=dcol(sc), ha="center", weight="bold")
    fig.text(x, 0.355, "sum", fontsize=14, color=DIM, ha="center")
    fig.text(x, 0.300, _fmt(row["ledger_sum_lz"]), fontsize=24, color=FG, ha="center", weight="bold")
    fig.text(x, 0.255, "(recoil defined as −core)", fontsize=12, color=DIM, ha="center")
    fig.text(x, 0.205, "tilt ×8  ·  swirl ×200", fontsize=12, color=ORANGE, ha="center")
    fig.text(x, 0.170, "orbits ×15, unit star mass", fontsize=12, color=ORANGE, ha="center")
    fig.text(0.40, 0.86, "24 stars   ·   5 ticks   ·   random distances (seed 7)",
             fontsize=18, color=DIM, ha="center", va="center")


v = Video(OUT, "_silent", "bcc_test4 · bcc_kugelblitz_spin.py",
          "Toy model on a 6-face cubic grid · numbers from the actual run of bcc_kugelblitz_spin.py")
v.add(4.5, title_scene)
v.add(10.5, p_pileup, [
    (0.3, "Stars at random distances send light inward"),
    (4.9, "At W(0) = 120 the core deadlocks  ·  0 escape"),
    (7.7, "In the code, the load does not depend on star distance"),
], "1 · Starlight pile-up")
v.add(24.0, p_spin, [
    (0.3, "Symmetric ring: rays hit dead centre  ·  nothing turns"),
    (4.1, "Rays tilt  ·  the core gains L = +14.4 and spins CCW"),
    (7.6, "Reaction: the stars get L = −14.4 and orbit CW"),
    (11.0, "Inner stars turn faster: similar kick, smaller radius"),
    (15.1, "Opposite tilt  ·  core CW (−5.76)  ·  stars CCW (+5.76)"),
    (19.6, "Core + stars = 0, because the code sets the recoil to −core"),
], "2 · Action and reaction")
v.add(6.0, end_card([
    ("Star recoil = −(core L): the sum is 0 by construction", ORANGE),
    ("Spin direction is set by the chosen ray tilt", YELLOW),
    ("Star distances are random and drawn only", DIM),
    ("Per-star split and orbit speeds are display choices", DIM),
], head="Toy model"))


def timeline():
    a = [x["start"] for x in scene_starts(v)]
    p_starts = [a[1] + e for e in P_EDGES[:-1]]
    p_arrive = [s + 0.15 + 0.5 * 1.30 for s in p_starts]
    s_starts = [a[2] + e for e in S_EDGES[:-1]]
    s_arrive = [s + 0.15 + 0.5 * 1.25 for s in s_starts]
    s_orbit = [s + ORBIT_T0 for s in s_starts]
    return {"total": v.duration, "scenes": scene_starts(v), "title": [0, a[1]],
            "pileup": [a[1], a[2]], "spin": [a[2], a[3]], "end": a[3],
            "p_starts": p_starts, "p_arrive": p_arrive, "deadlock": p_arrive[2], "w216": p_arrive[3],
            "s_starts": s_starts, "s_arrive": s_arrive, "s_orbit": s_orbit,
            "bias0": s_starts[0], "bias_ccw": s_starts[1], "bias_cw": s_starts[2]}


def still(t_abs, path):
    import matplotlib.pyplot as plt
    t0 = 0.0
    for dur, fn, caps, heading in v.scenes:
        if t_abs < t0 + dur:
            fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
            fn(fig, t_abs - t0, dur); v.chrome(fig, t_abs - t0, dur, caps, heading)
            fig.savefig(path); plt.close(fig); return
        t0 += dur


if __name__ == "__main__":
    assert abs(v.duration - 45.0) < 1e-9, v.duration
    if "--stills" in sys.argv:
        for ts in [2.5, 7.0, 13.5, 16.5, 25.0, 30.0, 36.0, 42.0]:
            still(ts, os.path.join(OUT, f"_still_{ts:05.1f}.png"))
        sys.exit()
    finish(v, "bcc_kugelblitz_spin", timeline(), os.path.join(OUT, "sfx_bcc_kugelblitz_spin.py"),
           thumb_t=4.5 + 10.5 + 10.5, audio_only="--audio-only" in sys.argv)
