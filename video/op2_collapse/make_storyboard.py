"""OP2 star-collapse storyboard stills + PDF.

Records the approved board (layout and captions). Does not render the release
MP4; that file is op2_collapse_v2.mp4 from render_op2_v2.py.
Layout: 1920x1080, all on-screen text >= 38 px, separated header / art / caption bands.
"""
from __future__ import annotations

import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.collections import PatchCollection

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

# Display size: 1920x1080 at 100 dpi figure → exact pixel canvas
DPI = 100
W_IN, H_IN = 19.20, 10.80  # inches → 1920x1080 at 100 dpi

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

# Verified G=0.01 (model units)
N_A, RHO_A = 141, 1.93
N_B, RHO_B = 3853, 8.1
N_COLLAPSE = 4738
N_C, RHO_C = 46127, 5500  # display rounding of 5506
G = 0.01

# Scene captions: 1–2 short lines. Details live on PDF notes page.
# (id, t0, t1, title, captions[1..2], show_g_badge)
SCENES = [
    (1, 0, 5, "Setup", [
        "Radial-shell Pauli packing  ·  G = 0.01 (model units)",
        "Motion and timing are illustrative, not measured collapse dynamics.",
    ], False),
    (2, 5, 12, "Supported lump", [
        f"N = {N_A}   ·   half-mass density ≈ {RHO_A}",
        "Finite lump held by Pauli packing. Blast-spill sets outer extent.",
    ], True),
    (3, 12, 19, "Add mass", [
        f"Mass added  →  N = {N_B}   ·   half-mass density ≈ {RHO_B}",
        "Core denser (~4×). Different mass states, not a time series.",
    ], True),
    (4, 19, 25, "Support cap", [
        f"Mass added  →  N ≈ {N_COLLAPSE}",
        "Chosen support cap exceeded.",
    ], True),
    (5, 25, 33, "Inward collapse", [
        "Core falls to the grid floor. Halo stays extended.",
        "Illustrative inward pile-up.",
    ], True),
    (6, 33, 38, "After collapse", [
        f"Mass added  →  N ≈ {N_C:,}   ·   half-mass density ≈ {RHO_C:,}",
        "Toy model—not a stellar simulation.",
    ], True),
]

# Layout bands in axes fraction (y from bottom)
# Footer tiny source line optional — keep clear of captions
Y_CAP1 = 0.11          # primary caption baseline
Y_CAP2 = 0.055         # secondary caption
Y_ART_BOTTOM = 0.18    # illustration area starts above captions
Y_ART_TOP = 0.76       # illustration area ends below header
Y_TITLE = 0.90
Y_FRAME1 = 0.955
Y_FRAME2 = 0.915
# Corner sits LEFT of title band, below frame lines to avoid collision
Y_CORNER = 0.84
X_CORNER = 0.018


def new_fig():
    fig, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=DPI, facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("auto")
    ax.axis("off")
    # clip art into a dedicated axes inset
    return fig, ax


def draw_chrome(ax, title, show_frame=True):
    """Persistent header chrome: framing (2 lines) + title + corner (no collision)."""
    if show_frame:
        ax.text(0.50, Y_FRAME1, FRAME_L1, transform=ax.transAxes, color=GOLD,
                fontsize=16, va="top", ha="center")  # 16 pt @100dpi ≈ 21px — TOO SMALL
    # NOTE: matplotlib fontsize is in points. At 100 dpi, 1 pt ≈ 1.333 px.
    # Requirement: >= 38 px → fontsize >= 38 / (DPI/72) = 38 * 72/100 = 27.36 pt
    # Use fontsize=28 for minimum (~38.9 px at 100 dpi), larger for titles.


# Recalculate: matplotlib fontsize is in points; pixels = pt * dpi / 72
# For dpi=100: px = pt * 100/72 ≈ pt * 1.389 → need pt >= 38/1.389 ≈ 27.36
# Use MIN_PT = 28 (≥38.9 px). Titles larger.

