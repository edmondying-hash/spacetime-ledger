#!/usr/bin/env python3
"""
Virtual Force-Carrier Signals on the 3D BCC (8-Diagonal) Lattice  (FIXED COPY).

Original (Edmond, sha256 dbf03e59713a14adcd6d1f78b416cf153d76ff213510869c9bf60c7ac41633d4)
kept verbatim in ../../originals/bcc_virtual_carriers_original.py.

What is INSERTED (closed form, not emergent) in PARTS 1-3:
  * V(r) = 1/r for the massless carrier and V(r) = exp(-r/r0)/r for the massive one.
  * "Shell flux" r^2 * F(r) with F = 1/r^2 -> exactly 1 by construction (circular check).
  * Gluon flux tube: ticks_per_hop * TICK_TO_MEV per hop and a 275 MeV snap threshold.
FIXED: the Yukawa range now follows from the carrier mass, r0 = hbar/(m c), converted
to hops under the HOP switch in bcc_config.py (OD1). In the original, mass_mev was only
an on/off flag and range_scale_hops (1.5, 1.2) set the range by hand.

What is GENUINE (PART 4, new): the static lattice Green's function on the 8 BCC links,
    sum_n [G(x+n) - G(x)] - mu^2 G(x) = -delta_{x,0},
solved by FFT on a periodic box. 1/r (mu = 0) and Yukawa (mu > 0) shapes are then
measured and compared with the parameter-free continuum predictions
    G(r) = exp(-r/lambda) / (4 pi r),  lambda = 2/mu  (coordinate units),
which follow from the 8-link Laplacian ~ 4 nabla^2 and a unit site source = 4 delta^3
(BCC cell volume 4), i.e. 4 nabla^2 G - mu^2 G = -4 delta^3.
"""

import math
import os
import sys
from typing import Any, Dict, List

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import bcc_config as cfg  # noqa: E402

TICK_TO_MEV = cfg.DECLARED_KNOBS["TICK_TO_MEV"][0]
TICKS_PER_LP = cfg.DECLARED_KNOBS["TICKS_PER_LP"][0]
BCC_TICKS_PER_HOP = TICKS_PER_LP * cfg.DERIVED["hop_length_lP"]  # 9*sqrt3 = 15.588 under 'sqrt3_lP'
MEV_J = 1.602176634e-13
HBAR_C_MEV_M = cfg.HBAR * cfg.C_LIGHT / MEV_J      # ~1.97327e-13 MeV m (from fixed constants)


def compton_range_hops(mass_mev: float) -> float:
    """r0 = hbar/(m c) in hops (inf for m = 0). Uses fixed constants + HOP switch only."""
    if mass_mev <= 0.0:
        return math.inf
    return (HBAR_C_MEV_M / mass_mev) / cfg.DERIVED["hop_length_m"]


