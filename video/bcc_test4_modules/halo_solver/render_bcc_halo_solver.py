#!/usr/bin/env python3
"""v5 preview (synthesized SFX): explainer video for bcc_halo_solver.py (toy model).

Edmond's modules are imported unchanged. Tabulated on-screen numbers are asserted
against BCCDarkMatterSim().rotation_curve, BCCHaloSolver().invert_rotation_curve
and cored_vs_cusp_profile. Smooth strokes evaluate the same functions at dense
radii (unrounded for the stroke; official rounded table values as markers).
"""
import sys, os, math
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
sys.path.insert(0, "/workspace/bcc_test4_videos/v5/bcc_test4")
from bccvid import *
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from bcc_dark_matter import BCCDarkMatterSim
from bcc_halo_solver import BCCHaloSolver

OUT = "/workspace/bcc_test4_videos/v5/bcc_halo_solver"
RADII = [2.0, 4.0, 8.0, 14.0, 20.0]
CUSP_R = [0.2, 0.5, 1.0, 2.5, 5.0, 10.0]
RHO_0, CORE_RADIUS, NODE_CAP = 85.0, 2.5, 100.0

dm = BCCDarkMatterSim()
solver = BCCHaloSolver(g_grid=1.0, node_cap=NODE_CAP, loop_mass_mev=2001.19)
CURVE = dm.rotation_curve(RADII)
INV = solver.invert_rotation_curve(CURVE)
CUSP = solver.cored_vs_cusp_profile(CUSP_R, rho_0=RHO_0, core_radius=CORE_RADIUS)

assert [(c["r"], c["v_baryon"], c["v_total"]) for c in CURVE] == [
    (2.0, 20.06, 21.26), (4.0, 16.36, 19.88), (8.0, 12.18, 19.43),
    (14.0, 9.26, 19.58), (20.0, 7.75, 19.76)]
assert [(r["m_baryon"], r["m_halo"], r["dark_to_baryon"], r["dark_fraction"], r["est_loops"], r["rho_halo"])
        for r in INV] == [
    (804.81, 99.17, 0.12, 0.1097, 247.8, 0.98644),
    (1070.6, 510.26, 0.48, 0.3228, 1274.9, 1.0223),
    (1186.82, 1833.38, 1.54, 0.607, 4580.7, 0.41129),
    (1200.47, 4166.8, 3.47, 0.7763, 10410.8, 0.1579),
    (1201.25, 6607.9, 5.5, 0.8462, 16509.9, 0.08094)]
assert [(c["r"], c["nfw_cusp_ticks"], c["grid_core_ticks"], c["status"]) for c in CUSP] == [
    (0.2, 1062.5, 84.46, "Cored & Bounded (< 100 cap)"),
    (0.5, 425.0, 81.73, "Cored & Bounded (< 100 cap)"),
    (1.0, 212.5, 73.28, "Cored & Bounded (< 100 cap)"),
    (2.5, 85.0, 42.5, "Cored & Bounded (< 100 cap)"),
    (5.0, 42.5, 17.0, "Cored & Bounded (< 100 cap)"),
    (10.0, 21.25, 5.0, "Cored & Bounded (< 100 cap)")]
assert all(c["grid_core_ticks"] < NODE_CAP for c in CUSP)

# Smooth strokes: same enclosed_loads / v = sqrt(W/r) and invert / cusp formulas.
R_V = np.linspace(0.7, 21.0, 280)
ENC = [dm.enclosed_loads(float(r)) for r in R_V]
V_BAR = np.array([math.sqrt(e["baryon_load"] / e["r"]) for e in ENC])
V_TOT = np.array([math.sqrt(e["total_load"] / e["r"]) for e in ENC])
R_M = np.linspace(1.0, 20.0, 220)
INV_D = solver.invert_rotation_curve(dm.rotation_curve([float(r) for r in R_M]))
M_HALO_D = np.array([row["m_halo"] for row in INV_D])
M_BAR_D = np.array([row["m_baryon"] for row in INV_D])
R_C = np.linspace(0.2, 10.0, 260)
CUSP_D = solver.cored_vs_cusp_profile([float(r) for r in R_C], rho_0=RHO_0, core_radius=CORE_RADIUS)
NFW_D = np.array([row["nfw_cusp_ticks"] for row in CUSP_D])
CORE_D = np.array([row["grid_core_ticks"] for row in CUSP_D])