MIN_PT = 28          # ≥ ~39 px at 100 dpi
TITLE_PT = 36        # ~50 px
FRAME_PT = 28        # ≥ 38 px
CAP1_PT = 32         # ~44 px
CAP2_PT = 28         # ≥ 38 px
CORNER_PT = 28       # ≥ 38 px — was tiny before; keep readable, place carefully


def draw_chrome(ax, title, show_frame=True):
    # Row 1 (own row): persistent corner — left only, nothing centered on this row
    ax.text(0.02, 0.990, CORNER, transform=ax.transAxes, color=MUTED,
            fontsize=CORNER_PT, va="top", ha="left")
    # Rows 2–3: gold framing, centered (always explicit toy-model marking)
    if show_frame:
        ax.text(0.50, 0.935, FRAME_L1, transform=ax.transAxes, color=GOLD,
                fontsize=FRAME_PT, va="top", ha="center")
        ax.text(0.50, 0.888, FRAME_L2, transform=ax.transAxes, color=GOLD,
                fontsize=FRAME_PT, va="top", ha="center", weight="bold")
    # Row 4: scene title, centered — clear of corner and framing
    ax.text(0.50, 0.835, title, transform=ax.transAxes, color=W,
            fontsize=TITLE_PT, va="top", ha="center", weight="bold")


def draw_captions(ax, caps):
    """1–2 caption lines in dedicated bottom band. Never overlaps art."""
    assert 1 <= len(caps) <= 2
    ax.text(0.50, Y_CAP1, caps[0], transform=ax.transAxes, color=GOLD,
            fontsize=CAP1_PT, va="center", ha="center", weight="bold")
    if len(caps) > 1:
        ax.text(0.50, Y_CAP2, caps[1], transform=ax.transAxes, color=MUTED,
                fontsize=CAP2_PT, va="center", ha="center")


def art_axes(fig):
    """Dedicated illustration axes between header and caption bands."""
    # [left, bottom, width, height] in figure fraction
    # Leave left/right margins; art vertically between Y_ART_BOTTOM and Y_ART_TOP
    left, right = 0.06, 0.94
    bottom, top = Y_ART_BOTTOM, Y_ART_TOP - 0.02
    ax = fig.add_axes([left, bottom, right - left, top - bottom])
    ax.set_facecolor(BG)
    ax.set_aspect("equal")
    ax.axis("off")
    return ax


def draw_radial_lump(ax, r_core, r_out, density_core=1.0, collapse=False,
                     label_rings=False):
    """Schematic radial shells of square nodes. No tiny radius labels by default."""
    # Fit lump in view
    pad = r_out * 1.25 + 0.8
    ax.set_xlim(-pad, pad)
    ax.set_ylim(-pad * 0.72, pad * 0.72)

    step = max(0.55, r_out / 10.5)
    s = step * 0.62
    xs = np.arange(-r_out - step, r_out + step + 0.01, step)
    ys = np.arange(-r_out - step, r_out + step + 0.01, step)
    patches, colors = [], []
    for x in xs:
        for y in ys:
            r = math.hypot(x, y)
            if r > r_out + step * 0.35:
                continue
            if r <= r_core:
                t = 1.0 - 0.30 * (r / max(r_core, 1e-6))
                heat = min(1.0, density_core * t)
            else:
                heat = 0.22  # thin halo
            if heat < 0.35:
                c = (*plt.matplotlib.colors.to_rgb(CYAN_DIM), 0.60 + 0.25 * heat)
            elif heat < 0.70:
                c = (*plt.matplotlib.colors.to_rgb(CYAN), 0.80)
            else:
                g = GOLD_HOT if (collapse and r < r_core * 0.7) else GOLD
                c = (*plt.matplotlib.colors.to_rgb(g), min(0.96, 0.55 + 0.4 * heat))
            patches.append(Rectangle((x - s / 2, y - s / 2), s, s))
            colors.append(c)
    if patches:
        ax.add_collection(PatchCollection(
            patches, facecolors=colors, edgecolors="#0b0e14", linewidths=0.35, zorder=2))

    ax.add_patch(Circle((0, 0), r_out, fill=False, edgecolor=CYAN, lw=2.0,
                        alpha=0.55, linestyle="--", zorder=3))
    ax.add_patch(Circle((0, 0), max(r_core, 0.35), fill=False, edgecolor=GOLD,
                        lw=2.2, alpha=0.90, zorder=3))
    # No tiny R_out / R_half text labels (reviewer request).


