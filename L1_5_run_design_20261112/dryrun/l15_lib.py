"""Shared code for the unscored L1.5 design dry-run.

All symbols are the paper's Sec. 6.2 symbols (Table dirac4), massless unless stated:
  A^e = u - i n.sigma, S^e = diag(A^e, A^e dagger) (m = 0), X^e = u T + SY (x) n.sigma,
  V^e = (cos phi - i sin phi X^e)(cos phi + i sin phi T), T = SX (x) 1,
  U = V^- S^- V^+ S^+, e^{-4 i omega} an eigenvalue of U, k in radians per a/2 (kappa = |k|).
The analytic (non-conjugating) construction is used so that the same code can be
evaluated at complex k (Taylor extraction) and in mpmath.
"""
import itertools
import numpy as np

S0 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)
SIG = (SX, SY, SZ)
I4 = np.eye(4, dtype=complex)
T = np.kron(SX, S0)


def un(eps, k):
    kx, ky, kz = k
    cx, cy, cz = np.cos(kx), np.cos(ky), np.cos(kz)
    sx, sy, sz = np.sin(kx), np.sin(ky), np.sin(kz)
    u = cx * cy * cz - eps * sx * sy * sz
    n = np.array([sx * cy * cz + eps * cx * sy * sz,
                  cx * sy * cz - eps * sx * cy * sz,
                  cx * cy * sz + eps * sx * sy * cz])
    return u, n


def A_sym(eps, k, dag=False):
    u, n = un(eps, k)
    sg = 1 if dag else -1
    return u * S0 + sg * 1j * (n[0] * SX + n[1] * SY + n[2] * SZ)


def S_sym(eps, k):
    Z = np.zeros((2, 2), complex)
    return np.block([[A_sym(eps, k), Z], [Z, A_sym(eps, k, True)]])


def V_sym(eps, k, phi):
    u, n = un(eps, k)
    X = u * T + np.kron(SY, n[0] * SX + n[1] * SY + n[2] * SZ)
    return (np.cos(phi) * I4 - 1j * np.sin(phi) * X) @ (np.cos(phi) * I4 + 1j * np.sin(phi) * T)


def XY(k, phi):
    """X = V^- S^-, Y = V^+ S^+, so U = X Y."""
    return V_sym(-1, k, phi) @ S_sym(-1, k), V_sym(1, k, phi) @ S_sym(1, k)


def U_sym(k, phi, phi_plus=None):
    p2 = phi if phi_plus is None else phi_plus
    return V_sym(-1, k, phi) @ S_sym(-1, k) @ V_sym(1, k, p2) @ S_sym(1, k)


def band_set(k, phi):
    """Sorted eigenphases of U (radians per cycle)."""
    return np.sort(np.angle(np.linalg.eigvals(U_sym(k, phi))))


def omega_bar(k, phi):
    """Mean of the two lowest positive per-layer frequencies (pairs +-theta)."""
    a = np.sort(np.abs(np.angle(np.linalg.eigvals(U_sym(k, phi)))))
    return (a[0] + a[2]) / 8.0


# ---- real-space hop form -------------------------------------------------
H8 = [np.array(h) for h in itertools.product((1, -1), repeat=3)]


def hop_weights(eps):
    out = []
    for h in H8:
        hx, hy, hz = h
        al = (1 - 1j * eps * hx * hy * hz) / 8
        be = np.array([-1j * hx - eps * hy * hz,
                       -1j * hy + eps * hx * hz,
                       -1j * hz - eps * hx * hy]) / 8
        out.append((h, al, be))
    return out


def hop_matrices(eps):
    out = []
    for h, al, be in hop_weights(eps):
        A2 = al * S0 - 1j * sum(be[j] * SIG[j] for j in range(3))
        Ad2 = al * S0 + 1j * sum(be[j] * SIG[j] for j in range(3))
        Z = np.zeros((2, 2), complex)
        S4 = np.block([[A2, Z], [Z, Ad2]])
        X4 = al * T + sum(be[j] * np.kron(SY, SIG[j]) for j in range(3))
        out.append((h, S4, X4))
    return out


WP, WM = hop_matrices(1), hop_matrices(-1)


