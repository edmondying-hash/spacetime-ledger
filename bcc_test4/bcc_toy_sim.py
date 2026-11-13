#!/usr/bin/env python3
"""Minimal 3D BCC lattice toy simulation bridging microscopic grid rules to baryon_calculator.

Demonstrates:
1. Discrete 8-neighbor BCC hopping (kinetic dressing -> constituent mass).
2. Linear flux-tree confinement (Y-junction link tension).
3. Local plaquette spin-spin exchange suppressed by hopping amplitudes (1 / m_i m_j).
4. Ground-state mass extraction via imaginary-time projection, feeding into Parameters.from_anchors().
"""
import math
import random
from baryon_calculator import Parameters, calculate

# 8 nearest-neighbor displacement vectors on a 3D BCC lattice
BCC_DIRS = [
    (dx, dy, dz)
    for dx in (-1, 1)
    for dy in (-1, 1)
    for dz in (-1, 1)
]


def bcc_distance(p1, p2, L):
    """Minimum-image L_inf (Chebyshev) step distance on a periodic BCC grid."""
    steps = 0
    for a, b in zip(p1, p2):
        d = abs(a - b)
        d = min(d, L - d)
        steps = max(steps, d)
    return steps


def y_junction_links(positions, L):
    """Minimal discrete link count connecting 3 quark nodes to a Steiner node on the BCC grid."""
    best = 999
    q0 = positions[0]
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            for dz in range(-3, 4):
                center = ((q0[0] + dx) % L, (q0[1] + dy) % L, (q0[2] + dz) % L)
                total = sum(bcc_distance(q, center, L) for q in positions)
                if total < best:
                    best = total
    return best


class BCCToyLattice:
    def __init__(
        self,
        L=8,
        m_bare_light=280.0,
        m_bare_strange=460.0,
        hop_scale=11000.0,
        string_tension=115.0,
        plaq_coupling=480.0,
        seed=42,
    ):
        self.L = L
        self.m_bare = {'l': m_bare_light, 's': m_bare_strange}
        # Hopping amplitude scales inversely with bare mass (Compton localization)
        self.hop = {
            'l': hop_scale / m_bare_light,
            's': hop_scale / m_bare_strange,
        }
        self.sigma = string_tension
        self.J_plaq = plaq_coupling
        self.rng = random.Random(seed)

    def potential_energy(self, positions, flavors, pair_spins):
        """Total static + plaquette hyperfine energy (MeV) for a 3-quark configuration."""
        # 1. Bare quark rest energies
        energy = sum(self.m_bare[f] for f in flavors)

        # 2. Confining Y-junction flux tube energy
        links = y_junction_links(positions, self.L)
        energy += self.sigma * links

        # 3. Local plaquette spin-spin interaction when quarks overlap on the same BCC cell
        pairs = [(0, 1), (0, 2), (1, 2)]
        for idx, (i, j) in enumerate(pairs):
            if positions[i] == positions[j]:
                g_ij = self.J_plaq * (self.hop[flavors[i]] * self.hop[flavors[j]]) / (self.hop['l'] ** 2)
                energy += g_ij * pair_spins[idx]
        return energy

    def measure_ground_state(self, flavors, pair_spins, n_walkers=400, n_steps=180, dtau=0.0025):
        """Extract ground-state baryon mass via imaginary-time diffusion Monte Carlo."""
        walkers = [[(0, 0, 0), (0, 0, 0), (0, 0, 0)] for _ in range(n_walkers)]
        energies = []

        for step in range(n_steps):
            new_walkers = []
            weights = []

            for pos in walkers:
                trial = list(pos)
                for q_idx, flv in enumerate(flavors):
                    p_hop = min(0.85, 8.0 * self.hop[flv] * dtau)
                    if self.rng.random() < p_hop:
                        dx, dy, dz = self.rng.choice(BCC_DIRS)
                        x, y, z = trial[q_idx]
                        trial[q_idx] = ((x + dx) % self.L, (y + dy) % self.L, (z + dz) % self.L)

                v_pot = self.potential_energy(trial, flavors, pair_spins)
                w = math.exp(-dtau * v_pot)
                new_walkers.append(trial)
                weights.append(w)

            total_w = sum(weights)
            mean_w = total_w / n_walkers
            e_est = -math.log(mean_w) / dtau
            if step >= n_steps // 3:
                energies.append(e_est)

            cdf = []
            acc = 0.0
            for w in weights:
                acc += w / total_w
                cdf.append(acc)

            u0 = self.rng.random() / n_walkers
            resampled = []
            idx = 0
            for k in range(n_walkers):
                target = u0 + k / n_walkers
                while idx < n_walkers - 1 and cdf[idx] < target:
                    idx += 1
                resampled.append(list(new_walkers[idx]))
            walkers = resampled

        return sum(energies) / len(energies)


def run_bridge_experiment():
    sim = BCCToyLattice()

    # Exact pair spin expectations (<s_0.s_1>, <s_0.s_2>, <s_1.s_2>) for ordered quarks (q0, q1, q2)
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

    print("Running 3D BCC lattice imaginary-time projection...")
    lattice_masses = {}
    for name, (flvs, spins) in channel_specs.items():
        lattice_masses[name] = sim.measure_ground_state(flvs, spins)

    derived_params = Parameters.from_anchors(
        N_MeV=lattice_masses['N'],
        Delta_MeV=lattice_masses['Delta'],
        Lambda_MeV=lattice_masses['Lambda'],
    )

    print("\n=== Emergent Effective Parameters (via Parameters.from_anchors) ===")
    print(f"m_light   = {derived_params.m_light:.2f} MeV  (bare input: {sim.m_bare['l']:.1f} MeV + flux dressing)")
    print(f"m_strange = {derived_params.m_strange:.2f} MeV  (bare input: {sim.m_bare['s']:.1f} MeV + flux dressing)")
    print(f"A         = {derived_params.A:.2f} MeV  (emergent plaquette hyperfine coupling)")

    print("\n=== Lattice Simulation vs. Effective Pair-Spin Rule ===")
    print(f"{'Family':10} {'BCC Lattice (MeV)':>18} {'Pair-Spin Rule (MeV)':>22} {'Diff (MeV)':>12}  Role")
    map_to_channel = {
        'N': 'p', 'Delta': 'Delta+', 'Lambda': 'Lambda', 'Sigma': 'Sigma0',
        'Xi': 'Xi0', 'SigmaStar': 'SigmaStar0', 'XiStar': 'XiStar0', 'Omega': 'Omega-',
    }
    for fam, ch in map_to_channel.items():
        lat_m = lattice_masses[fam]
        rule_m = calculate(ch, parameters=derived_params)['mass_MeV']
        role = "anchor" if fam in ('N', 'Delta', 'Lambda') else "out-of-calibration test"
        print(f"{fam:10} {lat_m:18.2f} {rule_m:22.2f} {lat_m - rule_m:12.2f}  {role}")


if __name__ == '__main__':
    run_bridge_experiment()

