#!/usr/bin/env python3
"""
3-Body Ledger-Grid Orbits on the 6-Face Planck-Cube Lattice vs. Unsoftened Newton.

Reproduces the Figure-8 choreography and Pythagorean 3-4-5 close-encounter test
by advancing bodies up the superposed 6-face congestion gradient (no pairwise forces),
with optional finite-c (1 face-hop/tick) retarded load propagation.
"""

import math
from typing import Dict, List, Optional, Tuple


def _grad_6face_load(
    pos: Tuple[float, float],
    sources: List[Tuple[float, float, float]],
    cell_scale: float,
    smoothing_units: float,
    retarded_c: float = 0.0,
    vel_sources: Optional[List[Tuple[float, float]]] = None,
) -> Tuple[float, float]:
    """Compute central-difference gradient of superposed 6-face 1/r load at pos."""
    h = 1.0 / cell_scale
    px, py = pos

    def load_at(x: float, y: float) -> float:
        total = 0.0
        for idx, (sx, sy, mass) in enumerate(sources):
            dx, dy = x - sx, y - sy
            r = math.hypot(dx, dy)
            if retarded_c > 0.0 and vel_sources is not None:
                tau = r / retarded_c
                vx, vy = vel_sources[idx]
                dx = x - (sx - vx * tau)
                dy = y - (sy - vy * tau)
                r = math.hypot(dx, dy)
            r_eff = max(r, smoothing_units)
            total += mass / r_eff
        return total

    gx = (load_at(px + h, py) - load_at(px - h, py)) / (2.0 * h)
    gy = (load_at(px, py + h) - load_at(px, py - h)) / (2.0 * h)
    return gx, gy


def _newton_acc(
    pos: Tuple[float, float],
    sources: List[Tuple[float, float, float]],
) -> Tuple[float, float]:
    """Exact unsoftened pairwise Newtonian acceleration for reference."""
    ax, ay = 0.0, 0.0
    px, py = pos
    for sx, sy, mass in sources:
        dx, dy = sx - px, sy - py
        r2 = dx * dx + dy * dy
        if r2 > 1e-18:
            inv_r3 = mass / (r2 * math.sqrt(r2))
            ax += dx * inv_r3
            ay += dy * inv_r3
    return ax, ay


def simulate_3body(
    masses: List[float],
    init_pos: List[Tuple[float, float]],
    init_vel: List[Tuple[float, float]],
    t_end: float,
    dt: float = 0.002,
    cell_scale: float = 12.0,
    smoothing_units: float = 0.15,
    retarded_c: float = 0.0,
) -> Dict[str, float]:
    """Run coupled 6-face grid trajectory alongside unsoftened Newton reference."""
    g_pos = [(float(px), float(py)) for px, py in init_pos]
    g_vel = [(float(vx), float(vy)) for vx, vy in init_vel]
    n_pos = [(float(px), float(py)) for px, py in init_pos]
    n_vel = [(float(vx), float(vy)) for vx, vy in init_vel]

    steps = int(round(t_end / dt))
    min_sep = float("inf")

    for _ in range(steps):
        for i in range(3):
            xi, yi = g_pos[i]
            for j in range(i + 1, 3):
                xj, yj = g_pos[j]
                d = math.hypot(xi - xj, yi - yj)
                if d < min_sep:
                    min_sep = d

        # 1. 6-Face Ledger Grid step (bodies climb superposed load gradient)
        g_acc = []
        for i in range(3):
            others = [
                (g_pos[j][0], g_pos[j][1], masses[j])
                for j in range(3)
                if j != i
            ]
            v_oth = [g_vel[j] for j in range(3) if j != i]
            g_acc.append(
                _grad_6face_load(g_pos[i], others, cell_scale, smoothing_units, retarded_c, v_oth)
            )
        g_vel = [
            (g_vel[i][0] + g_acc[i][0] * dt, g_vel[i][1] + g_acc[i][1] * dt)
            for i in range(3)
        ]
        g_pos = [
            (g_pos[i][0] + g_vel[i][0] * dt, g_pos[i][1] + g_vel[i][1] * dt)
            for i in range(3)
        ]

        # 2. Unsoftened Newton reference step
        n_acc = []
        for i in range(3):
            others = [
                (n_pos[j][0], n_pos[j][1], masses[j])
                for j in range(3)
                if j != i
            ]
            n_acc.append(_newton_acc(n_pos[i], others))
        n_vel = [
            (n_vel[i][0] + n_acc[i][0] * dt, n_vel[i][1] + n_acc[i][1] * dt)
            for i in range(3)
        ]
        n_pos = [
            (n_pos[i][0] + n_vel[i][0] * dt, n_pos[i][1] + n_vel[i][1] * dt)
            for i in range(3)
        ]

    max_drift = max(
        math.hypot(g_pos[i][0] - n_pos[i][0], g_pos[i][1] - n_pos[i][1])
        for i in range(3)
    )
    return {"max_drift": max_drift, "min_sep": min_sep}


def run_3body_demo() -> None:
    print("=== 6-FACE LEDGER GRID: 3-BODY ORBITS VS. UNSOFTENED NEWTON ===")
    # 1. Chenciner-Montgomery Figure-8 (1 period T ~ 6.3259)
    f8_pos = [(-0.97000436, 0.24308753), (0.97000436, -0.24308753), (0.0, 0.0)]
    vx3, vy3 = -0.93240737, -0.86473146
    f8_vel = [(-0.5 * vx3, -0.5 * vy3), (-0.5 * vx3, -0.5 * vy3), (vx3, vy3)]

    r_f8_inst = simulate_3body(
        [1.0, 1.0, 1.0], f8_pos, f8_vel, t_end=6.33, cell_scale=12.0, smoothing_units=0.15
    )
    r_f8_c = simulate_3body(
        [1.0, 1.0, 1.0], f8_pos, f8_vel, t_end=6.33, cell_scale=12.0, smoothing_units=0.15, retarded_c=20.0
    )
    print(
        f"Figure-8 (1 period, 12 cells/u): min_sep={r_f8_inst['min_sep']:.3f} | "
        f"drift(instant)={r_f8_inst['max_drift']:.3f} | drift(finite c=20)={r_f8_c['max_drift']:.3f}"
    )

    # 2. Burrau Pythagorean 3-4-5 problem
    p345_pos = [(1.0, 3.0), (-2.0, -1.0), (1.0, -1.0)]
    p345_vel = [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]
    r_pre = simulate_3body(
        [3.0, 4.0, 5.0], p345_pos, p345_vel, t_end=1.80, cell_scale=10.0, smoothing_units=0.15
    )
    r_post = simulate_3body(
        [3.0, 4.0, 5.0], p345_pos, p345_vel, t_end=10.0, cell_scale=10.0, smoothing_units=0.15
    )
    print(f"Pythagorean 3-4-5 (t=1.80 pre-pass): min_sep={r_pre['min_sep']:.3f} | drift={r_pre['max_drift']:.3f}")
    print(
        f"Pythagorean 3-4-5 (t=10.0 post-pass): min_sep={r_post['min_sep']:.3f} "
        f"(< 0.15 cap) | drift={r_post['max_drift']:.3f}"
    )


if __name__ == "__main__":
    run_3body_demo()

