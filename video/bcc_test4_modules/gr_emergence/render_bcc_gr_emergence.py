#!/usr/bin/env python3
"""v5 preview (synthesized SFX): explainer video for bcc_gr_emergence.py (toy model).

Edmond's module is imported unchanged. Tabulated on-screen numbers are asserted
against BCCGREmergenceSim().time_dilation_profile and perihelion_precession.
Light deflection is omitted (already covered in an earlier video).
The rosette uses the code's grid advance, visually exaggerated and labelled so.
"""
import sys, os, math
sys.path.insert(0, "/workspace/bcc_test4_videos/v2_sound/_common")
sys.path.insert(0, "/workspace/bcc_test4_videos/v5/bcc_test4")
from bccvid import *
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
from matplotlib.patches import Wedge
from bcc_gr_emergence import BCCGREmergenceSim

OUT = "/workspace/bcc_test4_videos/v5/gr_emergence"
RADII = [20.0, 10.0, 6.0, 4.0, 3.0]  # outer to inner, as on screen
NODE_CAP, R_S = 100.0, 3.0
A_ORB, E_ORB = 1200.0, 0.5
EXAG = 15  # visual-only exaggeration of the perihelion advance
TAU_REV = 8.0  # seconds of proper time for one clock revolution
N_ORBITS = 7

sim = BCCGREmergenceSim(node_cap=NODE_CAP, r_s=R_S)
CLOCKS = sim.time_dilation_profile(RADII)
PREC = sim.perihelion_precession(semi_major_a=A_ORB, eccentricity=E_ORB)

assert [(c["r"], c["workload"], c["grid_dtau_dt"], c["gr_dtau_dt"], c["status"]) for c in CLOCKS] == [
    (20.0, 15.0, 0.921954, 0.921954, "Active Clock"),
    (10.0, 30.0, 0.836660, 0.836660, "Active Clock"),
    (6.0, 50.0, 0.707107, 0.707107, "Active Clock"),
    (4.0, 75.0, 0.500000, 0.500000, "Active Clock"),
    (3.0, 100.0, 0.000000, 0.000000, "DEADLOCKED Horizon (0 escape)"),
]
assert PREC["a"] == A_ORB and PREC["e"] == E_ORB and PREC["r_s"] == R_S
assert PREC["grid_advance_rad"] == 0.031657
assert PREC["gr_advance_rad"] == 0.031416
assert PREC["rel_error_pct"] == 0.767

# Keplerian samples for a smooth rosette (grid advance, exaggerated for display)
P_LATUS = A_ORB * (1.0 - E_ORB ** 2)
N_SAMP = 720 * N_ORBITS


def rosette_xy(n_orbits, exag, n_samp=N_SAMP):
    """Return x,y of a precessing ellipse; periapsis advances by exag * grid Delta phi per orbit."""
    mean = np.linspace(0.0, 2 * np.pi * n_orbits, n_samp, endpoint=False)
    # solve Kepler's equation E - e sin E = M
    E = mean.copy()
    for _ in range(8):
        E -= (E - E_ORB * np.sin(E) - mean) / (1.0 - E_ORB * np.cos(E))
    theta = 2.0 * np.arctan2(np.sqrt(1 + E_ORB) * np.sin(E / 2.0),
                             np.sqrt(1 - E_ORB) * np.cos(E / 2.0))
    r = P_LATUS / (1.0 + E_ORB * np.cos(theta))
    peri = (mean / (2.0 * np.pi)) * (exag * PREC["grid_advance_rad"])
    ang = theta + peri
    return r * np.cos(ang), r * np.sin(ang), r, mean


XS_FULL, YS_FULL, RS_FULL, MEAN_FULL = rosette_xy(N_ORBITS, EXAG)


