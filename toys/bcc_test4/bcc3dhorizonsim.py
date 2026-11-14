#!/usr/bin/env python3
"""Standalone 3D Horizon & Network-Deadlock Simulator on a 6-Face Planck-Cube Grid.

Models event horizons as complete I/O saturation (workload >= max_node_ticks) across
space-filling 1.0 l_P^3 Planck cubes connected via 6 orthogonal faces (±x, ±y, ±z).
Incoming 3D packets pile up symmetrically on the outer 3D boundary shell with zero
central point singularity and zero escapes.
"""
import argparse
import json
import random

FACE_DIRS_6 = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1),
]


class BCC3DHorizonSim:
    """3D 6-face Planck-cube network-deadlock horizon and shell accretion solver."""

    def __init__(self, size=19, max_node_ticks=100, seed=42):
        self.size = size
        self.max_ticks = max_node_ticks
        self.source_rho = [[[0.0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.workload = [[[0.0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.deadlocked = set()
        self.rng = random.Random(seed)

    def inject_3d_core(self, cx, cy, cz, total_workload, radius=1):
        """Inject a localized 3D mass+momentum core centered at (cx, cy, cz)."""
        core_nodes = []
        for dz in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx * dx + dy * dy + dz * dz <= radius * radius:
                        x, y, z = cx + dx, cy + dy, cz + dz
                        if 1 <= x < self.size - 1 and 1 <= y < self.size - 1 and 1 <= z < self.size - 1:
                            core_nodes.append((x, y, z))

        per_node = total_workload / max(1, len(core_nodes))
        for x, y, z in core_nodes:
            self.source_rho[z][y][x] += per_node

    def relax_3d_congestion(self, iterations=250):
        """Relax the 6-face 3D discrete Laplacian and mark network-deadlocked nodes."""
        L = self.size
        W = [[[0.0 for _ in range(L)] for _ in range(L)] for _ in range(L)]

        for _ in range(iterations):
            next_W = [[[0.0 for _ in range(L)] for _ in range(L)] for _ in range(L)]
            for z in range(1, L - 1):
                for y in range(1, L - 1):
                    for x in range(1, L - 1):
                        nbr_sum = (
                            W[z][y][x - 1]
                            + W[z][y][x + 1]
                            + W[z][y - 1][x]
                            + W[z][y + 1][x]
                            + W[z - 1][y][x]
                            + W[z + 1][y][x]
                        )
                        next_W[z][y][x] = (nbr_sum + self.source_rho[z][y][x]) / 6.0
            W = next_W

        self.workload = W
        self.deadlocked.clear()
        for z in range(L):
            for y in range(L):
                for x in range(L):
                    if self.workload[z][y][x] >= self.max_ticks:
                        self.deadlocked.add((x, y, z))

    def get_3d_boundary_shell(self):
        """Return non-deadlocked 3D nodes 1 orthogonal face step outside the deadlocked horizon."""
        shell = set()
        for x, y, z in self.deadlocked:
            for dx, dy, dz in FACE_DIRS_6:
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx < self.size and 0 <= ny < self.size and 0 <= nz < self.size:
                    if (nx, ny, nz) not in self.deadlocked:
                        shell.add((nx, ny, nz))
        return shell

    def step_accretion(self, incoming_packets=260, packet_load=25, checkpoints=(50, 100, 200, 300)):
        """Route incoming 3D packets onto the 3D horizon shell under complete network deadlock."""
        edge_hits = {}
        history = []

        for step in range(1, incoming_packets + 1):
            boundary = sorted(self.get_3d_boundary_shell())
            if not boundary:
                break
            tx, ty, tz = self.rng.choice(boundary)
            self.workload[tz][ty][tx] += packet_load
            edge_hits[(tx, ty, tz)] = edge_hits.get((tx, ty, tz), 0) + 1
            if self.workload[tz][ty][tx] >= self.max_ticks:
                self.deadlocked.add((tx, ty, tz))

            if step in checkpoints:
                history.append({
                    'packets_absorbed': step,
                    'deadlocked_nodes': len(self.deadlocked),
                    'exposed_shell_nodes': len(self.get_3d_boundary_shell()),
                })

        xs = [x for x, _, _ in self.deadlocked]
        ys = [y for _, y, _ in self.deadlocked]
        zs = [z for _, _, z in self.deadlocked]
        span = (max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, max(zs) - min(zs) + 1) if xs else (0, 0, 0)

        return {
            'total_deadlocked': len(self.deadlocked),
            'exposed_3d_shell': len(self.get_3d_boundary_shell()),
            'active_edge_nodes_hit': len(edge_hits),
            'escaped_packets': 0,
            'span_xyz': span,
            'checkpoints': history,
        }

    def radial_horizon_profile(self, cx, cy, cz, max_r=6):
        """Probe workload, status, and queueing delay along +x from core center (cx, cy, cz)."""
        profile = []
        for r in range(0, max_r + 1):
            x = cx + r
            if x >= self.size:
                break
            w_val = self.workload[cz][cy][x]
            is_locked = (x, cy, cz) in self.deadlocked or w_val >= self.max_ticks
            delay = None if is_locked else int((w_val / self.max_ticks) * 4)
            profile.append({
                'r': r,
                'pos': (x, cy, cz),
                'workload': round(w_val, 2),
                'status': 'DEADLOCKED / BLOCKED' if is_locked else 'Active I/O',
                'extra_tick_delay': delay,
            })
        return profile


def run_3d_horizon_demo(size=19, total_workload=2400.0, incoming_packets=300, seed=42):
    c = size // 2
    sim = BCC3DHorizonSim(size=size, max_node_ticks=100, seed=seed)
    sim.inject_3d_core(c, c, c, total_workload=total_workload, radius=1)
    sim.relax_3d_congestion(iterations=250)

    init_core = len(sim.deadlocked)
    init_shell = len(sim.get_3d_boundary_shell())
    stats = sim.step_accretion(incoming_packets=incoming_packets, packet_load=25)
    profile = sim.radial_horizon_profile(c, c, c, max_r=min(6, size - c - 1))

    print("=== STANDALONE 3D HORIZON & NETWORK-DEADLOCK SIMULATION ===")
    print(f"Grid: {size}x{size}x{size} (6-face 1.0 l_P^3 Planck cubes) | Initial core: {init_core} nodes (shell: {init_shell})")
    print(f"Post-infall deadlocked nodes: {stats['total_deadlocked']} | Exposed 3D shell: {stats['exposed_3d_shell']} | Escaped: {stats['escaped_packets']}")
    print(f"3D Bounding Volume (X x Y x Z): {stats['span_xyz']}")
    print("Radius r   Node (x,y,z)   Workload   Horizon Status         Tick Delay")
    print("-" * 72)
    for row in profile:
        delay_str = "BLOCKED (0 escape)" if row['extra_tick_delay'] is None else f"+{row['extra_tick_delay']} ticks"
        print(f"{row['r']:8d}   {str(row['pos']):>12}   {row['workload']:8.2f}   {row['status']:<20}   {delay_str}")

    return {
        'initial_core_nodes': init_core,
        'initial_shell_nodes': init_shell,
        'accretion_stats': stats,
        'radial_profile': profile,
    }


def main():
    parser = argparse.ArgumentParser(description="Standalone 3D 6-Face Horizon & Network-Deadlock Simulator")
    parser.add_argument("--size", type=int, default=19, help="Cubic grid dimension (default: 19)")
    parser.add_argument("--workload", type=float, default=2400.0, help="Initial core workload (default: 2400.0)")
    parser.add_argument("--packets", type=int, default=300, help="Incoming 3D infall packets (default: 300)")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic RNG seed (default: 42)")
    parser.add_argument("--json-out", type=str, default=None, help="Optional path to export JSON output")
    args = parser.parse_args()

    result = run_3d_horizon_demo(
        size=args.size,
        total_workload=args.workload,
        incoming_packets=args.packets,
        seed=args.seed,
    )
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"Exported horizon snapshot to {args.json_out}")


if __name__ == "__main__":
    main()
