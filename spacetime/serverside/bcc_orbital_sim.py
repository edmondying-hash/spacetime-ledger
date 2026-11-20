#!/usr/bin/env python3
"""3D BCC Orbital Mechanics: Emergent Orbits & Perihelion Precession from Node Congestion."""

import argparse
import math
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np


class BCCOrbitalEngine:
    """Routes wavepackets through a 3D BCC radial node-congestion field c_eff(r)."""

    def __init__(self, core_mass_mev: float = 1218.3, cluster_count: int = 18):
        # Coupled directly to Module 1 mass workload (default: Omega cluster)
        self.coupling = (core_mass_mev / 938.0) * cluster_count * 0.28
        self.horizon_radius = 4.5  # 100% node tick saturation radius

    def c_eff(self, r: float) -> float:
        """Local effective propagation speed from 1/r BCC node queuing delay."""
        r_safe = max(r, self.horizon_radius)
        util = self.coupling / r_safe
        return 1.0 / (1.0 + util)

    def grad_c_eff(self, pos: np.ndarray) -> np.ndarray:
        """Spatial gradient of local BCC tick speed across the wavepacket width."""
        r = float(np.linalg.norm(pos))
        if r <= self.horizon_radius:
            return np.zeros(3)
        # d/dr [1 / (1 + k/r)] = (k / r^2) / (1 + k/r)^2
        dc_dr = (self.coupling / (r * r)) / ((1.0 + self.coupling / r) ** 2)
        return dc_dr * (pos / r)

    def trace_trajectory(
        self,
        r0: float = 24.0,
        v_tan_ratio: float = 1.0,
        ticks: int = 1600,
        dt: float = 0.5,
    ) -> Dict[str, object]:
        """Integrate wavepacket refraction through the 3D BCC congestion gradient."""
        # Circular orbit balance condition: v^2 / r = c_eff * |grad(c_eff)|
        c0 = self.c_eff(r0)
        g0 = float(np.linalg.norm(self.grad_c_eff(np.array([r0, 0.0, 0.0]))))
        v_circ = math.sqrt(r0 * c0 * g0)

        pos = np.array([r0, 0.0, 0.0], dtype=np.float64)
        # Slight 3D tilt (vz != 0) to demonstrate full 3D BCC orbital plane
        vel = np.array([0.0, v_circ * v_tan_ratio, 0.06 * v_circ], dtype=np.float64)

        path: List[np.ndarray] = [pos.copy()]
        radii: List[float] = [r0]
        perihelion_angles: List[float] = []
        captured = False

        for _ in range(ticks):
            # Velocity-Verlet / Leapfrog refractive steering (a = -c_eff * grad(c_eff))
            acc1 = -self.c_eff(float(np.linalg.norm(pos))) * self.grad_c_eff(pos)
            pos_next = pos + vel * dt + 0.5 * acc1 * (dt * dt)
            r_next = float(np.linalg.norm(pos_next))

            if r_next <= self.horizon_radius:
                captured = True
                path.append(pos_next.copy())
                radii.append(r_next)
                break

            acc2 = -self.c_eff(r_next) * self.grad_c_eff(pos_next)
            vel = vel + 0.5 * (acc1 + acc2) * dt
            pos = pos_next

            path.append(pos.copy())
            radii.append(r_next)

            # Detect local radial minima (perihelion passages)
            if len(radii) >= 3 and radii[-2] < radii[-3] and radii[-2] < radii[-1]:
                px, py, _ = path[-2]
                angle_deg = math.degrees(math.atan2(float(py), float(px))) % 360.0
                perihelion_angles.append(angle_deg)

            if r_next > r0 * 3.5:
                break

        pts = np.array(path)
        precession_per_orbit = 0.0
        if len(perihelion_angles) >= 2:
            diffs = [
                (perihelion_angles[i + 1] - perihelion_angles[i]) % 360.0
                for i in range(len(perihelion_angles) - 1)
            ]
            precession_per_orbit = sum(diffs) / len(diffs)

        return {
            "points": pts,
            "min_r": round(min(radii), 2),
            "max_r": round(max(radii), 2),
            "captured": captured,
            "perihelions": len(perihelion_angles),
            "precession_deg": round(precession_per_orbit, 2),
        }


