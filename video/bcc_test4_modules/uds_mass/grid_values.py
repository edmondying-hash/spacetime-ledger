#!/usr/bin/env python3
"""Run the v4 (6-face) bcc_unified_sim.py Part 1 unchanged - same calls as run_unified_demo() -
and save the baryon tick values the uds video uses (new API: BCCUnifiedGridSim)."""
import json, sys
sys.path.insert(0, "/workspace/bcc_test4_videos/v4/bcc_test4")
import bcc_unified_sim as us, baryon_calculator as bc
sim = us.BCCUnifiedGridSim(size=8)
out = {fam: sim.simulate_baryon_family(flv, sp, cycles=3000, seed=42 + i)
       for i, (fam, flv, sp) in enumerate(us.BARYON_FAMILIES)}
out['_pdg'] = {'p': bc.MEASURED_MEV['p'], 'Lambda': bc.MEASURED_MEV['Lambda'], 'Omega-': bc.MEASURED_MEV['Omega-']}
out['_note'] = ("v4 unified sim returns ticks only (no mev_per_tick); its glueball printout labels ticks as MeV 1:1. "
                "bare = 12 + 91*n_s, spin = factor*(6.5 - 1.4*n_s), Load% = 98 - 11*n_s are formulas; "
                "RouteT = 95 * average 6-face Steiner links is the simulated part.")
json.dump(out, open("/workspace/bcc_test4_videos/v2_sound/uds_mass/grid_values.json", "w"), indent=2)
for k in ('N', 'Lambda', 'Omega'): print(k, out[k])
