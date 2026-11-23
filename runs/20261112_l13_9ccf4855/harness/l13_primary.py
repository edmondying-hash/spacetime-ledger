#!/usr/bin/env python3
"""L1.3 PRIMARY implementation (design sha256 9ccf48559c099289b24af638164ca64b95195872b1e4a0d8966ed44ca800d098).

Written from the Sec. 6.2 text of space-ledger-v2.md on main cc2cc5c8 (sha256 8cbb94ec...6aad70),
lines 525-543 only (hop symbols, S^eps, V^eps(phi), boxed cycle, low-energy limit).
It does NOT import or read the frozen dirac4.py (f71c782e...) or any qca/ module.

Usage: l13_primary.py S0|S1|S2|S3   (run once per step under harness/run_step.sh)

Conventions (paper Sec. 6.2):
  4-component state (psi_R, psi_L); tau_a acts on the (R,L) label, sigma_a inside each Weyl spinor;
  a 4x4 matrix is kron(tau, sigma). k in radians per a/2.
  A^eps = u sigma0 - i n.sigma,  u = cx cy cz - eps sx sy sz,
  n = (sx cy cz + eps cx sy sz, cx sy cz - eps sx cy sz, cx cy sz + eps sx sy cz)
  S^eps = [[nu A, i m 1],[i m 1, nu A^dag]],  nu^2 + m^2 = 1; here m = 0, nu = nu_S = 1.
  X^eps = u tau_x + tau_y (x) (n.sigma);  V^eps(phi) = exp(-i phi X) exp(+i phi tau_x)
        = (cos phi - i sin phi X)(cos phi + i sin phi tau_x)  [X^2 = 1 checked in P2; tau_x^2 = 1]
  U = V^-(phi4) S^- V^+(phi2) S^+,  phi2 = step-2 Wilson angle, phi4 = step-4 Wilson angle (D2).
  omega per layer: eigenvalue of U = exp(-4 i omega), omega = arg(lambda)/(-4).

Pre-declared measurement (design R1): v(kappa) = omega_min(kappa)/kappa, omega_min = min |omega| over the
4 eigenvalues; kappa in {0.0025, 0.005, 0.01, 0.02}; v0 = full Richardson (Neville) extrapolation in
h = kappa^2 to h = 0 through all four points (exact cubic in kappa^2). Lower-order extrapolants are
recorded as diagnostics only.

Pre-declared gating (hard rule 'stop on any failed check'): S0 FAIL (any of P1-P4) -> S1-S3 refuse.
S1 FAIL (R1) -> S2, S3 refuse.  S2 FAIL (R2) -> S3 refuses.  A refusal is recorded, never retried.
Random k: numpy.random.default_rng(20261112 + task_index), uniform in [-pi, pi]^3, task indices fixed below.
"""
import sys, os, json, time, math, platform
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)
OUT = os.path.join(RUN, 'out')
SEED0 = 20261112
TASK = dict(P1=1, P2=2, P4=4, N1_layers=11, N1_U_equal=12, N1_U_pairs=13, S0_timing=20)
TOL_V0 = 1e-6          # design R1/R2, D3 (frozen)
TOL_P1 = 1e-12; TOL_P2 = 1e-13; TOL_P3 = 1e-13; TOL_P4 = 1e-13; TOL_N1 = 1e-12
KAPPAS = [0.0025, 0.005, 0.01, 0.02]

# ---------- Pauli algebra ----------
s0 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
SIG = np.stack([sx, sy, sz])
I4 = np.eye(4, dtype=complex)
TX = np.kron(sx, s0)   # tau_x (x) sigma_0

def hop_symbol(k, eps):
    """u (N,), n (N,3) for k (N,3)."""
    k = np.atleast_2d(np.asarray(k, dtype=float))
    c = np.cos(k); s = np.sin(k)
    cx, cy, cz = c[:, 0], c[:, 1], c[:, 2]
    sx_, sy_, sz_ = s[:, 0], s[:, 1], s[:, 2]
    u = cx*cy*cz - eps*sx_*sy_*sz_
    n = np.stack([sx_*cy*cz + eps*cx*sy_*sz_,
                  cx*sy_*cz - eps*sx_*cy*sz_,
                  cx*cy*sz_ + eps*sx_*sy_*cz], axis=1)
    return u, n

