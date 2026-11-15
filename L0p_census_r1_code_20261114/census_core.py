"""L0' census r1: rule definitions, symbols and real-space engines.
Design: /workspace/L0p_census_design_r1_20261114/L0P_CENSUS_DESIGN_r1.md
sha256 c2673a6426ca5728738c7e7e63871bd26577e8475e9b2819d9980aeccb642fd1
"""
import itertools
import numpy as np

EPS64 = 2.220446049250313e-16
S0_ = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)
SIG = [SX, SY, SZ]
I4 = np.eye(4, dtype=complex)
PR = np.kron(np.diag([1., 0.]), S0_).astype(complex)
PL = np.kron(np.diag([0., 1.]), S0_).astype(complex)
TX = np.kron(SX, S0_)                  # tau_x (x) 1 = beta
BETA = TX
ALPHA = [np.kron(SZ, s) for s in SIG]  # tau_z (x) sigma_i
E = np.eye(3, dtype=int)
SQ3 = np.sqrt(3.0)


def Rb(s):  # sigma on R block
    return np.kron(np.diag([1., 0.]), s).astype(complex)


def Lb(s):  # sigma on L block
    return np.kron(np.diag([0., 1.]), s).astype(complex)


# ---------------------------------------------------------------- layers
# A layer is dict: terms {h (tuple of 3 ints): C (d x d)}, hop: bool.
# Action: (L psi)(x) = sum_h C_h psi(x - h); symbol sum_h C_h exp(-i k.h).

def layer_shifts(d, shifts):
    """shifts: list of (axis, M, P) with P a block projector, M Hermitian
    involution on that block (M = P M P, M^2 = P). Each block makes one
    conditional face shift along its axis; components outside all blocks
    are untouched."""
    terms = {}
    C0 = np.eye(d, dtype=complex)
    for axis, M, P in shifts:
        C0 = C0 - P
        hp = tuple(E[axis]); hm = tuple(-E[axis])
        terms[hp] = terms.get(hp, 0) + (P + M) / 2
        terms[hm] = terms.get(hm, 0) + (P - M) / 2
    if np.abs(C0).max() > 0:
        terms[(0, 0, 0)] = C0
    return {'terms': terms, 'hop': True}


def layer_onsite(Mat):
    return {'terms': {(0, 0, 0): np.array(Mat, complex)}, 'hop': False}


def adjoint_layer(L):
    return {'terms': {tuple(-np.array(h)): C.conj().T for h, C in L['terms'].items()},
            'hop': L['hop']}


def layer_symbol(L, k, d):
    """k: (...,3) -> (..., d, d)"""
    k = np.asarray(k, float)
    if '_H' not in L:          # cache stacked hop vectors and coefficient matrices
        hs = list(L['terms'].keys())
        L['_H'] = np.array(hs, float).T                                   # (3, nh)
        L['_C'] = np.stack([L['terms'][h] for h in hs]).reshape(len(hs), d * d)
    ph = np.exp(-1j * (k.reshape(-1, 3) @ L['_H']))                       # (P, nh)
    return (ph @ L['_C']).reshape(k.shape[:-1] + (d, d))


def cycle_symbol(layers, k, d):
    k = np.asarray(k, float)
    U = np.broadcast_to(np.eye(d, dtype=complex), k.shape[:-1] + (d, d)).copy()
    for L in layers:
        U = layer_symbol(L, k, d) @ U
    return U


# --------------------------------------------------------- building blocks
def expm_tx(phi, sign):  # exp(sign * i * phi * tau_x)
    return np.cos(phi) * I4 + sign * 1j * np.sin(phi) * TX


def S_layers(eps):
    """S^eps = diag(A^eps, A^eps dag) as three face sub-steps."""
    if eps > 0:   # R applies z,y,x with +sigma; L applies x,y,z with -sigma
        pairs = [(2, 0), (1, 1), (0, 2)]
    else:         # R applies x,y,z with +sigma; L applies z,y,x with -sigma
        pairs = [(0, 2), (1, 1), (2, 0)]
    return [layer_shifts(4, [(ra, Rb(SIG[ra]), PR), (la, Lb(-SIG[la]), PL)])
            for ra, la in pairs]


