#!/usr/bin/env python3
"""L1.3b MEASUREMENT code (new). Design L1_3b_RUN_DESIGN.md sha256 dc90fd231d9a92602187f61dc68bded2891b3ece5274290ba18b75f86d604a8d.

U-builder: harness/l13_primary.py from run 20261112_l13_9ccf4855 (PR #8), whole-file sha256
5e606a0631b0124992d65f22dd15ffb90e9ad388706c73a9b7739cb388870d8e, used UNCHANGED; only its lines 51-96
(hop_symbol, ndots, A_sym, S_sym, X_sym, V_sym, U_cycle_primary) are called. Everything else here is new.
The frozen dirac4.py (f71c782e...) is imported only in S3, only after out/S3/result_S3_primary.json is written,
as the labelled cross-check (design Sec. 5).

Usage: l13b_measure.py S0|S1|S2|S3   (once per step, under run_step.sh / harness/meter.py)

Measurement (design Sec. 4 line 47): 13 directions; kappa in {0.001,0.002,0.004,0.008,0.016};
v(kappa) = omega_min/kappa, omega = arg(lambda)/(-4), omega_min = min |omega| over the 4 eigenvalues of U_k;
v0 = Neville extrapolation to kappa = 0 in kappa (all powers) through all five kappa (degree 4);
degree 3 (four smallest kappa) diagnostic; b, c = linear and quadratic coefficients of the degree-4 interpolant.
Gating (design Sec. 6 stop rules): S1 needs S0 PASS; S2 needs S0, S1 PASS; S3 needs S0, S1, S2 PASS.
Random k: numpy.random.default_rng(20261112 + task index), uniform in [-pi, pi]^3 (design Sec. 7).
"""
import sys, os, json, time, math, platform, hashlib, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)
OUT = os.path.join(RUN, 'out')
sys.path.insert(0, HERE)
import l13_primary as ub      # U-builder (unchanged file; hash checked in P0 before any use)

EXPECTED = dict(
    design=('design/L1_3b_RUN_DESIGN.md', 'dc90fd231d9a92602187f61dc68bded2891b3ece5274290ba18b75f86d604a8d'),
    paper=('inputs/space-ledger-v2_main_cc2cc5c8.md', '8cbb94ec481b3332f074ea028505478dd2d576a8b5d60915f072b653ab6aad70'),
    u_builder=('harness/l13_primary.py', '5e606a0631b0124992d65f22dd15ffb90e9ad388706c73a9b7739cb388870d8e'),
    frozen_dirac4=('frozen/dirac4.py', 'f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff'),
)
PAPER_COMMIT = 'cc2cc5c8c9b572c68bd1a1f074fdfacbfac4fe32'
SEED0 = 20261112
TASK = dict(P1=1, P2=2, P4=4, N1_layers=11, N1_U_equal=12, N1_U_pairs=13, S0_timing=20)
TOL_V0 = 1e-6; TOL_SPREAD = 1e-6; TOL_B = 1e-6
TOL_P1 = 1e-12; TOL_P2 = 1e-13; TOL_P3 = 1e-13; TOL_P4 = 1e-13; TOL_P5 = 1e-13; TOL_N1 = 1e-12
N2_THRESH = 1e-4; N3_GAP = 1e-6
KAPPAS = [0.001, 0.002, 0.004, 0.008, 0.016]
I4 = np.eye(4, dtype=complex)

DIRS_INT = [(1,0,0),(0,1,0),(0,0,1),
            (1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1),
            (1,1,1),(1,1,-1),(1,-1,1),(-1,1,1)]
DIRS = np.array([np.array(d, float)/np.linalg.norm(d) for d in DIRS_INT])
DIR_CLASS = ['100']*3 + ['110']*6 + ['111']*4

R1_GRID = [(f"{i/10:.1f}", i/10) for i in range(1, 16)] + [("pi/2", math.pi/2)]
PAPER = {"0.5": "0.650", "0.8": "0.797", "1.0": "0.884", "1.2": "0.949", "1.4": "0.989", "1.5": "0.998", "pi/2": "1.000"}
R2_VALS = [("0.2", 0.2), ("0.5", 0.5), ("0.8", 0.8), ("1.0", 1.0), ("1.2", 1.2), ("1.4", 1.4), ("pi/2", math.pi/2)]
P5_EQ = [0.5, 0.8, 1.0, 1.2, 1.4, 1.5, math.pi/2]
P5_SYM = [(0.5, 1.3), (0.2, 1.4), (0.8, math.pi/2), (1.0, 1.2), (0.2, 0.5)]

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def jdump(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=1)

