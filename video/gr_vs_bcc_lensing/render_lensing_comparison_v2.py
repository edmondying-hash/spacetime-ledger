#!/usr/bin/env python3
"""
v2 Conceptual side-by-side lensing illustration renderer.
GR geometric description (LEFT) vs proposed fixed-BCC congestion (RIGHT).

FIXES vs v1:
  (1) Nonzero impact parameter: source ABOVE mass; initial tangent horizontal;
      outgoing tangent deflected DOWN toward mass (attractive schematic);
      monotonic downward curvature; beam clear of mass disk.
  (2) Active BCC links = body-center→8-corner nearest neighbours ONLY
      (no cubic-frame axis edges in the network/capacity set).
  (3) Larger source/mass icons; right 'mass' label drawn last with opaque backing
      clear of glow/network.

NOT a physics simulation. Paths and load colours are artist-selected.
No GR delay map inherited. No quantitative validation claim.
Preserves v1 artifacts; this writes *_v2 outputs only.
"""
from __future__ import annotations

import json
import math
import struct
import subprocess
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Outputs sit beside this script. The reviewed copy used /workspace/lensing_storyboard.
OUT_DIR = Path(__file__).resolve().parent
FRAMES_DIR = OUT_DIR / "frames_v2"
MP4_PATH = OUT_DIR / "lensing_comparison_v2.mp4"
CONTACT_PATH = OUT_DIR / "contact_sheet_v2.jpg"
NOTES_PATH = OUT_DIR / "SCIENTIFIC_NOTES_v2.md"
VALIDATION_PATH = OUT_DIR / "validation_v2.json"
GEOM_PATH = OUT_DIR / "bcc_geometry_v2.json"

W, H = 1920, 1080
FPS = 30
DURATION = 38.0
N_FRAMES = int(DURATION * FPS)  # 1140

MARGIN = 28
GAP = 20
PANEL_W = (W - 2 * MARGIN - GAP) // 2
PANEL_H = H - 160
LEFT_X0 = MARGIN
RIGHT_X0 = MARGIN + PANEL_W + GAP
PANEL_Y0 = 78

BG = (12, 14, 20)
PANEL_BG = (18, 22, 32)
PANEL_BORDER = (48, 56, 72)
FOOTER_BG = (10, 12, 16)

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# --- Shared scene: source ABOVE mass (nonzero impact parameter) ---
# Artist-chosen layout (panel-local). Mass below the beam; beam stays clear.
SRC_X, SRC_Y = 70, 330
MASS_X, MASS_Y = PANEL_W // 2 + 20, 500  # impact parameter ≈ 170 px
FAR_X = PANEL_W - 70
MASS_R = 34  # drawn radius; path clearance enforced in validation


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def scene_points(panel_x0: int):
    src = (SRC_X, SRC_Y)
    mass = (MASS_X, MASS_Y)
    far = (FAR_X, SRC_Y)  # undeflected reference level
    return {
        "src": (panel_x0 + src[0], PANEL_Y0 + src[1]),
        "mass": (panel_x0 + mass[0], PANEL_Y0 + mass[1]),
        "far": (panel_x0 + far[0], PANEL_Y0 + far[1]),
        "src_local": src,
        "mass_local": mass,
        "far_local": far,
    }


# ---------------------------------------------------------------------------
# Artist-selected Bezier paths — attractive schematic (NOT physics)
# Initial tangent horizontal (P1.y == P0.y).
# Near encounter: monotonic downward curvature (y increases) toward mass.
# Outgoing tangent has positive dy (deflected down vs initial).
# Beam stays above mass disk. Distinct left/right shapes.
# ---------------------------------------------------------------------------
GR_CTRL = [
    (SRC_X, SRC_Y),                 # P0 source
    (300, SRC_Y),                   # P1 horizontal initial tangent
    (500, SRC_Y + 95),              # P2 bend down near mass (still above mass)
    (FAR_X, SRC_Y + 145),           # P3 outgoing further down
]

# Distinct hypothetical — slightly stronger downward bend, different landing
BCC_CTRL = [
    (SRC_X, SRC_Y),
    (320, SRC_Y),                   # horizontal initial
    (485, SRC_Y + 125),             # stronger / earlier downward bend
    (FAR_X, SRC_Y + 185),           # distinct lower arrival
]


def bezier_point(ctrl, t: float):
    p0, p1, p2, p3 = ctrl
    u = 1 - t
    x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
    y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
    return (x, y)