def L_A_layers(eps, dag):
    """L-block conditional shifts realising diag(1, A^eps) (dag=False) or
    diag(1, A^eps dag) (dag=True)."""
    # A+ = e^{-ix sx} e^{-iy sy} e^{-iz sz}: applied z,y,x with +sigma
    # A- = e^{-iz sz} e^{-iy sy} e^{-ix sx}: applied x,y,z with +sigma
    order = [2, 1, 0] if eps > 0 else [0, 1, 2]
    sign = 1.0
    if dag:
        order = order[::-1]; sign = -1.0
    return [layer_shifts(4, [(a, Lb(sign * SIG[a]), PL)]) for a in order]


def V_layers(eps, phi):
    """V^eps = Q e^{-i phi tx} Q^dag e^{i phi tx}, Q = diag(1, A^eps dag).
    Applied: e^{i phi tx}, Q^dag (= diag(1, A^eps)), e^{-i phi tx}, Q."""
    return ([layer_onsite(expm_tx(phi, +1))] + L_A_layers(eps, dag=False) +
            [layer_onsite(expm_tx(phi, -1))] + L_A_layers(eps, dag=True))


def W_layers(i, phi):
    """W_i = Q_i e^{-i phi tx} Q_i^dag e^{i phi tx}, Q_i = diag(1, e^{i k_i s_i})."""
    return [layer_onsite(expm_tx(phi, +1)),
            layer_shifts(4, [(i, Lb(SIG[i]), PL)]),     # Q_i^dag = diag(1, e^{-ik s})
            layer_onsite(expm_tx(phi, -1)),
            layer_shifts(4, [(i, Lb(-SIG[i]), PL)])]    # Q_i = diag(1, e^{+ik s})


def VF_layers(eps, phi):
    # V_F+ = W_z W_y W_x (W_x applied first); V_F- = W_x W_y W_z (W_z first)
    order = [0, 1, 2] if eps > 0 else [2, 1, 0]
    out = []
    for i in order:
        out += W_layers(i, phi)
    return out


def compose_to_corner_layer(layers, d):
    """Compose sub-layers into one layer by exact 3^3 DFT (symbol degree <= 1
    per axis). Used for B0's four layers."""
    g = 2 * np.pi * np.arange(3) / 3
    K = np.array(list(itertools.product(g, g, g)))
    Us = cycle_symbol(layers, K, d)
    terms = {}
    for h in itertools.product([-1, 0, 1], repeat=3):
        C = np.einsum('k,kij->ij', np.exp(1j * (K @ np.array(h, float))), Us) / 27.0
        if np.abs(C).max() > 1e-13:
            terms[h] = C
    hop = any(h != (0, 0, 0) for h in terms)
    return {'terms': terms, 'hop': hop}


# ---------------------------------------------------------- staggered C2
def stag_index(s):
    return s[0] + 2 * s[1] + 4 * s[2]


SUBS = [tuple(s) for s in itertools.product([0, 1], repeat=3)]
SUBS = sorted(SUBS, key=stag_index)


def eta(i, x):
    if i == 0:
        return 1
    if i == 1:
        return (-1) ** int(x[0])
    return (-1) ** int(x[0] + x[1])


def stag_bond_layer(i, p, theta):
    """8x8 Bloch layer (site-position phase convention)."""
    terms = {(0, 0, 0): np.cos(theta) * np.eye(8, dtype=complex)}
    hm = tuple(-E[i]); hp = tuple(E[i])
    Cm = np.zeros((8, 8), complex); Cp = np.zeros((8, 8), complex)
    for s in SUBS:
        a = stag_index(s)
        t = list(s); t[i] ^= 1; b = stag_index(t)
        if s[i] % 2 == p:      # left site: partner at +e_i, phase e^{+ik_i}
            Cm[a, b] += eta(i, s) * np.sin(theta)
        else:                  # right site: partner at -e_i, phase e^{-ik_i}
            Cp[a, b] += -eta(i, s) * np.sin(theta)
    terms[hm] = Cm; terms[hp] = Cp
    return {'terms': terms, 'hop': True, 'bond': (i, p, theta)}


C2_ORDER = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1),
            (2, 1), (2, 0), (1, 1), (1, 0), (0, 1), (0, 0)]


# ------------------------------------------------------------ candidates
CAND_INDEX = {'B0': 0, 'C1': 1, 'C2': 2, 'C3': 3, 'C4': 4, 'RC3': 5}
R1_TABLE = {  # components, declared knobs, hop layers, on-site layers (r1 table)
    'B0': (4, 1, 4, 0), 'C1': (4, 1, 18, 12), 'C2': (1, 1, 12, 0),
    'C3': (4, 1, 18, 4), 'C4': (2, 0, 6, 0), 'RC3': (4, 1, 30, 16)}


