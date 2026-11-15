#!/usr/bin/env python3
"""
2-Body EM Link-Flux Attraction, Repulsion & Mass-Gated Recoil on the 6-Face Grid.

Tests the separation between electric charge sign (link-flux orientation +-1)
and particle mass (total tick workload m):
  1. Equal-and-opposite link-flux force (F_12 = -F_21) conserves total momentum
     (p_1 + p_2 = 0) across every tick.
  2. Acceleration scales inversely with tick budget (a = F / m), proving that
     the lighter particle moves more regardless of charge sign:
       - e- (0.511 MeV) vs p+ (938.272 MeV): negative electron moves 1,836x more.
       - p+ (938.272 MeV) vs Xi- (1321.710 MeV): positive proton moves 1.41x more.
       - e- (0.511 MeV) vs e+ (0.511 MeV): exact 50% / 50% symmetric meet.
"""

from typing import Any, Dict


class BCCEMRecoilSim:
    """2-body discrete link-flux force and mass-gated recoil simulator."""

    def __init__(self, k_flux: float = 10.0, min_sep_lp: float = 0.25):
        self.k_flux = k_flux
        self.min_sep = min_sep_lp

    def simulate_pair(
        self,
        name_1: str,
        q1: float,
        mass1_mev: float,
        name_2: str,
        q2: float,
        mass2_mev: float,
        sep0_lp: float = 10.0,
        steps: int = 40,
        dt: float = 0.05,
    ) -> Dict[str, Any]:
        """
        Evolve two charged loop particles along a 1D 6-face axis under inverse-square
        link-flux force F = k_flux * q1 * q2 / r^2 (attractive if q1*q2 < 0, repulsive if > 0).
        """
        x1 = -0.5 * sep0_lp
        x2 = +0.5 * sep0_lp
        v1 = 0.0
        v2 = 0.0

        for _ in range(steps):
            r = max(self.min_sep, x2 - x1)
            # Force on particle 2 from particle 1 (+x if repulsive, -x if attractive)
            f_on_2 = (self.k_flux * q1 * q2) / (r ** 2)
            f_on_1 = -f_on_2

            v1 += (f_on_1 / mass1_mev) * dt
            v2 += (f_on_2 / mass2_mev) * dt
            x1 += v1 * dt
            x2 += v2 * dt

        disp1 = abs(x1 - (-0.5 * sep0_lp))
        disp2 = abs(x2 - (+0.5 * sep0_lp))
        tot_disp = max(1e-18, disp1 + disp2)
        p_tot = mass1_mev * v1 + mass2_mev * v2
        interaction = "Attraction (flux cancellation)" if q1 * q2 < 0 else "Repulsion (flux pile-up)"

        return {
            "pair": f"{name_1} vs {name_2}",
            "interaction": interaction,
            "disp1_lp": disp1,
            "disp2_lp": disp2,
            "share1_pct": round((disp1 / tot_disp) * 100.0, 2),
            "share2_pct": round((disp2 / tot_disp) * 100.0, 2),
            "disp_ratio_1_to_2": round(disp1 / max(1e-18, disp2), 2),
            "final_sep_lp": round(x2 - x1, 4),
            "momentum_residual": round(abs(p_tot), 12),
        }


def run_em_recoil_demo() -> None:
    sim = BCCEMRecoilSim(k_flux=50.0)
    cases = [
        ("e- (-1, 0.511 MeV)", -1.0, 0.511, "p+ (+1, 938.27 MeV)", +1.0, 938.272),
        ("p+ (+1, 938.27 MeV)", +1.0, 938.272, "Xi- (-1, 1321.71 MeV)", -1.0, 1321.710),
        ("e- (-1, 0.511 MeV)", -1.0, 0.511, "e+ (+1, 0.511 MeV)", +1.0, 0.511),
        ("p+ (+1, 938.27 MeV)", +1.0, 938.272, "p+ (+1, 938.27 MeV)", +1.0, 938.272),
    ]

    print("=== 2-Body EM Link-Flux Attraction/Repulsion & Mass-Gated Recoil ===")
    print("Particle Pair                           Regime                          Move% (1 vs 2)   Ratio 1/2   p_tot")
    print("-" * 108)
    for n1, q1, m1, n2, q2, m2 in cases:
        res = sim.simulate_pair(n1, q1, m1, n2, q2, m2, sep0_lp=10.0, steps=40, dt=0.05)
        move_str = f"{res['share1_pct']:5.2f}% vs {res['share2_pct']:5.2f}%"
        print(
            f"{res['pair']:<39} {res['interaction']:<31} {move_str:<16} "
            f"{res['disp_ratio_1_to_2']:>8.2f}x   {res['momentum_residual']:.1e}"
        )


if __name__ == "__main__":
    run_em_recoil_demo()