def ndots(n):
    return np.einsum('ni,iab->nab', n.astype(complex), SIG)

def A_sym(k, eps):
    u, n = hop_symbol(k, eps)
    return u[:, None, None]*s0[None] - 1j*ndots(n)

def S_sym(k, eps, m=0.0):
    nu = math.sqrt(1.0 - m*m)
    A = A_sym(k, eps)
    N = A.shape[0]
    S = np.zeros((N, 4, 4), dtype=complex)
    S[:, :2, :2] = nu*A
    S[:, 2:, 2:] = nu*np.conj(np.transpose(A, (0, 2, 1)))
    S[:, :2, 2:] = 1j*m*s0
    S[:, 2:, :2] = 1j*m*s0
    return S

def X_sym(k, eps):
    u, n = hop_symbol(k, eps)
    nd = ndots(n)
    N = u.shape[0]
    X = u[:, None, None]*TX[None]
    X = X + np.einsum('ab,ncd->nacbd', sy, nd).reshape(N, 4, 4)   # tau_y (x) (n.sigma), kron index order
    return X

def V_sym(k, eps, phi):
    X = X_sym(k, eps)
    e1 = math.cos(phi)*I4[None] - 1j*math.sin(phi)*X
    e2 = math.cos(phi)*I4 + 1j*math.sin(phi)*TX
    return e1 @ e2

def U_cycle_primary(k, phi2, phi4, m=0.0):
    return V_sym(k, -1, phi4) @ S_sym(k, -1, m) @ V_sym(k, +1, phi2) @ S_sym(k, +1, m)

def unit_res(M):
    """max over batch of ||M^dag M - I||_inf (max abs row sum) and max abs entry."""
    D = np.conj(np.transpose(M, (0, 2, 1))) @ M - np.eye(M.shape[-1])[None]
    return float(np.max(np.sum(np.abs(D), axis=2))), float(np.max(np.abs(D)))

def rand_k(task, n):
    rng = np.random.default_rng(SEED0 + task)
    return rng.uniform(-np.pi, np.pi, size=(n, 3))

# ---------- directions (13: 3 [100], 6 [110], 4 [111]) ----------
DIRS_INT = [(1,0,0),(0,1,0),(0,0,1),
            (1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1),
            (1,1,1),(1,1,-1),(1,-1,1),(-1,1,1)]
DIRS = np.array([np.array(d, float)/np.linalg.norm(d) for d in DIRS_INT])

def omega_min(k, phi2, phi4):
    U = U_cycle_primary(k, phi2, phi4)
    lam = np.linalg.eigvals(U)
    w = np.angle(lam)/(-4.0)
    return np.min(np.abs(w), axis=1), U

def neville0(h, y):
    """Neville extrapolation to h=0; returns full value and table diagonal (orders 0..n-1, using the n smallest h)."""
    h = list(h); y = list(y)
    n = len(h); P = [list(y)]
    for j in range(1, n):
        row = []
        for i in range(n - j):
            row.append((h[i+j]*P[j-1][i] - h[i]*P[j-1][i+1])/(h[i+j] - h[i]))
        P.append(row)
    return P[-1][0], [P[j][0] for j in range(n)]

def measure_v0(phi2, phi4):
    """For each of 13 directions: v(kappa) at 4 kappas, v0 (Richardson in kappa^2), max unitarity residual."""
    ks = np.concatenate([DIRS*kap for kap in KAPPAS])          # (4*13, 3), kappa-major
    wmin, U = omega_min(ks, phi2, phi4)
    ures = unit_res(U)[0]
    w = wmin.reshape(len(KAPPAS), len(DIRS))
    rows = []
    for d in range(len(DIRS)):
        v = [float(w[i, d]/KAPPAS[i]) for i in range(len(KAPPAS))]
        v0, diag = neville0([kap*kap for kap in KAPPAS], v)
        rows.append(dict(direction=list(DIRS_INT[d]), v_kappa=v, v0=float(v0), richardson_orders=[float(x) for x in diag]))
    return rows, ures