def make_candidate(name, knob):
    if name == 'C4':
        Ap = [layer_shifts(2, [(a, SIG[a], S0_)]) for a in (2, 1, 0)]
        Am = [layer_shifts(2, [(a, SIG[a], S0_)]) for a in (0, 1, 2)]
        return dict(name=name, d=2, lattice='sc', layers=Ap + Am)
    if name == 'C2':
        layers = [stag_bond_layer(i, p, knob) for i, p in C2_ORDER]
        return dict(name=name, d=8, lattice='stag', layers=layers)
    phi = knob
    if name == 'C3':
        layers = S_layers(+1) + V_layers(+1, phi) + S_layers(-1) + V_layers(-1, phi)
    elif name == 'C1':
        layers = S_layers(+1) + VF_layers(+1, phi) + S_layers(-1) + VF_layers(-1, phi)
    elif name == 'RC3':
        layers = (S_layers(+1) + V_layers(+1, phi) + VF_layers(+1, phi) +
                  S_layers(-1) + V_layers(-1, phi) + VF_layers(-1, phi))
    elif name == 'B0':
        groups = [S_layers(+1), V_layers(+1, phi), S_layers(-1), V_layers(-1, phi)]
        layers = [compose_to_corner_layer(g, 4) for g in groups]
        return dict(name=name, d=4, lattice='bcc', layers=layers)
    else:
        raise ValueError(name)
    return dict(name=name, d=4, lattice='sc', layers=layers)


def layer_counts(cand):
    hop = sum(1 for L in cand['layers'] if L['hop'])
    return hop, len(cand['layers']) - hop


# ------------------------------------------------------- lattice helpers
def gamma_dist(k, lattice):
    """distance (grid units) from k to nearest Gamma image."""
    k = np.asarray(k, float)
    if lattice == 'sc':
        d = k - 2 * np.pi * np.round(k / (2 * np.pi)); return float(np.linalg.norm(d))
    if lattice == 'stag':
        d = k - np.pi * np.round(k / np.pi); return float(np.linalg.norm(d))
    g0 = np.round(k / np.pi)
    best = 1e9
    for off in itertools.product([-1, 0, 1], repeat=3):
        g = g0 + np.array(off)
        if int(g.sum()) % 2 == 0:
            best = min(best, float(np.linalg.norm(k - np.pi * g)))
    return best


def equivalent(k1, k2, lattice, tol=1e-5):
    d = np.asarray(k1, float) - np.asarray(k2, float)
    if lattice == 'sc':
        r = d - 2 * np.pi * np.round(d / (2 * np.pi)); return np.linalg.norm(r) < tol
    if lattice == 'stag':
        r = d - np.pi * np.round(d / np.pi); return np.linalg.norm(r) < tol
    g = np.round(d / np.pi)
    if np.linalg.norm(d - np.pi * g) < tol and int(g.sum()) % 2 == 0:
        return True
    return False


def high_symmetry_points(lattice):
    pts = []
    if lattice == 'sc':
        for c in itertools.product([0, np.pi], repeat=3):
            pts.append(c)
    elif lattice == 'stag':
        for c in itertools.product([0, np.pi / 2], repeat=3):
            pts.append(c)
    else:
        for c in itertools.product([0, np.pi], repeat=3):   # Gamma, H, and images
            pts.append(c)
        for perm in set(itertools.permutations([np.pi / 2, np.pi / 2, 0])):  # N
            for sg in itertools.product([1, -1], repeat=3):
                pts.append(tuple(np.array(perm) * np.array(sg)))
        for sg in itertools.product([1, -1], repeat=3):   # P
            pts.append(tuple(np.pi / 2 * np.array(sg)))
    return [np.array(p, float) for p in pts]


def ell_grid(lattice):
    """grid units per ell."""
    return SQ3 if lattice == 'bcc' else 1.0


