#!/usr/bin/env python3
"""Animated 3D GIF of 3 Quarks Hopping Across 8 BCC Diagonals & Redrawing Steiner Tree."""

import argparse
from collections import deque
import itertools
import random
from typing import Dict, List, Tuple
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

Coord3D = Tuple[int, int, int]
BCC_DIAGONALS_8: Tuple[Coord3D, ...] = tuple(itertools.product((-1, 1), repeat=3))


def build_bounded_bcc(low: int = -2, high: int = 3) -> Tuple[List[Coord3D], Dict[Coord3D, Dict[Coord3D, List[Coord3D]]]]:
    """Build valid 3D BCC nodes in [low, high] and shortest diagonal paths via BFS."""
    nodes = [
        (x, y, z)
        for x in range(low, high + 1)
        for y in range(low, high + 1)
        for z in range(low, high + 1)
        if (x % 2) == (y % 2) == (z % 2)
    ]
    node_set = set(nodes)
    paths: Dict[Coord3D, Dict[Coord3D, List[Coord3D]]] = {}

    for src in nodes:
        src_paths: Dict[Coord3D, List[Coord3D]] = {src: [src]}
        queue = deque([src])
        while queue:
            curr = queue.popleft()
            cx, cy, cz = curr
            for dx, dy, dz in BCC_DIAGONALS_8:
                nb = (cx + dx, cy + dy, cz + dz)
                if nb in node_set and nb not in src_paths:
                    src_paths[nb] = src_paths[curr] + [nb]
                    queue.append(nb)
        paths[src] = src_paths
    return nodes, paths


def exact_steiner_tree(
    quarks: List[Coord3D],
    nodes: List[Coord3D],
    paths: Dict[Coord3D, Dict[Coord3D, List[Coord3D]]],
) -> Tuple[Coord3D, List[List[Coord3D]], int]:
    """Find optimal BCC Y-junction node minimizing total diagonal gluon links."""
    q1, q2, q3 = quarks
    best_junction = nodes[0]
    best_links = 10**9

    for j in nodes:
        cost = (len(paths[q1][j]) - 1) + (len(paths[q2][j]) - 1) + (len(paths[q3][j]) - 1)
        if cost < best_links:
            best_links = cost
            best_junction = j

    branches = [paths[q1][best_junction], paths[q2][best_junction], paths[q3][best_junction]]
    return best_junction, branches, best_links


def generate_bcc_gif(
    out_path: str = "bcc_quark_hopping.gif",
    frames: int = 50,
    fps: int = 5,
    seed: int = 42,
) -> None:
    low, high = -2, 3
    nodes, paths = build_bounded_bcc(low, high)
    node_set = set(nodes)
    rng = random.Random(seed)

    quarks: List[Coord3D] = [(-1, -1, -1), (1, -1, 1), (2, 2, 0)]
    labels = ("u1", "u2", "d")
    colors = ("#2a9d8f", "#219ebc", "#e76f51")
    redraw_prob = 0.72

    # Pre-simulate trajectory so every frame is deterministic and smooth
    history = []
    for tick in range(frames):
        if tick > 0:
            next_quarks = []
            for q in quarks:
                if rng.random() < redraw_prob:
                    valid_moves = [
                        (q[0] + dx, q[1] + dy, q[2] + dz)
                        for dx, dy, dz in BCC_DIAGONALS_8
                        if (q[0] + dx, q[1] + dy, q[2] + dz) in node_set
                    ]
                    next_quarks.append(valid_moves[rng.randrange(len(valid_moves))])
                else:
                    next_quarks.append(q)
            quarks = next_quarks

        junction, branches, total_links = exact_steiner_tree(quarks, nodes, paths)
        route_mev = total_links * 198.0
        total_mev = 12.0 + route_mev - 6.5
        history.append((tick, list(quarks), junction, branches, total_links, total_mev))

    fig = plt.figure(figsize=(8.5, 7.2))
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    b_arr = np.array(nodes)

    def update(frame_idx: int) -> None:
        ax.clear()
        tick, q_list, junction, branches, n_links, mass_mev = history[frame_idx]

        # Plot idle BCC background nodes
        ax.scatter(b_arr[:, 0], b_arr[:, 1], b_arr[:, 2], s=18, color="#adb5bd", alpha=0.35)

        # Plot active gluon Steiner flux tree branches
        for b_idx, branch in enumerate(branches):
            if len(branch) > 1:
                p_arr = np.array(branch)
                ax.plot(
                    p_arr[:, 0], p_arr[:, 1], p_arr[:, 2],
                    color="#f77f00", linewidth=3.8,
                    label="Gluon Steiner Flux Links" if b_idx == 0 else "",
                )

        # Plot Steiner Y-junction node
        jx, jy, jz = junction
        ax.scatter(
            (jx,), (jy,), (jz,),
            s=150, color="#d62828", edgecolors="black", zorder=9,
            label=f"Steiner Junction {junction}",
        )

        # Plot 3 hopping valence quarks
        for q_idx, (qx, qy, qz) in enumerate(q_list):
            ax.scatter(
                (qx,), (qy,), (qz,),
                s=165, color=colors[q_idx], edgecolors="black", zorder=10,
                label=f"Quark {labels[q_idx]} {(qx, qy, qz)}",
            )
            ax.text(qx + 0.14, qy + 0.14, qz + 0.14, labels[q_idx], fontsize=9, fontweight="bold")

        ax.set_title(
            f"3D BCC Quark Hopping & Dynamic Steiner Flux Tree\n"
            f"Tick {tick:02d}/{frames - 1:02d} | Active Gluon Links = {n_links} | "
            f"Instantaneous Mass = {mass_mev:.1f} MeV",
            fontsize=10.5,
            fontweight="bold",
        )
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_xlim(low - 0.3, high + 0.3)
        ax.set_ylim(low - 0.3, high + 0.3)
        ax.set_zlim(low - 0.3, high + 0.3)
        # Slow smooth camera orbit so 3D depth stays easy to read
        ax.view_init(elev=22, azim=35 + frame_idx * 1.4)
        ax.legend(loc="upper left", fontsize=7.5)

    print(f"Rendering {frames}-frame 3D BCC animation...")
    anim = animation.FuncAnimation(fig, update, frames=frames, interval=1000 // fps)
    anim.save(out_path, writer=animation.PillowWriter(fps=fps), dpi=130)
    plt.close(fig)
    print(f"[Saved animated 3D GIF -> {out_path}]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export animated GIF of 3D BCC quark hopping")
    parser.add_argument("--out", type=str, default="bcc_quark_hopping.gif", help="Output GIF path")
    parser.add_argument("--frames", type=int, default=50, help="Number of ticks/frames")
    parser.add_argument("--fps", type=int, default=5, help="Frames per second")
    args = parser.parse_args()
    generate_bcc_gif(out_path=args.out, frames=args.frames, fps=args.fps)


if __name__ == "__main__":
    main()
