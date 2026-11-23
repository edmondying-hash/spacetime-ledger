#!/usr/bin/env python3
"""Bookkeeping only: assemble result.json from out/S*/ and logs/. No physics computed here.
Written during the run (after S2), applying the rules frozen in expected.json and DESIGN_vs_PREREG.md."""
import os, json, hashlib, math, glob, datetime
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda p: json.load(open(os.path.join(R, p)))
sha = lambda p: hashlib.sha256(open(os.path.join(R, p), 'rb').read()).hexdigest()
def s6(x): return None if x is None else float(f'{x:.6g}')
def w5(m, p): return abs(m - p)/abs(p) <= 0.05
def rounds(m, p, fmt): return (fmt % m) == (fmt % p)
EX = J('expected.json'); S0 = J('out/S0/S0.json'); S1 = J('out/S1/S1.json'); S2 = J('out/S2/S2.json')
S3 = J('out/S3/S3.json'); S4 = J('out/S4/S4.json'); S5 = J('out/S5/S5.json'); GE = J('out/G0END/G0END.json')
DF = J('out/S1/dw_final.json')
res = {}
for f in sorted(glob.glob(os.path.join(R, 'logs', 'resources_*.json'))):
    d = json.load(open(f)); st = d['step']
    od = os.path.join(R, 'out', st); size = sum(os.path.getsize(os.path.join(a, b)) for a, _, bs in os.walk(od) for b in bs) if os.path.isdir(od) else 0
    res[st] = dict(cpu_s=d['cpu_s'], wall_s=d['wall_s'], peak_tree_rss_GiB=d['peak_tree_rss_GiB'], max_procs=d['max_procs_in_tree'],
                   exit_code=d['exit_code'], output_bytes=size, start=datetime.datetime.fromtimestamp(d['start_epoch']).astimezone().isoformat())
r = {'run': '20261112_l12_7e09b7c4', 'path_bigbang': R,
     'authority': {'design_approval': 'Edmond, 2026-11-12 4:56 PM ET, "Approve 7e09b7c4"',
                   'go': 'Edmond, 2026-11-12 6:41 PM ET, "yes, start" (S0-S5, bigbang)',
                   'decisions': 'D1 load-free; D2 revised (4:51 PM ET); D3 accept; D4 pre-reg governs'},
     'design_sha256_as_frozen': sha('design/L1_2_RUN_DESIGN.md'), 'prereg_sha256': sha('inputs/PREREGISTRATION.md'),
     'decisions_sha256': sha('inputs/L1_2_DECISIONS.txt'),
     'paper': {'commit': EX['paper']['commit'], 'sha256': sha('inputs/space-ledger-v2.md')},
     'expected_json_sha256': sha('expected.json'), 'DESIGN_vs_PREREG_sha256': sha('DESIGN_vs_PREREG.md'),
     'DESIGN_vs_PREREG_md': open(os.path.join(R, 'DESIGN_vs_PREREG.md')).read(),
     'code_version': {'hashes_start_P0': {k: v['actual'] for k, v in S0['P0'].items()}, 'hashes_end_G0END_all_ok': GE['all_ok'],
                      'git': 'frozen qca sources are not in a git repo (copied byte-identical from box /workspace/qca); paper from git commit above',
                      'harness_sha256': {p: sha(p) for p in ('harness/l12.py', 'harness/meter.py', 'run_step.sh')},
                      'python': S0['python'], 'numpy': S0['numpy'], 'scipy': S0['scipy'], 'platform': S0['platform'], 'host': S0['hostname'],
                      'path_redirect': S0['redirects']},
     'seeds': {'preflight_P1_P2_and_timing_and_Ns1_check': 'numpy default_rng(20261112)', 'E2_R4a': 'dw_gscan.py: fresh default_rng(1) per (b,Ns), 60 starts',
               'bulk_ring': 'dw_ring.py: default_rng(2), 40 starts', 'dw_final.py': 'deterministic', 'R4b': 'deterministic grid', 'E1_R5': 'deterministic'},
     'grid': {'R4b': S3['grid'], 'X1': 'periodic 40^3 cubic grid (dw_real.py)'}, 'boundary_condition': 'periodic, one BCC orbit (k 2pi-periodic, reciprocal vectors pi*g, g even-sum)',
     'units': 'omega in E_P per tick (arg(lambda)/4 of the four-layer cycle); speeds in units of the hop rate',
     'load_rule': 'none, section 6.2 vacuum symbol, per D1 (X3 not run)',
     'caps': {'ceilings_soft': '96 GiB, 20 threads, 8 h total, 2 h/step, 1 GiB output', 'threads': 'BLAS/OMP pinned to 1 per process; up to 20 worker processes (S2: 7, S3/S4: 20)',
              'attempts': 'one per step', 'location': 'bigbang (Edmond ruling 6:41 PM ET)'},
     'resources_per_step': res,
     'cost_estimate_restated_before_S3': S0['timing_Ns16_grid_point'],
     'preflight': {k: S0[k] for k in ('P0_pass', 'P1_pass', 'P2_pass', 'P3_pass', 'P4_pass', 'G0b_pass', 'G1_pass', 'P1', 'P2_maxdiff', 'P3_dist_gamma_pi_pi_0', 'P3_dist_gamma_pi2',
                   'P4_Ucycle_r0_edge_vs_Gamma', 'P4_chain_Ns4_b0.2_edge_vs_Gamma', 'G0b_chain', 'G0b_cycle', 'G1_residual_m0_0_Ns16')},
     'definitions_verbatim': {
        'source': 'qca/dw_final.py (sha256 48046ea5...6aa1) lines 18-23; qca/dw.py (769833f0...d651) contains neither definition (it defines Wmat, bd, layers, floq, spec only)',
        'abs_gamma5': 'p=abs(W[:,j].reshape(Ns,4))**2; ...  gamma5=float(p[:,:2].sum()-p[:,2:].sum())   [W from line 18: S=v[:,i]; Q,_=np.linalg.qr(S); pos=np.kron(np.arange(Ns),np.ones(4)); Mpos=Q.conj().T@(pos[:,None]*Q); e,U=np.linalg.eigh(Mpos); W=Q@U]; table cell = abs(walls[0].gamma5)',
        'localisation_length': 'p=abs(W[:,j].reshape(Ns,4))**2; ps=p.sum(1); side=0 if ps[:Ns//2].sum()>.5 else Ns-1\n        dist=abs(np.arange(Ns)-side); m=(dist<Ns//2)&(ps>1e-15)\n        xi=-1/np.polyfit(dist[m][:6],np.log(ps[m][:6]),1)[0]   -> loc_len_slices=float(xi); table cell = walls[0].loc_len_slices',
        'dw_final_lines_18_23_raw': open(os.path.join(R, 'frozen/qca/dw_final.py')).read().splitlines()[17:23]}}
