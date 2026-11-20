#!/usr/bin/env python3
"""
4-Component Dirac Spinor (Dirac4) Simulation on the 3D BCC (8-Diagonal) Lattice.

Maps the Dirac Clifford algebra onto the 3D BCC 8-diagonal crystal network:
  - Spatial Generators (alpha_x, alpha_y, alpha_z): Coupled simultaneously along all
    8 body-diagonal links <sx, sy, sz> in {+-1}^3 via (sx*sigma_x + sy*sigma_y + sz*sigma_z)/sqrt(3).
  - Temporal Rest-Mass Generator (gamma^0): In-place chiral mixing oscillating between
    left-handed (psi_L) and right-handed (psi_R) spinor components (Zitterbewegung).
  - Spin-1/2 Double Cover: 360° rotation yields -psi; 720° restores +psi.
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

    def propagate_bcc_wavepacket(
        self, half_size: int = 10, ticks: int = 6, k_mom: float = 0.50
    ) -> Dict[str, Any]:
        """
        Evolve a 4-component Dirac spinor wavepacket across a true 3D BCC parity grid
        using a unitary split-step Weyl/Dirac walk over all 8 body diagonals <sx, sy, sz>.
        """
        n = 2 * half_size + 1
        center = half_size

        # Pauli matrices & 3D BCC diagonal projectors P_+- = 0.5 * (I +- (sx*sigma_x + sy*sigma_y + sz*sigma_z)/sqrt(3))
        sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
        sigma_y = np.array([[0.0, -1j], [1j, 0.0]], dtype=np.complex128)
        sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
        eye2 = np.eye(2, dtype=np.complex128)

        # Build 8 normalized directional spin projectors across the 8 BCC body diagonals
        inv_sqrt3 = 1.0 / math.sqrt(3.0)
        diag_projectors: List[Tuple[Tuple[int, int, int], np.ndarray, np.ndarray]] = []
        for sx, sy, sz in BCC_DIAGONALS_8:
            sigma_n = inv_sqrt3 * (sx * sigma_x + sy * sigma_y + sz * sigma_z)
            # Right-handed moves along +n; Left-handed moves along -n (opposite helicity)
            proj_r = (0.5 * (eye2 + sigma_n)) / 4.0
            proj_l = (0.5 * (eye2 - sigma_n)) / 4.0
            diag_projectors.append(((sx, sy, sz), proj_r, proj_l))

        # Chiral rest-mass coin (gamma^0 mixing between L and R spinors)
        theta_m = 0.25
        c_m, s_m = math.cos(theta_m), math.sin(theta_m)

        # Initialize localized right-handed spin-up packet at center (0,0,0) with momentum along (1,1,1)
        psi = np.zeros((4, n, n, n), dtype=np.complex128)
        for d in (-2, 0, 2):
            amp = math.exp(-0.25 * (d * d)) * cmath.exp(1j * k_mom * d)
            # Spinor aligned with (1,1,1) diagonal
            psi[2, center + d, center + d, center + d] = amp * 0.8881
            psi[3, center + d, center + d, center + d] = amp * (0.3251 + 0.3251j)

        norm0 = float(np.sqrt(np.sum(np.abs(psi) ** 2)))
        psi /= norm0

        for _ in range(ticks):
            # Step 1: In-place rest-mass chiral mixing (gamma^0)
            psi_l = psi[0:2]
            psi_r = psi[2:4]
            mix_l = c_m * psi_l - 1j * s_m * psi_r
            mix_r = -1j * s_m * psi_l + c_m * psi_r

            # Step 2: Unitary 8-diagonal 3D BCC spatial shift
            nxt = np.zeros_like(psi)
            for (sx, sy, sz), proj_r, proj_l in diag_projectors:
                # Apply 2x2 spin projector across spatial volume
                shifted_r = np.einsum("ab,bxyz->axyz", proj_r, mix_r)
                shifted_l = np.einsum("ab,bxyz->axyz", proj_l, mix_l)

                src_x = slice(1, n - 1)
                dst_x = slice(1 + sx, n - 1 + sx)
                src_y = slice(1, n - 1)
                dst_y = slice(1 + sy, n - 1 + sy)
                src_z = slice(1, n - 1)
                dst_z = slice(1 + sz, n - 1 + sz)

                nxt[2:4, dst_x, dst_y, dst_z] += shifted_r[:, src_x, src_y, src_z]
                nxt[0:2, dst_x, dst_y, dst_z] += shifted_l[:, src_x, src_y, src_z]

            psi = nxt

        prob_density = np.sum(np.abs(psi) ** 2, axis=0)
        total_norm = float(np.sum(prob_density))

        coords = np.arange(-half_size, half_size + 1, dtype=np.float64)
        X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
        mean_x = float(np.sum(X * prob_density)) / max(1e-12, total_norm)
        mean_y = float(np.sum(Y * prob_density)) / max(1e-12, total_norm)
        mean_z = float(np.sum(Z * prob_density)) / max(1e-12, total_norm)
        radial_shift = math.sqrt(mean_x ** 2 + mean_y ** 2 + mean_z ** 2)

        p_mev = self.mass_mev * k_mom
        e_mev = math.sqrt((p_mev ** 2) + (self.mass_mev ** 2))

        return {
            "ticks": ticks,
            "total_norm": round(total_norm, 6),
            "mean_vec": (round(mean_x, 4), round(mean_y, 4), round(mean_z, 4)),
            "radial_shift_bcc": round(radial_shift, 4),
            "momentum_mev": round(p_mev, 4),
            "dirac_energy_mev": round(e_mev, 4),
        }


def run_dirac4_demo() -> None:
    sim = BCCDirac4SpinorSim(mass_mev=0.511, c_bcc=1.0)

    print("=" * 78)
    print("PART 1: Spin-1/2 Double Cover on 3D BCC Grid (360° -> -psi, 720° -> +psi)")
    print("=" * 78)
    print("Rotation (deg)   Re<psi|psi'>   Im<psi|psi'>   Dirac4 Spinor State")
    print("-" * 78)
    for r in sim.spin_rotation_360_vs_720([0.0, 180.0, 360.0, 540.0, 720.0]):
        print(
            f"{r['angle_deg']:>14.1f} {r['real_overlap']:>+14.6f} "
            f"{r['imag_overlap']:>+14.6f}   {r['spinor_state']}"
        )

    print("\n" + "=" * 78)
    print("PART 2: Rest-Mass Zitterbewegung (gamma^0 Chiral Oscillation L <-> R at p=0)")
    print("=" * 78)
    print("Tick   Time t   Left P(L)   Right P(R)   Total Norm |psi|^2")
    print("-" * 78)
    for z in sim.rest_mass_zitterbewegung(steps=6, dt=0.2618):
        print(
            f"{z['step']:>4} {z['t']:>8.2f} {z['prob_L']:>11.6f} "
            f"{z['prob_R']:>12.6f} {z['norm']:>19.6f}"
        )

    print("\n" + "=" * 78)
    print("PART 3: 3D BCC 8-Diagonal Chiral Wave-Packet Transport & Dirac Energy")
    print("=" * 78)
    wp = sim.propagate_bcc_wavepacket(half_size=10, ticks=6, k_mom=0.50)
    print(
        f"After {wp['ticks']} BCC ticks: Norm = {wp['total_norm']:.6f} | "
        f"Centroid <r> = {wp['mean_vec']} (|r| = {wp['radial_shift_bcc']:.4f}) | "
        f"p = {wp['momentum_mev']:.4f} MeV -> E = {wp['dirac_energy_mev']:.4f} MeV"
    )


if __name__ == "__main__":
    run_dirac4_demo()