def draw_mass_inflow(ax, r_out, n_arrows=5):
    r0 = r_out * 1.55
    r1 = r_out * 0.55
    for i in range(n_arrows):
        ang = -0.50 + i * (1.00 / max(n_arrows - 1, 1))
        x0, y0 = r0 * math.cos(ang), r0 * math.sin(ang) * 0.75
        x1, y1 = r1 * math.cos(ang), r1 * math.sin(ang) * 0.75
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color=GOLD, lw=2.4,
                                    mutation_scale=18),
                    zorder=5)
    ax.text(r0 * 0.92, r0 * 0.42, "mass\nadded", color=GOLD,
            fontsize=MIN_PT, ha="center", va="center", weight="bold")


def draw_inward_arrows(ax, r_out, r_core):
    for ang in np.linspace(0, 2 * math.pi, 8, endpoint=False):
        x0, y0 = r_out * 0.72 * math.cos(ang), r_out * 0.72 * math.sin(ang)
        x1, y1 = (r_core + 0.55) * math.cos(ang), (r_core + 0.55) * math.sin(ang)
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color=GOLD_HOT, lw=2.2,
                                    mutation_scale=16),
                    zorder=5)


def compose(path, title, caps, paint_art, show_frame=True):
    fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI, facecolor=BG)
    # Full-frame chrome axes (transparent overlay for text bands only)
    ax_txt = fig.add_axes([0, 0, 1, 1])
    ax_txt.set_facecolor(BG)
    ax_txt.set_xlim(0, 1)
    ax_txt.set_ylim(0, 1)
    ax_txt.axis("off")
    # Soft separators for bands (subtle, not labels)
    ax_txt.axhline(Y_ART_TOP, color="#1c2430", lw=1.0, xmin=0.04, xmax=0.96)
    ax_txt.axhline(Y_ART_BOTTOM, color="#1c2430", lw=1.0, xmin=0.04, xmax=0.96)

    draw_chrome(ax_txt, title, show_frame=show_frame)
    draw_captions(ax_txt, caps)

    ax_art = art_axes(fig)
    paint_art(ax_art)

    fig.savefig(path, dpi=DPI, facecolor=BG)
    plt.close(fig)
    # Verify pixel size
    from PIL import Image
    im = Image.open(path)
    assert im.size == (1920, 1080), f"{path} size {im.size}"
    return path


def still_setup(path):
    def paint(ax):
        draw_radial_lump(ax, r_core=1.2, r_out=3.0, density_core=0.45)
    return compose(path, "Setup", SCENES[0][4], paint, show_frame=True)


def still_supported(path):
    def paint(ax):
        draw_radial_lump(ax, r_core=2.1, r_out=3.0, density_core=0.55)
    return compose(path, "Supported lump", SCENES[1][4], paint)


def still_add_mass(path):
    def paint(ax):
        draw_radial_lump(ax, r_core=3.6, r_out=7.2, density_core=0.85)
        draw_mass_inflow(ax, r_out=7.2)
    return compose(path, "Add mass", SCENES[2][4], paint)


def still_cap(path):
    def paint(ax):
        # Bridge B → threshold: mass still being added
        draw_radial_lump(ax, r_core=3.2, r_out=6.5, density_core=1.05)
        draw_mass_inflow(ax, r_out=6.5, n_arrows=4)
        ax.add_patch(Circle((0, 0), 1.15, fill=False, edgecolor=GOLD_HOT,
                            lw=3.0, zorder=6))
    return compose(path, "Support cap", SCENES[3][4], paint)