# ---------- closed forms (expected.json) ----------
def c0_eq(phi):
    return 0.5*math.sqrt(1.0 + 3.0*math.sin(phi)**2)

def c0_pair(p2, p4):
    return 0.25*math.sqrt((2 + math.sin(p2)**2 + math.sin(p4)**2)**2 + (math.sin(p2)*math.cos(p2) + math.sin(p4)*math.cos(p4))**2)

def dc0_eq(phi):
    return 3*math.sin(phi)*math.cos(phi)/(2*math.sqrt(1 + 3*math.sin(phi)**2))

# ---------- helpers ----------
def unit_res(M):
    D = np.conj(np.transpose(M, (0, 2, 1))) @ M - np.eye(M.shape[-1])[None]
    return float(np.max(np.sum(np.abs(D), axis=2)))

def rand_k(task, n):
    return np.random.default_rng(SEED0 + task).uniform(-np.pi, np.pi, size=(n, 3))

def neville0(x, y):
    """Neville extrapolation of the interpolating polynomial through (x_i, y_i) to x = 0."""
    x = list(x); P = list(y); n = len(x)
    for j in range(1, n):
        P = [(x[i+j]*P[i] - x[i]*P[i+1])/(x[i+j] - x[i]) for i in range(n - j)]
    return P[0]

def poly_coeffs(x, y):
    """Coefficients a0..a_{n-1} of the interpolating polynomial in x (solved in scaled variable x/x_max)."""
    x = np.asarray(x, float); s = x.max(); t = x/s
    V = np.vander(t, len(t), increasing=True)
    a = np.linalg.solve(V, np.asarray(y, float))
    return [float(a[i]/s**i) for i in range(len(a))]

def measure(phi2, phi4):
    ks = np.concatenate([DIRS*kap for kap in KAPPAS])            # kappa-major (5*13, 3)
    U = ub.U_cycle_primary(ks, phi2, phi4)
    lam = np.linalg.eigvals(U)
    w = np.angle(lam)/(-4.0)
    wmin = np.min(np.abs(w), axis=1).reshape(len(KAPPAS), len(DIRS))
    rows = []
    for d in range(len(DIRS)):
        v = [float(wmin[i, d]/KAPPAS[i]) for i in range(len(KAPPAS))]
        v0 = float(neville0(KAPPAS, v))
        v0_d3 = float(neville0(KAPPAS[:4], v[:4]))
        a = poly_coeffs(KAPPAS, v)
        rows.append(dict(direction=list(DIRS_INT[d]), dir_class=DIR_CLASS[d], v_kappa=v, v0=v0, v0_degree3=v0_d3,
                         poly_a0=a[0], b=a[1], c=a[2], poly_a3=a[3], poly_a4=a[4]))
    return rows, unit_res(U)

def status_of(step):
    p = os.path.join(OUT, step, f'result_{step}.json')
    return json.load(open(p))['status'] if os.path.exists(p) else None

def gate(step):
    for s in {'S1': ['S0'], 'S2': ['S0', 'S1'], 'S3': ['S0', 'S1', 'S2']}.get(step, []):
        st = status_of(s)
        if st != 'PASS':
            return f'refused: prerequisite {s} status {st} (design Sec. 6 stop rule)'
    return None

