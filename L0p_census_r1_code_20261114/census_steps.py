"""L0' census r1: step implementations S0-S7 (one subprocess per step).
Design: L0P_CENSUS_DESIGN_r1.md sha256 c2673a6426ca5728738c7e7e63871bd26577e8475e9b2819d9980aeccb642fd1
"""
import os, sys, json, time, math, hashlib, itertools, platform, traceback, resource
import numpy as np
import census_core as cc
import scipy.fft as sfft

R1_PATH = '/workspace/L0p_census_design_r1_20261114/L0P_CENSUS_DESIGN_r1.md'
R1_SHA = 'c2673a6426ca5728738c7e7e63871bd26577e8475e9b2819d9980aeccb642fd1'
CODE_DIR = os.path.dirname(os.path.abspath(__file__))
EPS64 = 2.220446049250313e-16
MEM_THRESHOLD_KB = 3670016
LOAD_RULE = 'none (free rule)'
UNITS = {'sc': 'ell = face link length = cube side (simple cubic, one site per Planck cube)',
         'stag': 'ell = face link length = cube side (simple cubic, one site per Planck cube)',
         'bcc': 'ell = BCC link length = a*sqrt(3)/2 (OD8(a)); grid unit a/2; k*ell = sqrt(3) k_grid'}
MET, NOT, UNI = 'MET', 'NOT MET', 'UNINFORMATIVE'

PHI_K7 = [0.5 + j / 6 for j in range(7)]
PHI_K3 = [0.5, 1.0, 1.5]
TH_K7 = [math.pi / 16 + j * math.pi / 32 for j in range(7)]
TH_K3 = [math.pi / 16, 5 * math.pi / 32, math.pi / 4]
CENSUS_CANDS = ['B0', 'C1', 'C2', 'C3', 'C4']
D13 = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1),
       (0, 1, 1), (0, 1, -1), (1, 1, 1), (1, -1, 1), (1, 1, -1), (-1, 1, 1)]
D26 = D13 + [tuple(-np.array(v)) for v in D13]

CAPS = {  # (cpu s, wall s, rss MiB, output MiB) -- r1 Section 7
    'census': {'S0': (120, 180, 512, 1), 'S1': (600, 900, 1024, 10), 'S2': (300, 450, 512, 5),
               'S3': (3600, 4500, 2048, 50), 'S4': (600, 900, 1024, 10),
               'S5a': (5400, 7200, 3072, 50), 'S5b': (1200, 1800, 2048, 10),
               'S6': (3600, 4500, 1024, 20), 'S7': (120, 180, 512, 5)},
    'repair': {'S0': (60, 90, 512, 1), 'S1': (120, 180, 1024, 2), 'S2b': (60, 90, 512, 1),
               'S3': (900, 1200, 2048, 10), 'S4': (120, 180, 1024, 2),
               'S5a': (600, 900, 2048, 10), 'S6': (720, 900, 1024, 5), 'S7': (60, 90, 512, 1)}}

# Census-size parameters (r1) and tiny smoke parameters (NOT CENSUS).
PARAMS = {
    'census': dict(S1_L=24, S1_cycles=50, T_nk=1000, S2b_L=24, LF_len=4096, LF_t0=200, LF_t1=1200,
                   S3_n=129, S3_nc=65, S3_n_stag=65, S3_nc_stag=33, S3_maxref=100,
                   S4_kappa=[0.010 + 0.005 * i for i in range(39)], S4_rays=D26,
                   S5a_sigmas=[1.5, 3.0, 6.0], S5a_box_sc=[48, 90, 180], S5a_box_bcc=[80, 160, 320],
                   S5b_box_sc=[96, 192], S5b_box_bcc=[168, 336], S5b_r=[3, 6, 12],
                   S6_L=16, S6_L_bcc=32, S6_layers=100000, knob_sub=None),
    'smoke': dict(S1_L=6, S1_cycles=3, T_nk=20, S2b_L=6, LF_len=1024, LF_t0=20, LF_t1=120,
                  S3_n=9, S3_nc=5, S3_n_stag=5, S3_nc_stag=3, S3_maxref=3,
                  S4_kappa=[0.010 + 0.02 * i for i in range(10)], S4_rays=D13[:3] + [D13[9]],
                  S5a_sigmas=[0.5, 1.0], S5a_box_sc=[16, 30], S5a_box_bcc=[28, 52],
                  S5b_box_sc=[16, 24], S5b_box_bcc=[28, 40], S5b_r=[2, 3],
                  S6_L=6, S6_L_bcc=8, S6_layers=200, knob_sub=1),
}


def knobs(name, which, mode):
    if name == 'C4':
        return [None]
    if name == 'C2':
        g = TH_K7 if which == 'K7' else TH_K3
    else:
        g = PHI_K7 if which == 'K7' else PHI_K3
    sub = PARAMS[mode]['knob_sub']
    return g if sub is None else g[:sub]


def midpoint(name):
    if name == 'C4':
        return None
    return TH_K3[1] if name == 'C2' else PHI_K3[1]


# ---------------------------------------------------------------- utilities
def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def meminfo_kb(key='MemAvailable'):
    with open('/proc/meminfo') as f:
        for line in f:
            if line.startswith(key + ':'):
                return int(line.split()[1])
    return None


def reset_hwm():
    try:
        with open('/proc/self/clear_refs', 'w') as f:
            f.write('5')
        return True
    except Exception:
        return False


def vm_hwm_mib():
    with open('/proc/self/status') as f:
        for line in f:
            if line.startswith('VmHWM:'):
                return int(line.split()[1]) / 1024.0
    return None


class Meter:
    def __enter__(self):
        reset_hwm(); self.c0 = time.process_time(); self.w0 = time.time(); return self

    def __exit__(self, *a):
        self.cpu = time.process_time() - self.c0; self.wall = time.time() - self.w0
        self.rss = vm_hwm_mib()
        return False

    def d(self):
        return {'cpu_s': round(self.cpu, 3), 'wall_s': round(self.wall, 3),
                'peak_rss_mib': round(self.rss, 1) if self.rss else None,
                'peak_rss_note': 'VmHWM of the step process after clear_refs reset at the start of this record'}


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, complex):
        return [o.real, o.imag]
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return repr(o)
    return o


class Ctx:
    def __init__(self, args):
        self.mode = args.mode; self.run_dir = args.run_dir; self.round = args.round
        self.code_sums_sha = args.code_sums_sha; self.P = PARAMS[self.mode]
        self.step = args.step

    def path(self, *parts):
        p = os.path.join(self.run_dir, *parts)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        return p

    def write_result(self, cand, step, rec, meter=None, cand_name_for_units=None):
        base = {
            'NOTICE': ('NOT CENSUS - tiny smoke test, sizes are not the r1 sizes' if self.mode == 'smoke' else None),
            'design_sha256': R1_SHA, 'implementation_manifest_sha256': self.code_sums_sha,
            'candidate': cand, 'step': step, 'round': self.round, 'mode': self.mode,
            'boundary': rec.pop('boundary', 'periodic'),
            'units': rec.pop('units', None), 'load_rule': LOAD_RULE,
            'caps_cpu_wall_rss_out': CAPS[self.round].get(self.step),
        }
        if meter is not None:
            base.update(meter.d())
        base.update(rec)
        p = self.path(cand, step, 'result.json')
        if os.path.exists(p):
            raise RuntimeError('refusing to overwrite ' + p)
        with open(p, 'w') as f:
            json.dump(jsonable(base), f, indent=1)
        return p

    def read_result(self, cand, step):
        p = os.path.join(self.run_dir, cand, step, 'result.json')
        if not os.path.exists(p):
            return None
        with open(p) as f:
            return json.load(f)


def combine(labels):
    labels = list(labels)
    if any(l == NOT for l in labels):
        return NOT
    if any(l != MET for l in labels):
        return UNI
    return MET


def cand_units(name):
    return UNITS[cc.make_candidate(name, 1.0 if name != 'C2' else 0.3)['lattice']] if name != 'C4' else UNITS['sc']


def guarded(fn):
    """Run fn(); exceptions become an UNINFORMATIVE record with traceback."""
    try:
        return fn()
    except Exception as e:
        return {'outcome': UNI, 'error': repr(e), 'traceback': traceback.format_exc()}


def symbol(cand, k):
    if 'symfn' in cand:
        return cand['symfn'](np.asarray(k, float))
    return cc.cycle_symbol(cand['layers'], k, cand['d'])


def omegas(U):
    """quasi-energies omega in (-pi, pi], eigenvalues e^{-i omega}."""
    w = -np.angle(np.linalg.eigvals(U))
    w = np.where(w <= -np.pi, w + 2 * np.pi, w)
    return w