def still_collapse(path):
    def paint(ax):
        draw_radial_lump(ax, r_core=0.95, r_out=7.5, density_core=1.6, collapse=True)
        draw_inward_arrows(ax, r_out=7.5, r_core=0.95)
    return compose(path, "Inward collapse", SCENES[4][4], paint)


def still_after(path):
    def paint(ax):
        # Bridge threshold → C via mass addition
        draw_radial_lump(ax, r_core=0.9, r_out=9.0, density_core=1.9, collapse=True)
        draw_mass_inflow(ax, r_out=9.0, n_arrows=4)
    return compose(path, "After collapse", SCENES[5][4], paint)


def make_tally(ax):
    vals = [RHO_A, RHO_B, RHO_C]
    labels = [
        f"A\nN={N_A}\nρ≈{RHO_A}",
        f"B\nN={N_B}\nρ≈{RHO_B}",
        f"C\nN≈{N_C // 1000}k\nρ≈{RHO_C:,}",
    ]
    heights = [math.sqrt(v) for v in vals]
    xs = [0.0, 1.5, 3.0]
    for x, h, lab, v in zip(xs, heights, labels, vals):
        ax.add_patch(Rectangle((x, 0), 1.0, h,
                               facecolor=GOLD if v > 100 else CYAN,
                               edgecolor=W, lw=1.0))
        ax.text(x + 0.5, h + 0.2, lab, color=W, fontsize=11, ha="center", va="bottom")
    ax.set_xlim(-0.4, 4.4)
    ax.set_ylim(0, max(heights) * 1.4)
    ax.axis("off")
    ax.set_facecolor(BG)
    ax.text(2.0, -0.12 * max(heights),
            "half-mass density tally (√-scaled for display)",
            color=MUTED, fontsize=10, ha="center", va="top")