# ---------- S0: P0-P5 + timed eigensolve ----------
def S0():
    res = dict(step='S0')
    p0 = {}
    for key, (rel, exp) in EXPECTED.items():
        got = sha(os.path.join(RUN, rel)); p0[key] = dict(file=rel, sha256=got, expected=exp, match=(got == exp))
    ubsrc = open(os.path.join(RUN, 'harness/l13_primary.py'), 'rb').read().split(b'\n')
    p0['u_builder_lines_51_96_sha256'] = hashlib.sha256(b'\n'.join(ubsrc[50:96]) + b'\n').hexdigest()
    seg = ubsrc[50:96]
    p0['u_builder_lines_51_96_first_last'] = [seg[0].decode(), seg[-1].decode()] if seg else []
    p0['measurement_code'] = dict(file='harness/l13b_measure.py', sha256=sha(os.path.abspath(__file__)))
    p0['paper_commit'] = PAPER_COMMIT
    p0['pass_'] = all(p0[k]['match'] for k in EXPECTED)
    res['P0'] = p0
    if not p0['pass_']:
        res['status'] = 'FAIL'; res['note'] = 'P0 failed; P1-P5 not run'; return res
    phis = [p for _, p in R1_GRID] + [0.0, 0.05, 0.2]
    k = rand_k(TASK['P1'], 50)
    p1 = dict(A=0.0, S=0.0, V=0.0)
    for eps in (+1, -1):
        p1['A'] = max(p1['A'], unit_res(ub.A_sym(k, eps)))
        p1['S'] = max(p1['S'], unit_res(ub.S_sym(k, eps)))
        for ph in phis:
            p1['V'] = max(p1['V'], unit_res(ub.V_sym(k, eps, ph)))
    m1 = max(p1.values())
    res['P1'] = dict(n_k=50, phis=phis, max_resid_inf_norm=p1, max=m1, tol=TOL_P1, pass_=m1 <= TOL_P1)
    k = rand_k(TASK['P2'], 50); r_un = []; r_x = []
    for eps in (+1, -1):
        u, n = ub.hop_symbol(k, eps)
        r_un.append(float(np.max(np.abs(u**2 + np.sum(n**2, axis=1) - 1))))
        X = ub.X_sym(k, eps)
        r_x.append(float(np.max(np.abs(X @ X - I4[None]))))
    m2 = max(r_un + r_x)
    res['P2'] = dict(n_k=50, u2_n2_resid=max(r_un), X2_resid=max(r_x), max=m2, tol=TOL_P2, pass_=m2 <= TOL_P2)
    k0 = np.zeros((1, 3)); r = []
    for ph in phis:
        for eps in (+1, -1):
            r.append(float(np.max(np.abs(ub.V_sym(k0, eps, ph)[0] - I4))))
        r.append(float(np.max(np.abs(ub.U_cycle_primary(k0, ph, ph)[0] - I4))))
    for _, p2 in R2_VALS:
        for _, p4 in R2_VALS:
            r.append(float(np.max(np.abs(ub.U_cycle_primary(k0, p2, p4)[0] - I4))))
    res['P3'] = dict(phis=phis, pairs='R2b 7x7 grid', max=max(r), tol=TOL_P3, pass_=max(r) <= TOL_P3)
    k = rand_k(TASK['P4'], 20)
    G = [(1,1,0),(1,-1,0),(-1,1,0),(-1,-1,0),(1,0,1),(1,0,-1),(-1,0,1),(-1,0,-1),(0,1,1),(0,1,-1),(0,-1,1),(0,-1,-1)]
    U0 = ub.U_cycle_primary(k, 1.4, 1.4)
    r = [float(np.max(np.abs(ub.U_cycle_primary(k + np.pi*np.array(g, float)[None], 1.4, 1.4) - U0))) for g in G]
    res['P4'] = dict(n_k=20, phi=1.4, shifts=[list(g) for g in G], max=max(r), tol=TOL_P4, pass_=max(r) <= TOL_P4)
    d5 = []
    for ph in P5_EQ:
        d5.append(dict(case='c0(phi,phi) vs 0.5 sqrt(1+3 sin^2 phi)', phi=ph, diff=abs(c0_pair(ph, ph) - c0_eq(ph))))
    d5.append(dict(case='c0(0,0) vs 0.5', diff=abs(c0_pair(0.0, 0.0) - 0.5)))
    d5.append(dict(case='c0(pi/2,pi/2) vs 1', diff=abs(c0_pair(math.pi/2, math.pi/2) - 1.0)))
    for a, b in P5_SYM:
        d5.append(dict(case='c0(phi2,phi4) vs c0(phi4,phi2)', pair=[a, b], diff=abs(c0_pair(a, b) - c0_pair(b, a))))
    m5 = max(x['diff'] for x in d5)
    res['P5'] = dict(checks=d5, max=m5, tol=TOL_P5, pass_=m5 <= TOL_P5)
    kt = rand_k(TASK['S0_timing'], 1); Ut = ub.U_cycle_primary(kt, 1.4, 1.4)
    t0 = time.perf_counter(); tc = time.process_time(); np.linalg.eigvals(Ut)
    t1 = time.perf_counter() - t0; t1c = time.process_time() - tc
    reps = 2000; Ub = ub.U_cycle_primary(rand_k(TASK['S0_timing'], reps), 1.4, 1.4)
    t0 = time.perf_counter(); np.linalg.eigvals(Ub); tb = (time.perf_counter() - t0)/reps
    n_eig = dict(R1prime=len(R1_GRID)*13*5, R2b=49*13*5, N3_ext=2*13*5)
    res['timing'] = dict(single_eigensolve_wall_s=t1, single_eigensolve_cpu_s=t1c, batched_per_eigensolve_wall_s=tb, eigensolve_counts=n_eig,
                         restated_estimate=f"~{sum(n_eig.values())} 4x4 eigensolves (~{sum(n_eig.values())*t1:.3f} s at the single-solve time) plus N1 (~{401*200*2+41*41*200} unitarity checks) and the cross-check ({49*65+16*65} frozen builds); seconds per step on one core, well inside 10 min/step and 2 GiB")
    res['status'] = 'PASS' if all(res[p]['pass_'] for p in ('P0', 'P1', 'P2', 'P3', 'P4', 'P5')) else 'FAIL'
    return res

