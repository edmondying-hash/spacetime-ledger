#!/usr/bin/env python3
"""
Inverse Dark-Matter Halo Solver on the 3D 6-Face Planck-Cube Grid.

Reconstructs the EM-neutral (Q_EM = 0) topological loop halo from observed galaxy
rotation curves (v_total vs. v_baryon):
  1. Enclosed Halo Mass & Loop Count: Inverts M_halo(<r) = r * (v_tot^2 - v_bar^2) / G_grid
     and counts discrete neutral closed loops (m_loop = 2001.19 MeV from Module #2).
  2. Cusp-to-Core Saturation: Enforces the 100-tick/cycle Planck-cube throughput cap
     so central density saturates at a finite core rho_0 instead of diverging as 1/r.
  3. Cosmic Dark-to-Baryon Ratio: Recovers M_halo / M_baryon ~ 5.4 : 1 (~84.4% dark)
     at the outer galactic halo boundary.
"""

import math
from typing import Any, Dict, List
from bcc_dark_matter import BCCDarkMatterSim


class BCCHaloSolver:
    """Inverts rotation curves into cored Q_EM = 0 topological loop halo profiles."""

    def __init__(
        self,
        g_grid: float = 1.0,
        node_cap: float = 100.0,
        loop_mass_mev: float = 2001.19,
        tick_to_mev: float = 5.0,
    ):
        self.g_grid = g_grid
        self.node_cap = node_cap
        self.loop_mass_mev = loop_mass_mev
        self.loop_ticks = loop_mass_mev / tick_to_mev

    def invert_rotation_curve(self, curve_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Invert v_total(r) and v_baryon(r) into enclosed halo mass M_halo(<r),
        shell density rho_halo(r), discrete Q_EM=0 loop counts, and dark fraction.
        """
        results: List[Dict[str, Any]] = []
        prev_r = 0.0
        prev_m_halo = 0.0

        for row in curve_rows:
            r = float(row["r"])
            v_bar = float(row["v_baryon"])
            v_tot = float(row["v_total"])

            m_bar = (r * (v_bar ** 2)) / self.g_grid
            m_tot = (r * (v_tot ** 2)) / self.g_grid
            m_halo = max(0.0, m_tot - m_bar)

            dr = max(1e-6, r - prev_r)
            dm_halo = max(0.0, m_halo - prev_m_halo)
            shell_vol = 4.0 * math.pi * (r ** 2) * dr
            rho_halo = dm_halo / shell_vol

            dark_frac = m_halo / m_tot if m_tot > 0.0 else 0.0
            ratio_db = m_halo / m_bar if m_bar > 0.0 else 0.0
            # Convert grid mass units (scaled by 1000 ticks/unit) to discrete closed loops
            est_loops = (m_halo * 1000.0) / self.loop_ticks

            results.append({
                "r": r,
                "m_baryon": round(m_bar, 2),
                "m_halo": round(m_halo, 2),
                "rho_halo": round(rho_halo, 5),
                "est_loops": round(est_loops, 1),
                "dark_fraction": round(dark_frac, 4),
                "dark_to_baryon": round(ratio_db, 2),
            })
            prev_r = r
            prev_m_halo = m_halo

        return results

    def cored_vs_cusp_profile(
        self, radii: List[float], rho_0: float = 85.0, core_radius: float = 2.5
    ) -> List[Dict[str, Any]]:
        """
        Compare divergent NFW cusp rho_cusp(r) ~ 1/r against the lattice's
        pseudo-isothermal cored halo capped by the 100-tick/cycle node limit.
        """
        rows: List[Dict[str, Any]] = []
        for r in radii:
            nfw_cusp = (rho_0 * core_radius) / max(0.1, r)
            raw_core = rho_0 / (1.0 + (r / core_radius) ** 2)
            grid_capped = min(self.node_cap, raw_core)
            rows.append({
                "r": r,
                "nfw_cusp_ticks": round(nfw_cusp, 2),
                "grid_core_ticks": round(grid_capped, 2),
                "capped": grid_capped >= self.node_cap or nfw_cusp > self.node_cap,
                "status": "Cored & Bounded (< 100 cap)" if grid_capped < self.node_cap else "Saturated at 100 Cap",
            })
        return rows


def run_halo_solver_demo() -> None:
    dm_sim = BCCDarkMatterSim()
    solver = BCCHaloSolver(g_grid=1.0, node_cap=100.0, loop_mass_mev=2001.19)
    radii = [2.0, 4.0, 8.0, 14.0, 20.0]
    curve = dm_sim.rotation_curve(radii)

    print("=== PART 1: Inverse Halo Reconstruction from Galaxy Rotation Curve ===")
    print("Radius r   M_Baryon   M_Halo(<r)   rho_Halo(r)   Q_EM=0 Loops   Dark Frac   Dark:Baryon")
    print("-" * 88)
    inv_rows = solver.invert_rotation_curve(curve)
    for r in inv_rows:
        print(
            f"{r['r']:>8.1f} {r['m_baryon']:>10.2f} {r['m_halo']:>12.2f} "
            f"{r['rho_halo']:>13.5f} {r['est_loops']:>14.1f} {r['dark_fraction']:>11.4f} "
            f"{r['dark_to_baryon']:>10.2f} : 1"
        )

    print("\n=== PART 2: Cusp-vs.-Core Central Density (100-Tick/Cycle Node Throughput Cap) ===")
    print("Radius r   NFW Cusp (1/r)   Grid Core Density   Lattice Core Status")
    print("-" * 74)
    for c in solver.cored_vs_cusp_profile([0.2, 0.5, 1.0, 2.5, 5.0, 10.0]):
        print(
            f"{c['r']:>8.1f} {c['nfw_cusp_ticks']:>16.2f} {c['grid_core_ticks']:>19.2f}   {c['status']}"
        )


if __name__ == "__main__":
    run_halo_solver_demo()
