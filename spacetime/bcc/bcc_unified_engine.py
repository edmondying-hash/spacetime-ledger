#!/usr/bin/env python3
"""Master 3D BCC (8-Diagonal) Unified Spacetime Network Engine with CLI & Export."""

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
import bcc_config as cfg  # noqa: E402  (HOP switch, constants, DECLARED_KNOBS)


# ---- Fixed-copy label (Nov 19, 2026) ---------------------------------------
# INSERTED, NOT EMERGENT: baryon bare/spin terms and 198 MeV link weight (tuned), glueball
# 165+362.5L, lensing 1/r queue law, horizon escaped=0 (fixed return), Huygens 1/r load.
# GENUINE lattice parts: Steiner BFS link counts, double-slit walk, vacuum Huygens wave.
# DECLARED KNOB: Huygens dt = 0.55 (sets wave speed; see bcc_config.DECLARED_KNOBS).
# ---------------------------------------------------------------------------


import argparse
from collections import deque
import csv
import itertools
import json
import math
import random
from typing import Any, Dict, List, Set, Tuple
import numpy as np

Coord3D = Tuple[int, int, int]
BCC_DIAGONALS_8: Tuple[Coord3D, ...] = tuple(itertools.product((-1, 1), repeat=3))

BARYON_FAMILIES: List[Tuple[str, Tuple[str, str, str], float]] = [
    ("N", ("u", "u", "d"), -1.0),
    ("Delta", ("u", "u", "u"), 1.0),
    ("Lambda", ("u", "d", "s"), -1.0),
    ("Sigma", ("u", "u", "s"), -0.5),
    ("Xi", ("u", "s", "s"), -0.66),
    ("SigmaStar", ("u", "u", "s"), 0.8),
    ("XiStar", ("u", "s", "s"), 0.56),
    ("Omega", ("s", "s", "s"), 0.34),
]


def is_valid_bcc_node(pos: Coord3D) -> bool:
    """In a 3D BCC grid, coordinates are either all-even or all-odd."""
    return (pos[0] % 2) == (pos[1] % 2) == (pos[2] % 2)


def build_periodic_bcc_graph(
    size: int = 8,
) -> Tuple[List[Coord3D], Dict[Coord3D, Dict[Coord3D, int]]]:
    """Build valid 3D BCC sites and exact all-pairs shortest diagonal hop distances."""
    if size % 2 != 0:
        raise ValueError("Periodic BCC grid size must be even.")

    nodes = [
        (x, y, z)
        for x in range(size)
        for y in range(size)
        for z in range(size)
        if is_valid_bcc_node((x, y, z))
    ]

    dist_map: Dict[Coord3D, Dict[Coord3D, int]] = {}
    for src in nodes:
        d_src = {src: 0}
        queue = deque([src])
        while queue:
            cx, cy, cz = queue.popleft()
            cd = d_src[(cx, cy, cz)]
            for dx, dy, dz in BCC_DIAGONALS_8:
                nb = ((cx + dx) % size, (cy + dy) % size, (cz + dz) % size)
                if nb not in d_src:
                    d_src[nb] = cd + 1
                    queue.append(nb)
        dist_map[src] = d_src

    return nodes, dist_map


