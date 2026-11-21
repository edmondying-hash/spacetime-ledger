"""Four-component BCC node with Wilson layer (Sec. 6.2).

Implements the paper's explicit symbols:
    A^eps_k, n^eps_k, S^eps_k, V^eps_k
    U_k = V^- S^- V^+ S^+
Conventions: lattice units, hop vectors h = (+-1,+-1,+-1)/2, k in the cube
[-pi,pi]^3 (periodic under reciprocal vectors, so the cube covers the BZ).
"""
import numpy as np

S0 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)
SIG = (SX, SY, SZ)
I4 = np.eye(4, dtype=complex)
TX = np.kron(SX, S0)


def _u_n(eps, k, patch=False):
    """u, n of the BCC symbol.

    patch=True adds (1/3) sum_i (1 - cos k_i) to u. This lifts the twelve exact
    massless modes at the face centres (+-pi, +-pi, 0) and permutations, where
    u = +1, n = 0 and the Wilson layer collapses to the identity. It leaves k = 0
    untouched (the added term vanishes there), so Gamma stays massless -- but it
    also shifts the O(k^2) expansion of u, which is what the cost measurement is
    for. Default False: existing runs are unchanged.
    """
    kx, ky, kz = k
    cx, cy, cz = np.cos(kx), np.cos(ky), np.cos(kz)
    sx, sy, sz = np.sin(kx), np.sin(ky), np.sin(kz)
    u = cx * cy * cz - eps * sx * sy * sz
    if patch:
        # patch may be True (the default 1/3 coefficient) or an explicit float.
        a = (1.0 / 3.0) if patch is True else float(patch)
        u = u + a * ((1 - cx) + (1 - cy) + (1 - cz))
    n = np.array([
        sx * cy * cz + eps * cx * sy * sz,
        cx * sy * cz - eps * sx * cy * sz,
        cx * cy * sz + eps * sx * sy * cz,
    ])
    return u, n


def A(eps, k, patch=False):
    u, n = _u_n(eps, k, patch)
    return u * S0 - 1j * (n[0] * SX + n[1] * SY + n[2] * SZ)


def S_step(eps, k, m=0.0, patch=False, wilson=0.0):
    """Mass block [[cos t, i sin t],[i sin t, cos t]] with t = arcsin(m) + Wilson.

    The angle form is unitary for ANY t. The original nu = sqrt(1-m^2) is the same
    thing at Wilson = 0, but it clamps silently to nu = 0 once |m| > 1, which
    silently destroys unitarity (max|eig| = m, error up to 8 at m = 3). A Wilson
    mass m_W = r sum_i (1 - cos k_i) reaches 6r at the corner, so any r > 1/6
    breaks the original parameterisation while leaving the angle form exact.

    New degeneracy trap: wherever t(k) is a multiple of pi at an n = 0 point, the
    mass rotation is +-identity again and the collapse returns -- so the condition
    is on t, not on u + g.
    """
    a = A(eps, k, patch)
    if wilson:
        t = np.arcsin(m) + wilson * float(np.sum(1.0 - np.cos(k)))
    else:
        t = np.arcsin(m)
    ct, st = np.cos(t), np.sin(t)
    return np.block([[ct * a, 1j * st * S0],
                     [1j * st * S0, ct * a.conj().T]])


def V_step(eps, k, phi, patch=False):
    u, n = _u_n(eps, k, patch)
    X = u * np.kron(SX, S0) + np.kron(SY, n[0] * SX + n[1] * SY + n[2] * SZ)
    # X^2 = 1
    return (np.cos(phi) * I4 - 1j * np.sin(phi) * X) @ (np.cos(phi) * I4 + 1j * np.sin(phi) * TX)


def U_cycle(k, phi=1.4, m=0.0, wilson=True, patch=False, wilson_mass=0.0):
    s_plus = S_step(+1, k, m, patch, wilson_mass)
    s_minus = S_step(-1, k, m, patch, wilson_mass)
    if wilson:
        v_plus, v_minus = V_step(+1, k, phi, patch), V_step(-1, k, phi, patch)
    else:
        v_plus = v_minus = I4
    return v_minus @ s_minus @ v_plus @ s_plus


def omega(k, phi=1.4, m=0.0, wilson=True, patch=False, wilson_mass=0.0):
    """Lowest positive per-layer frequency of U (radians per layer)."""
    lam = np.linalg.eigvals(U_cycle(k, phi, m, wilson, patch, wilson_mass))
    theta = np.angle(lam)
    w = np.mod(-theta, 2 * np.pi) / 4.0
    return float(np.min(w))
