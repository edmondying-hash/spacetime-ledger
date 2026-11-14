#!/usr/bin/env python3
"""
3-Generation Baryogenesis on the 3D 6-Face Planck-Cube Grid  (revision r2, 2026-11-13).

Status: CONJECTURE / TOY.  Edmond's guess linking 3 generations to the baryon asymmetry.
Nothing here is derived from the lattice yet.  What changed from r1:
  * CP violation now comes from the real CKM matrix (PDG 2024 angles), not sin(phase).
  * "No CP violation below 3 generations" is now *shown* numerically (rephasing a
    general 2x2 unitary matrix; Jarlskog determinant vanishing for degenerate masses),
    not hard-coded.
  * The per-decay bias epsilon is an OUTPUT: the value the lattice would have to
    supply to reach the observed eta, given the real J.  It is no longer tuned in.
  * Every remaining hand-set number is listed in the KNOBS block below.

Data sources (inputs, not knobs):
  * CKM: PDG 2024, Review "CKM Quark-Mixing Matrix" (rev. 31 May 2024), Eq. (12.28):
        sin th12 = 0.22501 +- 0.00068, sin th13 = 0.003732 +0.000090 -0.000085,
        sin th23 = 0.04183 +0.00079 -0.00069, delta = 1.147 +- 0.026 rad,
        and the global-fit Jarlskog invariant J = 3.12 +0.13 -0.12 x 1e-5.
        https://pdg.lbl.gov/2024/reviews/rpp2024-rev-ckm-matrix.pdf
  * eta = n_B / n_gamma ~ 6.1e-10: Planck 2018 VI (arXiv:1807.06209),
        Omega_b h^2 = 0.02237 +- 0.00015, consistent with BBN (PDG BBN review).
  * Number of light neutrinos from the Z width: N_nu = 2.9840 +- 0.0082
        (ALEPH, DELPHI, L3, OPAL, SLD, Phys. Rept. 427 (2006) 257).
        Quoted as DATA only; the lattice tick table below does not test it.
  * Quark masses for the degeneracy demo only (PDG 2024, GeV, rough):
        u 0.00216, c 1.27, t 172.69; d 0.00467, s 0.0934, b 4.18.

Physics caveat kept on the record: in the real Standard Model the CP-violating measure
J * prod(m^2 differences) / T^12 is ~1e-20 at the electroweak scale, ~1e-10 short of
what baryogenesis needs, and the m_H = 125 GeV electroweak transition is a crossover
(no departure from equilibrium).  This toy does not solve either problem.
"""

import cmath
import math
import random
from typing import Any, Dict, List, Sequence

# ---------------------------------------------------------------------------
# KNOBS  -- every hand-set number that is NOT measured data.  Each is a knob.
# ---------------------------------------------------------------------------
KNOB_STEP_FACTOR_21 = 0.5          # KNOB: Gen2->Gen1 bias = 0.5 * Gen3->Gen2 bias
KNOB_PHOTONS_PER_PAIR = 2.0        # KNOB: photons per annihilated pair (only annihilation photons counted)
KNOB_WASHOUT_KAPPA = 1.0           # KNOB placeholder: fraction surviving inverse decays/washout (1 = none)
KNOB_PHOTON_DILUTION = 1.0         # KNOB placeholder: dilution from annihilation photons to thermal bath (1 = none)
KNOB_GEN_TICKS = {                 # KNOB: tick loads per generation (typed in, not derived)
    "Gen 1 (u, d, e)": ("1D Linear Hop", 18.0),
    "Gen 2 (c, s, mu)": ("2D Planar Turn", 44.0),
    "Gen 3 (t, b, tau)": ("3D Volumetric Twist", 82.0),
    "Gen 4 (Hypothetical)": ("Over-Cap Multi-Loop", 128.0),
}
KNOB_NODE_CAP = 100.0              # KNOB: node throughput cap in ticks
KNOBS = {
    "KNOB_STEP_FACTOR_21": KNOB_STEP_FACTOR_21,
    "KNOB_PHOTONS_PER_PAIR": KNOB_PHOTONS_PER_PAIR,
    "KNOB_WASHOUT_KAPPA": KNOB_WASHOUT_KAPPA,
    "KNOB_PHOTON_DILUTION": KNOB_PHOTON_DILUTION,
    "KNOB_GEN_TICKS": {k: v[1] for k, v in KNOB_GEN_TICKS.items()},
    "KNOB_NODE_CAP": KNOB_NODE_CAP,
}

