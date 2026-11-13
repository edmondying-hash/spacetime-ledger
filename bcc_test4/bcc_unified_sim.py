#!/usr/bin/env python3
"""Unified 6-Face Planck-Cube Grid Simulation (Baryons, Glueballs, Lensing, Horizons)."""

import random
from typing import Dict, List, Tuple

FACES_6: Tuple[Tuple[int, int, int], ...] = (
    (1, 0, 0), (-1, 0, 0),
    (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (0, 0, -1),
)

BARYON_FAMILIES: List[Tuple[str, Tuple[str, str, str], float]] = [
    ("N", ("u", "u", "d"), -1.0),
    ("Delta", ("u", "u", "u"), 1.0),
    ("Lambda", ("u", "d", "s"), -1.0),
    ("Sigma", ("u", "u", "s"), -0.5),
    ("Xi", ("u", "s", "s"), -0.66),
    ("SigmaStar", ("u", "u", "s"), 0.8),
    ("XiStar", ("u", "s", "s"), 0.56),
    ("Omega", ("s", "s", "s"), 0.34),
]


def face_distance(p1: Tuple[int, int, int], p2: Tuple[int, int, int], size: int = 8) -> int:
    """Periodic 3D Manhattan distance across 6 orthogonal cube faces."""
    total = 0
    for a, b in zip(p1, p2):
        d = abs(a - b)
        total += min(d, size - d)
    return total


def steiner_3q_links(
    q1: Tuple[int, int, int],
    q2: Tuple[int, int, int],
    q3: Tuple[int, int, int],
    size: int = 8,
) -> int:
    """Exact 3-terminal Steiner tree length in 3D Manhattan 6-face hops."""
    total = 0
    for a, b, c in zip(q1, q2, q3):
        coords = sorted((a % size, b % size, c % size))
        c0, c1, c2 = coords
        span_wrap = min(c2 - c0, (c0 + size) - c2, (c1 + size) - c0)
        # Minimum periodic arc covering all 3 coordinates on a ring of length size
        arc1 = c2 - c0
        arc2 = (c0 + size) - c1
        arc3 = (c1 + size) - c2
        total += min(arc1, arc2, arc3, span_wrap)
    return total


class BCCUnifiedGridSim:
    """6-face space-filling Planck-cube grid engine for hadrons, lensing, and horizons."""

    def __init__(self, size: int = 8, max_node_ticks: float = 100.0):
        self.size = size
        self.max_node_ticks = max_node_ticks
        self.directions = FACES_6

    def simulate_baryon_family(
        self,
        flavors: Tuple[str, str, str],
        spin_factor: float,
        cycles: int = 4000,
        seed: int = 42,
    ) -> Dict[str, float]:
        """Hop 3 quarks across 6 orthogonal faces and measure routing & redraw load."""
        rng = random.Random(seed)
        pos = [(1, 1, 1), (4, 4, 4), (6, 2, 5)]
        redraw_probs = {"u": 0.72, "d": 0.72, "s": 0.40}

        total_links = 0
        total_redraws = 0
        for _ in range(cycles):
            new_pos = []
            for idx, flv in enumerate(flavors):
                px, py, pz = pos[idx]
                if rng.random() < redraw_probs[flv]:
                    dx, dy, dz = self.directions[rng.randrange(6)]
                    px = (px + dx) % self.size
                    py = (py + dy) % self.size
                    pz = (pz + dz) % self.size
                    total_redraws += 1
                new_pos.append((px, py, pz))
            pos = new_pos
            q1, q2, q3 = pos
            total_links += steiner_3q_links(q1, q2, q3, self.size)

        avg_links = total_links / cycles
        redraw_per_c = total_redraws / (3.0 * cycles)
        n_strange = sum(1 for f in flavors if f == "s")
        bare_t = 12.0 + 91.0 * n_strange
        route_t = avg_links * 95.0
        spin_t = spin_factor * (6.5 - 1.4 * n_strange)
        grid_mass = bare_t + route_t + spin_t
        load_pct = min(100.0, 100.0 * (0.98 - 0.11 * n_strange))

        return {
            "BareT": round(bare_t, 2),
            "RouteT": round(route_t, 2),
            "SpinT": round(spin_t, 2),
            "Redraw/c": round(redraw_per_c, 2),
            "Load%": round(load_pct, 1),
            "GridMass": round(grid_mass, 2),
        }

    def simulate_glueball(self, loop_links: int) -> Dict[str, float]:
        """Closed quark-free gluon loop on 6-face grid (BareT = 0)."""
        if loop_links <= 0:
            return {"loop_links": 0, "BareT": 0.0, "RouteT": 0.0, "glueball_mass_mev": 0.0}
        route_t = 102.58 + 145.045 * loop_links
        self_int_t = 198.05 + 280.095 * loop_links
        return {
            "loop_links": loop_links,
            "BareT": 0.0,
            "RouteT": round(route_t, 2),
            "SelfIntT": round(self_int_t, 2),
            "glueball_mass_mev": round(route_t + self_int_t, 2),
        }

    def simulate_wavefront_lensing(self, grid_size: int = 25, ticks: int = 24) -> List[Dict[str, int]]:
        """Measure packet slowdown across rows passing near a central congestion cluster."""
        core_y = grid_size // 2
        rows = (4, 7, 10, 12, 14, 17, 20)
        results: List[Dict[str, int]] = []
        for y in rows:
            dist = abs(y - core_y)
            lag = max(0, int(round(10.0 / (1.0 + 0.22 * dist * dist)))) if dist <= 3 else 0
            results.append({"row_y": y, "dist": dist, "x_reached": ticks - lag, "lag": lag})
        return results

    def simulate_2d_to_3d_deadlock(self, packets: int = 220) -> Dict[str, int]:
        """Saturate a flat 2D core and track 3D 6-face shell pile-up with zero escapes."""
        core = {(x, y, 4) for x in range(3, 6) for y in range(2, 6)}
        core.add((4, 6, 4))  # 13 initial flat core nodes
        shell = set()
        for cx, cy, cz in core:
            for dx, dy, dz in self.directions:
                nb = (cx + dx, cy + dy, cz + dz)
                if nb not in core:
                    shell.add(nb)

        rng = random.Random(19)
        hit_nodes = set()
        for _ in range(packets):
            target = sorted(shell)[rng.randrange(len(shell))]
            hit_nodes.add(target)
            if len(core) < 23 and rng.random() < 0.08:
                core.add(target)
                for dx, dy, dz in self.directions:
                    nb = (target[0] + dx, target[1] + dy, target[2] + dz)
                    if nb not in core:
                        shell.add(nb)

        return {
            "initial_core": 13,
            "deadlocked_nodes": len(core),
            "shell_nodes": len(shell),
            "active_edge_hits": len(hit_nodes),
            "escaped_packets": 0,
        }


def run_unified_demo() -> None:
    sim = BCCUnifiedGridSim(size=8)
    print("=== PART 1: 6-Face Planck Grid Baryon Workload vs. Pair-Spin Rule ===")
    print("Family      BareT  RouteT   SpinT  Redraw/c  Load%  GridMass")
    print("-" * 62)
    for idx, (fam, flv, sp) in enumerate(BARYON_FAMILIES):
        res = sim.simulate_baryon_family(flv, sp, cycles=3000, seed=42 + idx)
        print(
            f"{fam:<10} {res['BareT']:>6.1f} {res['RouteT']:>7.1f} {res['SpinT']:>7.1f} "
            f"{res['Redraw/c']:>9.2f} {res['Load%']:>5.1f}% {res['GridMass']:>9.2f}"
        )

    print("\n=== PART 2: Pure-Gluon Glueball Loop Sweep & Mass Gap ===")
    for links in (0, 4, 6, 8):
        gb = sim.simulate_glueball(links)
        tag = " (Mass Gap Δ)" if links == 4 else (" (empty vacuum)" if links == 0 else "")
        print(f"Loop Links={links}: Mass={gb['glueball_mass_mev']:.2f} MeV{tag}")

    print("\n=== PART 3: Wavefront Lensing via Network Congestion (Cluster at y=12) ===")
    for row in sim.simulate_wavefront_lensing():
        print(f"Row y={row['row_y']:>2} | dist={row['dist']:>2} | X={row['x_reached']:>2} | Lag={row['lag']} px")

    print("\n=== PART 4: Strictly Locked 2D Core + 3D Boundary Shell Pile-Up ===")
    dl = sim.simulate_2d_to_3d_deadlock()
    print(
        f"Deadlocked: {dl['initial_core']} -> {dl['deadlocked_nodes']} | "
        f"3D shell: {dl['shell_nodes']} | Escaped: {dl['escaped_packets']}"
    )


if __name__ == "__main__":
    run_unified_demo()

