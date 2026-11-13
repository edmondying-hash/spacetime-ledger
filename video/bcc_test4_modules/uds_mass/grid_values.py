#!/usr/bin/env python3
"""Run bcc_unified_sim.py Part 1 unchanged (same call order as run_all) and save the
unrounded baryon tick values the uds video uses."""
import json, os, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../bcc_test4")))  # path edit: was /workspace/bcc_test4_videos/v3/bcc_test4
import bcc_unified_sim as us, baryon_calculator as bc
g = us.BCCUnifiedGrid()
specs = {
    'N': (('l', 'l', 'l'), (-0.75, 0.00, 0.00)), 'Delta': (('l', 'l', 'l'), (+0.25, +0.25, +0.25)),
    'Lambda': (('l', 'l', 's'), (-0.75, 0.00, 0.00)), 'Sigma': (('l', 'l', 's'), (+0.25, -0.50, -0.50)),
    'Xi': (('s', 's', 'l'), (+0.25, -0.50, -0.50)), 'SigmaStar': (('l', 'l', 's'), (+0.25, +0.25, +0.25)),
    'XiStar': (('s', 's', 'l'), (+0.25, +0.25, +0.25)), 'Omega': (('s', 's', 's'), (+0.25, +0.25, +0.25)),
}  # identical to run_all() channel_specs
out = {k: g.run_baryon_subroutine(*v) for k, v in specs.items()}
out['_inputs'] = {'ticks_bare_l': g.bare_ticks['l'], 'ticks_bare_s': g.bare_ticks['s'],
                  'mev_per_tick_in_code': g.mev_per_tick}
out['_pdg'] = {'p': bc.MEASURED_MEV['p'], 'Lambda': bc.MEASURED_MEV['Lambda'], 'Omega-': bc.MEASURED_MEV['Omega-'],
               'calc_model_p': bc.calculate('p')['mass_MeV'], 'calc_model_Omega-': bc.calculate('Omega-')['mass_MeV']}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "grid_values.json"), "w"), indent=2)  # path edit: this script's folder; was /workspace/bcc_test4_videos/uds_mass/grid_values.json
for k in ('N', 'Lambda', 'Omega'):
    print(k, {a: round(b, 4) for a, b in out[k].items()})
print(out['_inputs'], out['_pdg'])
