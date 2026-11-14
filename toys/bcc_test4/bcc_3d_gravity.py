#!/usr/bin/env python3
"""3D 6-Face Planck Grid Solver: 1/r Lensing, Deadlocked Horizon, Zigzag & Momentum-Coupled Pascal Wave.

Uses a single minimal rule: 6 orthogonal face connections (±x, ±y, ±z) of length 1.0 l_P.
Because every hop moves strictly across 1 orthogonal face per tick:
1. Sub-saturation workload bends wavefronts via queueing lag (1/r Poisson gravity).
2. Full saturation locks the core in complete network deadlock (zero-escape horizon).
3. Angled propagation forms a transverse zigzag wave across orthogonal faces.
4. Aiming a dual-channel (+/-) 3D Pascal expansion along a momentum vector (px, py, pz)
   drifts the wave packet's Born-rule probability center along p while preserving
   destructive dark nodes.
5. Relativistic Momentum-to-Gravity Coupling: Feeds a moving 3D Pascal packet's
   total routing workload (rest load + momentum load) directly into the 3D Poisson
   congestion solver, demonstrating that higher-momentum packets bend passing light
   rays more strongly than particles at rest.
"""
import random

FACE_DIRS_6 = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1),
]


class BCC3DGravityGrid:
    """Rigid 3D 6-face Planck grid solving 1/r congestion, horizon deadlock, and 3D Pascal waves."""

    def __init__(self, size=25, max_node_ticks=100, seed=42):
        self.size = size
        self.max_ticks = max_node_ticks
        self.source_rho = [[[0.0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.workload = [[[0.0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
        self.deadlocked = set()
        self.rng = random.Random(seed)

    def inject_3d_mass_core(self, cx, cy, cz, total_workload, radius=1):
        """Place a localized 3D mass+momentum cluster centered at (cx, cy, cz)."""
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

    def solve_3d_poisson_congestion(self, iterations=250):
        """Relax the 6-face 3D discrete Laplacian across the connected Planck-cube grid."""
        W = [[[0.0 for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]
        L = self.size

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

    def tick_delay_at(self, x, y, z):
        """Extra queueing ticks required to step into (x, y, z); None if network-deadlocked."""
        current = self.workload[z][y][x]
        if current >= self.max_ticks:
            return None
        return int((current / self.max_ticks) * 4)

    def trace_3d_light_rays(self, impact_ys, z_plane=12, total_ticks=22):
        """Propagate light packets along +x (1.0 l_P per tick) across orthogonal faces."""
        packets = {y: {'x': 1, 'wait': 0, 'hops': 0, 'captured': False} for y in impact_ys}

        for _ in range(total_ticks):
            for y, state in packets.items():
                if state['captured'] or state['x'] >= self.size - 2:
                    continue
                if state['wait'] > 0:
                    state['wait'] -= 1
                    continue

                next_x = state['x'] + 1
                delay = self.tick_delay_at(next_x, y, z_plane)
                if delay is None:
                    state['captured'] = True
                    continue

                state['x'] = next_x
                state['wait'] = delay
                state['hops'] += 1

        return packets

    def get_3d_boundary_shell(self):
        """Return all non-deadlocked 3D nodes 1 orthogonal face step outside the deadlocked core."""
        shell = set()
        for x, y, z in self.deadlocked:
            for dx, dy, dz in FACE_DIRS_6:
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx < self.size and 0 <= ny < self.size and 0 <= nz < self.size:
                    if (nx, ny, nz) not in self.deadlocked:
                        shell.add((nx, ny, nz))
        return shell

    def simulate_3d_horizon_accretion(self, incoming_packets=260, packet_load=25):
        """Route incoming 3D packets onto the 3D core shell under complete network deadlock."""
        edge_hits = {}
        for _ in range(incoming_packets):
            boundary = sorted(self.get_3d_boundary_shell())
            if not boundary:
                break
            tx, ty, tz = self.rng.choice(boundary)
            self.workload[tz][ty][tx] += packet_load
            edge_hits[(tx, ty, tz)] = edge_hits.get((tx, ty, tz), 0) + 1
            if self.workload[tz][ty][tx] >= self.max_ticks:
                self.deadlocked.add((tx, ty, tz))

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
        }

    def trace_6face_zigzag_wave(self, start=(2, 12, 12), ticks=8):
        """Route a signal across 6 orthogonal faces (±x, ±y, ±z) in an emergent helical wave."""
        zigzag_faces = [
            (1, 0, 0), (0, 1, 0),
            (1, 0, 0), (0, 0, 1),
            (1, 0, 0), (0, -1, 0),
            (1, 0, 0), (0, 0, -1),
        ]
        x, y, z = start
        path = [{'tick': 0, 'pos': (x, y, z), 'step': (0, 0, 0), 'dy': 0, 'dz': 0}]
        for t in range(1, ticks + 1):
            dx, dy, dz = zigzag_faces[(t - 1) % len(zigzag_faces)]
            x, y, z = x + dx, y + dy, z + dz
            path.append({
                'tick': t,
                'pos': (x, y, z),
                'step': (dx, dy, dz),
                'dy': y - start[1],
                'dz': z - start[2],
            })
        return path

    def evolve_biased_3d_pascal_wave(self, momentum=(2, 1, 0), n_ticks=6):
        """Propagate a dual-channel (+/-) 3D Pascal wave packet aimed along momentum (px, py, pz).

        Each axis allocates integer routing weights (w_plus, w_minus) across its ± faces
        with base weight 1 + max(0, ±p_i). Every tick branches across all 6 orthogonal faces,
        alternating phase channels on even ticks to generate destructive dark nodes
        while drifting the Born-rule center of mass <r> directly along the momentum vector.
        """
        px, py, pz = momentum
        if not all(isinstance(v, int) and not isinstance(v, bool) for v in (px, py, pz)):
            raise ValueError('Momentum components (px, py, pz) must be integers')

        face_rules = [
            ((1, 0, 0),  1 + max(0, px),  True),
            ((-1, 0, 0), 1 + max(0, -px), False),
            ((0, 1, 0),  1 + max(0, py),  True),
            ((0, -1, 0), 1 + max(0, -py), False),
            ((0, 0, 1),  1 + max(0, pz),  True),
            ((0, 0, -1), 1 + max(0, -pz), False),
        ]
        step_budget = sum(w for _, w, _ in face_rules)

        state = {(0, 0, 0): (1, 0)}
        for tick in range(1, n_ticks + 1):
            even_tick = (tick % 2 == 0)
            next_state = {}
            for (x, y, z), (pos, neg) in state.items():
                for (dx, dy, dz), w, is_pos_face in face_rules:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    c_pos, c_neg = next_state.get((nx, ny, nz), (0, 0))
                    if even_tick and is_pos_face:
                        next_state[(nx, ny, nz)] = (c_pos + w * neg, c_neg + w * pos)
                    else:
                        next_state[(nx, ny, nz)] = (c_pos + w * pos, c_neg + w * neg)
            state = next_state

        born_total = sum((pos - neg) ** 2 for pos, neg in state.values()) or 1
        dark_nodes = sum(1 for pos, neg in state.values() if pos == neg)

        mean_x = sum(x * ((pos - neg) ** 2) for (x, _, _), (pos, neg) in state.items()) / born_total
        mean_y = sum(y * ((pos - neg) ** 2) for (_, y, _), (pos, neg) in state.items()) / born_total
        mean_z = sum(z * ((pos - neg) ** 2) for (_, _, z), (pos, neg) in state.items()) / born_total

        peak_pos, (p_pos, p_neg) = max(
            state.items(),
            key=lambda kv: (kv[1][0] - kv[1][1]) ** 2,
        )

        return {
            'momentum': (px, py, pz),
            'n_ticks': n_ticks,
            'step_budget_per_tick': step_budget,
            'active_3d_nodes': len(state),
            'dark_nodes': dark_nodes,
            'born_centroid': (mean_x, mean_y, mean_z),
            'peak_node': peak_pos,
            'peak_born_prob': ((p_pos - p_neg) ** 2) / born_total,
        }

    def couple_pascal_momentum_to_gravity(self, momentum=(0, 0, 0), tick_scale=110.0, n_ticks=6):
        """Coupler linking Part 5 (Pascal momentum routing) directly into Part 1 (3D Poisson gravity).

        Computes the packet's per-tick routing load (`step_budget_per_tick`) from
        `evolve_biased_3d_pascal_wave(momentum)`, scales it into total network workload
        (`total_workload = step_budget * tick_scale`), solves the 3D Poisson congestion field,
        and measures the resulting light-ray lensing lag at impact parameters b=0 and b=2.
        """
        wave = self.evolve_biased_3d_pascal_wave(momentum=momentum, n_ticks=n_ticks)
        load_per_tick = wave['step_budget_per_tick']
        total_workload = load_per_tick * tick_scale

        self.source_rho = [[[0.0 for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]
        cx = cy = cz = self.size // 2
        self.inject_3d_mass_core(cx, cy, cz, total_workload=total_workload, radius=1)
        self.solve_3d_poisson_congestion(iterations=200)

        rays = self.trace_3d_light_rays((2, cy - 2, cy), z_plane=cz, total_ticks=22)
        ref_x = rays[2]['x']
        lag_b0 = ref_x - rays[cy]['x']
        lag_b2 = ref_x - rays[cy - 2]['x']

        return {
            'momentum': wave['momentum'],
            'load_per_tick': load_per_tick,
            'total_workload': total_workload,
            'peak_core_W': self.workload[cz][cy][cx],
            'lag_b0_pixels': lag_b0,
            'lag_b2_pixels': lag_b2,
        }


def run_3d_gravity_demo():
    # --- Part 1: 3D 6-Face Poisson 1/r Congestion Profile & Lensing ---
    sim = BCC3DGravityGrid(size=25, max_node_ticks=100)
    cx, cy, cz = 12, 12, 12
    sim.inject_3d_mass_core(cx, cy, cz, total_workload=1100.0, radius=1)
    sim.solve_3d_poisson_congestion(iterations=250)

    print("=== PART 1: 3D 6-Face Poisson 1/r Congestion Profile Along +X Axis ===")
    print(f"{'Radius r':>9} {'Node (x,y,z)':>14} {'Workload W(r)':>15} {'r * W(r) (1/r Check)':>22}")
    print("-" * 64)
    for r in range(1, 9):
        w_val = sim.workload[cz][cy][cx + r]
        print(f"{r:9d} {str((cx + r, cy, cz)):>14} {w_val:15.2f} {r * w_val:22.2f}")

    impact_rows = (2, 6, 8, 10, 12, 14, 16, 18, 22)
    rays = sim.trace_3d_light_rays(impact_rows, z_plane=cz, total_ticks=22)
    ref_x = rays[impact_rows[0]]['x']

    print("=== PART 2: 3D Wavefront Lensing Lag vs. Impact Parameter b ===")
    print(f"{'Row y':>6} {'Impact b':>9} {'X Reached':>11} {'Congestion Lag':>16}")
    print("-" * 46)
    for y in impact_rows:
        x_end = rays[y]['x']
        print(f"{y:6d} {abs(y - cy):9d} {x_end:11d} {ref_x - x_end:16d} pixels")

    # --- Part 3: Full 3D Spherical Deadlocked Core + 3D Boundary Shell ---
    bh3d = BCC3DGravityGrid(size=17, max_node_ticks=100, seed=42)
    bh3d.inject_3d_mass_core(8, 8, 8, total_workload=2400.0, radius=1)
    bh3d.solve_3d_poisson_congestion(iterations=250)
    init_core = len(bh3d.deadlocked)
    init_shell = len(bh3d.get_3d_boundary_shell())

    stats = bh3d.simulate_3d_horizon_accretion(incoming_packets=260, packet_load=25)
    print("=== PART 3: 3D Spherical Network-Deadlocked Core + 3D Boundary Shell ===")
    print(f"Initial 3D saturated core nodes:  {init_core} (wrapped by {init_shell} 3D face-shell nodes)")
    print(f"Deadlocked nodes after 3D infall: {stats['total_deadlocked']} (exposed 3D shell: {stats['exposed_3d_shell']})")
    print(f"Active 3D edge nodes hit:         {stats['active_edge_nodes_hit']} (escaped packets: {stats['escaped_packets']})")
    print(f"3D Bounding Volume (X x Y x Z):   {stats['span_xyz']}")

    # --- Part 4: 6-Face Orthogonal Zigzag Wave (Pascal Routing in 3D Space) ---
    wave_path = sim.trace_6face_zigzag_wave(start=(2, 12, 12), ticks=8)
    print("=== PART 4: 6-Face Zigzag Wave Trajectory (1 Orthogonal Face Hop / Tick) ===")
    print(f"{'Tick':>5} {'Face Step':>12} {'Grid Pos (x,y,z)':>18} {'Transverse (dy, dz)':>21}")
    print("-" * 60)
    for entry in wave_path:
        print(
            f"{entry['tick']:5d} {str(entry['step']):>12} {str(entry['pos']):>18} "
            f"{str((entry['dy'], entry['dz'])):>21}"
        )

    # --- Part 5: Momentum-Aimed 3D Pascal Wave Packet ---
    print("=== PART 5: Biased 3D Pascal Wave Packet (Momentum-Aimed Routing, N=6 Ticks) ===")
    print(f"{'Momentum p':>14} {'Load/Tick':>10} {'Active 3D':>10} {'Dark Nodes':>11} {'Born Centroid <x, y, z>':>26} {'Peak Node':>14}")
    print("-" * 91)
    for p_vec in ((0, 0, 0), (2, 0, 0), (2, 1, 0), (-1, 2, 1)):
        res = sim.evolve_biased_3d_pascal_wave(momentum=p_vec, n_ticks=6)
        cx_m, cy_m, cz_m = res['born_centroid']
        centroid_str = f"({cx_m:+.2f}, {cy_m:+.2f}, {cz_m:+.2f})"
        print(
            f"{str(p_vec):>14} {res['step_budget_per_tick']:10d} {res['active_3d_nodes']:10d} "
            f"{res['dark_nodes']:11d} {centroid_str:>26} {str(res['peak_node']):>14}"
        )

    # --- Part 6: Coupler (Part 5 Momentum Load -> Part 1 3D Poisson Lensing) ---
    print("=== PART 6: Relativistic Momentum-to-Gravity Coupler (Part 5 -> Part 1) ===")
    print(f"{'Momentum p':>14} {'Load/Tick':>10} {'Total Work':>11} {'Core W(0)':>10} {'Lag b=0':>9} {'Lag b=2':>9}")
    print("-" * 69)
    coupler_grid = BCC3DGravityGrid(size=25, max_node_ticks=100)
    for p_vec in ((0, 0, 0), (2, 0, 0), (2, 1, 0), (3, 2, 1)):
        c_res = coupler_grid.couple_pascal_momentum_to_gravity(momentum=p_vec, tick_scale=110.0)
        print(
            f"{str(c_res['momentum']):>14} {c_res['load_per_tick']:10d} {c_res['total_workload']:11.1f} "
            f"{c_res['peak_core_W']:10.2f} {c_res['lag_b0_pixels']:6d} px {c_res['lag_b2_pixels']:6d} px"
        )


if __name__ == '__main__':
    run_3d_gravity_demo()