# Stylized Q_EM=0 loop positions (visual stand-in; counts on screen are official est_loops).
RNG = np.random.default_rng(2026)
N_VIS = 160
LOOP_TH = RNG.uniform(0, 2 * np.pi, N_VIS)
LOOP_R = 2.4 + 17.4 * np.sqrt(RNG.uniform(0, 1, N_VIS))
LOOP_PHI = RNG.uniform(0, np.pi, N_VIS)
LOOP_A = RNG.uniform(0.28, 0.48, N_VIS)


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
    # faint equatorial ring suggesting a halo around the central cube
    th = np.linspace(0, 2 * np.pi, 80)
    ring_a = 0.35 * ramp(t, 0.4, 0.8)
    ax.plot(2 + 2.15 * np.cos(th), 2 + 2.15 * np.sin(th), np.full_like(th, 2.0),
            color=VIOLET, lw=1.6, alpha=ring_a)
    ax.set_xlim(-0.4, 4.4); ax.set_ylim(-0.4, 4.4); ax.set_zlim(-0.4, 4.4)
    ax.set_axis_off()
    ax.view_init(elev=17, azim=-48 + 16 * (t / max(T, 1e-6)))
    ta = ramp(t, 0.15, 0.6)
    fig.text(0.5, 0.58, "Dark-matter halo solver (toy model)", fontsize=48, weight="bold",
             ha="center", va="center", alpha=ta,
             bbox=dict(boxstyle="round,pad=0.35", fc="#0b0d13", ec="none", alpha=0.62 * ta))
    fig.text(0.5, 0.455, "Inverting a rotation curve on a 6-face Planck-cube lattice",
             fontsize=24, color=DIM, ha="center", va="center", alpha=ramp(t, 0.55, 0.6))


def p_curve(fig, t, T):
    ax = style_ax(fig.add_axes([0.08, 0.20, 0.86, 0.64]))
    g_bar = ease(max(0.0, min(1.0, (t - 0.4) / 3.2)))
    g_tot = ease(max(0.0, min(1.0, (t - 4.0) / 2.6)))
    g_gap = ramp(t, 7.0, 1.2)
    if g_bar > 0:
        n = max(2, int(g_bar * len(R_V)))
        ax.plot(R_V[:n], V_BAR[:n], color=ORANGE, lw=3.0, label="v_baryon")
    if g_tot > 0:
        n = max(2, int(g_tot * len(R_V)))
        ax.plot(R_V[:n], V_TOT[:n], color=CYAN, lw=3.0, label="v_total")
    if g_gap > 0:
        ax.fill_between(R_V, V_BAR, V_TOT, color=VIOLET, alpha=0.28 * g_gap, label="halo")
        ax.text(12.2, 14.6, "halo", color=VIOLET, fontsize=22, alpha=g_gap, weight="bold")
    rmax_bar = 0.7 + g_bar * (21.0 - 0.7)
    rmax_tot = 0.7 + g_tot * (21.0 - 0.7)
    for row in CURVE:
        r, vb, vt = row["r"], row["v_baryon"], row["v_total"]
        if r <= rmax_bar + 0.05:
            ax.plot(r, vb, "o", ms=10, color=ORANGE, mec=FG, mew=0.8, zorder=5)
            ax.text(r, vb - 1.35, f"{vb:.2f}", ha="center", va="top", fontsize=14, color=ORANGE)
        if r <= rmax_tot + 0.05:
            ax.plot(r, vt, "o", ms=10, color=CYAN, mec=FG, mew=0.8, zorder=5)
            dy = 1.15 if r > 2.5 else 1.55
            ax.text(r, vt + dy, f"{vt:.2f}", ha="center", va="bottom", fontsize=14, color=CYAN)
    ax.set_xlim(0.0, 22.0); ax.set_ylim(0.0, 26.0)
    ax.set_xlabel("radius r", fontsize=16)
    ax.set_ylabel("orbital speed v  (grid units)", fontsize=16)
    h, lab = ax.get_legend_handles_labels()
    if lab:
        # keep first occurrence of each label
        seen, H, L = set(), [], []
        for hh, ll in zip(h, lab):
            if ll not in seen:
                seen.add(ll); H.append(hh); L.append(ll)
        ax.legend(H, L, loc="upper right", frameon=False, fontsize=18)


def _ratio_at(r):
    rs = [row["r"] for row in INV]
    if r >= rs[-1]:
        return INV[-1]["dark_to_baryon"], INV[-1]["dark_fraction"], INV[-1]["m_halo"], INV[-1]["est_loops"]
    db = float(np.interp(r, rs, [row["dark_to_baryon"] for row in INV], left=0.0))
    df = float(np.interp(r, rs, [row["dark_fraction"] for row in INV], left=0.0))
    mh = float(np.interp(r, rs, [row["m_halo"] for row in INV], left=0.0))
    lp = float(np.interp(r, rs, [row["est_loops"] for row in INV], left=0.0))
    return db, df, mh, lp


