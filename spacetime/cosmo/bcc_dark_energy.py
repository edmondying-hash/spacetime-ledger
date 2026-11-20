#!/usr/bin/env python3
"""
Congestion-Gated Dark Energy & Void Expansion on the 3D BCC (8-Diagonal) Lattice.

Models idle-node truncated-octahedron (~0.770 V_P) vacuum cell insertion:
  1. Bound vs. Void Gating: Dark energy acts on every BCC node, but expansion ticks
     only fire when local routing load W < W_thresh (idle vacuum). Bound galaxies
     (high W) stay fixed in size while intergalactic BCC voids (W ~ 0) expand.
  2. Matter-to-Vacuum Transition: As expansion dilutes matter density (rho_m ~ a^-3),
     idle BCC vacuum cells come to dominate 3D volume (Omega_Lambda = 0.685 vs
     Omega_m = 0.315), flipping the cosmic deceleration parameter q(z) from
     positive (slowing down) to negative (late-time acceleration) near z ~ 0.63.
"""

from typing import Any, Dict, List


class BCCDarkEnergySim:
    """Simulates congestion-gated vacuum cell insertion on the 3D BCC lattice."""

    def __init__(
        self,
        node_cap: float = 100.0,
        expand_thresh: float = 20.0,
        h_vac_rate: float = 0.01,
        omega_m0: float = 0.315,
        omega_l0: float = 0.685,
    ):
        self.node_cap = node_cap
        self.expand_thresh = expand_thresh
        self.h_vac_rate = h_vac_rate
        self.omega_m0 = omega_m0
        self.omega_l0 = omega_l0

    def node_idle_gate(self, workload: float) -> float:
        """
        Fraction of dark-energy expansion rate active on a BCC node with routing load W.
        Returns 1.0 in empty vacuum (W = 0) and 0.0 inside bound objects (W >= W_thresh).
        """
        if workload >= self.expand_thresh:
            return 0.0
        return max(0.0, 1.0 - (workload / self.expand_thresh))

    def evolve_galaxy_void_ruler(
        self,
        galaxy_width_lp: float = 10.0,
        void_width_lp: float = 20.0,
        galaxy_load: float = 85.0,
        void_load: float = 0.0,
        steps: int = 50,
    ) -> Dict[str, Any]:
        """
        Evolve two bound galaxies separated by an intergalactic BCC void over `steps` ticks.
        Bound galaxies have W >= W_thresh (gate = 0 -> zero internal expansion), while
        idle BCC void cells have W = 0 (gate = 1 -> exponential vacuum node insertion).
        """
        g_gate = self.node_idle_gate(galaxy_load)
        v_gate = self.node_idle_gate(void_load)

        g1 = galaxy_width_lp
        void = void_width_lp
        g2 = galaxy_width_lp

        for _ in range(steps):
            g1 *= 1.0 + self.h_vac_rate * g_gate
            void *= 1.0 + self.h_vac_rate * v_gate
            g2 *= 1.0 + self.h_vac_rate * g_gate

        return {
            "steps": steps,
            "galaxy_gate": round(g_gate, 4),
            "void_gate": round(v_gate, 4),
            "galaxy_initial_lp": round(galaxy_width_lp, 2),
            "galaxy_final_lp": round(g1, 2),
            "void_initial_lp": round(void_width_lp, 2),
            "void_final_lp": round(void, 2),
            "total_initial_lp": round(2.0 * galaxy_width_lp + void_width_lp, 2),
            "total_final_lp": round(g1 + void + g2, 2),
        }
    def cosmic_acceleration_history(self, redshifts: List[float]) -> List[Dict[str, Any]]:
        """
        Track busy matter fraction Omega_m(z), idle BCC vacuum fraction Omega_Lambda(z),
        and deceleration parameter q(z) = 0.5 * Omega_m(z) - Omega_Lambda(z).
        """
        rows: List[Dict[str, Any]] = []
        for z in redshifts:
            opz3 = (1.0 + z) ** 3
            e2 = self.omega_m0 * opz3 + self.omega_l0
            om_z = (self.omega_m0 * opz3) / e2
            ol_z = self.omega_l0 / e2
            q_z = 0.5 * om_z - ol_z
            regime = (
                "Accelerating (Vacuum-Dominated)"
                if q_z < -0.02
                else ("Decelerating (Matter-Dominated)" if q_z > 0.02 else "Inflection (q ~ 0)")
            )
            rows.append({
                "z": z,
                "scale_a": round(1.0 / (1.0 + z), 4),
                "omega_m_z": round(om_z, 4),
                "omega_l_z": round(ol_z, 4),
                "decel_q": round(q_z, 4),
                "regime": regime,
            })
        return rows

    def transition_redshift(self) -> float:
        """Exact redshift z_acc where q(z) = 0 (Omega_Lambda(z) = 0.5 * Omega_m(z))."""
        return ((2.0 * self.omega_l0) / self.omega_m0) ** (1.0 / 3.0) - 1.0


def run_dark_energy_demo() -> None:
    sim = BCCDarkEnergySim()
    ruler = sim.evolve_galaxy_void_ruler(
        galaxy_width_lp=10.0, void_width_lp=20.0, galaxy_load=85.0, void_load=0.0, steps=50
    )

    print("=== PART 1: Congestion-Gated BCC Expansion (Bound Galaxies vs. Cosmic Void) ===")
    print(
        f"After {ruler['steps']} cosmic ticks (h_vac = {sim.h_vac_rate}):\n"
        f"  Bound Galaxy (W=85, gate={ruler['galaxy_gate']:.2f}): "
        f"{ruler['galaxy_initial_lp']:.2f} BCC -> {ruler['galaxy_final_lp']:.2f} BCC (unchanged)\n"
        f"  Cosmic Void  (W=0,  gate={ruler['void_gate']:.2f}): "
        f"{ruler['void_initial_lp']:.2f} BCC -> {ruler['void_final_lp']:.2f} BCC (+64.5% expansion)\n"
        f"  Total Ruler  (G1 + Void + G2):     "
        f"{ruler['total_initial_lp']:.2f} BCC -> {ruler['total_final_lp']:.2f} BCC"
    )

    z_acc = sim.transition_redshift()
    print(f"\n=== PART 2: Cosmic Deceleration-to-Acceleration Flip (z_acc = {z_acc:.3f}) ===")
    print("Redshift z   Scale a(t)   Busy Matter Om(z)   Idle Vacuum OL(z)   Decel q(z)   Cosmic Expansion Regime")
    print("-" * 102)
    for r in sim.cosmic_acceleration_history([3.0, 1.5, round(z_acc, 3), 0.3, 0.0]):
        print(
            f"{r['z']:>10.3f} {r['scale_a']:>12.4f} {r['omega_m_z']:>19.4f} "
            f"{r['omega_l_z']:>19.4f} {r['decel_q']:>12.4f}   {r['regime']}"
        )


if __name__ == "__main__":
    run_dark_energy_demo()