def run_orbital_suite(out_png: str = "bcc_orbits.png") -> None:
    sim = BCCOrbitalEngine(core_mass_mev=1218.3, cluster_count=18)

    scenarios = [
        ("Circular Orbit (1.00 v_circ)", 1.00, 1400, "#2a9d8f"),
        ("Precessing Ellipse (0.84 v_circ)", 0.84, 2200, "#f77f00"),
        ("Hyperbolic Flyby (1.42 v_circ)", 1.42, 600, "#457b9d"),
        ("Horizon Capture (0.32 v_circ)", 0.32, 600, "#d62828"),
    ]

    print("=" * 78)
    print("3D BCC CONGESTION ORBITAL MECHANICS (Refractive Wavepacket Steering)")
    print("=" * 78)
    print("Trajectory Regime              | Min R | Max R | Orbits | Precession/Orbit")
    print("-" * 78)

    fig, (ax_xy, ax_3d) = plt.subplots(
        1, 2, figsize=(14, 6.2), subplot_kw={"projection": None}
    )
    fig.clf()
    ax_xy = fig.add_subplot(1, 2, 1)
    ax_3d = fig.add_subplot(1, 2, 2, projection="3d")

    # Plot 100%-saturated BCC Horizon Core
    horizon = plt.Circle((0, 0), sim.horizon_radius, color="#1d1e2c", label="Saturation Horizon (r=4.5)")
    ax_xy.add_patch(horizon)

    for label, v_ratio, steps, color in scenarios:
        res = sim.trace_trajectory(r0=24.0, v_tan_ratio=v_ratio, ticks=steps)
        pts = res["points"]
        status = "CAPTURED" if res["captured"] else f"{res['precession_deg']:>6.2f}°/orbit"
        print(
            f"{label:<30} | {res['min_r']:>5.1f} | {res['max_r']:>5.1f} | "
            f"{res['perihelions']:>6} | {status}"
        )

        ax_xy.plot(pts[:, 0], pts[:, 1], color=color, linewidth=1.8, label=label)
        ax_3d.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=color, linewidth=1.8, label=label)

    ax_xy.set_aspect("equal")
    ax_xy.set_xlim(-32, 32)
    ax_xy.set_ylim(-32, 32)
    ax_xy.set_xlabel("X (BCC Lattice Units)")
    ax_xy.set_ylabel("Y (BCC Lattice Units)")
    ax_xy.set_title("Equatorial Projection: Orbits & Perihelion Precession", fontweight="bold")
    ax_xy.grid(True, linestyle=":", alpha=0.6)
    ax_xy.legend(loc="upper right", fontsize=8)

    ax_3d.scatter((0,), (0,), (0,), s=180, color="#1d1e2c", label="Congested BCC Core")
    ax_3d.set_xlim(-28, 28)
    ax_3d.set_ylim(-28, 28)
    ax_3d.set_zlim(-8, 8)
    ax_3d.set_xlabel("X")
    ax_3d.set_ylabel("Y")
    ax_3d.set_zlabel("Z")
    ax_3d.set_title("3D BCC Tilted Orbital Trajectories", fontweight="bold")
    ax_3d.view_init(elev=24, azim=40)

    plt.tight_layout()
    plt.savefig(out_png, dpi=180)
    print("-" * 78)
    print(f"[Saved 3D BCC orbital plot -> {out_png}]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate orbits around a congested BCC mass core")
    parser.add_argument("--out", type=str, default="bcc_orbits.png", help="Output PNG filename")
    args = parser.parse_args()
    run_orbital_suite(out_png=args.out)


if __name__ == "__main__":
    main()
