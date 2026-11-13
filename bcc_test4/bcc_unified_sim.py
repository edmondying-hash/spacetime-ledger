#!/usr/bin/env python3
"""Unified 3D BCC Pixel Grid Simulation:
1. Baryon subroutine tick accounting & redraw() lag -> emergent constituent mass.
2. Pure-gluon closed BCC plaquette loops (4, 6, 8 links) -> Yang-Mills mass gap & excited glueballs.
3. Sub-saturation network congestion -> gravitational lensing without curved space.
4. Strictly locked 2D deadlocked core + 3D volumetric boundary shell -> zero-escape horizon pile-up.
"""
import math
import random
from baryon_calculator import Parameters, calculate

# 8 nearest-neighbor pixel steps on a rigid 3D BCC lattice
BCC_DIRS = [
    (dx, dy, dz)
    for dx in (-1, 1)
    for dy in (-1, 1)
    for dz in (-1, 1)
]


def bcc_step_distance(p1, p2, L):
    """Minimum-image L_inf (Chebyshev) step distance on a periodic 3D BCC grid."""
    steps = 0
    for a, b in zip(p1, p2):
        d = abs(a - b)
        d = min(d, L - d)
        steps = max(steps, d)
    return steps


def steiner_y_links(positions, L):
    """Minimum active routing links connecting 3 quark pixels via a central Y-junction."""
    best = 999
    qx, qy, qz = positions[0]
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            for dz in range(-3, 4):
                hub = ((qx + dx) % L, (qy + dy) % L, (qz + dz) % L)
                total = sum(bcc_step_distance(q, hub, L) for q in positions)
                if total < best:
                    best = total
    return best


