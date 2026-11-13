#!/usr/bin/env python3
"""BCC grid congestion module: gravitational lensing and I/O buffer deadlock (event horizon).

Demonstrates:
1. Sub-saturation congestion: light packets redraw slower near high-workload nodes,
   refraction-bending the wavefront inward without curving the rigid grid.
2. Full saturation (black hole deadlock): when node workload hits MAX_NODE_TICKS,
   outbound I/O blocks completely and incoming packets pile up on the perimeter shell.
"""
import math


class BCCCongestionGrid:
    def __init__(self, size=25, max_node_ticks=100):
        self.size = size
        self.max_ticks = max_node_ticks
        # Static background workload (ticks/cycle) at each grid pixel (x, y)
        self.load = [[0 for _ in range(size)] for _ in range(size)]

    def place_mass_cluster(self, cx, cy, core_load, falloff=3.0):
        """Add a localized cluster of high-tick subroutines centered at (cx, cy)."""
        for y in range(self.size):
            for x in range(self.size):
                dist = math.hypot(x - cx, y - cy)
                added = int(round(core_load * math.exp(-dist / falloff)))
                self.load[y][x] += added

    def tick_delay_at(self, x, y):
        """Extra queueing ticks required to redraw() through pixel (x, y).

        Returns None if the node is deadlocked (at or above max_node_ticks).
        """
        current = self.load[y][x]
        if current >= self.max_ticks:
            return None  # I/O deadlock: outbound redraw blocked
        # Queueing delay grows as load approaches the hardware bandwidth ceiling
        utilization = current / self.max_ticks
        return int(utilization * 4)

    def trace_light_wavefront(self, y_rows, total_ticks=24):
        """Propagate light packets from x=0 across the grid and measure lensing deflection."""
        # Each packet tracks [x_pos, wait_timer, total_hops]
        packets = {y: [0, 0, 0] for y in y_rows}

        for _ in range(total_ticks):
            for y, state in packets.items():
                x, wait, hops = state
                if x >= self.size - 1:
                    continue
                if wait > 0:
                    state[1] -= 1
                    continue

                delay = self.tick_delay_at(x + 1, y)
                if delay is None:
                    # Captured at deadlocked horizon edge: cannot advance
                    continue
                # Redraw at next pixel and load queueing delay for the next tick
                state[0] += 1
                state[1] = delay
                state[2] += 1

        return packets

    def simulate_horizon_pileup(self, cx, cy, incoming_packets=40):
        """Inject packets toward a deadlocked core and observe boundary shell accumulation."""
        # Saturate the central core node above hardware capacity
        self.load[cy][cx] = self.max_ticks + 50
        deadlocked_nodes = {(cx, cy)}
        shell_counts = {}

        # Packets approach radially and pile up at the first deadlocked boundary they hit
        for step in range(incoming_packets):
            # Walk inward from the left edge along y=cy
            for x in range(cx):
                if (x + 1, cy) in deadlocked_nodes:
                    # Blocked from entering (x+1, cy); load piles up on edge node (x, cy)
                    self.load[cy][x] += 15
                    shell_counts[(x, cy)] = shell_counts.get((x, cy), 0) + 1
                    if self.load[cy][x] >= self.max_ticks:
                        deadlocked_nodes.add((x, cy))
                    break

        return deadlocked_nodes, shell_counts


def run_demo():
    # --- Part 1: Gravitational Lensing via Network Congestion ---
    lensing_grid = BCCCongestionGrid(size=25, max_node_ticks=100)
    # Place a sub-critical mass cluster at (12, 12) (high load, but not deadlocked)
    lensing_grid.place_mass_cluster(cx=12, cy=12, core_load=85, falloff=3.2)

    rows = [4, 7, 10, 12, 14, 17, 20]
    packets = lensing_grid.trace_light_wavefront(rows, total_ticks=24)

    print("=== 1. Wavefront Lensing from Network Congestion (Mass at y=12) ===")
    print(f"{'Row y':>6} {'Dist from Core':>15} {'X Reached':>11} {'Lag Behind Vacuum':>19}")
    vacuum_x = packets[4][0]
    for y in rows:
        x_end, _, _ = packets[y]
        lag = vacuum_x - x_end
        print(f"{y:6d} {abs(y - 12):15d} {x_end:11d} {lag:19d} pixels")

    # --- Part 2: Black Hole Event Horizon as I/O Buffer Deadlock ---
    bh_grid = BCCCongestionGrid(size=25, max_node_ticks=100)
    deadlocked, shell = bh_grid.simulate_horizon_pileup(cx=15, cy=12, incoming_packets=35)

    print("\n=== 2. Black Hole Deadlock & Perimeter Shell Pile-Up ===")
    print(f"Total deadlocked nodes (100% I/O blocked): {len(deadlocked)}")
    print("Deadlocked horizon coordinates (sorted):", sorted(deadlocked))
    print("Packets piled up along the outer boundary:", shell)


if __name__ == '__main__':
    run_demo()

