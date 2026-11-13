#!/usr/bin/env python3
"""Minimal 3D BCC lattice toy simulation with explicit workload accounting.

Demonstrates:
1. Bare node baseline (~1% static rest load) vs. active grid workload (~99% emergent mass).
2. Discrete 8-neighbor BCC hopping and Y-junction flux link routing.
3. Local plaquette spin-spin exchange suppressed by hopping amplitudes (1 / m_i m_j).
4. Ground-state mass extraction feeding directly into Parameters.from_anchors().
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
        m_bare_light=3.5,       # ~3.5 MeV per light quark (~10.5 MeV total = ~1.1% of proton)
        m_bare_strange=95.0,    # ~95 MeV bare strange quark mass
        hop_scale=160.0,
        string_tension=365.0,   # Flux-tube routing cost per active BCC link (MeV/link)
        plaq_coupling=440.0,    # Local color-magnetic plaquette exchange (MeV)
        seed=42,
    ):
        self.L = L
        self.m_bare = {'l': m_bare_light, 's': m_bare_strange}
        # Effective inertial resistance to hopping includes baseline confinement dressing
        self.hop = {
            'l': hop_scale / (m_bare_light + 280.0),
            's': hop_scale / (m_bare_strange + 280.0),
        }
        self.sigma = string_tension
        self.J_plaq = plaq_coupling
        self.rng = random.Random(seed)

    def energy_breakdown(self, positions, flavors, pair_spins):
        """Return static bare node cost and active flux/plaquette workload components (MeV)."""
        # 1. Static bare node markers (~1% baseline for light baryons)
        bare = sum(self.m_bare[f] for f in flavors)

        # 2. Active Y-junction flux routing load across BCC links
        links = y_junction_links(positions, self.L)
        flux = self.sigma * links

        # 3. Local plaquette spin-spin exchange when quarks overlap on the same BCC cell
        spin = 0.0
        overlaps = 0
        pairs = [(0, 1), (0, 2), (1, 2)]
        for idx, (i, j) in enumerate(pairs):
            if positions[i] == positions[j]:
                overlaps += 1
                g_ij = self.J_plaq * (self.hop[flavors[i]] * self.hop[flavors[j]]) / (self.hop['l'] ** 2)
                spin += g_ij * pair_spins[idx]

        return {
            'total': bare + flux + spin,
            'bare': bare,
            'flux': flux,
            'spin': spin,
            'links': links,
            'overlaps': overlaps,
        }

    def measure_ground_state(self, flavors, pair_spins, n_walkers=500, n_steps=200, dtau=0.002):
        """Extract ground-state mass and average grid workload metrics via imaginary-time projection."""
        walkers = [[(0, 0, 0), (0, 0, 0), (0, 0, 0)] for _ in range(n_walkers)]
        post_burnin = []

        for step in range(n_steps):
            new_walkers = []
            weights = []
            step_records = []

            for pos in walkers:
                trial = list(pos)
                hops_this_tick = 0
                for q_idx, flv in enumerate(flavors):
                    p_hop = min(0.85, 8.0 * self.hop[flv] * dtau)
                    if self.rng.random() < p_hop:
                        dx, dy, dz = self.rng.choice(BCC_DIRS)
                        x, y, z = trial[q_idx]
                        trial[q_idx] = ((x + dx) % self.L, (y + dy) % self.L, (z + dz) % self.L)
                        hops_this_tick += 1

                parts = self.energy_breakdown(trial, flavors, pair_spins)
                parts['hops'] = hops_this_tick
                w = math.exp(-dtau * parts['total'])
                new_walkers.append(trial)
                weights.append(w)
                step_records.append(parts)

            total_w = sum(weights)
            mean_w = total_w / n_walkers
            e_est = -math.log(mean_w) / dtau

            if step >= n_steps // 3:
                # Boltzmann-weighted averages of workload counters for this tick
                avg_bare = sum(w * r['bare'] for w, r in zip(weights, step_records)) / total_w
                avg_flux = sum(w * r['flux'] for w, r in zip(weights, step_records)) / total_w
                avg_spin = sum(w * r['spin'] for w, r in zip(weights, step_records)) / total_w
                avg_links = sum(w * r['links'] for w, r in zip(weights, step_records)) / total_w
                avg_hops = sum(w * r['hops'] for w, r in zip(weights, step_records)) / total_w
                post_burnin.append((e_est, avg_bare, avg_flux, avg_spin, avg_links, avg_hops))

            # Systematic resampling
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

        n = len(post_burnin)
        mass = sum(x[0] for x in post_burnin) / n
        bare = sum(x[1] for x in post_burnin) / n
        flux = sum(x[2] for x in post_burnin) / n
        spin = sum(x[3] for x in post_burnin) / n
        links = sum(x[4] for x in post_burnin) / n
        hops = sum(x[5] for x in post_burnin) / n
        dynamic_pct = 100.0 * (mass - bare) / mass

        return {
            'mass_MeV': mass,
            'bare_MeV': bare,
            'flux_MeV': flux,
            'spin_MeV': spin,
            'avg_links': links,
            'avg_hops': hops,
            'dynamic_pct': dynamic_pct,
        }


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

    print("Running 3D BCC lattice workload simulation...")
    results = {}
    for name, (flvs, spins) in channel_specs.items():
        results[name] = sim.measure_ground_state(flvs, spins)

    derived_params = Parameters.from_anchors(
        N_MeV=results['N']['mass_MeV'],
        Delta_MeV=results['Delta']['mass_MeV'],
        Lambda_MeV=results['Lambda']['mass_MeV'],
    )

    print("\n=== Emergent Constituent Parameters (via Parameters.from_anchors) ===")
    print(f"m_light   = {derived_params.m_light:.2f} MeV  (bare node: {sim.m_bare['l']:.1f} MeV -> {100*(1 - sim.m_bare['l']/derived_params.m_light):.1f}% emergent workload)")
    print(f"m_strange = {derived_params.m_strange:.2f} MeV  (bare node: {sim.m_bare['s']:.1f} MeV -> {100*(1 - sim.m_bare['s']/derived_params.m_strange):.1f}% emergent workload)")
    print(f"A         = {derived_params.A:.2f} MeV  (emergent plaquette hyperfine coupling)")

    print("\n=== Lattice Workload Breakdown vs. Static Pair-Spin Rule ===")
    header = (f"{'Family':10} {'Bare':>7} {'Flux':>8} {'Spin':>8} {'Links':>6} "
              f"{'Dyn%':>6} {'BCC Mass':>10} {'Rule Mass':>10} {'Diff':>7}")
    print(header)
    print("-" * len(header))

    map_to_channel = {
        'N': 'p', 'Delta': 'Delta+', 'Lambda': 'Lambda', 'Sigma': 'Sigma0',
        'Xi': 'Xi0', 'SigmaStar': 'SigmaStar0', 'XiStar': 'XiStar0', 'Omega': 'Omega-',
    }
    for fam, ch in map_to_channel.items():
        r = results[fam]
        rule_m = calculate(ch, parameters=derived_params)['mass_MeV']
        print(f"{fam:10} {r['bare_MeV']:7.1f} {r['flux_MeV']:8.1f} {r['spin_MeV']:8.1f} "
              f"{r['avg_links']:6.2f} {r['dynamic_pct']:5.1f}% {r['mass_MeV']:10.2f} "
              f"{rule_m:10.2f} {r['mass_MeV'] - rule_m:7.2f}")


if __name__ == '__main__':
    run_bridge_experiment()

