"""Dry-run B (unscored): 50-digit expansion of the massless band-mean frequency.

omega_bar(kappa n) / kappa = c0 + a1 kappa + a2 kappa^2 + ...  (all powers fitted,
12 points kappa_j = j/500, exact interpolation). xi1' = a1/c0, xi2' = a2/c0, so that
omega = c0 kappa (1 + xi1' kappa + xi2' kappa^2 + ...), the paper's Test 3 form with
E/E_P = kappa.
"""
import json, os, sys
import mpmath as mp
sys.path.insert(0, os.path.dirname(__file__))
from l15_lib import DIR13
mp.mp.dps = 50
I = mp.mpc(0, 1)
def M(r): return mp.matrix(r)
S0 = mp.eye(2); SX = M([[0, 1], [1, 0]]); SY = M([[0, -I], [I, 0]]); SZ = M([[1, 0], [0, -1]]); I4 = mp.eye(4)
def kron(a, b):
    r = mp.zeros(a.rows * b.rows, a.cols * b.cols)
    for i in range(a.rows):
        for j in range(a.cols):
            for p in range(b.rows):
                for q in range(b.cols):
                    r[i * b.rows + p, j * b.cols + q] = a[i, j] * b[p, q]
    return r
T = kron(SX, S0)
def un(e, k):
    kx, ky, kz = k
    cx, cy, cz = mp.cos(kx), mp.cos(ky), mp.cos(kz); sx, sy, sz = mp.sin(kx), mp.sin(ky), mp.sin(kz)
    return cx * cy * cz - e * sx * sy * sz, [sx * cy * cz + e * cx * sy * sz, cx * sy * cz - e * sx * cy * sz, cx * cy * sz + e * sx * sy * cz]
def ns(n): return n[0] * SX + n[1] * SY + n[2] * SZ
def A(e, k, dag=False):
    u, n = un(e, k); return u * S0 + (1 if dag else -1) * I * ns(n)
def S(e, k):
    a, ad = A(e, k), A(e, k, True); r = mp.zeros(4)
    for i in range(2):
        for j in range(2):
            r[i, j] = a[i, j]; r[i + 2, j + 2] = ad[i, j]
    return r
def V(e, k, phi):
    u, n = un(e, k); X = u * T + kron(SY, ns(n))
    return (mp.cos(phi) * I4 - I * mp.sin(phi) * X) * (mp.cos(phi) * I4 + I * mp.sin(phi) * T)
def U(k, phi): return V(-1, k, phi) * S(-1, k) * V(1, k, phi) * S(1, k)
def abs_phases(k, phi):
    E = mp.eig(U(k, phi), left=False, right=False)
    return sorted(abs(mp.arg(e)) for e in E)

KAP = [mp.mpf(j) / 500 for j in range(1, 13)]
VM = mp.matrix([[kk ** j for j in range(12)] for kk in KAP])
def unit(d):
    n = [mp.mpf(x) for x in d]; r = mp.sqrt(sum(x * x for x in n)); return [x / r for x in n]
def coeffs(d, phi):
    n = unit(d); y = []; split = []
    for kk in KAP:
        a = abs_phases([kk * x for x in n], phi)
        y.append(((a[0] + a[2]) / 8) / kk); split.append((a[2] - a[0]) / 4)
    return mp.lu_solve(VM, mp.matrix(y)), split

PHIS = ['0.5', '0.8', '1.0', '1.2', '1.4', '1.5']
q = lambda d: sum(x ** 4 for x in d) / sum(x ** 2 for x in d) ** 2
exp = {}
print("convention: omega = c0 kappa (1 + xi1' kappa + xi2' kappa^2 + ...), kappa = |k| per a/2, E/E_P = kappa (paper Test 3 convention)")
for ph in PHIS:
    phi = mp.mpf(ph); c0 = mp.sqrt(1 + 3 * mp.sin(phi) ** 2) / 2
    worst_c0 = mp.mpf(0); worst_odd = mp.mpf(0); rows = {}
    for d in DIR13:
        for sgn in (1, -1):
            c, sp = coeffs([sgn * x for x in d], phi)
            worst_c0 = max(worst_c0, abs(c[0] - c0)); worst_odd = max(worst_odd, abs(c[1] / c0))
            if sgn == 1: rows[d] = c[2] / c0
    # template xi2' = Aphi + (1/3) q   (B = c0/3  =>  B/c0 = 1/3)
    Aphi = rows[(1, 0, 0)] - mp.mpf(1) / 3
    tmpl = max(abs(rows[d] - (Aphi + q(d) / 3)) for d in DIR13)
    gap = rows[(1, 0, 0)] - rows[(1, 1, 1)]   # xi2'(100) - xi2'(111)
    print("phi=%s  c0=%s" % (ph, mp.nstr(c0, 15)))
    print("   max over 26 signed directions: |a0 - c0| = %s ; |xi1'| = %s" % (mp.nstr(worst_c0, 3), mp.nstr(worst_odd, 3)))
    print("   xi2'[100]=%s  xi2'[110]=%s  xi2'[111]=%s" % tuple(mp.nstr(rows[d], 12) for d in [(1, 0, 0), (1, 1, 0), (1, 1, 1)]))
    print("   template xi2' = A(phi) + q/3 (q = sum n_i^4): A(phi)=%s ; max template residual over 13 directions = %s" % (mp.nstr(Aphi, 12), mp.nstr(tmpl, 3)))
    print("   xi2'[100] - xi2'[111] = %s  (2/9 = %s)" % (mp.nstr(gap, 15), mp.nstr(mp.mpf(2) / 9, 15)))
    exp[ph] = dict(c0=mp.nstr(c0, 20), A_phi=mp.nstr(Aphi, 20), xi2prime={str(list(d)): mp.nstr(rows[d], 20) for d in DIR13})
# band splitting at [111], [100], [110], phi=1.4
phi = mp.mpf('1.4')
print("band splitting (second lowest minus lowest positive frequency), phi=1.4:")
for d in [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 2, 3)]:
    c, sp = coeffs(d, phi)
    e = mp.log(abs(sp[5]) / abs(sp[2])) / mp.log(KAP[5] / KAP[2]) if abs(sp[2]) > mp.mpf(10) ** -40 else None
    print("   ", d, "split at kappa=0.012: %s ; local exponent between kappa=0.006 and 0.012: %s" % (mp.nstr(sp[5], 4), mp.nstr(e, 4) if e is not None else "degenerate"))
json.dump(exp, open(os.path.join(os.path.dirname(__file__), 'expected_pilot.json'), 'w'), indent=1)