class BCCUnifiedGrid:
    def __init__(
        self,
        L=8,
        ticks_bare_l=4,
        ticks_bare_s=95,
        ticks_link_route=145,
        ticks_spin_conflict=460,
        redraw_period_l=3,
        redraw_period_s=5,
        mev_per_tick=1.0,
        seed=42,
    ):
        self.L = L
        self.bare_ticks = {'l': ticks_bare_l, 's': ticks_bare_s}
        self.redraw_period = {'l': redraw_period_l, 's': redraw_period_s}
        self.ticks_link = ticks_link_route
        self.ticks_spin = ticks_spin_conflict
        self.mev_per_tick = mev_per_tick
        self.rng = random.Random(seed)

    def redraw_node(self, pos):
        """Clear pixel at pos and redraw at one of the 8 adjacent BCC pixels."""
        px, py, pz = pos
        dx, dy, dz = self.rng.choice(BCC_DIRS)
        return ((px + dx) % self.L, (py + dy) % self.L, (pz + dz) % self.L)

    def run_baryon_subroutine(self, flavors, pair_spins, total_cycles=6000):
        """Execute a 3-node baryon subroutine and count exact hardware ticks."""
        positions = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
        timers = [self.redraw_period[f] for f in flavors]

        total_ticks = 0
        bare_ticks_acc = 0
        route_ticks_acc = 0
        spin_ticks_acc = 0
        redraw_count = 0

        for _ in range(total_cycles):
            for i, flv in enumerate(flavors):
                timers[i] -= 1
                if timers[i] <= 0:
                    candidate = self.redraw_node(positions[i])
                    trial_positions = list(positions)
                    trial_positions[i] = candidate
                    if steiner_y_links(trial_positions, self.L) <= 4:
                        positions[i] = candidate
                        redraw_count += 1
                    timers[i] = self.redraw_period[flv]

            t_bare = sum(self.bare_ticks[f] for f in flavors)
            active_links = steiner_y_links(positions, self.L)
            t_route = active_links * self.ticks_link

            t_spin = 0
            pairs = ((0, 1), (0, 2), (1, 2))
            for idx, (i, j) in enumerate(pairs):
                if positions[i] == positions[j]:
                    rate_scale = (self.redraw_period['l'] ** 2) / (
                        self.redraw_period[flavors[i]] * self.redraw_period[flavors[j]]
                    )
                    t_spin += round(self.ticks_spin * rate_scale * pair_spins[idx])

            cycle_ticks = t_bare + t_route + t_spin
            total_ticks += cycle_ticks
            bare_ticks_acc += t_bare
            route_ticks_acc += t_route
            spin_ticks_acc += t_spin

        avg_ticks = total_ticks / total_cycles
        avg_bare = bare_ticks_acc / total_cycles
        avg_route = route_ticks_acc / total_cycles
        avg_spin = spin_ticks_acc / total_cycles

        return {
            'mass_MeV': avg_ticks * self.mev_per_tick,
            'avg_ticks': avg_ticks,
            'bare_ticks': avg_bare,
            'route_ticks': avg_route,
            'spin_ticks': avg_spin,
            'redraws_per_cycle': redraw_count / total_cycles,
            'active_load_pct': 100.0 * (avg_ticks - avg_bare) / avg_ticks,
        }

    def run_glueball_loop(self, loop_links=4, vertex_self_coupling=280, total_cycles=6000):
        """Simulate a pure-gluon closed BCC plaquette ring (zero quarks) to measure the mass gap.

        On a 3D BCC lattice, every diagonal move flips coordinate parity, so the smallest
        non-trivial closed flux loop requires 4 diagonal links (an elementary BCC plaquette).
        Because gluons self-interact at loop vertices, any closed loop carries a strict
        nonzero tick workload above the empty vacuum (0 ticks).
        """
        if loop_links < 4 or loop_links % 2 != 0:
            raise ValueError('Closed BCC plaquette loops require an even number of links >= 4')

        total_ticks = 0
        route_ticks_acc = 0
        self_int_ticks_acc = 0
        redraw_count = 0

        for _ in range(total_cycles):
            # Quantum plaquette breathing: loop fluctuates between minimal (loop_links)
            # and excited (loop_links + 2) configurations as vertices redraw on BCC nodes
            if self.rng.random() < 0.35:
                active_links = loop_links + 2
                redraw_count += 1
            else:
                active_links = loop_links

            t_bare = 0
            t_route = active_links * self.ticks_link
            t_self = active_links * vertex_self_coupling

            total_ticks += t_bare + t_route + t_self
            route_ticks_acc += t_route
            self_int_ticks_acc += t_self

        avg_ticks = total_ticks / total_cycles
        return {
            'loop_links': loop_links,
            'mass_MeV': avg_ticks * self.mev_per_tick,
            'bare_ticks': 0.0,
            'route_ticks': route_ticks_acc / total_cycles,
            'self_int_ticks': self_int_ticks_acc / total_cycles,
            'redraws_per_cycle': redraw_count / total_cycles,
            'active_load_pct': 100.0,
        }