class BCCUnifiedEngine:
    """Unified 3D BCC 8-link network simulation engine."""

    def __init__(
        self,
        size: int = 8,
        max_node_ticks: float = 100.0,
        link_weight_mev: float = 198.0,
    ):
        self.size = size
        self.max_node_ticks = max_node_ticks
        self.link_weight_mev = link_weight_mev
        self.directions = BCC_DIAGONALS_8
        self.bcc_nodes, self.dist_map = build_periodic_bcc_graph(size)

    def steiner_3q_bcc_links(self, q1: Coord3D, q2: Coord3D, q3: Coord3D) -> int:
        """Exact 3-terminal Steiner tree hop count across the 8-diagonal BCC lattice."""
        d1, d2, d3 = self.dist_map[q1], self.dist_map[q2], self.dist_map[q3]
        return min(d1[j] + d2[j] + d3[j] for j in self.bcc_nodes)

    def simulate_baryon_workload(
        self,
        flavors: Tuple[str, str, str],
        spin_factor: float,
        cycles: int = 3000,
        seed: int = 42,
    ) -> Dict[str, float]:
        """Module 1: Hop 3 quarks across 8 BCC diagonals and measure workload."""
        rng = random.Random(seed)
        pos: List[Coord3D] = [(1, 1, 1), (4, 4, 4), (6, 2, 6)]
        redraw_probs = {"u": 0.72, "d": 0.72, "s": 0.40}

        total_links = 0
        total_redraws = 0
        for _ in range(cycles):
            new_pos: List[Coord3D] = []
            for idx, flv in enumerate(flavors):
                px, py, pz = pos[idx]
                if rng.random() < redraw_probs[flv]:
                    dx, dy, dz = self.directions[rng.randrange(8)]
                    px = (px + dx) % self.size
                    py = (py + dy) % self.size
                    pz = (pz + dz) % self.size
                    total_redraws += 1
                new_pos.append((px, py, pz))
            pos = new_pos
            total_links += self.steiner_3q_bcc_links(pos[0], pos[1], pos[2])

        avg_links = total_links / cycles
        redraw_per_c = total_redraws / (3.0 * cycles)
        n_strange = sum(1 for f in flavors if f == "s")

        # INSERTED/TUNED (declared knobs): bare term, 198 MeV link weight, spin factors.
        bare_t = 12.0 + 91.0 * n_strange
        route_t = avg_links * self.link_weight_mev
        spin_t = spin_factor * (6.5 - 1.4 * n_strange)
        grid_mass = bare_t + route_t + spin_t

        raw_load = 100.0 * (
            (avg_links * 18.5 + redraw_per_c * 16.0) / self.max_node_ticks
        )
        load_pct = min(99.5, max(10.0, raw_load))

        return {
            "AvgLinks": round(avg_links, 2),
            "BareT": round(bare_t, 1),
            "RouteT": round(route_t, 1),
            "SpinT": round(spin_t, 1),
            "Redraw/c": round(redraw_per_c, 2),
            "Load%": round(load_pct, 1),
            "GridMass": round(grid_mass, 1),
        }
    def simulate_bcc_glueball(self, loop_links: int) -> Dict[str, float]:
        """Pure-gluon closed cycle on 3D BCC (minimal non-planar rhombus = 4 links)."""
        if loop_links <= 0:
            return {"loop_links": 0, "glueball_mass_mev": 0.0}
        # INSERTED formula (declared knob), not a lattice computation.
        mass_mev = 165.0 + 362.5 * loop_links
        return {"loop_links": loop_links, "glueball_mass_mev": round(mass_mev, 1)}

    def simulate_coupled_bcc_lensing(
        self,
        source_workload: Dict[str, float],
        num_clusters: int = 12,
        span_steps: int = 24,
    ) -> List[Dict[str, float]]:
        """Module 2: Route 3D BCC wavefront packets past a mass-loaded cluster."""
        cluster_mass_gev = (source_workload["GridMass"] * num_clusters) / 1000.0
        base_load_frac = source_workload["Load%"] / 100.0
        impact_radii = (0, 2, 4, 6, 8, 12, 16)
        results: List[Dict[str, float]] = []

        for b in impact_radii:
            total_queue_delay = 0.0
            for step in range(-span_steps // 2, span_steps // 2):
                r = math.sqrt(step * step + b * b + 1.0)
                # INSERTED 1/r utilisation and queue law (not emergent).
                local_util = min(0.95, (base_load_frac * cluster_mass_gev * 0.24) / r)
                step_delay = (local_util / (1.0 - local_util)) * 0.18
                total_queue_delay += step_delay

            lag_hops = int(round(total_queue_delay))
            effective_c = round(span_steps / (span_steps + total_queue_delay), 3)
            results.append({
                "impact_b": b,
                "x_reached": max(0, span_steps - lag_hops),
                "lag_ticks": lag_hops,
                "eff_c_ratio": effective_c,
            })
        return results

    def simulate_bcc_saturation_horizon(
        self,
        source_workload: Dict[str, float],
        packets: int = 240,
    ) -> Dict[str, float]:
        """Module 3: Saturate a 3D BCC core to 100% ticks and measure 8-link shell."""
        core: Set[Coord3D] = {(x, y, 4) for x in (2, 4, 6) for y in (0, 2, 4, 6)}
        core.add((4, 8, 4))
        initial_core = len(core)

        workload_scale = source_workload["GridMass"] / 938.0
        max_core_nodes = int(round(initial_core + 10 * workload_scale))

        shell: Set[Coord3D] = set()
        for cx, cy, cz in core:
            for dx, dy, dz in self.directions:
                nb = (cx + dx, cy + dy, cz + dz)
                if nb not in core:
                    shell.add(nb)

        rng = random.Random(19)
        for _ in range(packets):
            target = sorted(shell)[rng.randrange(len(shell))]
            if len(core) < max_core_nodes and rng.random() < 0.08:
                core.add(target)
                for dx, dy, dz in self.directions:
                    nb = (target[0] + dx, target[1] + dy, target[2] + dz)
                    if nb not in core:
                        shell.add(nb)

        return {
            "initial_core": initial_core,
            "saturated_core": len(core),
            "bcc_shell_nodes": len(shell),
            "shell_to_core": round(len(shell) / len(core), 2),
            "escaped_packets": 0,  # INSERTED fixed value: escape is not simulated
        }

    def simulate_bcc_double_slit(
        self,
        total_clicks: int = 1000,
        seed: int = 42,
    ) -> Tuple[np.ndarray, Dict[int, int], Dict[int, int]]:
        """Module 4: 3D BCC Feynman checkerboard walk & which-path slit detector."""
        max_x, half_w = 64, 56
        y_vals = np.arange(-half_w, half_w + 1)
        z_vals = np.arange(-half_w, half_w + 1)
        ny, nz = len(y_vals), len(z_vals)
        fwd_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        theta = math.pi / 4.0
        c, s = math.cos(theta), math.sin(theta)
        u_1d = np.array([[c, 1j * s], [1j * s, c]], dtype=np.complex128)
        u_4d = np.kron(u_1d, u_1d)

        slit_x, slit_centers, z_window = 16, (-6, 6), 4
        psi = np.zeros((4, ny, nz), dtype=np.complex128)
        for d in range(4):
            psi[d, half_w, half_w] = 0.5 + 0.0j

        def propagate(state: np.ndarray, start_x: int, end_x: int) -> np.ndarray:
            curr = state.copy()
            for x in range(start_x, end_x):
                nxt = np.zeros_like(curr)
                parity = x % 2
                for iy in range(parity, ny, 2):
                    for iz in range(parity, nz, 2):
                        vec = curr[:, iy, iz]
                        if np.all(vec == 0):
                            continue
                        out_vec = u_4d @ vec
                        for d_out, (dy, dz) in enumerate(fwd_dirs):
                            ny_idx, nz_idx = iy + dy, iz + dz
                            if 0 <= ny_idx < ny and 0 <= nz_idx < nz:
                                nxt[d_out, ny_idx, nz_idx] += out_vec[d_out]
                curr = nxt
            return curr

        psi_slit = propagate(psi, 0, slit_x)

        mask_both = np.zeros((ny, nz))
        for iy, y in enumerate(y_vals):
            if y in slit_centers:
                mask_both[iy, np.abs(z_vals) <= z_window] = 1.0
        prob_coh = np.sum(
            np.abs(propagate(psi_slit * mask_both[None], slit_x, max_x)) ** 2, axis=0
        )

        prob_wp = np.zeros((ny, nz))
        for sc in slit_centers:
            mask_single = np.zeros((ny, nz))
            for iy, y in enumerate(y_vals):
                if y == sc:
                    mask_single[iy, np.abs(z_vals) <= z_window] = 1.0
            prob_wp += np.sum(
                np.abs(propagate(psi_slit * mask_single[None], slit_x, max_x)) ** 2,
                axis=0,
            )

        central_mask = (y_vals >= -18) & (y_vals <= 18) & (y_vals % 2 == 0)
        cy = y_vals[central_mask]
        w_coh = np.sum(prob_coh, axis=1)[central_mask]
        w_wp = np.sum(prob_wp, axis=1)[central_mask]

        rng = np.random.default_rng(seed)
        clicks_coh = rng.choice(cy, size=total_clicks, p=w_coh / np.sum(w_coh))
        clicks_wp = rng.choice(cy, size=total_clicks, p=w_wp / np.sum(w_wp))

        return (
            cy,
            {int(y): int(np.sum(clicks_coh == y)) for y in cy},
            {int(y): int(np.sum(clicks_wp == y)) for y in cy},
        )

    def simulate_bcc_huygens_isotropy(
        self,
        source_workload: Dict[str, float],
        target_radius: int = 60,
    ) -> Dict[str, Any]:
        """Module 5: 3D BCC Huygens spherical wavefront isotropy & 1/r Shapiro delay."""
        half_g = target_radius + 8
        n = 2 * half_g + 1
        coords = np.arange(-half_g, half_g + 1, dtype=np.float64)
        X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
        R = np.sqrt(X * X + Y * Y + Z * Z)

        ix = np.arange(n)[:, None, None]
        iy = np.arange(n)[None, :, None]
        iz = np.arange(n)[None, None, :]
        bcc_mask = ((ix % 2) == (iy % 2)) & ((iy % 2) == (iz % 2))

        def propagate_shell(load_strength: float) -> np.ndarray:
            # INSERTED 1/r congestion for the "mass" run (vacuum run: load 0, clean).
            local_util = np.minimum(0.65, load_strength / np.maximum(R, 2.0))
            c_eff = np.where(bcc_mask, 1.0 / (1.0 + local_util), 0.0)

            u_prev = np.where(bcc_mask & (np.abs(R - 3.0) <= 1.2), 1.0, 0.0)
            u_curr = u_prev.copy()
            arr = np.full((n, n, n), -1.0)
            arr[u_curr > 0.1] = 0.0

            # DECLARED KNOB: dt sets the wave speed. Phase speed of this leapfrog = dt/sqrt(2)
            # coord/tick = 0.389 (0.2245 hop/tick). One hop per tick (sqrt(3) coord/tick) is NOT
            # reachable: the scheme is stable only for dt <= sqrt(2), i.e. <= 1 coord/tick = 0.577 hop/tick.
            dt = cfg.DECLARED_KNOBS["huygens_dt"][0]
            dt2 = dt * dt
            max_ticks = int(target_radius * 4.5)
            for tick in range(1, max_ticks + 1):
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

        arr_vac = propagate_shell(load_strength=0.0)
        load_str = (source_workload["GridMass"] / 938.0) * 6.5
        arr_mass = propagate_shell(load_strength=load_str)

        test_dirs = [
            ("Axis (1,0,0)", (1.0, 0.0, 0.0)),
            ("Face Diag (1,1,0)", (1.0, 1.0, 0.0)),
            ("Body Diag (1,1,1)", (1.0, 1.0, 1.0)),
            ("Off-Axis (2,1,0)", (2.0, 1.0, 0.0)),
            ("Oblique (3,2,1)", (3.0, 2.0, 1.0)),
        ]

        rows = []
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
            t_vac = arr_vac[half_g + tx, half_g + ty, half_g + tz]
            t_mass = arr_mass[half_g + tx, half_g + ty, half_g + tz]
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
        mean_err = sum(r["isotropy_err_pct"] for r in rows) / len(rows)
        return {"rows": rows, "mean_anisotropy_err": round(mean_err, 2)}


def export_csv_report(filepath: str, report: Dict[str, Any]) -> None:
    """Flatten executed module metrics into a clean CSV sweep log."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["module", "entity", "metric", "value"])
        for mod_key, mod_data in report.get("modules", {}).items():
            if isinstance(mod_data, list):
                # FIXED: list-valued modules (module_5_isotropy_sweep) were skipped, so
                # scaling_sweep.csv held only its header.
                for item in mod_data:
                    label = f"R={item.get('radius', '')}"
                    for mk, mv in item.items():
                        if mk == "directions":
                            for d in mv:
                                for dk, dv in d.items():
                                    if dk != "direction":
                                        writer.writerow([mod_key, f"{label} {d['direction']}", dk, dv])
                        else:
                            writer.writerow([mod_key, label, mk, mv])
            if isinstance(mod_data, dict):
                for k, v in mod_data.items():
                    if isinstance(v, list):
                        for item in v:
                            label = (
                                item.get("Family")
                                or item.get("direction")
                                or item.get("impact_b", "")
                            )
                            for mk, mv in item.items():
                                writer.writerow([mod_key, label, mk, mv])
                    elif isinstance(v, dict):
                        for mk, mv in v.items():
                            writer.writerow([mod_key, k, mk, mv])
                    else:
                        writer.writerow([mod_key, "summary", k, v])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="3D BCC (8-Diagonal) Unified Spacetime Network Engine"
    )
    parser.add_argument(
        "--module",
        nargs="+",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=[1, 2, 3, 4, 5],
        help="Select which module(s) to run (1..5). Default: all.",
    )
    parser.add_argument("--cycles", type=int, default=3000, help="Baryon cycles")
    parser.add_argument("--clicks", type=int, default=1000, help="Detector clicks")
    parser.add_argument( "--radius", nargs="+", type=int, default=[60], help="One or more Huygens wavefront radii (e.g., --radius 30 60 90 120)",)
    parser.add_argument("--link-weight", type=float, default=198.0, help="Link MeV")
    parser.add_argument("--json", type=str, default="", help="JSON export path")
    parser.add_argument("--csv", type=str, default="", help="CSV export path")

    return parser.parse_args()
def main() -> None:
    args = parse_args()
    selected = set(args.module)
    engine = BCCUnifiedEngine(size=8, max_node_ticks=100.0, link_weight_mev=args.link_weight)

    report: Dict[str, Any] = {
        "parameters": {
            "cycles": args.cycles,
            "clicks": args.clicks,
            "radius": args.radius,
            "link_weight_mev": args.link_weight,
        },
        "modules": {},
    }

    baryon_results: Dict[str, Dict[str, Any]] = {}
    if selected & {1, 2, 3, 5}:
        for idx, (fam, flv, sp) in enumerate(BARYON_FAMILIES):
            res = engine.simulate_baryon_workload(flv, sp, cycles=args.cycles, seed=42 + idx)
            baryon_results[fam] = {"Family": fam, **res}

    if 1 in selected:
        n_mass = baryon_results["N"]["GridMass"]
        gb4 = engine.simulate_bcc_glueball(4)
        gb_ratio = round(gb4["glueball_mass_mev"] / n_mass, 3)
        report["modules"]["module_1_baryons"] = {
            "families": list(baryon_results.values()),
            "glueball_4link_mev": gb4["glueball_mass_mev"],
            "glueball_to_nucleon_ratio": gb_ratio,
        }
        print("=" * 76)
        print("MODULE 1: 3D BCC (8-Diagonal) Baryon Workload & Mass Spectrum")
        print("=" * 76)
        print("Family      AvgLinks  BareT  RouteT  SpinT  Redraw/c  Load%  GridMass")
        print("-" * 76)
        for res in baryon_results.values():
            print(
                f"{res['Family']:<10} {res['AvgLinks']:>8.2f} {res['BareT']:>6.1f} {res['RouteT']:>7.1f} "
                f"{res['SpinT']:>6.1f} {res['Redraw/c']:>9.2f} {res['Load%']:>5.1f}% {res['GridMass']:>9.1f}"
            )
        print("-" * 76)
        print(f"Glueball(4-link)/N = {gb_ratio:.3f} (LQCD: ~1.70)  [glueball mass is an inserted formula]")

    if 2 in selected or 3 in selected:
        lensing_log: Dict[str, Any] = {}
        horizon_log: Dict[str, Any] = {}
        for label, key in [("Nucleon Cluster (N)", "N"), ("Omega Cluster (Omega)", "Omega")]:
            src = baryon_results[key]
            print("\n" + "=" * 76)
            print(f"MODULES 2 & 3: {label} (Mass={src['GridMass']} MeV, Load={src['Load%']}%)")
            print("=" * 76)
            if 2 in selected:
                rows = engine.simulate_coupled_bcc_lensing(src)
                lensing_log[key] = rows
                for row in rows:
                    print(
                        f"  Impact b={row['impact_b']:>2} | X={row['x_reached']:>2}/24 | "
                        f"Lag={row['lag_ticks']:>2} ticks | c_eff={row['eff_c_ratio']:.3f}c"
                    )
            if 3 in selected:
                hz = engine.simulate_bcc_saturation_horizon(src)
                horizon_log[key] = hz
                print(
                    f"\nSaturation Horizon: Core {hz['initial_core']} -> {hz['saturated_core']} | "
                    f"8-Link Shell = {hz['bcc_shell_nodes']} ({hz['shell_to_core']}x) | "
                    f"Escaped = {hz['escaped_packets']}"
                )
        if 2 in selected:
            report["modules"]["module_2_lensing"] = lensing_log
        if 3 in selected:
            report["modules"]["module_3_horizons"] = horizon_log

    if 4 in selected:
        cy, coh, wp = engine.simulate_bcc_double_slit(total_clicks=args.clicks)
        report["modules"]["module_4_double_slit"] = {
            "clicks": args.clicks,
            "coherent_counts": coh,
            "which_path_counts": wp,
        }
        print("\n" + "=" * 76)
        print(f"MODULE 4: 3D BCC Double-Slit Zigzag Wave ({args.clicks} Clicks)")
        print("=" * 76)
        print("Pos y | Coherent (No Sensor)     | Which-Path (Sensor at y=-6)")
        print("-" * 76)
        scale = max(1, args.clicks // 250)
        for y in cy:
            iy = int(y)
            print(
                f"y={iy:>3} | {coh[iy]:>4} {'*' * (coh[iy] // scale):<19} | "
                f"{wp[iy]:>4} {'*' * (wp[iy] // scale)}"
            )

    if 5 in selected:
        sweep_summary = []
        for rad in args.radius:
            iso = engine.simulate_bcc_huygens_isotropy(baryon_results["N"], target_radius=rad)
            mean_lag = round(sum(r["shapiro_lag"] for r in iso["rows"]) / len(iso["rows"]), 2)
            mean_spd = round(sum(r["eff_speed"] for r in iso["rows"]) / len(iso["rows"]), 4)
            sweep_summary.append({
                "radius": rad,
                "mean_speed": mean_spd,
                "mean_shapiro_lag": mean_lag,
                "mean_isotropy_err_pct": iso["mean_anisotropy_err"],
                "directions": iso["rows"],
            })

            print("\n" + "=" * 76)
            print(f"MODULE 5: 3D BCC Huygens Spherical Isotropy & Shapiro Delay (R={rad})")
            print("=" * 76)
            print("Direction          | Radius | Vac Tick | Mass Tick | 1/r Lag | Speed  | Err")
            print("-" * 76)
            for r in iso["rows"]:
                print(
                    f"{r['direction']:<18} | {r['r_actual']:>6.2f} | {r['vac_tick']:>8.1f} | "
                    f"{r['mass_tick']:>9.1f} | {r['shapiro_lag']:>7.1f} | {r['eff_speed']:>6.4f} | "
                    f"{r['isotropy_err_pct']:>5.2f}%"
                )
            print("-" * 76)
            print(f"Mean 3D Spherical Isotropy Error at R={rad}: {iso['mean_anisotropy_err']:.2f}%")
            dt_k = cfg.DECLARED_KNOBS["huygens_dt"][0]
            print(f"Analytic vacuum phase speed dt/sqrt(2) = {dt_k/math.sqrt(2):.4f} coord/tick = "
                  f"{dt_k/math.sqrt(6):.4f} hop/tick (dt = {dt_k} is a declared knob; 'Speed' column is mass run)")

        if len(sweep_summary) > 1:
            print("\n" + "=" * 76)
            print("RADIAL SCALING SWEEP SUMMARY (Continuum Limit Convergence)")
            print("=" * 76)
            print("Target R | Mean Speed | Mean 1/r Lag | Mean Spherical Error")
            print("-" * 76)
            for s in sweep_summary:
                print(
                    f"R = {s['radius']:>4} | {s['mean_speed']:>10.4f} | "
                    f"{s['mean_shapiro_lag']:>12.2f} | {s['mean_isotropy_err_pct']:>19.2f}%"
                )

        report["modules"]["module_5_isotropy_sweep"] = sweep_summary


    if args.json:
        with open(args.json, "w", encoding="utf-8") as jf:
            json.dump(report, jf, indent=2)
        print(f"\n[Exported JSON report -> {args.json}]")

    if args.csv:
        export_csv_report(args.csv, report)
        print(f"[Exported CSV sweep log -> {args.csv}]")


if __name__ == "__main__":
    main()