# ---------------------------------------------------------------------------
# DATA (measured inputs, with sources above)
# ---------------------------------------------------------------------------
PDG2024_S12, PDG2024_S13, PDG2024_S23, PDG2024_DELTA = 0.22501, 0.003732, 0.04183, 1.147
PDG2024_J, PDG2024_J_ERR_UP, PDG2024_J_ERR_DN = 3.12e-5, 0.13e-5, 0.12e-5
ETA_TARGET = 6.1e-10               # Planck 2018 / BBN
LEP_N_NU, LEP_N_NU_ERR = 2.9840, 0.0082
J_MAX = 1.0 / (6.0 * math.sqrt(3.0))   # mathematical maximum of |J| for any 3x3 unitary matrix
QUARK_MASSES_GEV = {"up": (0.00216, 1.27, 172.69), "down": (0.00467, 0.0934, 4.18)}

Matrix = List[List[complex]]


# --------------------------- small complex linear algebra -------------------
def _matmul(a: Matrix, b: Matrix) -> Matrix:
    n, m, p = len(a), len(b), len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def _dagger(a: Matrix) -> Matrix:
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]


def _diag(vals: Sequence[complex]) -> Matrix:
    n = len(vals)
    return [[complex(vals[i]) if i == j else 0j for j in range(n)] for i in range(n)]


def _det3(m: Matrix) -> complex:
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def unitarity_defect(u: Matrix) -> float:
    """max |(U U^dagger - 1)_ij|."""
    p = _matmul(u, _dagger(u))
    return max(abs(p[i][j] - (1.0 if i == j else 0.0)) for i in range(len(u)) for j in range(len(u)))


