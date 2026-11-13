#!/usr/bin/env python3
"""Effective baryon mass calculator: one pair-spin rule, not BCC dynamics.

Natural units c=hbar=1: effective constituent energies and A are in MeV.
s=sigma/2 is dimensionless. C_ab sums <s_i.s_j> over unordered pairs.
Only the idealized light/strange L=0 octet and decuplet are catalogued.
"""
import argparse
from dataclasses import dataclass
import json
import math

SOURCE = 'https://pdg.lbl.gov/2024/tables/rpp2024-sum-baryons.pdf'
PROVENANCE = ('Defaults calibrated analytically from the PDG 2024 p/n arithmetic '
              'mean, mixed-charge Delta Breit-Wigner proxy 1232 MeV, and Lambda. '
              'Not bare-quark masses, isolated gluon energies, or derived lattice parameters.')

DEFAULT_N_MEV = (938.27208816 + 939.5654205) / 2
DEFAULT_DELTA_MEV = 1232.0
DEFAULT_LAMBDA_MEV = 1115.683


@dataclass(frozen=True)
class Parameters:
    m_light: float = 361.8197923883333
    m_strange: float = 538.5840380583334
    A: float = 195.38749711333335

    def __post_init__(self):
        for name in ('m_light', 'm_strange', 'A'):
            x = getattr(self, name)
            if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
                raise ValueError(f'{name} must be a finite number')
        if self.m_light <= 0 or self.m_strange <= 0 or self.A < 0:
            raise ValueError('Effective energies must be positive and A nonnegative')

    @classmethod
    def from_anchors(
        cls,
        N_MeV: float = DEFAULT_N_MEV,
        Delta_MeV: float = DEFAULT_DELTA_MEV,
        Lambda_MeV: float = DEFAULT_LAMBDA_MEV,
    ) -> 'Parameters':
        """Derive effective constituent masses and hyperfine coupling from N, Delta, and Lambda."""
        for name, val in (('N_MeV', N_MeV), ('Delta_MeV', Delta_MeV), ('Lambda_MeV', Lambda_MeV)):
            if isinstance(val, bool) or not isinstance(val, (int, float)) or not math.isfinite(val):
                raise ValueError(f'{name} must be a finite number')
        if Delta_MeV < N_MeV:
            raise ValueError('Delta_MeV must be greater than or equal to N_MeV so A >= 0')
        m_light = (N_MeV + Delta_MeV) / 6.0
        A = 2.0 * (Delta_MeV - N_MeV) / 3.0
        m_strange = m_light + Lambda_MeV - N_MeV
        return cls(m_light=m_light, m_strange=m_strange, A=A)


# Sums of pair expectations, NOT classical spin signs or individual phase flips.
# Columns: light-light, light-strange, strange-strange.
PAIR_SUMS = {
    'N': (-.75, 0., 0.),
    'Lambda': (-.75, 0., 0.),
    'Sigma': (.25, -1., 0.),
    'Xi': (0., -1., .25),
    'Delta': (.75, 0., 0.),
    'SigmaStar': (.25, .5, 0.),
    'XiStar': (0., .5, .25),
    'Omega': (0., 0., .75),
}


@dataclass(frozen=True)
class Channel:
    quarks: str
    family: str
    J: float
    I: float


# Explicit spin/isospin channels avoid inventing low-spin uuu, ddd or sss.
CHANNELS = {
    'p': Channel('uud', 'N', .5, .5),
    'n': Channel('udd', 'N', .5, .5),
    'Lambda': Channel('uds', 'Lambda', .5, 0.),
    'Sigma+': Channel('uus', 'Sigma', .5, 1.),
    'Sigma0': Channel('uds', 'Sigma', .5, 1.),
    'Sigma-': Channel('dds', 'Sigma', .5, 1.),
    'Xi0': Channel('uss', 'Xi', .5, .5),
    'Xi-': Channel('dss', 'Xi', .5, .5),
    'Delta++': Channel('uuu', 'Delta', 1.5, 1.5),
    'Delta+': Channel('uud', 'Delta', 1.5, 1.5),
    'Delta0': Channel('udd', 'Delta', 1.5, 1.5),
    'Delta-': Channel('ddd', 'Delta', 1.5, 1.5),
    'SigmaStar+': Channel('uus', 'SigmaStar', 1.5, 1.),
    'SigmaStar0': Channel('uds', 'SigmaStar', 1.5, 1.),
    'SigmaStar-': Channel('dds', 'SigmaStar', 1.5, 1.),
    'XiStar0': Channel('uss', 'XiStar', 1.5, .5),
    'XiStar-': Channel('dss', 'XiStar', 1.5, .5),
    'Omega-': Channel('sss', 'Omega', 1.5, 0.),
}