def c0_eq(phi):
    return 0.5*math.sqrt(1.0 + 3.0*math.sin(phi)**2)

def c0_pair(p2, p4):          # formula_used_for_R2 (expected.json, DEV-1)
    return 0.25*math.sqrt((2 + math.sin(p2)**2 + math.sin(p4)**2)**2 + (math.sin(p2)*math.cos(p2) + math.sin(p4)*math.cos(p4))**2)

def c0_pair_literal(p2, p4):  # design line 47 as printed
    return 0.5*math.sqrt((2 + math.sin(p2)**2 + math.sin(p4)**2)**2 + (math.sin(p2)*math.cos(p2) + math.sin(p4)*math.cos(p4))**2)

R1_GRID = [(f"{i/10:.1f}", i/10) for i in range(1, 16)] + [("pi/2", math.pi/2)]
PAPER = {"0.5": "0.650", "0.8": "0.797", "1.0": "0.884", "1.2": "0.949", "1.4": "0.989", "1.5": "0.998", "pi/2": "1.000"}
R2_VALS = [("0.2", 0.2), ("0.5", 0.5), ("0.8", 0.8), ("1.0", 1.0), ("1.2", 1.2), ("1.4", 1.4), ("pi/2", math.pi/2)]

def jdump(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=1)

def status_of(step):
    p = os.path.join(OUT, step, f'result_{step}.json')
    if not os.path.exists(p):
        return None
    return json.load(open(p))['status']

def gate(step):
    need = {'S1': ['S0'], 'S2': ['S0', 'S1'], 'S3': ['S0', 'S1', 'S2']}.get(step, [])
    for s in need:
        st = status_of(s)
        if st != 'PASS':
            return f'refused: prerequisite {s} status {st}'
    return None

# ---------- steps ----------
def S0():
    res = dict(step='S0')
    phis = [p for _, p in R1_GRID]
    # P1: A, S, V unitary at 50 random k, phi in the R1 scan
    k = rand_k(TASK['P1'], 50)
    p1 = dict(A=[], S=[], V=[])
    for eps in (+1, -1):
        p1['A'].append(unit_res(A_sym(k, eps))[0])
        p1['S'].append(unit_res(S_sym(k, eps))[0])
        for ph in phis:
            p1['V'].append(unit_res(V_sym(k, eps, ph))[0])
    p1max = max(max(v) for v in p1.values())
    res['P1'] = dict(n_k=50, phis=phis, max_resid_inf_norm={kk: max(v) for kk, v in p1.items()}, max=p1max, tol=TOL_P1, pass_=p1max <= TOL_P1)
    # P2
    k = rand_k(TASK['P2'], 50)
    r_un = []; r_x = []
    for eps in (+1, -1):
        u, n = hop_symbol(k, eps)
        r_un.append(float(np.max(np.abs(u**2 + np.sum(n**2, axis=1) - 1))))
        X = X_sym(k, eps)
        r_x.append(float(np.max(np.abs(X @ X - I4[None]))))
        r_x.append(float(np.max(np.abs(X - np.conj(np.transpose(X, (0, 2, 1)))))))  # Hermitian
    p2max = max(r_un + r_x)
    res['P2'] = dict(n_k=50, u2_n2_resid=max(r_un), X2_and_hermitian_resid=max(r_x), max=p2max, tol=TOL_P2, pass_=p2max <= TOL_P2)
    # P3
    k0 = np.zeros((1, 3))
    r = []
    for ph in phis:
        for eps in (+1, -1):
            r.append(float(np.max(np.abs(V_sym(k0, eps, ph)[0] - I4))))
        r.append(float(np.max(np.abs(U_cycle_primary(k0, ph, ph)[0] - I4))))
    res['P3'] = dict(phis=phis, max=max(r), tol=TOL_P3, pass_=max(r) <= TOL_P3)
    # P4
    k = rand_k(TASK['P4'], 20)
    G = []
    for perm in [(1,1,0),(1,0,1),(0,1,1)]:
        for sa in (1, -1):
            for sb in (1, -1):
                g = []; it = iter([sa, sb])
                for c in perm:
                    g.append(next(it) if c else 0)
                G.append(tuple(g))
    U0 = U_cycle_primary(k, 1.4, 1.4)
    r = []
    for g in G:
        Ug = U_cycle_primary(k + np.pi*np.array(g, float)[None], 1.4, 1.4)
        r.append(float(np.max(np.abs(Ug - U0))))
    res['P4'] = dict(n_k=20, phi=1.4, shifts=[list(g) for g in G], max=max(r), tol=TOL_P4, pass_=max(r) <= TOL_P4)
    # one timed eigensolve
    kt = rand_k(TASK['S0_timing'], 1)
    Ut = U_cycle_primary(kt, 1.4, 1.4)
    t0 = time.perf_counter(); tc = time.process_time()
    np.linalg.eigvals(Ut)
    t1 = time.perf_counter() - t0; t1c = time.process_time() - tc
    reps = 2000
    Ub = U_cycle_primary(rand_k(TASK['S0_timing'], reps), 1.4, 1.4)
    t0 = time.perf_counter(); np.linalg.eigvals(Ub); tb = (time.perf_counter() - t0)/reps
    n_eig = dict(R1=len(R1_GRID)*13*4, R2=49*13*4, N3_ext=2*13*4)
    n_n1 = None
    res['timing'] = dict(single_eigensolve_wall_s=t1, single_eigensolve_cpu_s=t1c, batched_per_eigensolve_wall_s=tb,
                         eigensolve_counts=n_eig, N1_note='N1 uses matrix products only (no eigensolves): 401 phi x 200 k layers + 401 x 200 U + 41x41 pairs x 200 U',
                         restated_estimate=f"~{sum(n_eig.values())} eigensolves of 4x4 plus ~{(401*200*2+41*41*200)} unitarity checks; estimate seconds per step on one core, well inside 10 min/step and 2 GiB")
    ok = all(res[p]['pass_'] for p in ('P1', 'P2', 'P3', 'P4'))
    res['status'] = 'PASS' if ok else 'FAIL'
    return res

