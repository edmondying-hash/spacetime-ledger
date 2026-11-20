#!/usr/bin/env python3
"""
4-Component Dirac Spinor (Dirac4) Simulation on the 3D BCC (8-Diagonal) Lattice.

Maps the Dirac Clifford algebra onto the 3D BCC 8-diagonal crystal network:
  - Spatial shift (FIXED, unitary): for each of the 8 links n = (sx,sy,sz),
    A_n = Pi_z(sz) Pi_y(sy) Pi_x(sx) with Pi_a(s) = (I + s sigma_a)/2; shift = sum_n A_n T_n
    = S_z S_y S_x (product of unitary spin-conditioned axis shifts). OD3: form open.
  - Temporal Rest-Mass Generator (gamma^0): In-place chiral mixing oscillating between
    left-handed (psi_L) and right-handed (psi_R) spinor components (Zitterbewegung).
  - Spin-1/2 Double Cover: 360 deg -> -psi; 720 deg -> +psi (closed form, inserted).
"""

import cmath
import itertools
import math
from typing import Any, Dict, List, Tuple
import numpy as np

BCC_DIAGONALS_8: Tuple[Tuple[int, int, int], ...] = tuple(itertools.product((-1, 1), repeat=3))


class BCCDirac4SpinorSim:
    """4-component Dirac spinor evolution on the 3D BCC 8-diagonal lattice."""

    def __init__(self, mass_mev: float = 0.511, c_bcc: float = 1.0):
        # Default rest mass = electron (0.511 MeV)
        self.mass_mev = mass_mev
        self.c = c_bcc

    def spin_rotation_360_vs_720(self, angles_deg: List[float]) -> List[Dict[str, Any]]:
        """
        Rotate a spin-up Dirac4 spinor psi = (1, 0, 0, 0) around the z-axis:
        U_z(theta) = diag(exp(-i*theta/2), exp(+i*theta/2), exp(-i*theta/2), exp(+i*theta/2)).
        """
        rows: List[Dict[str, Any]] = []
        for deg in angles_deg:
            rad = math.radians(deg)
            phase_up = cmath.exp(-0.5j * rad)
            overlap_real = phase_up.real
            state_label = (
                "Identity (+psi)"
                if abs(overlap_real - 1.0) < 1e-6
                else ("Sign Flip (-psi)" if abs(overlap_real + 1.0) < 1e-6 else "Superposition")
            )
            rows.append({
                "angle_deg": deg,
                "real_overlap": round(overlap_real, 6),
                "imag_overlap": round(phase_up.imag, 6),
                "spinor_state": state_label,
            })
        return rows

    def rest_mass_zitterbewegung(self, steps: int = 6, dt: float = 0.2618) -> List[Dict[str, Any]]:
        """
        Evolve a pure left-handed spinor psi(0) = (1, 0, 0, 0) at rest (p = 0) under
        the gamma^0 rest-mass coupling H_0 = omega * gamma^0 (swaps L <-> R).
        """
        omega = 1.0
        rows: List[Dict[str, Any]] = []

        for step in range(steps + 1):
            t = step * dt
            psi_l = math.cos(omega * t) + 0.0j
            psi_r = -1j * math.sin(omega * t)
            prob_l = abs(psi_l) ** 2
            prob_r = abs(psi_r) ** 2
            norm = prob_l + prob_r
            rows.append({
                "step": step,
                "t": round(t, 2),
                "prob_L": round(prob_l, 6),
                "prob_R": round(prob_r, 6),
                "norm": round(norm, 6),
            })
        return rows

    @staticmethod
    def _weyl_link_ops() -> List[Tuple[Tuple[int, int, int], np.ndarray]]:
        """
        FIXED (unitary) 8-link shift.  For each BCC link n = (sx, sy, sz):
            A_n = Pi_z(sz) @ Pi_y(sy) @ Pi_x(sx),   Pi_a(s) = (I + s*sigma_a)/2.
        The one-tick shift  S psi(r) = sum_n A_n psi(r - n)  equals the product
        S_z S_y S_x of three spin-conditioned axis shifts, each unitary, so S is
        exactly unitary, and every term moves amplitude along one of the 8 BCC
        body diagonals (+-1,+-1,+-1).  (The previous projector-sum
        sum_n (I + sigma.n/sqrt3)/8 T_n was not unitary: norm 0.028 after 6 ticks.)
        Alternative unitary forms exist (other axis orderings; the paper's dirac4
        construction) -- OD3, left open for Edmond.
        """
        sig = {
            "x": np.array([[0, 1], [1, 0]], dtype=np.complex128),
            "y": np.array([[0, -1j], [1j, 0]], dtype=np.complex128),
            "z": np.array([[1, 0], [0, -1]], dtype=np.complex128),
        }
        eye2 = np.eye(2, dtype=np.complex128)
        ops = []
        for sx, sy, sz in BCC_DIAGONALS_8:
            a = (0.5 * (eye2 + sz * sig["z"])) @ (0.5 * (eye2 + sy * sig["y"])) @ (0.5 * (eye2 + sx * sig["x"]))
            ops.append(((sx, sy, sz), a))
        return ops

    def step_operator_symbol(self, k: Tuple[float, float, float], theta_m: float = 0.25) -> np.ndarray:
        """4x4 one-tick Bloch symbol U(k) = Shift(k) @ Coin (same convention as the grid walk)."""
        ops = self._weyl_link_ops()
        w_r = sum(a * np.exp(-1j * np.dot(k, n)) for n, a in ops)
        w_l = sum(a * np.exp(+1j * np.dot(k, n)) for n, a in ops)  # L moves along -n
        shift = np.zeros((4, 4), dtype=np.complex128)
        shift[0:2, 0:2] = w_l
        shift[2:4, 2:4] = w_r
        c_m, s_m = math.cos(theta_m), math.sin(theta_m)
        coin = np.array([[c_m, 0, -1j * s_m, 0], [0, c_m, 0, -1j * s_m],
                         [-1j * s_m, 0, c_m, 0], [0, -1j * s_m, 0, c_m]], dtype=np.complex128)
        return shift @ coin

    def dispersion_check(self, theta_m: float = 0.25, kmag: float = 0.1, ndirs: int = 200) -> Dict[str, Any]:
        """Measured (not inserted) quasi-energy omega(k) from the walk's own symbol."""
        def omega(kv):
            ev = np.linalg.eigvals(self.step_operator_symbol(tuple(kv), theta_m))
            return float(np.min(np.abs(np.angle(ev))))
        unit_err = max(
            float(np.max(np.abs(self.step_operator_symbol(tuple(kv), theta_m).conj().T
                                @ self.step_operator_symbol(tuple(kv), theta_m) - np.eye(4))))
            for kv in np.random.default_rng(0).uniform(-math.pi, math.pi, (20, 3))
        )
        golden = math.pi * (3.0 - math.sqrt(5.0))
        oms = []
        for i in range(ndirs):
            z = 1.0 - 2.0 * (i + 0.5) / ndirs
            rr = math.sqrt(1.0 - z * z)
            d = np.array([rr * math.cos(golden * i), rr * math.sin(golden * i), z])
            oms.append(omega(kmag * d))
        oms = np.array(oms)
        om0 = omega((0.0, 0.0, 0.0))
        # small-k speed in coordinate units/tick: sqrt(omega(k)^2 - omega(0)^2)/|k|
        v_eff = float(np.mean(np.sqrt(np.maximum(oms**2 - om0**2, 0.0)) / kmag))
        return {
            "symbol_unitarity_max_err": unit_err,
            "omega_k0_rest_mass": round(om0, 6),
            "kmag": kmag,
            "omega_mean": round(float(oms.mean()), 6),
            "omega_rel_anisotropy": float((oms.max() - oms.min()) / oms.mean()),
            "small_k_speed_coord_per_tick": round(v_eff, 4),
            "small_k_speed_hop_per_tick": round(v_eff / math.sqrt(3.0), 4),
        }

    def propagate_bcc_wavepacket(
        self, half_size: int = 12, ticks: int = 1000, k_mom: float = 0.50, theta_m: float = 0.25
    ) -> Dict[str, Any]:
        """
        Evolve a 4-component spinor on a periodic BCC grid (n = 2*half_size, even, so
        BCC parity is preserved under wrap).  Each tick: rest-mass coin (gamma^0 L<->R
        mixing, unitary) then the unitary 8-link Weyl shift (R along +n, L along -n).
        Norm is measured, not assumed.
        """
        n = 2 * half_size
        ops = self._weyl_link_ops()
        c_m, s_m = math.cos(theta_m), math.sin(theta_m)
        psi = np.zeros((4, n, n, n), dtype=np.complex128)
        center = half_size if half_size % 2 == 0 else half_size - 1
        for d in (-2, 0, 2):  # all-even sites along the (1,1,1) body diagonal
            amp = math.exp(-0.25 * (d * d)) * cmath.exp(1j * k_mom * d)
            psi[2, center + d, center + d, center + d] = amp * 0.8881
            psi[3, center + d, center + d, center + d] = amp * (0.3251 + 0.3251j)
        psi /= np.sqrt(np.sum(np.abs(psi) ** 2))

        coords = np.arange(n, dtype=np.float64) - center
        max_drift = 0.0
        for _ in range(ticks):
            psi_l = c_m * psi[0:2] - 1j * s_m * psi[2:4]
            psi_r = -1j * s_m * psi[0:2] + c_m * psi[2:4]
            nxt = np.zeros_like(psi)
            for (sx, sy, sz), a in ops:
                nxt[2:4] += np.roll(np.einsum("ab,bxyz->axyz", a, psi_r), (sx, sy, sz), axis=(1, 2, 3))
                nxt[0:2] += np.roll(np.einsum("ab,bxyz->axyz", a, psi_l), (-sx, -sy, -sz), axis=(1, 2, 3))
            psi = nxt
            max_drift = max(max_drift, abs(float(np.sum(np.abs(psi) ** 2)) - 1.0))

        prob = np.sum(np.abs(psi) ** 2, axis=0)
        total_norm = float(np.sum(prob))
        odd_parity_weight = float(np.sum(prob[(np.indices((n, n, n)).sum(axis=0) % 2 == 1)]))
        X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
        mean = [float(np.sum(A * prob)) / total_norm for A in (X, Y, Z)]

        # NOTE: inserted textbook relation, kept for display only (not measured):
        p_mev = self.mass_mev * k_mom
        e_mev = math.sqrt(p_mev ** 2 + self.mass_mev ** 2)
        return {
            "ticks": ticks,
            "grid": n,
            "total_norm": total_norm,
            "max_norm_drift": max_drift,
            "mixed_parity_weight": odd_parity_weight,
            "mean_vec_last_tick": tuple(round(m, 4) for m in mean),
            "momentum_mev_inserted": round(p_mev, 4),
            "dirac_energy_mev_inserted": round(e_mev, 4),
        }