def bezier_tangent(ctrl, t: float):
    """dB/dt for cubic Bezier (not unit-normalized)."""
    p0, p1, p2, p3 = ctrl
    u = 1 - t
    dx = 3 * u**2 * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t**2 * (p3[0] - p2[0])
    dy = 3 * u**2 * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t**2 * (p3[1] - p2[1])
    return (dx, dy)


# ---------------------------------------------------------------------------
# True BCC lattice — nearest-eight ONLY (body-center → 8 corners)
# No cubic-frame axis edges in the active network/capacity set.
# ---------------------------------------------------------------------------
def build_bcc_lattice():
    a = 1.0
    cells = [(ix, iy, iz) for ix in range(-1, 2) for iy in range(-1, 2) for iz in range(-1, 2)]

    node_set = {}

    def add_node(p3):
        key = (round(p3[0], 6), round(p3[1], 6), round(p3[2], 6))
        if key not in node_set:
            node_set[key] = len(node_set)
        return node_set[key]

    links = set()
    for cx, cy, cz in cells:
        corners = []
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    p = ((cx + dx) * a, (cy + dy) * a, (cz + dz) * a)
                    corners.append(add_node(p))
        center = add_node(((cx + 0.5) * a, (cy + 0.5) * a, (cz + 0.5) * a))
        # BCC nearest neighbours ONLY: body-center to each of 8 corners
        for c in corners:
            i, j = sorted((center, c))
            links.add((i, j))
        # NO cube-axis corner–corner edges in active link set

    inv = [None] * len(node_set)
    for key, idx in node_set.items():
        inv[idx] = key

    def project(p3):
        x, y, z = p3
        yaw = math.radians(35)
        pitch = math.radians(25)
        xz = x * math.cos(yaw) + z * math.sin(yaw)
        zz = -x * math.sin(yaw) + z * math.cos(yaw)
        y2 = y * math.cos(pitch) - zz * math.sin(pitch)
        z2 = y * math.sin(pitch) + zz * math.cos(pitch)
        return xz, y2, z2

    projected3 = [project(p) for p in inv]
    xs = [p[0] for p in projected3]
    ys = [p[1] for p in projected3]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    span = max(maxx - minx, maxy - miny) or 1.0
    target_span = 300.0
    scale = target_span / span
    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2

    nodes_2d = []
    for p in projected3:
        px = MASS_X + (p[0] - cx) * scale
        py = MASS_Y + (p[1] - cy) * scale
        nodes_2d.append((px, py))

    link_list = sorted(links)
    n_body = sum(
        1 for p in inv
        if all(abs((c - math.floor(c)) - 0.5) < 1e-6 for c in p)
    )
    n_corner = len(inv) - n_body
    meta = {
        "n_nodes": len(nodes_2d),
        "n_links": len(link_list),
        "expected_nodes": 91,
        "expected_nearest_links": 216,  # 27 cells × 8, unique
        "n_body_centers": n_body,
        "n_corners": n_corner,
        "active_links": "body-center to 8 corners ONLY (BCC nearest neighbours)",
        "cube_axis_edges_in_network": False,
        "note": (
            "True BCC schematic projection. Active capacity/network links are "
            "exclusively body-center→corner nearest neighbours. No cubic-frame "
            "axis edges in the active set. Node positions FIXED every frame."
        ),
        "projection": {"yaw_deg": 35, "pitch_deg": 25, "scale": scale},
        "artist_selected": True,
        "physics_simulation": False,
    }
    return nodes_2d, link_list, meta, inv


NODES_2D, LINKS, BCC_META, NODES_3D = build_bcc_lattice()


