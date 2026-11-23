#!/usr/bin/env python3
"""L1.2 harness, run 20261112_l12_7e09b7c4. Usage: l12.py <S0|S1|S2|S3|S4|S5|G0END> .
Loads the frozen generating stack unchanged through a read-only path redirect (pre-reg decision 3)."""
import os, sys, json, time, hashlib, builtins, itertools, io, contextlib, platform
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FROZ = os.path.join(RUN, 'frozen', 'qca'); F71 = os.path.join(RUN, 'frozen', 'f71c782e')
OUT = os.path.join(RUN, 'out')
PINS = {  # design §1 + pre-reg pins
 'frozen/qca/dw.py':'769833f0393dc1599d5944f6a2837c6ff5ac207ce6ca169eaa2ba9b2ca5fd651',
 'frozen/qca/dirac4s.py':'4db41fe71ce2844f58f1c61c3c84a768b37b82de1bd546a468d3980c3f0627b4',
 'frozen/qca/dirac4.py':'9f01ea8f10947eb6a30506e1499de22e373fc7e1a25fa2689e38c873e2b5aedd',
 'frozen/qca/sym.py':'7b1bbafd4b01464c8f4d4643582c60994f34ed3e119c4167625f2e5905131764',
 'frozen/qca/dw_gscan.py':'5bf6af5d089fd17dbe922f335855e9bf961dc731be4025b591e3e0ff16bf938e',
 'frozen/qca/dw_final.py':'48046ea5332a12322d05ec11a0ea733dc920e05b6f7948a5387904bb43fc6aa1',
 'frozen/qca/dirac4_checks.py':'4e316d9895f035966bb0aa269216dcc38c3986c50c5118907ab609af8e519c05',
 'frozen/f71c782e/dirac4.py':'f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff',
 'design/L1_2_RUN_DESIGN.md':'7e09b7c42bf0b0b44db0057bc7a23c25add9503c441c163f47defabbe93f679b',
 'inputs/PREREGISTRATION.md':'733752444dfdbaab68654e583b15fdc97619883224fc30357f8ecba998747239',
 'inputs/L1_2_DECISIONS.txt':'c3225f353a1ad68956e2d39443814586b8c6e62ce862dced70e9c1f5aa17cf4e',
 'inputs/space-ledger-v2.md':'8cbb94ec481b3332f074ea028505478dd2d576a8b5d60915f072b653ab6aad70',
 # report-only generators, pinned at staging (box /workspace/qca copies)
 'frozen/qca/dw_ring.py':'8cbd5eb07af30663f48331bb96964c446ddf6876b3de8dd6f1a4d7c551b2b43b',
 'frozen/qca/dw_real.py':'276c5fdc225320ebddc8970602d03be73d56c16851cfcba04966b606e4e737f8',
}
def sha(p): return hashlib.sha256(open(os.path.join(RUN, p), 'rb').read()).hexdigest()
_open = builtins.open
REDIRECTS = []
def ropen(f, *a, **k):
    if isinstance(f, str):
        if f.startswith('/workspace/qca/'):
            n = os.path.join(FROZ, f[len('/workspace/qca/'):]); REDIRECTS.append((f, n)); f = n
        elif f == 'sym.py':
            n = os.path.join(FROZ, 'sym.py'); REDIRECTS.append((f, n)); f = n
    return _open(f, *a, **k)
builtins.open = ropen
import numpy as np
from scipy.optimize import minimize
def load(name='dw.py'):
    g = {'__name__': '__l12_' + name}
    exec(compile(open('/workspace/qca/' + name).read(), '/workspace/qca/' + name, 'exec'), g)
    return g
def dump(step, obj):
    d = os.path.join(OUT, step); os.makedirs(d, exist_ok=True)
    json.dump(obj, _open(os.path.join(d, step + '.json'), 'w'), indent=1, default=float)
def stop(msg):
    print('STOP:', msg, flush=True); sys.exit(3)
PHI = 1.4
EDGE12 = []
for z in range(3):
    for s1 in (1, -1):
        for s2 in (1, -1):
            v = [s1*np.pi, s2*np.pi]; v.insert(z, 0.0); EDGE12.append(np.array(v))