# ---------- S1: R1' ----------
def S1():
    rows = []
    for lab, ph in R1_GRID:
        dirs, ures = measure(ph, ph)
        cf = c0_eq(ph)
        for d in dirs:
            d['closed_form'] = cf; d['abs_diff'] = abs(d['v0'] - cf); d['abs_diff_degree3'] = abs(d['v0_degree3'] - cf)
        v0s = [d['v0'] for d in dirs]
        md = max(d['abs_diff'] for d in dirs); sp = max(v0s) - min(v0s)
        row = dict(phi_label=lab, phi=ph, closed_form=cf, v0_min=min(v0s), v0_max=max(v0s), max_abs_diff=md,
                   max_abs_diff_degree3=max(d['abs_diff_degree3'] for d in dirs), direction_spread=sp,
                   max_abs_b=max(abs(d['b']) for d in dirs), U_unitarity_resid=ures, per_direction=dirs)
        row['within_tol'] = (md <= TOL_V0 and sp <= TOL_SPREAD)
        if lab in PAPER:
            rr = sorted(set(f"{v:.3f}" for v in v0s))
            row['paper_printed'] = PAPER[lab]; row['v0_rounded_3dp_over_directions'] = rr; row['rounds_to_paper'] = (rr == [PAPER[lab]])
        row['pass_'] = row['within_tol'] and row.get('rounds_to_paper', True)
        rows.append(row)
    ok = all(r['pass_'] for r in rows)
    R = dict(kappas=KAPPAS, tol_abs=TOL_V0, tol_spread=TOL_SPREAD, rows=rows,
             max_abs_diff=max(r['max_abs_diff'] for r in rows), max_direction_spread=max(r['direction_spread'] for r in rows),
             max_abs_diff_degree3=max(r['max_abs_diff_degree3'] for r in rows),
             all_tabulated_round_to_paper=all(r['rounds_to_paper'] for r in rows if 'rounds_to_paper' in r),
             max_U_unitarity_resid=max(r['U_unitarity_resid'] for r in rows), pass_=ok)
    return dict(step='S1', R1prime=R, status='PASS' if ok else 'FAIL')