# ------------------------------------------------------ real-space engines
class SCEngine:
    """psi shape (B, d, L, L, L) on Z^3 periodic."""
    def __init__(self, cand, L):
        self.c = cand; self.L = L; self.d = cand['d']

    def apply(self, psi, layer):
        B, d = psi.shape[:2]
        out = np.zeros_like(psi)
        for h, C in layer['terms'].items():
            src = psi if h == (0, 0, 0) else np.roll(psi, shift=h, axis=(2, 3, 4))
            out += np.matmul(C, src.reshape(B, d, -1)).reshape(psi.shape)
        return out

    def positions(self):
        L = self.L; a = np.arange(L); a = np.where(a > L // 2, a - L, a)
        return a

    def mask(self):
        return np.ones((self.L,) * 3, bool)


class BCCEngine:
    """psi shape (B, d, 2, M, M, M): sublattice 0 = psi(2y), 1 = psi(2y+1)."""
    def __init__(self, cand, L):
        assert L % 2 == 0
        self.c = cand; self.L = L; self.M = L // 2; self.d = cand['d']

    def apply(self, psi, layer):
        B, d = psi.shape[:2]
        out = np.zeros_like(psi)
        Ev = psi[:, :, 0]; Od = psi[:, :, 1]
        for h, C in layer['terms'].items():
            h = np.array(h)
            if not h.any():
                out += np.matmul(C, psi.reshape(B, d, -1)).reshape(psi.shape)
                continue
            assert np.all(np.abs(h) == 1)
            se = tuple((h + 1) // 2); so = tuple((h - 1) // 2)
            out[:, :, 0] += np.matmul(C, np.roll(Od, shift=se, axis=(2, 3, 4)).reshape(B, d, -1)).reshape(Ev.shape)
            out[:, :, 1] += np.matmul(C, np.roll(Ev, shift=so, axis=(2, 3, 4)).reshape(B, d, -1)).reshape(Od.shape)
        return out

    def cart(self):
        """Cartesian coordinates (a/2 units) of the two sublattices: (2, M,M,M,3)."""
        y = np.stack(np.meshgrid(*(np.arange(self.M),) * 3, indexing='ij'), -1)
        return np.stack([2 * y, 2 * y + 1])


class StagEngine:
    """psi shape (B, L, L, L): one component per site."""
    def __init__(self, cand, L):
        assert L % 2 == 0
        self.c = cand; self.L = L
        x = np.stack(np.meshgrid(*(np.arange(L),) * 3, indexing='ij'), -1)
        self.x = x
        self.eta = [np.ones((L,) * 3), (-1.0) ** x[..., 0], (-1.0) ** (x[..., 0] + x[..., 1])]
        self.par = [x[..., i] % 2 for i in range(3)]

    def apply_bond(self, psi, i, p, theta):
        left = (self.par[i] == p)
        fwd = np.roll(psi, shift=-1, axis=1 + i)   # psi(x + e_i)
        bwd = np.roll(psi, shift=+1, axis=1 + i)   # psi(x - e_i)
        et = self.eta[i]
        return (np.cos(theta) * psi + np.sin(theta) * np.where(left, et * fwd, -et * bwd))

    def apply(self, psi, layer):
        i, p, th = layer['bond']
        return self.apply_bond(psi, i, p, th)

    def apply_adj(self, psi, layer):
        i, p, th = layer['bond']
        return self.apply_bond(psi, i, p, -th)


def make_engine(cand, L):
    if cand['lattice'] == 'sc':
        return SCEngine(cand, L)
    if cand['lattice'] == 'bcc':
        return BCCEngine(cand, L)
    return StagEngine(cand, L)


def run_cycle(eng, psi, adjoint=False, callback=None):
    layers = eng.c['layers']
    seq = layers[::-1] if adjoint else layers
    for L in seq:
        if isinstance(eng, StagEngine):
            psi = eng.apply_adj(psi, L) if adjoint else eng.apply(psi, L)
        else:
            psi = eng.apply(psi, adjoint_layer(L) if adjoint else L)
        if callback is not None:
            callback(psi, L)
    return psi


# ------------------------------------------- k-space operators (FFT based)
def stag_D(k):
    """diag(e^{i k.s}) for the 8 sublattices; k (...,3)."""
    S = np.array(SUBS, float)  # (8,3)
    return np.exp(1j * (np.asarray(k)[..., None, :] * S).sum(-1))   # (...,8)


def cell_symbol_stag(cand, q):
    """Operator acting on cell-FFT amplitudes phi_hat(q): D M(q/2) D^dag."""
    k = np.asarray(q) / 2.0
    M = cycle_symbol(cand['layers'], k, 8)
    D = stag_D(k)
    return D[..., :, None] * M * D.conj()[..., None, :]


def matpow(U, n):
    """U (..., d, d), integer n >= 0 by repeated squaring."""
    d = U.shape[-1]
    R = np.broadcast_to(np.eye(d, dtype=complex), U.shape).copy()
    P = U.copy()
    while n > 0:
        if n & 1:
            R = P @ R
        n >>= 1
        if n:
            P = P @ P
    return R