assert len(EDGE12) == 12
DIRS13 = [np.array(x, float)/np.linalg.norm(x) for x in ([1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,1,1],[1,-1,1],[-1,1,1],[1,1,-1],[1,2,3],[3,1,2],[2,3,1])]
def recip_dist(x, p):  # distance from x to p modulo pi*g, g integer triple of even sum
    best = 9e9
    for g in itertools.product(range(-3, 4), repeat=3):
        if sum(g) % 2: continue
        best = min(best, float(np.linalg.norm(np.asarray(x) - np.asarray(p) - np.pi*np.array(g))))
    return best

# ---------------------------------------------------------------- S0
def S0():
    r = {'platform': platform.platform(), 'python': sys.version, 'numpy': np.__version__,
         'scipy': __import__('scipy').__version__, 'hostname': platform.node()}
    r['P0'] = {p: dict(expected=h, actual=sha(p), ok=sha(p) == h) for p, h in PINS.items()}
    r['P0_pass'] = all(v['ok'] for v in r['P0'].values()); print('P0', r['P0_pass'], flush=True)
    dump('S0', r)
    if not r['P0_pass']: stop('P0 hash mismatch')
    g = load('dw.py'); floq = g['floq']; dist_gamma = g['dist_gamma']; periodS = g['periodS']
    rng = np.random.default_rng(20261112)
    # P1 unitarity
    K = rng.uniform(-np.pi, np.pi, (50, 3)); P1 = {}
    for Ns in (2, 8, 16, 32):
        for b in (0.1, 0.2, 0.25):
            U = floq(K, Ns, PHI, b); D = np.einsum('nji,njk->nik', U.conj(), U) - np.eye(4*Ns)
            P1[f'Ns{Ns}_b{b}'] = dict(max_inf_norm=float(np.abs(D).sum(-1).max()), max_abs_entry=float(np.abs(D).max()))
    r['P1'] = P1; r['P1_pass'] = all(v['max_inf_norm'] <= 1e-12 for v in P1.values()); print('P1', r['P1_pass'], flush=True)
    # P2 one-orbit periodicity
    K2 = rng.uniform(-np.pi, np.pi, (20, 3)); sh = [np.pi*np.array(v, float) for v in ([1,1,0],[1,0,1],[0,1,1])]
    r['P2_maxdiff'] = max(float(np.abs(floq(K2 + s, 4, PHI, 0.2) - floq(K2, 4, PHI, 0.2)).max()) for s in sh)
    r['P2_pass'] = r['P2_maxdiff'] <= 1e-13; print('P2', r['P2_maxdiff'], flush=True)
    # P3
    r['P3_dist_gamma_pi_pi_0'] = float(dist_gamma(np.array([[np.pi, np.pi, 0.]]))[0])
    r['P3_dist_gamma_pi2'] = float(dist_gamma(np.array([[np.pi/2]*3]))[0])
    r['P3_pass'] = r['P3_dist_gamma_pi_pi_0'] == 0.0 and r['P3_dist_gamma_pi2'] > 0.3
    # P4 sum-form diagnostic at r=0 (frozen f71c782e U_cycle) + chain
    sys.path.insert(0, F71); import dirac4 as F
    assert os.path.abspath(F.__file__) == os.path.join(F71, 'dirac4.py')
    U0 = F.U_cycle(np.zeros(3), wilson_mass=0.0)
    r['P4_Ucycle_r0_edge_vs_Gamma'] = max(float(np.abs(F.U_cycle(L, wilson_mass=0.0) - U0).max()) for L in EDGE12)
    C0 = floq(np.zeros((1, 3)), 4, PHI, 0.2)[0]
    r['P4_chain_Ns4_b0.2_edge_vs_Gamma'] = max(float(np.abs(floq(L[None], 4, PHI, 0.2)[0] - C0).max()) for L in EDGE12)
    r['P4_pass'] = r['P4_Ucycle_r0_edge_vs_Gamma'] <= 1e-13 and r['P4_chain_Ns4_b0.2_edge_vs_Gamma'] <= 1e-13
    # G0b
    Kg = np.array([[0, 0, 0], [0.05, 0, 0], [0.1, 0.1, 0.1]], float)
    Uc = floq(Kg, 16, PHI, 0.2); Ub, _ = periodS(Kg, 0.0, PHI)
    r['G0b_chain'] = float(np.abs(np.einsum('nji,njk->nik', Uc.conj(), Uc) - np.eye(64)).sum(-1).max())
    r['G0b_cycle'] = float(np.abs(np.einsum('nji,njk->nik', Ub.conj(), Ub) - np.eye(4)).sum(-1).max())
    r['G0b_pass'] = max(r['G0b_chain'], r['G0b_cycle']) <= 1e-12
    # G1
    om, _ = g['spec'](np.zeros((1, 3)), 16, PHI, 0.2, 0.0)
    r['G1_residual_m0_0_Ns16'] = float(np.sort(abs(om[0]))[0]); r['G1_pass'] = r['G1_residual_m0_0_Ns16'] <= 1e-14
    r['redirects'] = sorted(set(map(tuple, REDIRECTS)))
    # timing of one Ns=16 grid point (before S3)
    def low16(k, b=0.2): om, _ = g['spec'](k[None], 16, PHI, b, 0.0); return float(np.sort(abs(om[0]))[0])
    k1 = np.array([0.3, -1.1, 2.0]); low16(k1)
    t = time.process_time(); tw = time.time()
    for _ in range(200): low16(k1)
    single = (time.process_time() - t)/200; single_w = (time.time() - tw)/200
    Kb = rng.uniform(-np.pi, np.pi, (2000, 3)); t = time.process_time()
    np.sort(np.abs(np.angle(np.linalg.eigvals(floq(Kb, 16, PHI, 0.2)))), -1)[:, 0]
    batch = (time.process_time() - t)/2000
    npts = 129**3 * 4
    r['timing_Ns16_grid_point'] = dict(single_point_cpu_s=single, single_point_wall_s=single_w, batched_per_point_cpu_s=batch,
        S3_grid_points=npts, S3_grid_cpu_s_est=npts*batch, S3_grid_wall_s_est_20proc=npts*batch/20,
        note='S3 estimate = 4 x 129^3 points x batched per-point CPU; plus Nelder-Mead refinement of local minima (~1500 single-point evaluations each, unknown count until the grid is done). Design guess was "order of an hour, multi-thread".')
    keys = ['P0_pass', 'P1_pass', 'P2_pass', 'P3_pass', 'P4_pass', 'G0b_pass', 'G1_pass']
    r['preflight_all_pass'] = all(r[k] for k in keys)
    for k in keys: print(k, r[k], flush=True)
    print('timing', r['timing_Ns16_grid_point'], flush=True)
    dump('S0', r)
    if not r['preflight_all_pass']: stop('pre-flight failed: ' + ','.join(k for k in keys if not r[k]))