# --- R1 residual
rows = dict((int(a), b) for a, b in DF['residual_mass_k0']['0.05']['rows'])
fmt = {'2': '%.1e', '4': '%.1e', '8': '%.1e', '12': '%.1e'}
R1 = {}
for N, p in EX['table_dw']['residual_mass_m0_0.05'].items():
    if N == '24':
        m = rows[24]; R1[N] = dict(measured=s6(m), log10=math.log10(m) if m > 0 else None, Ns22_floor_diagnostic=s6(rows[22]), paper=p, verdict='UNINFORMATIVE (pre-reg decision 1)',
                                  design_f24_record=S1['f24_record'], design_floor_rule_record=('pass' if abs(m) <= max(10*S1['f24_record'], 1e-14) else 'fail') + ' (record only; superseded by pre-reg)')
    else:
        m = rows[int(N)]; R1[N] = dict(measured=s6(m), paper=p, rel_dev=s6(abs(m-p)/p), within5=w5(m, p), rounds_to_printed=rounds(m, p, fmt[N]))
r['R1_residual_mass_m0_0.05'] = R1
r['R1_components'] = {N: 4*int(N) for N in R1}
fit05 = DF['residual_mass_k0']['0.05']['fit_log_decay_per_slice']; fit10 = DF['residual_mass_k0']['0.1']['fit_log_decay_per_slice']
r['R1_decay_rates_reference'] = {
  'm0_0.05': dict(dw_final_fit=s6(fit05), paper=-1.390, within5_paper=w5(fit05, -1.390), pred=s6(DF['residual_mass_k0']['0.05']['pred']), within5_pred=w5(fit05, DF['residual_mass_k0']['0.05']['pred']),
                  design_fit_Ns2_12=s6(S1['design_fit_Ns2_12_m0_0.05'])),
  'm0_0.1': dict(dw_final_fit=s6(fit10), paper=-0.698, within5_paper=w5(fit10, -0.698), pred=s6(DF['residual_mass_k0']['0.1']['pred']), within5_pred=w5(fit10, DF['residual_mass_k0']['0.1']['pred']),
                 design_fit_Ns2_12=s6(S1['design_fit_Ns2_12_m0_0.1'])),
  'note': 'reference only, not in the 5% PASS (pre-reg)'}