# ===================================================================== S0
def k_checks():
    """K1-K7 recomputed inside the implementation (r1 Appendix A)."""
    import dirac4_cycle_symbol as d4
    from scipy.linalg import expm
    rng = np.random.default_rng(20261114)
    out = {}
    def face(i, k):
        return expm(-1j * k[i] * cc.SIG[i])
    k1 = 0
    for _ in range(200):
        k = rng.uniform(-np.pi, np.pi, 3)
        Ap = face(0, k) @ face(1, k) @ face(2, k); Am = face(2, k) @ face(1, k) @ face(0, k)
        k1 = max(k1, abs(Ap - d4.A(+1, k)).max(), abs(Am - d4.A(-1, k)).max())
    out['K1'] = k1
    k2a = k2b = 0
    for _ in range(200):
        k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.3, 1.6)
        for eps in (+1, -1):
            A = d4.A(eps, k)
            Xr = cc.TX @ np.block([[A.conj().T, np.zeros((2, 2))], [np.zeros((2, 2)), A]])
            k2a = max(k2a, abs(d4.X(eps, k) - Xr).max())
            Q = np.block([[np.eye(2), np.zeros((2, 2))], [np.zeros((2, 2)), A.conj().T]])
            Vr = Q @ expm(-1j * phi * cc.TX) @ Q.conj().T @ expm(1j * phi * cc.TX)
            k2b = max(k2b, abs(d4.V(eps, k, phi) - Vr).max())
            k2b = max(k2b, abs(cc.cycle_symbol(cc.V_layers(eps, phi), k, 4) - Vr).max())
    out['K2_X'] = k2a; out['K2_V'] = k2b
    k3 = 0
    for _ in range(200):
        k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.3, 1.6)
        k3 = max(k3, abs(cc.cycle_symbol(cc.make_candidate('C3', phi)['layers'], k, 4) - d4.U(k, phi=phi)).max())
    out['K3'] = k3
    k3b = 0
    for _ in range(200):
        k = rng.uniform(-np.pi, np.pi, 3)
        Sp = cc.cycle_symbol(cc.S_layers(+1), k, 4)
        Ad = d4.A(+1, k).conj().T
        Lz = face(2, -k) @ face(1, -k) @ face(0, -k)   # e^{+i k_z s_z} e^{+i k_y s_y} e^{+i k_x s_x}... order z,y,x applied
        k3b = max(k3b, abs(Sp[2:, 2:] - Ad).max(), abs(Sp[:2, :2] - d4.A(+1, k)).max())
    out['K3b'] = k3b
    k4 = 0
    for _ in range(100):
        k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.3, 1.6)
        for i in range(3):
            X = cc.BETA @ expm(1j * k[i] * cc.ALPHA[i])
            k4 = max(k4, abs(X - X.conj().T).max(), abs(X @ X - cc.I4).max())
            W = cc.cycle_symbol(cc.W_layers(i, phi), k, 4)
            Wr = (np.cos(phi) * cc.I4 - 1j * np.sin(phi) * X) @ (np.cos(phi) * cc.I4 + 1j * np.sin(phi) * cc.BETA)
            k4 = max(k4, abs(W - Wr).max(), abs(W @ W.conj().T - cc.I4).max())
            k0 = k.copy(); k0[i] = 0.0
            kp = k.copy(); kp[i] = np.pi
            k4 = max(k4, abs(cc.cycle_symbol(cc.W_layers(i, phi), k0, 4) - cc.I4).max(),
                     abs(cc.cycle_symbol(cc.W_layers(i, phi), kp, 4) - expm(2j * phi * cc.BETA)).max())
    out['K4'] = k4
    phi = 1.4; c1 = cc.make_candidate('C1', phi); c3 = cc.make_candidate('C3', phi); c4 = cc.make_candidate('C4', None)
    k5a = k5b = k5d = 0; k5c = []
    for corner in itertools.product([0, np.pi], repeat=3):
        k = np.array(corner); p = int(round(sum(corner) / np.pi))
        k5a = max(k5a, abs(cc.cycle_symbol(c1['layers'], k, 4) - expm(4j * p * phi * cc.BETA)).max())
        U3 = cc.cycle_symbol(c3['layers'], k, 4)
        if p % 2 == 0:
            k5b = max(k5b, abs(U3 - cc.I4).max())
        else:
            k5c.append(float(abs(U3 - cc.I4).max()))   # max-abs entry, as Appendix A
        k5d = max(k5d, abs(cc.cycle_symbol(c4['layers'], k, 2) - np.eye(2)).max())
    out['K5_C1'] = k5a; out['K5_C3_even'] = k5b; out['K5_C3_odd_norm'] = k5c; out['K5_C4'] = k5d
    k6 = True
    for x in itertools.product(range(2), repeat=3):
        for i, j in [(0, 1), (0, 2), (1, 2)]:
            xi = np.array(x); ei = cc.E[i]; ej = cc.E[j]
            prod = cc.eta(i, xi) * cc.eta(j, xi + ei) * cc.eta(i, xi + ej) * cc.eta(j, xi)
            k6 = k6 and (prod == -1)
    out['K6'] = bool(k6)
    k7 = 0
    for _ in range(100):
        k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.3, 1.6)
        for n in ('C1', 'C3'):
            U = cc.cycle_symbol(cc.make_candidate(n, phi)['layers'], k, 4)
            k7 = max(k7, abs(U @ U.conj().T - cc.I4).max())
    out['K7'] = k7
    # implementation-level consistency checks (same family as K-checks)
    extra = {}
    e = 0
    for _ in range(50):
        k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.5, 1.5)
        e = max(e, abs(cc.cycle_symbol(cc.make_candidate('B0', phi)['layers'], k, 4) - d4.U(k, phi=phi)).max())
    extra['B0_composed_vs_dirac4'] = e
    e = 0
    for _ in range(50):
        k = rng.uniform(-np.pi, np.pi, 3)
        Ap = face(0, k) @ face(1, k) @ face(2, k); Am = face(2, k) @ face(1, k) @ face(0, k)
        e = max(e, abs(cc.cycle_symbol(c4['layers'], k, 2) - Am @ Ap).max())
    extra['C4_vs_AmAp'] = e
    e = 0
    for _ in range(50):
        k = rng.uniform(-np.pi, np.pi, 3); phi = rng.uniform(0.5, 1.5)
        def Wf(i):
            X = cc.BETA @ expm(1j * k[i] * cc.ALPHA[i])
            return (np.cos(phi) * cc.I4 - 1j * np.sin(phi) * X) @ (np.cos(phi) * cc.I4 + 1j * np.sin(phi) * cc.BETA)
        Sp = cc.cycle_symbol(cc.S_layers(+1), k, 4); Sm = cc.cycle_symbol(cc.S_layers(-1), k, 4)
        VFp = Wf(2) @ Wf(1) @ Wf(0); VFm = Wf(0) @ Wf(1) @ Wf(2)
        e = max(e, abs(cc.cycle_symbol(cc.make_candidate('C1', phi)['layers'], k, 4) - VFm @ Sm @ VFp @ Sp).max())
        Vp = d4.V(+1, k, phi); Vm = d4.V(-1, k, phi)
        e = max(e, abs(cc.cycle_symbol(cc.make_candidate('RC3', phi)['layers'], k, 4) - VFm @ Vm @ Sm @ VFp @ Vp @ Sp).max())
    extra['C1_RC3_vs_closed_form'] = e
    e = 0
    for _ in range(50):
        k = rng.uniform(-np.pi, np.pi, 3); th = rng.uniform(0.1, 0.8)
        U = cc.cycle_symbol(cc.make_candidate('C2', th)['layers'], k, 8)
        e = max(e, abs(U @ U.conj().T - np.eye(8)).max())
    extra['C2_unitarity'] = e
    counts = {}
    for n in ['B0', 'C1', 'C2', 'C3', 'C4', 'RC3']:
        c = cc.make_candidate(n, 1.0 if n != 'C2' else 0.3)
        hop, ons = cc.layer_counts(c)
        r1 = cc.R1_TABLE[n]
        counts[n] = {'hop': hop, 'onsite': ons, 'r1_hop': r1[2], 'r1_onsite': r1[3],
                     'match': (n == 'B0' and hop + ons == 4) or (hop == r1[2] and ons == r1[3])}
    extra['layer_counts'] = counts
    tol = 1e-12
    passed = (all(out[k] <= tol for k in ['K1', 'K2_X', 'K2_V', 'K3', 'K3b', 'K4', 'K5_C1', 'K5_C3_even', 'K5_C4', 'K7'])
              and all(abs(v - 0.631) < 5e-4 for v in out['K5_C3_odd_norm']) and out['K6']
              and all(extra[k] <= tol for k in ['B0_composed_vs_dirac4', 'C4_vs_AmAp', 'C1_RC3_vs_closed_form', 'C2_unitarity'])
              and all(v['match'] for v in counts.values()))
    return out, extra, passed