# ---------------------------------------------------------------- S1
def S1():
    d = os.path.join(OUT, 'S1'); os.makedirs(d, exist_ok=True); os.chdir(d)
    # (a) dw_final.py executed unchanged (writes dw_final.json in cwd = out/S1)
    t = time.process_time()
    load('dw_final.py')
    r = {'dw_final_cpu_s': time.process_time() - t}
    DF = json.load(_open(os.path.join(d, 'dw_final.json')))
    r['dw_final_json_sha256'] = hashlib.sha256(_open(os.path.join(d, 'dw_final.json'), 'rb').read()).hexdigest()
    g = load('dw.py'); spec = g['spec']; floq = g['floq']; periodS = g['periodS']; b = 0.2
    def sp(k, Ns, m0=0.0, bb=b): om, v = spec(np.atleast_2d(k), Ns, PHI, bb, m0); return om[0], v[0]
    # m0=0 residuals and f24 (record)
    r['residual_m0_0'] = {Ns: float(np.sort(abs(sp(np.zeros(3), Ns, 0.0)[0]))[0]) for Ns in range(2, 25, 2)}
    r['f24_record'] = r['residual_m0_0'][24]
    # design decay fit over Ns=2..12 (record)
    for m0 in ('0.05', '0.1'):
        rows = np.array(DF['residual_mass_k0'][m0]['rows']); m = rows[:, 0] <= 12
        r[f'design_fit_Ns2_12_m0_{m0}'] = float(np.polyfit(rows[m, 0], np.log(rows[m, 1]), 1)[0])
    # Dirac fit (two ways), m0=0.05
    dd = np.array([1, 2, 3.])/np.sqrt(14); ks = np.array([0.002, 0.004, 0.006, 0.008, 0.01]); DFit = {}
    for Ns in (2, 4, 8, 12):
        w = np.array([np.sort(abs(sp(k*dd, Ns, 0.05)[0]))[0] for k in ks])
        c = np.polyfit(ks**2, w**2, 1); DFit[Ns] = dict(omega0_fit=float(np.sqrt(max(c[1], 0))), v_fit=float(np.sqrt(c[0])),
            omega_k0=float(np.sort(abs(sp(np.zeros(3), Ns, 0.05)[0]))[0]))
    r['residual_two_ways_m0_0.05'] = DFit
    # 13-direction profile record + independent gamma5 (low-subspace Gamma5 eigenvalues) — copy of dw_final.py profile algorithm
    Ns = 16; G5 = np.kron(np.ones(Ns), np.array([1, 1, -1, -1.]))
    def profile(kvec):
        om, v = sp(kvec, Ns); i = np.argsort(abs(om))[:4]
        S = v[:, i]; Q, _ = np.linalg.qr(S); pos = np.kron(np.arange(Ns), np.ones(4)); Mpos = Q.conj().T@(pos[:, None]*Q); e, U = np.linalg.eigh(Mpos); W = Q@U
        ws = []
        for j in range(4):
            p = abs(W[:, j].reshape(Ns, 4))**2; ps = p.sum(1); side = 0 if ps[:Ns//2].sum() > .5 else Ns-1
            dist = abs(np.arange(Ns)-side); m = (dist < Ns//2) & (ps > 1e-15)
            xi = -1/np.polyfit(dist[m][:6], np.log(ps[m][:6]), 1)[0]
            ws.append(dict(wall=side, gamma5=float(p[:, :2].sum()-p[:, 2:].sum()), loc_len_slices=float(xi)))
        g5ev = np.linalg.eigvalsh(Q.conj().T@(G5[:, None]*Q))
        return ws, g5ev
    PR = {}
    def _pr():
      for kk in (0.01, 0.05, 0.1, 0.15, 0.2, 0.3):
        rows = []
        for x in DIRS13:
            ws, ev = profile(kk*x); rows.append(dict(walls0_gamma5=ws[0]['gamma5'], walls0_loc=ws[0]['loc_len_slices'], walls0_side=ws[0]['wall'],
                                                   indep_gamma5_maxabs_eig=float(np.abs(ev).max()), indep_gamma5_eigs=ev.tolist(),
                                                   sign_ok=all((w['gamma5'] > 0) == (w['wall'] == 0) for w in ws)))
        a5 = [abs(x['walls0_gamma5']) for x in rows]; al = [x['walls0_loc'] for x in rows]
        PR[str(kk)] = dict(per_direction=rows, abs_gamma5_min=min(a5), abs_gamma5_max=max(a5), loc_min=min(al), loc_max=max(al),
                           all_signs_ok=all(x['sign_ok'] for x in rows))
    try: _pr()
    except Exception as ex: PR['error'] = repr(ex)
    r['profiles_13dir_record'] = PR
    r['indep_gamma5_123'] = {}
    for kk in (0.01, 0.05, 0.1, 0.15, 0.2, 0.3):
        ws, ev = profile(kk*dd); r['indep_gamma5_123'][str(kk)] = dict(harness_walls0_gamma5=ws[0]['gamma5'], harness_walls0_loc=ws[0]['loc_len_slices'],
                                                                      indep_maxabs_eig=float(np.abs(ev).max()), eigs=ev.tolist())
    # speeds: one harness function, two matrix providers (end = chain Ns=16 b=0.2 m0=0 ; bulk = periodS m=0 ; plus floq Ns=1)
    def low_chain(kv): om, _ = sp(kv, 16); return np.sort(abs(om))[0]
    def low_bulk(kv): P, L = periodS(np.atleast_2d(kv), 0.0, PHI); return np.sort(np.abs(np.angle(np.linalg.eigvals(P[0])))/4)[0]
    def low_ns1(kv): om, _ = sp(kv, 1); return np.sort(abs(om))[0]
    def iso(low):
        I = {}
        for kk in (0.0125, 0.025, 0.05):
            v = [low(kk*x)/kk for x in DIRS13]; I[str(kk)] = dict(speed_mean=float(np.mean(v)), spread=float(np.ptp(v)), per_direction=[float(x) for x in v])
        kks = np.array([0.0125, 0.025, 0.05]); s = np.array([I[str(k)]['spread'] for k in kks])
        return dict(table=I, slope=float(np.polyfit(np.log(kks), np.log(s), 1)[0]))
    E = iso(low_chain); B = iso(low_bulk); B1 = iso(low_ns1)
    Kt = np.random.default_rng(20261112).uniform(-np.pi, np.pi, (20, 3))
    r['periodS_equals_floq_Ns1_maxdiff'] = float(max(np.abs(floq(k[None], 1, PHI, 0.2)[0] - periodS(k[None], 0.0, PHI)[0][0]).max() for k in Kt))
    r['speed_end'] = E; r['speed_bulk_periodS'] = B; r['speed_bulk_floq_Ns1'] = B1
    r['speed_end_matches_dw_final'] = max(abs(E['table'][k]['speed_mean'] - DF['isotropy_wall_Ns16']['table'][k]['speed_mean']) for k in E['table'])
    ve = E['table']['0.0125']['speed_mean']; vb = B['table']['0.0125']['speed_mean']
    r['speed_compare_k0.0125'] = dict(v_end=ve, v_bulk=vb, diff=ve-vb, rel_diff=(ve-vb)/vb)
    # design-R6 supplementary: group velocity extrapolated to k->0 (v(k)=v0+a k^2 over k=0.01..0.05)
    h = 1e-5; kg = np.array([0.01, 0.02, 0.03, 0.04, 0.05])
    def vg0(low):
        out = []
        for x in DIRS13:
            v = np.array([(low((k+h)*x)-low((k-h)*x))/(2*h) for k in kg]); out.append(float(np.polyfit(kg**2, v, 1)[1]))
        return dict(mean=float(np.mean(out)), spread=float(np.ptp(out)), per_direction=out)
    try: r['design_R6_groupvel_record'] = dict(end=vg0(low_chain), bulk=vg0(low_bulk))
    except Exception as ex: r['design_R6_groupvel_record'] = dict(error=repr(ex))
    # end-mode omega(k) curve to 0.25 along (1,2,3), and lowest gapped bulk chain mode at k=0.0125 (reference)
    r['end_mode_curve_123'] = {f'{k:.3f}': float(low_chain(k*dd)) for k in np.arange(0.01, 0.2501, 0.01)}
    om, _ = sp(0.0125*np.array([1., 0, 0]), 16); s = np.sort(abs(om))
    r['chain_modes_k0.0125_x_lowest8'] = s[:8].tolist()
    dump('S1', r); print(json.dumps({k: r[k] for k in ('speed_compare_k0.0125', 'periodS_equals_floq_Ns1_maxdiff', 'speed_end_matches_dw_final')}), flush=True)

# ---------------------------------------------------------------- S2
def _gscan_worker(b):
    d = os.path.join(OUT, 'S2'); os.chdir(d)
    sys.argv = ['dw_gscan.py', str(b)]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): load('dw_gscan.py')
    return b, buf.getvalue()
def _ring_worker(_):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): load('dw_ring.py')
    return 'ring', buf.getvalue()
