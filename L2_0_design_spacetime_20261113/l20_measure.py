#!/usr/bin/env python3
"""L2.0 measurement code for C1-C5 on the canonical dirac4 rule (one BCC orbit, phi=1.4).

Written 13 November 2026 (America/New_York) to accompany L2_0_RUN_DESIGN.md in this folder.
Imports the hashed frozen dirac4.py in ./frozen/ (sha256
f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff).
Does not import /workspace/qca/bcc.py.

This file scores nothing unless it is invoked as a named check after Edmond has
named the design sha256. The --probe path only records wall time, CPU time and
peak RSS of small, unsized-down pieces of the same procedures; it writes
L2_0_PROBE_TIMING.json and must not be used as a C1-C5 result.

usage:
  l20_measure.py --probe
  l20_measure.py --check C1|C2|C3|C4|C5b|C5c|C5d|S0
Environment L20_RUN sets the run folder (default: this design folder).
"""
from __future__ import annotations

import os, sys, time, json, hashlib, argparse, resource, math, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.join(HERE, "frozen")
sys.path.insert(0, FROZEN)
import dirac4  # noqa: E402

PHI = 1.4
M_DEFAULT = 0.0
HOPS = [(hx, hy, hz) for hx in (1, -1) for hy in (1, -1) for hz in (1, -1)]
DIRAC4_SHA = "f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff"
S0, SX, SY, SZ = dirac4.S0, dirac4.SX, dirac4.SY, dirac4.SZ
I2 = np.eye(2, dtype=complex)
I4 = dirac4.I4
SIG = (SX, SY, SZ)
# Component order of frozen dirac4: (R, L) tensor (sigma); sigma acts in the last factor.
SIG4 = tuple(np.kron(I2, s) for s in SIG)
TAU4 = tuple(np.kron(s, I2) for s in SIG)

P_POWERS = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0)
# Displacements that appear as y-z for y, z in {0} union the 8 corner neighbours.
def _neighbourhood_displacements():
    pts = [(0, 0, 0)] + list(HOPS)
    D = set()
    for a in pts:
        for b in pts:
            D.add((a[0] - b[0], a[1] - b[1], a[2] - b[2]))
    return tuple(sorted(D))

DISPLACEMENTS = _neighbourhood_displacements()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def peak_rss_mib():
    # Linux ru_maxrss is in kibibytes.
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def cpu_s():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# ---------------------------------------------------------------------------
# Cycle symbol (frozen U_cycle) and FFT stepper on one BCC orbit in an L-cell
# ---------------------------------------------------------------------------
def U_cycle(k, phi=PHI, m=M_DEFAULT):
    return dirac4.U_cycle(np.asarray(k, float), phi=phi, m=m, wilson=True, patch=False, wilson_mass=0.0)


def k_grid(L):
    n = np.fft.fftfreq(L, d=1.0 / L).astype(int)
    kx, ky, kz = np.meshgrid(n, n, n, indexing="ij")
    return 2 * np.pi * np.stack([kx, ky, kz], axis=-1) / L


def precompute_U(L, phi=PHI, m=M_DEFAULT):
    k = k_grid(L)
    U = np.empty((L, L, L, 4, 4), complex)
    # Vectorised evaluation is not provided by frozen dirac4; loop is fine at L<=32.
    flat = k.reshape(-1, 3)
    out = U.reshape(-1, 4, 4)
    for i, ki in enumerate(flat):
        out[i] = U_cycle(ki, phi, m)
    return U


def fft_cycle(psi, Ugrid):
    pk = np.fft.fftn(psi, axes=(1, 2, 3))
    pk = np.einsum("xyzij,jxyz->ixyz", Ugrid, pk)
    return np.fft.ifftn(pk, axes=(1, 2, 3))


def orbit_mask(L):
    """True on the one BCC orbit: all-even or all-odd integer coordinates."""
    x = np.arange(L)
    xx, yy, zz = np.meshgrid(x, x, x, indexing="ij")
    even = ((xx & 1) == 0) & ((yy & 1) == 0) & ((zz & 1) == 0)
    odd = ((xx & 1) == 1) & ((yy & 1) == 1) & ((zz & 1) == 1)
    return even | odd


def random_orbit_state(L, rng, mask=None):
    if mask is None:
        mask = orbit_mask(L)
    re = rng.standard_normal((4, L, L, L))
    im = rng.standard_normal((4, L, L, L))
    psi = (re + 1j * im)
    psi[:, ~mask] = 0
    n = math.sqrt(float(np.sum(np.abs(psi) ** 2)))
    return psi / n


