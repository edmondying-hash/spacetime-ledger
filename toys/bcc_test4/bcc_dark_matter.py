#!/usr/bin/env python3
"""
Dark Matter on the 6-Face Planck-Cube Grid: Gravitational Load Without EM Coupling.

Demonstrates three emergent dark-halo effects using EM-neutral closed gluon loops
(Q_EM = 0, BareT = 0, positive routing load W > 0):
  1. Invisible Lensing: 0% EM scattering/absorption, nonzero gravitational wavefront lag.
  2. Flat Galaxy Rotation Curve: Baryons-only Keplerian falloff vs. flat halo plateau.
  3. Bullet-Cluster Offset: Collisional EM baryons stall while Q_EM=0 halos pass through.
"""

import math
from typing import Dict, List


class BCCDarkMatterSim:
    """6-face lattice simulator separating EM link flux (photons) from routing load (gravity)."""

    def __init__(self, core_baryon_load: float = 1200.0, halo_scale_load: float = 420.0, r_core: float = 3.0):
        self.core_baryon_load = core_baryon_load
        self.halo_scale_load = halo_scale_load
        self.r_core = r_core

    def enclosed_loads(self, r: float) -> Dict[str, float]:
        """Return visible baryonic load (Q_EM != 0) and dark loop-halo load (Q_EM = 0) within radius r."""
        # Baryonic disk concentrates near center; dark closed-loop halo grows linearly with r outside r_core
        m_baryon = self.core_baryon_load * (1.0 - math.exp(-r / 1.8))
        m_dark = self.halo_scale_load * (r - self.r_core * math.atan(r / self.r_core))
        return {
            "r": r,
            "baryon_load": m_baryon,
            "dark_load": m_dark,
            "total_load": m_baryon + m_dark,
        }

    def rotation_curve(self, radii: List[float]) -> List[Dict[str, float]]:
        """Compare orbital speed v(r) = sqrt(W_enc / r) for baryons-only vs. baryons + dark halo."""
        rows: List[Dict[str, float]] = []
        for r in radii:
            enc = self.enclosed_loads(r)
            v_baryon = math.sqrt(enc["baryon_load"] / r)
            v_total = math.sqrt(enc["total_load"] / r)
            rows.append({
                "r": r,
                "v_baryon": round(v_baryon, 2),
                "v_total": round(v_total, 2),
                "dark_fraction": round(enc["dark_load"] / enc["total_load"], 3),
            })
        return rows

    def invisible_lensing_probe(self, impact_b: int, dark_loops: int = 12) -> Dict[str, float]:
        """Measure EM photon scattering (0 because Q_EM=0) vs. gravitational wavefront lag."""
        # Each closed 4-link gluon loop carries ~2001 MeV (~395 grid ticks) with Q_EM = 0
        q_em_total = 0.0
        em_scattering = q_em_total * 0.0  # Photons do not couple to Q_EM = 0 loops
        halo_load = dark_loops * 395.0
        grav_lag_px = int(round((halo_load / 400.0) / (1.0 + 0.35 * impact_b * impact_b)))
        return {
            "impact_b": impact_b,
            "q_em": q_em_total,
            "em_attenuation": em_scattering,
            "halo_load": halo_load,
            "grav_lag_px": grav_lag_px,
        }

    def bullet_cluster_collision(self, ticks: int = 10) -> Dict[str, float]:
        """Simulate two clusters colliding: EM baryons shock/drag while Q_EM=0 halos pass through."""
        # Initial positions at x = -8 and x = +8 moving inward at 1.0 l_P / tick
        baryon_x1, baryon_x2 = -8.0, 8.0
        dark_x1, dark_x2 = -8.0, 8.0
        v1, v2 = 1.0, -1.0

        for _ in range(ticks):
            # Dark halos (Q_EM = 0) are collisionless on the 6-face grid
            dark_x1 += v1
            dark_x2 += v2
            # Baryons experience EM link-flux drag when overlapping within 2 l_P
            overlap = abs(baryon_x1 - baryon_x2) < 2.5
            drag = 0.15 if overlap else 1.0
            baryon_x1 += v1 * drag
            baryon_x2 += v2 * drag

        return {
            "baryon_sep": round(abs(baryon_x1 - baryon_x2), 2),
            "dark_halo_sep": round(abs(dark_x1 - dark_x2), 2),
            "lensing_offset": round(abs(dark_x1) - abs(baryon_x1), 2),
        }


def run_dark_matter_demo() -> None:
    sim = BCCDarkMatterSim()
    print("=== PART 1: Invisible Gravitational Lensing (Q_EM = 0 Closed-Loop Halo) ===")
    print("Impact b   Q_EM   EM Attenuation   Halo Load (ticks)   Grav Wavefront Lag")
    print("-" * 73)
    for b in (0, 2, 4, 8):
        res = sim.invisible_lensing_probe(b)
        print(
            f"{res['impact_b']:>8} {res['q_em']:>6.1f} {res['em_attenuation']:>15.1f} "
            f"{res['halo_load']:>19.1f} {res['grav_lag_px']:>17} px"
        )

    print("\n=== PART 2: Galaxy Rotation Curve (Baryons Only vs. Baryons + Dark Halo) ===")
    print("Radius r   v_Baryon (Keplerian)   v_Total (Flat Halo)   Dark Load Fraction")
    print("-" * 74)
    for row in sim.rotation_curve([2.0, 4.0, 8.0, 14.0, 20.0]):
        print(
            f"{row['r']:>8.1f} {row['v_baryon']:>22.2f} {row['v_total']:>21.2f} "
            f"{row['dark_fraction']:>21.3f}"
        )

    print("\n=== PART 3: Bullet-Cluster Collision (EM Baryon Drag vs. Collisionless Halo) ===")
    bc = sim.bullet_cluster_collision(ticks=10)
    print(
        f"Baryon separation: {bc['baryon_sep']} l_P | Dark halo separation: {bc['dark_halo_sep']} l_P | "
        f"Lensing peak offset: {bc['lensing_offset']:+.2f} l_P"
    )


if __name__ == "__main__":
    run_dark_matter_demo()

