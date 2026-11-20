#!/usr/bin/env python3
"""
Converging Starlight Black Hole (Kugelblitz), Recoil Ledger & 3D BCC Frame-Dragging.

Upgraded for the 3D BCC (8-Diagonal) Spacetime Network:
  1. 3D BCC Light-Web Convergence (Kugelblitz): Photons emitted inward from a ring
     of stars hop across 3D BCC diagonals to the galactic center. Below the 100-tick
     node cap, light passes freely; at W(0) >= 100, central BCC nodes deadlock into a
     radiation-seeded black hole (0 escape) with dimensionless Kerr spin a* = L / M^2.
  2. Symmetry Breaking -> Core Torque & Recoil Conservation: Mirror-symmetric infall
     yields L_z = 0. Off-axis aim bias injects tangential torque (+L_core) while
     conserving total server angular momentum (L_core + L_stars = 0.0000).
  3. Outward 3D BCC Lense-Thirring Frame-Dragging (omega_drag = 2 * L_core / r^3):
     Measures the azimuthal link-drag curl across 3D BCC radial shells and verifies
     the exact r^3 * omega invariant.
"""

import math
from typing import Any, Dict, List


class BCCKugelblitzSpinSim:
    """Simulates 3D BCC converging starlight black holes, recoil, and frame dragging."""

    def __init__(self, node_cap: float = 100.0, ring_radius_bcc: float = 12.0):
        self.node_cap = node_cap
        self.ring_radius = ring_radius_bcc  # In 3D BCC diagonal units (sqrt(3) l_P)

    def simulate_star_ring(
        self,
        num_stars: int = 24,
        ray_ticks: float = 5.0,
        asymmetry_bias: float = 0.0,
        aim_offset_bcc: float = 0.65,
    ) -> Dict[str, Any]:
        """
        Route inward photon rays across 3D BCC nodes from `num_stars` on an equatorial
        ring of radius R. Computes central node workload W(0), Kerr spin a*, net torque
        L_core, and exact action-reaction star recoil L_stars = -L_core.
        """
        central_workload = 0.0
        net_lz = 0.0
        total_flux = 0.0

        for k in range(num_stars):
            theta = (2.0 * math.pi * k) / num_stars
            # Snap star coordinates to nearest even-parity 3D BCC equatorial site (x, y, 0)
            sx = 2 * round((self.ring_radius * math.cos(theta)) / 2.0)
            sy = 2 * round((self.ring_radius * math.sin(theta)) / 2.0)
            r_bcc = max(2.0, math.hypot(sx, sy))

            weight = max(0.1, 1.0 + asymmetry_bias * math.sin(theta))
            flux = ray_ticks * weight

            # Tangential impact offset b_k in BCC diagonal units
            b_k = asymmetry_bias * aim_offset_bcc * (1.0 + 0.5 * math.cos(theta))
            # Gaussian beam overlap across the central BCC truncated-octahedron cell
            overlap = math.exp(-0.5 * ((b_k / 0.85) ** 2))

            central_workload += flux * overlap
            # Angular momentum L_z = p_tangential * r = flux * b_k
            net_lz += flux * b_k
            total_flux += flux * (self.ring_radius / r_bcc)

        deadlocked = central_workload >= self.node_cap
        # Dimensionless Kerr spin parameter a* = |L_z| / (W(0)^2 / node_cap)
        mass_equiv = max(1.0, central_workload / 10.0)
        kerr_a_star = min(0.999, abs(net_lz) / (mass_equiv ** 2))
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
            "kerr_a_star": round(kerr_a_star, 4),
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
        Compute outward Lense-Thirring frame-dragging angular velocity
        omega_drag(r) = 2 * L_core / r^3 across 3D BCC shells.
        """
        rows: List[Dict[str, Any]] = []
        for r in radii:
            omega_drag = (2.0 * core_lz) / (r ** 3)
            rows.append({
                "r": r,
                "core_lz": round(core_lz, 4),
                "omega_drag": round(omega_drag, 6),
                "r3_invariant": round(omega_drag * (r ** 3), 4),
                "alignment": (
                    "Strong Co-Rotating Drag (Bardeen-Petterson)"
                    if omega_drag >= 0.05
                    else "Weak Outer Drift"
                ),
            })
        return rows


def run_kugelblitz_spin_demo() -> None:
    sim = BCCKugelblitzSpinSim(node_cap=100.0, ring_radius_bcc=12.0)

    print("=" * 86)
    print("PART 1: 3D BCC Star-Ring Photon Convergence (Light Web vs. Kugelblitz Black Hole)")
    print("=" * 86)
    print("Stars   Ray Ticks   Central W(0)   100-Cap Status          Emergent Core State")
    print("-" * 86)
    for n_stars, r_ticks in [(12, 3.0), (16, 5.0), (24, 5.0), (36, 6.0)]:
        res = sim.simulate_star_ring(num_stars=n_stars, ray_ticks=r_ticks, asymmetry_bias=0.0)
        cap_str = "OVER CAP (>= 100)" if res["deadlocked_bh"] else "Under Cap (< 100)"
        state = "DEADLOCKED Black Hole (0 escape)" if res["deadlocked_bh"] else "Transparent Light Web"
        print(f"{n_stars:>5} {r_ticks:>11.1f} {res['central_workload']:>14.2f}   {cap_str:<21}   {state}")

    print("\n" + "=" * 86)
    print("PART 2: Ring Asymmetry -> Core Torque, Kerr Spin a* & Recoil Ledger (L_total = 0)")
    print("=" * 86)
    print("Asymmetry   Core L_z   Star Recoil L_z   Ledger Sum   Kerr a*   Core Spin Direction")
    print("-" * 86)
    for bias in [0.0, 0.08, -0.08, 0.20]:
        res = sim.simulate_star_ring(num_stars=24, ray_ticks=5.0, asymmetry_bias=bias)
        print(
            f"{bias:>+9.2f} {res['net_lz']:>+10.4f} {res['recoil_stars_lz']:>+17.4f} "
            f"{res['ledger_sum_lz']:>12.4f} {res['kerr_a_star']:>9.4f}   {res['rotation_dir']}"
        )

    print("\n" + "=" * 86)
    print("PART 3: Outward 3D BCC Lense-Thirring Frame-Dragging (omega_drag = 2*L_core / r^3)")
    print("=" * 86)
    print("Radius r   Core L_z   Drag omega(r)   r^3 * omega   Disk Alignment Regime")
    print("-" * 86)
    sample_lz = sim.simulate_star_ring(num_stars=24, ray_ticks=5.0, asymmetry_bias=0.20)["net_lz"]
    for row in sim.frame_dragging_radial_profile(core_lz=sample_lz, radii=[2.0, 4.0, 6.0, 8.0, 10.0]):
        print(
            f"{row['r']:>8.1f} {row['core_lz']:>10.4f} {row['omega_drag']:>15.6f} "
            f"{row['r3_invariant']:>13.4f}   {row['alignment']}"
        )


if __name__ == "__main__":
    run_kugelblitz_spin_demo()