def localized_packet(L, rng, width=2.0, centre=None, spin=None):
    """Gaussian envelope on the orbit, internal spinor `spin` (default random)."""
    if centre is None:
        centre = np.array([L // 2, L // 2, L // 2], float)
    if spin is None:
        v = rng.normal(size=4) + 1j * rng.normal(size=4)
        spin = v / np.linalg.norm(v)
    x = np.arange(L)
    xx, yy, zz = np.meshgrid(x, x, x, indexing="ij")
    # minimum-image distance
    def mi(a, c):
        d = (a - c + L / 2) % L - L / 2
        return d
    r2 = mi(xx, centre[0]) ** 2 + mi(yy, centre[1]) ** 2 + mi(zz, centre[2]) ** 2
    env = np.exp(-r2 / (2 * width * width))
    mask = orbit_mask(L)
    env = env * mask
    psi = spin[:, None, None, None] * env[None]
    n = math.sqrt(float(np.sum(np.abs(psi) ** 2)))
    return psi / n


def p_norms(psi, powers=P_POWERS):
    a = np.abs(psi)
    return {p: float(np.sum(a ** p)) for p in powers}


# ---------------------------------------------------------------------------
# C1: local conserved quadratic forms on node + 8 neighbours
# ---------------------------------------------------------------------------
def half_displacements():
    """Split D minus 0 into pairs {h, -h}; return positive representatives."""
    pos = []
    seen = set()
    for h in DISPLACEMENTS:
        if h == (0, 0, 0):
            continue
        if h in seen or tuple(-x for x in h) in seen:
            continue
        # pick a stable representative: first in lexicographic of {h,-h}
        mh = tuple(-x for x in h)
        rep = min(h, mh)
        pos.append(rep)
        seen.add(h)
        seen.add(mh)
    return pos


def pack_params(M0_h, Mh_list):
    """Flatten Hermitian M0 (16 real) and general 4x4 Mh (32 real each) to a real vector."""
    parts = [M0_h.real.diagonal()]  # 4
    iu = np.triu_indices(4, 1)
    parts.append(M0_h.real[iu])
    parts.append(M0_h.imag[iu])
    for M in Mh_list:
        parts.append(M.real.ravel())
        parts.append(M.imag.ravel())
    return np.concatenate(parts)


def n_params(n_h):
    return 16 + 32 * n_h


def apply_params_to_symbol(k, vec, pos_h):
    """m(k) from parameter vector. k shape (3,)."""
    M = np.zeros((4, 4), complex)
    # M0 Hermitian
    diag = vec[0:4]
    iu = np.triu_indices(4, 1)
    n_off = iu[0].size
    re_off = vec[4:4 + n_off]
    im_off = vec[4 + n_off:16]
    M0 = np.zeros((4, 4), complex)
    M0[np.diag_indices(4)] = diag
    M0[iu] = re_off + 1j * im_off
    M0 = M0 + M0.conj().T - np.diag(np.diag(M0))
    M = M + M0
    off = 16
    kx, ky, kz = k
    for h in pos_h:
        re = vec[off:off + 16].reshape(4, 4)
        im = vec[off + 16:off + 32].reshape(4, 4)
        off += 32
        Mh = re + 1j * im
        phase = np.exp(1j * (h[0] * kx + h[1] * ky + h[2] * kz))
        M = M + Mh * phase + Mh.conj().T * np.conj(phase)
    return M


def constraint_row_blocks(k, pos_h, phi=PHI, m=M_DEFAULT):
    """Linear map R^{npar} -> R^{16} given by (U dagger m U - m) at this k, as a (16, npar) matrix."""
    U = U_cycle(k, phi, m)
    npar = n_params(len(pos_h))
    # Build by columns (one-hot). For npar=560 this is 560 U-multiplies; acceptable at a few hundred k.
    # Faster: differentiate m linearly in the packed basis.
    cols = np.empty((16, npar), float)
    e = np.zeros(npar)
    for j in range(npar):
        e[j] = 1.0
        mk = apply_params_to_symbol(k, e, pos_h)
        e[j] = 0.0
        C = U.conj().T @ mk @ U - mk
        cols[:, j] = np.concatenate([C.real[np.triu_indices(4)], C.imag[np.triu_indices(4, 1)]])
        # wait, triu real is 10, imag off is 6, total 16. Good.
        # Actually I used triu for real including diagonal (10) + imag strict (6) = 16.
    return cols


def build_constraint_matrix(k_points, pos_h, phi=PHI, m=M_DEFAULT, log_every=0):
    npar = n_params(len(pos_h))
    blocks = []
    for i, k in enumerate(k_points):
        blocks.append(constraint_row_blocks(k, pos_h, phi, m))
        if log_every and (i + 1) % log_every == 0:
            log("constraint rows", i + 1, "of", len(k_points))
    return np.vstack(blocks)


def constraint_matrix_fast(k_points, pos_h, phi=PHI, m=M_DEFAULT):
    """Same linear map, built from an explicit basis of m(k) generators (one matrix-vector per column shared).

    For each parameter, m(k) is a known combination of e^{ik·h} times a matrix unit.
    """
    npar = n_params(len(pos_h))
    n_k = len(k_points)
    A = np.zeros((16 * n_k, npar), float)
    Us = [U_cycle(k, phi, m) for k in k_points]
    # Precompute, for each k, the 16-vector extractor
    def pack_herm_diff(C):
        return np.concatenate([C.real[np.triu_indices(4)], C.imag[np.triu_indices(4, 1)]])

    # Column j: one-hot still, but we evaluate m(k) cheaply by structure.
    # M0 diagonal entries j=0..3
    def add_columns():
        iu = np.triu_indices(4, 1)
        n_off = iu[0].size
        # helper: for a generator mk(k), fill column
        def fill_col(j, mk_of_k):
            for i, (k, U) in enumerate(zip(k_points, Us)):
                mk = mk_of_k(k)
                C = U.conj().T @ mk @ U - mk
                A[16 * i:16 * (i + 1), j] = pack_herm_diff(C)

        # M0 diagonal
        for a in range(4):
            E = np.zeros((4, 4), complex)
            E[a, a] = 1.0
            fill_col(a, lambda k, E=E: E)
        # M0 real off-diag: E_ab + E_ba
        for t in range(n_off):
            a, b = iu[0][t], iu[1][t]
            E = np.zeros((4, 4), complex)
            E[a, b] = 1.0
            E[b, a] = 1.0
            fill_col(4 + t, lambda k, E=E: E)
        # M0 imag off-diag: i E_ab - i E_ba
        for t in range(n_off):
            a, b = iu[0][t], iu[1][t]
            E = np.zeros((4, 4), complex)
            E[a, b] = 1j
            E[b, a] = -1j
            fill_col(4 + n_off + t, lambda k, E=E: E)
        off = 16
        for h in pos_h:
            # Mh real entry (c,d): contrib Mh e^{ikh} + Mh^T e^{-ikh} for real parameter of Re Mh_cd
            # If param is Re Mh_cd, mk = E_cd e^{ikh} + E_dc e^{-ikh}
            # If param is Im Mh_cd, mk = i E_cd e^{ikh} - i E_dc e^{-ikh}
            for c in range(4):
                for d in range(4):
                    # real
                    jre = off + (c * 4 + d)
                    jim = off + 16 + (c * 4 + d)
                    Ecd = np.zeros((4, 4), complex)
                    Ecd[c, d] = 1.0
                    Edc = np.zeros((4, 4), complex)
                    Edc[d, c] = 1.0

                    def mk_re(k, Ecd=Ecd, Edc=Edc, h=h):
                        ph = np.exp(1j * (h[0] * k[0] + h[1] * k[1] + h[2] * k[2]))
                        return Ecd * ph + Edc * np.conj(ph)

                    def mk_im(k, Ecd=Ecd, Edc=Edc, h=h):
                        ph = np.exp(1j * (h[0] * k[0] + h[1] * k[1] + h[2] * k[2]))
                        return 1j * Ecd * ph - 1j * Edc * np.conj(ph)

                    fill_col(jre, mk_re)
                    fill_col(jim, mk_im)
            off += 32
    add_columns()
    return A


def nullspace_svd(A, atol=1e-8, grey_lo=1e-8, grey_hi=1e-4):
    _, s, vh = np.linalg.svd(A, full_matrices=True)
    npar = vh.shape[1] if vh.ndim == 2 else A.shape[1]
    # s has length min(shape)
    # pad if needed
    if s.size < npar:
        s_full = np.zeros(npar)
        s_full[: s.size] = s
    else:
        s_full = s
    n_clear = int(np.sum(s_full < atol))
    n_grey = int(np.sum((s_full >= grey_lo) & (s_full < grey_hi)))
    # basis: right singular vectors with s < atol
    idx = np.where(s_full < atol)[0]
    # vh rows correspond to singular values then leftover free dims
    basis = vh[idx] if idx.size else np.zeros((0, npar))
    return dict(singular_values=s_full, n_clear=n_clear, n_grey=n_grey, basis=basis, atol=atol)


def identity_params(pos_h):
    """Parameter vector for m(k) = I_4 (the |a|^2 charge)."""
    v = np.zeros(n_params(len(pos_h)))
    v[0:4] = 1.0
    return v


# ---------------------------------------------------------------------------
# Client read primitives used by C2-C5 (rule unitary + exclusive channels)
# ---------------------------------------------------------------------------
def charges(psi, masks):
    return np.array([float(np.sum(np.abs(psi[:, m]) ** 2)) if m.ndim == 3 else float(np.sum(np.abs(psi[m]) ** 2))
                     for m in masks])


def charges_power(psi, masks, p):
    out = []
    for m in masks:
        if m.ndim == 3:
            a = np.abs(psi[:, m])
        else:
            a = np.abs(psi[m])
        out.append(float(np.sum(a ** p)))
    return np.array(out)


def lock_to_channel(psi, mask):
    out = np.zeros_like(psi)
    if mask.ndim == 3:
        out[:, mask] = psi[:, mask]
    else:
        out[mask] = psi[mask]
    n = math.sqrt(float(np.sum(np.abs(out) ** 2)))
    if n == 0:
        return out, 0.0
    return out / n, n


def sample_channel(weights, rng):
    w = np.asarray(weights, float)
    s = w.sum()
    if s <= 0:
        return None
    w = w / s
    return int(rng.choice(len(w), p=w))


def onsite_apply(psi, M):
    sh = psi.shape
    return (M @ psi.reshape(4, -1)).reshape(sh)


def projector_sigma(n_hat):
    n_hat = np.asarray(n_hat, float)
    n_hat = n_hat / np.linalg.norm(n_hat)
    nsig = n_hat[0] * SIG4[0] + n_hat[1] * SIG4[1] + n_hat[2] * SIG4[2]
    return 0.5 * (I4 + nsig), 0.5 * (I4 - nsig), n_hat


def projector_tau(n_hat):
    n_hat = np.asarray(n_hat, float)
    n_hat = n_hat / np.linalg.norm(n_hat)
    ntau = n_hat[0] * TAU4[0] + n_hat[1] * TAU4[1] + n_hat[2] * TAU4[2]
    return 0.5 * (I4 + ntau), 0.5 * (I4 - ntau), n_hat


def factor_expect(psi, P):
    """⟨P⟩ for an on-site 4x4 projector P."""
    phi = onsite_apply(psi, P)
    return float(np.vdot(psi.ravel(), phi.ravel()).real)


def spin_dependent_shift(psi, n_hat, d, factor="sigma"):
    """Discrete Stern-Gerlach embedding: project on factor·n = ±1, translate by ±d along nearest axis."""
    if factor == "sigma":
        Pp, Pm, nh = projector_sigma(n_hat)
    else:
        Pp, Pm, nh = projector_tau(n_hat)
    axis = int(np.argmax(np.abs(nh)))
    # axis 0,1,2 -> spatial axes of the (4,L,L,L) array (1,2,3)
    spa = axis + 1
    plus = onsite_apply(psi, Pp)
    minus = onsite_apply(psi, Pm)
    plus = np.roll(plus, d, axis=spa)
    minus = np.roll(minus, -d, axis=spa)
    return plus + minus, axis, nh


def halfspace_masks(L, axis, origin=None):
    """Two exclusive half-spaces along `axis` (0,1,2), split at origin (default L//2)."""
    if origin is None:
        origin = L // 2
    coords = np.arange(L)
    # Use a cyclic half-window of length L//2 starting just after origin-d? Simpler: < origin vs >= origin
    # After shifts ±d from a packet at origin, + lives near origin+d, - near origin-d.
    x = [np.arange(L) for _ in range(3)]
    grids = np.meshgrid(*x, indexing="ij")
    coord = grids[axis]
    # minimum-image coordinate relative to origin
    rel = (coord - origin + L // 2) % L - L // 2
    plus = rel > 0
    minus = rel < 0
    mid = rel == 0
    # mid-plane is assigned to neither; exclusivity requires mid charge ~ 0
    return plus, minus, mid


# ---------------------------------------------------------------------------
# Probe path (timing only)
# ---------------------------------------------------------------------------
def probe(out_path):
    rec = dict(
        note="Unscored timing probe for L2_0_RUN_DESIGN.md. Not a C1-C5 result. No gate is scored.",
        time_local=time.strftime("%Y-%m-%d %H:%M:%S %Z"),
        dirac4_sha256=sha256_file(os.path.join(FROZEN, "dirac4.py")),
        expected_dirac4_sha256=DIRAC4_SHA,
        phi=PHI,
        m=M_DEFAULT,
        displacements=len(DISPLACEMENTS),
        n_params=n_params(len(half_displacements())),
        pieces={},
    )
    assert rec["dirac4_sha256"] == DIRAC4_SHA

    # Unitarity of U_cycle at a few k.
    t0, c0, m0 = time.time(), cpu_s(), peak_rss_mib()
    rng = np.random.default_rng(20261113)
    ks = rng.uniform(-np.pi, np.pi, size=(32, 3))
    ks = np.vstack([ks, [0, 0, 0], [np.pi, 0, 0], [0.4, 0.8, 1.2]])
    resid = 0.0
    for k in ks:
        U = U_cycle(k)
        resid = max(resid, float(np.linalg.norm(U.conj().T @ U - I4, ord=2)))
    rec["pieces"]["U_cycle_unitarity"] = dict(
        n_k=len(ks), max_dev_from_unitary=resid,
        wall_s=time.time() - t0, cpu_s=cpu_s() - c0, peak_rss_mib=max(m0, peak_rss_mib()),
    )

    # FFT evolution timing at L=16 and L=32, 40 cycles (then scale).
    for L in (16, 32):
        t0, c0, m0 = time.time(), cpu_s(), peak_rss_mib()
        Ugrid = precompute_U(L)
        t_pre = time.time() - t0
        psi = localized_packet(L, np.random.default_rng(1), width=2.0)
        # also a random state
        psi_r = random_orbit_state(L, np.random.default_rng(2))
        n_cyc = 40
        t1 = time.time()
        hist = {p: [] for p in P_POWERS}
        p = psi.copy()
        for _ in range(n_cyc):
            for pp, val in p_norms(p).items():
                hist[pp].append(val)
            p = fft_cycle(p, Ugrid)
        for pp, val in p_norms(p).items():
            hist[pp].append(val)
        t_ev = time.time() - t1
        # wrap a second state for a second timing sample
        t2 = time.time()
        q = psi_r
        for _ in range(n_cyc):
            q = fft_cycle(q, Ugrid)
        t_ev_r = time.time() - t2
        rec["pieces"][f"fft_L{L}"] = dict(
            precompute_U_s=t_pre,
            cycles=n_cyc,
            packet_evolve_s=t_ev,
            s_per_cycle_packet=t_ev / n_cyc,
            random_evolve_s=t_ev_r,
            s_per_cycle_random=t_ev_r / n_cyc,
            projected_1000_cycles_s=1000.0 * (t_ev / n_cyc),
            # relative drifts over 40 cycles, recorded only as a timing-harness sanity, not a C1 result
            rel_drift_40_cycles={str(pp): float(abs(np.array(h)[-1] / h[0] - 1)) for pp, h in hist.items()},
            wall_s=time.time() - t0, cpu_s=cpu_s() - c0, peak_rss_mib=max(m0, peak_rss_mib()),
        )

    # Constraint-matrix + SVD timing. Use a reduced k-set for the clock, plus one
    # 8^3 build. Physics numbers from the SVD are omitted on purpose.
    pos_h = half_displacements()
    rng = np.random.default_rng(3)
    for tag, kpts in (
        ("k_random_40", rng.uniform(-np.pi, np.pi, size=(40, 3))),
        ("k_grid_6cubed", np.array(list(itertools.product(*[np.linspace(-np.pi, np.pi, 6, endpoint=False)] * 3)))),
    ):
        t0, c0, m0 = time.time(), cpu_s(), peak_rss_mib()
        A = constraint_matrix_fast(kpts, pos_h)
        t_build = time.time() - t0
        t1 = time.time()
        s = np.linalg.svd(A, compute_uv=False)
        t_svd = time.time() - t1
        rec["pieces"][f"algebra_{tag}"] = dict(
            n_k=len(kpts), n_eq=A.shape[0], n_par=A.shape[1],
            build_s=t_build, svd_s=t_svd,
            # spectrum endpoints only, so the cost model can judge conditioning; no nullspace count
            s_max=float(s[0]), s_min=float(s[-1]),
            wall_s=time.time() - t0, cpu_s=cpu_s() - c0, peak_rss_mib=max(m0, peak_rss_mib()),
        )

    # Client-read shot loop: 1e5 draws from a 4-channel weight vector (no evolution).
    t0, c0, m0 = time.time(), cpu_s(), peak_rss_mib()
    rng = np.random.default_rng(4)
    w = np.array([0.5, 0.3, 0.15, 0.05])
    nshots = 100_000
    hits = np.zeros(4, int)
    for _ in range(nshots):
        hits[sample_channel(w, rng)] += 1
    rec["pieces"]["shots_1e5_four_channel"] = dict(
        nshots=nshots, wall_s=time.time() - t0, cpu_s=cpu_s() - c0,
        peak_rss_mib=max(m0, peak_rss_mib()),
        s_per_1e5=time.time() - t0,
    )

    # Factor hop + charge totals at L=16, 50 directions, 5 states (the C5b geometry, one seed, no shots).
    t0, c0, m0 = time.time(), cpu_s(), peak_rss_mib()
    L = 16
    rng = np.random.default_rng(5)
    states = [
        localized_packet(L, rng, width=1.5, spin=np.array([1, 0, 0, 0], complex)),
        localized_packet(L, rng, width=1.5, spin=np.array([1, 1, 0, 0], complex) / math.sqrt(2)),
        localized_packet(L, rng, width=1.5, spin=np.array([1, 0, 1, 0], complex) / math.sqrt(2)),
        localized_packet(L, rng, width=1.5) + np.roll(localized_packet(L, rng, width=1.5, centre=np.array([L//2+4, L//2, L//2], float)), 0, axis=2),
        random_orbit_state(L, rng),
    ]
    # renormalize state 3
    states[3] = states[3] / math.sqrt(float(np.sum(np.abs(states[3]) ** 2)))
    # 50 directions on a Fibonacci sphere
    n_dir = 50
    ga = math.pi * (3 - math.sqrt(5))
    dirs = []
    for i in range(n_dir):
        z = 1 - 2 * (i + 0.5) / n_dir
        r = math.sqrt(max(0.0, 1 - z * z))
        th = ga * i
        dirs.append(np.array([r * math.cos(th), r * math.sin(th), z]))
    d_shift = 4
    mid_charge = 0.0
    n_ok = 0
    for psi in states:
        for nh in dirs:
            moved, axis, _ = spin_dependent_shift(psi, nh, d_shift, factor="sigma")
            plus, minus, mid = halfspace_masks(L, axis)
            Qp = float(np.sum(np.abs(moved[:, plus]) ** 2))
            Qm = float(np.sum(np.abs(moved[:, minus]) ** 2))
            Qmid = float(np.sum(np.abs(moved[:, mid]) ** 2))
            mid_charge = max(mid_charge, Qmid)
            if Qmid <= 1e-8:
                n_ok += 1
    rec["pieces"]["c5b_geometry_L16_50x5"] = dict(
        n_pairs=len(states) * n_dir,
        shift_d=d_shift,
        max_midplane_charge=mid_charge,
        n_exclusive_pairs=n_ok,
        wall_s=time.time() - t0, cpu_s=cpu_s() - c0, peak_rss_mib=max(m0, peak_rss_mib()),
        note="max_midplane_charge and n_exclusive_pairs are geometry-timing sanity, not a C5 result.",
    )

    rec["peak_rss_mib_end"] = peak_rss_mib()
    rec["cpu_s_end"] = cpu_s()
    with open(out_path, "w") as f:
        json.dump(rec, f, indent=1)
    log("wrote", out_path, "peak_MiB", rec["peak_rss_mib_end"])
    return rec


# ---------------------------------------------------------------------------
# Check stubs: present so the scored run can call the same file later.
# They refuse to score unless L20_SCORE=1 is set after a named design hash.
# ---------------------------------------------------------------------------
def refuse_score(name):
    log(name, "not scored. This file scores a check only when L20_SCORE=1 is set")
    log("after the design sha256 has been named. No output of this invocation is a result.")
    return 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--check", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    if args.probe:
        out = args.out or os.path.join(HERE, "L2_0_PROBE_TIMING.json")
        probe(out)
        return 0
    if args.check:
        if os.environ.get("L20_SCORE") != "1":
            return refuse_score(args.check)
        log("scored path is not filled in this design drop; the procedures live in L2_0_RUN_DESIGN.md")
        return 2
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