def hop_apply(psi, Ws, idx):
    out = np.zeros_like(psi)
    for h, S4, X4 in Ws:
        M = (S4, X4)[idx]
        sh = np.roll(psi, shift=(-h[0], -h[1], -h[2]), axis=(1, 2, 3))
        out += np.einsum('ab,bxyz->axyz', M, sh)
    return out


def V_apply(psi, Ws, phi):
    c, s = np.cos(phi), np.sin(phi)
    p1 = c * psi + 1j * s * np.einsum('ab,bxyz->axyz', T, psi)
    return c * p1 - 1j * s * hop_apply(p1, Ws, 1)


def cycle(psi, phi):
    psi = hop_apply(psi, WP, 0)
    psi = V_apply(psi, WP, phi)
    psi = hop_apply(psi, WM, 0)
    return V_apply(psi, WM, phi)


def centroid(psi, grid, x0, N):
    w = (np.abs(psi) ** 2).sum(axis=0)
    wrap = lambda d: (d + N // 2) % N - N // 2
    return np.array([(w * wrap(g - x0[i])).sum() for i, g in enumerate(grid)])


def pos2(k, phi):
    lam, V = np.linalg.eig(U_sym(k, phi))
    th = np.angle(lam)
    idx = sorted([i for i in range(4) if th[i] < 0], key=lambda i: abs(th[i]))[:2]
    return [(-th[i] / 4, V[:, i]) for i in idx]


def vg_band(k, phi, j, h=1e-5):
    g = np.zeros(3)
    for i in range(3):
        e = np.zeros(3)
        e[i] = h
        g[i] = 4 * (pos2(k + e, phi)[j][0] - pos2(k - e, phi)[j][0]) / (2 * h)
    return g


def build_packet(N, k0, sigma, phi, x0, kmin=0.1):
    """Gaussian packet (|psi|^2 std sigma) built in k-space on the two lowest
    positive-frequency bands; returns real-space state, grid, and the predicted
    centroid velocity (coordinates per cycle) from band-resolved weights."""
    sk = 1 / (2 * sigma)
    m = np.arange(N)
    kk = 2 * np.pi * np.where(m <= N // 2, m, m - N) / N
    b0 = pos2(k0, phi)
    Q0, _ = np.linalg.qr(np.stack([b0[0][1], b0[1][1]], axis=1))
    vref = Q0[:, 0]
    psik = np.zeros((4, N, N, N), complex)
    acc = np.zeros(3)
    tot = 0.0
    for i, kx in enumerate(kk):
        if abs(kx - k0[0]) > 6 * sk:
            continue
        for j, ky in enumerate(kk):
            if abs(ky - k0[1]) > 6 * sk:
                continue
            for l, kz in enumerate(kk):
                if abs(kz - k0[2]) > 6 * sk:
                    continue
                k = np.array([kx, ky, kz])
                if np.linalg.norm(k) < kmin:
                    continue
                q = k - k0
                w = np.exp(-np.dot(q, q) / (4 * sk ** 2))
                b = pos2(k, phi)
                E = np.stack([b[0][1], b[1][1]], axis=1)
                Q, _ = np.linalg.qr(E)
                v = Q @ (Q.conj().T @ vref)
                nv = np.linalg.norm(v)
                if nv < 1e-6:
                    continue
                v /= nv
                a = w * np.exp(-1j * np.dot(k, x0)) * v
                psik[:, i, j, l] = a
                c = np.linalg.lstsq(E, a, rcond=None)[0]
                wts = np.abs(c) ** 2
                for jb in range(2):
                    acc += wts[jb] * vg_band(k, phi, jb)
                tot += wts.sum()
    psi = np.fft.ifftn(psik, axes=(1, 2, 3)) * N ** 3
    g = np.arange(N)
    X, Y, Z = np.meshgrid(g, g, g, indexing='ij')
    valid = ((X % 2) == (Y % 2)) & ((Y % 2) == (Z % 2))
    psi = psi * valid[None]
    psi /= np.sqrt((np.abs(psi) ** 2).sum())
    return psi, (X, Y, Z), acc / tot


# ---- the 13 directions (cubic classes) and their negatives ----------------
DIR13 = [(1, 0, 0), (0, 1, 0), (0, 0, 1),
         (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1),
         (1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]