def p_halo(fig, t, T):
    grow = ease(max(0.0, min(1.0, (t - 0.25) / 8.6)))
    r_now = 20.0 * grow
    # left: core + Q_EM=0 loops
    ax = fig.add_axes([0.03, 0.16, 0.40, 0.70])
    ax.set_facecolor(BG)
    ax.set_xlim(-22, 22); ax.set_ylim(-22, 22); ax.set_aspect("equal"); ax.axis("off")
    # scan circle
    if r_now > 0.2:
        ax.add_patch(Circle((0, 0), r_now, fc="none", ec=GRID, lw=1.0, ls="--", alpha=0.7))
    # bright baryon core
    for rad, al in ((4.8, 0.10), (3.2, 0.18), (2.0, 0.35), (1.1, 0.7)):
        ax.add_patch(Circle((0, 0), rad, fc=YELLOW, ec="none", alpha=al))
    ax.add_patch(Circle((0, 0), 0.55, fc="#fff6c8", ec="none", alpha=0.95))
    ax.text(0, 0.0, "baryon\ncore", ha="center", va="center", fontsize=11, color=BG, weight="bold")
    # loops with r <= r_now
    for th, rr, phi, aa in zip(LOOP_TH, LOOP_R, LOOP_PHI, LOOP_A):
        if rr > r_now:
            continue
        cx, cy = rr * np.cos(th), rr * np.sin(th)
        tt = np.linspace(0, 2 * np.pi, 28)
        ex = aa * np.cos(tt)
        ey = 0.45 * aa * np.sin(tt)
        c, s = np.cos(phi), np.sin(phi)
        ax.plot(cx + c * ex - s * ey, cy + s * ex + c * ey, color=VIOLET, lw=1.15, alpha=0.82, solid_capstyle="round")
    ax.text(0, -20.6, "Q_EM = 0 loops  (stylized)", ha="center", fontsize=13, color=DIM)
    db, df, mh, lp = _ratio_at(r_now)
    # snap official values when we have reached a tabulated radius
    shown = None
    for row in INV:
        if r_now + 1e-6 >= row["r"]:
            shown = row
    if shown and r_now >= 19.85:
        db, df, mh, lp = shown["dark_to_baryon"], shown["dark_fraction"], shown["m_halo"], shown["est_loops"]
        db_s, df_s, mh_s, lp_s = f"{db:.2f}", f"{100 * df:.1f}%", f"{mh:.2f}", f"{lp:.1f}"
    elif shown and abs(r_now - shown["r"]) < 0.35:
        db, df, mh, lp = shown["dark_to_baryon"], shown["dark_fraction"], shown["m_halo"], shown["est_loops"]
        db_s, df_s, mh_s, lp_s = f"{db:.2f}", f"{100 * df:.1f}%", f"{mh:.2f}", f"{lp:.1f}"
    else:
        db_s, df_s, mh_s, lp_s = f"{db:.2f}", f"{100 * df:.1f}%", f"{mh:.0f}", f"{lp:.0f}"
    fig.text(0.23, 0.88, f"{db_s}  :  1", fontsize=34, color=FG, ha="center", va="center", weight="bold")
    fig.text(0.23, 0.835, "dark : baryon", fontsize=15, color=DIM, ha="center", va="center")
    if r_now >= 19.85:
        fig.text(0.23, 0.795, "84.6% dark   at r = 20", fontsize=16, color=YELLOW, ha="center", va="center")

    # right: enclosed mass
    b = style_ax(fig.add_axes([0.50, 0.20, 0.46, 0.62]))
    n = max(2, int(grow * len(R_M)))
    b.plot(R_M[:n], M_BAR_D[:n], color=ORANGE, lw=2.6, label="M_baryon")
    b.plot(R_M[:n], M_HALO_D[:n], color=VIOLET, lw=3.0, label="M_halo(<r)")
    for row in INV:
        if r_now + 0.05 >= row["r"]:
            b.plot(row["r"], row["m_halo"], "o", ms=9, color=VIOLET, mec=FG, zorder=5)
            b.plot(row["r"], row["m_baryon"], "o", ms=8, color=ORANGE, mec=FG, zorder=5)
            b.text(row["r"] + 0.15, row["m_halo"] + 220, f"{row['m_halo']:.2f}",
                   fontsize=13, color=VIOLET, ha="left")
    b.set_xlim(0, 22); b.set_ylim(0, 7800)
    b.set_xlabel("radius r", fontsize=16)
    b.set_ylabel("enclosed mass  (grid units)", fontsize=16)
    b.legend(loc="upper left", frameon=False, fontsize=16)
    if r_now > 0.3:
        b.axvline(r_now, color=GRID, lw=1.0, ls="--")


