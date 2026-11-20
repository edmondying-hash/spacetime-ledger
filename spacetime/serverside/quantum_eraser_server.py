#!/usr/bin/env python3
"""Serverside Module 4: Delayed-Choice Quantum Eraser via Zero-Metadata redraw() API."""

import math
from typing import Dict, List, Optional, Tuple
import numpy as np


class ClientParticle:
    """Opaque client packet holding ZERO slit or entanglement metadata."""

    __slots__ = ("pid", "pos")

    def __init__(self, pid: str, pos: Tuple[int, int, int] = (0, 0, 0)):
        self.pid = pid
        self.pos = pos


class QuantumEraserServer:
    """Backend server managing private slit-entanglement tables during redraw()."""

    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)
        self._next_eid = 1
        # Private server tables (completely hidden from client objects)
        self._signal_to_eid: Dict[int, int] = {}
        self._idler_to_eid: Dict[int, int] = {}
        self._screen_y: Dict[int, int] = {}
        self._slit_amplitudes: Dict[int, Tuple[complex, complex]] = {}

    def entangle_slit_pair(
        self,
        signal: ClientParticle,
        idler: ClientParticle,
        amp_left: complex,
        amp_right: complex,
    ) -> int:
        """Bind a Signal/Idler pair to the left/right slit amplitudes at the crystal."""
        eid = self._next_eid
        self._next_eid += 1
        self._signal_to_eid[id(signal)] = eid
        self._idler_to_eid[id(idler)] = eid
        self._slit_amplitudes[eid] = (amp_left, amp_right)
        return eid

    def redraw_screen_hit(self, signal: ClientParticle, screen_y: int) -> None:
        """Advance Signal to detector D0 and log its screen y-hit in server memory."""
        signal.pos = (64, screen_y, 0)
        eid = self._signal_to_eid.get(id(signal))
        if eid is not None:
            self._screen_y[eid] = screen_y

    def read_idler(self, idler: ClientParticle, basis: str) -> str:
        """Delayed-choice readout on Idler packet ('Z' = Which-Path, 'X' = Eraser)."""
        eid = self._idler_to_eid.get(id(idler))
        if eid is None:
            raise ValueError("Unregistered Idler packet.")

        amp_l, amp_r = self._slit_amplitudes[eid]
        if basis == "Z":
            # Which-path detector: projects onto Left ('L') or Right ('R') slit
            p_l = abs(amp_l) ** 2
            p_r = abs(amp_r) ** 2
            prob_left = p_l / max(p_l + p_r, 1e-12)
            return "L" if self.rng.random() < prob_left else "R"

        if basis == "X":
            # Quantum eraser (45° beam splitter): projects onto |+> = (L+R)/sqrt(2) or |-> = (L-R)/sqrt(2)
            p_plus = 0.5 * abs(amp_l + amp_r) ** 2
            p_minus = 0.5 * abs(amp_l - amp_r) ** 2
            prob_plus = p_plus / max(p_plus + p_minus, 1e-12)
            return "+" if self.rng.random() < prob_plus else "-"

        raise ValueError("Basis must be 'Z' (which-path) or 'X' (eraser).")


def compute_bcc_slit_amplitudes() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute exact 3D BCC Feynman checkerboard amplitudes at x=64 from Left/Right slits."""
    max_x, half_w = 64, 56
    y_vals = np.arange(-half_w, half_w + 1)
    z_vals = np.arange(-half_w, half_w + 1)
    ny, nz = len(y_vals), len(z_vals)
    fwd_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    theta = math.pi / 4.0
    c, s = math.cos(theta), math.sin(theta)
    u_1d = np.array([[c, 1j * s], [1j * s, c]], dtype=np.complex128)
    u_4d = np.kron(u_1d, u_1d)

    slit_x, z_window = 16, 4
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

    def slit_wave(slit_y: int) -> np.ndarray:
        mask = np.zeros((ny, nz))
        for iy, y in enumerate(y_vals):
            if y == slit_y:
                mask[iy, np.abs(z_vals) <= z_window] = 1.0
        out = propagate(psi_slit * mask[None], slit_x, max_x)
        # Sum amplitude across channels and z-slice at central detector strip
        return np.sum(out, axis=(0, 2))

    amp_l_full = slit_wave(-6)
    amp_r_full = slit_wave(6)

    central_mask = (y_vals >= -18) & (y_vals <= 18) & (y_vals % 2 == 0)
    return y_vals[central_mask], amp_l_full[central_mask], amp_r_full[central_mask]


def run_quantum_eraser(total_pairs: int = 4000, seed: int = 42) -> None:
    cy, amp_l, amp_r = compute_bcc_slit_amplitudes()

    # Raw D0 screen hit probabilities (incoherent sum |L|^2 + |R|^2 before Idler readout)
    raw_weights = (np.abs(amp_l) ** 2) + (np.abs(amp_r) ** 2)
    raw_probs = raw_weights / np.sum(raw_weights)

    srv = QuantumEraserServer(seed=seed)
    rng = np.random.default_rng(seed)

    # Lists to store D0 screen y-hits sorted by delayed Idler server readout
    hits_all: List[int] = []
    hits_which_path_L: List[int] = []
    hits_eraser_plus: List[int] = []
    hits_eraser_minus: List[int] = []

    for i in range(total_pairs):
        sig = ClientParticle(f"Sig_{i}", (16, 0, 0))
        idl = ClientParticle(f"Idl_{i}", (16, 0, 0))

        idx = int(rng.choice(len(cy), p=raw_probs))
        y_hit = int(cy[idx])

        # 1. Crystal entangles Signal & Idler in private server table
        srv.entangle_slit_pair(sig, idl, complex(amp_l[idx]), complex(amp_r[idx]))

        # 2. Signal hits screen D0 first (opaque client packet)
        srv.redraw_screen_hit(sig, y_hit)
        hits_all.append(y_hit)

        # 3. Delayed choice on Idler: half measured in Z (which-path), half in X (eraser)
        if i % 2 == 0:
            tag = srv.read_idler(idl, basis="Z")
            if tag == "L":
                hits_which_path_L.append(y_hit)
        else:
            tag = srv.read_idler(idl, basis="X")
            if tag == "+":
                hits_eraser_plus.append(y_hit)
            else:
                hits_eraser_minus.append(y_hit)

    print("=" * 82)
    print("SERVERSIDE MODULE 4: Delayed-Choice Quantum Eraser (Zero-Metadata Client)")
    print("=" * 82)
    print("Pos y | Raw D0 (All) | Z-Basis (Slit L) | Eraser |+> (Fringes) | Eraser |-> (Anti)")
    print("-" * 82)
    for y in cy:
        iy = int(y)
        c_all = sum(1 for v in hits_all if v == iy)
        c_wp = sum(1 for v in hits_which_path_L if v == iy)
        c_ep = sum(1 for v in hits_eraser_plus if v == iy)
        c_em = sum(1 for v in hits_eraser_minus if v == iy)
        print(
            f"y={iy:>3} | {c_all:>12} | {c_wp:>16} | {c_ep:>10} {'*' * (c_ep // 6):<10} | "
            f"{c_em:>10} {'#' * (c_em // 6)}"
        )
    print("-" * 82)
    print("Notice: Eraser |+> recovers dark fringes at y=±12, while |-> peaks at y=±12,")
    print("        and their sum (|+> + |->) equals the washed-out Raw D0 curve!")


if __name__ == "__main__":
    run_quantum_eraser()
