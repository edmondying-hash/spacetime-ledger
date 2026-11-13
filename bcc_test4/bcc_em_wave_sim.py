#!/usr/bin/env python3
"""3D BCC Maxwell Flux-Conservation & Discrete Double-Slit Interference Module.

Core rules on the rigid 3D BCC pixel grid:
1. Charge Conservation (Discrete Gauss's Law): Every BCC node has 8 diagonal links.
   Total signed flux leaving a node equals the node's net charge density (div E = rho),
   and any local charge redraw() hop updates the connecting link flux so charge is
   conserved at every tick.
2. Transverse Electromagnetic Wave Propagation: Wave displacements propagate across
   the 8 BCC diagonals at the fixed hardware clock limit.
3. Double-Slit Interference & Which-Slit Detector Collapse: Wave packets passing
   through two open pixel slits diffract across diagonal BCC links and accumulate
   in two-sublattice detector bins (det_x and det_x - 1) so every screen row
   samples both diagonal parities cleanly.
"""
import math
import random

BCC_DIRS = [
    (dx, dy, dz)
    for dx in (-1, 1)
    for dy in (-1, 1)
    for dz in (-1, 1)
]


class BCCMaxwellGrid:
    """Discrete 3D BCC lattice enforcing Gauss's law and Maxwell link updates."""

    def __init__(self, L=10):
        self.L = L
        self.E = {
            (x, y, z): [0.0] * 8
            for x in range(L)
            for y in range(L)
            for z in range(L)
        }
        self.rho = {
            (x, y, z): 0.0
            for x in range(L)
            for y in range(L)
            for z in range(L)
        }
        self.phi = [[[0.0 for _ in range(L)] for _ in range(L)] for _ in range(L)]
        self.dphi = [[[0.0 for _ in range(L)] for _ in range(L)] for _ in range(L)]

    def neighbor(self, x, y, z, dir_idx):
        dx, dy, dz = BCC_DIRS[dir_idx]
        return ((x + dx) % self.L, (y + dy) % self.L, (z + dz) % self.L)

    def place_dipole_charges(self, pos_plus, pos_minus, q_mag=10.0, iterations=300):
        """Inject equal and opposite charges and solve discrete Gauss's law on BCC links."""
        V = [[[0.0 for _ in range(self.L)] for _ in range(self.L)] for _ in range(self.L)]
        for node in self.rho:
            self.rho[node] = 0.0
        self.rho[pos_plus] = +q_mag
        self.rho[pos_minus] = -q_mag

        for _ in range(iterations):
            new_V = [[[0.0 for _ in range(self.L)] for _ in range(self.L)] for _ in range(self.L)]
            for x in range(self.L):
                for y in range(self.L):
                    for z in range(self.L):
                        nbr_sum = 0.0
                        for d_idx in range(8):
                            nx, ny, nz = self.neighbor(x, y, z, d_idx)
                            nbr_sum += V[nx][ny][nz]
                        new_V[x][y][z] = (nbr_sum + self.rho[(x, y, z)]) / 8.0
            V = new_V

        for x in range(self.L):
            for y in range(self.L):
                for z in range(self.L):
                    for d_idx in range(8):
                        nx, ny, nz = self.neighbor(x, y, z, d_idx)
                        self.E[(x, y, z)][d_idx] = V[x][y][z] - V[nx][ny][nz]

    def redraw_charge_step(self, node, dir_idx, dq):
        """Redraw charge dq from node to neighbor along dir_idx while updating link flux E."""
        nx, ny, nz = node
        target = self.neighbor(nx, ny, nz, dir_idx)
        rev_idx = 7 - dir_idx
        self.rho[node] -= dq
        self.rho[target] += dq
        self.E[node][dir_idx] -= dq
        self.E[target][rev_idx] += dq
        return target

    def verify_gauss_law(self):
        """Check discrete divergence sum_links E_out(node) == rho(node) across every BCC cell."""
        max_residual = 0.0
        total_flux_sum = 0.0
        total_charge = 0.0
        for node, links in self.E.items():
            div_e = sum(links)
            total_flux_sum += div_e
            total_charge += self.rho[node]
            residual = abs(div_e - self.rho[node])
            if residual > max_residual:
                max_residual = residual
        return {
            'max_gauss_residual': max_residual,
            'net_global_flux': total_flux_sum,
            'net_global_charge': total_charge,
        }

    def step_em_wave(self, c_sq=0.22):
        """Advance discrete Maxwell wave equation on the 8-neighbor BCC grid by 1 hardware tick."""
        next_phi = [[[0.0 for _ in range(self.L)] for _ in range(self.L)] for _ in range(self.L)]
        for x in range(self.L):
            for y in range(self.L):
                for z in range(self.L):
                    nbr_sum = 0.0
                    for d_idx in range(8):
                        nx, ny, nz = self.neighbor(x, y, z, d_idx)
                        nbr_sum += self.phi[nx][ny][nz]
                    laplacian = nbr_sum - 8.0 * self.phi[x][y][z]
                    self.dphi[x][y][z] += c_sq * laplacian
                    next_phi[x][y][z] = self.phi[x][y][z] + self.dphi[x][y][z]
        self.phi = next_phi