# ---------- S2: R2b + R2c ----------
def S2():
    pairs = []
    for l2, p2 in R2_VALS:
        for l4, p4 in R2_VALS:
            dirs, ures = measure(p2, p4)
            cf = c0_pair(p2, p4)
            for d in dirs:
                d['closed_form'] = cf; d['abs_diff'] = abs(d['v0'] - cf); d['abs_diff_degree3'] = abs(d['v0_degree3'] - cf)
            v0s = [d['v0'] for d in dirs]
            md = max(d['abs_diff'] for d in dirs); sp = max(v0s) - min(v0s)
            pairs.append(dict(phi2_label=l2, phi4_label=l4, phi2=p2, phi4=p4, diagonal=(l2 == l4), closed_form=cf,
                              v0_min=min(v0s), v0_max=max(v0s), max_abs_diff=md, max_abs_diff_degree3=max(d['abs_diff_degree3'] for d in dirs),
                              direction_spread=sp, U_unitarity_resid=ures, pass_=(md <= TOL_V0 and sp <= TOL_SPREAD), per_direction=dirs))
    ok = all(p['pass_'] for p in pairs)
    worst = max(pairs, key=lambda p: p['max_abs_diff']); worst_sp = max(pairs, key=lambda p: p['direction_spread'])
    R2b = dict(n_pairs=len(pairs), kappas=KAPPAS, tol_abs=TOL_V0, tol_spread=TOL_SPREAD, pairs=pairs,
               max_abs_diff=worst['max_abs_diff'], worst_pair=[worst['phi2_label'], worst['phi4_label']],
               max_direction_spread=worst_sp['direction_spread'], worst_spread_pair=[worst_sp['phi2_label'], worst_sp['phi4_label']],
               max_abs_diff_degree3=max(p['max_abs_diff_degree3'] for p in pairs), pairs_passing=sum(p['pass_'] for p in pairs),
               max_U_unitarity_resid=max(p['U_unitarity_resid'] for p in pairs), pass_=ok)
    table = [dict(phi2=p['phi2_label'], phi4=p['phi4_label'], direction=d['direction'], dir_class=d['dir_class'], b=d['b'], c=d['c'])
             for p in pairs for d in p['per_direction']]
    q1 = max(abs(t['b']) for t in table if t['dir_class'] == '100')
    q2 = max(abs(t['b']) for t in table if t['phi2'] == t['phi4'])
    R2c = dict(note='record only; not in the verdict (design Sec. 4 R2c)', table=table,
               Q1=dict(statement='|b| <= 1e-6 on the three [100] directions for every pair (replication, not prediction)', max_abs_b=q1, tol=TOL_B, pass_=q1 <= TOL_B),
               Q2=dict(statement='|b| <= 1e-6 at every diagonal pair phi2 = phi4 (replication, not prediction)', max_abs_b=q2, tol=TOL_B, pass_=q2 <= TOL_B),
               max_abs_b_all=max(abs(t['b']) for t in table), max_abs_c_all=max(abs(t['c']) for t in table))
    return dict(step='S2', R2b=R2b, R2c=R2c, status='PASS' if ok else 'FAIL')

# ---------- S3: N1-N3, N4, N5, cross-check, result.json ----------
N5_FILES = [('inputs/space-ledger-v2_main_cc2cc5c8.md', (419, 626), 'paper Sec. 6.2 (lines 419-626)'),
            ('inputs/plans/layered_plan_v3.3_r2.md', None, 'plan v3.3 r2'),
            ('inputs/l1_1/REASON_L1_1_one_BCC.md', None, 'L1.1 reason note r1'),
            ('inputs/l1_1/REASON_L1_1_one_BCC_r2.md', None, 'L1.1 reason note r2'),
            ('inputs/l1_1/REPAIR_SPEC_L1_1_r8.md', None, 'L1.1 repair spec r8'),
            ('inputs/l1_1/L1_1_repair_spec_r8_20261111_SIGNOFF.txt', None, 'L1.1 r8 sign-off')]
N5_HIT = re.compile(r'(?<![\d.])1\.4(?!\d)')
N5_ANGLE = re.compile(r'varphi|\\phi|φ|phi|Wilson angle', re.I)
N5_FLAG = re.compile(r'deriv|determin|fixed by|fixes|select|forced|required by|unique|predict', re.I)

