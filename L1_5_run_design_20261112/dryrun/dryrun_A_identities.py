"""Dry-run A (unscored): the exact k -> -k identities and their consequences."""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from l15_lib import *
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frozen'))
from dirac4 import U_cycle

rng = np.random.default_rng(20261112)
print("A1  frozen dirac4.py vs analytic construction (200 random k, phi):")
worst = 0
for _ in range(200):
    k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.05, 1.55)
    worst = max(worst, np.abs(U_cycle(k, phi) - U_sym(k, phi)).max())
print("    max |U_frozen - U_analytic| = %.2e" % worst)

print("A2  one-layer identities, 200 random k, phi, both eps:")
w = dict(A=0, S=0, V=0)
for _ in range(200):
    k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.05, 1.55)
    for e in (1, -1):
        w['A'] = max(w['A'], np.abs(A_sym(e, -k) - A_sym(-e, k).conj().T).max())
        w['S'] = max(w['S'], np.abs(S_sym(e, -k) - T @ S_sym(-e, k) @ T).max())
        w['V'] = max(w['V'], np.abs(V_sym(e, -k, phi) - T @ V_sym(-e, k, phi) @ T).max())
print("    A^e(-k) = A^-e(k)^dag          : %.2e" % w['A'])
print("    S^e(-k) = T S^-e(k) T          : %.2e" % w['S'])
print("    V^e(-k) = T V^-e(k) T          : %.2e" % w['V'])

print("A3  U(-k) = T (Y X) T and Y X = X^-1 U X, 200 random k, phi:")
worst = 0
for _ in range(200):
    k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.05, 1.55)
    X, Y = XY(k, phi); Xm, Ym = XY(-k, phi)
    worst = max(worst, np.abs(Xm @ Ym - T @ (Y @ X) @ T).max(),
                np.abs(Y @ X - np.linalg.inv(X) @ (X @ Y) @ X).max())
print("    max deviation = %.2e" % worst)

print("A4  spectrum of U(k) against spectrum of U(-k), equal angles, 200 random k, phi:")
worst = 0
for _ in range(200):
    k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.05, 1.55)
    worst = max(worst, np.abs(band_set(k, phi) - band_set(-k, phi)).max())
print("    max eigenphase difference = %.2e" % worst)

Q = np.kron(SZ, SY)
print("A5  Q = SZ (x) SY: Q A Q^-1 = A*, Q S Q^-1 = S*, Q V Q^-1 = V*, hence Q U Q^-1 = U*  (200 random k, phi, both eps):")
w = dict(S=0, V=0, U=0)
Qi = np.linalg.inv(Q)
for _ in range(200):
    k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.05, 1.55)
    for e in (1, -1):
        w['S'] = max(w['S'], np.abs(Q @ S_sym(e, k) @ Qi - S_sym(e, k).conj()).max())
        w['V'] = max(w['V'], np.abs(Q @ V_sym(e, k, phi) @ Qi - V_sym(e, k, phi).conj()).max())
    w['U'] = max(w['U'], np.abs(Q @ U_sym(k, phi) @ Qi - U_sym(k, phi).conj()).max())
print("    S: %.2e   V: %.2e   U: %.2e" % (w['S'], w['V'], w['U']))
print("A5b the spectrum is symmetric under theta -> -theta (a consequence of A5), 200 random k, phi:")
worst = 0
for _ in range(200):
    k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.05, 1.55)
    th = band_set(k, phi)
    worst = max(worst, np.abs(th + th[::-1]).max())
print("    max |theta_j + theta_(5-j)| = %.2e" % worst)

print("A6  record: the identity needs equal angles (phi on V+ differs from phi on V-):")
for p2, p4 in [(0.5, 1.3), (0.9, 1.0), (1.4, 1.4)]:
    d = []
    for _ in range(20):
        k = rng.uniform(-1, 1, 3)
        a = np.sort(np.angle(np.linalg.eigvals(U_sym(k, p4, p2))))
        b = np.sort(np.angle(np.linalg.eigvals(U_sym(-k, p4, p2))))
        d.append(np.abs(a - b).max())
    print("    (phi+, phi-) = (%.1f, %.1f): max eigenphase difference U(k) vs U(-k) over 20 k = %.2e" % (p2, p4, max(d)))