def run_dirac4_demo() -> None:
    sim = BCCDirac4SpinorSim(mass_mev=0.511, c_bcc=1.0)

    print("=" * 78)
    print("PART 1: Spin-1/2 Double Cover (closed-form exp(-i theta/2); inserted textbook identity, not a lattice evolution)")
    print("=" * 78)
    print("Rotation (deg)   Re<psi|psi'>   Im<psi|psi'>   Dirac4 Spinor State")
    print("-" * 78)
    for r in sim.spin_rotation_360_vs_720([0.0, 180.0, 360.0, 540.0, 720.0]):
        print(
            f"{r['angle_deg']:>14.1f} {r['real_overlap']:>+14.6f} "
            f"{r['imag_overlap']:>+14.6f}   {r['spinor_state']}"
        )

    print("\n" + "=" * 78)
    print("PART 2: L<->R oscillation at p=0 (closed-form cos/sin of the coin; inserted, not evolved)")
    print("=" * 78)
    print("Tick   Time t   Left P(L)   Right P(R)   Total Norm |psi|^2")
    print("-" * 78)
    for z in sim.rest_mass_zitterbewegung(steps=6, dt=0.2618):
        print(
            f"{z['step']:>4} {z['t']:>8.2f} {z['prob_L']:>11.6f} "
            f"{z['prob_R']:>12.6f} {z['norm']:>19.6f}"
        )

    print("\n" + "=" * 78)
    print("PART 3: Unitary 8-link BCC Dirac walk (FIXED: was non-unitary projector sum)")
    print("=" * 78)
    wp = sim.propagate_bcc_wavepacket(half_size=12, ticks=1000, k_mom=0.50)
    print(
        f"After {wp['ticks']} ticks on a periodic {wp['grid']}^3 BCC grid: Norm = {wp['total_norm']:.15f} | "
        f"max |norm-1| = {wp['max_norm_drift']:.2e} | weight on odd sublattice (0 expected after an even tick count) = {wp['mixed_parity_weight']:.3e}"
    )
    print(f"Centroid at last tick = {wp['mean_vec_last_tick']} (periodic grid; indicative only)")
    print(f"[inserted, not measured] p = {wp['momentum_mev_inserted']} MeV -> E = sqrt(p^2+m^2) = {wp['dirac_energy_mev_inserted']} MeV")
    print("\n" + "=" * 78)
    print("PART 4: Measured quasi-energy omega(k) from the walk symbol (theta_m = 0.25)")
    print("=" * 78)
    for key, val in sim.dispersion_check().items():
        print(f"  {key:<32} {val}")


if __name__ == "__main__":
    run_dirac4_demo()
