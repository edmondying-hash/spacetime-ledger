"""Dry-run G (unscored): second S4 pilot, on a grid different from dry-run D.

Dry-run D: N=96, phi=1.4. This one: N=104, phi=1.2, directions (1,0,0), (-1,0,0), (1,1,1), (-1,-1,-1),
(1,-1,1), (-1,1,-1), (2,1,1), (3,1,1). The S4 gate grid (N=100, phi=1.3, other directions) lies between the
two pilots and has not been run. Same packet parameters (sigma = 9, kappa0 = 0.6, 3 cycles).
"""
import os, sys, time, resource, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from l15_lib import *

phi = 1.2
N = 104; sigma = 9.0; cyc = 3; kap0 = 0.6; x0 = np.array([N // 2] * 3)
dirs = [(1, 0, 0), (-1, 0, 0), (1, 1, 1), (-1, -1, -1), (1, -1, 1), (-1, 1, -1), (2, 1, 1), (3, 1, 1)]
res = {}
t00 = time.process_time(); w0 = time.time()
print("G   N=%d sigma=%.0f cycles=%d kappa0=%.1f phi=%.1f ; velocity in coordinates per cycle" % (N, sigma, cyc, kap0, phi))
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
print("G   direction-odd test, |v(n) + v(-n)|_max:")
for a, b in [((1, 0, 0), (-1, 0, 0)), ((1, 1, 1), (-1, -1, -1))]:
    print("   %s vs %s : %.2e" % (a, b, np.abs(res[a][0] + res[b][0]).max()))
print("G   worst |measured - predicted| over the 8 directions: %.2e" % max(np.abs(r[0] - r[1]).max() for r in res.values()))
print("G   resources: CPU %.0f s, wall %.0f s, peak RSS %.0f MiB" % (time.process_time() - t00, time.time() - w0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))