def title_scene(fig, t, T):
    ax = fig.add_axes([0.04, 0.16, 0.92, 0.72])
    ax.set_facecolor(BG)
    ax.set_xlim(0, 15)
    ax.set_ylim(0.4, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")
    a = 0.22 * ramp(t, 0.1, 0.8)
    xs = [1.5, 4.5, 7.5, 10.5, 13.5]
    for i, (x, row) in enumerate(zip(xs, CLOCKS)):
        stopped = row["grid_dtau_dt"] == 0.0
        col = RED if stopped else CYAN
        ax.add_patch(Circle((x, 2.55), 1.05, fc=PANEL, ec=col, lw=2.0, alpha=a))
        for k in range(12):
            ang = math.radians(90 - k * 30)
            c, s = math.cos(ang), math.sin(ang)
            ax.plot([x + 0.84 * 1.05 * c, x + 0.97 * 1.05 * c],
                    [2.55 + 0.84 * 1.05 * s, 2.55 + 0.97 * 1.05 * s],
                    color=DIM, lw=1.2, alpha=a)
    ta = ramp(t, 0.2, 0.55)
    fig.text(0.5, 0.58, "Weak-field GR on the lattice (toy model)", fontsize=48, weight="bold",
             ha="center", va="center", alpha=ta,
             bbox=dict(boxstyle="round,pad=0.35", fc="#0b0d13", ec="none", alpha=0.70 * ta))
    fig.text(0.5, 0.455, "Time dilation and perihelion precession on a 6-face lattice",
             fontsize=24, color=DIM, ha="center", va="center", alpha=ramp(t, 0.6, 0.55))


def _draw_clock(ax, x, y, R, tau, row, alpha=1.0):
    stopped = row["grid_dtau_dt"] == 0.0
    col = RED if stopped else CYAN
    ax.add_patch(Circle((x, y), R, fc=PANEL, ec=col, lw=2.4, alpha=alpha, zorder=3))
    ax.add_patch(Circle((x, y), R * 0.96, fc=PANEL, ec="none", alpha=alpha, zorder=3))
    for k in range(12):
        ang = math.radians(90 - k * 30)
        c, s = math.cos(ang), math.sin(ang)
        lw = 2.2 if k % 3 == 0 else 1.2
        ax.plot([x + 0.80 * R * c, x + 0.95 * R * c],
                [y + 0.80 * R * s, y + 0.95 * R * s],
                color=DIM, lw=lw, alpha=alpha, zorder=4, solid_capstyle="round")
    ang = math.radians(90 - 360.0 * (tau / TAU_REV))
    hc, hs = math.cos(ang), math.sin(ang)
    hand_c = RED if stopped else YELLOW
    ax.plot([x, x + 0.72 * R * hc], [y, y + 0.72 * R * hs],
            color=hand_c, lw=3.4, alpha=alpha, zorder=5, solid_capstyle="round")
    ax.plot(x, y, "o", color=FG, ms=5, alpha=alpha, zorder=6)
    if stopped:
        # freeze mark: a short cross through the hub
        ax.plot([x - 0.12 * R, x + 0.12 * R], [y, y], color=RED, lw=1.4, alpha=0.8 * alpha, zorder=6)


def p_clocks(fig, t, T):
    ax = fig.add_axes([0.03, 0.14, 0.94, 0.74])
    ax.set_facecolor(BG)
    ax.set_xlim(0, 15)
    ax.set_ylim(-1.15, 4.55)
    ax.set_aspect("equal")
    ax.axis("off")
    t_coord = max(0.0, t - 0.35)
    xs = [1.5, 4.5, 7.5, 10.5, 13.5]
    y, R = 2.15, 1.18
    for x, row in zip(xs, CLOCKS):
        rate = row["grid_dtau_dt"]
        tau = rate * t_coord  # stays 0 for the deadlocked clock
        _draw_clock(ax, x, y, R, tau, row)
        col = RED if rate == 0.0 else FG
        ax.text(x, y + R + 0.42, f"r = {row['r']:.0f}", ha="center", va="bottom",
                fontsize=20, color=col, weight="bold")
        ax.text(x, y - R - 0.28, f"dτ/dt = {row['grid_dtau_dt']:.6f}",
                ha="center", va="top", fontsize=14, color=CYAN if rate else RED)
        ax.text(x, y - R - 0.68, f"W = {row['workload']:.2f}",
                ha="center", va="top", fontsize=14, color=DIM)
        if rate == 0.0:
            ax.text(x, y - R - 1.12, "DEADLOCKED", ha="center", va="top",
                    fontsize=13, color=RED, weight="bold")
            ax.text(x, y - R - 1.46, "100-tick cap", ha="center", va="top",
                    fontsize=12, color=YELLOW)
    fig.text(0.97, 0.86, f"t = {t_coord:.2f} s", fontsize=16, color=DIM, ha="right", va="center")
    fig.text(0.50, 0.86, r"d$\tau$/dt = $\sqrt{1 - W/C}$    with    $W = C \cdot r_s / r$"
             "    (same as Schwarzschild, by construction)",
             fontsize=14, color=DIM, ha="center", va="center")


def p_orbit(fig, t, T):
    ax = style_ax(fig.add_axes([0.05, 0.16, 0.62, 0.70]), grid=False)
    ax.set_aspect("equal")
    # trail grows with eased orbit count
    g = ease(max(0.0, min(1.0, (t - 0.3) / 11.6)))
    n = max(2, int(g * len(XS_FULL)))
    ax.plot(XS_FULL[:n], YS_FULL[:n], color=CYAN, lw=1.6, alpha=0.9, zorder=3)
    # current position
    ax.plot(XS_FULL[n - 1], YS_FULL[n - 1], "o", ms=11, color=YELLOW, mec=FG, zorder=5)
    # central congestion core (r_s = 3 is tiny vs a=1200; marker is schematic)
    ax.add_patch(Circle((0, 0), 70, fc="#4a1d24", ec=RED, lw=1.2, alpha=0.95, zorder=4))
    ax.add_patch(Circle((0, 0), 28, fc=RED, ec="none", alpha=0.9, zorder=4))
    lim = 2000
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim * 0.72, lim * 0.72)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("precessing orbit  (a = 1200,  e = 0.50,  r_s = 3)", fontsize=16, color=DIM, pad=8)
    # exaggeration callout on the plot
    ax.text(0.50, 0.06, "precession exaggerated  ×15  for display",
            transform=ax.transAxes, ha="center", va="center", fontsize=15, color=ORANGE,
            bbox=dict(boxstyle="round,pad=0.3", fc="#0b0d13", ec=ORANGE, lw=1.0, alpha=0.85))

    # numbers panel
    fig.text(0.84, 0.72, "per orbit", fontsize=16, color=DIM, ha="center")
    fig.text(0.84, 0.64, "grid  0.031657 rad", fontsize=22, color=CYAN, ha="center", weight="bold")
    fig.text(0.84, 0.57, "GR    0.031416 rad", fontsize=22, color=FG, ha="center")
    fig.text(0.84, 0.49, "diff  0.767%", fontsize=22, color=YELLOW, ha="center", weight="bold")
    fig.text(0.84, 0.38, r"$\Delta\phi = 3\pi r_s / [a(1-e^2)]$",
             fontsize=15, color=DIM, ha="center")
    n_orb = g * N_ORBITS
    fig.text(0.84, 0.28, f"orbit  {n_orb:.1f}  /  {N_ORBITS}",
             fontsize=16, color=DIM, ha="center")