def S1():
    rows = []
    worst = 0.0; worst_spread = 0.0; all_round = True
    for lab, ph in R1_GRID:
        dirs, ures = measure_v0(ph, ph)
        cf = c0_eq(ph)
        v0s = [d['v0'] for d in dirs]
        diffs = [abs(v - cf) for v in v0s]
        spread = max(v0s) - min(v0s)
        row = dict(phi_label=lab, phi=ph, closed_form=cf, v0_min=min(v0s), v0_max=max(v0s), v0_mean=float(np.mean(v0s)),
                   max_abs_diff=max(diffs), direction_spread=spread, U_unitarity_resid=ures,
                   pass_=(max(diffs) <= TOL_V0 and spread <= TOL_V0), per_direction=dirs)
        for d in dirs:
            d['closed_form'] = cf; d['abs_diff'] = abs(d['v0'] - cf)
        if lab in PAPER:
            rr = sorted(set(f"{v:.3f}" for v in v0s))
            row['paper_printed'] = PAPER[lab]; row['v0_rounded_3dp_over_directions'] = rr
            row['rounds_to_paper'] = (rr == [PAPER[lab]])
            all_round = all_round and row['rounds_to_paper']
        rows.append(row)
        worst = max(worst, max(diffs)); worst_spread = max(worst_spread, spread)
    ok = all(r['pass_'] for r in rows)
    mid_ok = all(r['U_unitarity_resid'] <= TOL_N1 for r in rows)
    return dict(step='S1', R1=dict(kappas=KAPPAS, tol=TOL_V0, rows=rows, max_abs_diff=worst, max_direction_spread=worst_spread,
                                   pass_=ok, all_tabulated_round_to_paper=all_round), mid_run_unitarity_ok=mid_ok,
                status='PASS' if (ok and mid_ok) else 'FAIL')

