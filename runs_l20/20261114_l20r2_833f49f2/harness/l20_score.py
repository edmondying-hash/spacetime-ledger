#!/usr/bin/env python3
"""Scored L2.0 checks S0, C1, C2, C3, C4, C5 (b)-(d) for design L2_0_RUN_DESIGN.md
sha256 833f49f26418b2267cc0a9b389a46220078b453eebe92cf149145af330077ed9, all D1-D16 defaults.
Glue code written 14 Nov 2026 (America/New_York) in the run folder; it imports the design folder's
l20_measure.py (and through it frozen/dirac4.py) unchanged and read-only. Implementation choices are
listed in IMPLEMENTATION_NOTES.md beside this file.
r2 code fix (14 Nov 2026, America/New_York; see R2_NOTE.md): (1) C5 no longer keeps post-hop arrays in its
geometry cache; (2) C4 Q-share/control shots use an RNG derived from (seed, partition index). Nothing else changed.
usage: l20_score.py S0|C1|C2|C3|C4|C5   (env L20_SCORE=1, L20_OUT=<out dir>)"""
import sys
sys.dont_write_bytecode = True
import os, json, time, math, hashlib, itertools, resource

DESIGN = "/workspace/L2_0_design_spacetime_20261113"
sys.path.insert(0, DESIGN)
import numpy as np
import scipy.linalg as sla
import l20_measure as H  # noqa: E402

EXPECT = {
    "L2_0_RUN_DESIGN.md": "833f49f26418b2267cc0a9b389a46220078b453eebe92cf149145af330077ed9",
    "L2_0_RUN_DESIGN.pdf": "6bae2decb7984454830be973f086dc7938eb0ec36a3b8e5ec2138b20b0e33992",
    "L2_0_C5A_AUDIT.md": "423920fe845e26df1871e0e2a5ebc044c780735919c1df1af3c47ecabf683090",
    "L2_0_OPEN_DECISIONS.md": "6e313901623227c9818606e18b398b3e3b3dfbf39f0a4f41e77bc0e19339ab9b",
    "l20_measure.py": "08e98af5d2936474260f233f85c4b1ef06b4564d6533409f36c34a7bfa5dd516",
    "L2_0_PROBE_TIMING.json": "9bad7d32371956121f3c6905d4dbaf3916f2a4d8c0b888dccf5988da5f45227d",
    "frozen/dirac4.py": "f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff",
    "SHA256SUMS": "ae005712b98eb2263e702cdc5701abfd1fb0e9e0bef102367c40d28dab858edc",
}
SEEDS = [20261113, 20261114, 20261115, 20261116, 20261117]
NSHOT = 100_000
PHI, M0 = 1.4, 0.0
OUT = os.environ.get("L20_OUT", "")
T_START = time.time()


def cpu_now():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        f = float(o)
        if math.isnan(f):
            return "nan"
        if math.isinf(f):
            return "inf" if f > 0 else "-inf"
        return f
    if isinstance(o, complex):
        return [o.real, o.imag]
    return o


def hashes():
    got = {k: H.sha256_file(os.path.join(DESIGN, k)) for k in EXPECT}
    got["imported_dirac4"] = H.sha256_file(H.dirac4.__file__)
    got["imported_l20_measure"] = H.sha256_file(H.__file__)
    got["this_file_l20_score"] = H.sha256_file(os.path.abspath(__file__))
    ok = all(got[k] == v for k, v in EXPECT.items()) and got["imported_dirac4"] == EXPECT["frozen/dirac4.py"] \
        and got["imported_l20_measure"] == EXPECT["l20_measure.py"]
    return got, ok