v = Video(OUT, "_silent", "bcc_test4 · bcc_gr_emergence.py",
          "Toy model on a 6-face cubic grid · numbers from the actual run of bcc_gr_emergence.py")
v.add(4.5, title_scene)

v.add(14.0, p_clocks, [(0.3, "Clocks tick at dτ/dt = √(1 − W/C)"),
                       (6.0, "At r = 3, W hits the 100-tick cap  ·  the clock stops")],
      "1 · Time dilation")

v.add(13.5, p_orbit, [(0.3, "A precessing ellipse traces a rosette  (advance exaggerated ×15)"),
                      (7.0, "Grid 0.031657 rad/orbit  vs  GR 0.031416  (0.767% diff)")],
      "2 · Perihelion precession")

v.add(6.0, end_card([
    (r"Workload is set to  $W = C \cdot r_s / r$, so it reproduces GR's numbers", ORANGE),
    ("Emergence on the full grid is still to be tested", YELLOW),
], head="Toy model"))


def timeline():
    sc = scene_starts(v); a = [x["start"] for x in sc]
    # proper-time click times for each active clock (every 1 s of tau)
    clicks = []
    clock_start = a[1] + 0.35
    clock_end = a[2]
    for i, row in enumerate(CLOCKS):
        rate = row["grid_dtau_dt"]
        if rate <= 0:
            continue
        tau = 1.0
        while True:
            tt = clock_start + tau / rate
            if tt >= clock_end - 0.05:
                break
            clicks.append({"t": tt, "i": i, "rate": rate})
            tau += 1.0
    peri = []
    orb0 = a[2] + 0.3
    orb_dur = 11.6
    for k in range(1, N_ORBITS + 1):
        # ease-inverse is awkward; periapsis at orbit boundaries in eased time
        frac = k / N_ORBITS
        # invert cubic smoothstep x^2(3-2x); endpoints are exact (deriv vanishes there)
        if frac <= 0:
            x = 0.0
        elif frac >= 1:
            x = 1.0
        else:
            x = frac
            for _ in range(10):
                x -= (x * x * (3 - 2 * x) - frac) / (6 * x * (1 - x))
        peri.append(orb0 + orb_dur * x)
    return {
        "total": v.duration,
        "scenes": sc,
        "title": [0, a[1]],
        "clocks": [a[1], a[2]],
        "clock_start": clock_start,
        "deadlock": a[1] + 6.0,
        "clicks": clicks,
        "orbit": [a[2], a[3]],
        "peri": peri,
        "prec_ann": a[2] + 7.0,
        "end": a[3],
    }


if __name__ == "__main__":
    assert abs(v.duration - 38.0) < 1e-9, v.duration
    finish(v, "bcc_gr_emergence", timeline(), os.path.join(OUT, "sfx_bcc_gr_emergence.py"),
           thumb_t=4.5 + 14.0 + 12.2, audio_only="--audio-only" in sys.argv)