class BCCDoubleSlitSim:
    """Discrete pixel redraw() wave interference with two-sublattice detector bins."""

    def __init__(
        self,
        width=36,
        height=45,
        barrier_x=10,
        slit_ys=(17, 27),
        wavelength_ticks=6,
        detector_slit_y=None,
        seed=42,
    ):
        self.width = width
        self.height = height
        self.barrier_x = barrier_x
        self.slit_ys = set(slit_ys)
        self.wavelength = wavelength_ticks
        self.detector_slit_y = detector_slit_y
        self.rng = random.Random(seed)
        self.u_curr = [[0.0 for _ in range(width)] for _ in range(height)]
        self.u_prev = [[0.0 for _ in range(width)] for _ in range(height)]
        self.detector_intensity = [0.0 for _ in range(height)]

    def step_redraw_wave(self, tick):
        """Propagate discrete wave displacement u across diagonal BCC links by 1 tick."""
        source_val = math.sin(2.0 * math.pi * tick / self.wavelength)
        for y in range(1, self.height - 1):
            self.u_curr[y][1] = source_val

        u_next = [[0.0 for _ in range(self.width)] for _ in range(self.height)]
        c_sq = 0.45

        for y in range(1, self.height - 1):
            for x in range(2, self.width - 1):
                if x == self.barrier_x and y not in self.slit_ys:
                    continue
                diag_sum = (
                    self.u_curr[y - 1][x - 1]
                    + self.u_curr[y - 1][x + 1]
                    + self.u_curr[y + 1][x - 1]
                    + self.u_curr[y + 1][x + 1]
                )
                lap = diag_sum - 4.0 * self.u_curr[y][x]
                val = 2.0 * self.u_curr[y][x] - self.u_prev[y][x] + c_sq * lap

                # Which-slit detector: high-load sensor node scrambles phase ticks at monitored slit
                if x == self.barrier_x and y == self.detector_slit_y:
                    val *= self.rng.choice((-1.0, 0.0, 1.0))

                u_next[y][x] = val

        self.u_prev = self.u_curr
        self.u_curr = u_next

        # Two-sublattice detector bin: combine det_x and det_x - 1 so both diagonal
        # parities contribute to every screen row y
        if tick >= 35:
            det_x = self.width - 3
            for y in range(1, self.height - 1):
                self.detector_intensity[y] += (
                    self.u_curr[y][det_x] ** 2 + self.u_curr[y][det_x - 1] ** 2
                )


def run_em_and_slit_demo():
    # --- Part 1: Maxwell Flux Conservation & Charge Hop ---
    maxwell = BCCMaxwellGrid(L=10)
    p_plus = (3, 5, 5)
    p_minus = (7, 5, 5)
    maxwell.place_dipole_charges(p_plus, p_minus, q_mag=10.0)
    gauss_static = maxwell.verify_gauss_law()

    curr = p_plus
    for d_idx in (7, 3, 5):
        curr = maxwell.redraw_charge_step(curr, d_idx, dq=10.0)
    gauss_after_hop = maxwell.verify_gauss_law()

    maxwell.phi[0][0][0] = 1.0
    wave_peaks = []
    for t in range(1, 7):
        maxwell.step_em_wave()
        diag_val = maxwell.phi[t % maxwell.L][t % maxwell.L][t % maxwell.L]
        wave_peaks.append((t, diag_val))

    print("=== PART 1: 3D BCC Maxwell Flux Conservation & Wave Propagation ===")
    print(f"Dipole charges placed: +10.0 at {p_plus}, -10.0 at {p_minus}")
    print(f"Static Gauss's Law max residual (1,000 nodes): {gauss_static['max_gauss_residual']:.2e}")
    print(f"Post-hop Gauss's Law residual (charge at {curr}): {gauss_after_hop['max_gauss_residual']:.2e}")
    print(f"Global conserved link flux sum:                 {gauss_after_hop['net_global_flux']:.2e}")
    print("Diagonal EM wavefront amplitude per tick:",
          ", ".join(f"t={t}:{val:+.4f}" for t, val in wave_peaks))

    # --- Part 2: Double-Slit Interference vs. Which-Slit Detector Collapse ---
    unobserved = BCCDoubleSlitSim(
        width=36, height=45, barrier_x=10, slit_ys=(17, 27), wavelength_ticks=6
    )
    observed = BCCDoubleSlitSim(
        width=36, height=45, barrier_x=10, slit_ys=(17, 27), wavelength_ticks=6, detector_slit_y=17, seed=42
    )
    for t in range(120):
        unobserved.step_redraw_wave(t)
        observed.step_redraw_wave(t)

    print("\n=== PART 2: Double-Slit Fringes vs. Which-Slit Detector (Two-Sublattice Bin) ===")
    print("Unobserved: both slits open | Observed: sensor congestion at y=17")
    print(f"{'Screen Y':>8} {'No-Detector':>12} {'With-Detector':>14}  Pattern Comparison (Unobserved | Observed)")
    print("-" * 78)
    max_unobs = max(unobserved.detector_intensity) or 1.0
    max_obs = max(observed.detector_intensity) or 1.0
    for y in range(15, 30):
        n_unobs = unobserved.detector_intensity[y] / max_unobs
        n_obs = observed.detector_intensity[y] / max_obs
        bar_u = "#" * int(round(n_unobs * 16))
        bar_o = "*" * int(round(n_obs * 16))
        print(f"{y:8d} {n_unobs:12.3f} {n_obs:14.3f}  {bar_u:<16} | {bar_o}")


if __name__ == '__main__':
    run_em_and_slit_demo()
