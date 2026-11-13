"""Dry-run F (unscored): does E/E_P = kappa reproduce the paper's Test 3 numbers (line 704)?

Single-handed step U1 = V^+ S^+ at m = 0. Along [111] the positive-band phase theta(+k) != theta(-k):
omega = c0 kappa (1 + xi1 kappa + ...), xi1 = (theta(+k) - theta(-k)) / (2 theta_mean kappa), extrapolated to kappa -> 0.
Then the paper's quantities: E_QG1 = E_P/(2|xi1|), group-velocity slope 2 xi1, E_QG2 = E_P/sqrt(2|xi2|).
Also: the phi above which max|xi2'| (body diagonal, closed form of the derivation) is <= 0.23.
"""
import numpy as np
from l15_lib import V_sym, S_sym

def theta(k, phi):
    U = V_sym(1, k, phi) @ S_sym(1, k)
    a = np.angle(np.linalg.eigvals(U))
    return np.sort(a[a > 0])[0]

def xi1(d, phi, kap):
    d = np.array(d, float); d /= np.linalg.norm(d)
    tp, tm = theta(kap * d, phi), theta(-kap * d, phi)
    return (tp - tm) / (tp + tm) / kap

for phi in (0.5, 1.0, 1.4):
    k1, k2 = 0.02, 0.01
    v1, v2 = xi1((1, 1, 1), phi, k1), xi1((1, 1, 1), phi, k2)
    ext = (4 * v2 - v1) / 3
    print("phi=%.1f  xi1[111]: kappa=0.02 %.6f  kappa=0.01 %.6f  extrapolated %.6f   (paper 0.19245 = 1/(3 sqrt3) = %.6f)" % (phi, v1, v2, ext, 1 / (3 * np.sqrt(3))))
    print("          [100]: %.2e" % xi1((1, 0, 0), phi, k1))
x1 = 1 / (3 * np.sqrt(3)); EP = 1.22e19
print("E_QG1 = E_P/(2 xi1) = %.3f E_P ; slope 2 xi1 = %.4f" % (1 / (2 * x1), 2 * x1))

def xi2_111(phi):
    s2, c2 = np.sin(phi) ** 2, np.cos(phi) ** 2
    return -(1 - 1 / 3) / 3 - 3 / 8 * s2 * c2 / (1 + 3 * s2)
for phi in (0.5, 0.8, 1.0, 1.2, 1.25, 1.27, 1.3, 1.4, 1.5):
    x = abs(xi2_111(phi))
    print("phi=%.2f  |xi2'|[111] = %.4f  E_QG2 = %.3g GeV" % (phi, x, EP / np.sqrt(2 * x)))
lo, hi = 0.5, 1.5
for _ in range(60):
    mid = (lo + hi) / 2
    if abs(xi2_111(mid)) > 0.23: lo = mid
    else: hi = mid
print("max|xi2'| <= 0.23 for phi >= %.4f" % hi)
