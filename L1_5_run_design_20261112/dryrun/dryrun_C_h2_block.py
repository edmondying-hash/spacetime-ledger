"""Dry-run C (unscored): effective-Hamiltonian expansion U = exp(-4 i H(k)) near k = 0.

H(t n) = sum_j H_j t^j is extracted from the analytic (non-conjugating) symbol at
complex t on a circle (FFT), with the matrix logarithm as a power series in U - 1.
H_1 has eigenvalues +-c0 (each twice). Second-order degenerate perturbation theory:
the O(t^2) frequency shifts of the +c0 pair are the eigenvalues of P+ H_2 P+.
"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from l15_lib import U_sym, DIR13

def logm_near_I(U, terms=60):
    N = U - np.eye(4); R = np.zeros((4, 4), complex); P = np.eye(4, dtype=complex)
    for n in range(1, terms):
        P = P @ N; R += ((-1) ** (n + 1) / n) * P
    return R

def taylor_H(nhat, phi, J=4, r=0.04, M=64):
    ts = r * np.exp(2j * np.pi * np.arange(M) / M)
    Hs = np.array([(1j / 4) * logm_near_I(U_sym(t * np.asarray(nhat), phi)) for t in ts])
    return [(Hs * (ts ** -j)[:, None, None]).mean(axis=0) for j in range(J)]

print("U(0) = 1 check: max |U(0)-1| = %.1e" % np.abs(U_sym(np.zeros(3), 1.4) - np.eye(4)).max())
for phi in (1.4, 0.8):
    c0 = 0.5 * np.sqrt(1 + 3 * np.sin(phi) ** 2)
    print("phi = %.1f, c0 = %.10f" % (phi, c0))
    worst = 0.0
    for d in DIR13 + [(2, 1, 0), (3, 1, 2), (1, 2, -3)]:
        for sg in (1, -1):
            n = sg * np.array(d, float); n /= np.linalg.norm(n)
            H = taylor_H(n, phi)
            H1 = (H[1] + H[1].conj().T) / 2; H2 = (H[2] + H[2].conj().T) / 2
            w, V = np.linalg.eigh(H1)
            assert abs(w[-1] - c0) < 1e-10 and abs(w[-2] - c0) < 1e-10
            Vp = V[:, w > 0]
            e2 = np.linalg.eigvalsh(Vp.conj().T @ H2 @ Vp)
            worst = max(worst, np.abs(e2).max())
    print("   H_1 eigenvalues +-c0 (double) confirmed in 32 signed directions; max |eig(P+ H_2 P+)| = %.2e" % worst)