# Values from the existing archived PDG 2024 transcription. Delta is separate:
# there is no charge-specific Delta mass entry here.
MEASURED_MEV = {
    'p': 938.27208816, 'n': 939.5654205, 'Lambda': 1115.683,
    'Sigma+': 1189.37, 'Sigma0': 1192.642, 'Sigma-': 1197.449,
    'Xi0': 1314.86, 'Xi-': 1321.71,
    'SigmaStar+': 1382.83, 'SigmaStar0': 1383.7, 'SigmaStar-': 1387.2,
    'XiStar0': 1531.80, 'XiStar-': 1535.0, 'Omega-': 1672.45,
}
DELTA_BW_PROXY_MEV = 1232.0


def normalize_quarks(value):
    if not isinstance(value, str):
        raise ValueError('quark_combo must be a string')
    value = value.strip().lower()
    if len(value) != 3 or any(q not in 'uds' for q in value):
        raise ValueError('Supply exactly three flavours from u, d, s')
    return value


def calculate(channel, quark_combo=None, *, J=None, I=None, parameters=None):
    """Calculate an explicit catalogued channel; optional labels cross-check it.

    Quark order never changes the result. The channel specifies the quantum
    pair state (e.g. Lambda vs Sigma0); J alone cannot specify that state.
    Return unrounded numbers: display formatting is not quantization.
    """
    if not isinstance(channel, str) or channel not in CHANNELS:
        raise ValueError('Unknown channel; choose one of: ' + ', '.join(CHANNELS))
    state = CHANNELS[channel]
    q = normalize_quarks(state.quarks if quark_combo is None else quark_combo)
    if sorted(q) != sorted(state.quarks):
        raise ValueError('Flavours do not match the selected channel')
    for label, supplied, expected in (('J', J, state.J), ('I', I, state.I)):
        if supplied is not None and (isinstance(supplied, bool) or supplied != expected):
            raise ValueError(f'{label} must be {expected} for {channel}')
    p = Parameters() if parameters is None else parameters
    if not isinstance(p, Parameters):
        raise ValueError('parameters must be a Parameters instance')
    ns = q.count('s')
    nl = 3 - ns
    counts = (nl * (nl - 1) // 2, nl * ns, ns * (ns - 1) // 2)
    sums = PAIR_SUMS[state.family]
    r = p.m_light / p.m_strange
    couplings = (p.A, p.A * r, p.A * r * r)
    base = nl * p.m_light + ns * p.m_strange
    shift = sum(a * c for a, c in zip(couplings, sums))
    pairs = {kind: {'count': n, 'spin_expectation_sum': c,
                    'coupling_MeV': a, 'energy_MeV': a * c}
             for kind, n, c, a in zip(('ll', 'ls', 'ss'), counts, sums, couplings)}
    is_delta = state.family == 'Delta'
    target = DELTA_BW_PROXY_MEV if is_delta else MEASURED_MEV[channel]
    role = ('calibration: shared mixed-charge proxy' if is_delta else
            'calibration: p/n mean, not individual splitting' if state.family == 'N' else
            'calibration' if state.family == 'Lambda' else
            'out-of-calibration comparison (not blind validation)')
    return {'channel': channel, 'quarks': state.quarks, 'J': state.J, 'I': state.I,
            'baseline_MeV': base, 'spin_shift_MeV': shift, 'mass_MeV': base + shift,
            'pairs': pairs, 'measured_mass_MeV': None if is_delta else target,
            'comparison_MeV': target,
            'comparison_kind': 'shared mixed-charge Delta BW proxy' if is_delta else
                               'archived PDG 2024 tabulated mass',
            'difference_MeV': base + shift - target, 'comparison_role': role,
            'source_url': SOURCE}


def demo(channels):
    print('Effective pair-spin mass calculator; not a BCC or time-evolution simulation.')
    print('Default calibration: p/n mean + Delta mixed-charge BW proxy + Lambda.')
    print(f'{"Channel":12} {"Baseline":>10} {"Spin":>10} {"Model":>10} {"Compare":>10}  Status')
    for name in channels:
        x = calculate(name)
        label = x['comparison_role']
        print(f'{name:12} {x["baseline_MeV"]:10.2f} {x["spin_shift_MeV"]:10.2f} '
              f'{x["mass_MeV"]:10.2f} {x["comparison_MeV"]:10.2f}  {label}')
    print('All energies in MeV. Delta comparisons are NOT charge-specific measurements.')
    print('Source:', SOURCE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('channels', nargs='*', help='Channel IDs; quote names containing + or - if needed')
    parser.add_argument('--all', action='store_true', help='Show all 18 catalogued charge states')
    parser.add_argument('--json', action='store_true', help='Unrounded structured results')
    args = parser.parse_args()
    names = list(CHANNELS) if args.all else (args.channels or ['p', 'Delta+', 'Lambda', 'Sigma0', 'Xi0', 'Omega-'])
    try:
        if args.json:
            print(json.dumps([calculate(name) for name in names], indent=2, allow_nan=False))
        else:
            demo(names)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