def assert_bcc_static_geometry():
    checks = []
    for i, (x, y) in enumerate(NODES_2D):
        ok = (-40 <= x <= PANEL_W + 40) and (-40 <= y <= PANEL_H + 40)
        checks.append({"check": f"node_{i}_near_panel", "ok": bool(ok), "xy": [x, y]})
    for a, b in LINKS:
        ok = 0 <= a < len(NODES_2D) and 0 <= b < len(NODES_2D) and a != b
        checks.append({"check": f"link_{a}_{b}_valid", "ok": bool(ok)})

    half = sum(1 for p in NODES_3D if all(abs((c - math.floor(c)) - 0.5) < 1e-6 for c in p))
    cornerish = len(NODES_3D) - half
    checks.append({"check": "has_body_centers", "ok": half == 27, "n_body_centers": half})
    checks.append({"check": "has_corner_nodes", "ok": cornerish == 64, "n_corners": cornerish})
    checks.append({"check": "n_nodes_91", "ok": len(NODES_2D) == 91, "n": len(NODES_2D)})
    checks.append({"check": "n_nearest_links_216", "ok": len(LINKS) == 216, "n": len(LINKS)})

    # Every active link must be body-center ↔ corner (one endpoint all-half, other all-integer)
    def is_body(p):
        return all(abs((c - math.floor(c)) - 0.5) < 1e-6 for c in p)

    def is_corner(p):
        return all(abs(c - round(c)) < 1e-6 for c in p)

    bad = 0
    for a, b in LINKS:
        pa, pb = NODES_3D[a], NODES_3D[b]
        ok = (is_body(pa) and is_corner(pb)) or (is_corner(pa) and is_body(pb))
        if not ok:
            bad += 1
    checks.append({"check": "all_links_bcc_nearest_eight", "ok": bad == 0, "non_nn_count": bad})

    # No axis-aligned corner–corner edges of length a slipped in
    axis_cc = 0
    for a, b in LINKS:
        pa, pb = NODES_3D[a], NODES_3D[b]
        if is_corner(pa) and is_corner(pb):
            diffs = [abs(pa[k] - pb[k]) for k in range(3)]
            if sorted(diffs) == [0.0, 0.0, 1.0]:
                axis_cc += 1
    checks.append({"check": "no_cube_axis_corner_edges", "ok": axis_cc == 0, "count": axis_cc})

    blob = struct.pack(f"{len(NODES_2D)*2}d", *[c for xy in NODES_2D for c in xy])
    geom_hash = hashlib.sha256(blob).hexdigest()
    return checks, geom_hash


def analyze_paths():
    """Confirm attractive schematic geometry (render validation, not physics)."""
    out = {}
    for name, ctrl in (("GR", GR_CTRL), ("BCC", BCC_CTRL)):
        t0 = bezier_tangent(ctrl, 0.0)
        t1 = bezier_tangent(ctrl, 1.0)
        # sample clearance to mass
        min_dist = 1e9
        ys = []
        for i in range(200):
            t = i / 199
            x, y = bezier_point(ctrl, t)
            ys.append(y)
            d = math.hypot(x - MASS_X, y - MASS_Y)
            min_dist = min(min_dist, d)
        # monotonic-ish downward near encounter (t in [0.25, 0.85]): y nondecreasing
        near = [bezier_point(ctrl, t)[1] for t in [i / 100 for i in range(25, 86)]]
        mono_down = all(near[i] <= near[i + 1] + 1e-6 for i in range(len(near) - 1))
        out[name] = {
            "initial_tangent_xy": t0,
            "initial_horizontal": abs(t0[1]) < 1e-6 and t0[0] > 0,
            "outgoing_tangent_xy": t1,
            "outgoing_deflected_down": t1[1] > 0 and t1[0] > 0,
            "source_above_mass": SRC_Y < MASS_Y,
            "impact_parameter_px": MASS_Y - SRC_Y,
            "min_dist_to_mass": min_dist,
            "clear_of_mass_disk": min_dist > MASS_R + 8,
            "monotonic_down_near_encounter": mono_down,
            "y_start": ctrl[0][1],
            "y_end": ctrl[3][1],
            "end_below_start": ctrl[3][1] > ctrl[0][1],
        }
    out["paths_distinct"] = GR_CTRL != BCC_CTRL
    out["matched_initial_source"] = GR_CTRL[0] == BCC_CTRL[0]
    return out


def load_factor(node_xy, t_sec: float) -> float:
    mx, my = MASS_X, MASS_Y
    dist = math.hypot(node_xy[0] - mx, node_xy[1] - my)
    spatial = math.exp(-(dist ** 2) / (2 * 95 ** 2))
    if t_sec < 6:
        temp = 0.08
    elif t_sec < 14:
        temp = 0.08 + 0.75 * ((t_sec - 6) / 8)
    elif t_sec < 24:
        temp = 0.83 + 0.12 * ((t_sec - 14) / 10)
    elif t_sec < 32:
        temp = 0.95
    else:
        temp = 0.90
    return max(0.0, min(1.0, spatial * temp + 0.05))


def load_color(u: float):
    u = max(0.0, min(1.0, u))
    r = int(40 + u * 200)
    g = int(80 + u * 100)
    b = int(180 - u * 140)
    return (r, g, b)


