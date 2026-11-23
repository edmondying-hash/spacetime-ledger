import math, numpy as np, itertools
import l13_primary as L
K = [0.001,0.002,0.004,0.008,0.016]
def meas(p2,p4):
    res=[]
    for dv in L.DIRS:
        ks=np.stack([dv*k for k in K]); w,_=L.omega_min(ks,p2,p4); v=list(w/np.array(K))
        v0,_=L.neville0(K,v)
        # linear coeff via exact degree-4 polynomial through 5 points
        c=np.polyfit(K,v,4)[::-1]
        res.append((v0,c[1]))
    return res
worst=0; worstR1=0; bmax_eq=0; b100=0
grid=[0.2,0.5,0.8,1.0,1.2,1.4,math.pi/2]
for p2,p4 in itertools.product(grid,grid):
    r=meas(p2,p4); cf=L.c0_pair(p2,p4)
    worst=max(worst,max(abs(a-cf) for a,_ in r))
    if p2==p4: bmax_eq=max(bmax_eq,max(abs(b) for _,b in r))
    b100=max(b100,max(abs(r[i][1]) for i in range(3)))
print("R2b worst |v0-cf| over 49 pairs x13 dirs:",worst)
print("equal-angle max|b|:",bmax_eq," axis [100] max|b| all pairs:",b100)
phis=[i/10 for i in range(1,16)]+[0.8,1.2,math.pi/2]
for p in phis:
    r=meas(p,p); worstR1=max(worstR1,max(abs(a-L.c0_eq(p)) for a,_ in r))
print("R1' worst:",worstR1)
# exchange symmetry
d=0;db=0
for p2,p4 in itertools.combinations(grid,2):
    a=meas(p2,p4); b=meas(p4,p2)
    d=max(d,max(abs(x[0]-y[0]) for x,y in zip(a,b))); db=max(db,max(abs(x[1]-y[1]) for x,y in zip(a,b)))
print("exchange: max|dv0|",d," max|db|",db)
# formula special cases
print("cf(0,0)",L.c0_pair(0,0),"cf(pi/2,pi/2)",L.c0_pair(math.pi/2,math.pi/2),"cf(.5,1.3)-cf(1.3,.5)",L.c0_pair(.5,1.3)-L.c0_pair(1.3,.5))
m=0
for p2,p4 in itertools.combinations(grid,2):
    a=meas(p2,p4); b=meas(p4,p2)
    m=max(m,max(abs(x[1]+y[1]) for x,y in zip(a,b)))
print("antisymmetry max|b(p2,p4)+b(p4,p2)|:",m)
