#!/usr/bin/env python3
"""Orbits in an inserted congestion field c_eff(r) = 1/(1 + k/r) (smooth 3D, not a lattice walk).

Inserted, not emergent: the 1/r congestion law and the force a = -c_eff grad c_eff.
FIXED: periapsis advance is measured from successive periapses in the orbital plane.
"""

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
        # Slight 3D tilt to show a tilted orbital plane.  FIXED: the tilt now rotates the
        # velocity instead of adding vz = 0.06 v_circ (which raised the speed above v_circ,
        # so the "circular" orbit was not circular).
        tilt = math.atan(0.06)
        speed = v_circ * v_tan_ratio
        vel = np.array([0.0, speed * math.cos(tilt), speed * math.sin(tilt)], dtype=np.float64)

        path: List[np.ndarray] = [pos.copy()]
        radii: List[float] = [r0]
        swept: List[float] = [0.0]          # cumulative in-plane angle swept (rad)
        peri_swept: List[float] = []         # swept angle at each periapsis
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

            prev = path[-1]
            path.append(pos.copy())
            radii.append(r_next)
            cosang = float(np.dot(prev, pos) / (np.linalg.norm(prev) * np.linalg.norm(pos)))
            swept.append(swept[-1] + math.acos(max(-1.0, min(1.0, cosang))))

            # Periapsis passages: local minima of r, refined by a parabola through 3 samples
            if len(radii) >= 3 and radii[-2] < radii[-3] and radii[-2] < radii[-1]:
                r_a, r_b, r_c = radii[-3], radii[-2], radii[-1]
                denom = r_a - 2.0 * r_b + r_c
                frac = 0.5 * (r_a - r_c) / denom if denom > 0 else 0.0
                s_b = swept[-2]
                ds = (swept[-1] - swept[-3]) / 2.0
                peri_swept.append(s_b + frac * ds)

            if r_next > r0 * 3.5:
                break

        pts = np.array(path)
        r_min, r_max = min(radii), max(radii)
        ecc = (r_max - r_min) / (r_max + r_min)
        # FIXED: advance = (swept angle between successive periapses) - 360 deg.
        # The old code averaged (atan2 angle difference mod 360), i.e. reported the
        # full inter-periapsis angle (~272-281 deg), not the advance, and read noise
        # minima on the circular orbit as periapses.
        advances = [math.degrees(peri_swept[i + 1] - peri_swept[i]) - 360.0
                    for i in range(len(peri_swept) - 1)]
        if ecc < 1e-3:
            precession_per_orbit = 0.0      # circular: periapsis undefined
            status = "circular"
        elif advances:
            precession_per_orbit = sum(advances) / len(advances)
            status = "measured"
        else:
            precession_per_orbit = float("nan")
            status = "fewer than 2 periapses"

        return {
            "points": pts,
            "min_r": round(min(radii), 2),
            "max_r": round(max(radii), 2),
            "captured": captured,
            "perihelions": len(peri_swept),
            "eccentricity": round(ecc, 5),
            "precession_deg": round(precession_per_orbit, 3),
            "precession_status": status,
            "orbits_swept": round(swept[-1] / (2 * math.pi), 2),
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
    print("Advance per orbit = swept angle between successive periapses - 360 deg (+ = prograde)")
    print("Trajectory Regime                | Min R | Max R |   e     | Periapses | Advance/Orbit")
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
        if res["captured"]:
            status = "CAPTURED"
        elif res["precession_status"] == "circular":
            status = "~0 (circular, e < 1e-3)"
        elif res["precession_status"] == "measured":
            status = f"{res['precession_deg']:+8.3f} deg/orbit"
        else:
            status = "n/a (unbound or < 2 periapses)"
        print(
            f"{label:<32} | {res['min_r']:>5.1f} | {res['max_r']:>5.1f} | {res['eccentricity']:.5f} | "
            f"{res['perihelions']:>9} | {status}"
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