def draw_rounded_rect(draw, xy, fill, outline=None, width=1, radius=12):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_text_checked(draw, xy, text, fnt, fill, bounds_log, tag, max_w=None):
    x, y = xy
    tw, th = text_size(draw, text, fnt)
    if max_w and tw > max_w:
        while tw > max_w and len(text) > 4:
            text = text[:-2] + "…"
            tw, th = text_size(draw, text, fnt)
    draw.text((x, y), text, font=fnt, fill=fill)
    entry = {
        "tag": tag, "x": x, "y": y, "w": tw, "h": th,
        "right": x + tw, "bottom": y + th,
        "in_frame": x >= 0 and y >= 0 and x + tw <= W and y + th <= H,
        "text": text,
    }
    bounds_log.append(entry)
    return entry


def draw_label_backed(draw, xy, text, fnt, fill, bg, bounds_log, tag, pad=5):
    """Opaque backing so label stays readable over glow/network."""
    x, y = xy
    tw, th = text_size(draw, text, fnt)
    draw.rounded_rectangle(
        (x - pad, y - pad, x + tw + pad, y + th + pad),
        radius=6, fill=bg,
    )
    return draw_text_checked(draw, (x, y), text, fnt, fill, bounds_log, tag)


def draw_mass(draw, cx, cy, r=MASS_R):
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(55, 55, 70), outline=(170, 170, 190), width=3)
    draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=(210, 210, 220))


def draw_source(draw, cx, cy, glow=1.0):
    r = int(12 + 5 * glow)
    draw.ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), fill=(40, 55, 28))
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(190, 230, 110))


def draw_guides(draw, sp, color=(55, 65, 85)):
    sx, sy = sp["src"]
    fx, fy = sp["far"]
    # faint horizontal undeflected level through source
    draw.line([(sx, sy), (fx, fy)], fill=color, width=1)


def draw_undeflected_ref(draw, panel_x0, color=(90, 100, 120)):
    """Illustrative dashed undeflected reference (horizontal from source)."""
    y = PANEL_Y0 + SRC_Y
    x0 = panel_x0 + SRC_X
    x1 = panel_x0 + FAR_X
    # dashed
    x = x0
    on = True
    while x < x1:
        x2 = min(x + 14, x1)
        if on:
            draw.line([(x, y), (x2, y)], fill=color, width=2)
        on = not on
        x = x2


def draw_path(draw, ctrl, panel_x0, t_progress, color, width=4, dashed=False):
    n = max(2, int(100 * max(t_progress, 0.001)))
    pts = []
    for i in range(n):
        tt = (i / (n - 1)) * t_progress
        lx, ly = bezier_point(ctrl, tt)
        pts.append((panel_x0 + lx, PANEL_Y0 + ly))
    if len(pts) < 2:
        return pts
    if not dashed:
        draw.line(pts, fill=color, width=width, joint="curve")
    else:
        for i in range(0, len(pts) - 1, 2):
            if i + 1 < len(pts):
                draw.line([pts[i], pts[i + 1]], fill=color, width=width)
    return pts


def draw_pulse(draw, ctrl, panel_x0, t_progress, color):
    if t_progress <= 0:
        return
    lx, ly = bezier_point(ctrl, min(1.0, t_progress))
    x, y = panel_x0 + lx, PANEL_Y0 + ly
    draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=color)
    draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 255, 240))


def draw_arrow_head(draw, ctrl, panel_x0, t_progress, color):
    if t_progress < 0.15:
        return
    t0 = max(0.0, t_progress - 0.04)
    x0, y0 = bezier_point(ctrl, t0)
    x1, y1 = bezier_point(ctrl, t_progress)
    x0, y0 = panel_x0 + x0, PANEL_Y0 + y0
    x1, y1 = panel_x0 + x1, PANEL_Y0 + y1
    ang = math.atan2(y1 - y0, x1 - x0)
    L = 16
    a1 = ang + math.radians(150)
    a2 = ang - math.radians(150)
    p1 = (x1 + L * math.cos(a1), y1 + L * math.sin(a1))
    p2 = (x1 + L * math.cos(a2), y1 + L * math.sin(a2))
    draw.polygon([(x1, y1), p1, p2], fill=color)


def stage_caption(t: float):
    if t < 6:
        return "Same source & mass arrangement · two different proposed descriptions"
    if t < 14:
        return "LEFT: geometric null-path illustration · RIGHT: illustrative load activity (hypothesis)"
    if t < 24:
        return "Different descriptions of lensing · equivalence is not demonstrated"
    if t < 32:
        return "Similar visual lensing can be described differently — equivalence not shown"
    return "LEFT: established GR geometry · RIGHT: speculative fixed-BCC congestion · not validation"


