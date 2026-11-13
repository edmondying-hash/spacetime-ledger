"""Dry-run D (unscored): real-space hop implementation of the whole tick.

D1  operator identity on a plane wave (N=16): hop-form cycle vs symbol U(k).
D2  Gaussian packet on the two lowest positive-frequency bands, periodic BCC cell
    (N=96), 3 cycles, kappa0 = 0.6, sigma = 9, phi = 1.4. Centroid velocity
    (coordinates per cycle, coordinate = a/2) against the band-resolved prediction
    sum_k w_k grad_k(4 omega_j), and against its negated-direction partner.
"""
import os, sys, time, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from l15_lib import *

phi = 1.4
rng = np.random.default_rng(3)
N = 16; m = np.array([3, -2, 1]); k = 2 * np.pi * m / N
g = np.arange(N); X, Y, Z = np.meshgrid(g, g, g, indexing='ij')
valid = ((X % 2) == (Y % 2)) & ((Y % 2) == (Z % 2))
v = rng.normal(size=4) + 1j * rng.normal(size=4); v /= np.linalg.norm(v)
pw = np.exp(1j * (k[0] * X + k[1] * Y + k[2] * Z)) * valid
out = cycle(np.einsum('a,xyz->axyz', v, pw), phi)
pred = np.einsum('ab,b,xyz->axyz', U_sym(k, phi), v, pw)
print("D1  plane-wave cycle, hop form vs symbol: max deviation %.2e" % np.abs(out - pred).max())

N = 96; sigma = 9.0; cyc = 3; kap0 = 0.6; x0 = np.array([N // 2] * 3)
dirs = [(1, 0, 0), (-1, 0, 0), (1, 1, 1), (-1, -1, -1), (1, 1, -1), (-1, -1, 1), (1, 1, 0), (1, 2, 3)]
res = {}
print("D2  N=%d sigma=%.0f cycles=%d kappa0=%.1f phi=%.1f ; velocity in coordinates per cycle" % (N, sigma, cyc, kap0, phi))
for d in dirs:
    n = np.array(d, float); n /= np.linalg.norm(n); k0 = kap0 * n
    t = time.time()
    psi, grid, pr = build_packet(N, k0, sigma, phi, x0)
    c0 = centroid(psi, grid, x0, N)
    for _ in range(cyc): psi = cycle(psi, phi)
    c1 = centroid(psi, grid, x0, N); vel = (c1 - c0) / cyc
    res[d] = (vel, pr, (np.abs(psi) ** 2).sum())
    print("   %-10s measured %s  predicted %s  max|diff| %.2e  norm-1 %.1e  (%.0fs)" % (
        str(d), np.array2string(vel, precision=5), np.array2string(pr, precision=5),
        np.abs(vel - pr).max(), res[d][2] - 1, time.time() - t), flush=True)
print("D2  direction-odd test, |v(n) + v(-n)|_max:")
for a, b in [((1, 0, 0), (-1, 0, 0)), ((1, 1, 1), (-1, -1, -1))]:
    print("   %s vs %s : %.2e" % (a, b, np.abs(res[a][0] + res[b][0]).max()))
print("D2  worst |measured - predicted| over the 8 directions: %.2e" % max(np.abs(r[0] - r[1]).max() for r in res.values()))
