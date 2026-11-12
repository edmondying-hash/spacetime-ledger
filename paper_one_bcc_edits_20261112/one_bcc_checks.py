import os,sys,json,numpy as np
os.environ['OMP_NUM_THREADS']='1'
sys.path.insert(0,'/workspace/chiral_rscan_20261109/src_readonly'); import dirac4 as F
rng=np.random.default_rng(20261112); K=rng.uniform(-np.pi,np.pi,(20,3))
sh=[np.pi*np.array(v) for v in ([1,1,0],[1,0,1],[0,1,1])]
out={}
out['sum_t_r0.05']={str(p):0.05*float(np.sum(1-np.cos(np.array(p,float)))) for p in ([0,0,0],[np.pi,np.pi,0],[np.pi,0,0],[np.pi,np.pi,np.pi])}
for r in (0.0,0.05):
    out[f'Ucycle_maxdiff_shift_r{r}']=max(float(np.abs(F.U_cycle(k+s,wilson_mass=r)-F.U_cycle(k,wilson_mass=r)).max()) for k in K for s in sh)
    out[f'U(pi,pi,0)-U(G)_r{r}']=float(np.abs(F.U_cycle(np.array([np.pi,np.pi,0.]),wilson_mass=r)-F.U_cycle(np.zeros(3),wilson_mass=r)).max())
os.chdir('/workspace/qca'); g={}
exec(open('/workspace/qca/dw.py').read(),g)
out['qca_dist_gamma_(pi,pi,0)']=float(g['dist_gamma'](np.array([[np.pi,np.pi,0.]]))[0])
out['qca_chain_Ns4_b0.2_maxdiff_shift']=max(float(np.abs(g['floq'](k+s,4,1.4,0.2)-g['floq'](k,4,1.4,0.2)).max()) for k in K[:8] for s in sh)
out['qca_cycle_maxdiff_shift']=max(float(np.abs(g['periodS']((k+s)[None],0.0,1.4)[0]-g['periodS'](k[None],0.0,1.4)[0]).max()) for k in K for s in sh)
print(json.dumps(out,indent=1)); json.dump(out,open('/tmp/onebcc_chk/chk_out.json','w'),indent=1)