def S2():
    import multiprocessing as mp
    d = os.path.join(OUT, 'S2'); os.makedirs(d, exist_ok=True)
    bs = ['0.1', '0.15', '0.2', '0.25', '0.3', '0.35']
    with mp.get_context('fork').Pool(7) as P:
        res = [P.apply_async(_gscan_worker, (b,)) for b in bs] + [P.apply_async(_ring_worker, (0,))]
        out = [x.get() for x in res]
    r = {'E2_raw_stdout': {}, 'E2': {}}
    for k, txt in out:
        _open(os.path.join(d, f'stdout_{k}.txt'), 'w').write(txt)
        r['E2_raw_stdout'][k] = txt
        if k == 'ring':
            r['bulk_ring_raw'] = txt; continue
        for line in txt.strip().splitlines():
            p = line.split(); r['E2'][f'b{p[0]}_Ns{p[1]}'] = dict(b=float(p[0]), Ns=int(p[1]), gap=float(p[2]), argmin_rounded=' '.join(p[3:]))
    r['bulk_ring_gap'] = float(r['bulk_ring_raw'].split()[0])
    dump('S2', r); print(json.dumps(r['E2'], indent=0), r['bulk_ring_raw'], flush=True)

# ---------------------------------------------------------------- S3
_G = None
def _g():
    global _G
    if _G is None: _G = load('dw.py')
    return _G
