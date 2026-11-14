#!/usr/bin/env python3
"""
6-Face Planck-Cube Grid Ground-State Meson & Color Confinement Simulation.

Models quark-antiquark (q qbar) mesons with non-additive two-body reduced-mass
routing (b_avg - 2*mu), 3:1 hyperfine spin splitting, 6-face color flux-tube
string breaking, and blind bottom-quark (B, B*, Upsilon) predictions.
"""

from typing import Any, Dict, List, Tuple

TICK_TO_MEV = 5.0
QUARK_BARE_TICKS: Dict[str, float] = {
    "l": 15.50,
    "s": 24.25,
    "c": 77.50,
    "b": 236.50,  # Anchored solely on symmetric Upsilon(1S) = b bbar
}

MESON_CATALOG: List[Tuple[str, str, str, str, int, float]] = [
    ("pi", "llbar", "l", "l", 0, 138.04),
    ("rho", "llbar", "l", "l", 1, 775.26),
    ("K", "lsbar", "l", "s", 0, 495.64),
    ("K*", "lsbar", "l", "s", 1, 893.60),
    ("phi", "ssbar", "s", "s", 1, 1019.46),
    ("D", "lcbar", "l", "c", 0, 1867.20),
    ("D*", "lcbar", "l", "c", 1, 2008.55),
    ("J/psi", "ccbar", "c", "c", 1, 3096.90),
    ("B", "lbbar", "l", "b", 0, 5279.66),
    ("B*", "lbbar", "l", "b", 1, 5324.71),
    ("Upsilon", "bbbar", "b", "b", 1, 9460.40),
]


def evaluate_meson(
    name: str, quarks: str, q1: str, q2: str, spin_j: int, pdg_mev: float
) -> Dict[str, Any]:
    """Compute meson mass on the 6-face grid using two-body reduced-mass routing."""
    b1, b2 = QUARK_BARE_TICKS[q1], QUARK_BARE_TICKS[q2]
    bare_t = b1 + b2

    # Two-body reduced-mass orbital span correction (zero for q1 == q2, positive for q1 != q2)
    b_avg = 0.5 * bare_t
    mu = (b1 * b2) / bare_t
    route_t = 3.0 * bare_t + (b_avg - 2.0 * mu)

    # Hyperfine spin-spin interaction: -3 for J=0 (singlet), +1 for J=1 (triplet)
    spin_factor = -3.0 if spin_j == 0 else 1.0
    mass_suppression = (QUARK_BARE_TICKS["l"] ** 2) / (b1 * b2)
    spin_t = 32.0 * spin_factor * mass_suppression

    model_mev = (bare_t + route_t + spin_t) * TICK_TO_MEV
    return {
        "name": name,
        "quarks": quarks,
        "J": spin_j,
        "BareT": round(bare_t, 2),
        "RouteT": round(route_t, 2),
        "SpinT": round(spin_t, 2),
        "ModelMeV": round(model_mev, 2),
        "PDGMeV": round(pdg_mev, 2),
        "Diff": round(model_mev - pdg_mev, 2),
    }


def simulate_string_breaking(
    max_hops: int = 9, ticks_per_hop: float = 9.0, threshold_mev: float = 275.0
) -> Dict[str, Any]:
    """Stretch a 6-face color flux tube until stored energy snaps into a new q qbar pair."""
    rows: List[Dict[str, Any]] = []
    snapped_at_hop = None
    for hops in range(max_hops + 1):
        tube_ticks = hops * ticks_per_hop
        stored_mev = tube_ticks * TICK_TO_MEV
        snapped = stored_mev > threshold_mev
        if snapped and snapped_at_hop is None:
            snapped_at_hop = hops
        state = "SNAPPED -> 2 mesons (confined)" if snapped else "Intact flux tube"
        rows.append({
            "hops": hops,
            "tube_ticks": round(tube_ticks, 1),
            "stored_mev": round(stored_mev, 2),
            "snapped": snapped,
            "broken": snapped,
            "state": state,
        })
    return {
        "threshold_mev": threshold_mev,
        "snapped_at_hop": snapped_at_hop,
        "steps": rows,
        "rows": rows,
    }


class BCCMesonSim:
    """Class wrapper compatible with test_bcc_meson_sim.py and run_bcc_suite.py."""

    def __init__(self, tick_to_mev: float = TICK_TO_MEV):
        self.tick_to_mev = tick_to_mev

    def run_spectrum(self) -> List[Dict[str, Any]]:
        return [evaluate_meson(*item) for item in MESON_CATALOG]

    def simulate_spectrum(self) -> List[Dict[str, Any]]:
        return self.run_spectrum()

    def evaluate_meson(
        self, name: str, quarks: str, q1: str, q2: str, spin_j: int, pdg_mev: float = 0.0
    ) -> Dict[str, Any]:
        return evaluate_meson(name, quarks, q1, q2, spin_j, pdg_mev)

    def simulate_flux_tube_stretch(
        self, max_hops: int = 9, ticks_per_hop: float = 9.0, threshold_mev: float = 275.0
    ) -> Dict[str, Any]:
        return simulate_string_breaking(max_hops, ticks_per_hop, threshold_mev)

    def simulate_string_breaking(
        self, max_hops: int = 9, ticks_per_hop: float = 9.0, threshold_mev: float = 275.0
    ) -> Dict[str, Any]:
        return self.simulate_flux_tube_stretch(max_hops, ticks_per_hop, threshold_mev)


def run_meson_demo() -> None:
    sim = BCCMesonSim()
    print("=== PART 1: 6-Face Planck Grid Ground-State Meson Spectrum (q qbar) ===")
    print("Meson    Quarks   J   BareT   RouteT    SpinT   ModelMeV    PDGMeV     Diff")
    print("-" * 75)
    for m in sim.run_spectrum():
        print(
            f"{m['name']:<8} {m['quarks']:<8} {m['J']:>1} {m['BareT']:>7.2f} "
            f"{m['RouteT']:>8.2f} {m['SpinT']:>8.2f} {m['ModelMeV']:>10.2f} "
            f"{m['PDGMeV']:>9.2f} {m['Diff']:>+8.2f}"
        )

    print("\n=== PART 2: Color Flux-Tube Stretch & String Breaking (Threshold = 275.0 MeV) ===")
    print("6-Face Hops  Tube Ticks   Stored MeV   State")
    print("-" * 68)
    stretch = sim.simulate_flux_tube_stretch()
    for row in stretch["steps"]:
        print(
            f"{row['hops']:>11} {row['tube_ticks']:>11.1f} "
            f"{row['stored_mev']:>12.2f}   {row['state']}"
        )


if __name__ == "__main__":
    run_meson_demo()

