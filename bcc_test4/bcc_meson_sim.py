#!/usr/bin/env python3
"""6-Face Planck Grid Meson Flux-Tube & Mass Spectrum Simulator.

Models quark-antiquark (q qbar) pairs connected across 6 orthogonal faces (±x, ±y, ±z)
of 1.0 l_P^3 Planck cubes:
1. Ground-state meson mass spectrum across light (u/d), strange (s), and charm (c)
   sectors with exact 3:1 pseudoscalar (J=0) vs. vector (J=1) color-magnetic hyperfine
   splitting and 1/(m_i m_j) heavy-quark suppression.
2. Color flux-tube stretch & string breaking: separating q and qbar across 6-face
   Manhattan hops increases routing workload linearly until hitting the pion-pair
   creation threshold (275.0 MeV), snapping into two lighter mesons (color confinement).
"""

# Constituent quark masses (MeV) calibrated on the 6-face Planck grid
QUARK_MASS_MEV = {
    'l': 310.0,   # light (u / d)
    's': 485.0,   # strange
    'c': 1550.0,  # charm
}

# Hyperfine coupling constant A_meson (MeV^3) scaled by light-quark mass squared
M_LIGHT = QUARK_MASS_MEV['l']
A_MESON_BASE = 160.0 * (M_LIGHT ** 2)  # yields -480 MeV for J=0 pi and +160 MeV for J=1 rho
MEV_PER_TICK = 5.0
PION_PAIR_THRESHOLD_MEV = 275.0
TUBE_TENSION_MEV_PER_HOP = 45.0

MESON_CHANNELS = [
    ('pi',    ('l', 'l'), 0, 138.04),
    ('rho',   ('l', 'l'), 1, 775.26),
    ('K',     ('l', 's'), 0, 495.64),
    ('K*',    ('l', 's'), 1, 893.60),
    ('phi',   ('s', 's'), 1, 1019.46),
    ('D',     ('l', 'c'), 0, 1867.20),
    ('D*',    ('l', 'c'), 1, 2008.55),
    ('J/psi', ('c', 'c'), 1, 3096.90),
]


class BCCMesonSim:
    """6-face quark-antiquark flux-tube and hyperfine mass calculator."""

    def __init__(self, mev_per_tick=MEV_PER_TICK):
        self.mev_per_tick = mev_per_tick

    def evaluate_meson(self, name, flavors, spin_j, pdg_mev=None):
        """Compute bare capacitance ticks, flux-tube routing ticks, and exact 3:1 SpinT."""
        q1, q2 = flavors
        if q1 not in QUARK_MASS_MEV or q2 not in QUARK_MASS_MEV:
            raise ValueError(f"Unknown quark flavor in {flavors}")
        if spin_j not in (0, 1):
            raise ValueError("Meson total spin J must be 0 (pseudoscalar) or 1 (vector)")

        m1 = QUARK_MASS_MEV[q1]
        m2 = QUARK_MASS_MEV[q2]

        # Color-spin factor: <S1 . S2> = -3/4 for J=0 (singlet), +1/4 for J=1 (triplet)
        # Multiply by 4 so J=0 -> -3 and J=1 -> +1 (exact 3:1 magnitude ratio)
        spin_factor = -3.0 if spin_j == 0 else 1.0
        spin_mev = spin_factor * (A_MESON_BASE / (m1 * m2))

        # Split baseline (m1 + m2) into bare capacitance ticks + active 6-face flux-tube routing
        bare_mev = 0.25 * (m1 + m2)
        route_mev = 0.75 * (m1 + m2)
        total_mev = bare_mev + route_mev + spin_mev

        bare_ticks = round(bare_mev / self.mev_per_tick, 2)
        route_ticks = round(route_mev / self.mev_per_tick, 2)
        # Keep full floating precision on SpinT so |SpinT(J=0)| / |SpinT(J=1)| == 3.0000 exactly
        spin_ticks = spin_mev / self.mev_per_tick

        return {
            'name': name,
            'flavors': f"{q1}{q2}bar",
            'J': spin_j,
            'BareT': bare_ticks,
            'RouteT': route_ticks,
            'SpinT': spin_ticks,
            'ModelMeV': round(total_mev, 2),
            'PDGMeV': pdg_mev,
            'DiffMeV': round(total_mev - pdg_mev, 2) if pdg_mev is not None else None,
        }

    def run_spectrum(self):
        """Evaluate all 8 ground-state meson channels."""
        return [
            self.evaluate_meson(name, flv, j, pdg)
            for name, flv, j, pdg in MESON_CHANNELS
        ]

    def simulate_flux_tube_stretch(self, max_hops=9):
        """Stretch a q-qbar flux tube across 6-face Manhattan hops until string breaking."""
        steps = []
        broken_at = None
        for hops in range(max_hops + 1):
            tube_mev = hops * TUBE_TENSION_MEV_PER_HOP
            tube_ticks = tube_mev / self.mev_per_tick
            if tube_mev >= PION_PAIR_THRESHOLD_MEV and broken_at is None:
                broken_at = hops
            status = "SNAPPED -> 2 mesons (confined)" if tube_mev >= PION_PAIR_THRESHOLD_MEV else "Intact flux tube"
            steps.append({
                'hops': hops,
                'tube_ticks': round(tube_ticks, 1),
                'tube_mev': round(tube_mev, 2),
                'broken': tube_mev >= PION_PAIR_THRESHOLD_MEV,
                'status': status,
            })
        return {
            'threshold_mev': PION_PAIR_THRESHOLD_MEV,
            'tension_mev_per_hop': TUBE_TENSION_MEV_PER_HOP,
            'snapped_at_hop': broken_at,
            'steps': steps,
        }


def run_meson_demo():
    sim = BCCMesonSim()
    spectrum = sim.run_spectrum()

    print("=== PART 1: 6-Face Planck Grid Ground-State Meson Spectrum (q qbar) ===")
    print(f"{'Meson':<7} {'Quarks':<7} {'J':>2} {'BareT':>7} {'RouteT':>8} {'SpinT':>8} {'ModelMeV':>10} {'PDGMeV':>9} {'Diff':>8}")
    print("-" * 74)
    for row in spectrum:
        print(
            f"{row['name']:<7} {row['flavors']:<7} {row['J']:>2d} {row['BareT']:>7.2f} "
            f"{row['RouteT']:>8.2f} {row['SpinT']:>8.2f} {row['ModelMeV']:>10.2f} "
            f"{row['PDGMeV']:>9.2f} {row['DiffMeV']:>+8.2f}"
        )

    stretch = sim.simulate_flux_tube_stretch(max_hops=9)
    print(f"=== PART 2: Color Flux-Tube Stretch & String Breaking (Threshold = {stretch['threshold_mev']:.1f} MeV) ===")
    print(f"{'6-Face Hops':>11} {'Tube Ticks':>11} {'Stored MeV':>12}   {'State'}")
    print("-" * 68)
    for st in stretch['steps']:
        print(f"{st['hops']:>11d} {st['tube_ticks']:>11.1f} {st['tube_mev']:>12.2f}   {st['status']}")


if __name__ == '__main__':
    run_meson_demo()