def finish(name, rec):
    rec["check"] = name
    rec["design_sha256"] = EXPECT["L2_0_RUN_DESIGN.md"]
    rec["dirac4_sha256"] = H.sha256_file(H.dirac4.__file__)
    rec["l20_measure_sha256"] = H.sha256_file(H.__file__)
    rec["l20_score_sha256"] = H.sha256_file(os.path.abspath(__file__))
    rec["params"] = dict(phi=PHI, m=M0, wilson=True, wilson_mass=0.0, patch=False, load_rule="none",
                         seeds=SEEDS, nshot=NSHOT)
    rec["self_wall_s"] = time.time() - T_START
    rec["self_cpu_s"] = cpu_now()
    rec["self_ru_maxrss_MiB"] = H.peak_rss_mib()
    rec["finished_local"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    p = os.path.join(OUT, f"{name}.json")
    with open(p, "w") as f:
        json.dump(clean(rec), f, indent=1)
    H.log("wrote", p, "label", rec.get("label"))


# ---------------------------------------------------------------- shared helpers
def draw(rng, w, n=NSHOT):
    w = np.asarray(w, float)
    p = w / w.sum()
    idx = rng.choice(len(p), size=n, p=p)
    return np.bincount(idx, minlength=len(p)), p, idx


def zval(diff, sigma, floor=1e-12):
    """|diff| / sigma; sigma == 0 -> 0 if |diff| <= floor else inf."""
    if sigma > 0:
        return abs(diff) / sigma
    return 0.0 if abs(diff) <= floor else float("inf")


def within(diff, sigma, nsig, floor=1e-12):
    return abs(diff) <= nsig * sigma + floor


def site_coords(L):
    x = np.arange(L)
    return np.meshgrid(x, x, x, indexing="ij")


def mi(a, L):
    return (a + L / 2) % L - L / 2


def unit(v):
    v = np.asarray(v, complex)
    return v / np.linalg.norm(v)


def rand_spin(rng):
    v = rng.normal(size=4) + 1j * rng.normal(size=4)
    return v / np.linalg.norm(v)


def norm2(psi):
    return float(np.sum(np.abs(psi) ** 2))


def fib_dirs(n=50):
    ga = math.pi * (3 - math.sqrt(5))
    out = []
    for i in range(n):
        z = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(max(0.0, 1 - z * z))
        out.append(np.array([r * math.cos(ga * i), r * math.sin(ga * i), z]))
    return out


AXIS_DIRS = [np.array(v, float) for v in ([1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1])]


# ---------------------------------------------------------------- S0
def check_S0():
    rec = dict(label=None)
    got, ok = hashes()
    rec["P0"] = dict(hashes=got, expected=EXPECT, L20_SCORE=os.environ.get("L20_SCORE"),
                     ok=bool(ok and os.environ.get("L20_SCORE") == "1"))
    rng = np.random.default_rng(SEEDS[0])
    ks = [np.zeros(3)]
    for i in range(3):
        for s in (1, -1):
            e = np.zeros(3); e[i] = s * math.pi / 2; ks.append(e)
    ks += list(rng.uniform(-math.pi, math.pi, size=(32, 3)))
    ks += list(rng.uniform(-math.pi, math.pi, size=(25, 3)))
    dev = 0.0
    for k in ks:
        U = H.U_cycle(k)
        dev = max(dev, float(np.abs(U.conj().T @ U - np.eye(4)).max()))
    rec["P1"] = dict(n_k=len(ks), max_abs_dev_UdagU_minus_I=dev, bound=1e-14, ok=dev <= 1e-14)
    p2, p3 = {}, {}
    for L in (16, 32):
        Ug = H.precompute_U(L)
        mask = H.orbit_mask(L)
        X, Y, Z = site_coords(L)
        ns = [(0, 0, 0), (1, 0, 0), (1, 2, 3), (L // 2 - 1, 3, L // 4)] + \
             [tuple(int(v) for v in rng.integers(-L // 2, L // 2, size=3)) for _ in range(2)]
        dmax = 0.0
        for n in ns:
            k = 2 * np.pi * np.array(n, float) / L
            chi = rand_spin(rng)
            wave = np.exp(1j * (k[0] * X + k[1] * Y + k[2] * Z)) * mask
            psi = chi[:, None, None, None] * wave[None]
            out = H.fft_cycle(psi, Ug)
            exp = (H.U_cycle(k) @ chi)[:, None, None, None] * wave[None]
            dmax = max(dmax, float(np.abs(out - exp).max()))
        p2[str(L)] = dict(n_list=ns, max_abs_dev=dmax, ok=dmax <= 1e-12)
        psi = H.random_orbit_state(L, rng, mask)
        for _ in range(10):
            psi = H.fft_cycle(psi, Ug)
        off = float(np.abs(psi[:, ~mask]).max())
        p3[str(L)] = dict(max_abs_offorbit_after_10_cycles=off, ok=off <= 1e-14)
        del Ug
    rec["P2"] = dict(per_L=p2, bound=1e-12, ok=all(v["ok"] for v in p2.values()))
    rec["P3"] = dict(per_L=p3, bound=1e-14, ok=all(v["ok"] for v in p3.values()))
    tv = {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                                         "NUMEXPR_NUM_THREADS", "CUDA_VISIBLE_DEVICES", "L20_METER")}
    nthreads = len(os.listdir("/proc/self/task"))
    p4ok = all(tv[k] == "1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")) \
        and tv["L20_METER"] == "1" and tv["CUDA_VISIBLE_DEVICES"] == "" and nthreads == 1
    rec["P4"] = dict(env=tv, os_threads_in_process=nthreads, gpu_used=False,
                     numpy_version=np.__version__, ok=bool(p4ok))
    allok = all(rec[p]["ok"] for p in ("P0", "P1", "P2", "P3", "P4"))
    rec["label"] = "PASS" if allok else "FAIL"
    finish("S0", rec)
    return 0


# ---------------------------------------------------------------- C1
def edge_mask(L):
    X, Y, Z = site_coords(L)
    e = np.zeros((L, L, L), bool)
    for A in (X, Y, Z):
        e |= (A < 2) | (A >= L - 2)
    return e


def run_series(psi0, Ug, L, ncyc=1000):
    mask = H.orbit_mask(L)
    em = edge_mask(L) & mask
    psi = psi0.copy()
    ser = np.empty((ncyc + 1, len(H.P_POWERS)))
    edge = np.empty(ncyc + 1)
    for t in range(ncyc + 1):
        a = np.abs(psi[:, mask])
        ser[t] = [np.sum(a ** p) for p in H.P_POWERS]
        q = float(np.sum(np.abs(psi[:, em]) ** 2))
        edge[t] = q / ser[t][H.P_POWERS.index(2.0)]
        if t == 1:
            d1 = abs(ser[1][H.P_POWERS.index(2.0)] / ser[0][H.P_POWERS.index(2.0)] - 1)
            if d1 > 1e-12:
                return ser[:2], edge[:2], True
        if t < ncyc:
            psi = H.fft_cycle(psi, Ug)
    return ser, edge, False


def drifts(ser):
    return {str(p): float(np.max(np.abs(ser[:, i] / ser[0, i] - 1))) for i, p in enumerate(H.P_POWERS)}


def mpow_d(M, g):
    T, Zs = sla.schur(M, output="complex")
    d = np.diag(T)
    return (Zs * np.exp(g * np.log(d))) @ Zs.conj().T, float(np.max(np.abs(np.angle(d))))


def precompute_ruleB(L, g=0.81, phi=PHI, m=M0):
    D = H.dirac4
    k = H.k_grid(L).reshape(-1, 3)
    U = np.empty((k.shape[0], 4, 4), complex)
    thmax, udev = 0.0, 0.0
    for i, ki in enumerate(k):
        Sp = D.S_step(+1, ki, m, False, 0.0); Sm = D.S_step(-1, ki, m, False, 0.0)
        Vp = D.V_step(+1, ki, phi, False); Vm = D.V_step(-1, ki, phi, False)
        mats = []
        for F in (Vm, Sm, Vp, Sp):
            P, th = mpow_d(F, g); mats.append(P); thmax = max(thmax, th)
        U[i] = mats[0] @ mats[1] @ mats[2] @ mats[3]
        udev = max(udev, float(np.abs(U[i].conj().T @ U[i] - np.eye(4)).max()))
    return U.reshape(L, L, L, 4, 4), thmax, udev


def c1_states(L, rng, spins=None):
    c = L // 2
    if spins is None:
        s1 = rand_spin(rng)
    else:
        s1 = spins["S1"]
    S1 = H.localized_packet(L, rng, 2.0, centre=np.array([c, c, c], float), spin=s1)
    S2 = H.random_orbit_state(L, rng) if spins is None else None
    s3 = rand_spin(rng) if spins is None else spins["S3"]
    a = H.localized_packet(L, rng, 2.0, centre=np.array([L // 4, c, c], float), spin=s3)
    b = H.localized_packet(L, rng, 2.0, centre=np.array([3 * L // 4, c, c], float), spin=s3)
    S3 = a + np.exp(0.7j) * b
    S3 = S3 / math.sqrt(norm2(S3))
    return dict(S1=S1, S2=S2, S3=S3), dict(S1=s1, S3=s3)


def sym_eval(v, ks, pos_h):
    ks = np.asarray(ks, float)
    nk = ks.shape[0]
    iu = np.triu_indices(4, 1)
    M0m = np.zeros((4, 4), complex)
    M0m[np.diag_indices(4)] = v[0:4]
    M0m[iu] = v[4:10] + 1j * v[10:16]
    M0m = M0m + M0m.conj().T - np.diag(np.diag(M0m))
    out = np.broadcast_to(M0m, (nk, 4, 4)).copy()
    off = 16
    for h in pos_h:
        Mh = v[off:off + 16].reshape(4, 4) + 1j * v[off + 16:off + 32].reshape(4, 4)
        off += 32
        ph = np.exp(1j * (ks @ np.array(h, float)))
        out += ph[:, None, None] * Mh[None] + np.conj(ph)[:, None, None] * Mh.conj().T[None]
    return out


def product_grid(n):
    g = -np.pi + 2 * np.pi * np.arange(n) / n
    return np.array(list(itertools.product(g, g, g)))


def extra_points():
    pts = [np.zeros(3)]
    for i in range(3):
        for s in (1, -1):
            e = np.zeros(3); e[i] = s * math.pi / 2; pts.append(e)
    return np.array(pts)


def orbit_classes(ks):
    reps = set()
    shifts = [np.zeros(3), np.array([1, 1, 0.]), np.array([1, 0, 1.]), np.array([0, 1, 1.])]
    for k in ks:
        p = np.mod(np.asarray(k) / np.pi, 2.0)
        cands = [tuple(np.round(np.mod(p + s, 2.0), 9) % 2.0) for s in shifts]
        reps.add(min(cands))
    return len(reps)


def chunked_search(ks, pos_h, chunk=128, extra_vecs=None):
    npar = H.n_params(len(pos_h))
    R = np.zeros((0, npar)); R16 = np.zeros((0, 16))
    res = {k: 0.0 for k in (extra_vecs or {})}
    for i in range(0, len(ks), chunk):
        A = H.constraint_matrix_fast(ks[i:i + chunk], pos_h)
        for name, v in (extra_vecs or {}).items():
            res[name] = max(res[name], float(np.abs(A @ v).max()))
        R = np.linalg.qr(np.vstack([R, A]), mode="r")
        R16 = np.linalg.qr(np.vstack([R16, A[:, :16]]), mode="r")
    return R, R16, res


def nullspace(R, atol=1e-8, grey_hi=1e-4):
    _, s, vh = np.linalg.svd(R, full_matrices=True)
    n = vh.shape[1]
    s_full = np.zeros(n); s_full[:s.size] = s
    idx = np.where(s_full < atol)[0]
    return dict(s=s_full, n_clear=int(idx.size), n_grey=int(np.sum((s_full >= atol) & (s_full < grey_hi))),
                basis=vh[idx])


def complement_basis(B, vI):
    vh = vI / np.linalg.norm(vI)
    if B.shape[0] == 0:
        return np.zeros((0, B.shape[1] if B.ndim == 2 else len(vI))), 1.0
    proj_res = float(np.linalg.norm(vh - B.T @ (B @ vh)))
    Bp = B - np.outer(B @ vh, vh)
    u, s, w = np.linalg.svd(Bp, full_matrices=False)
    return w[s > 0.5], proj_res


def check_C1():
    rec = dict()
    t0 = time.time()
    L = 16
    Ug = H.precompute_U(L)
    cells, series = [], {}
    fault = False
    spins_by_seed = {}
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        st, spins = c1_states(L, rng)
        spins_by_seed[seed] = spins
        for name in ("S1", "S2", "S3"):
            ser, edge, f = run_series(st[name], Ug, L)
            series[f"L16_{seed}_{name}"] = ser
            if f:
                fault = True
            dr = drifts(ser)
            cells.append(dict(seed=seed, state=name, L=16, drift=dr, stepper_fault=f,
                              max_edge_fraction=float(edge.max()), edge_exceeds_1em6=bool(edge.max() > 1e-6)))
        if fault:
            break
    rec["drift_L16_cells"] = cells
    reruns = []
    if not fault:
        Ug32 = H.precompute_U(32)
        for c in cells:
            if c["state"] in ("S1", "S3") and c["edge_exceeds_1em6"]:
                rng = np.random.default_rng(c["seed"])
                st, _ = c1_states(32, rng, spins=spins_by_seed[c["seed"]])
                ser, edge, f = run_series(st[c["state"]], Ug32, 32)
                series[f"L32_{c['seed']}_{c['state']}"] = ser
                reruns.append(dict(seed=c["seed"], state=c["state"], L=32, drift=drifts(ser), stepper_fault=f,
                                   max_edge_fraction=float(edge.max()), still_wraps=bool(edge.max() > 1e-6),
                                   label="UNINFORMATIVE" if edge.max() > 1e-6 else "recorded"))
        del Ug32
    rec["drift_L32_reruns"] = reruns
    rec["drift_wall_s"] = time.time() - t0
    # gate 5.1
    if fault:
        drift_label = "UNINFORMATIVE"; fails = ["stepper fault at cycle 1"]
    else:
        fails, s3_reported = [], []
        for c in cells:
            d2 = c["drift"]["2.0"]
            others = {p: v for p, v in c["drift"].items() if p != "2.0"}
            if d2 > 1e-12:
                fails.append(f"{c['seed']} {c['state']} p=2 drift {d2}")
            quiet = [p for p, v in others.items() if v <= 1e-3]
            if c["state"] in ("S1", "S2") and quiet:
                fails.append(f"{c['seed']} {c['state']} quiet p {quiet}")
            if c["state"] == "S3" and quiet:
                s3_reported.append(dict(seed=c["seed"], quiet_p=quiet))
        rec["S3_quiet_p_reported"] = s3_reported
        drift_label = "FAIL" if fails else "PASS"
    rec["drift_gate"] = dict(label=drift_label, failures=fails)
    # diagnostics (not gated): seed 20261113, state S1, L=16
    diag = {}
    rng = np.random.default_rng(SEEDS[0])
    st, _ = c1_states(L, rng)
    Um = H.precompute_U(L, m=0.3)
    ser, edge, f = run_series(st["S1"], Um, L)
    series["diag_m0.3"] = ser
    diag["m0.3"] = dict(note="diagnostic, not gated", m=0.3, drift=drifts(ser), stepper_fault=f)
    del Um
    UB, thmax, udev = precompute_ruleB(L, 0.81)
    ser, edge, f = run_series(st["S1"], UB, L)
    series["diag_loadON_ruleB_s0.81"] = ser
    diag["uniform_load_ON_ruleB"] = dict(note="diagnostic, not gated", rule="B: each of S+,V+,S-,V- to principal s-th power",
                                         s=0.81, phi=PHI, m=0.0, max_abs_factor_eigenphase=thmax,
                                         max_unitarity_dev=udev, drift=drifts(ser), stepper_fault=f)
    del UB
    rec["diagnostics"] = diag
    np.savez_compressed(os.path.join(OUT, "C1_series.npz"), powers=np.array(H.P_POWERS),
                        **{k: v for k, v in series.items()})
    # 5.2 search
    t1 = time.time()
    pos_h = H.half_displacements()
    npar = H.n_params(len(pos_h))
    vI = H.identity_params(pos_h)
    vSz = np.zeros(npar); vSz[0:4] = [1, -1, 1, -1]   # kron(I2, sigma_z): on-site diag (R up, R dn, L up, L dn)
    ks12 = np.vstack([product_grid(12), extra_points()])
    R, R16, res = chunked_search(ks12, pos_h, extra_vecs=dict(identity=vI / np.linalg.norm(vI), sigma_z=vSz / np.linalg.norm(vSz)))
    ns = nullspace(R); ns16 = nullspace(R16)
    comp, projres = complement_basis(ns["basis"], vI)
    comp16, projres16 = complement_basis(ns16["basis"], vI[:16])
    ks16 = product_grid(16)
    # symbol evaluator self-check against l20_measure.apply_params_to_symbol
    rv = np.random.default_rng(SEEDS[0]).normal(size=npar)
    sdev = max(float(np.abs(sym_eval(rv, [k], pos_h)[0] - H.apply_params_to_symbol(k, rv, pos_h)).max()) for k in ks12[:5])

    def posinfo(v, pos_h_used):
        out = {}
        for tag, kk in (("official", ks12), ("diag16", ks16)):
            if len(pos_h_used):
                ev = np.linalg.eigvalsh(sym_eval(v, kk, pos_h_used))
            else:
                full = np.zeros(npar); full[:16] = v
                ev = np.linalg.eigvalsh(sym_eval(full, kk, pos_h))
            out[tag] = dict(min_eig=float(ev.min()), max_eig=float(ev.max()))
        lo = min(out["official"]["min_eig"], out["diag16"]["min_eig"])
        hi = max(out["official"]["max_eig"], out["diag16"]["max_eig"])
        out["positive_plus_sign"] = bool(lo >= -1e-10)
        out["positive_minus_sign"] = bool(-hi >= -1e-10)
        out["positive"] = out["positive_plus_sign"] or out["positive_minus_sign"]
        return out

    def describe(v):
        d = {"onsite_M0_params": v[:16]}
        off = 16
        norms = {}
        for h in pos_h:
            norms[str(h)] = float(np.linalg.norm(v[off:off + 32])); off += 32
        d["norm_per_displacement"] = norms
        return d

    extra = []
    for i, v in enumerate(comp):
        extra.append(dict(index=i, vector=v, description=describe(v), positivity=posinfo(v, pos_h)))
    extra16 = []
    for i, v in enumerate(comp16):
        extra16.append(dict(index=i, vector=v, positivity=posinfo(v, [])))
    ident_pos = posinfo(vI / np.linalg.norm(vI), pos_h)
    # control 3
    ctrl3 = {}
    for n in (6, 8):
        kk = np.vstack([product_grid(n), extra_points()])
        Rn, R16n, _ = chunked_search(kk, pos_h)
        nn = nullspace(Rn)
        ctrl3[f"{n}^3"] = dict(n_k=len(kk), n_clear=nn["n_clear"], n_grey=nn["n_grey"],
                              s_below_1em4=nn["s"][nn["s"] < 1e-4], s_min=float(nn["s"].min()), s_max=float(nn["s"].max()))
    c1ok = res["identity"] <= 1e-10 and projres <= 1e-10
    c2ok = res["sigma_z"] >= 1e-3
    c3ok = all(v["n_clear"] == ns["n_clear"] and v["n_grey"] == 0 for v in ctrl3.values())
    grey = ns["n_grey"] > 0 or ns16["n_grey"] > 0
    pos_other = [e["index"] for e in extra if e["positivity"]["positive"]]
    pos_other16 = [e["index"] for e in extra16 if e["positivity"]["positive"]]
    if grey:
        slab, why = "UNINFORMATIVE", "grey singular value in [1e-8,1e-4)"
    elif not c1ok:
        slab, why = "UNINFORMATIVE", "control (1): identity ray not in numerical nullspace (harness fault, not scored)"
    elif not c2ok:
        slab, why = "UNINFORMATIVE", "control (2): sigma_z not rejected"
    elif not c3ok:
        slab, why = "UNINFORMATIVE", "control (3): 6^3/8^3 clear nullspace dimension differs from 12^3"
    elif pos_other or pos_other16:
        slab, why = "FAIL", "positive conserved density other than c*I"
    else:
        slab, why = "PASS", "only c*I positive among nullspace rays"
    rec["search"] = dict(
        n_params=npar, n_pairs=len(pos_h), n_k_official=len(ks12), n_k_orbit_classes_reporting=orbit_classes(ks12),
        method="block-Householder QR of A (chunks of 128 k) then SVD of R; same singular values/right vectors as SVD of A",
        s_min=float(ns["s"].min()), s_max=float(ns["s"].max()), singular_values_all=ns["s"],
        s_below_1em4=ns["s"][ns["s"] < 1e-4], n_clear=ns["n_clear"], n_grey=ns["n_grey"],
        identity_residual_maxabs=res["identity"], identity_projection_residual=projres,
        sigma_z_residual_maxabs=res["sigma_z"], symbol_eval_selfcheck_maxdev=sdev,
        identity_positivity=ident_pos, extra_nullspace_dim=len(extra), extra_vectors=extra,
        sdp_note="no SDP solver on box (cvxpy absent); fallback m(k)>=0 test used, labelled as such",
        positivity_test="m(k) >= 0 fallback (official 12^3+7 grid and 16^3 diagnostic grid), tol -1e-10",
        onsite=dict(singular_values=ns16["s"], n_clear=ns16["n_clear"], n_grey=ns16["n_grey"],
                    identity_projection_residual=projres16, extra_dim=len(extra16), extra_vectors=extra16),
        control1_ok=c1ok, control2_ok=c2ok, control3=ctrl3, control3_ok=c3ok,
        positive_other_indices=pos_other, positive_other_onsite_indices=pos_other16,
        label=slab, reason=why, wall_s=time.time() - t1)
    if drift_label == "FAIL" or slab == "FAIL":
        lab = "FAIL"
    elif drift_label == "PASS" and slab == "PASS":
        lab = "PASS"
    else:
        lab = "UNINFORMATIVE"
    rec["label"] = lab
    finish("C1", rec)
    return 0


# ---------------------------------------------------------------- C2 / C3
def quad_masks(L):
    X, Y, Z = site_coords(L)
    h = L // 2
    return [(X < h) & (Y < h), (X < h) & (Y >= h), (X >= h) & (Y < h), (X >= h) & (Y >= h)]


def half_masks(L):
    X, Y, Z = site_coords(L)
    return [X < L // 2, X >= L // 2]


def rescale(psi, masks, ws):
    out = np.zeros_like(psi)
    for m, w in zip(masks, ws):
        q = float(np.sum(np.abs(psi[:, m]) ** 2))
        out[:, m] = psi[:, m] * math.sqrt(w / q)
    return out


def c2_states(L, rng):
    c = L // 2
    cen = np.array([c, c, c], float)
    Q4, H2 = quad_masks(L), half_masks(L)
    st = {}
    st["P1"] = (H.localized_packet(L, rng, 2.0, centre=cen, spin=np.array([1, 0, 0, 0], complex)), Q4)
    st["P2"] = (H.localized_packet(L, rng, 2.0, centre=cen, spin=rand_spin(rng)), Q4)
    st["SPLIT"] = (rescale(H.random_orbit_state(L, rng), H2, [2 / 3, 1 / 3]), H2)
    st["EQ4"] = (rescale(H.random_orbit_state(L, rng), Q4, [0.25] * 4), Q4)
    st["RANDQ"] = (H.random_orbit_state(L, rng), Q4)
    return st


def check_C2():
    L = 16
    Ug = H.precompute_U(L)
    cells = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        st = c2_states(L, rng)
        for name, (psi0, masks) in st.items():
            server = psi0.copy()
            tprev = 0
            for t in (0, 10, 100):
                for _ in range(t - tprev):
                    server = H.fft_cycle(server, Ug)
                tprev = t
                client = server.copy()
                Qj = H.charges(client, masks)
                keep = [j for j in range(len(masks)) if Qj[j] >= 1e-12]
                cell = dict(seed=seed, state=name, t=t, Q_before=Qj, kept_channels=keep)
                if len(keep) < 2:
                    cell["label"] = "UNINFORMATIVE"; cells.append(cell); continue
                Q = float(Qj[keep].sum())
                lockQ = []
                for j in keep:
                    lk, n = H.lock_to_channel(client, masks[j])
                    lk = lk * math.sqrt(Q)
                    qa = H.charges(lk, [masks[i] for i in keep])
                    lockQ.append(qa)
                lockQ = np.array(lockQ)   # row: outcome, col: channel charge after
                cell["lock_check_maxdev"] = float(np.abs(lockQ - Q * np.eye(len(keep))).max())
                cell["unequal"] = bool(np.ptp(Qj[keep]) > 1e-12)
                rules = {}
                for rname, p in (("Qshare", 2.0), ("p1", 1.0), ("p4", 4.0)):
                    w = H.charges_power(client, [masks[j] for j in keep], p)
                    counts, pw, _ = draw(rng, w)
                    est = (counts / NSHOT) @ lockQ          # E[Q_j after]
                    bias = est - Qj[keep]
                    sig = Q * np.sqrt(pw * (1 - pw) / NSHOT)
                    z = [zval(b, s) for b, s in zip(bias, sig)]
                    rules[rname] = dict(weights=pw, counts=counts, bias=bias, sigma=sig, z=z,
                                        within3=[within(b, s, 3) for b, s in zip(bias, sig)],
                                        beyond5=[not within(b, s, 5) for b, s in zip(bias, sig)])
                cell["rules"] = rules
                cell["label"] = "scored"
                cells.append(cell)
    fails, ctrl_fail, uninf = [], [], []
    for c in cells:
        if c["label"] == "UNINFORMATIVE":
            uninf.append(f"{c['seed']} {c['state']} t={c['t']}"); continue
        if not all(c["rules"]["Qshare"]["within3"]):
            fails.append(f"{c['seed']} {c['state']} t={c['t']} Qshare z={max(c['rules']['Qshare']['z'])}")
        if c["t"] == 0 and c["unequal"]:
            for r in ("p1", "p4"):
                if not any(c["rules"][r]["beyond5"]):
                    ctrl_fail.append(f"{c['seed']} {c['state']} {r} max z={max(c['rules'][r]['z'])}")
    scored = [c for c in cells if c["label"] == "scored"]
    if not scored:
        lab = "UNINFORMATIVE"
    else:
        lab = "FAIL" if (fails or ctrl_fail) else "PASS"
    zq = [z for c in scored for z in c["rules"]["Qshare"]["z"]]
    rec = dict(label=lab, cells=cells, qshare_failures=fails, control_failures=ctrl_fail, uninformative=uninf,
               n_scored_cells=len(scored), n_qshare_channel_tests=len(zq), qshare_max_z=max(zq) if zq else None,
               qshare_n_beyond_3sigma=int(sum(1 for z in zq if z > 3)))
    finish("C2", rec)
    return 0


def check_C3():
    L = 16
    cells = []
    tot_dis1 = tot_dis2 = tot_srv = 0
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        st = c2_states(L, rng)
        for name, (psi0, masks) in st.items():
            server = psi0.copy()
            server.flags.writeable = False
            snap = server.copy()
            sha0 = hashlib.sha256(server.tobytes()).hexdigest()
            client = server.copy()
            Qj = H.charges(client, masks)
            keep = [j for j in range(len(masks)) if Qj[j] >= 1e-12]
            if len(keep) < 2:
                cells.append(dict(seed=seed, state=name, label="UNINFORMATIVE")); continue
            km = [masks[j] for j in keep]
            Q = float(Qj[keep].sum())
            counts, pw, k1 = draw(rng, H.charges(client, km))
            k2 = np.empty(NSHOT, int); k3 = np.empty(NSHOT, int)
            lock_bytes_equal = True
            for jj in range(len(keep)):
                sel = np.where(k1 == jj)[0]
                if sel.size == 0:
                    continue
                lk, _ = H.lock_to_channel(client, km[jj]); lk = lk * math.sqrt(Q)
                w2 = H.charges(lk, km)
                k2[sel] = rng.choice(len(keep), size=sel.size, p=w2 / w2.sum())
                lk2 = lk.copy()
                lock_bytes_equal &= bool(np.array_equal(lk2, lk))
                w3 = H.charges(lk2, km)
                k3[sel] = rng.choice(len(keep), size=sel.size, p=w3 / w3.sum())
            srv_diff = 0
            for _ in range(NSHOT):
                if not np.array_equal(server, snap):
                    srv_diff += 1
            sha1 = hashlib.sha256(server.tobytes()).hexdigest()
            d1 = int(np.sum(k2 != k1)); d2 = int(np.sum(k3 != k1))
            tot_dis1 += d1; tot_dis2 += d2; tot_srv += srv_diff + (sha0 != sha1)
            cells.append(dict(seed=seed, state=name, label="scored", nshot=NSHOT, counts=counts,
                              repeat_disagreements=d1, second_client_disagreements=d2,
                              server_byte_differences=srv_diff, server_sha256_before=sha0, server_sha256_after=sha1,
                              second_client_copy_bytes_equal=lock_bytes_equal))
    scored = [c for c in cells if c["label"] == "scored"]
    lab = "UNINFORMATIVE" if not scored else ("PASS" if tot_dis1 == 0 and tot_dis2 == 0 and tot_srv == 0 else "FAIL")
    finish("C3", dict(label=lab, cells=cells, total_repeat_disagreements=tot_dis1,
                      total_second_client_disagreements=tot_dis2, total_server_differences=tot_srv,
                      uninformative=[f"{c['seed']} {c['state']}" for c in cells if c['label'] != 'scored']))
    return 0


# ---------------------------------------------------------------- C4
def c4_partitions(L):
    X, Y, Z = site_coords(L)
    h, q = L // 2, L // 4
    quad = [(X < h) & (Y < h), (X < h) & (Y >= h), (X >= h) & (Y < h), (X >= h) & (Y >= h)]
    slab = [(X >= i * q) & (X < (i + 1) * q) for i in range(4)]
    bx, by = (X // q) % 2, (Y // q) % 2
    cheq = [(bx == 0) & (by == 0), (bx == 0) & (by == 1), (bx == 1) & (by == 0), (bx == 1) & (by == 1)]
    return dict(quadrants=quad, slabs_x=slab, chequer=cheq)


def check_C4():
    L = 16
    parts = c4_partitions(L)
    cells = []
    for pidx, (pname, masks) in enumerate(parts.items()):
        for si, seed in enumerate(SEEDS):
            rng = np.random.default_rng(seed)  # state construction: unchanged from the first run
            rng_shot = np.random.default_rng([seed, pidx])  # r2 fix 2: shots independent per (seed, partition)
            if si < 4:
                psi = rescale(H.random_orbit_state(L, rng), masks, [0.4, 0.3, 0.2, 0.1]); sname = "random_0.4/0.3/0.2/0.1"
            else:
                psi = H.localized_packet(L, rng, 2.0, centre=np.array([L // 2] * 3, float), spin=rand_spin(rng)); sname = "packet"
            Qj = H.charges(psi, masks)
            merged = [masks[0], masks[1] | masks[2], masks[3]]
            QR = 1.0 - float(Qj.sum()) / norm2(psi)
            cell = dict(partition=pname, partition_index=pidx, shot_rng_entropy=[seed, pidx], seed=seed, state=sname,
                        Q=Qj, merge_QR_over_Q=QR)
            if (Qj < 1e-12).any() or QR > 1e-6:
                cell["label"] = "UNINFORMATIVE"; cells.append(cell); continue
            rules = {}
            for rname, p in (("Qshare", 2.0), ("p1", 1.0), ("p4", 4.0)):
                cu, wu, _ = draw(rng_shot, H.charges_power(psi, masks, p))
                cm, wm, _ = draw(rng_shot, H.charges_power(psi, merged, p))
                fu, fm = cu / NSHOT, cm / NSHOT
                sA = math.sqrt(wu[0] * (1 - wu[0]) / NSHOT + wm[0] * (1 - wm[0]) / NSHOT)
                sD = math.sqrt(wu[3] * (1 - wu[3]) / NSHOT + wm[2] * (1 - wm[2]) / NSHOT)
                wbc = wu[1] + wu[2]
                sBC = math.sqrt(wbc * (1 - wbc) / NSHOT + wm[1] * (1 - wm[1]) / NSHOT)
                dA, dD, dBC = fm[0] - fu[0], fm[2] - fu[3], fm[1] - (fu[1] + fu[2])
                rules[rname] = dict(w_unmerged=wu, w_merged=wm, counts_unmerged=cu, counts_merged=cm,
                                    shift_A=dA, sigma_A=sA, z_A=zval(dA, sA), shift_D=dD, sigma_D=sD, z_D=zval(dD, sD),
                                    additivity_diff=dBC, sigma_BC=sBC, z_BC=zval(dBC, sBC),
                                    ok3=within(dA, sA, 3) and within(dD, sD, 3) and within(dBC, sBC, 3),
                                    shift_beyond5=(not within(dA, sA, 5)) or (not within(dD, sD, 5)))
            cell["rules"] = rules; cell["label"] = "scored"
            cells.append(cell)
    scored = [c for c in cells if c["label"] == "scored"]
    qfail = [f"{c['partition']} {c['seed']}" for c in scored if not c["rules"]["Qshare"]["ok3"]]
    ctrl = {r: any(c["rules"][r]["shift_beyond5"] for c in scored) for r in ("p1", "p4")}
    if not scored:
        lab = "UNINFORMATIVE"
    elif not qfail and all(ctrl.values()):
        lab = "PASS"
    else:
        lab = "FAIL"
    finish("C4", dict(label=lab, cells=cells, qshare_failures=qfail, control_shift_found=ctrl,
                      control_note="controls weight w_k ∝ sum_{i in k}|a_i|^p as in design §2",
                      uninformative=[f"{c['partition']} {c['seed']}" for c in cells if c['label'] != 'scored']))
    return 0


# ---------------------------------------------------------------- C5
def c5_state(name, L, spin4=None):
    c = L // 2
    cen = np.array([c, c, c], float)
    rng0 = np.random.default_rng(0)  # unused by localized_packet when spin is given
    if name == "S1":
        sp = [np.array([1, 0, 0, 0], complex)]
    elif name == "S2":
        sp = [np.array([1, 1, 0, 0], complex) / math.sqrt(2)]
    elif name == "S3":
        sp = [np.array([1, 0, 0, 1], complex) / math.sqrt(2)]
    elif name == "S4":
        sp = [spin4]
    if name != "S5":
        return H.localized_packet(L, rng0, 1.5, centre=cen, spin=sp[0]), [cen]
    c2 = cen.copy(); c2[1] = (c2[1] + 16) % L
    a = H.localized_packet(L, rng0, 1.5, centre=cen, spin=np.array([1, 0, 0, 0], complex))
    b = H.localized_packet(L, rng0, 1.5, centre=c2, spin=np.array([0, 0, 0, 1], complex))
    psi = a + b
    return psi / math.sqrt(norm2(psi)), [cen, c2]


_MASKS = {}


def voronoi(L, axis, centres, d):
    key = (L, axis, tuple(tuple(c) for c in centres), d)
    if key in _MASKS:
        return _MASKS[key]
    X = site_coords(L)
    plus_c, minus_c = [], []
    for c in centres:
        e = np.zeros(3); e[axis] = d
        plus_c.append((c + e) % L); minus_c.append((c - e) % L)

    def nearest(cs):
        best = None
        for ci, c in enumerate(cs):
            dv = [mi(X[i] - c[i], L) for i in range(3)]
            d2 = dv[0] ** 2 + dv[1] ** 2 + dv[2] ** 2
            if best is None:
                best = [d2, np.zeros(d2.shape, int)]
            else:
                upd = d2 < best[0]
                best[0] = np.where(upd, d2, best[0]); best[1] = np.where(upd, ci, best[1])
        return best
    d2p, ip = nearest(plus_c)
    d2m, im = nearest(minus_c)
    P, M = np.array(plus_c), np.array(minus_c)
    sepv = mi(P[ip] - M[im], L)  # (...,3)
    sep = np.sqrt(np.sum(sepv ** 2, axis=-1))
    with np.errstate(divide="ignore", invalid="ignore"):
        bdist = np.where(sep > 0, np.abs(d2p - d2m) / (2 * sep), 0.0)
    band = bdist <= 1.0
    plus = (d2p < d2m) & ~band
    minus = (d2m < d2p) & ~band
    _MASKS[key] = (plus, minus, band)
    return _MASKS[key]


def fine_masks(L, axis, fg, factor):
    """Fine-graining j: list of (spatial mask or None, component list)."""
    X = site_coords(L)
    c = L // 2
    b, cc = (axis + 1) % 3, (axis + 2) % 3
    allc = [0, 1, 2, 3]
    if fg == "FG1_halves":
        r = mi(X[b] - c, L)
        return [(r >= 0, allc), (r < 0, allc)]
    if fg == "FG2_quadrants":
        r1, r2 = mi(X[b] - c, L), mi(X[cc] - c, L)
        return [((r1 >= 0) & (r2 >= 0), allc), ((r1 >= 0) & (r2 < 0), allc),
                ((r1 < 0) & (r2 >= 0), allc), ((r1 < 0) & (r2 < 0), allc)]
    if fg == "FG3_unread_factor":
        if factor == "sigma":
            return [(None, [0, 1]), (None, [2, 3])]   # tau_z = R / L
        return [(None, [0, 2]), (None, [1, 3])]       # sigma_z = up / down


def chg(moved, mask, comps):
    sub = moved[comps]
    if mask is None:
        return float(np.sum(np.abs(sub) ** 2))
    return float(np.sum(np.abs(sub[:, mask]) ** 2))


def prepare_cell(name, n, factor, spin4):
    """Return geometry dict for an informative cell (L=32,d=8, retry L=64,d=16) or the UNINFORMATIVE record."""
    tries = []
    for L, d in ((32, 8), (64, 16)):
        psi, cents = c5_state(name, L, spin4)
        P = H.projector_sigma(n)[0] if factor == "sigma" else H.projector_tau(n)[0]
        pi_n = H.factor_expect(psi, P)
        moved, axis, nh = H.spin_dependent_shift(psi, n, d, factor=factor)
        plus, minus, band = voronoi(L, axis, cents, d)
        Qp, Qm, Qb = chg(moved, plus, [0, 1, 2, 3]), chg(moved, minus, [0, 1, 2, 3]), chg(moved, band, [0, 1, 2, 3])
        Qt = norm2(moved)
        overlap = bool((plus & minus).any())
        un = Qb / Qt
        tries.append(dict(L=L, d=d, unassigned_fraction=un, Qplus=Qp, Qminus=Qm, pi_n=pi_n))
        if un <= 1e-6 and not overlap and Qt >= 1e-12:
            return dict(ok=True, L=L, d=d, axis=axis, moved=moved, plus=plus, minus=minus, pi_n=pi_n,
                        Qp=Qp, Qm=Qm, tries=tries)
    return dict(ok=False, tries=tries)


def fine_charges(g, fac, FGS):
    """r2 fix 1: the C5(c)/(d) fine-graining charges, computed from g["moved"] once, so moved can be discarded.
    Same masks and arithmetic as the first run's inline code."""
    out = {}
    for fg in FGS:
        fm = fine_masks(g["L"], g["axis"], fg, fac)
        qpj, qmj = [], []
        for (sm, comps) in fm:
            mp_ = g["plus"] if sm is None else (g["plus"] & sm)
            mm_ = g["minus"] if sm is None else (g["minus"] & sm)
            qpj.append(chg(g["moved"], mp_, comps)); qmj.append(chg(g["moved"], mm_, comps))
        qpj, qmj = np.array(qpj), np.array(qmj)
        Q = g["Qp"] + g["Qm"]
        out[fg] = (qpj, qmj, 1.0 - (qpj.sum() + qmj.sum()) / Q)
    return out


def check_C5():
    sph = fib_dirs(50)
    dirs = [("fib", i, v) for i, v in enumerate(sph)] + [("axis", i, v) for i, v in enumerate(AXIS_DIRS)]
    states = ["S1", "S2", "S3", "S4", "S5"]
    factors = ["sigma", "tau"]
    rngs = {s: np.random.default_rng(s) for s in SEEDS}
    spin4 = {s: rand_spin(rngs[s]) for s in SEEDS}
    geo = {}
    FGS = ["FG1_halves", "FG2_quadrants", "FG3_unread_factor"]
    cdirs = [(i, sph[i]) for i in range(0, 40, 2)]
    need_fine = {(st, "fib", i, fac, None) for st in ["S2", "S3", "S5"] for (i, _) in cdirs for fac in factors}
    b_cells = []
    for st in states:
        for (kind, i, n) in dirs:
            for fac in factors:
                for seed in SEEDS:
                    gkey = (st, kind, i, fac, seed if st == "S4" else None)
                    if gkey not in geo:
                        geo[gkey] = prepare_cell(st, n, fac, spin4[seed] if st == "S4" else None)
                        # r2 fix 1: keep only scalars and (for C5(c)/(d) cells) the fine charges; drop the arrays
                        gg = geo[gkey]
                        if gg["ok"]:
                            if gkey in need_fine:
                                gg["fine"] = fine_charges(gg, fac, FGS)
                            for k in ("moved", "plus", "minus"):
                                gg.pop(k, None)
                    g = geo[gkey]
                    cell = dict(state=st, dir_kind=kind, dir_index=i, n=n, factor=fac, seed=seed,
                                official=(kind == "fib"), tries=g["tries"])
                    if not g["ok"]:
                        cell["label"] = "UNINFORMATIVE"; b_cells.append(cell); continue
                    Q = g["Qp"] + g["Qm"]
                    cnt, pw, _ = draw(rngs[seed], [g["Qp"], g["Qm"]])
                    wh = cnt[0] / NSHOT
                    sig = math.sqrt(pw[0] * (1 - pw[0]) / NSHOT)
                    diff = wh - g["pi_n"]
                    cell.update(L=g["L"], d=g["d"], w_hat=wh, pi_n=g["pi_n"], sigma=sig, z=zval(diff, sig),
                                within3=within(diff, sig, 3), label="scored")
                    b_cells.append(cell)
    off_b = [c for c in b_cells if c["official"]]
    sc_b = [c for c in off_b if c["label"] == "scored"]
    fail_b = [c for c in sc_b if not c["within3"]]
    lab_b = "UNINFORMATIVE" if not sc_b else ("FAIL" if fail_b else "PASS")
    zb = [c["z"] for c in sc_b]
    # C5(c) and C5(d)
    c_cells, d_cells = [], []
    for st in ["S2", "S3", "S5"]:
        for (i, n) in cdirs:
            for fac in factors:
                g = geo[(st, "fib", i, fac, None)]
                for fg in FGS:
                    if g["ok"]:
                        qpj, qmj, fine_res = g["fine"][fg]  # r2 fix 1: precomputed in the (b) loop
                        Q = g["Qp"] + g["Qm"]
                    for seed in SEEDS:
                        rng = rngs[seed]
                        base = dict(state=st, dir_index=i, factor=fac, fine_graining=fg, seed=seed)
                        if not g["ok"] or abs(fine_res) > 1e-6:
                            c_cells.append(dict(base, label="UNINFORMATIVE"))
                            continue
                        # Q-share (C5(c))
                        cc_, pc, _ = draw(rng, [g["Qp"], g["Qm"]])
                        cf, pf, _ = draw(rng, np.concatenate([qpj, qmj]))
                        J = len(qpj)
                        wc_hat, wf_hat = cc_[0] / NSHOT, cf[:J].sum() / NSHOT
                        wf = pf[:J].sum()
                        sig = math.sqrt(pc[0] * (1 - pc[0]) / NSHOT + wf * (1 - wf) / NSHOT)
                        diff = wc_hat - wf_hat
                        c_cells.append(dict(base, label="scored", L=g["L"], q_plus_j=qpj, q_minus_j=qmj,
                                            fine_residual=fine_res, w_coarse_hat=wc_hat, w_fine_sum_hat=wf_hat,
                                            sigma=sig, z=zval(diff, sig), within3=within(diff, sig, 3)))
                        if st not in ("S2", "S3"):
                            continue
                        for rule in ("g3", "g1", "g4"):
                            def gplus(qp, qm):
                                q = qp + qm
                                if q < 1e-12:
                                    return 0.0
                                if rule == "g3":
                                    x = (qp - qm) / q
                                    return (1 + x ** 3) / 2
                                pp = {"g1": 1.0, "g4": 4.0}[rule]
                                a, b = qp ** (pp / 2), qm ** (pp / 2)
                                return a / (a + b)
                            wc_p = gplus(g["Qp"], g["Qm"])
                            wcw = [wc_p, 1 - wc_p]
                            wfw = [(qpj[j] + qmj[j]) / Q * gplus(qpj[j], qmj[j]) for j in range(J)] + \
                                  [(qpj[j] + qmj[j]) / Q * (1 - gplus(qpj[j], qmj[j])) if (qpj[j] + qmj[j]) >= 1e-12 else 0.0 for j in range(J)]
                            ccn, pcn, _ = draw(rng, wcw)
                            cfn, pfn, _ = draw(rng, wfw)
                            wch, wfh = ccn[0] / NSHOT, cfn[:J].sum() / NSHOT
                            wfp = pfn[:J].sum()
                            sid = math.sqrt(pcn[0] * (1 - pcn[0]) / NSHOT + wfp * (1 - wfp) / NSHOT)
                            did = wch - wfh
                            # C2 per-channel drift on the coarse read: E[Q_+ after] - Q_+
                            ddr = wch * Q - g["Qp"]
                            sdr = Q * math.sqrt(pcn[0] * (1 - pcn[0]) / NSHOT)
                            d_cells.append(dict(base, rule=rule, w_coarse=pcn[0], w_fine_sum=wfp,
                                                identity_diff=did, identity_sigma=sid, identity_z=zval(did, sid),
                                                identity_beyond5=not within(did, sid, 5),
                                                drift=ddr, drift_sigma=sdr, drift_z=zval(ddr, sdr),
                                                drift_beyond5=not within(ddr, sdr, 5)))
    sc_c = [c for c in c_cells if c["label"] == "scored"]
    fail_c = [c for c in sc_c if not c["within3"]]
    lab_c = "UNINFORMATIVE" if not sc_c else ("FAIL" if fail_c else "PASS")
    zc = [c["z"] for c in sc_c]
    rejected = {}
    for rule in ("g3", "g1", "g4"):
        tests = {}
        for c in d_cells:
            if c["rule"] != rule:
                continue
            k_id = (c["state"], c["dir_index"], c["factor"], "identity_" + c["fine_graining"])
            k_dr = (c["state"], c["dir_index"], c["factor"], "drift_coarse_read_of_" + c["fine_graining"])
            tests.setdefault(k_id, {})[c["seed"]] = c["identity_beyond5"]
            tests.setdefault(k_dr, {})[c["seed"]] = c["drift_beyond5"]
        consistent = [list(k) for k, v in tests.items() if len(v) == 5 and all(v.values())]
        rejected[rule] = dict(rejected=bool(consistent), n_consistent_tests=len(consistent),
                              example=consistent[:5], n_tests=len(tests))
    lab_d = "PASS" if all(v["rejected"] for v in rejected.values()) else "FAIL"
    if not d_cells:
        lab_d = "UNINFORMATIVE"
    rec = dict(
        label="NOT PASSED (D10: C5(a) does not pass; C5 is not treated as passed while §5.5 stays a two-outcome primitive)",
        C5a="does not pass (read-only audit L2_0_C5A_AUDIT.md sha256 423920fe845e26df1871e0e2a5ebc044c780735919c1df1af3c47ecabf683090; not rerun)",
        C5b=dict(label=lab_b, n_official_cells=len(off_b), n_scored=len(sc_b),
                 n_uninformative=len(off_b) - len(sc_b), n_beyond_3sigma=len(fail_b),
                 max_z=max(zb) if zb else None,
                 failures=[{k: c[k] for k in ("state", "dir_index", "factor", "seed", "w_hat", "pi_n", "sigma", "z", "L")} for c in fail_b],
                 uninformative=[{k: c[k] for k in ("state", "dir_index", "factor", "seed")} for c in off_b if c["label"] != "scored"],
                 n_retried_L64=sum(1 for c in off_b if c["label"] == "scored" and c["L"] == 64),
                 axis_reporting_cells_scored=sum(1 for c in b_cells if not c["official"] and c["label"] == "scored"),
                 axis_reporting_beyond_3sigma=sum(1 for c in b_cells if not c["official"] and c["label"] == "scored" and not c["within3"])),
        C5c=dict(label=lab_c, n_cells=len(c_cells), n_scored=len(sc_c), n_beyond_3sigma=len(fail_c),
                 max_z=max(zc) if zc else None,
                 failures=[{k: c[k] for k in ("state", "dir_index", "factor", "fine_graining", "seed", "z")} for c in fail_c],
                 uninformative=[{k: c[k] for k in ("state", "dir_index", "factor", "fine_graining", "seed")} for c in c_cells if c["label"] != "scored"]),
        C5d=dict(label=lab_d, controls=rejected, n_cells=len(d_cells)),
        b_cells=b_cells, c_cells=c_cells, d_cells=d_cells)
    finish("C5", rec)
    return 0


if __name__ == "__main__":
    if os.environ.get("L20_SCORE") != "1" or not OUT:
        print("refusing: L20_SCORE=1 and L20_OUT required"); sys.exit(2)
    name = sys.argv[1]
    got, ok = hashes()
    if not ok:
        print("hash mismatch", got); sys.exit(3)
    H.log("start", name)
    sys.exit({"S0": check_S0, "C1": check_C1, "C2": check_C2, "C3": check_C3, "C4": check_C4, "C5": check_C5}[name]())
