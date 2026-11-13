#!/usr/bin/env python3
"""3D BCC Horizon Simulation: Flat 2D Deadlocked Core + 3D Volumetric Edge Shell."""
import math
import random

BCC_DIRS_3D = [
    (dx, dy, dz)
    for dx in (-1, 1)
    for dy in (-1, 1)
    for dz in (-1, 1)
]


class BCC3DHorizonSim:
    def __init__(self, size=15, max_node_ticks=100, seed=42):
        self.size = size
        self.max_ticks = max_node_ticks
        # 3D BCC load grid: load[z][y][x]
        self.load = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.deadlocked = set()
        self.rng = random.Random(seed)

    def seed_flat_2d_core(self, cx, cy, cz, radius=2):
        """Initialize a flat 2D deadlocked sheet in the x-y plane at z=cz."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    x, y, z = cx + dx, cy + dy, cz
                    self.load[z][y][x] = self.max_ticks + 50
                    self.deadlocked.add((x, y, z))

    def get_3d_boundary_shell(self):
        """Find all non-deadlocked 3D BCC nodes directly adjacent (1 diagonal step) to the deadlocked core."""
        shell = set()
        for (x, y, z) in self.deadlocked:
            for dx, dy, dz in BCC_DIRS_3D:
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx < self.size and 0 <= ny < self.size and 0 <= nz < self.size:
                    if (nx, ny, nz) not in self.deadlocked:
                        shell.add((nx, ny, nz))
        return shell

    def simulate_3d_infall(self, incoming_packets=220, packet_load=20):
        """Route packets from the 3D BCC volume onto the 2D core, piling up on the 3D outer edge."""
        shell_hits = {}

        for _ in range(incoming_packets):
            boundary = sorted(self.get_3d_boundary_shell())
            if not boundary:
                break
            # Incoming 3D packet hits an exposed node on the 3D boundary shell
            target = self.rng.choice(boundary)
            tx, ty, tz = target
            self.load[tz][ty][tx] += packet_load
            shell_hits[target] = shell_hits.get(target, 0) + 1

            # Once a 3D edge node saturates, it locks into the deadlocked horizon
            if self.load[tz][ty][tx] >= self.max_ticks:
                self.deadlocked.add(target)

        # Measure z-thickness (3D edge spread) vs. x-y footprint of the deadlocked region
        zs = [p[2] for p in self.deadlocked]
        xs = [p[0] for p in self.deadlocked]
        ys = [p[1] for p in self.deadlocked]

        return {
            'total_deadlocked': len(self.deadlocked),
            'exposed_3d_shell_nodes': len(self.get_3d_boundary_shell()),
            'x_span': max(xs) - min(xs) + 1,
            'y_span': max(ys) - min(ys) + 1,
            'z_thickness': max(zs) - min(zs) + 1,
            'shell_hits_count': len(shell_hits),
        }


if __name__ == '__main__':
    sim = BCC3DHorizonSim(size=15, max_node_ticks=100)
    sim.seed_flat_2d_core(cx=7, cy=7, cz=7, radius=2)
    initial_nodes = len(sim.deadlocked)
    initial_shell = len(sim.get_3d_boundary_shell())

    stats = sim.simulate_3d_infall(incoming_packets=220, packet_load=20)
    print("=== 2D Deadlocked Core + 3D Volumetric Boundary Shell ===")
    print(f"Initial flat 2D core nodes (z=7 plane): {initial_nodes}")
    print(f"Initial 3D BCC edge nodes wrapping it:  {initial_shell}")
    print(f"Deadlocked nodes after 3D infall:       {stats['total_deadlocked']}")
    print(f"Final 3D boundary shell nodes:          {stats['exposed_3d_shell_nodes']}")
    print(f"Bounding dimensions (X x Y x Z):        {stats['x_span']} x {stats['y_span']} x {stats['z_thickness']}")

