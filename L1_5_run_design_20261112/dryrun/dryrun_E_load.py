"""Dry-run E (unscored): congestion ON for dirac4, two declared uniform-load implementations.

Rule A (paper load-first, uniform clock potential U0): the whole cycle is slowed, U_A = U^g,
  g = f^2 = exp(-2 U0), set equal to s for comparability, U0 = -(1/2) ln s.
Rule B (OP4-style, uniform node load l0): every rotation angle (bond angle and on-site clock
  phase) is scaled by s = (1 + l0)^(-1/2): each of S^+, V^+, S^-, V^- is replaced by its s-th
  power (principal branch), U_B = V^-^s S^-^s V^+^s S^+^s.
Both reduce to the unloaded cycle at s = 1. Same fit as dry-run B (50 digits, 12 points).
"""
import json, os, sys
import mpmath as mp
sys.path.insert(0, os.path.dirname(__file__))
from l15_lib import DIR13
src = open(os.path.join(os.path.dirname(__file__), 'dryrun_B_mp_expansion.py')).read().split("KAP = ")[0]
ns = {'__file__': os.path.join(os.path.dirname(__file__), 'dryrun_B_mp_expansion.py')}
exec(src, ns)
mp.mp.dps = 50
Sf, Vf = ns['S'], ns['V']

def fpow(Mx, g):
    E, ER = mp.eig(Mx)
    return ER * mp.diag([mp.exp(g * mp.log(e)) for e in E]) * mp.inverse(ER)

def U_load(k, phi, g, rule):
    Sp, Sm, Vp, Vm = Sf(1, k), Sf(-1, k), Vf(1, k, phi), Vf(-1, k, phi)
    if rule == 'B':
        return fpow(Vm, g) * fpow(Sm, g) * fpow(Vp, g) * fpow(Sp, g)
    return fpow(Vm * Sm * Vp * Sp, g)

def abs_phases(k, phi, g, rule):
    E = mp.eig(U_load(k, phi, g, rule), left=False, right=False)
    return sorted(abs(mp.arg(e)) for e in E)

KAP = [mp.mpf(j) / 500 for j in range(1, 13)]
VM = mp.matrix([[kk ** j for j in range(12)] for kk in KAP])
def coeffs(d, phi, g, rule):
    r = mp.sqrt(sum(x * x for x in d)); n = [mp.mpf(x) / r for x in d]; y = []
    for kk in KAP:
        a = abs_phases([kk * x for x in n], phi, g, rule); y.append(((a[0] + a[2]) / 8) / kk)
    return mp.lu_solve(VM, mp.matrix(y))

q = lambda d: sum(x ** 4 for x in d) / sum(x ** 2 for x in d) ** 2
out = {}
for rule in ('A', 'B'):
    for l0 in ('0.5', '2.0'):
        s = (1 + mp.mpf(l0)) ** mp.mpf(-0.5)
        worst_xi1 = worst_a3 = worst_a0 = worst_a2dev = mp.mpf(0); maxxi2 = mp.mpf(0)
        rows = {}
        for ph in ('0.5', '0.8', '1.0', '1.2', '1.4', '1.5'):
            phi = mp.mpf(ph); c0 = mp.sqrt(1 + 3 * mp.sin(phi) ** 2) / 2
            s2 = mp.sin(phi) ** 2; c2 = mp.cos(phi) ** 2
            for d in DIR13:
                for sg in (1, -1):
                    c = coeffs([sg * x for x in d], phi, s, rule)
                    worst_a0 = max(worst_a0, abs(c[0] - s * c0))
                    worst_xi1 = max(worst_xi1, abs(c[1] / c[0])); worst_a3 = max(worst_a3, abs(c[3] / c[0]))
                    if sg == 1:
                        xi2 = c[2] / c[0]; maxxi2 = max(maxxi2, abs(xi2)); rows[(ph, d)] = xi2
                        pred = -(1 - q(d)) / 3 - mp.mpf(3) / 8 * s2 * c2 / (1 + 3 * s2)
                        worst_a2dev = max(worst_a2dev, abs(xi2 - pred))
        print("rule %s  l0=%s  s=%s : max|a0 - s c0| = %s ; max|xi1'| = %s ; max|a3/a0| = %s ; max|xi2'| = %s ; max|xi2' - unloaded closed form| = %s"
              % (rule, l0, mp.nstr(s, 8), mp.nstr(worst_a0, 3), mp.nstr(worst_xi1, 3), mp.nstr(worst_a3, 3), mp.nstr(maxxi2, 8), mp.nstr(worst_a2dev, 3)), flush=True)
        out["%s_%s" % (rule, l0)] = {"%s|%s" % (k[0], list(k[1])): mp.nstr(v, 20) for k, v in rows.items()}
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'expected_pilot_load.json'), 'w'), indent=0)