def S3():
    res = dict(step='S3')
    grid = [math.pi*i/400 for i in range(401)]
    kl = rand_k(TASK['N1_layers'], 200); lay = 0.0
    for eps in (+1, -1):
        lay = max(lay, unit_res(ub.A_sym(kl, eps)), unit_res(ub.S_sym(kl, eps)))
        for ph in grid:
            lay = max(lay, unit_res(ub.V_sym(kl, eps, ph)))
    ku = rand_k(TASK['N1_U_equal'], 200)
    ue = max(unit_res(ub.U_cycle_primary(ku, ph, ph)) for ph in grid)
    grid41 = [math.pi*i/40 for i in range(41)]
    kp = rand_k(TASK['N1_U_pairs'], 200)
    up = max(unit_res(ub.U_cycle_primary(kp, a, b)) for a in grid41 for b in grid41)
    n1 = max(lay, ue, up)
    res['N1'] = dict(phi_grid='pi*i/400, i=0..400 (each layer A, S, V; and U at phi2=phi4)', pair_grid='pi*i/40, 41x41 (U(phi2,phi4))', n_k=200,
                     max_layer_resid=lay, max_U_equal_resid=ue, max_U_pair_resid=up, max=n1, tol=TOL_N1, holds=n1 <= TOL_N1)
    s1 = json.load(open(os.path.join(OUT, 'S1', 'result_S1.json')))
    byl = {r['phi_label']: r for r in s1['R1prime']['rows']}
    fd = [(byl['1.5']['per_direction'][d]['v0'] - byl['1.3']['per_direction'][d]['v0'])/0.2 for d in range(13)]
    res['N2'] = dict(method='central difference (v0(1.5) - v0(1.3))/0.2 on the R1prime v0, per direction', fd_per_direction=fd,
                     fd_min=min(fd), fd_max=max(fd), closed_form_derivative_at_1p4=dc0_eq(1.4), design_quoted=0.127,
                     closed_form_same_fd=(c0_eq(1.5) - c0_eq(1.3))/0.2, max_abs_fd_minus_closed_form_fd=max(abs(x - (c0_eq(1.5) - c0_eq(1.3))/0.2) for x in fd),
                     nonzero_threshold=N2_THRESH, holds=min(abs(x) for x in fd) > N2_THRESH)
    ext = []
    for lab, ph in [("0.0", 0.0), ("0.05", 0.05)]:
        dirs, ures = measure(ph, ph); v0s = [d['v0'] for d in dirs]
        ext.append(dict(phi_label=lab, phi=ph, v0_min=min(v0s), v0_max=max(v0s), closed_form=c0_eq(ph),
                        max_abs_diff=max(abs(v - c0_eq(ph)) for v in v0s), U_unitarity_resid=ures, per_direction=dirs))
    seq = sorted([(e['phi'], e['phi_label'], e['v0_min'], e['v0_max']) for e in ext] +
                 [(r['phi'], r['phi_label'], r['v0_min'], r['v0_max']) for r in s1['R1prime']['rows']])
    gaps = [seq[i+1][2] - seq[i][3] for i in range(len(seq) - 1)]
    mono = all(g > N3_GAP for g in gaps)
    lo, hi = seq[0], seq[-1]
    span_ok = (lo[1] == '0.0' and hi[1] == 'pi/2' and max(abs(lo[2] - 0.5), abs(lo[3] - 0.5)) <= TOL_V0 and max(abs(hi[2] - 1.0), abs(hi[3] - 1.0)) <= TOL_V0)
    res['N3'] = dict(extension=ext, sequence=[dict(phi=s[0], label=s[1], v0_min=s[2], v0_max=s[3]) for s in seq], min_gap=min(gaps),
                     strictly_monotone=mono, span_endpoints=dict(phi0=[lo[2], lo[3]], phi_pi2=[hi[2], hi[3]]), span_ok=span_ok, holds=mono and span_ok,
                     rule='strict: v0_min at next phi exceeds v0_max at previous phi by > 1e-6 over all directions; endpoints within 1e-6 of 0.5 (phi=0) and 1 (phi=pi/2); with continuity this gives each target in [0.5,1] exactly one phi')
    rj = os.path.join(RUN, 'inputs/V5v2_census_results.json')
    n4 = dict(source='inputs/V5v2_census_results.json', sha256=sha(rj), expected_sha256='ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708')
    try:
        row = json.load(open(rj))['regenerate'][5]['rows'][6]
        n4.update(json_path='/regenerate/5/rows/6', phi=row.get('phi'), phi_label=row.get('phi_label'),
                  gap_cell=row.get('cells', {}).get('gap'), light_speed_cell=row.get('cells', {}).get('light_speed'))
    except Exception as ex:
        n4['read_error'] = repr(ex)
    n4.update(closed_form_c0_pi2=c0_eq(math.pi/2), note='cited, not re-run; speed 1 needs phi = pi/2, where the doublers return (gap ~0): a trade-off, not a selection of 1.4')
    res['N4'] = n4
    hits = []
    for rel, rng, label in N5_FILES:
        p = os.path.join(RUN, rel)
        lines = open(p, encoding='utf-8').read().split('\n')
        for i, line in enumerate(lines, 1):
            if rng and not (rng[0] <= i <= rng[1]):
                continue
            if N5_HIT.search(line) and N5_ANGLE.search(line):
                hits.append(dict(file=rel, file_sha256=sha(p), where=label, line=i, text=line, flag_keyword=bool(N5_FLAG.search(line))))
    res['N5'] = dict(rule="lines containing '1.4' (not part of a longer number) and an angle word (varphi/phi/φ/Wilson angle); flag_keyword marks lines with derive/determine/fixed by/fixes/select/forced/required by/unique/predict for manual reading",
                     files=[dict(file=f, scope=l) for f, _, l in N5_FILES], n_hits=len(hits), n_flagged=sum(h['flag_keyword'] for h in hits), hits=hits,
                     classification='done by the post-run record after reading each flagged hit verbatim (not computed here)')
    s2 = json.load(open(os.path.join(OUT, 'S2', 'result_S2.json')))
    comp = dict(R1prime=s1['R1prime']['pass_'], R2b=s2['R2b']['pass_'], N1=res['N1']['holds'], N2=res['N2']['holds'], N3=res['N3']['holds'])
    res['verdict_components'] = comp
    res['verdict_before_N5_classification'] = 'PASS' if all(comp.values()) else 'FAIL / OPEN'
    res['status'] = 'PASS'
    os.makedirs(os.path.join(OUT, 'S3'), exist_ok=True)
    jdump(res, os.path.join(OUT, 'S3', 'result_S3_primary.json'))       # primary written before the cross-check
    # ---- labelled cross-check against the frozen module (after primary is written) ----
    fz = os.path.join(RUN, 'frozen', 'dirac4.py')
    xc = dict(frozen='frozen/dirac4.py', sha256_at_import=sha(fz), expected=EXPECTED['frozen_dirac4'][1])
    if xc['sha256_at_import'] == xc['expected']:
        import importlib.util
        spec = importlib.util.spec_from_file_location('dirac4_frozen', fz); d4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(d4)
        ks = np.concatenate([DIRS*kap for kap in KAPPAS])
        mx_pair = 0.0; mx_cyc = 0.0; mx_v0 = 0.0
        s2pairs = {(p['phi2_label'], p['phi4_label']): p for p in s2['R2b']['pairs']}
        for l2, p2 in R2_VALS:
            for l4, p4 in R2_VALS:
                Up = ub.U_cycle_primary(ks, p2, p4)
                Uf = np.array([d4.V_step(-1, k, p4) @ d4.S_step(-1, k) @ d4.V_step(+1, k, p2) @ d4.S_step(+1, k) for k in ks])
                mx_pair = max(mx_pair, float(np.max(np.abs(Up - Uf))))
                w = np.min(np.abs(np.angle(np.linalg.eigvals(Uf))/(-4.0)), axis=1).reshape(len(KAPPAS), len(DIRS))
                for d in range(13):
                    v0f = neville0(KAPPAS, [w[i, d]/KAPPAS[i] for i in range(len(KAPPAS))])
                    mx_v0 = max(mx_v0, abs(v0f - s2pairs[(l2, l4)]['per_direction'][d]['v0']))
                if l2 == l4:
                    Uc = np.array([d4.U_cycle(k, phi=p2) for k in ks]); mx_cyc = max(mx_cyc, float(np.max(np.abs(Up - Uc))))
        for lab, ph in R1_GRID:
            Up = ub.U_cycle_primary(ks, ph, ph); Uc = np.array([d4.U_cycle(k, phi=ph) for k in ks])
            mx_cyc = max(mx_cyc, float(np.max(np.abs(Up - Uc))))
        xc.update(max_abs_U_diff_pairs_frozen_layers=mx_pair, max_abs_U_diff_frozen_U_cycle_equal_angles=mx_cyc,
                  max_abs_v0_diff_R2b_grid=mx_v0,
                  method='49 R2b pairs x 13 directions x 5 kappa: frozen V_step(-1,k,phi4) S_step(-1,k) V_step(+1,k,phi2) S_step(+1,k) (frozen U_cycle takes one phi; same order as U_cycle); diagonal pairs and the 16 R1prime phi also through frozen U_cycle(k, phi) directly')
    else:
        xc['status'] = 'NOT RUN: frozen hash mismatch at import'
    res['cross_check'] = xc
    assemble_result(res, s1, s2)
    return res