def make_pdf(still_paths):
    pdf_path = os.path.join(OUT, "storyboard.pdf")
    with PdfPages(pdf_path) as pdf:
        # ---- Cover / scene index ----
        fig = plt.figure(figsize=(11, 8.5), facecolor=BG)
        fig.text(0.05, 0.94, CORNER, color=MUTED, fontsize=11)
        fig.text(0.5, 0.88, "Storyboard: OP2 star collapse (toy model)",
                 ha="center", color=W, fontsize=18, weight="bold")
        fig.text(0.5, 0.835, FRAME_L1, ha="center", color=GOLD, fontsize=11)
        fig.text(0.5, 0.805, FRAME_L2, ha="center", color=GOLD, fontsize=11, weight="bold")
        fig.text(0.5, 0.76,
                 "Approved board on record · G = 0.01 · ~38 s · release: op2_collapse_v2.mp4",
                 ha="center", color=MUTED, fontsize=10)
        y = 0.68
        for sid, t0, t1, title, caps, _ in SCENES:
            dur = t1 - t0
            fig.text(0.06, y, f"F{sid}  {t0:>2d}–{t1:<2d}s ({dur}s)",
                     color=CYAN, fontsize=10, family="monospace")
            fig.text(0.30, y, title, color=W, fontsize=11, weight="bold")
            fig.text(0.30, y - 0.025, caps[0], color=GOLD, fontsize=9)
            if len(caps) > 1:
                fig.text(0.30, y - 0.045, caps[1], color=MUTED, fontsize=8.5)
            y -= 0.085
        fig.text(0.05, 0.06,
                 "Layout: 1920×1080 · all on-screen text ≥38 px · header / art / caption bands separated",
                 color="#667", fontsize=8)
        pdf.savefig(fig, facecolor=BG)
        plt.close(fig)

        # ---- Notes / disclosures page (detailed numbers + caveats) ----
        fig = plt.figure(figsize=(11, 8.5), facecolor=BG)
        fig.text(0.05, 0.94, CORNER, color=MUTED, fontsize=11)
        fig.text(0.5, 0.88, "Notes page — numbers, sources, caveats",
                 ha="center", color=W, fontsize=16, weight="bold")
        fig.text(0.5, 0.84, "Kept off the video frames. Approved board; release file is op2_collapse_v2.mp4",
                 ha="center", color=MUTED, fontsize=10)

        lines = [
            f"Dataset: Pauli v4 radial-shell mean-field toy · G = {G} (model units) · not a 3D stellar/hydro sim",
            "Choices: 2 spin slots/level/node; no self-load; blast-spill = max-radius load-packing rule (not ejecta)",
            "Support cap: LCAP = 7 is a disclosed interpretation of 8-neighbour spill capacity (model choice)",
            "Past the chosen cap, other-particle congestion pulls mass inward; R_half → 1 (lattice floor)",
            f"Point A (supported): N={N_A}, ρ_half≈{RHO_A} (exact 1.925…), R_half≈2.06, R_out=3",
            f"Point B (near collapse): N={N_B}, ρ_half≈{RHO_B} (exact 8.066…), R_half≈3.85, R_out=8",
            f"Collapse threshold: N={N_COLLAPSE} (data/pauli_deg4_G0.01_excerpt.json collapse_N; that row has R_half=1)",
            f"Point C (~10× collapse N): N={N_C}, ρ_half≈{RHO_C:,} (exact 5506…), R_half=1, R_out=18",
            "ρ_half = (N/2)/(4/3 π R_half³). Outer/halo density stays ~1–2 (thin ground-level envelope).",
            "B/A half-mass density ≈ 4.2× at G=0.01 — not real planet→WD density matching (~10⁵).",
            "No sustained white-dwarf R ∝ M⁻¹/³ branch in this scan.",
            "A/B/threshold/C are separate mass states: bridge on screen by explicitly adding mass (A→B→threshold→C).",
            "Motion/timing are illustrative — not measured collapse dynamics.",
            "Do not depict: blast-spill ejecta, supernova, bounce, nuclear burning, neutron phase, BH/horizon.",
            "Sources: provenance/pauli_massdens_SUMMARY.md + data/pauli_massdens_G0.01_excerpt.json;",
            "         provenance/pauli_deg4_SUMMARY.md + data/pauli_deg4_G0.01_excerpt.json",
        ]
        y = 0.78
        for line in lines:
            fig.text(0.05, y, "•  " + line, color=W if line.startswith("Point") or line.startswith("Collapse") else MUTED,
                     fontsize=8.5)
            y -= 0.035

        ax = fig.add_axes([0.22, 0.04, 0.56, 0.18])
        make_tally(ax)
        pdf.savefig(fig, facecolor=BG)
        plt.close(fig)

        # ---- One page per still ----
        for sid, path in still_paths:
            fig = plt.figure(figsize=(11, 8.5), facecolor=BG)
            sc = next(s for s in SCENES if s[0] == sid)
            fig.text(0.05, 0.965, f"Frame {sid}", color=CYAN, fontsize=11)
            fig.text(0.18, 0.965, f"{sc[3]}  ·  {sc[1]}–{sc[2]}s", color=W, fontsize=11)
            img = plt.imread(path)
            ax = fig.add_axes([0.03, 0.04, 0.94, 0.90])
            ax.imshow(img)
            ax.axis("off")
            pdf.savefig(fig, facecolor=BG)
            plt.close(fig)
    return pdf_path


def main():
    makers = [
        (1, "sb_01_setup.png", still_setup),
        (2, "sb_02_supported.png", still_supported),
        (3, "sb_03_add_mass.png", still_add_mass),
        (4, "sb_04_cap.png", still_cap),
        (5, "sb_05_collapse.png", still_collapse),
        (6, "sb_06_after.png", still_after),
    ]
    still_paths = []
    for sid, name, fn in makers:
        path = os.path.join(OUT, name)
        fn(path)
        print("wrote", path)
        still_paths.append((sid, path))
    pdf = make_pdf(still_paths)
    print("wrote", pdf)


if __name__ == "__main__":
    main()