r['R1_m0_0_residuals'] = S1['residual_m0_0']; r['R1_two_ways_record'] = S1['residual_two_ways_m0_0.05']
r['all_residuals_m0_0.05_dw_final_rows'] = DF['residual_mass_k0']
# --- R2/R3
P = DF['profiles_m0_0_Ns16']; R2 = {}; R3 = {}
f2 = {'0.01': '%.4f', '0.05': '%.4f', '0.1': '%.4f', '0.15': '%.4f', '0.2': '%.3f'}
for k, p in EX['table_dw']['abs_gamma5_Ns16_m0_0'].items():
    ws = P[k]['walls']; m = abs(ws[0]['gamma5'])
    R2[k] = dict(measured=s6(m), measured_4dp=round(m, 4), paper=p, within5=w5(m, p), rounds_to_printed=rounds(m, p, f2[k]),
                 signs_ok=all((w['gamma5'] > 0) == (w['wall'] == 0) for w in ws), indep_lowsubspace_gamma5=s6(S1['indep_gamma5_123'][k]['indep_maxabs_eig']),
                 dir13_min=s6(S1['profiles_13dir_record'][k]['abs_gamma5_min']), dir13_max=s6(S1['profiles_13dir_record'][k]['abs_gamma5_max']),
                 dir13_all_within5=all(w5(abs(x['walls0_gamma5']), p) for x in S1['profiles_13dir_record'][k]['per_direction']))
for k, p in EX['table_dw']['loc_length_components_Ns16_m0_0'].items():
    m = P[k]['walls'][0]['loc_len_slices']
    R3[k] = dict(measured=s6(m), code_rounding_3dp=round(m, 3), paper=p, within5=w5(m, p), within5_after_code_rounding=w5(round(m, 3), p), rounds_to_printed=rounds(m, p, '%.2f'),
                 dir13_min=s6(S1['profiles_13dir_record'][k]['loc_min']), dir13_max=s6(S1['profiles_13dir_record'][k]['loc_max']),
                 dir13_all_within5=all(w5(x['walls0_loc'], p) for x in S1['profiles_13dir_record'][k]['per_direction']))
r['R2_abs_gamma5'] = R2; r['R3_loc_length'] = R3
r['R2_k0.3_record'] = dict(measured=s6(abs(P['0.3']['walls'][0]['gamma5'])), paper_approx=0.47, loc_len=s6(P['0.3']['walls'][0]['loc_len_slices']))
r['R2_sign_record'] = 'wall 0 (s=1) gamma5>0 right-handed; wall Ns-1 (s=Ns) gamma5<0 left-handed, checked on every k and all 4 resolved modes'
scored = [v['within5'] for v in R1.values() if 'within5' in v] + [v['within5'] for v in R2.values()] + [v['within5'] for v in R3.values()]
r['TABLE_DW_REPRODUCTION_prereg'] = dict(n_scored=len(scored), n_within5=sum(scored), PASS=all(scored), Ns24='UNINFORMATIVE, does not block')
r['design_R2_13dir_gate_record'] = dict(all_directions_within5=all(v['dir13_all_within5'] for v in R2.values()), signs_all_dirs=all(S1['profiles_13dir_record'][k]['all_signs_ok'] for k in R2))
# --- R4
R4 = {}
for b, p in EX['prose']['doubler_gap_Ns16'].items():
    bk = str(float(b)); e2 = S2['E2'][f'b{float(b):g}_Ns16']['gap']; pb = S3['per_b'][bk]; g = pb['R4b_gap']
    if g is None: cls = 'no R4b point found'
    elif abs(g-p)/p <= 0.05: cls = "within 5%: paper's value stands"
    elif g < p: cls = "R4b below paper by >5%: paper's value is NOT the minimum (finding, not a pass)"
    else: cls = "R4b above paper by >5%: R4a random search found a point the grid refinement did not"
    R4[b] = dict(paper=p, R4a_E2=s6(e2), R4a_argmin_rounded=S2['E2'][f'b{float(b):g}_Ns16']['argmin_rounded'], R4a_within5=w5(e2, p), R4a_rounds=rounds(e2, p, '%.3f'),
                 R4b=s6(g), R4b_argmin_wrapped=pb['R4b_argmin_wrapped'], R4b_dist_gamma=s6(pb['R4b_argmin_dist_gamma']), R4b_within5=(g is not None and w5(g, p)),
                 R4b_classification=cls, R4b_minus_R4a=s6(g-e2) if g is not None else None, grid_min_nonexcluded=s6(pb['grid_min_nonexcluded']),
                 n_local_minima=pb['n_local_minima'], n_refined=pb['n_refined'], n_kept=pb['n_kept'])
