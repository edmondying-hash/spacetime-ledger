#!/usr/bin/env python3
"""Render OP2 star-collapse storyboard v2: balanced 8-direction inward inflow.

Preserves approved 38s board/captions. No audio. Writes op2_collapse_v2.mp4 beside this script by default.
Release package ships the reviewed MP4; re-run only to regenerate. v2b: 8-dir balanced inward; single monotonic bead/track (no wrap/trains).
Edmond/videoReview: unmistakable inward motion.
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from matplotlib.collections import PatchCollection, LineCollection

# Portable: all outputs next to this script (or CWD override via OP2_OUT)
OUT = Path(__file__).resolve().parent
if __import__("os").environ.get("OP2_OUT"):
    OUT = Path(__import__("os").environ["OP2_OUT"]).resolve()
FRAMES = OUT / "frames_v2"
QA = OUT / "qa_stills_v2"
MP4 = OUT / "op2_collapse_v2.mp4"

DPI = 100
W_IN, H_IN = 19.20, 10.80
FPS = 30
DURATION = 38.0
N_FRAMES = int(DURATION * FPS)  # 1140

BG = "#0b0e14"
W = "#e8eef7"
MUTED = "#9aa3b5"
CYAN = "#3ec7e0"
CYAN_DIM = "#1a5a6a"
GOLD = "#e6b84d"
GOLD_HOT = "#ffd27a"

CORNER = "Illustration of a proposed model."
FRAME_L1 = "Illustrative visualization of the"
FRAME_L2 = "Quantized Space-Ledger toy model"

N_A, RHO_A = 141, 1.93
N_B, RHO_B = 3853, 8.1
N_COLLAPSE = 4738
N_C, RHO_C = 46127, 5500

MIN_PT = 28
TITLE_PT = 36
FRAME_PT = 28
CAP1_PT = 32
CAP2_PT = 28
CORNER_PT = 28

Y_CAP1 = 0.11
Y_CAP2 = 0.055
Y_ART_BOTTOM = 0.18
Y_ART_TOP = 0.76

# Approved scene table (id, t0, t1, title, caps)
SCENES = [
    (1, 0.0, 5.0, "Setup", [
        "Radial-shell Pauli packing  ·  G = 0.01 (model units)",
        "Motion and timing are illustrative, not measured collapse dynamics.",
    ]),
    (2, 5.0, 12.0, "Supported lump", [
        f"N = {N_A}   ·   half-mass density ≈ {RHO_A}",
        "Finite lump held by Pauli packing. Blast-spill sets outer extent.",
    ]),
    (3, 12.0, 19.0, "Add mass", [
        f"Mass added  →  N = {N_B}   ·   half-mass density ≈ {RHO_B}",
        "Core denser (~4×). Different mass states, not a time series.",
    ]),
    (4, 19.0, 25.0, "Support cap", [
        f"Mass added  →  N ≈ {N_COLLAPSE}",
        "Chosen support cap exceeded.",
    ]),
    (5, 25.0, 33.0, "Inward collapse", [
        "Core falls to the grid floor. Halo stays extended.",
        "Illustrative inward pile-up.",
    ]),
    (6, 33.0, 38.0, "After collapse", [
        f"Mass added  →  N ≈ {N_C:,}   ·   half-mass density ≈ {RHO_C:,}",
        "Toy model—not a stellar simulation.",
    ]),
]

# Key radii from verified data (display scaled for framing)
# A: R_half≈2.06 R_out=3; B: 3.85/8; threshold onset then floor; C: 1/18
STATE = {
    "A": dict(r_core=2.10, r_out=3.00, dens=0.55, collapse=False),
    "B": dict(r_core=3.60, r_out=7.20, dens=0.85, collapse=False),
    "T": dict(r_core=3.20, r_out=6.50, dens=1.05, collapse=False),  # near threshold
    "F": dict(r_core=0.95, r_out=7.50, dens=1.60, collapse=True),   # floor mid-collapse
    "C": dict(r_core=0.90, r_out=9.00, dens=1.90, collapse=True),
}


def smoothstep(x: float) -> float:
    x = float(np.clip(x, 0.0, 1.0))
    return x * x * (3.0 - 2.0 * x)


def lerp(a, b, t):
    return a + (b - a) * t


def scene_at(t: float):
    for sid, t0, t1, title, caps in SCENES:
        if t < t1 or sid == 6:
            local = (t - t0) / max(t1 - t0, 1e-9)
            return sid, t0, t1, title, caps, float(np.clip(local, 0.0, 1.0))
    sid, t0, t1, title, caps = SCENES[-1]
    return sid, t0, t1, title, caps, 1.0


def visual_state(t: float):
    """Illustrative interpolated visual parameters across approved beats."""
    sid, t0, t1, title, caps, u = scene_at(t)

    if sid == 1:
        # Quiet packing settle into A
        s = smoothstep(u)
        st = STATE["A"].copy()
        st["dens"] = lerp(0.35, STATE["A"]["dens"], s)
        st["r_core"] = lerp(1.2, STATE["A"]["r_core"], s)
        st["r_out"] = lerp(2.2, STATE["A"]["r_out"], s)
        st["mode"] = "pack"
        st["inflow"] = 0.0
        st["inward"] = 0.0
        st["cap"] = 0.0
        st["tension"] = 0.0
    elif sid == 2:
        st = STATE["A"].copy()
        st["mode"] = "pack"
        st["inflow"] = 0.0
        st["inward"] = 0.0
        st["cap"] = 0.0
        st["tension"] = 0.05 * math.sin(2 * math.pi * u * 2.0) ** 2
        # gentle packing pulse
        pulse = 1.0 + 0.04 * math.sin(2 * math.pi * (t - t0) * 0.85)
        st["dens"] *= pulse
    elif sid == 3:
        # A → B with visible mass addition
        s = smoothstep(u)
        st = {}
        for k in ("r_core", "r_out", "dens"):
            st[k] = lerp(STATE["A"][k], STATE["B"][k], s)
        st["collapse"] = False
        st["mode"] = "add"
        st["inflow"] = 1.0
        st["inward"] = 0.0
        st["cap"] = 0.0
        st["tension"] = 0.15 * s
    elif sid == 4:
        # B → threshold; rising tension; cap exceeded late in scene
        s = smoothstep(u)
        st = {}
        for k in ("r_core", "r_out", "dens"):
            st[k] = lerp(STATE["B"][k], STATE["T"][k], s)
        st["collapse"] = False
        st["mode"] = "add"
        st["inflow"] = 1.0
        st["inward"] = 0.10 * s
        st["cap"] = smoothstep((u - 0.35) / 0.65)
        st["tension"] = 0.25 + 0.75 * s
    elif sid == 5:
        # Dramatic inward collapse to lattice floor; halo stays
        s = smoothstep(u)
        st = {}
        st["r_core"] = lerp(STATE["T"]["r_core"], STATE["F"]["r_core"], s)
        # halo remains extended (do not shrink R_out with core)
        st["r_out"] = lerp(STATE["T"]["r_out"], STATE["F"]["r_out"], smoothstep(u * 0.6))
        st["dens"] = lerp(STATE["T"]["dens"], STATE["F"]["dens"], s)
        st["collapse"] = True
        st["mode"] = "collapse"
        st["inflow"] = 0.0
        st["inward"] = 0.35 + 0.65 * s
        st["cap"] = 1.0
        st["tension"] = 1.0
    else:
        # After: more mass added; core at floor, denser; halo larger
        s = smoothstep(u)
        st = {}
        st["r_core"] = lerp(STATE["F"]["r_core"], STATE["C"]["r_core"], s)
        st["r_out"] = lerp(STATE["F"]["r_out"], STATE["C"]["r_out"], s)
        st["dens"] = lerp(STATE["F"]["dens"], STATE["C"]["dens"], s)
        st["collapse"] = True
        st["mode"] = "add"
        st["inflow"] = 1.0
        st["inward"] = 0.15
        st["cap"] = 0.0
        st["tension"] = 0.4
    st["title"] = title
    st["caps"] = caps
    st["sid"] = sid
    st["u"] = u
    st["t"] = t
    return st


def node_lattice(r_out: float):
    step = max(0.55, r_out / 10.5)
    s = step * 0.62
    xs = np.arange(-r_out - step, r_out + step + 0.01, step)
    ys = np.arange(-r_out - step, r_out + step + 0.01, step)
    X, Y = np.meshgrid(xs, ys)
    return X.ravel(), Y.ravel(), step, s


def rgba_for_heat(heat: float, collapse: bool, r: float, r_core: float):
    if heat < 0.35:
        rgb = plt.matplotlib.colors.to_rgb(CYAN_DIM)
        a = 0.55 + 0.30 * heat
    elif heat < 0.70:
        rgb = plt.matplotlib.colors.to_rgb(CYAN)
        a = 0.80
    else:
        g = GOLD_HOT if (collapse and r < r_core * 0.75) else GOLD
        rgb = plt.matplotlib.colors.to_rgb(g)
        a = min(0.96, 0.55 + 0.42 * heat)
    return (*rgb, a)


def draw_chrome(ax, title, caps):
    ax.text(0.02, 0.990, CORNER, transform=ax.transAxes, color=MUTED,
            fontsize=CORNER_PT, va="top", ha="left")
    ax.text(0.50, 0.935, FRAME_L1, transform=ax.transAxes, color=GOLD,
            fontsize=FRAME_PT, va="top", ha="center")
    ax.text(0.50, 0.888, FRAME_L2, transform=ax.transAxes, color=GOLD,
            fontsize=FRAME_PT, va="top", ha="center", weight="bold")
    ax.text(0.50, 0.835, title, transform=ax.transAxes, color=W,
            fontsize=TITLE_PT, va="top", ha="center", weight="bold")
    ax.axhline(Y_ART_TOP, color="#1c2430", lw=1.0, xmin=0.04, xmax=0.96)
    ax.axhline(Y_ART_BOTTOM, color="#1c2430", lw=1.0, xmin=0.04, xmax=0.96)
    ax.text(0.50, Y_CAP1, caps[0], transform=ax.transAxes, color=GOLD,
            fontsize=CAP1_PT, va="center", ha="center", weight="bold")
    if len(caps) > 1:
        ax.text(0.50, Y_CAP2, caps[1], transform=ax.transAxes, color=MUTED,
                fontsize=CAP2_PT, va="center", ha="center")


def art_axes(fig):
    left, right = 0.06, 0.94
    bottom, top = Y_ART_BOTTOM, Y_ART_TOP - 0.02
    ax = fig.add_axes([left, bottom, right - left, top - bottom])
    ax.set_facecolor(BG)
    ax.set_aspect("equal")
    ax.axis("off")
    return ax


def draw_lump(ax, st, phase: float):
    r_core = st["r_core"]
    r_out = st["r_out"]
    dens = st["dens"]
    collapse = st["collapse"]
    inward = st["inward"]
    tension = st["tension"]

    # Square data limits so 8-dir inflow fits without vertical clipping
    pad = r_out * 1.35 + 0.8
    ax.set_xlim(-pad, pad)
    ax.set_ylim(-pad, pad)

    xs, ys, step, s = node_lattice(r_out)
    # packing shimmer / congestion: slight radial jitter for supported scenes
    if st["mode"] == "pack":
        jitter = 0.035 * step * np.sin(phase * 2.2 + xs * 1.7 + ys * 1.1)
        xs = xs + jitter * (ys / (np.abs(ys) + 0.2)) * 0.15
        ys = ys + jitter * 0.4

    # inward advection of non-halo nodes during collapse (illustrative)
    r = np.hypot(xs, ys)
    if inward > 0:
        # move mid-shell nodes inward; keep outermost halo nearly fixed
        halo = r > (0.82 * r_out)
        pull = inward * 0.55 * (1.0 - np.clip(r / max(r_out, 1e-6), 0, 1))
        # time-varying pull so motion is visible within the scene
        pull = pull * (0.65 + 0.35 * math.sin(phase * 3.0))
        scale = np.where(halo, 1.0, np.clip(1.0 - pull, 0.08, 1.0))
        xs = xs * scale
        ys = ys * scale
        r = np.hypot(xs, ys)

    patches, colors = [], []
    for x, y, rr in zip(xs, ys, r):
        if rr > r_out + step * 0.35:
            continue
        if rr <= r_core:
            tt = 1.0 - 0.30 * (rr / max(r_core, 1e-6))
            heat = min(1.0, dens * tt)
            # tension brightens core
            heat = min(1.0, heat + 0.18 * tension * (1.0 - rr / max(r_core, 1e-6)))
        else:
            heat = 0.20 + 0.04 * tension
        patches.append(Rectangle((x - s / 2, y - s / 2), s, s))
        colors.append(rgba_for_heat(heat, collapse, rr, r_core))

    if patches:
        ax.add_collection(PatchCollection(
            patches, facecolors=colors, edgecolors="#0b0e14",
            linewidths=0.30, zorder=2))

    ax.add_patch(Circle((0, 0), r_out, fill=False, edgecolor=CYAN, lw=2.0,
                        alpha=0.55, linestyle="--", zorder=3))
    ax.add_patch(Circle((0, 0), max(r_core, 0.35), fill=False, edgecolor=GOLD,
                        lw=2.2, alpha=0.90, zorder=3))

    if st["cap"] > 0.05:
        ax.add_patch(Circle((0, 0), 1.15, fill=False, edgecolor=GOLD_HOT,
                            lw=2.0 + 2.0 * st["cap"],
                            alpha=0.35 + 0.65 * st["cap"], zorder=6))


def ease_inout(x: float) -> float:
    x = float(np.clip(x, 0.0, 1.0))
    return x * x * (3.0 - 2.0 * x)


def draw_inflow(ax, st, phase: float):
    """Balanced inward mass addition from 8 directions — NO wrap/reset.

    One bright square per track: starts outer at scene begin, moves
    monotonically inward, fades/absorbs at core near scene end.
    Short fading tail (larger r only) may trail behind; never outward travel.
    """
    if st["inflow"] <= 0.01:
        return
    sid = st["sid"]
    u = float(st["u"])
    # Fixed endpoints: always r_start > r_end so progress is unambiguously inward.
    # Absorb near the bright core center (not the growing R_half ring).
    if sid == 3:  # Add mass A→B
        r_start = STATE["B"]["r_out"] * 1.12
        r_end = 1.40
    elif sid == 4:  # Support cap B→threshold
        r_start = STATE["B"]["r_out"] * 1.12
        r_end = 1.35
    elif sid == 6:  # After collapse — more mass
        r_start = STATE["C"]["r_out"] * 1.08
        r_end = 1.30
    else:
        return
    assert r_start > r_end

    # Monotonic progress across scene; brief hold, then absorb/fade at end
    if u <= 0.04:
        p = 0.0
        fade = 1.0
    elif u >= 0.92:
        p = 1.0
        fade = float(np.clip(1.0 - (u - 0.92) / 0.08, 0.0, 1.0))
    else:
        p = ease_inout((u - 0.04) / 0.88)
        fade = 1.0

    rr = lerp(r_start, r_end, p)  # decreases as p increases (r_start > r_end)
    n_dir = 8
    # Static inward guide arrows (all 8); tips near absorption radius
    for i in range(n_dir):
        ang = i * (2.0 * math.pi / n_dir) + 0.20
        x0, y0 = r_start * math.cos(ang), r_start * math.sin(ang)
        x1, y1 = r_end * math.cos(ang), r_end * math.sin(ang)
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.6,
                                    mutation_scale=13, alpha=0.55 * fade),
                    zorder=5)

        # Short inward-pointing tail BEHIND bead (larger radius only)
        span = max(r_start - r_end, 1e-6)
        for k in (3, 2, 1):
            r_tail = rr + k * 0.22 * span / 3.0
            if r_tail > r_start:
                continue
            xt, yt = r_tail * math.cos(ang), r_tail * math.sin(ang)
            s = 0.22
            ax.add_patch(Rectangle((xt - s / 2, yt - s / 2), s, s,
                                   facecolor=GOLD, edgecolor="none",
                                   alpha=0.18 * fade * (1.0 - 0.25 * k),
                                   zorder=6))

        # Single distinct bright square — the moving mass packet
        xb, yb = rr * math.cos(ang), rr * math.sin(ang)
        s = 0.42
        ax.add_patch(Rectangle((xb - s / 2, yb - s / 2), s, s,
                               facecolor=GOLD_HOT, edgecolor=GOLD,
                               linewidth=1.0, alpha=0.95 * fade, zorder=7))


def draw_inward_arrows(ax, st, phase: float):
    """Collapse: 8-direction inward convergence from all sides; never outward."""
    if st["inward"] < 0.2 or st["mode"] != "collapse":
        return
    r_out = st["r_out"]
    r_core = st["r_core"]
    pulse = 0.75 + 0.25 * math.sin(phase * 4.0)
    n_dir = 8
    for i in range(n_dir):
        ang = i * (2.0 * math.pi / n_dir)
        x0 = r_out * 0.72 * math.cos(ang)
        y0 = r_out * 0.72 * math.sin(ang)
        x1 = (r_core + 0.7) * math.cos(ang)
        y1 = (r_core + 0.7) * math.sin(ang)
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color=GOLD_HOT,
                                    lw=2.0 + 0.8 * st["inward"],
                                    mutation_scale=14 + 4 * pulse,
                                    alpha=0.55 + 0.45 * st["inward"]),
                    zorder=5)


def render_frame(t: float, path: Path):
    st = visual_state(t)
    phase = t * 2.0 * math.pi  # generic phase

    fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI, facecolor=BG)
    ax_txt = fig.add_axes([0, 0, 1, 1])
    ax_txt.set_facecolor(BG)
    ax_txt.set_xlim(0, 1)
    ax_txt.set_ylim(0, 1)
    ax_txt.axis("off")
    draw_chrome(ax_txt, st["title"], st["caps"])

    ax = art_axes(fig)
    draw_lump(ax, st, phase)
    draw_inflow(ax, st, phase)
    draw_inward_arrows(ax, st, phase)

    fig.savefig(path, dpi=DPI, facecolor=BG)
    plt.close(fig)


def encode_mp4(frame_pattern: str, out_mp4: Path):
    # silent H264 yuv420p 30fps
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", frame_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-profile:v", "high",
        "-crf", "18",
        "-movflags", "+faststart",
        "-an",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True)


def _render_one(i: int):
    t = i / FPS
    path = FRAMES / f"frame_{i:05d}.png"
    render_frame(t, path)
    return i


def main():
    from concurrent.futures import ProcessPoolExecutor, as_completed
    import os as _os

    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)

    workers = max(1, min(8, (_os.cpu_count() or 4)))
    print(f"Rendering {N_FRAMES} frames ({DURATION}s @ {FPS}fps) with {workers} workers…")

    done = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_render_one, i) for i in range(N_FRAMES)]
        for fut in as_completed(futs):
            fut.result()
            done += 1
            if done % 120 == 0 or done == N_FRAMES:
                print(f"  {done}/{N_FRAMES}")

    qa_times = {1: 2.5, 2: 8.5, 3: 15.5, 4: 22.0, 5: 29.0, 6: 35.5}
    for sid, tq in qa_times.items():
        idx = int(round(tq * FPS))
        idx = min(max(idx, 0), N_FRAMES - 1)
        qpath = QA / f"qa_f{sid}.png"
        shutil.copy(FRAMES / f"frame_{idx:05d}.png", qpath)
        print("QA", qpath)

    print("Encoding", MP4)
    encode_mp4(str(FRAMES / "frame_%05d.png"), MP4)
    print("done", MP4)


if __name__ == "__main__":
    main()