def path_progress(t: float) -> float:
    if t < 6:
        return 0.0
    if t < 32:
        return (t - 6) / 26.0
    return 1.0


def render_frame(fi: int, geom_hash: str, bounds_all: list):
    t = fi / FPS
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    bounds_log = []

    draw_text_checked(
        draw, (MARGIN, 18),
        "Conceptual lensing comparison  ·  Established GR geometry  vs  Proposed fixed-BCC congestion",
        font(26, True), (210, 215, 225), bounds_log, "title", max_w=W - 2 * MARGIN,
    )

    for x0 in (LEFT_X0, RIGHT_X0):
        draw_rounded_rect(
            draw, (x0, PANEL_Y0, x0 + PANEL_W, PANEL_Y0 + PANEL_H),
            fill=PANEL_BG, outline=PANEL_BORDER, width=2, radius=14,
        )

    f_lab = font(28, True)
    draw_text_checked(
        draw, (LEFT_X0 + 16, PANEL_Y0 + 12),
        "GR — geometric (null geodesics)",
        f_lab, (140, 200, 255), bounds_log, "left_label", max_w=PANEL_W - 32,
    )
    draw_text_checked(
        draw, (RIGHT_X0 + 16, PANEL_Y0 + 12),
        "Proposed fixed BCC — congestion (hypothesis)",
        f_lab, (255, 190, 120), bounds_log, "right_label", max_w=PANEL_W - 32,
    )
    f_chip = font(22, True)
    draw_text_checked(
        draw, (LEFT_X0 + 16, PANEL_Y0 + 48),
        "Established description",
        f_chip, (100, 160, 220), bounds_log, "left_chip",
    )
    draw_text_checked(
        draw, (RIGHT_X0 + 16, PANEL_Y0 + 48),
        "Proposed mechanism — not calculated",
        f_chip, (220, 150, 90), bounds_log, "right_chip",
    )

    spL = scene_points(LEFT_X0)
    spR = scene_points(RIGHT_X0)

    draw_guides(draw, spL)
    draw_guides(draw, spR)

    # Undeflected reference (makes attractive downward deflection obvious)
    if t >= 6:
        draw_undeflected_ref(draw, LEFT_X0)
        draw_undeflected_ref(draw, RIGHT_X0)

    draw_source(draw, spL["src"][0], spL["src"][1], glow=1.0)
    draw_source(draw, spR["src"][0], spR["src"][1], glow=1.0)

    # RIGHT: fixed BCC nearest-eight network with illustrative load (under mass)
    for a, b in LINKS:
        xa, ya = NODES_2D[a]
        xb, yb = NODES_2D[b]
        sa = (RIGHT_X0 + xa, PANEL_Y0 + ya)
        sb = (RIGHT_X0 + xb, PANEL_Y0 + yb)
        u = 0.5 * (load_factor((xa, ya), t) + load_factor((xb, yb), t))
        col2 = tuple(max(20, int(c * 0.65)) for c in load_color(u))
        draw.line([sa, sb], fill=col2, width=2)
    for (xa, ya) in NODES_2D:
        u = load_factor((xa, ya), t)
        col = load_color(u)
        x = RIGHT_X0 + xa
        y = PANEL_Y0 + ya
        r = 5
        draw.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=(230, 230, 240), width=1)

    # Mass above lattice
    draw_mass(draw, spL["mass"][0], spL["mass"][1])
    draw_mass(draw, spR["mass"][0], spR["mass"][1])

    f_tiny = font(20)
    draw_text_checked(draw, (spL["src"][0] - 14, spL["src"][1] - 36), "source", f_tiny, (140, 160, 120), bounds_log, "srcL")
    draw_text_checked(draw, (spR["src"][0] - 14, spR["src"][1] - 36), "source", f_tiny, (140, 160, 120), bounds_log, "srcR")
    # LEFT mass label below icon (panel is emptier)
    draw_text_checked(draw, (spL["mass"][0] - 20, spL["mass"][1] + MASS_R + 8), "mass", f_tiny, (160, 160, 180), bounds_log, "massL")
    # RIGHT mass label deferred to end (opaque backing) — placeholder skip here

    prog = path_progress(t)

    if t >= 6:
        draw_path(draw, GR_CTRL, LEFT_X0, prog, color=(120, 190, 255), width=5, dashed=False)
        draw_pulse(draw, GR_CTRL, LEFT_X0, prog, color=(150, 210, 255))
        if t >= 14:
            draw_arrow_head(draw, GR_CTRL, LEFT_X0, prog, color=(120, 190, 255))

        draw_path(draw, BCC_CTRL, RIGHT_X0, prog, color=(255, 170, 80), width=5, dashed=True)
        draw_pulse(draw, BCC_CTRL, RIGHT_X0, prog, color=(255, 200, 120))
        if t >= 14:
            draw_arrow_head(draw, BCC_CTRL, RIGHT_X0, prog, color=(255, 170, 80))

    f_cap = font(34, True)
    f_ann = font(26, True)
    f_sub = font(24)

    if t >= 14:
        hx = RIGHT_X0 + 24
        hy = PANEL_Y0 + 100
        draw_label_backed(draw, (hx, hy), "Hypothetical deflection", f_ann, (255, 180, 100), (28, 24, 18), bounds_log, "hyp_deflect")
        draw_label_backed(draw, (hx, hy + 36), "Not a calculated prediction", f_ann, (255, 150, 90), (28, 24, 18), bounds_log, "not_calc")

    if 6 <= t < 14:
        draw_text_checked(
            draw, (LEFT_X0 + 16, PANEL_Y0 + PANEL_H - 70),
            "Geometry: null geodesics near mass · local c unchanged",
            f_sub, (150, 190, 230), bounds_log, "capL2", max_w=PANEL_W - 32,
        )
        draw_text_checked(
            draw, (RIGHT_X0 + 16, PANEL_Y0 + PANEL_H - 70),
            "Hypothesis: illustrative link/node load · rigid lattice fixed",
            f_sub, (230, 180, 120), bounds_log, "capR2", max_w=PANEL_W - 32,
        )

    if 14 <= t < 24:
        draw_text_checked(
            draw, (LEFT_X0 + 16, PANEL_Y0 + PANEL_H - 70),
            "GR: lensing as geometric path effect (illustration)",
            f_sub, (150, 190, 230), bounds_log, "capL3", max_w=PANEL_W - 32,
        )
        draw_text_checked(
            draw, (RIGHT_X0 + 16, PANEL_Y0 + PANEL_H - 70),
            "Proposed: congestion affects propagation (not demonstrated)",
            f_sub, (230, 180, 120), bounds_log, "capR3", max_w=PANEL_W - 32,
        )

    if 24 <= t < 32:
        lx, ly = bezier_point(GR_CTRL, 1.0)
        ax, ay = LEFT_X0 + lx, PANEL_Y0 + ly
        draw.ellipse((ax - 8, ay - 8, ax + 8, ay + 8), outline=(120, 190, 255), width=2)
        draw_text_checked(draw, (ax - 22, ay + 12), "arrival", f_tiny, (120, 190, 255), bounds_log, "arrL")
        rx, ry = bezier_point(BCC_CTRL, 1.0)
        bx, by = RIGHT_X0 + rx, PANEL_Y0 + ry
        draw.ellipse((bx - 8, by - 8, bx + 8, by + 8), outline=(255, 170, 80), width=2)
        draw_text_checked(draw, (bx - 22, by + 12), "arrival", f_tiny, (255, 170, 80), bounds_log, "arrR")

    if t >= 32:
        draw_text_checked(
            draw, (LEFT_X0 + 16, PANEL_Y0 + PANEL_H - 70),
            "Established GR geometry",
            f_sub, (150, 190, 230), bounds_log, "capL5", max_w=PANEL_W - 32,
        )
        draw_text_checked(
            draw, (RIGHT_X0 + 16, PANEL_Y0 + PANEL_H - 70),
            "Speculative fixed-BCC congestion mechanism",
            f_sub, (230, 180, 120), bounds_log, "capR5", max_w=PANEL_W - 32,
        )

    # RIGHT mass label LAST with opaque backing — BELOW entire BCC node cloud
    # Node y extent is ~350..650 panel-local; place label under max extent.
    max_node_y = max(y for _, y in NODES_2D)
    mass_label_xy = (RIGHT_X0 + MASS_X - 22, PANEL_Y0 + max_node_y + 12)
    draw_label_backed(
        draw, mass_label_xy, "mass", f_tiny, (210, 210, 220), (18, 22, 32),
        bounds_log, "massR", pad=6,
    )

    cap = stage_caption(t)
    cw, ch = text_size(draw, cap, f_cap)
    cx = (W - cw) // 2
    cy = PANEL_Y0 + PANEL_H + 10
    if cy + ch > H - 36:
        cy = H - 36 - ch
    draw_text_checked(draw, (cx, cy), cap, f_cap, (230, 230, 235), bounds_log, "stage_cap", max_w=W - 40)

    footer = "Conceptual illustration — not quantitative validation"
    fw, fh = text_size(draw, footer, font(22, True))
    draw.rectangle((0, H - 34, W, H), fill=FOOTER_BG)
    draw_text_checked(
        draw, ((W - fw) // 2, H - 28),
        footer, font(22, True), (160, 165, 175), bounds_log, "footer",
    )

    bounds_all.append({"frame": fi, "t": t, "items": bounds_log})

    blob = struct.pack(f"{len(NODES_2D)*2}d", *[c for xy in NODES_2D for c in xy])
    h = hashlib.sha256(blob).hexdigest()
    assert h == geom_hash, "BCC node positions mutated across frames — forbidden"
    return img


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if FRAMES_DIR.exists():
        for p in FRAMES_DIR.glob("*.png"):
            p.unlink()
    else:
        FRAMES_DIR.mkdir(parents=True)

    checks, geom_hash = assert_bcc_static_geometry()
    path_analysis = analyze_paths()
    assert path_analysis["GR"]["initial_horizontal"], path_analysis["GR"]
    assert path_analysis["GR"]["outgoing_deflected_down"], path_analysis["GR"]
    assert path_analysis["GR"]["clear_of_mass_disk"], path_analysis["GR"]
    assert path_analysis["GR"]["monotonic_down_near_encounter"], path_analysis["GR"]
    assert path_analysis["BCC"]["initial_horizontal"], path_analysis["BCC"]
    assert path_analysis["BCC"]["outgoing_deflected_down"], path_analysis["BCC"]
    assert path_analysis["BCC"]["clear_of_mass_disk"], path_analysis["BCC"]
    assert path_analysis["BCC"]["monotonic_down_near_encounter"], path_analysis["BCC"]
    assert path_analysis["paths_distinct"]
    failed = [c for c in checks if not c.get("ok")]
    assert not failed, failed

    GEOM_PATH.write_text(json.dumps({
        "meta": BCC_META,
        "geom_hash_sha256": geom_hash,
        "n_nodes": len(NODES_2D),
        "n_links": len(LINKS),
        "nodes_2d": NODES_2D,
        "links": LINKS,
        "static_checks": checks,
        "path_analysis": path_analysis,
        "scene": {
            "src": [SRC_X, SRC_Y],
            "mass": [MASS_X, MASS_Y],
            "impact_parameter_px": MASS_Y - SRC_Y,
            "mass_r": MASS_R,
        },
        "gr_bezier_ctrl_panel_local": GR_CTRL,
        "bcc_bezier_ctrl_panel_local": BCC_CTRL,
        "path_note": (
            "Artist-selected cubic Beziers. Source above mass (nonzero impact parameter). "
            "Initial tangent horizontal; outgoing deflected downward toward mass "
            "(attractive schematic). Distinct left/right shapes. NOT geodesic integrations."
        ),
        "load_note": (
            "Load colours: artist-selected Gaussian near mass × temporal envelope. "
            "Illustrative only — not a capacity simulation. Active links are BCC NN only."
        ),
        "v1_preserved": "not released (lensing_comparison_preview.mp4)",
    }, indent=2))

    bounds_all = []
    print(f"Rendering v2: {N_FRAMES} frames at {W}x{H} @{FPS}fps ...")
    print("Path analysis:", json.dumps(path_analysis, indent=2))
    for fi in range(N_FRAMES):
        img = render_frame(fi, geom_hash, bounds_all)
        img.save(FRAMES_DIR / f"frame_{fi:05d}.png")
        if fi % 60 == 0:
            print(f"  frame {fi}/{N_FRAMES}")

    oob = []
    for fr in bounds_all:
        for it in fr["items"]:
            if not it["in_frame"]:
                oob.append({"frame": fr["frame"], **it})
    print(f"Text OOB count: {len(oob)}")

    print("Encoding H.264 yuv420p ...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%05d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-profile:v", "high",
        "-crf", "18",
        "-movflags", "+faststart",
        "-an",
        str(MP4_PATH),
    ]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    probe = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,avg_frame_rate,nb_frames,duration,codec_name,pix_fmt,profile",
        "-show_entries", "format=duration,size,bit_rate",
        "-of", "json",
        str(MP4_PATH),
    ], text=True)
    probe_j = json.loads(probe)

    print("Full decode check ...")
    dec = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(MP4_PATH), "-f", "null", "-"],
        capture_output=True, text=True,
    )
    decode_ok = dec.returncode == 0 and not dec.stderr.strip()

    sample_times = [0, 3, 6, 10, 14, 19, 24, 28, 32, 37]
    thumbs = []
    for ts in sample_times:
        fi = min(N_FRAMES - 1, int(ts * FPS))
        thumbs.append(Image.open(FRAMES_DIR / f"frame_{fi:05d}.png").resize((384, 216), Image.Resampling.LANCZOS))
    cols, rows = 5, 2
    sheet = Image.new("RGB", (cols * 384 + 20, rows * 216 + 40), (20, 22, 28))
    sd = ImageDraw.Draw(sheet)
    for i, th in enumerate(thumbs):
        r, c = divmod(i, cols)
        sheet.paste(th, (10 + c * 384, 30 + r * 216))
        sd.text((14 + c * 384, 8 + r * 216), f"t={sample_times[i]}s", font=font(16), fill=(200, 200, 200))
    sheet.save(CONTACT_PATH, quality=92)

    h = hashlib.sha256()
    with open(MP4_PATH, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()

    NOTES_PATH.write_text(f"""# Scientific notes — lensing comparison v2

## Scope
Approved release v2 of the storyboard illustration. **Conceptual only.** No new physics simulations.
v1 preview (`lensing_comparison_preview.mp4`) was not released.

## v2 depiction fixes
1. **Attractive schematic geometry:** Source placed ABOVE mass (impact parameter {MASS_Y - SRC_Y} px). Initial path tangent horizontal; outgoing tangent deflected **down** toward mass. Monotonic downward curvature near encounter; beam clear of mass disk. Dashed undeflected reference line for contrast. Distinct left/right artist Beziers — not a GR calculation.
2. **BCC nearest-eight only:** Active network/capacity links are exclusively body-center→8-corner. No cubic-frame axis edges in the active set. Nodes: {len(NODES_2D)} (expect 91). Links: {len(LINKS)} (expect 216). Rigid every frame.
3. **Right mass label:** Drawn last with opaque backing, below mass icon, clear of glow/network.

## Evidential status (unchanged)
- LEFT: established GR geometric *illustration* (not newly integrated geodesic).
- RIGHT: **proposed** fixed-BCC congestion; dashed path **Hypothetical deflection / Not a calculated prediction**.
- Core: Different descriptions of lensing; equivalence is not demonstrated.
- Footer: Conceptual illustration — not quantitative validation.

## Output
- Video: `{MP4_PATH.name}`
- SHA256: `{sha}`
- Contact: `{CONTACT_PATH.name}`
- Geometry: `{GEOM_PATH.name}`
- Renderer: `render_lensing_comparison_v2.py`
""")

    validation = {
        "version": 2,
        "mp4": MP4_PATH.name,
        "sha256": sha,
        "v1_preserved": "not released (lensing_comparison_preview.mp4)",
        "spec": {
            "width": W, "height": H, "fps": FPS,
            "duration_target_s": DURATION, "n_frames": N_FRAMES,
            "codec": "libx264", "pix_fmt": "yuv420p", "audio": None,
        },
        "ffprobe": probe_j,
        "decode_ok": decode_ok,
        "decode_stderr": dec.stderr.strip(),
        "text_oob_count": len(oob),
        "text_oob_samples": oob[:10],
        "bcc_geom_hash": geom_hash,
        "bcc_n_nodes": len(NODES_2D),
        "bcc_n_links": len(LINKS),
        "bcc_static_checks_failed": [c for c in checks if not c.get("ok")],
        "path_analysis": path_analysis,
        "paths_are_artist_beziers": True,
        "physics_simulation": False,
        "contact_sheet": CONTACT_PATH.name,
        "notes": NOTES_PATH.name,
        "renderer": "render_lensing_comparison_v2.py",
    }
    VALIDATION_PATH.write_text(json.dumps(validation, indent=2))
    print(json.dumps({
        "mp4": validation["mp4"],
        "sha256": sha,
        "decode_ok": decode_ok,
        "text_oob": len(oob),
        "n_nodes": len(NODES_2D),
        "n_links": len(LINKS),
        "path_ok_GR": path_analysis["GR"]["outgoing_deflected_down"] and path_analysis["GR"]["initial_horizontal"],
        "path_ok_BCC": path_analysis["BCC"]["outgoing_deflected_down"] and path_analysis["BCC"]["initial_horizontal"],
    }, indent=2))
    print("DONE v2")


if __name__ == "__main__":
    main()