def step_S0(ctx):
    with Meter() as m:
        rec = {}
        mem = meminfo_kb()
        rec['MemAvailable_kB'] = mem; rec['threshold_kB'] = MEM_THRESHOLD_KB
        mem_ok = mem is not None and mem >= MEM_THRESHOLD_KB
        r1_ok = sha256_file(R1_PATH) == R1_SHA
        rec['design_file_sha256'] = sha256_file(R1_PATH)
        # code manifest
        sums = os.path.join(CODE_DIR, 'SHA256SUMS')
        man = {}; man_ok = os.path.exists(sums)
        if man_ok:
            man_sha = sha256_file(sums)
            man_ok = (man_sha == ctx.code_sums_sha)
            with open(sums) as f:
                for line in f:
                    h, fn = line.split(None, 1); fn = fn.strip().lstrip('*')
                    got = sha256_file(os.path.join(CODE_DIR, fn))
                    man[fn] = {'listed': h, 'recomputed': got, 'match': h == got}
                    man_ok = man_ok and (h == got)
            rec['manifest_sha256_recomputed'] = man_sha
        rec['manifest'] = man
        kc, extra, k_ok = k_checks()
        rec['K_checks'] = kc; rec['implementation_checks'] = extra
        import scipy
        try:
            from threadpoolctl import threadpool_info
            tp = threadpool_info()
        except Exception as e:
            tp = repr(e)
        rec['environment'] = {'python': sys.version, 'numpy': np.__version__, 'scipy': scipy.__version__,
                              'platform': platform.platform(), 'cpu_count': os.cpu_count(),
                              'threads_env': {k: os.environ.get(k) for k in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']},
                              'threadpools': tp}
        if ctx.mode == 'smoke':
            rec['memory_rule_note'] = 'NOT CENSUS smoke: memory value recorded, not enforced'
            mem_ok_eff = True
        else:
            mem_ok_eff = mem_ok
        rec['checks'] = {'memory': mem_ok, 'design_sha256': r1_ok, 'code_manifest': man_ok, 'K1_K7_and_impl': k_ok}
        rec['outcome'] = 'PASS' if (mem_ok_eff and r1_ok and man_ok and k_ok) else 'STOP'
        if rec['outcome'] == 'STOP':
            reasons = [k for k, v in rec['checks'].items() if not v and not (k == 'memory' and ctx.mode == 'smoke')]
            rec['stop_reasons'] = reasons
            rec['census_label'] = UNI
    ctx.write_result('_global', 'S0' if ctx.round == 'census' else 'S0_repair', rec, m)
    return 0 if rec['outcome'] == 'PASS' else 10


# ===================================================================== S1
def t_matrices(d):
    if d == 4:
        P = [cc.S0_, cc.SX, cc.SY, cc.SZ]
        return {f'tau{a}xsigma{b}': np.kron(P[a], P[b]) for a in range(4) for b in range(4)}
    if d == 2:
        P = [cc.S0_, cc.SX, cc.SY, cc.SZ]
        return {f'sigma{b}': P[b] for b in range(4)}
    out = {}
    S = np.array(cc.SUBS)
    for a in itertools.product([0, 1], repeat=3):
        out['signs' + ''.join(map(str, a))] = np.diag((-1.0) ** (S @ np.array(a))).astype(complex)
    return out


def rand_state(eng, B, seed):
    rng = np.random.default_rng(seed)
    c = eng.c; L = eng.L
    if c['lattice'] == 'sc':
        shp = (B, c['d'], L, L, L)
    elif c['lattice'] == 'bcc':
        shp = (B, c['d'], 2, L // 2, L // 2, L // 2)
    else:
        shp = (B, L, L, L)
    psi = rng.normal(size=shp) + 1j * rng.normal(size=shp)
    for b in range(B):
        psi[b] /= np.sqrt((abs(psi[b]) ** 2).sum())
    return psi


def delta_states(eng):
    c = eng.c; L = eng.L
    out = []
    if c['lattice'] == 'sc':
        for j in range(c['d']):
            p = np.zeros((1, c['d'], L, L, L), complex); p[0, j, 0, 0, 0] = 1; out.append((p, (0, 0, 0)))
    elif c['lattice'] == 'bcc':
        M = L // 2
        for j in range(c['d']):
            p = np.zeros((1, c['d'], 2, M, M, M), complex); p[0, j, 0, 0, 0, 0] = 1; out.append((p, (0, 0, 0)))
    else:
        for s in cc.SUBS:
            p = np.zeros((1, L, L, L), complex); p[0][s] = 1; out.append((p, s))
    return out


def dist_field(eng, origin):
    """distance of every stored site from origin (Manhattan SC/stag, Chebyshev BCC), periodic."""
    L = eng.L
    if eng.c['lattice'] == 'bcc':
        X = eng.cart()   # (2,M,M,M,3)
        d = (X - np.array(origin)) % L; d = np.minimum(d, L - d)
        return d.max(-1)
    x = np.stack(np.meshgrid(*(np.arange(L),) * 3, indexing='ij'), -1)
    d = (x - np.array(origin)) % L; d = np.minimum(d, L - d)
    return d.sum(-1)


def s1_candidate(ctx, name):
    P = ctx.P; ci = cc.CAND_INDEX[name]
    per = {}
    for kv in knobs(name, 'K3', ctx.mode):
        c = cc.make_candidate(name, kv)
        L = 2 * P['S1_L'] if c['lattice'] == 'bcc' else P['S1_L']
        eng = cc.make_engine(c, L)
        nl = len(c['layers']) * P['S1_cycles']
        psi0 = rand_state(eng, 1, 20261114 + 100 * ci + 0)
        psi = psi0.copy()
        for _ in range(P['S1_cycles']):
            psi = cc.run_cycle(eng, psi)
        dQ = abs((abs(psi) ** 2).sum() - 1.0)
        bandQ = 10 * nl * EPS64
        for _ in range(P['S1_cycles']):
            psi = cc.run_cycle(eng, psi, adjoint=True)
        dR = abs(psi - psi0).max(); bandR = 10 * 2 * nl * EPS64
        # light cone
        lc_ok = True; lc_max_out = 0.0
        for p0, origin in delta_states(eng):
            D = dist_field(eng, origin)
            state = {'r': 0}
            def cb(psi_, layer, D=D, state=state):
                nonlocal lc_ok, lc_max_out
                if layer['hop']:
                    state['r'] += 1
                a = abs(psi_[0]) if psi_.ndim == 4 else abs(psi_[0]).max(0)
                out = a[D > state['r']]
                mo = float(out.max()) if out.size else 0.0
                lc_max_out = max(lc_max_out, mo)
                if mo != 0.0:
                    lc_ok = False
            cc.run_cycle(eng, p0, callback=cb)
        # time-reversal record
        rng = np.random.default_rng(20261114 + 100 * ci + 77)
        ks = rng.uniform(-np.pi, np.pi, (P['T_nk'], 3))
        if c['lattice'] == 'stag':
            ks = ks / 2
        U = symbol(c, ks); Um = symbol(c, -ks)
        works = []
        for nm, Mx in t_matrices(c['d']).items():
            Mi = np.linalg.inv(Mx)
            dev = abs(Mx @ U.conj() @ Mi - Um.conj().transpose(0, 2, 1)).max()
            if dev <= 1e-12:
                works.append(nm)
        ok = (dQ <= bandQ) and (dR <= bandR) and lc_ok
        per[repr(kv)] = {'knob': kv, 'grid_L': L, 'n_layers': nl, 'dQ': dQ, 'bandQ': bandQ, 'dR': dR, 'bandR': bandR,
                         'lightcone_ok': lc_ok, 'lightcone_max_outside': lc_max_out,
                         'T_test_record_M_that_work': works, 'outcome': MET if ok else NOT}
    return {'per_knob': per, 'seed_random_state': 20261114 + 100 * ci + 0,
            'outcome_F3': combine(v['outcome'] for v in per.values()),
            'outcome_V1': combine(v['outcome'] for v in per.values())}


def step_S1(ctx):
    cands = CENSUS_CANDS if ctx.round == 'census' else ['RC3']
    for name in cands:
        with Meter() as m:
            rec = guarded(lambda: s1_candidate(ctx, name))
        rec['units'] = cand_units(name)
        if 'outcome' not in rec:
            rec['outcome'] = rec['outcome_F3']
        ctx.write_result(name, 'S1', rec, m)
    return 0


# ===================================================================== S2
def s2a_analytic():
    EP = 1.22e19
    rows = []
    def coef(E, n):
        n = np.array(n, float); n = n / np.linalg.norm(n)
        return (1 / 8) * (E / EP) ** 2 * (n ** 4).sum()
    printed = [('1 GeV [100]', coef(1, (1, 0, 0)), '8.4e-40'), ('1 GeV [111]', coef(1, (1, 1, 1)), '2.8e-40'),
               ('30 GeV [100]', coef(30, (1, 0, 0)), '7.6e-37'), ('31 GeV [100]', coef(31, (1, 0, 0)), '8.1e-37'),
               ('1 TeV [100]', coef(1000, (1, 0, 0)), '8.4e-34')]
    for nm, v, p in printed:
        rows.append({'cell': nm, 'value': v, 'formatted': '%.1e' % v, 'printed': p, 'match': ('%.1e' % v) == p})
    for nm, s4, p in [('E_QG2 [100]', 1.0, '4.2e+19'), ('E_QG2 [111]', 1 / 3, '7.3e+19')]:
        xi2 = s4 / 24.0
        v = EP / math.sqrt(2 * xi2)
        rows.append({'cell': nm, 'value': v, 'formatted': '%.1e' % v, 'printed': p, 'match': ('%.1e' % v) == p})
    return rows


def s2a_leapfrog(P):
    lam = 0.5
    printed = {((1, 0, 0), 0.25): 0.9940, ((1, 1, 0), 0.25): 0.9980, ((1, 1, 1), 0.25): 0.9993,
               ((1, 0, 0), 1.0): 0.9038, ((1, 1, 0), 1.0): 0.9676, ((1, 1, 1), 1.0): 0.9891,
               ((1, 0, 0), 2.0): 0.5955, ((1, 1, 0), 2.0): 0.8559, ((1, 1, 1), 2.0): 0.9508}
    Lx = P['LF_len']; T = 4; t0, t1 = P['LF_t0'], P['LF_t1']; w = 40.0
    rows = []
    for (n, ka), pv in printed.items():
        m = sum(n); sh = [0, 4 if n[1] else 0, 4 if n[2] else 0]   # sheared identification
        def nb(u, axis, s):
            v = np.roll(u, -s, axis=axis)   # u(x + s e_axis) with plain wrap
            if axis == 0 or sh[axis] == 0:
                return v
            if s == 1:
                if axis == 1:
                    v[:, T - 1, :] = np.roll(u[:, 0, :], -sh[1], axis=0)
                else:
                    v[:, :, T - 1] = np.roll(u[:, :, 0], -sh[2], axis=0)
            else:
                if axis == 1:
                    v[:, 0, :] = np.roll(u[:, T - 1, :], sh[1], axis=0)
                else:
                    v[:, :, 0] = np.roll(u[:, :, T - 1], sh[2], axis=0)
            return v
        x = np.arange(Lx)[:, None, None]; y = np.arange(T)[None, :, None]; z = np.arange(T)[None, None, :]
        p = x + n[1] * y + n[2] * z   # plane index
        kap = ka / math.sqrt(m)       # phase per plane
        om = 2 * math.asin(lam * math.sqrt(m) * math.sin(kap / 2))
        # group velocity in planes per tick; exact: sin(om/2) = lam sqrt(m) sin(kap/2) -> cos(om/2) dom/2 = lam sqrt(m) cos(kap/2) dkap/2
        vg = lam * math.sqrt(m) * math.cos(kap / 2) / math.cos(om / 2)
        p0 = Lx / 4
        u0 = (np.exp(-((p % Lx) - p0) ** 2 / (2 * w * w)) * np.exp(1j * kap * p)).astype(complex)
        um = (np.exp(-((p % Lx) - p0 + vg) ** 2 / (2 * w * w)) * np.exp(1j * (kap * p + om))).astype(complex)
        cents = {}
        u_prev, u = um, u0
        for t in range(0, t1 + 1):
            if t in (t0, t1):
                line = abs(u[:, 0, 0]) ** 2
                cents[t] = float((np.arange(Lx) * line).sum() / line.sum())
            lap = sum(nb(u, a, s) for a in range(3) for s in (1, -1)) - 6 * u
            u_prev, u = u, 2 * u - u_prev + lam ** 2 * lap
        speed = (cents[t1] - cents[t0]) / (t1 - t0) / (math.sqrt(m) * lam)
        ok = (round(speed, 4) == pv) or abs(speed - pv) <= 2e-4
        rows.append({'dir': n, 'ka': ka, 'speed_over_c': speed, 'printed': pv, 'match': bool(ok),
                     'group_velocity_analytic': math.cos(kap / 2) / math.cos(om / 2)})
    return rows


def s2a_b0_record():
    # BCC 8-corner scalar wave rule, k per a/2: omega^2 = 2 (1 - prod cos(k n_i)).
    # Taylor: omega = k (1 - k^2 [sum n^4 / 24 + sum_{i<j} n_i^2 n_j^2 / 4] + ...).
    out = []
    for n, pv in [((1, 0, 0), 1 / 24), ((1, 1, 0), 1 / 12), ((1, 1, 1), 7 / 72)]:
        v = np.array(n, float); v /= np.linalg.norm(v)
        c = (v ** 4).sum() / 24 + sum(v[i] ** 2 * v[j] ** 2 for i in range(3) for j in range(i + 1, 3)) / 4
        out.append({'dir': n, 'coefficient': float(c), 'printed': pv, 'abs_dev': abs(c - pv), 'match': abs(c - pv) <= 1e-12})
    return out


def plane_wave(eng, k, u):
    c = eng.c; L = eng.L
    if c['lattice'] == 'sc':
        x = np.stack(np.meshgrid(*(np.arange(L),) * 3, indexing='ij'), -1)
        return (u[:, None, None, None] * np.exp(1j * (x @ k)))[None]
    if c['lattice'] == 'bcc':
        X = eng.cart()
        return (u[:, None, None, None, None] * np.exp(1j * (X @ k)))[None]
    x = eng.x; sidx = x[..., 0] % 2 + 2 * (x[..., 1] % 2) + 4 * (x[..., 2] % 2)
    return (u[sidx] * np.exp(1j * (x @ k)))[None]


def s2b_candidate(ctx, name):
    P = ctx.P; ci = cc.CAND_INDEX[name]; L = P['S2b_L']
    per = {}
    for kv in knobs(name, 'K3', ctx.mode):
        c = cc.make_candidate(name, kv)
        LL = 2 * L if c['lattice'] == 'bcc' else L   # B0 on the a/2 grid
        eng = cc.make_engine(c, LL)
        rng = np.random.default_rng(20261114 + 100 * ci + 50)
        ms = [np.zeros(3, int)] + [np.array(cr) * (LL // 2) for cr in itertools.product([0, 1], repeat=3)][1:]
        ms += [rng.integers(0, LL, 3) for _ in range(12)]
        worst = 0.0; rows = []
        for m_ in ms:
            k = 2 * np.pi * m_ / LL
            u = rng.normal(size=c['d']) + 1j * rng.normal(size=c['d'])
            psi = plane_wave(eng, k, u)
            out = cc.run_cycle(eng, psi)
            ref = plane_wave(eng, k, symbol(c, k) @ u)
            dev = float(abs(out - ref).max()); worst = max(worst, dev)
            rows.append({'m': m_.tolist(), 'dev': dev})
        per[repr(kv)] = {'knob': kv, 'grid_L': LL, 'max_dev': worst, 'waves': rows,
                         'outcome': MET if worst <= 1e-12 else NOT}
    return {'per_knob': per, 'seed': 20261114 + 100 * ci + 50,
            'outcome_S2b': combine(v['outcome'] for v in per.values())}


def step_S2(ctx):
    if ctx.round == 'census':
        with Meter() as m:
            rec = guarded(lambda: {'analytic': s2a_analytic(), 'leapfrog': s2a_leapfrog(ctx.P),
                                   'B0_bcc_coefficients_record': s2a_b0_record()})
        if 'analytic' in rec:
            ok = all(r['match'] for r in rec['analytic']) and all(r['match'] for r in rec['leapfrog'])
            rec['outcome'] = MET if ok else NOT
        rec['units'] = 'six-face scalar reference, a = l_P'
        ctx.write_result('_global', 'S2a', rec, m)
        s2a = rec['outcome']
    else:
        s2a = (ctx.read_result('_global', 'S2a') or {}).get('outcome', UNI)
    cands = CENSUS_CANDS if ctx.round == 'census' else ['RC3']
    for name in cands:
        with Meter() as m:
            rec = guarded(lambda: s2b_candidate(ctx, name))
        rec['units'] = cand_units(name)
        rec['S2a_outcome_used'] = s2a
        if 'outcome_S2b' in rec:
            rec['outcome'] = combine([s2a, rec['outcome_S2b']])
        ctx.write_result(name, 'S2' if ctx.round == 'census' else 'S2b', rec, m)
    return 0


# ===================================================================== S4
def haar(d):
    rng = np.random.default_rng(20261114 + 900 + d)
    Z = (rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))) / np.sqrt(2)
    Q, R = np.linalg.qr(Z)
    ph = np.diag(R) / abs(np.diag(R))
    return Q * ph[None, :]


def control_cand(d):
    Rd = haar(d)
    def f(k):
        ws = 2 * np.sqrt((np.sin(k / 2) ** 2).sum(-1))
        diag = np.concatenate([np.repeat(np.exp(-1j * ws)[..., None], d // 2, -1),
                               np.repeat(np.exp(+1j * ws)[..., None], d // 2, -1)], -1)
        return np.einsum('ij,...j,kj->...ik', Rd, diag, Rd.conj())
    return {'name': f'ctrl{d}', 'd': d, 'lattice': 'sc', 'symfn': f}


def ray_fit(cand, kappas, rays):
    """Same code path for candidates and controls. Returns per ray/band fits."""
    lat = cand['lattice']; d = cand['d']
    scale = 1.0 / cc.SQ3 if lat == 'bcc' else 1.0          # k_grid = kappa / sqrt(3) for B0
    kap = np.array(kappas)
    w0 = np.sort(omegas(symbol(cand, np.zeros(3))))
    bands = [b for b in range(d) if abs(w0[b]) <= 1e-6]      # bands with omega -> 0 at Gamma
    t = kap / kap.max()
    Vm = np.stack([t ** m for m in range(1, 8)], -1)
    fits = []; maxw = 0.0
    for n in rays:
        nh = np.array(n, float); nh /= np.linalg.norm(nh)
        K = kap[:, None] * nh[None, :] * scale
        W = np.sort(omegas(symbol(cand, K)), axis=-1)       # (nk, d), sorted at each kappa
        maxw = max(maxw, float(abs(W[:, bands]).max()) if bands else 0.0)
        for b in bands:
            coef, *_ = np.linalg.lstsq(Vm, W[:, b], rcond=None)
            a = coef / kap.max() ** np.arange(1, 8)
            fits.append({'ray': list(n), 'band': b, 'a': a.tolist(), 'c0': float(a[0]),
                         'xi1': float(a[1] / a[0]), 'xi2': float(a[2] / a[0]),
                         'positive': bool(a[0] > 0)})
    return {'bands': bands, 'fits': fits, 'max_abs_omega_on_rays': maxw}


def s4_control(ctx):
    P = ctx.P; out = {}; valid = True; thr = {}
    for d in (2, 4, 8):
        r = ray_fit(control_cand(d), P['S4_kappa'], P['S4_rays'])
        pos = [f for f in r['fits'] if f['positive']]
        cbar = np.mean([abs(f['c0']) for f in pos])
        Fxi = max(abs(f['xi1']) for f in pos)
        Fc = max(abs(abs(f['c0']) / cbar - 1) for f in pos)
        x100 = [f['xi2'] for f in pos if tuple(f['ray']) == (1, 0, 0)]
        x111 = [f['xi2'] for f in pos if tuple(f['ray']) == (1, 1, 1)]
        ok = (len(x100) > 0 and len(x111) > 0 and all(abs(x + 1 / 24) <= 1e-6 for x in x100)
              and all(abs(x + 1 / 72) <= 1e-6 for x in x111) and Fxi <= 1e-9 and Fc <= 1e-9)
        valid = valid and ok
        out[d] = {'F_xi': Fxi, 'F_c': Fc, 'cbar0': cbar, 'xi2_100': x100, 'xi2_111': x111, 'valid': ok,
                  'n_positive_fits': len(pos), 'raw_fits': r['fits']}
        thr[d] = {'T_xi': 100 * max(Fxi, EPS64), 'T_c': 100 * max(Fc, EPS64)}
    return out, valid, thr


def s4_candidate(ctx, name, thr_file, thr_sha):
    P = ctx.P
    with open(thr_file, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != thr_sha:
        return {'outcome': UNI, 'reason': 'S4_control_thresholds.json sha256 mismatch'}
    T = json.loads(raw)
    dsize = cc.make_candidate(name, 1.0 if name != 'C2' else 0.3)['d'] if name != 'C4' else 2
    dkey = str(dsize)
    have_thr = T.get('valid', False)
    per = {}
    for kv in knobs(name, 'K7', ctx.mode):
        c = cc.make_candidate(name, kv)
        r = ray_fit(c, P['S4_kappa'], P['S4_rays'])
        fits = r['fits']
        if not fits:
            per[repr(kv)] = {'knob': kv, 'outcome': UNI, 'reason': 'no band with omega -> 0 at Gamma'}
            continue
        cbar = float(np.mean([abs(f['c0']) for f in fits]))
        mxi1 = max(abs(f['xi1']) for f in fits)
        mc = max(abs(abs(f['c0']) / cbar - 1) for f in fits)
        mxi2 = max(abs(f['xi2']) for f in fits)
        wrap_guard = r['max_abs_omega_on_rays'] > 3.0
        rec = {'knob': kv, 'cbar0': cbar, 'bands': r['bands'], 'max_abs_xi1': mxi1, 'max_c0_dev': mc,
               'max_abs_xi2': mxi2, 'max_abs_omega_on_rays': r['max_abs_omega_on_rays'],
               'fits': fits}
        # xi2 direction dependence with template [100]/[110]/[111]
        tmpl = {}
        for tag, ray in [('100', (1, 0, 0)), ('110', (1, 1, 0)), ('111', (1, 1, 1))]:
            v = [f['xi2'] for f in fits if tuple(f['ray']) == ray]
            tmpl[tag] = v
        allxi2 = [f['xi2'] for f in fits]
        rec['xi2_template'] = tmpl; rec['xi2_max_minus_min'] = max(allxi2) - min(allxi2)
        try:
            m100 = np.mean(np.abs(tmpl['100'])); m111 = np.mean(np.abs(tmpl['111']))
            rec['axis_diagonal_ordering_record'] = '|xi2[100]| > |xi2[111]|' if m100 > m111 else '|xi2[100]| <= |xi2[111]|'
        except Exception:
            pass
        rec['nu_type_ratios_record'] = {'cbar0': cbar}
        if wrap_guard:
            rec['outcome'] = UNI; rec['reason'] = 'quasi-energy on rays exceeds 3.0 (branch wrap guard)'
        elif not have_thr:
            rec['outcome'] = UNI; rec['reason'] = 'S4 control invalid; no thresholds formed'
        else:
            Txi = T['thresholds'][dkey]['T_xi']; Tc = T['thresholds'][dkey]['T_c']
            ok = (mxi1 <= Txi) and (mc <= Tc) and (mxi1 < 0.05) and (mxi2 < 1.56e14)
            rec.update({'T_xi': Txi, 'T_c': Tc, 'crit_i': mxi1 <= Txi, 'crit_ii': mc <= Tc,
                        'crit_iii': (mxi1 < 0.05) and (mxi2 < 1.56e14)})
            rec['outcome'] = MET if ok else NOT
        per[repr(kv)] = rec
    return {'per_knob': per, 'd_threshold_size': dsize, 'thresholds_sha256': thr_sha,
            'outcome_F4': combine(v['outcome'] for v in per.values()),
            'fit_note': 'fit of the size of a measured effect (plan v3.4 0.1 rule 4); c0 taken as |a1| for every band'}


def step_S4(ctx):
    thr_file = os.path.join(ctx.run_dir, '_global', 'S4', 'S4_control_thresholds.json')
    if ctx.round == 'census':
        with Meter() as m:
            out, valid, thr = s4_control(ctx)
            payload = {'valid': valid, 'thresholds': {str(d): thr[d] for d in thr} if valid else None,
                       'floors': {str(d): {'F_xi': out[d]['F_xi'], 'F_c': out[d]['F_c']} for d in out}}
            os.makedirs(os.path.dirname(thr_file), exist_ok=True)
            def fmt(o):   # 17 significant digits
                if isinstance(o, float):
                    return float('%.17g' % o)
                if isinstance(o, dict):
                    return {k: fmt(v) for k, v in o.items()}
                return o
            txt = json.dumps(fmt(jsonable(payload)), indent=1)   # floats written as shortest round-trip repr (<= 17 sig. digits)
            assert not os.path.exists(thr_file)
            with open(thr_file, 'w') as f:
                f.write(txt)
        thr_sha = sha256_file(thr_file)
        with open(os.path.join(ctx.run_dir, 'run_log.jsonl'), 'a') as f:
            f.write(json.dumps({'event': 'S4_control_thresholds', 'sha256': thr_sha, 'valid': bool(valid),
                                'time': time.time()}) + '\n')
        rec = {'control_valid': valid, 'thresholds_file': thr_file, 'thresholds_sha256': thr_sha,
               'control': out, 'outcome': 'CONTROL VALID' if valid else UNI,
               'units': 'six-face scalar control, k per ell'}
        ctx.write_result('_global', 'S4_control', rec, m)
    else:
        thr_sha = (ctx.read_result('_global', 'S4_control') or {}).get('thresholds_sha256')
        with open(os.path.join(ctx.run_dir, 'run_log.jsonl'), 'a') as f:
            f.write(json.dumps({'event': 'S4_thresholds_reused_repair', 'sha256': thr_sha, 'time': time.time()}) + '\n')
    cands = CENSUS_CANDS if ctx.round == 'census' else ['RC3']
    for name in cands:
        with Meter() as m:
            rec = guarded(lambda: s4_candidate(ctx, name, thr_file, thr_sha))
        rec['units'] = cand_units(name)
        rec['thresholds_sha256'] = thr_sha
        if 'outcome' not in rec:
            rec['outcome'] = rec['outcome_F4']
        ctx.write_result(name, 'S4', rec, m)
    return 0


def cbar_for(ctx, name, kv):
    r = ctx.read_result(name, 'S4')
    if not r or 'per_knob' not in r:
        return None
    e = r['per_knob'].get(repr(kv))
    if not e or 'cbar0' not in e:
        return None
    return e['cbar0']


# ===================================================================== S3
def naive_control():
    def f(k):
        s = np.sin(k)
        Hs = np.einsum('...i,ijk->...jk', s, np.stack(cc.ALPHA))
        r = np.sqrt((s ** 2).sum(-1))[..., None, None]
        sinc = np.where(r > 0, np.sin(r) / np.where(r > 0, r, 1), 1.0)
        return np.cos(r) * np.eye(4) - 1j * sinc * Hs
    return {'name': 'naive_control', 'd': 4, 'lattice': 'sc', 'symfn': f}


def gfuncs(cand, K):
    w = omegas(symbol(cand, K))
    g0 = np.abs(w).min(-1)
    gp = (np.pi - np.abs(w)).min(-1)
    return g0, gp


def scan(cand, n):
    lat = cand['lattice']
    lim = np.pi / 2 if lat == 'stag' else np.pi
    lin = np.linspace(-lim, lim, n)
    G0 = np.empty((n, n, n)); GP = np.empty((n, n, n))
    ky, kz = np.meshgrid(lin, lin, indexing='ij')
    for i, kx in enumerate(lin):
        K = np.stack([np.full_like(ky, kx), ky, kz], -1)
        G0[i], GP[i] = gfuncs(cand, K)
    return lin, G0, GP


def local_minima(G, lin, below=0.5):
    from scipy import ndimage
    f = ndimage.minimum_filter(G, size=3, mode='nearest')
    mask = (G <= f) & (G < below)
    lab, nl = ndimage.label(mask, structure=np.ones((3, 3, 3)))
    pts = []
    if nl:
        idx = ndimage.minimum_position(G, lab, index=np.arange(1, nl + 1))
        for ix in idx:
            pts.append((float(G[ix]), np.array([lin[ix[0]], lin[ix[1]], lin[ix[2]]])))
    pts.sort(key=lambda t: t[0])
    return pts


def refine(cand, x0, which):
    from scipy.optimize import minimize
    def f(k):
        g0, gp = gfuncs(cand, np.asarray(k)[None, :])
        return float(g0[0] if which == 0 else gp[0])
    r = minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-14, maxiter=2000))
    x = r.x if r.fun <= f(x0) else np.asarray(x0, float)
    return x, min(r.fun, f(x0)), int(r.nit)


def degeneracy(cand, k, which):
    w = omegas(symbol(cand, np.asarray(k)[None, :]))[0]
    if which == 0:
        return int((np.abs(w) <= 1e-6).sum())
    return int(((np.pi - np.abs(w)) <= 1e-6).sum())


def velocity_record(cand, k, which):
    h = 1e-5; rows = {}
    for a in range(3):
        e = np.zeros(3); e[a] = h
        wp = np.sort(omegas(symbol(cand, (k + e)[None, :]))[0])
        wm = np.sort(omegas(symbol(cand, (k - e)[None, :]))[0])
        if which == 1:
            wp = np.sort(np.mod(wp, 2 * np.pi) - np.pi); wm = np.sort(np.mod(wm, 2 * np.pi) - np.pi)
        sel_p = wp[np.argsort(np.abs(wp))[:degeneracy(cand, k, which)]]
        sel_m = wm[np.argsort(np.abs(wm))[:degeneracy(cand, k, which)]]
        rows['xyz'[a]] = {'omega_plus_over_h': np.sort(sel_p / h).tolist(), 'omega_minus_over_h': np.sort(sel_m / h).tolist()}
    tilt = [float(np.mean(rows[ax]['omega_plus_over_h'] + [-v for v in rows[ax]['omega_minus_over_h']]) / 2) if rows[ax]['omega_plus_over_h'] else 0.0 for ax in 'xyz']
    return {'finite_difference_step': h, 'per_axis': rows, 'tilt': tilt, 'chirality': 'not computed'}


def classify(cand, ctx, cbar, n, nc):
    """Scan, refine and classify one candidate at one knob value."""
    P = ctx.P; lat = cand['lattice']
    lin, G0, GP = scan(cand, n)
    _, G0c, _ = scan(cand, nc)
    n_fine = int((G0 < 1e-6).sum()); n_coarse = int((G0c < 1e-6).sum())
    not_isolated = (n_fine > 2 * n_coarse) if n_coarse > 0 else (n_fine > 2)
    del G0c
    refined = []; skipped = []
    for which, G in ((0, G0), (1, GP)):
        mins = local_minima(G, lin)
        for j, (gv, x0) in enumerate(mins):
            if j < P['S3_maxref']:
                refined.append((which, x0, 'grid_min'))
            else:
                skipped.append({'which': which, 'grid_value': gv, 'k': x0.tolist(),
                                'gamma_dist': cc.gamma_dist(x0, lat)})
    for hp in cc.high_symmetry_points(lat):
        refined.append((0, hp, 'high_symmetry')); refined.append((1, hp, 'high_symmetry'))
    zeros = []; pis = []; gapped = []; gapped_pi = []
    for which, x0, src in refined:
        x, g, nit = refine(cand, x0, which)
        if g <= 1e-9:
            deg = degeneracy(cand, x, which)
            (zeros if which == 0 else pis).append({'k': x.tolist(), 'g': g, 'deg': deg, 'source': src, 'nit': nit})
        else:
            gd = cc.gamma_dist(x, lat)
            (gapped if which == 0 else gapped_pi).append({'k': x.tolist(), 'g': g, 'gamma_dist': gd, 'source': src})
    def reduce(lst):
        classes = []
        for z in lst:
            for cl in classes:
                if cc.equivalent(z['k'], cl['k'], lat):
                    cl['deg'] = max(cl['deg'], z['deg']); cl['n_hits'] += 1
                    break
            else:
                classes.append({'k': z['k'], 'deg': z['deg'], 'n_hits': 1,
                                'is_gamma': cc.gamma_dist(z['k'], lat) < 1e-5})
        return classes
    zc = reduce(zeros); pc = reduce(pis)
    for cl in zc:
        cl['velocity'] = velocity_record(cand, np.array(cl['k']), 0)
    for cl in pc:
        cl['velocity'] = velocity_record(cand, np.array(cl['k']), 1)
    Ns0 = sum(c_['deg'] for c_ in zc); Nsp = sum(c_['deg'] for c_ in pc)
    res = {'grid_n': n, 'grid_n_coarse': nc, 'count_g0_below_1e-6_fine': n_fine,
           'count_g0_below_1e-6_coarse': n_coarse, 'not_isolated': not_isolated,
           'zero_classes': zc, 'pi_classes': pc, 'N_states_0': Ns0, 'N_states_pi': Nsp,
           'N_D_0': Ns0 / 4, 'n_refined': len(refined), 'skipped_minima': skipped}
    # conditions
    c1 = (len(zc) == 1 and zc[0]['is_gamma'] and zc[0]['deg'] in (2, 4) and not not_isolated)
    res['cond1'] = MET if c1 else NOT
    if cbar is None:
        res['cond2'] = UNI; res['cond3'] = NOT if pc else UNI
        res['note_cbar'] = 'cbar0 unavailable from S4 at this knob value'
    else:
        gp_out = [g for g in gapped if g['gamma_dist'] >= 0.3]
        for g in gapped:
            g['Delta_hat'] = g['g'] / cbar
        for g in gapped_pi:
            g['Delta_hat_pi'] = g['g'] / cbar
        thr_g = 0.01 * cbar
        c2 = all(g['g'] / cbar >= 0.01 for g in gp_out)
        c3 = (len(pc) == 0) and all(g['g'] / cbar >= 0.01 for g in gapped_pi)
        # skipped minima rule (implementation note): a skipped minimum whose grid value is below
        # max(2 * 0.01 * cbar0, 1e-6) could hide a sub-threshold minimum or zero.
        risky = [s for s in skipped if s['grid_value'] < max(2 * thr_g, 1e-6)]
        res['skipped_risky'] = len(risky)
        res['cond2'] = MET if c2 else NOT
        res['cond3'] = MET if c3 else NOT
        if risky:
            if res['cond2'] == MET: res['cond2'] = UNI
            if res['cond3'] == MET: res['cond3'] = UNI
            if res['cond1'] == MET: res['cond1'] = UNI
        res['cbar0'] = cbar
    res['gapped_minima'] = gapped; res['pi_gapped_minima'] = gapped_pi
    res['outcome'] = combine([res['cond1'], res['cond2'], res['cond3']])
    return res


def s3_candidate(ctx, name, control_valid):
    P = ctx.P; per = {}
    for kv in knobs(name, 'K7', ctx.mode):
        c = cc.make_candidate(name, kv)
        n, nc = (P['S3_n_stag'], P['S3_nc_stag']) if c['lattice'] == 'stag' else (P['S3_n'], P['S3_nc'])
        with Meter() as mk:
            r = guarded(lambda: classify(c, ctx, cbar_for(ctx, name, kv), n, nc))
        r['knob'] = kv; r.update({'knob_' + k: v for k, v in mk.d().items()})
        if not control_valid:
            r['outcome_raw'] = r.get('outcome'); r['outcome'] = UNI
        per[repr(kv)] = r
    zc = [len(v.get('zero_classes', [])) for v in per.values()]
    return {'per_knob': per, 'control_valid': control_valid,
            'zero_class_count_per_knob': zc,
            'outcome_F1': combine(v['outcome'] for v in per.values()),
            'outcome_V3': MET if (control_valid and all('error' not in v for v in per.values())) else UNI,
            'V3_note': 'V3 cell (implementation note): MET iff the scan completed at every K7 value and the control is valid'}


def step_S3(ctx):
    P = ctx.P
    if ctx.round == 'census':
        with Meter() as m:
            ctrl = naive_control()
            rec = guarded(lambda: classify(ctrl, ctx, None, P['S3_n'], P['S3_nc']))
        zc = rec.get('zero_classes', [])
        valid = (len(zc) == 8 and all(z['deg'] == 4 for z in zc))
        rec['control_valid'] = valid
        rec['outcome'] = 'CONTROL VALID' if valid else UNI
        rec['units'] = 'naive SC Floquet control, k per ell'
        ctx.write_result('_global', 'S3_control', rec, m)
    else:
        valid = bool((ctx.read_result('_global', 'S3_control') or {}).get('control_valid', False))
    cands = CENSUS_CANDS if ctx.round == 'census' else ['RC3']
    for name in cands:
        with Meter() as m:
            rec = guarded(lambda: s3_candidate(ctx, name, valid))
        rec['units'] = cand_units(name)
        if 'outcome' not in rec:
            rec['outcome'] = rec['outcome_F1']
        ctx.write_result(name, 'S3', rec, m)
    return 0


# ===================================================================== S5a

def s5a_evolve_state(c, N, j, src, ncyc):
    """Source e_j * src (restricted to the site set / sublattice j), normalised, evolved
    by U(k)^ncyc (repeated squaring per k-plane, complex128) with complex64 storage."""
    lat = c['lattice']; d = c['d']
    if lat == 'stag':
        M = N // 2
        s = cc.SUBS[j]
        mask = np.zeros((N, N, N), bool)
        mask[s[0]::2, s[1]::2, s[2]::2] = True
        psi = np.where(mask, src, 0.0).astype(np.complex64)
        del mask
        psi /= np.sqrt((np.abs(psi) ** 2).sum())
        phi = np.stack([psi[s_[0]::2, s_[1]::2, s_[2]::2] for s_ in cc.SUBS])   # phi_s(y) = psi(2y+s)
        del psi
        ph = sfft.fftn(phi, axes=(1, 2, 3)); del phi
        q = 2 * np.pi * np.fft.fftfreq(M)
        for i in range(M):
            Q = np.stack(np.meshgrid([q[i]], q, q, indexing='ij'), -1)[0]
            Un = cc.matpow(cc.cell_symbol_stag(c, Q), ncyc)
            ph[:, i] = np.einsum('yzab,byz->ayz', Un, ph[:, i].astype(complex)).astype(np.complex64)
        phi = sfft.ifftn(ph, axes=(1, 2, 3)); del ph
        full = np.zeros((N, N, N), np.complex64)
        for si, s_ in enumerate(cc.SUBS):
            full[s_[0]::2, s_[1]::2, s_[2]::2] = phi[si]
        return full
    kgrid = 2 * np.pi * np.fft.fftfreq(N)
    psi = np.zeros((d, N, N, N), np.complex64)
    if lat == 'bcc':
        par = np.arange(N) % 2
        orbit = (par[:, None, None] == par[None, :, None]) & (par[None, :, None] == par[None, None, :])
        s0 = np.where(orbit, src, 0.0); del orbit
    else:
        s0 = src
    psi[j] = s0 / np.sqrt((np.abs(s0) ** 2).sum()); del s0
    for a in range(d):
        psi[a] = sfft.fftn(psi[a])
    for i in range(N):
        K = np.stack(np.meshgrid([kgrid[i]], kgrid, kgrid, indexing='ij'), -1)[0]
        Un = cc.matpow(symbol(c, K), ncyc)
        psi[:, i] = np.einsum('yzab,byz->ayz', Un, psi[:, i].astype(complex)).astype(np.complex64)
    for a in range(d):
        psi[a] = sfft.ifftn(psi[a])
    return psi

def s5a_one(ctx, name, kv, sigma, N, cbar):
    """One candidate, knob, sigma. Box N in grid units (even)."""
    c = cc.make_candidate(name, kv); lat = c['lattice']; d = c['d']
    ell = cc.ell_grid(lat)
    ncyc = int(round(6 * sigma / cbar))
    R = cbar * ncyc
    coord = np.fft.fftfreq(N, 1.0 / N)                    # integer coords in (-N/2, N/2]
    coord = np.where(coord >= N / 2, coord - N, coord)    # [-N/2, N/2)
    xl = coord / ell                                      # in ell
    half_box = N / 2 / ell
    if lat == 'bcc':
        par = (np.arange(N) % 2)
    kgrid = 2 * np.pi * np.fft.fftfreq(N)                 # per grid unit in [-pi, pi)
    ktil = kgrid * ell                                    # per ell
    # reference
    def plane_geom(i):
        X, Y, Z = xl[i], xl[:, None], xl[None, :]
        r = np.sqrt(X * X + Y * Y + Z * Z)
        rs = np.where(r > 0, r, 1.0)
        K4 = 2.5 * ((X / rs) ** 4 + (Y / rs) ** 4 + (Z / rs) ** 4) - 1.5
        K4 = np.where(r > 0, K4, 0.0)
        face = (np.abs(X) > half_box - 2 * sigma) | (np.abs(Y) > half_box - 2 * sigma) | (np.abs(Z) > half_box - 2 * sigma)
        if lat == 'bcc':
            site = (par[i] == par[:, None]) & (par[:, None] == par[None, :])
        else:
            site = np.ones((N, N), bool)
        return X, Y, Z, r, K4, face, site
    def observables(rho):
        tot = 0.0; out = 0.0; wsum = 0.0; wk4 = 0.0; Tm = np.zeros((3, 3)); face_p = 0.0
        for i in range(N):
            X, Y, Z, r, K4, face, site = plane_geom(i)
            p = np.where(site, rho[i], 0.0)
            tot += p.sum(); out += p[r > R + 3 * sigma].sum(); face_p += p[face].sum()
            W = np.abs(r - R) <= 3 * sigma
            pw = np.where(W, p, 0.0)
            wsum += pw.sum(); wk4 += (pw * K4).sum()
            XX = np.broadcast_to(X, (N, N)); YY = np.broadcast_to(Y, (N, N)); ZZ = np.broadcast_to(Z, (N, N))
            comps = [XX, YY, ZZ]
            for a in range(3):
                for b in range(a, 3):
                    v = (pw * comps[a] * comps[b]).sum(); Tm[a, b] += v
                    if a != b: Tm[b, a] += v
        tr = np.trace(Tm)
        Q2 = float(np.abs(np.linalg.eigvalsh(Tm - tr / 3 * np.eye(3))).max() / tr) if tr > 0 else float('nan')
        return {'P_out': out / tot, 'A': wk4 / wsum if wsum > 0 else float('nan'), 'Q2': Q2,
                'P_face': face_p / tot, 'W_weight': wsum / tot}
    # Gaussian on the full grid
    g1 = np.exp(-xl ** 2 / (2 * sigma ** 2))
    g = (g1[:, None, None] * g1[None, :, None] * g1[None, None, :]).astype(np.complex64)
    gh = sfft.fftn(g); del g
    rho_ref = np.zeros((N, N, N))
    kk = np.sqrt(ktil[:, None, None] ** 2 + ktil[None, :, None] ** 2 + ktil[None, None, :] ** 2).astype(np.float32)
    phase = (cbar * kk * ncyc).astype(np.float32)
    rho_ref += np.abs(sfft.ifftn(np.cos(phase) * gh)) ** 2
    kks = np.where(kk > 0, kk, 1.0).astype(np.float32)
    for a in range(3):
        sh = [1, 1, 1]; sh[a] = N
        ki = ktil.reshape(sh).astype(np.float32)
        rho_ref += np.abs(sfft.ifftn((np.sin(phase) * ki / kks) * gh)) ** 2
    del kk, phase, kks, gh
    ref = observables(rho_ref); del rho_ref
    # lattice: one internal state at a time
    rho = np.zeros((N, N, N))
    src = (g1[:, None, None] * g1[None, :, None] * g1[None, None, :])
    for j in range(d):
        psi = s5a_evolve_state(c, N, j, src, ncyc)
        if lat == 'stag':
            rho += np.abs(psi) ** 2 / d
        else:
            rho += (np.abs(psi) ** 2).sum(0) / d
        del psi
    lt = observables(rho); del rho
    wrap_ok = lt['P_face'] <= 1e-7 and ref['P_face'] <= 1e-7
    return {'sigma': sigma, 'N_grid': N, 'cycles': ncyc, 'R_front': R, 'lattice_obs': lt, 'reference_obs': ref,
            'Lambda': lt['P_out'] - ref['P_out'], 'dA': lt['A'] - ref['A'], 'dQ2': lt['Q2'] - ref['Q2'],
            'wrap_ok': bool(wrap_ok)}


def slope(vals, xs):
    v = np.maximum(np.abs(np.array(vals, float)), 1e-10)   # clamp (implementation note)
    return float(np.polyfit(np.log(xs), np.log(v), 1)[0])


def s5a_candidate(ctx, name):
    P = ctx.P; per = {}
    for kv in knobs(name, 'K3', ctx.mode):
        cbar = cbar_for(ctx, name, kv)
        lat = cc.make_candidate(name, kv)['lattice']
        boxes = P['S5a_box_bcc'] if lat == 'bcc' else P['S5a_box_sc']
        if cbar is None:
            per[repr(kv)] = {'knob': kv, 'outcome': UNI, 'reason': 'cbar0 unavailable from S4'}
            continue
        rows = []
        for sig, N in zip(P['S5a_sigmas'], boxes):
            with Meter() as mm:
                r = guarded(lambda: s5a_one(ctx, name, kv, sig, N, cbar))
            r.update({'sigma': sig}); r.update({'res_' + k: v for k, v in mm.d().items()})
            rows.append(r)
        rec = {'knob': kv, 'cbar0': cbar, 'rows': rows}
        if any('error' in r or not r.get('wrap_ok', False) for r in rows):
            rec['outcome'] = UNI; rec['reason'] = 'a sigma errored or failed the wrap control'
        else:
            sig = np.array([r['sigma'] for r in rows])
            ok = True; obs = {}
            for key, lim in (('dA', 1e-2), ('dQ2', 1e-2), ('Lambda', 1e-3)):
                vals = [r[key] for r in rows]
                below = all(abs(v) <= 1e-10 for v in vals)
                sl = None if below else slope(vals, sig)
                last_ok = abs(vals[-1]) <= lim
                okk = below or (last_ok and sl <= -1.5)
                obs[key] = {'values': vals, 'below_floor': below, 'slope': sl, 'last_ok': last_ok, 'ok': okk}
                ok = ok and okk
            rec['observables'] = obs; rec['outcome'] = MET if ok else NOT
        per[repr(kv)] = rec
    return {'per_knob': per, 'outcome_F5a': combine(v['outcome'] for v in per.values())}


def step_S5a(ctx):
    cands = CENSUS_CANDS if ctx.round == 'census' else ['RC3']
    for name in cands:
        with Meter() as m:
            rec = guarded(lambda: s5a_candidate(ctx, name))
        rec['units'] = cand_units(name)
        if 'outcome' not in rec:
            rec['outcome'] = rec['outcome_F5a']
        ctx.write_result(name, 'S5a', rec, m)
    return 0


# ===================================================================== S5b
def green_fft(lat, N):
    k = 2 * np.pi * np.fft.fftfreq(N)
    kr = 2 * np.pi * np.fft.rfftfreq(N)
    cx = np.cos(k)[:, None, None]; cy = np.cos(k)[None, :, None]; cz = np.cos(kr)[None, None, :]
    if lat == 'sc':
        Lk = 2 * (1 - cx) + 2 * (1 - cy) + 2 * (1 - cz)
    else:
        Lk = 8 * (1 - cx * cy * cz)
    zero = np.abs(Lk) < 1e-12
    Lk = np.where(zero, 1.0, Lk)
    Gk = np.where(zero, 0.0, 1.0 / Lk)
    n_removed = int(zero.sum())
    G = sfft.irfftn(Gk, s=(N, N, N), axes=(0, 1, 2))
    return G, n_removed


def shell_obs(lat, N, G, r):
    ell = cc.ell_grid(lat)
    c = np.arange(N); c = np.where(c >= N // 2, c - N, c)
    Yp, Zp = np.meshgrid(c, c, indexing='ij')
    xs_l = []; gs_l = []
    for i in range(N):            # plane by plane to bound memory
        rr = np.sqrt(c[i] ** 2 + Yp ** 2 + Zp ** 2)
        sel = np.abs(rr / ell - r) <= 0.5
        if lat == 'bcc':
            sel &= ((c[i] % 2) == (Yp % 2)) & ((Yp % 2) == (Zp % 2))
        if sel.any():
            xs_l.append(np.stack([np.full(int(sel.sum()), c[i]), Yp[sel], Zp[sel]], -1))
            gs_l.append(G[i][sel])
    x = np.concatenate(xs_l).astype(float); Gs = np.concatenate(gs_l)
    rs = np.linalg.norm(x, axis=1)
    sel = slice(None)
    nh = x / rs[:, None]
    K4 = 2.5 * (nh ** 4).sum(-1) - 1.5
    w = rs * Gs
    A = float((K4 * w).sum() / w.sum()); Aref = float(K4.mean())
    def quad(wt):
        T = np.einsum('n,na,nb->ab', wt, nh, nh); tr = np.trace(T)
        return float(np.abs(np.linalg.eigvalsh(T - tr / 3 * np.eye(3))).max() / tr)
    return {'r': r, 'n_sites': int(len(rs)), 'A_load': A, 'A_ref': Aref, 'dA_load': A - Aref,
            'Q2_record': quad(w) - quad(np.ones_like(w))}, x


def bessel_G(x):
    from scipy.special import ive
    from scipy.integrate import quad
    a = [int(abs(v)) for v in x]
    f = lambda t: ive(a[0], 2 * t) * ive(a[1], 2 * t) * ive(a[2], 2 * t)
    v1, _ = quad(f, 0, 50, epsrel=1e-10, epsabs=0, limit=500)
    v2, _ = quad(f, 50, np.inf, epsrel=1e-10, epsabs=0, limit=500)
    return v1 + v2


def step_S5b(ctx):
    P = ctx.P
    with Meter() as m:
        def body():
            out = {}
            for lat, boxes in (('sc', P['S5b_box_sc']), ('bcc', P['S5b_box_bcc'])):
                per_box = {}
                for N in boxes:
                    G, nrem = green_fft(lat, N)
                    rows = [shell_obs(lat, N, G, r)[0] for r in P['S5b_r']]
                    per_box[str(N)] = {'n_gamma_modes_removed': nrem, 'shells': rows}
                    if lat == 'sc' and N == boxes[-1]:
                        rmax = P['S5b_r'][-1]
                        o, xs = shell_obs(lat, N, G, rmax)
                        cache = {}; Gb = []
                        for xv in xs:
                            key = tuple(sorted(int(abs(v)) for v in xv))
                            if key not in cache:
                                cache[key] = bessel_G(key)
                            Gb.append(cache[key])
                        Gb = np.array(Gb); rs = np.linalg.norm(xs, axis=1)
                        nh = xs / rs[:, None]; K4 = 2.5 * (nh ** 4).sum(-1) - 1.5
                        w = rs * Gb
                        dA_b = float((K4 * w).sum() / w.sum() - K4.mean())
                        out['method_control'] = {'r': rmax, 'dA_bessel': dA_b, 'dA_fft': o['dA_load'],
                                                 'n_unique_sites': len(cache),
                                                 'ok': abs(dA_b - o['dA_load']) <= 0.1 * abs(dA_b),
                                                 'boundary': 'infinite lattice (Bessel integral)'}
                    del G
                big, small = per_box[str(boxes[-1])], per_box[str(boxes[0])]
                a1 = big['shells'][-1]['dA_load']; a0 = small['shells'][-1]['dA_load']
                box_ok = abs(a1 - a0) <= 0.1 * abs(a1) or abs(a1 - a0) <= 1e-6
                vals = [s['dA_load'] for s in big['shells']]
                below = all(abs(v) <= 1e-10 for v in vals)
                sl = None if below else slope(vals, np.array(P['S5b_r'], float))
                gate = below or (abs(vals[-1]) <= 1e-2 and sl <= -1.5)
                out[lat] = {'boxes': per_box, 'box_control': {'dA12_big': a1, 'dA12_small': a0, 'ok': box_ok},
                            'gated_values': vals, 'slope': sl, 'below_floor': below, 'gate_raw': MET if gate else NOT}
            controls_ok = out['sc']['box_control']['ok'] and out['bcc']['box_control']['ok'] and out['method_control']['ok']
            out['controls_ok'] = controls_ok
            for lat in ('sc', 'bcc'):
                out[lat]['outcome'] = out[lat]['gate_raw'] if controls_ok else UNI
            out['outcome'] = 'see per-lattice outcomes'
            return out
        rec = guarded(body)
    rec['units'] = 'SC: ell = face link; BCC: ell = a*sqrt(3)/2, grid a/2'
    rec['boundary'] = 'periodic (FFT); infinite lattice for the method control'
    ctx.write_result('_global', 'S5b', rec, m)
    return 0


# ===================================================================== S6
class KSpace:
    """k-space representation for observables and the exact cross-check."""
    def __init__(self, cand, L):
        self.c = cand; self.L = L; lat = cand['lattice']; self.lat = lat
        if lat == 'stag':
            M = L // 2; q = 2 * np.pi * np.fft.fftfreq(M)
            Q = np.stack(np.meshgrid(q, q, q, indexing='ij'), -1).reshape(-1, 3)
            self.U = cc.cell_symbol_stag(cand, Q)
            self.shape = (M, M, M)
        else:
            k = 2 * np.pi * np.fft.fftfreq(L)
            K = np.stack(np.meshgrid(k, k, k, indexing='ij'), -1).reshape(-1, 3)
            self.U = symbol(cand, K)
            self.shape = (L, L, L)
        from scipy.linalg import schur
        Z = np.empty_like(self.U); lam = np.empty(self.U.shape[:2], complex)
        for i in range(self.U.shape[0]):
            T, Zi = schur(self.U[i], output='complex')
            Z[i] = Zi; lam[i] = np.diag(T)
        self.Z = Z; self.lam = lam
        w = -np.angle(lam); self.w = np.where(w <= -np.pi, w + 2 * np.pi, w)

    def to_k(self, psi):
        """psi (B,...) real-space -> (B, nk, d) amplitudes, normalised so sum |.|^2 = Q."""
        lat = self.lat
        if lat == 'stag':
            B = psi.shape[0]
            phi = np.stack([psi[:, s[0]::2, s[1]::2, s[2]::2] for s in cc.SUBS], 1)  # (B,8,M,M,M)
            ph = sfft.fftn(phi, axes=(2, 3, 4)) / np.sqrt(np.prod(self.shape))
            return ph.reshape(B, 8, -1).transpose(0, 2, 1)
        if lat == 'bcc':
            B, d = psi.shape[:2]; L = self.L; M = L // 2
            full = np.zeros((B, d, L, L, L), complex)
            full[:, :, 0::2, 0::2, 0::2] = psi[:, :, 0]
            full[:, :, 1::2, 1::2, 1::2] = psi[:, :, 1]
            ph = sfft.fftn(full, axes=(2, 3, 4)) / np.sqrt(L ** 3)
            return ph.reshape(B, d, -1).transpose(0, 2, 1)
        B, d = psi.shape[:2]
        ph = sfft.fftn(psi, axes=(2, 3, 4)) / np.sqrt(self.L ** 3)
        return ph.reshape(B, d, -1).transpose(0, 2, 1)

    def from_k(self, a):
        lat = self.lat; B = a.shape[0]
        if lat == 'stag':
            ph = a.transpose(0, 2, 1).reshape((B, 8) + self.shape) * np.sqrt(np.prod(self.shape))
            phi = sfft.ifftn(ph, axes=(2, 3, 4))
            psi = np.zeros((B, self.L, self.L, self.L), complex)
            for si, s in enumerate(cc.SUBS):
                psi[:, s[0]::2, s[1]::2, s[2]::2] = phi[:, si]
            return psi
        d = a.shape[2]; L = self.L
        full = sfft.ifftn(a.transpose(0, 2, 1).reshape(B, d, L, L, L) * np.sqrt(L ** 3), axes=(2, 3, 4))
        if lat == 'bcc':
            M = L // 2
            out = np.zeros((B, d, 2, M, M, M), complex)
            out[:, :, 0] = full[:, :, 0::2, 0::2, 0::2]; out[:, :, 1] = full[:, :, 1::2, 1::2, 1::2]
            return out
        return full

    def obs(self, psi):
        a = self.to_k(psi)                                   # (B,nk,d)
        c = np.einsum('kji,bkj->bki', self.Z.conj(), a)      # Z^dag a
        n = np.abs(c) ** 2
        E = (n * self.w[None]).sum((1, 2)); Eabs = (n * np.abs(self.w)[None]).sum((1, 2))
        Q = (np.abs(psi) ** 2).reshape(psi.shape[0], -1).sum(1)
        return Q, E, Eabs, n

    def exact(self, psi, ncyc):
        a = self.to_k(psi)
        c = np.einsum('kji,bkj->bki', self.Z.conj(), a) * (self.lam ** ncyc)[None]
        return self.from_k(np.einsum('kij,bkj->bki', self.Z, c))


def s6_states(eng, ci):
    c = eng.c; L = eng.L; lat = c['lattice']
    s1 = rand_state(eng, 1, 20261114 + 100 * ci + 1)[0]
    ell = cc.ell_grid(lat); sig = 2.0
    if lat == 'bcc':
        X = eng.cart(); dd = X % L; dd = np.minimum(dd, L - dd) / ell
        g = np.exp(-(dd ** 2).sum(-1) / (2 * sig ** 2))
        s2 = np.zeros_like(s1); s2[0] = g
        s3 = np.zeros_like(s1); s3[0, 0, 0, 0, 0] = 1
    else:
        x = np.stack(np.meshgrid(*(np.arange(L),) * 3, indexing='ij'), -1)
        dd = np.minimum(x % L, L - x % L)
        g = np.exp(-(dd ** 2).sum(-1) / (2 * sig ** 2))
        if lat == 'stag':
            s2 = np.where((x % 2 == 0).all(-1), g, 0.0).astype(complex)   # sublattice e_0
            s3 = np.zeros_like(s1); s3[0, 0, 0] = 1
        else:
            s2 = np.zeros_like(s1); s2[0] = g
            s3 = np.zeros_like(s1); s3[0, 0, 0, 0] = 1
    s2 = s2 / np.sqrt((np.abs(s2) ** 2).sum())
    return np.stack([s1, s2, s3])


def s6_candidate(ctx, name):
    P = ctx.P; ci = cc.CAND_INDEX[name]; kv = midpoint(name)
    if ctx.mode == 'smoke':
        kv = knobs(name, 'K3', 'smoke')[0]
    c = cc.make_candidate(name, kv)
    L = P['S6_L_bcc'] if c['lattice'] == 'bcc' else P['S6_L']
    eng = cc.make_engine(c, L); ks = KSpace(c, L)
    lpc = len(c['layers']); ncyc = int(math.ceil(P['S6_layers'] / lpc)); nlay = ncyc * lpc
    psi0 = s6_states(eng, ci)
    Q0, E0, Ea0, n0 = ks.obs(psi0)
    targets = sorted(set([1, 10, 100, 1000, 10000, ncyc]))
    targets = sorted(set(min(t, ncyc) for t in targets))
    psi = psi0.copy(); chk = {}
    for t in range(1, ncyc + 1):
        psi = cc.run_cycle(eng, psi)
        if t in targets:
            Q, E, Ea, n = ks.obs(psi)
            chk[t] = {'dQ': np.abs(Q - Q0).tolist(), 'dE': (np.abs(E - E0) / Ea0).tolist(),
                      'dn': (np.abs(n - n0).reshape(3, -1).max(1) / Q0).tolist()}
    band = 10 * nlay * EPS64
    last = chk[ncyc]
    ok = all(max(last[k]) <= band for k in ('dQ', 'dE', 'dn'))
    ex = ks.exact(psi0, ncyc)
    xdev = float(np.abs(ex - psi).max())
    rec = {'knob': kv, 'grid_L': L, 'cycles': ncyc, 'layers': nlay, 'band_C': band,
           'states': ['S1 random seed %d' % (20261114 + 100 * ci + 1), 'S2 Gaussian sigma=2 ell e0', 'S3 delta e0'],
           'checkpoints': chk, 'cross_check_max_abs': xdev, 'cross_check_ok': xdev <= 1e-9}
    rec['outcome_raw'] = MET if ok else NOT
    rec['outcome_V4'] = rec['outcome_raw'] if xdev <= 1e-9 else UNI
    return rec


def step_S6(ctx):
    cands = CENSUS_CANDS if ctx.round == 'census' else ['RC3']
    for name in cands:
        with Meter() as m:
            rec = guarded(lambda: s6_candidate(ctx, name))
        rec['units'] = cand_units(name)
        if 'outcome' not in rec:
            rec['outcome'] = rec['outcome_V4']
        ctx.write_result(name, 'S6', rec, m)
    return 0


# ===================================================================== S7
SIMPLE = {'B0': (4, 1), 'C1': (4, 1), 'C2': (1, 1), 'C3': (4, 1), 'C4': (2, 0), 'RC3': (4, 1)}


def per_knob_labels(r, key='outcome'):
    if not r or 'per_knob' not in r:
        return None
    return {k: v.get(key, UNI) for k, v in r['per_knob'].items()}


def row_for(ctx, name, s2_step):
    g = lambda st: ctx.read_result(name, st) or {}
    S1, S2, S3, S4, S5a, S6 = g('S1'), g(s2_step), g('S3'), g('S4'), g('S5a'), g('S6')
    S5b = ctx.read_result('_global', 'S5b') or {}
    lat = 'bcc' if name == 'B0' else 'sc'
    row = {}
    row['F1'] = S3.get('outcome_F1', UNI)
    row['F3'] = S1.get('outcome_F3', UNI)
    row['F4'] = S4.get('outcome_F4', UNI)
    row['F5a'] = S5a.get('outcome_F5a', UNI)
    row['F5b'] = (S5b.get(lat) or {}).get('outcome', UNI)
    row['V1'] = S1.get('outcome_V1', UNI)
    row['V2'] = S2.get('outcome', UNI)
    row['V3'] = S3.get('outcome_V3', UNI)
    row['V4'] = S6.get('outcome_V4', UNI)
    F5 = combine([row['F5a'], row['F5b']])
    if name == 'B0':
        row['F2'] = MET; f2note = 'no position-dependent factor or fixed order within a layer'
    else:
        lab = combine([row['F4'], F5])
        row['F2'] = lab
        f2note = ('fixed layer order (not a fixed direction provided F4 and F5 incl. dQ2 are MET, OD6(a))' +
                  ('; KS phases, checkerboard standing (OD5(a))' if name == 'C2' else ''))
    comp, nk = SIMPLE[name]
    row['simplicity'] = MET if (comp <= 4 and nk <= 2) else NOT
    # knob rule
    if name == 'C4':
        row['knob rule'] = 'not applicable (no knob)'
    else:
        labs = []
        for r in (S1, S2, S3, S4, S5a):
            pk = per_knob_labels(r)
            if pk is None:
                labs.append(UNI)
            else:
                labs += list(pk.values())
        zc = S3.get('zero_class_count_per_knob')
        same_zero = zc is not None and len(set(zc)) == 1
        labs.append(S6.get('outcome_V4', UNI))
        if any(l == NOT for l in labs) or (zc is not None and not same_zero):
            row['knob rule'] = NOT
        elif all(l == MET for l in labs) and same_zero:
            row['knob rule'] = MET
        else:
            row['knob rule'] = UNI
    return row, {'F2_factors': f2note, 'components': comp, 'declared_knobs': nk}


COLS = ['F1', 'F2', 'F3', 'F4', 'F5a', 'F5b', 'knob rule', 'simplicity', 'V1', 'V2', 'V3', 'V4']


def step_S7(ctx):
    with Meter() as m:
        def body():
            names = list(CENSUS_CANDS) + (['RC3'] if ctx.round == 'repair' else [])
            table = {}; notes = {}
            for n in names:
                table[n], notes[n] = row_for(ctx, n, 'S2b' if n == 'RC3' else 'S2')
            sc = [n for n in names if n != 'B0']
            def all_met(row):
                return all(row[c] == MET or (c == 'knob rule' and row[c].startswith('not applicable')) for c in COLS)
            def any_not(row):
                return any(row[c] == NOT for c in COLS)
            if any(all_met(table[n]) for n in sc):
                allsc = 'yes'
            elif all(any_not(table[n]) for n in sc):
                allsc = 'no'
            else:
                allsc = UNI
            if allsc == 'yes':
                trig = ('At least one simple cubic candidate is MET in every column of this table; '
                        'the trigger condition (no simple cubic candidate passes) does not hold in this round.')
            elif allsc == 'no':
                trig = ('No simple cubic candidate is MET in every column of this table; the trigger condition '
                        '(no simple cubic candidate passes F1-F5, the knob rule and the simplicity test) holds in this round, '
                        'to be read alongside the B0 row.')
            else:
                trig = ('No simple cubic candidate is MET in every column, and at least one candidate row has '
                        'UNINFORMATIVE cells without a NOT MET cell; the trigger cannot be read from this table.')
            c3f1 = table['C3']['F1']
            return {'table': table, 'columns': COLS, 'row_notes': notes,
                    'all_SC_criteria_MET_by_at_least_one_candidate': allsc,
                    'B0_row': table['B0'], 'trigger_statement': trig,
                    'C3_F1_cell': c3f1,
                    'repair_round_condition_met': (c3f1 == NOT) if ctx.round == 'census' else None,
                    'outcome': 'assembled'}
        rec = guarded(body)
    rec['units'] = 'assembly, no new computation'
    ctx.write_result('_global', 'S7' if ctx.round == 'census' else 'S7_repair', rec, m)
    # human-readable table
    if 'table' in rec:
        lines = ['| Candidate | ' + ' | '.join(COLS) + ' |', '|' + '---|' * (len(COLS) + 1)]
        for n, row in rec['table'].items():
            lines.append('| ' + n + ' | ' + ' | '.join(row[c] for c in COLS) + ' |')
        lines += ['', 'All SC criteria MET by at least one candidate: ' + rec['all_SC_criteria_MET_by_at_least_one_candidate'],
                  '', 'Trigger statement (from this table only): ' + rec['trigger_statement']]
        if ctx.mode == 'smoke':
            lines.insert(0, 'NOT CENSUS - tiny smoke test\n')
        p = ctx.path('_global', 'S7' if ctx.round == 'census' else 'S7_repair', 'READOUT.md')
        with open(p, 'w') as f:
            f.write('\n'.join(lines) + '\n')
    return 0


STEPS = {'S0': step_S0, 'S1': step_S1, 'S2': step_S2, 'S2b': step_S2, 'S3': step_S3, 'S4': step_S4,
         'S5a': step_S5a, 'S5b': step_S5b, 'S6': step_S6, 'S7': step_S7}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['census', 'smoke'], required=True)
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--step', required=True)
    ap.add_argument('--round', choices=['census', 'repair'], default='census')
    ap.add_argument('--code-sums-sha', required=True)
    a = ap.parse_args()
    if sha256_file(R1_PATH) != R1_SHA:
        print('design sha256 mismatch', file=sys.stderr); return 20
    if a.mode == 'census' and a.run_dir.startswith('/workspace/L0p_census_r1_smoke'):
        return 21
    if a.mode == 'smoke' and a.run_dir.startswith('/workspace/runs_l0p'):
        print('smoke must not write into runs_l0p', file=sys.stderr); return 22
    ctx = Ctx(a)
    return STEPS[a.step](ctx)


if __name__ == '__main__':
    sys.exit(main())
