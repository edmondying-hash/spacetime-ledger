#!/usr/bin/env python3
"""
First-Order BCC Congestion Phase Transition & Sakharov Out-of-Equilibrium Freeze-Out.

Couples `bcc_dark_energy.py` (congestion-gated vacuum cell insertion W < 20) with
`bcc_baryogenesis.py` (3-generation CKM CP-violating cascade) to test whether a
sudden congestion-unlock transition supplies Sakharov's third condition:
  1. Congestion-Locked Equilibrium (W > 20): Idle-node expansion gate = 0; thermal
     interaction rate Gamma_int >> H_grid, washing out baryon asymmetry (kappa -> 0).
  2. First-Order Bubble Wall at W = 20: Crossing the W = 20 node workload threshold
     unlocks rapid truncated-octahedron vacuum insertion, spiking H_grid above Gamma_int.
  3. Sakharov Freeze-Out (Gamma_int < H_grid): Inverse decays decouple across the
     expanding bubble wall, locking in surviving baryon-to-photon ratio eta ~ 6.1e-10.
"""

import math
from typing import Any, Dict, List

from bcc_baryogenesis import ETA_TARGET, PDG2024_J, required_epsilon
from bcc_dark_energy import BCCDarkEnergySim


class BCCPhaseTransitionSim:
    """Simulates congestion-gated bubble nucleation and Sakharov baryon freeze-out."""

    def __init__(
        self,
        node_cap: float = 100.0,
        expand_thresh: float = 20.0,
        h_vac_burst: float = 0.25,
    ):
        self.node_cap = node_cap
        self.expand_thresh = expand_thresh
        self.h_vac_burst = h_vac_burst
        self.de_sim = BCCDarkEnergySim(
            node_cap=node_cap,
            expand_thresh=expand_thresh,
            h_vac_rate=h_vac_burst,
        )

    def simulate_cooling_transition(
        self, workloads: List[float], eps_lattice: float = 3.20e-5
    ) -> List[Dict[str, Any]]:
        """
        Sweep early-universe BCC node workload W from 80.0 (congested plasma) down to
        2.0 (unlocked vacuum bubbles), tracking idle gate, expansion rate H_grid,
        inverse-decay rate Gamma_int, washout survival kappa, and frozen-out eta.
        """
        rows: List[Dict[str, Any]] = []
        j_ckm = PDG2024_J

        for w in workloads:
            gate = self.de_sim.node_idle_gate(w)
            # Baseline Hubble drift + first-order latent heat burst when idle gate unlocks (W < 20)
            h_base = 0.02 * (w / self.node_cap)
            latent_burst = self.h_vac_burst * (gate ** 1.5)
            h_grid = h_base + latent_burst

            # Thermal inverse-decay washout rate scales quadratically with local node congestion
            gamma_int = 0.45 * ((w / self.node_cap) ** 2)
            out_of_eq_ratio = h_grid / max(1e-9, gamma_int)

            # Sakharov freeze-out survival factor kappa = exp(-Gamma_int / H_grid)
            kappa_survival = math.exp(-gamma_int / max(1e-9, h_grid))

            # Net surviving baryon-to-photon ratio eta = (2/3) * eps * J * kappa
            b_val = eps_lattice * j_ckm
            eta_raw = (2.0 * b_val) / (3.0 - 2.0 * b_val + 0.5 * (b_val ** 2))
            eta_frozen = eta_raw * kappa_survival

            if w > self.expand_thresh:
                phase = "Locked Plasma (Equilibrium washout)"
            elif out_of_eq_ratio < 1.0:
                phase = "Bubble Nucleation (Threshold crossing)"
            else:
                phase = "FROZEN OUT (Sakharov departure)"

            rows.append({
                "workload_w": w,
                "idle_gate": round(gate, 4),
                "h_grid": round(h_grid, 5),
                "gamma_int": round(gamma_int, 5),
                "h_over_gamma": round(out_of_eq_ratio, 3),
                "kappa_survival": round(kappa_survival, 4),
                "eta_baryon": eta_frozen,
                "phase": phase,
            })
        return rows

    def bubble_wall_profile(self, wall_positions: List[float], w_inside: float = 4.0, w_outside: float = 36.0) -> List[Dict[str, Any]]:
        """
        Trace a spatial cross-section across a first-order BCC phase boundary (x = -4 to +4),
        showing the sharp jump in vacuum expansion speed across the bubble wall at x = 0.
        """
        rows: List[Dict[str, Any]] = []
        for x in wall_positions:
            # Sharp tanh bubble wall profile of thickness ~ 1.0 BCC diagonal hop
            blend = 0.5 * (1.0 + math.tanh(x / 0.8))
            w_local = w_inside + (w_outside - w_inside) * blend
            gate = self.de_sim.node_idle_gate(w_local)
            v_expand = self.h_vac_burst * gate
            region = (
                "True Vacuum Bubble (Unlocked)"
                if gate > 0.5
                else ("BUBBLE WALL (CP-bias sweep)" if gate > 0.0 else "False Vacuum Plasma (Locked)")
            )
            rows.append({
                "x_bcc": x,
                "w_local": round(w_local, 2),
                "idle_gate": round(gate, 4),
                "v_expand": round(v_expand, 5),
                "region": region,
            })
        return rows


def run_phase_transition_demo() -> None:
    sim = BCCPhaseTransitionSim(node_cap=100.0, expand_thresh=20.0, h_vac_burst=0.25)
    eps_req = required_epsilon(ETA_TARGET, PDG2024_J)

    print("=" * 94)
    print("PART 1: First-Order BCC Congestion Phase Transition (Sakharov Out-of-Equilibrium Check)")
    print(f"Target eta = {ETA_TARGET:.2e} | CKM J = {PDG2024_J:.4e} | Lattice eps = 3.20e-5 (min req: {eps_req:.2e})")
    print("=" * 94)
    print("Load W   IdleGate   H_grid   Gamma_int   H/Gamma   Washout kappa   Frozen eta   Cosmic Phase")
    print("-" * 94)
    workloads = [80.0, 50.0, 30.0, 21.0, 18.0, 14.0, 10.0, 5.0]
    for r in sim.simulate_cooling_transition(workloads, eps_lattice=3.20e-5):
        print(
            f"{r['workload_w']:>6.1f} {r['idle_gate']:>10.4f} {r['h_grid']:>8.5f} "
            f"{r['gamma_int']:>11.5f} {r['h_over_gamma']:>9.3f} {r['kappa_survival']:>15.4f} "
            f"{r['eta_baryon']:>12.3e}   {r['phase']}"
        )

    print("\n" + "=" * 94)
    print("PART 2: Spatial Bubble Wall Profile Across W = 20 Threshold (x = -3 to +3 BCC Hops)")
    print("=" * 94)
    print("Pos x (BCC)   Local Load W   Idle Gate   Expansion Rate   Bubble Wall Zone")
    print("-" * 94)
    for b in sim.bubble_wall_profile([-3.0, -1.5, -0.5, 0.0, 0.5, 1.5, 3.0]):
        print(
            f"{b['x_bcc']:>11.1f} {b['w_local']:>14.2f} {b['idle_gate']:>11.4f} "
            f"{b['v_expand']:>16.5f}   {b['region']}"
        )


if __name__ == "__main__":
    run_phase_transition_demo()