# --------------------------- CKM and Jarlskog --------------------------------
def ckm_standard(s12: float = PDG2024_S12, s13: float = PDG2024_S13,
                 s23: float = PDG2024_S23, delta: float = PDG2024_DELTA) -> Matrix:
    """PDG standard parametrisation, Eq. (12.3) of the PDG 2024 CKM review."""
    c12, c13, c23 = (math.sqrt(1 - s * s) for s in (s12, s13, s23))
    e = cmath.exp(1j * delta)
    return [
        [c12 * c13, s12 * c13, s13 / e],
        [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
        [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13],
    ]


def quartet_im(v: Matrix, i: int = 0, j: int = 1, k: int = 1, l: int = 2) -> float:
    """Rephasing-invariant Im(V_ij V_kl V_il* V_kj*).  Default = Im(V_us V_cb V_ub* V_cs*) = J."""
    return (v[i][j] * v[k][l] * v[i][l].conjugate() * v[k][j].conjugate()).imag


def jarlskog(v: Matrix) -> float:
    return quartet_im(v, 0, 1, 1, 2)


def rephase(v: Matrix, row_phases: Sequence[float], col_phases: Sequence[float]) -> Matrix:
    """V -> diag(e^{i a}) V diag(e^{i b}): a pure quark-field redefinition (unphysical)."""
    return [[cmath.exp(1j * row_phases[r]) * v[r][c] * cmath.exp(1j * col_phases[c])
             for c in range(len(v[0]))] for r in range(len(v))]


def physical_cp_phases(n_gen: int) -> int:
    """N^2 real params of U(N) = N(N-1)/2 angles + N(N+1)/2 phases; 2N-1 phases removable."""
    if n_gen < 1:
        raise ValueError("n_gen must be >= 1")
    return (n_gen - 1) * (n_gen - 2) // 2


def random_unitary_2x2(rng: random.Random) -> Matrix:
    """General U(2): e^{i a} [[e^{i b} c, e^{i g} s], [-e^{-i g} s, e^{-i b} c]]."""
    th, a, b, g = (rng.uniform(0, 2 * math.pi) for _ in range(4))
    c, s = math.cos(th), math.sin(th)
    ea = cmath.exp(1j * a)
    return [[ea * cmath.exp(1j * b) * c, ea * cmath.exp(1j * g) * s],
            [-ea * cmath.exp(-1j * g) * s, ea * cmath.exp(-1j * b) * c]]


def rephase_2x2_to_real(u: Matrix) -> Matrix:
    """Choose 3 field phases (2 rows + 2 cols, one overall redundant) making U real."""
    a1, a2 = -cmath.phase(u[0][0]), -cmath.phase(u[1][0]) + math.pi
    b2 = -cmath.phase(u[0][1]) - a1
    return rephase(u, [a1, a2], [0.0, b2])


def two_generation_check(trials: int = 200, seed: int = 2026) -> Dict[str, float]:
    """N=2: the only quartet Im(U11 U22 U12* U21*) is zero, and U rephases to a real rotation."""
    rng = random.Random(seed)
    max_quartet, max_imag_after = 0.0, 0.0
    for _ in range(trials):
        u = random_unitary_2x2(rng)
        max_quartet = max(max_quartet, abs(quartet_im(u, 0, 0, 1, 1)))
        r = rephase_2x2_to_real(u)
        max_imag_after = max(max_imag_after, max(abs(x.imag) for row in r for x in row))
    return {"trials": trials, "max_abs_quartet": max_quartet, "max_imag_after_rephasing": max_imag_after}


def jarlskog_determinant(v: Matrix, up_masses: Sequence[float], down_masses: Sequence[float]) -> complex:
    """det[M_u M_u^dag, M_d M_d^dag] in the up-diagonal basis = 2i J F_u F_d (up to sign)."""
    hu = _diag([m * m for m in up_masses])
    hd = _matmul(_matmul(v, _diag([m * m for m in down_masses])), _dagger(v))
    a, b = _matmul(hu, hd), _matmul(hd, hu)
    return _det3([[a[i][j] - b[i][j] for j in range(3)] for i in range(3)])


def mass_factor(m: Sequence[float]) -> float:
    m1, m2, m3 = (x * x for x in m)
    return (m3 - m2) * (m3 - m1) * (m2 - m1)


# --------------------------- cascade ----------------------------------------
def eta_closed_form(eps: float, j: float, step: float = KNOB_STEP_FACTOR_21) -> float:
    """Exact cascade result for step=0.5, photons=2: eta = 2b/(3 - 2b + b^2/2), b = eps*J (~ (2/3) eps J)."""
    if step != 0.5 or KNOB_PHOTONS_PER_PAIR != 2.0:
        raise ValueError("closed form written for step 0.5 and 2 photons per pair")
    b = eps * j
    return 2 * b / (3 - 2 * b + b * b / 2) * KNOB_WASHOUT_KAPPA / KNOB_PHOTON_DILUTION


def required_epsilon(eta_target: float = ETA_TARGET, j: float = None) -> float:
    """Invert the closed form: epsilon per decay the lattice must supply to reach eta_target."""
    j = jarlskog(ckm_standard()) if j is None else j
    e = eta_target * KNOB_PHOTON_DILUTION / KNOB_WASHOUT_KAPPA
    # (e/2) b^2 - (2 + 2e) b + 3e = 0, small root (cancellation-free form 2c / (-B + sqrt(B^2 - 4ac)))
    a, bq, c = e / 2, -(2 + 2 * e), 3 * e
    b = 2 * c / (-bq + math.sqrt(bq * bq - 4 * a * c))
    return b / j


class BCCBaryogenesisSim:
    """3D lattice cascade: Gen3 -> Gen2 -> Gen1 with CP bias eps * J, J from the mixing matrix."""

    def __init__(self, initial_per_gen: int = 10000, seed: int = 2026):
        self.initial_per_gen = initial_per_gen
        self.seed = seed

    def cp_invariant(self, n_gen: int) -> float:
        """Rephasing-invariant CP measure computed from an n_gen x n_gen mixing matrix."""
        if n_gen == 3:
            return jarlskog(ckm_standard())
        if n_gen == 2:   # most general U(2): computed, not assumed (comes out ~1e-17)
            return quartet_im(random_unitary_2x2(random.Random(self.seed)), 0, 0, 1, 1)
        if n_gen == 1:   # a 1x1 phase has no quartet: no rephasing-invariant CP measure exists
            return 0.0
        raise ValueError("3D lattice supports 1, 2, or 3 orthogonal generations.")

    def simulate_universe(self, n_gen: int, eps_3d: float = None) -> Dict[str, Any]:
        """Evolve an exact 50/50 matter/antimatter population through the Gen 3 -> 2 -> 1 cascade."""
        if n_gen not in (1, 2, 3):
            raise ValueError("3D lattice supports 1, 2, or 3 orthogonal generations.")
        j_cp = self.cp_invariant(n_gen)
        if eps_3d is None:
            eps_3d = required_epsilon(j=jarlskog(ckm_standard()))
        matter = {g: float(self.initial_per_gen) for g in range(1, n_gen + 1)}
        anti = {g: float(self.initial_per_gen) for g in range(1, n_gen + 1)}
        total_initial = sum(matter.values()) + sum(anti.values())

        if n_gen == 3:
            bias_32 = eps_3d * j_cp
            matter[2] += matter[3] * (1.0 + bias_32)
            anti[2] += anti[3] * (1.0 - bias_32)
            matter[3], anti[3] = 0.0, 0.0
        if n_gen >= 2:
            bias_21 = KNOB_STEP_FACTOR_21 * eps_3d * j_cp
            matter[1] += matter[2] * (1.0 + bias_21)
            anti[1] += anti[2] * (1.0 - bias_21)
            matter[2], anti[2] = 0.0, 0.0

        annihilated_pairs = min(matter[1], anti[1])
        em_photons = KNOB_PHOTONS_PER_PAIR * annihilated_pairs
        surviving_matter = matter[1] - annihilated_pairs
        surviving_anti = anti[1] - annihilated_pairs
        eta_raw = surviving_matter / em_photons if em_photons > 0 else 0.0
        eta_baryon = eta_raw * KNOB_WASHOUT_KAPPA / KNOB_PHOTON_DILUTION
        return {
            "n_gen": n_gen,
            "j_cp": j_cp,
            "eps_3d": eps_3d,
            "initial_total": int(total_initial),
            "em_photons": round(em_photons, 1),
            "surviving_matter": surviving_matter,
            "surviving_anti": surviving_anti,
            "baryon_to_photon": eta_baryon,
        }

    def generation_node_loads(self, node_cap: float = KNOB_NODE_CAP) -> List[Dict[str, Any]]:
        """Display only: the tick loads and cap are KNOBS, so 'Gen 4 blocked' is true by construction."""
        rows: List[Dict[str, Any]] = []
        for label, (geom, ticks) in KNOB_GEN_TICKS.items():
            allowed = ticks <= node_cap
            rows.append({"generation": label, "geometry": geom, "ticks": ticks, "allowed": allowed,
                         "status": "Allowed (< cap, knob)" if allowed else "Over cap (knob)"})
        return rows


def run_baryogenesis_demo() -> None:
    sim = BCCBaryogenesisSim()
    v = ckm_standard()
    j = jarlskog(v)

    print("=== PART 0: KNOBS (hand-set, not derived) ===")
    for k, val in KNOBS.items():
        print(f"  {k:<24} = {val}")

    print("\n=== PART 1: CKM Jarlskog invariant from PDG 2024 angles (Eq. 12.28) ===")
    print(f"  sin th12={PDG2024_S12}, sin th13={PDG2024_S13}, sin th23={PDG2024_S23}, delta={PDG2024_DELTA} rad")
    print(f"  unitarity defect max|VV^dag - 1| = {unitarity_defect(v):.2e}")
    print(f"  J = Im(V_us V_cb V_ub* V_cs*)    = {j:.4e}   (PDG 2024 fit: 3.12 +0.13 -0.12 e-5)")
    print(f"  J_max = 1/(6 sqrt 3)             = {J_MAX:.4e}   J/J_max = {j / J_MAX:.2e}")
    assert 0.0 < j <= J_MAX
    rng = random.Random(7)
    rp = rephase(v, [rng.uniform(0, 6.3) for _ in range(3)], [rng.uniform(0, 6.3) for _ in range(3)])
    print(f"  J after random quark rephasing   = {jarlskog(rp):.4e}   (rephasing invariant)")

    print("\n=== PART 2: Why CP violation needs >= 3 generations (computed, not assumed) ===")
    print("  N_gen   physical CP phases (N-1)(N-2)/2")
    for n in (1, 2, 3, 4):
        print(f"  {n:>5}   {physical_cp_phases(n)}")
    chk = two_generation_check()
    print(f"  N=2, {chk['trials']} random U(2): max |Im(U11 U22 U12* U21*)| = {chk['max_abs_quartet']:.1e}; "
          f"max |Im| after rephasing = {chk['max_imag_after_rephasing']:.1e}")
    mu, md = QUARK_MASSES_GEV["up"], QUARK_MASSES_GEV["down"]
    dj = jarlskog_determinant(v, mu, md)
    print(f"  N=3 Jarlskog det[HuHd]: |Im det| = {abs(dj.imag):.4e} vs 2 J F_u F_d = "
          f"{2 * abs(j) * mass_factor(mu) * mass_factor(md):.4e}")
    md_deg = (md[1], md[1], md[2])
    print(f"  N=3 with m_d = m_s (degenerate):  |det| = {abs(jarlskog_determinant(v, mu, md_deg)):.1e}  -> CP removable")

    print("\n=== PART 3: epsilon as an OUTPUT (target eta = 6.1e-10, Planck 2018) ===")
    eps = required_epsilon(ETA_TARGET, j)
    print(f"  closed form: eta = 2b/(3 - 2b + b^2/2), b = eps*J  ~  (2/3) eps J")
    print(f"  required eps per decay           = {eps:.4e}   (~ 1.5 eta / J = {1.5 * ETA_TARGET / j:.4e})")
    print("  N_gen  J_cp           Surviving Matter   eta (cascade)   (2/3) eps J")
    for n in (1, 2, 3):
        r = sim.simulate_universe(n, eps_3d=eps)
        print(f"  {n:>5}  {r['j_cp']:>12.4e}  {r['surviving_matter']:>16.4e}  {r['baryon_to_photon']:>13.4e}"
              f"   {2 / 3 * eps * r['j_cp']:.4e}")
    print("  Open question: can the lattice produce eps ~ 3e-5 per decay without a knob?")

    print("\n=== PART 4: Generation tick loads (ALL KNOBS) + LEP data ===")
    print("Generation             3D Routing Geometry     Tick Load   Status")
    print("-" * 78)
    for row in sim.generation_node_loads():
        print(f"{row['generation']:<22} {row['geometry']:<23} {row['ticks']:>9.1f}   {row['status']}")
    print(f"  Data (not a lattice test): LEP Z width gives N_nu = {LEP_N_NU} +- {LEP_N_NU_ERR} light neutrinos.")


if __name__ == "__main__":
    run_baryogenesis_demo()
