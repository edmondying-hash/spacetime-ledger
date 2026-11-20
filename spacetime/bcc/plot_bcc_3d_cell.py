#!/usr/bin/env python3
"""4-Panel 3D Wireframe: BCC Unit Cell, Truncated Octahedron, Steiner Tree & Glueball."""

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
import bcc_config as cfg  # noqa: E402


import argparse
import itertools
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def draw_cube_wireframe(ax, low: float = -1.0, high: float = 1.0, color: str = "#8d99ae") -> None:
    """Draw faint reference edges of a bounding cube."""
    pts = list(itertools.product((low, high), repeat=3))
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if sum(1 for a, b in zip(pts[i], pts[j]) if a != b) == 1:
                xs, ys, zs = zip(pts[i], pts[j])
                ax.plot(xs, ys, zs, linestyle=":", linewidth=1.0, color=color, alpha=0.55)


def build_truncated_octahedron_faces() -> list:
    """Return the 14 faces (8 hexagons + 6 squares) of the BCC Voronoi cell at (0,0,0)."""
    verts = set()
    for px, py, pz in itertools.permutations((0.0, 0.5, 1.0)):
        for sx, sy, sz in itertools.product((-1.0, 1.0), repeat=3):
            verts.add((px * sx, py * sy, pz * sz))
    vert_list = list(verts)

    def sort_face(face_pts, normal):
        center = np.mean(face_pts, axis=0)
        nx, ny, nz = normal
        n = np.array((nx, ny, nz), dtype=float)
        n /= np.linalg.norm(n)
        ref = np.array((1.0, 0.0, 0.0)) if abs(nx) < 0.9 else np.array((0.0, 1.0, 0.0))
        u = np.cross(n, ref)
        u /= np.linalg.norm(u)
        v = np.cross(n, u)
        return sorted(
            face_pts,
            key=lambda pt: math.atan2(
                np.dot(np.array(pt) - center, v), np.dot(np.array(pt) - center, u)
            ),
        )

    faces = []
    # 6 Square faces perpendicular to (+-1, 0, 0), (0, +-1, 0), (0, 0, +-1)
    for axis in range(3):
        for val in (-1.0, 1.0):
            sq = [pt for pt in vert_list if abs(pt[axis] - val) < 1e-6]
            normal = [0.0, 0.0, 0.0]
            normal[axis] = val
            faces.append(sort_face(sq, tuple(normal)))

    # 8 Hexagonal faces perpendicular to (+-1, +-1, +-1) diagonal links
    for sx, sy, sz in itertools.product((-1.0, 1.0), repeat=3):
        hx = [
            pt
            for pt in vert_list
            if abs(sx * pt[0] + sy * pt[1] + sz * pt[2] - 1.5) < 1e-6
        ]
        faces.append(sort_face(hx, (sx, sy, sz)))

    return faces



