#!/usr/bin/env python3
"""Small stdlib checks, no fitting, sweeps, or evolution."""
import itertools
import unittest
from baryon_calculator import (Parameters, CHANNELS, PAIR_SUMS, MEASURED_MEV,
                               calculate, demo)


class CalculatorTests(unittest.TestCase):
    def test_calibration(self):
        nmean = (MEASURED_MEV['p'] + MEASURED_MEV['n']) / 2
        for channel, target in [('p', nmean), ('n', nmean), ('Delta+', 1232.),
                                ('Lambda', MEASURED_MEV['Lambda'])]:
            self.assertAlmostEqual(calculate(channel)['mass_MeV'], target, places=9)

    def test_from_anchors(self):
        derived = Parameters.from_anchors()
        default = Parameters()
        self.assertAlmostEqual(derived.m_light, default.m_light, places=12)
        self.assertAlmostEqual(derived.m_strange, default.m_strange, places=12)
        self.assertAlmostEqual(derived.A, default.A, places=12)

        custom = Parameters.from_anchors(N_MeV=940.0, Delta_MeV=1230.0, Lambda_MeV=1116.0)
        self.assertAlmostEqual(calculate('p', parameters=custom)['mass_MeV'], 940.0, places=9)
        self.assertAlmostEqual(calculate('Delta+', parameters=custom)['mass_MeV'], 1230.0, places=9)
        self.assertAlmostEqual(calculate('Lambda', parameters=custom)['mass_MeV'], 1116.0, places=9)

        with self.assertRaises(ValueError):
            Parameters.from_anchors(N_MeV=1232.0, Delta_MeV=938.0, Lambda_MeV=1115.0)
        with self.assertRaises(ValueError):
            Parameters.from_anchors(N_MeV=True)

    def test_expected_outputs(self):
        self.assertAlmostEqual(calculate('Omega-')['mass_MeV'], 1681.887777988625, places=9)
        self.assertAlmostEqual(calculate('Sigma0')['mass_MeV'], 1179.809526410066, places=9)
        self.assertAlmostEqual(calculate('p')['spin_shift_MeV'], -146.540622835, places=9)

    def test_quantum_pair_sum(self):
        for name, state in CHANNELS.items():
            expected = (state.J * (state.J + 1) - 3 * .75) / 2
            self.assertAlmostEqual(sum(PAIR_SUMS[state.family]), expected)
            self.assertEqual(sum(v['count'] for v in calculate(name)['pairs'].values()), 3)
            for pair in calculate(name)['pairs'].values():
                if pair['count'] == 0:
                    self.assertEqual(pair['spin_expectation_sum'], 0)

    def test_explicit_lambda_sigma_pair_states(self):
        self.assertEqual(PAIR_SUMS['Lambda'], (-.75, 0., 0.))
        self.assertEqual(PAIR_SUMS['Sigma'], (.25, -1., 0.))
        self.assertNotEqual(calculate('Lambda')['mass_MeV'], calculate('Sigma0')['mass_MeV'])

    def test_permutations(self):
        for name, state in CHANNELS.items():
            expected = calculate(name)
            for perm in set(itertools.permutations(state.quarks)):
                self.assertEqual(calculate(name, ''.join(perm)), expected)
        self.assertEqual(calculate('p', ' UDU '), calculate('p'))

    def test_channel_validation(self):
        for kwargs in [{'quark_combo': 'sss'}, {'quark_combo': 'udx'}, {'quark_combo': 'uu'},
                       {'quark_combo': 3}, {'J': 1.5}, {'I': 1.5}, {'I': True}]:
            with self.assertRaises(ValueError):
                calculate('p', **kwargs)
        with self.assertRaises(ValueError):
            calculate('Lambda', 'uds', I=1.)
        for bad in ['proton-flipped', 'sss-low-spin', None]:
            with self.assertRaises(ValueError):
                calculate(bad)

    def test_catalogue_and_pauli_allowed_identical_flavours(self):
        self.assertEqual(len(CHANNELS), 18)
        self.assertEqual(sum(s.J == .5 for s in CHANNELS.values()), 8)
        self.assertEqual(sum(s.J == 1.5 for s in CHANNELS.values()), 10)
        for name, state in CHANNELS.items():
            if len(set(state.quarks)) == 1:
                self.assertEqual(state.J, 1.5)
                with self.assertRaises(ValueError):
                    calculate(name, J=.5)

    def test_one_rule_all_channels(self):
        p = Parameters()
        for name, state in CHANNELS.items():
            q = state.quarks
            nl, ns = 3 - q.count('s'), q.count('s')
            base = nl * p.m_light + ns * p.m_strange
            energies = []
            for c, mi, mj in zip(PAIR_SUMS[state.family],
                                 (p.m_light, p.m_light, p.m_strange),
                                 (p.m_light, p.m_strange, p.m_strange)):
                energies.append(p.A * p.m_light * p.m_light / (mi * mj) * c)
            self.assertAlmostEqual(calculate(name)['mass_MeV'], base + sum(energies), places=9)

    def test_zero_spin_coupling(self):
        p = Parameters(A=0.)
        for name in CHANNELS:
            x = calculate(name, parameters=p)
            self.assertEqual(x['mass_MeV'], x['baseline_MeV'])
            self.assertEqual(x['spin_shift_MeV'], 0.)

    def test_delta_proxy_not_charge_measurement(self):
        for name in ('Delta++', 'Delta+', 'Delta0', 'Delta-'):
            x = calculate(name)
            self.assertIsNone(x['measured_mass_MeV'])
            self.assertEqual(x['comparison_MeV'], 1232.)
            self.assertIn('mixed-charge', x['comparison_kind'])

    def test_parameter_validation(self):
        for kwargs in [{'m_light': 0}, {'m_strange': -1}, {'A': -1},
                       {'A': float('nan')}, {'m_light': float('inf')}, {'A': True}]:
            with self.assertRaises(ValueError):
                Parameters(**kwargs)


if __name__ == '__main__':
    try:
        import resource
    except ImportError:
        resource = None

    if resource is not None:
        resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
        if hasattr(resource, 'RLIMIT_AS'):
            resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(CalculatorTests))
    if result.wasSuccessful():
        print()
        demo(['p', 'Delta+', 'Lambda', 'Sigma0', 'Xi0', 'Omega-'])
        if resource is not None:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            print(f'CPU seconds: {usage.ru_utime + usage.ru_stime:.4f}; peak RSS KiB: {usage.ru_maxrss}')
    raise SystemExit(0 if result.wasSuccessful() else 1)
