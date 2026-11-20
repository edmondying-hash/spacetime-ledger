#!/usr/bin/env python3
"""Shared configuration for the BCC 8-link toy bundle.

ONE place for: fixed physical constants (never knobs), the hop-length switch
(OD1, open for Edmond), quantities derived from it, and DECLARED_KNOBS (every
hand-chosen model value used anywhere in the toys).

Lattice convention used throughout the code: BCC sites are integer points with
all-even or all-odd coordinates; the 8 links are (+-1, +-1, +-1). One link
therefore has length sqrt(3) in *coordinate units*, and the Voronoi cell
(truncated octahedron) has volume 4 coordinate units^3.
"""

import math
import os

# ---------------------------------------------------------------------------
# Fixed physical constants (CODATA 2018 exact / recommended). NEVER knobs.
# ---------------------------------------------------------------------------
C_LIGHT = 299_792_458.0            # m/s (exact)
G_NEWTON = 6.67430e-11             # m^3 kg^-1 s^-2
HBAR = 1.054571817e-34             # J s
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT**3)   # ~1.616e-35 m
T_PLANCK = L_PLANCK / C_LIGHT                         # ~5.391e-44 s
V_PLANCK = L_PLANCK**3

# ---------------------------------------------------------------------------
# OD1 -- hop-length convention (OPEN DECISION for Edmond).
#   'sqrt3_lP' : one BCC link = sqrt(3) l_P  (README's main wording). Then the
#                coordinate unit is l_P and the Voronoi cell is 4 V_P.
#   'lP'       : one BCC link = l_P. Then the coordinate unit is l_P/sqrt(3)
#                and the Voronoi cell is 4/3^1.5 = 0.7698 V_P (the "~0.770 V_P"
#                quoted in the READMEs only holds under this option).
# In BOTH options c is fixed: one hop per tick means the tick lasts
# hop_length / c, so the tick is derived, not chosen. Under 'sqrt3_lP' the tick
# is sqrt(3) t_P, not t_P (otherwise the hop speed would be sqrt(3) c).
# ---------------------------------------------------------------------------
HOP = os.environ.get("BCC_HOP", "sqrt3_lP")   # default = README main statement; flagged OD1 (env BCC_HOP overrides)

def hop_derived(hop: str = None) -> dict:
    hop = hop or HOP
    if hop == "sqrt3_lP":
        hop_len_lP = math.sqrt(3.0)
    elif hop == "lP":
        hop_len_lP = 1.0
    else:
        raise ValueError("HOP must be 'lP' or 'sqrt3_lP'")
    coord_unit_lP = hop_len_lP / math.sqrt(3.0)        # length of 1 coordinate unit
    return {
        "HOP": hop,
        "hop_length_lP": hop_len_lP,
        "hop_length_m": hop_len_lP * L_PLANCK,
        "coord_unit_lP": coord_unit_lP,
        "cell_volume_VP": 4.0 * coord_unit_lP**3,       # truncated octahedron
        "tick_tP": hop_len_lP,                          # tick = hop_length / c
        "tick_s": hop_len_lP * T_PLANCK,
        "hop_speed_over_c": 1.0,                        # by construction (c fixed)
        "coords_per_tick_at_c": math.sqrt(3.0),         # one hop = sqrt(3) coords
    }

DERIVED = hop_derived()

# ---------------------------------------------------------------------------
# DECLARED_KNOBS: every hand-chosen model value in the bundle (besides the
# paper's declared phi0 = 1.4 and load factor 1/2). Listed, not fitted here.
# "tuned" = value appears chosen to land on a known number (behaves as a fit).
# ---------------------------------------------------------------------------
DECLARED_KNOBS = {
    # paper-level declared knobs
    "phi0": (1.4, "paper declared knob (not used by these toys)"),
    "load_factor": (0.5, "paper declared knob (not used by these toys)"),
    # bcc/bcc_unified_engine.py
    "link_weight_mev": (198.0, "baryon MeV per Steiner link (tuned)"),
    "baryon_bare_ticks": ("12 + 91*n_s", "baryon bare term (tuned)"),
    "baryon_spin_factors": ("N -1, Delta 1, Lambda -1, Sigma -0.5, Xi -0.66, Sigma* 0.8, Xi* 0.56, Omega 0.34", "tuned"),
    "baryon_spin_scale": ("6.5 - 1.4*n_s", "tuned"),
    "redraw_probs": ("u,d 0.72; s 0.40; c 0.18; b 0.08", "hop probability per cycle by flavour"),
    "max_node_ticks": (100.0, "node capacity per cycle"),
    "glueball_formula": ("165 + 362.5*L MeV", "inserted formula (tuned)"),
    "lensing_queue": ("util = load*M*0.24/r, delay = u/(1-u)*0.18", "inserted 1/r"),
    "huygens_dt": (0.55, "wave time step; sets wave speed dt/sqrt(2) coord/tick"),
    "huygens_util_cap": (0.65, "max congestion in c_eff"),
    "huygens_arrival_threshold": (0.15, "|u|*r arrival trigger"),
    "huygens_load_strength": ("GridMass/938*6.5", "inserted 1/r load scale"),
    # bcc/bcc_meson_sim.py
    "TICK_TO_MEV": (5.0, "meson tick->MeV (tuned)"),
    "QUARK_BARE_TICKS": ("l 15.5, s 24.25, c 77.5, b 236.5", "tuned"),
    "meson_route_rule": ("3*bare + min(b_avg-2mu, 3.5*b_min); heavy saturation at c", "tuned"),
    "meson_hyperfine": ("32 * (-3|+1) * b_l^2/(b1 b2)", "tuned"),
    "TICKS_PER_LP": (9.0, "flux-tube ticks per l_P of tube length"),
    "string_break_mev": (275.0, "string-breaking threshold"),
    # bcc/bcc_dirac4_spinor.py
    "dirac_mass_coin_theta": (0.25, "rest-mass coin angle per tick"),
    # gr/
    "node_cap": (100.0, "congestion cap C"),
    "r_s_lattice": (3.0, "Schwarzschild radius in coord units"),
    "W_to_g00_map": ("dtau/dt = sqrt(1 - W/C)", "inserted mapping (OD2)"),
    "kugelblitz_ring": ("radius 12, overlap width 0.85, aim offsets", "inserted"),
    # serverside/
    "orbital_coupling": ("k from core mass", "c_eff = 1/(1+k/r) inserted"),
    "vacuum_noise_prob": ("0..0.06", "server decoherence rate"),
    # cosmo/
    "halo_profile": ("M_dark ~ r - r_c atan(r/r_c), r_c = 3", "inserted (gives flat curve)"),
    "baryon_profile": ("1200*(1 - exp(-r/1.8))", "inserted"),
    "Omega_m0, Omega_L0": ((0.315, 0.685), "Planck-2018 inputs"),
    "void_expand_thresh": (20.0, "idle gate threshold"),
    "h_vac_rate": (0.01, "void growth per tick"),
    "T_recomb, z_recomb": ((2994.775, 1098.0), "inputs (chosen so T0 = 2.725 K)"),
    "cmb_r_s_mpc, d_A_mpc": ((144.43, 13872.0), "inputs"),
    "cmb_phase_shift": (0.2709, "inserted factor that sets l_1 = 220 (tuned)"),
}

if __name__ == "__main__":
    for h in ("sqrt3_lP", "lP"):
        print(hop_derived(h))
    print(f"{len(DECLARED_KNOBS)} declared knobs")