def plot_bcc_3d(out_path: str = "bcc_3d_wireframe.png", interactive: bool = False) -> None:
    fig = plt.figure(figsize=(15, 12))
    corners = list(itertools.product((-1, 1), repeat=3))

    # -------------------------------------------------------------------------
    # PANEL 1: Fundamental 3D BCC Unit Cell (1 Center Node + 8 Corner Diagonals)
    # -------------------------------------------------------------------------
    ax1 = fig.add_subplot(2, 2, 1, projection="3d")
    draw_cube_wireframe(ax1, -1.0, 1.0)

    for cx, cy, cz in corners:
        ax1.plot((0, cx), (0, cy), (0, cz), color="#1d3557", linewidth=2.4, alpha=0.9)

    c_arr = np.array(corners)
    ax1.scatter(
        c_arr[:, 0], c_arr[:, 1], c_arr[:, 2],
        s=90, color="#457b9d", edgecolors="black", depthshade=False,
        label="8 Corner Neighbors (±1, ±1, ±1)",
    )
    ax1.scatter(
        (0,), (0,), (0,),
        s=170, color="#e63946", edgecolors="black", zorder=10,
        label="Center Node (0, 0, 0)",
    )

    ax1.set_title("1. 3D BCC Unit Cell (8 Body Diagonals)", fontsize=11.5, fontweight="bold")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_zlabel("Z")
    ax1.set_xlim(-1.3, 1.3)
    ax1.set_ylim(-1.3, 1.3)
    ax1.set_zlim(-1.3, 1.3)
    ax1.view_init(elev=20, azim=35)
    ax1.legend(loc="upper left", fontsize=8)

    # -------------------------------------------------------------------------
    # PANEL 2: BCC Node Territory = Truncated Octahedron (volume from bcc_config.HOP, OD1)
    # -------------------------------------------------------------------------
    ax2 = fig.add_subplot(2, 2, 2, projection="3d")
    faces = build_truncated_octahedron_faces()

    poly = Poly3DCollection(
        faces,
        facecolors="#48cae4",
        edgecolors="#023e8a",
        linewidths=1.3,
        alpha=0.22,
    )
    ax2.add_collection3d(poly)

    # Show the 8 diagonal links piercing through the 8 hexagonal face centers
    for cx, cy, cz in corners:
        ax2.plot((0, cx * 0.75), (0, cy * 0.75), (0, cz * 0.75), color="#e63946", linewidth=2.0)

    ax2.scatter((0,), (0,), (0,), s=160, color="#e63946", edgecolors="black", zorder=10, label=f"Node cell = {cfg.DERIVED['cell_volume_VP']:.3f} V_P (HOP={cfg.HOP})")
    ax2.set_title("2. BCC Node Voronoi Cell: Truncated Octahedron", fontsize=11.5, fontweight="bold")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.set_zlabel("Z")
    ax2.set_xlim(-1.15, 1.15)
    ax2.set_ylim(-1.15, 1.15)
    ax2.set_zlim(-1.15, 1.15)
    ax2.view_init(elev=22, azim=38)
    ax2.legend(loc="upper left", fontsize=8)
    # -------------------------------------------------------------------------
    # PANEL 3: 3-Quark Gluon Steiner Routing Tree on 3D BCC Lattice
    # -------------------------------------------------------------------------
    ax3 = fig.add_subplot(2, 2, 3, projection="3d")

    bcc_sites = [
        (x, y, z)
        for x in range(-1, 3)
        for y in range(-1, 3)
        for z in range(-1, 3)
        if (x % 2) == (y % 2) == (z % 2)
    ]
    b_arr = np.array(bcc_sites)
    ax3.scatter(
        b_arr[:, 0], b_arr[:, 1], b_arr[:, 2],
        s=22, color="#adb5bd", alpha=0.45, label="Idle Vacuum BCC Nodes",
    )

    bcc_set = set(bcc_sites)
    for x, y, z in bcc_sites:
        for dx, dy, dz in corners:
            nx, ny, nz = x + dx, y + dy, z + dz
            if (nx, ny, nz) in bcc_set and (x, y, z) < (nx, ny, nz):
                ax3.plot((x, nx), (y, ny), (z, nz), color="#ced4da", linewidth=0.6, alpha=0.35)

    quarks = {
        "u1 (-1,-1,-1)": (-1, -1, -1),
        "u2 (1,-1,1)": (1, -1, 1),
        "d  (2,2,0)": (2, 2, 0),
    }
    steiner_paths = (
        ((-1, -1, -1), (0, 0, 0)),
        ((1, -1, 1), (0, 0, 0)),
        ((2, 2, 0), (1, 1, 1), (0, 0, 0)),
    )

    for idx, path in enumerate(steiner_paths):
        p_arr = np.array(path)
        ax3.plot(
            p_arr[:, 0], p_arr[:, 1], p_arr[:, 2],
            color="#f77f00", linewidth=3.5,
            label="Gluon Steiner Flux Links (4 Hops)" if idx == 0 else "",
        )

    ax3.scatter((1,), (1,), (1,), s=70, color="#fcbf49", edgecolors="black", label="Relay Node (1,1,1)")
    ax3.scatter((0,), (0,), (0,), s=155, color="#d62828", edgecolors="black", label="Steiner Y-Junction (0,0,0)")

    q_coords = np.array(list(quarks.values()))
    ax3.scatter(
        q_coords[:, 0], q_coords[:, 1], q_coords[:, 2],
        s=145, color="#2a9d8f", edgecolors="black", zorder=10,
        label="3 Valence Quarks (u, u, d)",
    )
    for name, (qx, qy, qz) in quarks.items():
        ax3.text(qx + 0.14, qy + 0.14, qz + 0.14, name, fontsize=8.5, fontweight="bold")

    ax3.set_title("3. 3-Quark Steiner Tree (4 Diagonal Links)", fontsize=11.5, fontweight="bold")
    ax3.set_xlabel("X")
    ax3.set_ylabel("Y")
    ax3.set_zlabel("Z")
    ax3.set_xlim(-1.4, 2.4)
    ax3.set_ylim(-1.4, 2.4)
    ax3.set_zlim(-1.4, 2.4)
    ax3.view_init(elev=25, azim=65)
    ax3.legend(loc="upper left", fontsize=7.5)

    # -------------------------------------------------------------------------
    # PANEL 4: Minimal 4-Link Non-Planar Glueball Rhombus (Pure-Gluon Mass Gap)
    # -------------------------------------------------------------------------
    ax4 = fig.add_subplot(2, 2, 4, projection="3d")

    ax4.scatter(
        b_arr[:, 0], b_arr[:, 1], b_arr[:, 2],
        s=22, color="#adb5bd", alpha=0.45, label="Idle Vacuum BCC Nodes",
    )
    for x, y, z in bcc_sites:
        for dx, dy, dz in corners:
            nx, ny, nz = x + dx, y + dy, z + dz
            if (nx, ny, nz) in bcc_set and (x, y, z) < (nx, ny, nz):
                ax4.plot((x, nx), (y, ny), (z, nz), color="#ced4da", linewidth=0.6, alpha=0.35)

    glueball_cycle = (
        (0, 0, 0),
        (1, 1, 1),
        (2, 0, 0),
        (1, -1, -1),
        (0, 0, 0),
    )
    g_arr = np.array(glueball_cycle)
    ax4.plot(
        g_arr[:, 0], g_arr[:, 1], g_arr[:, 2],
        color="#7209b7", linewidth=3.8,
        label="4-Link Non-Planar Gluon Cycle",
    )

    unique_loop_nodes = glueball_cycle[:-1]
    u_arr = np.array(unique_loop_nodes)
    ax4.scatter(
        u_arr[:, 0], u_arr[:, 1], u_arr[:, 2],
        s=155, color="#b5179e", edgecolors="black", zorder=10,
        label="Active Gluon Self-Int Nodes (4)",
    )
    for lx, ly, lz in unique_loop_nodes:
        ax4.text(lx + 0.14, ly + 0.14, lz + 0.14, f"({lx},{ly},{lz})", fontsize=8.5, fontweight="bold")

    ax4.set_title("4. Pure-Gluon Glueball Rhombus (Mass Gap Δ)", fontsize=11.5, fontweight="bold")
    ax4.set_xlabel("X")
    ax4.set_ylabel("Y")
    ax4.set_zlabel("Z")
    ax4.set_xlim(-1.4, 2.4)
    ax4.set_ylim(-1.4, 2.4)
    ax4.set_zlim(-1.4, 2.4)
    ax4.view_init(elev=18, azim=125)
    ax4.legend(loc="upper left", fontsize=7.5)

    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    plt.savefig(out_path, dpi=200)
    print(f"[Saved 4-panel 3D BCC wireframe plot -> {out_path}]")
    if interactive:
        plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render 4-panel 3D BCC lattice wireframe")
    parser.add_argument("--out", type=str, default="bcc_3d_wireframe.png", help="Output PNG path")
    parser.add_argument("--show", action="store_true", help="Open interactive 3D rotatable window")
    args = parser.parse_args()
    plot_bcc_3d(out_path=args.out, interactive=args.show)


if __name__ == "__main__":
    main()
