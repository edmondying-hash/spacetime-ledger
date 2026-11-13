"""dirac4 cycle symbol U_k, for direct evaluation.

Source: paper §6.2 and the pinned modules
  frozen/dirac4.py          sha256 f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff
  dirac4_symbol.py          sha256 05f0f8e29bd77f7c809b25c2ee332474bdb2c9c74c7a9a100fa6369911cbb1b8
which agree to machine precision. This file is a working extract, not a
hashed gate document. It is a self-contained copy of the same formulas;
it does not import those modules.

k is in radians, same convention as P = (1+x)(1+y)(1+z)/4 - xyz, with
x = cos k_x, etc. Corner hops h in {(+-1,+-1,+-1)} in cubic-cell-2 units.
Default phi = 1.4 (paper), m = 0. Quasienergy: e^{-4 i omega} = lambda(U_k).

At m = 0:
    A^eps = u^eps I - i n^eps · sigma
    u^eps = c_x c_y c_z - eps s_x s_y s_z
    n^eps = (s_x c_y c_z + eps c_x s_y s_z,
             c_x s_y c_z - eps s_x c_y s_z,
             c_x c_y s_z + eps s_x s_y c_z)
    S^eps = diag(A^eps, A^{eps dagger})
    X^eps = u^eps tau_x + tau_y tensor (n^eps · sigma)
    V^eps = (cos(phi) I - i sin(phi) X^eps) (cos(phi) I + i sin(phi) tau_x)
    U_k   = V^- S^- V^+ S^+

Usage:
    from dirac4_cycle_symbol import U
    Uk = U([kx, ky, kz])          # (4, 4) complex
    Uk = U(k_array)               # k_array[..., 3] -> (..., 4, 4)
    Uk = U(k, phi=1.4, m=0.0)
"""
import numpy as np

S0 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)
SIG = (SX, SY, SZ)
I4 = np.eye(4, dtype=complex)
TX = np.kron(SX, S0)                       # tau_x tensor I_2
KSY = [np.kron(SY, s) for s in SIG]        # tau_y tensor sigma_i

PHI_DEFAULT = 1.4


def u_n(eps, k):
    k = np.asarray(k, float)
    c, s = np.cos(k), np.sin(k)
    cx, cy, cz = c[..., 0], c[..., 1], c[..., 2]
    sx, sy, sz = s[..., 0], s[..., 1], s[..., 2]
    u = cx * cy * cz - eps * sx * sy * sz
    n = (sx * cy * cz + eps * cx * sy * sz,
         cx * sy * cz - eps * sx * cy * sz,
         cx * cy * sz + eps * sx * sy * cz)
    return u, n


def A(eps, k):
    u, n = u_n(eps, k)
    return (u[..., None, None] * S0
            - 1j * (n[0][..., None, None] * SX
                    + n[1][..., None, None] * SY
                    + n[2][..., None, None] * SZ))


def S(eps, k, m=0.0):
    a = A(eps, k)
    t = np.arcsin(m)
    ct, st = np.cos(t), np.sin(t)
    out = np.zeros(a.shape[:-2] + (4, 4), complex)
    out[..., :2, :2] = ct * a
    out[..., :2, 2:] = 1j * st * S0
    out[..., 2:, :2] = 1j * st * S0
    out[..., 2:, 2:] = ct * np.conj(np.swapaxes(a, -1, -2))
    return out


def X(eps, k):
    u, n = u_n(eps, k)
    return (u[..., None, None] * TX
            + n[0][..., None, None] * KSY[0]
            + n[1][..., None, None] * KSY[1]
            + n[2][..., None, None] * KSY[2])


def V(eps, k, phi=PHI_DEFAULT):
    Xmat = X(eps, k)
    left = np.cos(phi) * I4 - 1j * np.sin(phi) * Xmat
    right = np.cos(phi) * I4 + 1j * np.sin(phi) * TX
    return left @ right


def U(k, phi=PHI_DEFAULT, m=0.0):
    """Cycle symbol U_k = V^- S^- V^+ S^+, shape (..., 4, 4)."""
    Sp = S(+1, k, m)
    Vp = V(+1, k, phi)
    Sm = S(-1, k, m)
    Vm = V(-1, k, phi)
    return Vm @ Sm @ Vp @ Sp


if __name__ == "__main__":
    # Self-check against the pinned vectorised symbol, if present.
    import os, sys
    here = "/workspace/L0_V5v2_code_r2_20261111"
    if os.path.isdir(here):
        sys.path.insert(0, here)
        import dirac4_symbol as d4
        rng = np.random.default_rng(0)
        k = rng.uniform(-np.pi, np.pi, size=(20, 3))
        k = np.vstack([k, [0, 0, 0], [np.pi, 0, 0], [0, np.pi, np.pi],
                       [np.pi, np.pi, np.pi], [1.0, 0.5, 2.0]])
        err = np.max(np.abs(U(k) - d4.U_cycle_vec(k, 1.4, 0.0)))
        print(f"max |U - U_cycle_vec| over 25 points: {err:.3e}")
    else:
        k0 = np.array([0.0, 0.0, 0.0])
        Uk = U(k0)
        print("U(0) =\n", Uk)
        print("U(0) - I  max", np.max(np.abs(Uk - np.eye(4))))