class BCCNetworkCongestion:
    """Models routing delay (lensing) and strictly locked 2D-core + 3D-shell horizon deadlock."""

    def __init__(self, size=25, max_node_ticks=100, seed=42):
        self.size = size
        self.max_ticks = max_node_ticks
        self.load_2d = [[0 for _ in range(size)] for _ in range(size)]
        self.load_3d = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.deadlocked_3d = set()
        self.rng = random.Random(seed)

    def place_mass_cluster_2d(self, cx, cy, core_load, falloff=3.0):
        """Inject localized subroutine tick-load centered at (cx, cy)."""
        for y in range(self.size):
            for x in range(self.size):
                dist = math.hypot(x - cx, y - cy)
                self.load_2d[y][x] += int(round(core_load * math.exp(-dist / falloff)))

    def tick_delay_at_2d(self, x, y):
        """Extra queueing ticks required to redraw() into (x, y); None if deadlocked."""
        current = self.load_2d[y][x]
        if current >= self.max_ticks:
            return None
        return int((current / self.max_ticks) * 4)

    def trace_light_wavefront(self, y_rows, total_ticks=24):
        """Propagate light packets (1 pixel/tick in vacuum) and measure congestion lag."""
        packets = {y: {'x': 0, 'wait': 0, 'hops': 0} for y in y_rows}
        for _ in range(total_ticks):
            for y, state in packets.items():
                if state['x'] >= self.size - 1:
                    continue
                if state['wait'] > 0:
                    state['wait'] -= 1
                    continue
                delay = self.tick_delay_at_2d(state['x'] + 1, y)
                if delay is None:
                    continue
                state['x'] += 1
                state['wait'] = delay
                state['hops'] += 1
        return packets

    def seed_flat_2d_core(self, cx, cy, cz, radius=2):
        """Initialize a flat 2D deadlocked sheet in the x-y plane at z=cz."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    x, y, z = cx + dx, cy + dy, cz
                    self.load_3d[z][y][x] = self.max_ticks + 50
                    self.deadlocked_3d.add((x, y, z))

    def get_3d_boundary_shell(self):
        """Return all non-deadlocked 3D BCC nodes 1 diagonal step outside the core."""
        shell = set()
        for x, y, z in self.deadlocked_3d:
            for dx, dy, dz in BCC_DIRS:
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx < self.size and 0 <= ny < self.size and 0 <= nz < self.size:
                    if (nx, ny, nz) not in self.deadlocked_3d:
                        shell.add((nx, ny, nz))
        return shell

    def simulate_3d_infall_strict_lock(self, incoming_packets=220, packet_load=20):
        """Route 3D packets onto the 2D core shell under strict I/O deadlock (zero escape)."""
        edge_hits = {}
        for _ in range(incoming_packets):
            boundary = sorted(self.get_3d_boundary_shell())
            if not boundary:
                break
            tx, ty, tz = self.rng.choice(boundary)
            self.load_3d[tz][ty][tx] += packet_load
            edge_hits[(tx, ty, tz)] = edge_hits.get((tx, ty, tz), 0) + 1
            if self.load_3d[tz][ty][tx] >= self.max_ticks:
                self.deadlocked_3d.add((tx, ty, tz))

        if self.deadlocked_3d:
            xs = [x for x, _, _ in self.deadlocked_3d]
            ys = [y for _, y, _ in self.deadlocked_3d]
            zs = [z for _, _, z in self.deadlocked_3d]
            span_xyz = (max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, max(zs) - min(zs) + 1)
        else:
            span_xyz = (0, 0, 0)

        return {
            'total_deadlocked': len(self.deadlocked_3d),
            'exposed_3d_shell': len(self.get_3d_boundary_shell()),
            'active_edge_nodes_hit': len(edge_hits),
            'escaped_packets': 0,
            'span_xyz': span_xyz,
        }


def run_all():
    # --- Part 1: Baryon Tick-Count & Emergent Mass Bridge ---
    grid = BCCUnifiedGrid()
    channel_specs = {
        'N':         (('l', 'l', 'l'), (-0.75,  0.00,  0.00)),
        'Delta':     (('l', 'l', 'l'), (+0.25, +0.25, +0.25)),
        'Lambda':    (('l', 'l', 's'), (-0.75,  0.00,  0.00)),
        'Sigma':     (('l', 'l', 's'), (+0.25, -0.50, -0.50)),
        'Xi':        (('s', 's', 'l'), (+0.25, -0.50, -0.50)),
        'SigmaStar': (('l', 'l', 's'), (+0.25, +0.25, +0.25)),
        'XiStar':    (('s', 's', 'l'), (+0.25, +0.25, +0.25)),
        'Omega':     (('s', 's', 's'), (+0.25, +0.25, +0.25)),
    }

    sim_data = {
        name: grid.run_baryon_subroutine(flvs, spins)
        for name, (flvs, spins) in channel_specs.items()
    }
    params = Parameters.from_anchors(
        N_MeV=sim_data['N']['mass_MeV'],
        Delta_MeV=sim_data['Delta']['mass_MeV'],
        Lambda_MeV=sim_data['Lambda']['mass_MeV'],
    )

    print("=== PART 1: BCC Pixel Grid Baryon Workload vs. Pair-Spin Rule ===")
    print(f"Emergent m_light={params.m_light:.2f}, m_strange={params.m_strange:.2f}, A={params.A:.2f} MeV/cycle")
    header = (f"{'Family':10} {'BareT':>6} {'RouteT':>7} {'SpinT':>7} {'Redraw/c':>9} "
              f"{'Load%':>6} {'GridMass':>9} {'RuleMass':>9} {'Diff':>7}")
    print(header)
    print("-" * len(header))
    map_to_channel = {
        'N': 'p', 'Delta': 'Delta+', 'Lambda': 'Lambda', 'Sigma': 'Sigma0',
        'Xi': 'Xi0', 'SigmaStar': 'SigmaStar0', 'XiStar': 'XiStar0', 'Omega': 'Omega-',
    }
    for fam, ch in map_to_channel.items():
        d = sim_data[fam]
        rule_m = calculate(ch, parameters=params)['mass_MeV']
        print(f"{fam:10} {d['bare_ticks']:6.1f} {d['route_ticks']:7.1f} {d['spin_ticks']:7.1f} "
              f"{d['redraws_per_cycle']:9.2f} {d['active_load_pct']:5.1f}% "
              f"{d['mass_MeV']:9.2f} {rule_m:9.2f} {d['mass_MeV'] - rule_m:7.2f}")

    # --- Part 2: Pure-Gluon Glueball Loop Sweep & Yang-Mills Mass Gap ---
    print("=== PART 2: Pure-Gluon Glueball Loop Sweep & Mass Gap ===")
    print(f"{'Loop Links':>10} {'BareT':>6} {'RouteT':>8} {'SelfIntT':>9} {'Load%':>6} {'GlueballMass':>13}")
    print("-" * 58)
    print(f"{0:10d} {0.0:6.1f} {0.0:8.2f} {0.0:9.2f} {'0%':>6} {0.0:13.2f}  (empty vacuum)")
    for links in (4, 6, 8):
        gb = grid.run_glueball_loop(loop_links=links, vertex_self_coupling=280)
        label = "  (Mass Gap Δ)" if links == 4 else ""
        print(f"{links:10d} {gb['bare_ticks']:6.1f} {gb['route_ticks']:8.2f} {gb['self_int_ticks']:9.2f} "
              f"{gb['active_load_pct']:5.0f}% {gb['mass_MeV']:13.2f}{label}")

    # --- Part 3: Wavefront Lensing from Network Congestion ---
    lensing = BCCNetworkCongestion(size=25, max_node_ticks=100)
    lensing.place_mass_cluster_2d(cx=12, cy=12, core_load=85, falloff=3.2)
    rows = (4, 7, 10, 12, 14, 17, 20)
    packets = lensing.trace_light_wavefront(rows, total_ticks=24)

    print("=== PART 3: Wavefront Lensing via Network Congestion (Cluster at y=12) ===")
    print(f"{'Row y':>6} {'Dist from Core':>15} {'X Reached':>11} {'Congestion Lag':>16}")
    vac_x = packets[4]['x']
    for y in rows:
        x_end = packets[y]['x']
        print(f"{y:6d} {abs(y - 12):15d} {x_end:11d} {vac_x - x_end:16d} pixels")

    # --- Part 4: Strictly Locked 2D Core + 3D Boundary Shell ---
    bh = BCCNetworkCongestion(size=15, max_node_ticks=100)
    bh.seed_flat_2d_core(cx=7, cy=7, cz=7, radius=2)
    init_core = len(bh.deadlocked_3d)
    init_shell = len(bh.get_3d_boundary_shell())
    bh_stats = bh.simulate_3d_infall_strict_lock(incoming_packets=220, packet_load=20)

    print("=== PART 4: Strictly Locked 2D Core + 3D Boundary Shell Pile-Up ===")
    print(f"Initial flat 2D core nodes: {init_core} (wrapped by {init_shell} 3D BCC edge nodes)")
    print(f"Deadlocked nodes after 3D infall: {bh_stats['total_deadlocked']} (3D shell: {bh_stats['exposed_3d_shell']})")
    print(f"Active 3D edge nodes hit:         {bh_stats['active_edge_nodes_hit']} (escaped packets: {bh_stats['escaped_packets']})")
    print(f"Bounding dimensions (X x Y x Z):  {bh_stats['span_xyz']}")


if __name__ == '__main__':
    run_all()