class BCCVirtualCarrierSim:
    """Closed-form carrier profiles (inserted) plus a genuine lattice Green's function."""

    def __init__(self, tick_to_mev: float = TICK_TO_MEV):
        self.tick_to_mev = tick_to_mev

    def simulate_carrier_range(self, max_hops: int = 8, mass_mev: float = 0.0) -> List[Dict[str, Any]]:
        """INSERTED profile V = exp(-r/r0)/r with r0 = hbar/(m c) in hops (FIXED: tied to mass)."""
        r0 = compton_range_hops(mass_mev)
        rows: List[Dict[str, Any]] = []
        for h in range(1, max_hops + 1):
            r = float(h)
            decay = 1.0 if math.isinf(r0) else math.exp(-r / r0)
            potential = decay / r
            force = potential * ((1.0 / r) + (0.0 if math.isinf(r0) else 1.0 / r0))
            rows.append({
                "hops": h,
                "dist_lP": round(h * cfg.DERIVED["hop_length_lP"], 3),
                "mass_mev": mass_mev,
                "range_hops": r0,
                "decay_factor": decay,
                "potential": round(potential, 6),
                "r2_force_inserted": round(r * r * force, 6),  # = 1 for m = 0 by construction
            })
        return rows

    def weak_flavor_transition_rate(self, separation_hops: int, w_mass_mev: float = 80379.0) -> Dict[str, Any]:
        """INSERTED Yukawa survival exp(-d/r0); FIXED: r0 = hbar/(m_W c) in hops, not 1.2 hops."""
        r0 = compton_range_hops(w_mass_mev)
        survival = math.exp(-separation_hops / r0)
        return {
            "separation_hops": separation_hops,
            "w_mass_mev": w_mass_mev,
            "range_hops": r0,
            "loan_survival": survival,
            "transition_active": survival > 0.01,
        }

    def gluon_carrier_bundling(self, max_hops: int = 8, break_threshold_mev: float = 275.0) -> List[Dict[str, Any]]:
        """INSERTED linear tube energy (ticks/hop * MeV/tick) and inserted snap threshold."""
        rows = []
        for h in range(1, max_hops + 1):
            tube_mev = h * BCC_TICKS_PER_HOP * self.tick_to_mev
            rows.append({"hops": h, "tube_mev": round(tube_mev, 2), "snapped": tube_mev > break_threshold_mev})
        return rows

    @staticmethod
    def lattice_green_function(n: int = 96, mu: float = 0.0) -> Dict[str, Any]:
        """GENUINE: solve sum_n[G(x+n)-G(x)] - mu^2 G = -delta on a periodic n^3 integer grid.
        The 8-link graph on Z^3 splits into 4 disconnected BCC copies; the origin's copy is
        the all-even + all-odd BCC lattice, so G lives on BCC sites automatically."""
        k = 2.0 * np.pi * np.fft.fftfreq(n)
        kx, ky, kz = np.meshgrid(k, k, k, indexing="ij", sparse=True)
        lam = 8.0 * np.cos(kx) * np.cos(ky) * np.cos(kz) - 8.0  # symbol of the 8-link Laplacian
        denom = mu * mu - lam
        zero = np.abs(denom) < 1e-12
        ghat = np.where(zero, 0.0, 1.0 / np.where(zero, 1.0, denom))
        # mu = 0: the symbol vanishes at k = 0 and at (pi,pi,0)-type points (the uniform modes of
        # the 4 disconnected Z^3 copies). Removing them is the periodic-box zero-mode removal and
        # leaves G = 1/(4 pi r) + const on the origin's BCC copy.
        G = np.real(np.fft.ifftn(ghat))
        out: Dict[str, Any] = {"n": n, "mu": mu}
        lam_pred = math.inf if mu == 0 else 2.0 / mu
        dirs = {"axis (2,0,0)": (2, 0, 0), "face (1,1,0)*2": (2, 2, 0), "body (1,1,1)": (1, 1, 1)}
        rows = []
        for name, d in dirs.items():
            for m in range(2, 40):
                p = tuple(m * c for c in d)
                r = math.sqrt(sum(c * c for c in p))
                if r < 6 or r > n / 4:
                    continue
                rows.append((name, r, float(G[p[0] % n, p[1] % n, p[2] % n])))
        rows = np.array([(r, g) for _, r, g in rows])
        names = []
        for name, d in dirs.items():
            for m in range(2, 40):
                r = m * math.sqrt(sum(c * c for c in d))
                if 6 <= r <= n / 4:
                    names.append(name)
        r_arr, g_arr = rows[:, 0], rows[:, 1]
        pred_A = 1.0 / (4.0 * math.pi)
        if mu == 0.0:
            # G = A/r + B (B = periodic-box zero-mode shift); A is measured, then compared to 1/(4 pi)
            M = np.vstack([1.0 / r_arr, np.ones_like(r_arr)]).T
            (A, B), *_ = np.linalg.lstsq(M, g_arr, rcond=None)
            resid = g_arr - (A / r_arr + B)
            out.update({"A_measured": float(A), "A_predicted": pred_A, "box_shift_B": float(B),
                        "max_rel_resid": float(np.max(np.abs(resid) / np.abs(A / r_arr)))})
            per_dir = {}
            for nm in set(names):
                idx = [i for i, x in enumerate(names) if x == nm]
                per_dir[nm] = float(np.mean((g_arr[idx] - B) * r_arr[idx]))
            out["rG_minus_B_by_direction"] = per_dir
        else:
            # log(r G) = log A - r/lambda: measure lambda and A, compare with 2/mu and 1/(4 pi)
            y = np.log(np.maximum(r_arr * g_arr, 1e-300))
            M = np.vstack([np.ones_like(r_arr), -r_arr]).T
            (logA, inv_l), *_ = np.linalg.lstsq(M, y, rcond=None)
            out.update({"lambda_measured": float(1.0 / inv_l), "lambda_predicted": lam_pred,
                        "A_measured": float(math.exp(logA)), "A_predicted": pred_A})
        return out


