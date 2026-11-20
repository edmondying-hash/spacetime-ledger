#!/usr/bin/env python3
"""Serverside Module 2: 8x Accelerated Octant-Symmetry 3D BCC Huygens Wavefront Engine."""

# ---- Fixed-copy label (Nov 19, 2026) ---------------------------------------
# Same physics as engine Module 5: genuine 8-neighbour BCC wave; INSERTED 1/r load for the 'mass' run.
# DECLARED KNOB: dt (wave speed dt/sqrt(2) coord/tick).
# ---------------------------------------------------------------------------


import argparse
import math
import time
from typing import Any, Dict, List
import numpy as np


def simulate_octant_bcc_wavefront(
    target_radius: int = 180,
    nucleon_mass_mev: float = 927.3,
) -> Dict[str, Any]:
    """Simulate 3D BCC Huygens spherical propagation using 8-fold octant symmetry."""
    t_start = time.perf_counter()
    # Pad by 2 cells on inner symmetry boundaries (x=0, y=0, z=0) and 6 on outer edge
    pad = 2
    max_coord = target_radius + 6
    n = max_coord + pad + 1

    coords = np.arange(-pad, max_coord + 1, dtype=np.float64)
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
    R = np.sqrt(X * X + Y * Y + Z * Z)

    ix = np.arange(-pad, max_coord + 1)[:, None, None]
    iy = np.arange(-pad, max_coord + 1)[None, :, None]
    iz = np.arange(-pad, max_coord + 1)[None, None, :]
    bcc_mask = ((ix % 2) == (iy % 2)) & ((iy % 2) == (iz % 2))

    def apply_octant_reflection(arr: np.ndarray) -> None:
        """Mirror across x=0, y=0, z=0 symmetry planes (index pad = 2)."""
        # index 2 is coord 0; index 1 is coord -1 (mirrors index 3 = coord +1)
        # index 0 is coord -2 (mirrors index 4 = coord +2)
        arr[0, :, :] = arr[4, :, :]
        arr[1, :, :] = arr[3, :, :]
        arr[:, 0, :] = arr[:, 4, :]
        arr[:, 1, :] = arr[:, 3, :]
        arr[:, :, 0] = arr[:, :, 4]
        arr[:, :, 1] = arr[:, :, 3]

    def propagate_octant(load_strength: float) -> np.ndarray:
        local_util = np.minimum(0.65, load_strength / np.maximum(R, 2.0))
        c_eff = np.where(bcc_mask, 1.0 / (1.0 + local_util), 0.0)

        u_prev = np.where(bcc_mask & (np.abs(R - 3.0) <= 1.2), 1.0, 0.0)
        u_curr = u_prev.copy()
        arr = np.full((n, n, n), -1.0)
        arr[u_curr > 0.1] = 0.0

        dt = 0.55  # DECLARED KNOB (bcc_config "huygens_dt"): phase speed dt/sqrt(2) = 0.389 coord/tick = 0.2245 hop/tick
        dt2 = dt * dt
        max_ticks = int(target_radius * 3.8)
        for tick in range(1, max_ticks + 1):
            apply_octant_reflection(u_curr)
            nb_sum = (
                u_curr[:-2, :-2, :-2] + u_curr[:-2, :-2, 2:]
                + u_curr[:-2, 2:, :-2] + u_curr[:-2, 2:, 2:]
                + u_curr[2:, :-2, :-2] + u_curr[2:, :-2, 2:]
                + u_curr[2:, 2:, :-2] + u_curr[2:, 2:, 2:]
            )
            lap = (nb_sum / 8.0) - u_curr[1:-1, 1:-1, 1:-1]
            u_next = np.zeros_like(u_curr)
            u_next[1:-1, 1:-1, 1:-1] = (
                2.0 * u_curr[1:-1, 1:-1, 1:-1]
                - u_prev[1:-1, 1:-1, 1:-1]
                + dt2 * (c_eff[1:-1, 1:-1, 1:-1] ** 2) * lap
            )
            u_next *= bcc_mask

            newly = (arr < 0) & ((np.abs(u_next) * np.maximum(R, 1.0)) > 0.15)
            arr[newly] = float(tick)
            u_prev, u_curr = u_curr, u_next
        return arr

    arr_vac = propagate_octant(load_strength=0.0)
    load_str = (nucleon_mass_mev / 938.0) * 6.5
    arr_mass = propagate_octant(load_strength=load_str)

    test_dirs = [
        ("Axis (1,0,0)", (1.0, 0.0, 0.0)),
        ("Face Diag (1,1,0)", (1.0, 1.0, 0.0)),
        ("Body Diag (1,1,1)", (1.0, 1.0, 1.0)),
        ("Off-Axis (2,1,0)", (2.0, 1.0, 0.0)),
        ("Oblique (3,2,1)", (3.0, 2.0, 1.0)),
    ]

    rows: List[Dict[str, Any]] = []
    for label, vec in test_dirs:
        norm = math.sqrt(sum(v * v for v in vec))
        ux, uy, uz = (v / norm for v in vec)
        tx = int(round(ux * target_radius))
        ty = int(round(uy * target_radius))
        tz = int(round(uz * target_radius))
        tx -= tx % 2
        ty -= ty % 2
        tz -= tz % 2

        r_actual = math.sqrt(tx * tx + ty * ty + tz * tz)
        t_vac = arr_vac[pad + tx, pad + ty, pad + tz]
        t_mass = arr_mass[pad + tx, pad + ty, pad + tz]
        shapiro_lag = max(0.0, t_mass - t_vac)
        eff_speed = r_actual / max(t_mass, 1e-6)

        rows.append({
            "direction": label,
            "r_actual": round(r_actual, 2),
            "vac_tick": round(t_vac, 1),
            "mass_tick": round(t_mass, 1),
            "shapiro_lag": round(shapiro_lag, 1),
            "eff_speed": round(eff_speed, 4),
        })

    mean_speed = sum(r["eff_speed"] for r in rows) / len(rows)
    for r in rows:
        err_pct = abs(r["eff_speed"] - mean_speed) / mean_speed * 100.0
        r["isotropy_err_pct"] = round(err_pct, 2)

    elapsed = round(time.perf_counter() - t_start, 2)
    mean_err = round(sum(r["isotropy_err_pct"] for r in rows) / len(rows), 3)
    mean_lag = round(sum(r["shapiro_lag"] for r in rows) / len(rows), 2)
    return {
        "radius": target_radius,
        "elapsed_sec": elapsed,
        "mean_speed": round(mean_speed, 4),
        "mean_shapiro_lag": mean_lag,
        "mean_isotropy_err": mean_err,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="8x Accelerated Octant-Symmetry 3D BCC Wavefront Sweep")
    parser.add_argument(
        "--radius",
        nargs="+",
        type=int,
        default=[60, 120, 180, 240],
        help="Target radii to sweep (default: 60 120 180 240)",
    )
    args = parser.parse_args()

    summary = []
    for rad in args.radius:
        res = simulate_octant_bcc_wavefront(target_radius=rad)
        summary.append(res)
        print("=" * 76)
        print(f"OCTANT-SYMMETRY BCC HUYGENS WAVEFRONT (R={rad}, Runtime={res['elapsed_sec']}s)")
        print("=" * 76)
        print("Direction          | Radius | Vac Tick | Mass Tick | 1/r Lag | Speed  | Err")
        print("-" * 76)
        for r in res["rows"]:
            print(
                f"{r['direction']:<18} | {r['r_actual']:>6.2f} | {r['vac_tick']:>8.1f} | "
                f"{r['mass_tick']:>9.1f} | {r['shapiro_lag']:>7.1f} | {r['eff_speed']:>6.4f} | "
                f"{r['isotropy_err_pct']:>5.2f}%"
            )
        print("-" * 76)
        print(f"Mean Spherical Isotropy Error at R={rad}: {res['mean_isotropy_err']:.3f}%\n")

    if len(summary) > 1:
        print("=" * 76)
        print("ULTRA-LARGE RADIUS CONTINUUM CONVERGENCE SUMMARY (8x Octant Speedup)")
        print("=" * 76)
        print("Target R | Runtime | Mean Speed | Mean 1/r Lag | Mean Spherical Error")
        print("-" * 76)
        for s in summary:
            print(
                f"R = {s['radius']:>4} | {s['elapsed_sec']:>6.2f}s | {s['mean_speed']:>10.4f} | "
                f"{s['mean_shapiro_lag']:>12.2f} | {s['mean_isotropy_err']:>19.3f}%"
            )


if __name__ == "__main__":
    main()