def _grid_chunk(args):
    b, K = args; g = _g()
    return np.sort(np.abs(np.angle(np.linalg.eigvals(g['floq'](K, 16, PHI, b))))/4, -1)[:, 0]
def _refine(args):
    b, x0 = args; g = _g()
    f = lambda k: float(np.sort(abs(g['spec'](k[None], 16, PHI, b, 0.0)[0][0]))[0])
    r = minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-12, maxiter=1500))
    return float(r.fun), r.x.tolist(), float(g['dist_gamma'](r.x[None])[0]), int(r.nit)
def S3():
    import multiprocessing as mp
    from scipy.ndimage import minimum_filter
    d = os.path.join(OUT, 'S3'); os.makedirs(d, exist_ok=True)
    g = _g(); n = 129; ax = np.linspace(-np.pi, np.pi, n)
    KK = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3)
    DG = g['dist_gamma'](KK)
    r = {'grid': '129^3 boundary-inclusive linspace(-pi,pi,129)^3', 'Ns': 16, 'phi': PHI, 'm0': 0.0, 'per_b': {}}
    with mp.get_context('fork').Pool(20) as P:
        for b in (0.1, 0.15, 0.2, 0.25):
            t0 = time.time()
            chunks = [(b, KK[i:i+1000]) for i in range(0, len(KK), 1000)]
            F = np.concatenate(P.map(_grid_chunk, chunks, chunksize=4)).reshape(n, n, n)
            np.save(os.path.join(d, f'grid_b{b}.npy'), F.astype(np.float32))
            t1 = time.time()
            lm = (F <= minimum_filter(F, size=3, mode='constant', cval=np.inf)).reshape(-1)
            ok = lm & (DG > 0.3)
            idx = np.nonzero(ok)[0]
            gm = np.nonzero(DG > 0.3)[0]; gi = gm[np.argmin(F.reshape(-1)[gm])]
            print(f'b={b} grid {t1-t0:.1f}s local minima {lm.sum()} non-excluded {len(idx)} grid-min {F.reshape(-1)[gi]:.6g} at {KK[gi]}', flush=True)
            ref = P.map(_refine, [(b, KK[i]) for i in idx], chunksize=1)
            kept = [x for x in ref if x[2] > 0.3]
            best = min(kept, key=lambda x: x[0]) if kept else None
            r['per_b'][str(b)] = dict(grid_s=t1-t0, refine_s=time.time()-t1, n_local_minima=int(lm.sum()), n_refined=len(idx), n_kept=len(kept),
                grid_min_nonexcluded=float(F.reshape(-1)[gi]), grid_min_at=KK[gi].tolist(),
                R4b_gap=best[0] if best else None, R4b_argmin=best[1] if best else None,
                R4b_argmin_wrapped=(np.mod(np.array(best[1])+np.pi, 2*np.pi)-np.pi).tolist() if best else None,
                R4b_argmin_dist_gamma=best[2] if best else None,
                refined_all=[dict(start=KK[i].tolist(), fun=x[0], x=x[1], dist_gamma=x[2], nit=x[3]) for i, x in zip(idx, ref)])
            print(f'  R4b b={b}: {best[0] if best else None} at {r["per_b"][str(b)]["R4b_argmin_wrapped"]} refine {time.time()-t1:.1f}s', flush=True)
            dump('S3', r)
    dump('S3', r)