def S2():
    pairs = []
    for l2, p2 in R2_VALS:
        for l4, p4 in R2_VALS:
            dirs, ures = measure_v0(p2, p4)
            cf = c0_pair(p2, p4); cl = c0_pair_literal(p2, p4)
            v0s = [d['v0'] for d in dirs]
            for d in dirs:
                d['closed_form'] = cf; d['abs_diff'] = abs(d['v0'] - cf)
            pairs.append(dict(phi2_label=l2, phi4_label=l4, phi2=p2, phi4=p4, closed_form=cf, closed_form_literal_design_line47=cl,
                              v0_min=min(v0s), v0_max=max(v0s), max_abs_diff=max(abs(v - cf) for v in v0s),
                              max_abs_diff_vs_literal=max(abs(v - cl) for v in v0s), direction_spread=max(v0s) - min(v0s),
                              U_unitarity_resid=ures, pass_=max(abs(v - cf) for v in v0s) <= TOL_V0, per_direction=dirs))
    worst = max(pairs, key=lambda p: p['max_abs_diff'])
    ok = all(p['pass_'] for p in pairs)
    mid_ok = all(p['U_unitarity_resid'] <= TOL_N1 for p in pairs)
    return dict(step='S2', D2_reading='two separate Wilson angles phi2 (step 2, V+) and phi4 (step 4, V-), nu_S = 1 at m = 0',
                R2=dict(n_pairs=len(pairs), tol=TOL_V0, pairs=pairs, max_abs_diff=worst['max_abs_diff'],
                        worst_pair=dict(phi2=worst['phi2_label'], phi4=worst['phi4_label'], max_abs_diff=worst['max_abs_diff']),
                        max_abs_diff_vs_literal=max(p['max_abs_diff_vs_literal'] for p in pairs), pass_=ok),
                mid_run_unitarity_ok=mid_ok, status='PASS' if (ok and mid_ok) else 'FAIL')