r['R4_doubler_gap_Ns16'] = R4
r['R4_bulk_gap_b0.2'] = dict(measured=s6(S2['bulk_ring_gap']), raw=S2['bulk_ring_raw'].strip(), paper=0.033, within5=w5(S2['bulk_ring_gap'], 0.033), method='dw_ring.py unchanged (ring=True, Ns=8, 40 starts rng(2)); RESULTS.md l.175 0.0331')
r['E2_full'] = S2['E2']
# --- boundary
r['BOUNDARY_prereg'] = S4['prereg_boundary']
r['R5_design'] = {b: dict(verdict=v['verdict'], slope_24_48=s6(v['slope_24_48']), gaps_24_32_48=[s6(x) for x in v['gaps_24_32_48']], R4_reference_gap=s6(v['R4_reference_gap']), survives=v['survives']) for b, v in S4['design_R5'].items()}
r['R5_design_pass'] = S4['design_R5_pass']
r['R5_note_b_ge_0.3'] = 'b=0.40 reference gap undefined in design and pre-reg (declared before data): verdict unresolved by rule'
r['E1_table'] = {k: dict(gap=s6(v['gap']), at=v['at'], end_weight=s6(v['end_weight'])) for k, v in S4['E1'].items()}
r['E1_equivalence_classes'] = S4['equivalence_classes_of_8_points']
r['R4b_vs_R5_crosscheck'] = S4['R4b_vs_R5_crosscheck']
r['face_centre_finding_report_only'] = S4['face_centre_finding']
# --- speeds
sc = S1['speed_compare_k0.0125']; ve = sc['v_end']; vb = sc['v_bulk']
a_ok = S1['periodS_equals_floq_Ns1_maxdiff'] < 1e-13 and len(S1['speed_end']['table']['0.0125']['per_direction']) == 13 and len(S1['speed_bulk_periodS']['table']['0.0125']['per_direction']) == 13
b_ok = w5(ve, 0.9855)
r['R6_speeds'] = dict(v_end=s6(ve), v_bulk=s6(vb), diff=s6(ve-vb), rel_diff=s6((ve-vb)/vb), species_independent_at_1em6=abs((ve-vb)/vb) <= 1e-6,
    paper_end=0.9855, end_within5=b_ok, end_rounds_to_09855=rounds(ve, 0.9855, '%.4f'), paper_bulk=0.989, bulk_within5=w5(vb, 0.989), bulk_minus_design_c0_098911=s6(vb-0.98911),
    v_bulk_floq_Ns1=s6(S1['speed_bulk_floq_Ns1']['table']['0.0125']['speed_mean']), periodS_vs_floqNs1_maxdiff=S1['periodS_equals_floq_Ns1_maxdiff'],
    end_table={k: dict(speed_mean=s6(v['speed_mean']), spread=s6(v['spread'])) for k, v in S1['speed_end']['table'].items()}, end_spread_slope=s6(S1['speed_end']['slope']),
    bulk_table={k: dict(speed_mean=s6(v['speed_mean']), spread=s6(v['spread'])) for k, v in S1['speed_bulk_periodS']['table'].items()}, bulk_spread_slope=s6(S1['speed_bulk_periodS']['slope']),
    paper_spread_exponent=2.00, paper_spread_k005=5e-4, end_spread_k005_within5=w5(S1['speed_end']['table']['0.05']['spread'], 5e-4),
    D2_a=a_ok, D2_b=b_ok, D2_CLAUSE='PASS' if (a_ok and b_ok) else 'NOT PASS',
    D2_finding=('measured species-dependent difference: v_end - v_bulk = %.6g (%.6g relative)' % (ve-vb, (ve-vb)/vb)) if abs((ve-vb)/vb) > 1e-6 else 'no difference above 1e-6',
    design_groupvel_record={k: (dict(mean=s6(v['mean']), spread=s6(v['spread'])) if isinstance(v, dict) and 'mean' in v else v) for k, v in S1['design_R6_groupvel_record'].items()},
    end_mode_curve_123=S1['end_mode_curve_123'], chain_modes_k00125_lowest8=S1['chain_modes_k0.0125_x_lowest8'])
# --- X
X1 = S5['X1']
r['X1_realspace'] = dict(measured={k: X1[k] for k in ('unitarity_err', 'outside_cone', 'norm_err', 'reversal_err', 'reach', 'gamma5')}, paper=EX['prose']['exactness_X1'])
r['X2_bookkeeping'] = dict(S5['X2'], paper_cost=EX['prose']['cost_X2'], ok=all(S5['X2'][str(n)]['components'] == c and S5['X2'][str(n)]['floq_shape'] == [c, c] for n, c in ((8, 32), (16, 64))))
r['raw_logs'] = {os.path.basename(f): open(f).read() for f in sorted(glob.glob(os.path.join(R, 'logs', '*.log')))}
json.dump(r, open(os.path.join(R, 'result.json'), 'w'), indent=1, default=float)
print('wrote result.json')
