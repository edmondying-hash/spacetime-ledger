#!/usr/bin/env python3
"""
Converging Starlight Black Hole (Kugelblitz), Recoil Conservation & Frame-Dragging Spin.

Toy-model simulation testing three coupled lattice mechanisms:
  1. Central Light-Web Congestion (Kugelblitz): Photons emitted inward from a ring
     of stars overlap at the galactic center. Below the 100-tick/cycle node cap,
     light passes freely; above W(0) >= 100, central nodes deadlock into a
     radiation-seeded black hole (0 escape).
  2. Symmetry Breaking -> Core Torque: A mirror-symmetric ring yields L_z = 0.
     A slight asymmetry tilts inward rays off-axis, injecting tangential torque.
  3. Action=Reaction Recoil vs. 1/r^3 Frame-Dragging: In an isolated L_total = 0
     system, spinning up the core (+L_core) forces stars to counter-rotate (-L_core).
     Once spinning from tidal infall (L_total > 0), the core's outward 1/r^3 routing
     curl drags inner orbits into co-rotation (Lense-Thirring / Bardeen-Petterson).
"""

import math
from typing import Any, Dict, List


class BCCKugelblitzSpinSim:
    """Simulates converging starlight congestion, recoil conservation, and frame-dragging."""

    def __init__(self, node_cap: float = 100.0, ring_radius_lp: float = 10.0):
        self.node_cap = node_cap
        self.ring_radius = ring_radius_lp

    def simulate_star_ring(
        self,
        num_stars: int = 24,
        ray_ticks: float = 5.0,
        asymmetry_bias: float = 0.0,
        aim_offset_lp: float = 0.6,
    ) -> Dict[str, Any]:
        """
        Trace inward photon rays from `num_stars` around a galactic ring of radius R.
        Returns central workload, net core angular momentum L_core, action-reaction star
        recoil L_stars = -L_core, and frame-dragging spin parameter.
        """
        central_workload = 0.0
        net_lz = 0.0
        total_flux = 0.0

        for k in range(num_stars):
            theta = (2.0 * math.pi * k) / num_stars
            weight = max(0.1, 1.0 + asymmetry_bias * math.sin(theta))
            flux = ray_ticks * weight

            b_k = asymmetry_bias * aim_offset_lp * (1.0 + 0.5 * math.cos(theta))
            overlap = math.exp(-0.5 * (b_k ** 2))
            central_workload += flux * overlap
            net_lz += flux * b_k
            total_flux += flux

        deadlocked = central_workload >= self.node_cap
        spin_omega = net_lz / max(1.0, total_flux * self.ring_radius)
        recoil_lz = -net_lz

        if abs(spin_omega) < 1e-6:
            direction = "Non-Rotating (Symmetric)"
        elif spin_omega > 0:
            direction = "Counter-Clockwise (CCW)"
        else:
            direction = "Clockwise (CW)"

        return {
            "num_stars": num_stars,
            "ray_ticks": ray_ticks,
            "asymmetry_bias": asymmetry_bias,
            "central_workload": round(central_workload, 2),
            "deadlocked_bh": deadlocked,
            "net_lz": round(net_lz, 4),
            "recoil_stars_lz": round(recoil_lz, 4),
            "ledger_sum_lz": round(net_lz + recoil_lz, 10),
            "frame_drag_omega": round(spin_omega, 6),
            "rotation_dir": direction,
        }

    def frame_dragging_radial_profile(
        self, core_lz: float, radii: List[float]
    ) -> List[Dict[str, Any]]:
        """
        Compute outward Lense-Thirring frame-dragging angular rate omega_drag(r) = 2 * L_core / r^3
        from a spinning central core (acquired via external tidal infall L_total > 0).
        """
        rows: List[Dict[str, Any]] = []
        for r in radii:
            omega_drag = (2.0 * core_lz) / (r ** 3)
            rows.append({
                "r": r,
                "core_lz": round(core_lz, 4),
                "omega_drag": round(omega_drag, 6),
                "r3_invariant": round(omega_drag * (r ** 3), 4),
                "alignment": "Co-rotating drag (Bardeen-Petterson)" if omega_drag > 1e-3 else "Weak outer drift",
            })
        return rows


def run_kugelblitz_spin_demo() -> None:
    sim = BCCKugelblitzSpinSim(node_cap=100.0, ring_radius_lp=10.0)

    print("=== PART 1: Star-Ring Photon Convergence (Normal Galaxy vs. Kugelblitz Black Hole) ===")
    print("Stars   Ray Ticks   Central W(0)   100-Cap Status          Emergent Core State")
    print("-" * 82)
    for n_stars, r_ticks in [(12, 3.0), (16, 5.0), (24, 5.0), (36, 6.0)]:
        res = sim.simulate_star_ring(num_stars=n_stars, ray_ticks=r_ticks, asymmetry_bias=0.0)
        cap_str = "OVER CAP (>= 100)" if res["deadlocked_bh"] else "Under Cap (< 100)"
        state = "DEADLOCKED Black Hole (0 escape)" if res["deadlocked_bh"] else "Transparent Light Web"
        print(f"{n_stars:>5} {r_ticks:>11.1f} {res['central_workload']:>14.2f}   {cap_str:<21}   {state}")

    print("\n=== PART 2: Ring Asymmetry -> Core Torque & Action=Reaction Recoil (L_total = 0) ===")
    print("Asymmetry   Core L_z   Star Recoil L_z   Ledger Sum   Core Spin Direction")
    print("-" * 80)
    for bias in [0.0, 0.08, -0.08, 0.20]:
        res = sim.simulate_star_ring(num_stars=24, ray_ticks=5.0, asymmetry_bias=bias)
        print(
            f"{bias:>+9.2f} {res['net_lz']:>+10.4f} {res['recoil_stars_lz']:>+17.4f} "
            f"{res['ledger_sum_lz']:>12.4f}   {res['rotation_dir']}"
        )

    print("\n=== PART 3: Outward Lense-Thirring Frame-Dragging (omega_drag ~ 1/r^3 from Tidal Infall) ===")
    print("Radius r   Core L_z   Drag omega(r)   r^3 * omega   Disk Alignment Regime")
    print("-" * 78)
    for row in sim.frame_dragging_radial_profile(core_lz=14.4, radii=[2.0, 3.0, 5.0, 8.0, 10.0]):
        print(
            f"{row['r']:>8.1f} {row['core_lz']:>10.4f} {row['omega_drag']:>15.6f} "
            f"{row['r3_invariant']:>13.4f}   {row['alignment']}"
        )


if __name__ == "__main__":
    run_kugelblitz_spin_demo()