def p_cusp(fig, t, T):
    ax = style_ax(fig.add_axes([0.09, 0.20, 0.84, 0.62]))
    # draw inward: right (r=10) first, climbing toward the centre
    g = ease(max(0.0, min(1.0, (t - 0.35) / 4.4)))
    r_cut = 10.0 - g * (10.0 - 0.2)
    mask = R_C >= r_cut - 1e-9
    ax.axhline(NODE_CAP, color=YELLOW, lw=1.6, ls="--", alpha=0.9, zorder=2)
    if t > 0.8:
        ax.text(7.3, 100 + 38, "100-tick cap", color=YELLOW, fontsize=16)
    if mask.sum() >= 2:
        ax.plot(R_C[mask], NFW_D[mask], color=RED, lw=3.0, label="NFW cusp  (1/r)")
        ax.plot(R_C[mask], CORE_D[mask], color=CYAN, lw=3.0, label="lattice core")
    g_ann = ramp(t, 5.0, 0.8)
    for row in CUSP:
        if row["r"] + 1e-6 >= r_cut:
            ax.plot(row["r"], row["nfw_cusp_ticks"], "o", ms=8, color=RED, mec=FG, zorder=5)
            ax.plot(row["r"], row["grid_core_ticks"], "o", ms=8, color=CYAN, mec=FG, zorder=5)
    if g_ann > 0 and r_cut <= 0.2 + 1e-6:
        ax.annotate("1062.50", xy=(0.2, 1062.5), xytext=(1.7, 980),
                    color=RED, fontsize=18, alpha=g_ann,
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
        ax.annotate("84.46", xy=(0.2, 84.46), xytext=(1.55, 260),
                    color=CYAN, fontsize=18, alpha=g_ann,
                    arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.2))
    ax.set_xlim(0.0, 10.6); ax.set_ylim(0, 1180)
    ax.set_xlabel("radius r", fontsize=16)
    ax.set_ylabel("density  (ticks)", fontsize=16)
    ax.legend(loc="upper right", frameon=False, fontsize=18)
    fig.text(0.52, 0.84, r"$\rho_0 = 85$  ·  core radius $= 2.5$  ·  cap $= 100$ (not reached)",
             fontsize=16, color=DIM, ha="center")


v = Video(OUT, "_silent", "bcc_test4 · bcc_halo_solver.py",
          "Toy model on a 6-face cubic grid · numbers from the actual run of bcc_halo_solver.py")
v.add(5.0, title_scene)

v.add(10.0, p_curve, [(0.3, "v_baryon falls off (Keplerian)"),
                      (4.0, "v_total stays flat"),
                      (7.0, "The gap is the halo")], "1 · Rotation curve")

v.add(11.0, p_halo, [(0.3, "Enclosed M_halo grows outward"),
                     (6.0, "Dark : baryon  0.12  →  5.50 : 1  at r = 20  (84.6% dark)")],
      "2 · Halo build-up")

v.add(8.0, p_cusp, [(0.3, "NFW 1/r cusp climbs to 1062.50 near the centre"),
                    (5.0, "Lattice core levels at 84.46  ·  100-tick cap not reached")],
      "3 · Cusp vs core")

v.add(6.0, end_card([
    ("The halo is put into the input curve; the solver recovers it", ORANGE),
    ("Consistency check, not a prediction", YELLOW),
    (r"Core height set by $\rho_0 = 85$  ·  100-tick cap not reached", DIM),
], head="Toy model"))


def timeline():
    sc = scene_starts(v); a = [x["start"] for x in sc]
    # rotation-curve point times (when the baryon stroke reaches each tabulated r)
    def t_at(scene_start, t0, dur, r, r0, r1):
        frac = (r - r0) / (r1 - r0)
        return scene_start + t0 + dur * frac
    return {
        "total": v.duration,
        "scenes": sc,
        "title": [0, a[1]],
        "vbar": [a[1] + 0.4, a[1] + 0.4 + 3.2],
        "vtot": [a[1] + 4.0, a[1] + 4.0 + 2.6],
        "gap": a[1] + 7.0,
        "vbar_pts": [t_at(a[1], 0.4, 3.2, r, 0.7, 21.0) for r in RADII],
        "vtot_pts": [t_at(a[1], 4.0, 2.6, r, 0.7, 21.0) for r in RADII],
        "halo": [a[2], a[3]],
        "halo_pts": [a[2] + 0.25 + 8.6 * (r / 20.0) for r in RADII],
        "ratio_final": a[2] + 0.25 + 8.6,
        "cusp": [a[3], a[4]],
        "cusp_draw": [a[3] + 0.35, a[3] + 0.35 + 4.4],
        "cusp_ann": a[3] + 5.0,
        "end": a[4],
    }


if __name__ == "__main__":
    assert abs(v.duration - 40.0) < 1e-9, v.duration
    finish(v, "bcc_halo_solver", timeline(), os.path.join(OUT, "sfx_bcc_halo_solver.py"),
           thumb_t=5.0 + 10.0 + 9.6, audio_only="--audio-only" in sys.argv)