def run_virtual_carrier_demo() -> None:
    sim = BCCVirtualCarrierSim()
    d = cfg.DERIVED
    print(f"HOP = {d['HOP']} (OD1, open): hop = {d['hop_length_lP']:.4f} l_P = {d['hop_length_m']:.4e} m")
    print("=== PART 1 [INSERTED profiles]: massless 1/r vs Yukawa with r0 = hbar/(m c) (FIXED) ===")
    em = sim.simulate_carrier_range(8, 0.0)
    wk = sim.simulate_carrier_range(8, 80379.0)
    print(f"W range r0 = hbar/(m_W c) = {wk[0]['range_hops']:.4e} hops  (original toy used 1.5 hops)")
    print("Hops   Dist(l_P)   1/r V   r^2*F (=1 by construction)   W decay exp(-r/r0)")
    for a, b in zip(em, wk):
        print(f"{a['hops']:>4} {a['dist_lP']:>10.3f} {a['potential']:>8.4f} {a['r2_force_inserted']:>16.6f} {b['decay_factor']:>26.17f}")
    print("\n=== PART 2 [INSERTED]: W flavour-transition survival exp(-d/r0) ===")
    for sep in (1, 2, 3, 10**6):
        r = sim.weak_flavor_transition_rate(sep)
        print(f"  d = {sep:>8} hops: survival = {r['loan_survival']:.15f}  active = {r['transition_active']}")
    print("  (with r0 ~ 1e17 hops the original '1-2 hop' cut-off does not follow from the W mass)")
    print("\n=== PART 3 [INSERTED]: gluon tube energy and 275 MeV snap ===")
    for g in sim.gluon_carrier_bundling(8):
        print(f"  {g['hops']:>2} hops: {g['tube_mev']:>8.2f} MeV  snapped = {g['snapped']}")
    print("\n=== PART 4 [GENUINE lattice]: static Green's function on the 8 BCC links (FFT, 96^3) ===")
    g0 = sim.lattice_green_function(96, 0.0)
    print(f"  mu = 0 : A_measured = {g0['A_measured']:.6f}  vs  1/(4 pi) = {g0['A_predicted']:.6f}  "
          f"(ratio {g0['A_measured']/g0['A_predicted']:.4f}); max rel. residual of A/r+B fit = {g0['max_rel_resid']:.2e}")
    for k, v in sorted(g0["rG_minus_B_by_direction"].items()):
        print(f"        r*(G-B) along {k:<15}: {v:.6f}")
    g1 = sim.lattice_green_function(96, 1.0 / 3.0)
    print(f"  mu = 1/3 (toy knob): lambda_measured = {g1['lambda_measured']:.4f} vs 2/mu = {g1['lambda_predicted']:.4f} coord units; "
          f"A_measured = {g1['A_measured']:.6f} vs {g1['A_predicted']:.6f}")


if __name__ == "__main__":
    run_virtual_carrier_demo()