def assemble_result(s3, s1, s2):
    """result.json (design Sec. 7). S3's own meter resources are written after this file (logs/resources_S3.json)."""
    s0 = json.load(open(os.path.join(OUT, 'S0', 'result_S0.json')))
    resources = {}
    for st in ('S0', 'S1', 'S2'):
        rp = os.path.join(RUN, 'logs', f'resources_{st}.json')
        resources[st] = json.load(open(rp)) if os.path.exists(rp) else None
    resources['S3'] = 'logs/resources_S3.json (written by harness/meter.py after this file)'
    r = dict(run='20261112_l13b_dc90fd23', written=time.strftime('%Y-%m-%d %H:%M:%S %Z'),
             code_version=dict(design_sha256=EXPECTED['design'][1], u_builder=dict(file='harness/l13_primary.py', sha256=s0['P0']['u_builder']['sha256'],
                               lines_51_96_sha256=s0['P0']['u_builder_lines_51_96_sha256'], origin='run 20261112_l13_9ccf4855, PR #8, unchanged'),
                               measurement_code=s0['P0']['measurement_code'], frozen_module=dict(file='frozen/dirac4.py', sha256=EXPECTED['frozen_dirac4'][1], used='S3 cross-check only'),
                               paper=dict(commit=PAPER_COMMIT, sha256=EXPECTED['paper'][1])),
             seed='none random in R1prime/R2b/R2c/N3; P1/P2/P4/N1/timing k from numpy.random.default_rng(20261112 + task index): ' + json.dumps(TASK),
             grid=dict(R1prime=[l for l, _ in R1_GRID], R2b=[l for l, _ in R2_VALS] , N3_extension=['0.0', '0.05'], kappas=KAPPAS, directions=DIRS_INT),
             boundary='periodic symbol, one BCC orbit; no real-space run', units='omega per layer; speeds in hop-rate units',
             load_rule='none, Sec. 6.2 vacuum symbol', m=0,
             caps=dict(memory='2 GiB (address-space ulimit 2 GiB in run_step.sh)', threads='1 pinned', gpu='none', wall='30 min total / 10 min per step', output='64 MiB', attempts='one per step'),
             resources=resources, preflight={k: s0[k] for k in ('P0', 'P1', 'P2', 'P3', 'P4', 'P5')}, timing=s0['timing'],
             R1prime=s1['R1prime'], R2b=s2['R2b'], R2c=s2['R2c'],
             R3={k: s3[k] for k in ('N1', 'N2', 'N3', 'N4', 'N5')}, cross_check=s3['cross_check'],
             verdict_components=s3['verdict_components'], verdict_before_N5_classification=s3['verdict_before_N5_classification'],
             raw_logs='logs/', frozen_design_sha256=EXPECTED['design'][1],
             previous_run='20261112_l13_9ccf4855 (PR #8, commit f4e45728, SHA256SUMS 17f5e19944dd36a7b257854951e5a4c594515d71dedd8e4a0d43da6f139e6157); R2 FAIL/OPEN as recorded, unaltered')
    jdump(r, os.path.join(RUN, 'result.json'))

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
    big = ('R1prime', 'R2b', 'R2c', 'N3', 'N5')
    print(json.dumps({k: v for k, v in res.items() if k not in big}, default=str)[:6000])
    print('status', res['status'])
    sys.exit(0 if res['status'] == 'PASS' else 4)

if __name__ == '__main__':
    main()