# ---------------------------------------------------------------- S4
def _e1(args):
    b, Ns = args; g = _g(); res = []
    for p in itertools.product((1, -1), repeat=3):
        k = np.array(p)*np.pi/2; om, v = g['spec'](k[None], Ns, PHI, b, 0.0); om = om[0]; v = v[0]
        i = int(np.argmin(abs(om))); w = abs(v[:, i])**2; w = w/w.sum(); ws = w.reshape(Ns, 4).sum(1)
        so = np.sort(abs(om))
        res.append(dict(point=list(p), gap=float(so[0]), second=float(so[1]), end_weight=float(ws[0]+ws[-1])))
    return b, Ns, res
def S4():
    import multiprocessing as mp
    d = os.path.join(OUT, 'S4'); os.makedirs(d, exist_ok=True)
    S2 = json.load(_open(os.path.join(OUT, 'S2', 'S2.json'))); S3 = json.load(_open(os.path.join(OUT, 'S3', 'S3.json')))
    bs = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]; Nss = [8, 12, 16, 24, 32, 48]
    with mp.get_context('fork').Pool(20) as P:
        out = P.map(_e1, [(b, Ns) for b in bs for Ns in Nss], chunksize=1)
    pts = [np.array(p)*np.pi/2 for p in itertools.product((1, -1), repeat=3)]
    classes = {}
    for i, p in enumerate(pts):
        cl = next((c for c, q in classes.items() if recip_dist(p, pts[q[0]]) < 1e-9), None)
        if cl is None: classes[len(classes)] = [i]
        else: classes[cl].append(i)
    r = {'equivalence_classes_of_8_points': {str(c): [list(map(int, np.sign(pts[i]))) for i in v] for c, v in classes.items()}, 'E1': {}}
    for b, Ns, res in out:
        m = min(res, key=lambda x: x['gap'])
        r['E1'][f'b{b:.2f}_Ns{Ns}'] = dict(b=b, Ns=Ns, gap=m['gap'], at=m['point'], end_weight=m['end_weight'], all_points=res)
    E1 = lambda b, Ns: r['E1'][f'b{b:.2f}_Ns{Ns}']['gap']
    E2 = lambda b, Ns: S2['E2'][f'b{b:g}_Ns{Ns}']['gap']
    # pre-reg clauses
    paper = {0.10: 0.058, 0.15: 0.046, 0.20: 0.034, 0.25: 0.022}
    ci = {str(b): dict(E2_Ns16=E2(b, 16), paper=p, rel=abs(E2(b, 16)-p)/p, ok=abs(E2(b, 16)-p)/p <= 0.05) for b, p in paper.items()}
    cii = {}
    for b in (0.30, 0.35):
        ns = [N for N in (8, 12, 16, 24)]; gs = [E1(b, N) for N in ns]
        use = [i for i in range(4) if all(gs[j] > 1e-12 for j in range(i+1))]
        nsu = [ns[i] for i in use]; gsu = [gs[i] for i in use]
        dec = all(gsu[i+1] < gsu[i] for i in range(len(gsu)-1))
        sl = float(np.polyfit(nsu, np.log(gsu), 1)[0]) if len(gsu) >= 2 else None
        cii[str(b)] = dict(Ns=ns, gaps=gs, Ns_used=nsu, strictly_decreasing=dec, slope=sl, ok=bool(dec and sl is not None and sl < 0))
    ciii = {str(b): dict(E1_Ns8=E1(b, 8), E1_Ns16=E1(b, 16), ratio=E1(b, 16)/E1(b, 8), E2_Ns16=E2(b, 16),
                         ok=bool(E1(b, 16) >= 0.5*E1(b, 8) and E2(b, 16) > 1e-3)) for b in (0.10, 0.15, 0.20, 0.25)}
    r['prereg_boundary'] = dict(i=ci, ii=cii, iii=ciii, i_ok=all(v['ok'] for v in ci.values()), ii_ok=all(v['ok'] for v in cii.values()),
                                iii_ok=all(v['ok'] for v in ciii.values()))
    r['prereg_boundary']['PASS'] = r['prereg_boundary']['i_ok'] and r['prereg_boundary']['ii_ok'] and r['prereg_boundary']['iii_ok']
    # design R5 verdicts (D3)
    R4ref = {f'{b:.2f}': S3['per_b'][str(b)]['R4b_gap'] for b in (0.1, 0.15, 0.2, 0.25)}
    R4ref.update({'0.30': E2(0.30, 16), '0.35': E2(0.35, 16), '0.40': None})
    R5 = {}
    for b in bs:
        ref = R4ref[f'{b:.2f}']; surv = {}
        for Ns in Nss:
            e = r['E1'][f'b{b:.2f}_Ns{Ns}']
            surv[Ns] = None if ref is None else bool(e['end_weight'] >= 0.5 and e['gap'] < ref)
        gs = [E1(b, N) for N in (24, 32, 48)]
        sl = float(np.polyfit([24, 32, 48], np.log(gs), 1)[0]) if all(x > 0 for x in gs) else None
        if ref is None or sl is None: v = 'unresolved (rule input missing)' if ref is None else 'unresolved (zero gap, slope undefined)'
        elif (not surv[48]) and sl > -0.05: v = 'allowed'
        elif surv[48] and sl <= -0.1: v = 'excluded'
        else: v = 'unresolved'
        R5[f'{b:.2f}'] = dict(R4_reference_gap=ref, survives=surv, gaps_24_32_48=gs, slope_24_48=sl, verdict=v)
    r['design_R5'] = R5
    r['design_R5_pass'] = all(R5[f'{b:.2f}']['verdict'] == 'allowed' for b in (0.1, 0.15, 0.2, 0.25)) and all(R5[f'{b:.2f}']['verdict'] == 'excluded' for b in (0.3, 0.35, 0.4))
    # R4b vs R5 cross-check (where an end mode survives at some Ns for b<=0.25)
    xc = {}
    for b in (0.1, 0.15, 0.2, 0.25):
        am = S3['per_b'][str(b)]['R4b_argmin']; dsp = min(recip_dist(am, p) for p in pts) if am is not None else None
        xc[str(b)] = dict(R4b_argmin=am, dist_to_nearest_special_point_mod_recip=dsp, any_survival=any(R5[f'{b:.2f}']['survives'].values()),
                          agree=(dsp is not None and dsp <= 0.3) if any(R5[f'{b:.2f}']['survives'].values()) else 'n/a (no surviving end mode)')
    r['R4b_vs_R5_crosscheck'] = xc
    # face-centre finding (pre-reg, report only)
    g = _g(); FC = {}
    for b in (0.2, 0.3):
        for Ns in (8, 16):
            U0 = g['floq'](np.zeros((1, 3)), Ns, PHI, b)[0]
            FC[f'b{b}_Ns{Ns}'] = dict(lowest_abs_omega=[float(np.sort(abs(g['spec'](L[None], Ns, PHI, b, 0.0)[0][0]))[0]) for L in EDGE12],
                                      maxdiff_vs_Gamma=max(float(np.abs(g['floq'](L[None], Ns, PHI, b)[0]-U0).max()) for L in EDGE12))
    r['face_centre_finding'] = FC
    dump('S4', r); print(json.dumps({'prereg_boundary': {k: r['prereg_boundary'][k] for k in ('i_ok', 'ii_ok', 'iii_ok', 'PASS')},
                                     'R5': {k: v['verdict'] for k, v in R5.items()}}), flush=True)

# ---------------------------------------------------------------- S5
def S5():
    d = os.path.join(OUT, 'S5'); os.makedirs(d, exist_ok=True); os.chdir(d)
    load('dw_real.py')
    X1 = json.load(_open(os.path.join(d, 'dw_real.json')))
    g = _g()
    X2 = {Ns: dict(components=4*Ns, floq_shape=list(g['floq'](np.zeros((1, 3)), Ns, PHI, 0.2).shape[1:])) for Ns in (2, 4, 8, 12, 16, 24)}
    dump('S5', dict(X1=X1, X2=X2)); print(X1, X2, flush=True)

def G0END():
    r = {p: dict(expected=h, actual=sha(p), ok=sha(p) == h) for p, h in PINS.items()}
    dump('G0END', dict(hashes=r, all_ok=all(v['ok'] for v in r.values()))); print('G0END', all(v['ok'] for v in r.values()), flush=True)
    if not all(v['ok'] for v in r.values()): stop('end hash mismatch')

if __name__ == '__main__':
    {'S0': S0, 'S1': S1, 'S2': S2, 'S3': S3, 'S4': S4, 'S5': S5, 'G0END': G0END}[sys.argv[1]]()