def S3():
    res = dict(step='S3')
    # N1: unitarity over a dense grid on [0, pi]
    grid = [math.pi*i/400 for i in range(401)]
    kl = rand_k(TASK['N1_layers'], 200)
    lay = 0.0
    for eps in (+1, -1):
        lay = max(lay, unit_res(A_sym(kl, eps))[0], unit_res(S_sym(kl, eps))[0])
        for ph in grid:
            lay = max(lay, unit_res(V_sym(kl, eps, ph))[0])
    ku = rand_k(TASK['N1_U_equal'], 200)
    ue = max(unit_res(U_cycle_primary(ku, ph, ph))[0] for ph in grid)
    grid41 = [math.pi*i/40 for i in range(41)]
    kp = rand_k(TASK['N1_U_pairs'], 200)
    up = 0.0
    for p2 in grid41:
        for p4 in grid41:
            up = max(up, unit_res(U_cycle_primary(kp, p2, p4))[0])
    n1max = max(lay, ue, up)
    res['N1'] = dict(phi_grid='pi*i/400, i=0..400 (layers and U at phi2=phi4)', pair_grid='pi*i/40 squared (41x41) for U(phi2,phi4)',
                     n_k=200, max_layer_resid=lay, max_U_equal_resid=ue, max_U_pair_resid=up, max=n1max, tol=TOL_N1,
                     holds=n1max <= TOL_N1, note='unitary at every tested phi, so unitarity selects no phi' if n1max <= TOL_N1 else 'a non-unitary point was found')
    # N2: d c0/d phi at 1.4 by central finite difference on the R1 values (1.3 and 1.5)
    r1 = json.load(open(os.path.join(OUT, 'S1', 'result_S1.json')))['R1']['rows']
    byl = {r['phi_label']: r for r in r1}
    fd_dirs = [(byl['1.5']['per_direction'][d]['v0'] - byl['1.3']['per_direction'][d]['v0'])/0.2 for d in range(13)]
    cf_d = 3*math.sin(1.4)*math.cos(1.4)/(2*math.sqrt(1 + 3*math.sin(1.4)**2))
    cf_fd = (c0_eq(1.5) - c0_eq(1.3))/0.2
    res['N2'] = dict(method='central difference (v0(1.5) - v0(1.3))/0.2 on R1 values, per direction',
                     fd_min=min(fd_dirs), fd_max=max(fd_dirs), closed_form_derivative=cf_d, closed_form_same_fd=cf_fd,
                     nonzero_threshold=1e-4, holds=min(abs(x) for x in fd_dirs) > 1e-4,
                     note='threshold 1e-4 >> 1e-5, the largest FD error from the 1e-6 tolerance on two v0 values over 0.2')
    # N3: monotone and range, R1 extended to phi in {0.0, 0.05}
    ext = []
    for lab, ph in [("0.0", 0.0), ("0.05", 0.05)]:
        dirs, ures = measure_v0(ph, ph)
        v0s = [d['v0'] for d in dirs]
        ext.append(dict(phi_label=lab, phi=ph, v0_min=min(v0s), v0_max=max(v0s), closed_form=c0_eq(ph),
                        max_abs_diff=max(abs(v - c0_eq(ph)) for v in v0s), U_unitarity_resid=ures, per_direction=dirs))
    seq = sorted([(e['phi'], e) for e in ext] + [(r['phi'], r) for r in r1], key=lambda t: t[0])
    mono = all(seq[i+1][1]['v0_min'] - seq[i][1]['v0_max'] > TOL_V0 for i in range(len(seq) - 1))
    lo = seq[0][1]; hi = seq[-1][1]
    span_ok = (max(abs(lo['v0_min'] - 0.5), abs(lo['v0_max'] - 0.5)) <= TOL_V0 and max(abs(hi['v0_min'] - 1.0), abs(hi['v0_max'] - 1.0)) <= TOL_V0)
    res['N3'] = dict(extension=ext, phis_sorted=[s[0] for s in seq], v0_min_sorted=[s[1]['v0_min'] for s in seq], v0_max_sorted=[s[1]['v0_max'] for s in seq],
                     strictly_monotone=mono, span_endpoints=dict(phi0=[lo['v0_min'], lo['v0_max']], phi_pi2=[hi['v0_min'], hi['v0_max']]),
                     span_ok=span_ok, holds=mono and span_ok,
                     rule='strict: min over directions at next phi exceeds max at previous phi by > 1e-6; endpoints within 1e-6 of 0.5 and 1')
    # Verdict (design Sec. 4), N5-derivation finding entered separately by the record step (text search, not computed here)
    s1 = json.load(open(os.path.join(OUT, 'S1', 'result_S1.json'))); s2 = json.load(open(os.path.join(OUT, 'S2', 'result_S2.json')))
    r1p = s1['R1']['pass_']; r2p = s2['R2']['pass_']
    comp = dict(R1=r1p, R2=r2p, N1=res['N1']['holds'], N2=res['N2']['holds'], N3=res['N3']['holds'])
    res['verdict_components'] = comp
    res['verdict_before_N5'] = 'PASS' if all(comp.values()) else 'FAIL / OPEN'
    res['verdict_rule'] = 'design Sec. 4: PASS iff R1, R2 pass, N1 holds, N2 and N3 hold; FAIL/OPEN if R1/R2 fail, N1 finds non-unitary phi, or N5 finds a derivation of phi=1.4 from the rule. N4, N5 recorded evidence.'
    res['status'] = 'PASS' if all(r <= TOL_N1 for r in [e['U_unitarity_resid'] for e in ext]) else 'FAIL'
    return res

def main():
    step = sys.argv[1]
    os.makedirs(os.path.join(OUT, step), exist_ok=True)
    path = os.path.join(OUT, step, f'result_{step}.json')
    if os.path.exists(path):
        print('already attempted'); sys.exit(9)
    meta = dict(python=sys.version, numpy=np.__version__, platform=platform.platform(),
                threads={v: os.environ.get(v) for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS')},
                start=time.strftime('%Y-%m-%d %H:%M:%S %Z'))
    g = gate(step)
    if g:
        jdump(dict(step=step, status='REFUSED', reason=g, meta=meta), path); print(g); sys.exit(3)
    t0 = time.perf_counter(); c0 = time.process_time()
    res = {'S0': S0, 'S1': S1, 'S2': S2, 'S3': S3}[step]()
    res['meta'] = meta; res['inner_wall_s'] = time.perf_counter() - t0; res['inner_cpu_s'] = time.process_time() - c0
    jdump(res, path)
    print(json.dumps({k: v for k, v in res.items() if k not in ('R1', 'R2', 'N3')}, default=str)[:4000])
    print('status', res['status'])
    sys.exit(0 if res['status'] == 'PASS' else 4)

if __name__ == '__main__':
    main()
