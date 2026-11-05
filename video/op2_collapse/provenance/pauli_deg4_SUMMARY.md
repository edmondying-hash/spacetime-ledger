# Pauli / degeneracy sketch v4 (blast-spill max radius + cap derived from 8 neighbours + v3 load-follow). Verdict: PARTIAL

Provenance excerpt for the OP2 collapse video. These are toy-run notes, not an empirical validation of the illustration. The video uses the G = 0.01 rows. Local copy of that slice: [`../data/pauli_deg4_G0.01_excerpt.json`](../data/pauli_deg4_G0.01_excerpt.json).
Choices, disclosed:
- Radial shells RMAX=40, 2 spin slots per level per node, level l costs l ticks, no self-load.
- Max radius: blast-spill rule (~/gpu/blast_radius: node cap, overflow split to the 8 BCC neighbours, R ∝ E^{1/3}). At G=0 the pack is exactly the blast ball: R_out ∝ N^{1/3} with slope 0.33, and R_half/R_blast = 0.80, which is the uniform-ball half-mass ratio 0.79, so the outer radius matches the blast radius.
- The hand-set LCAP=16 is replaced by a cap I derived, and it is my interpretation: a node can only shed overflow to its 8 neighbours, so it holds at most 8 levels × 2 spins = 16 fermions before spilling fails. That gives LCAP=7.
- Past that cap, v3's follow-congestion inward pile-up applies.
- G = 0, 0.002, 0.01, 0.03, 0.1; N from 50 to 1e7; ~0.07 s per G, numpy CPU on bigbang.

Collapse N per G: none at G=0 (the flag at N≈4.37M is the lattice running out of room, not a collapse); 56,728 (G=0.002); 4,738 (0.01); 736 (0.03); 61 (0.1).
- Scaling: N_c ∝ G^-1.54 for 0.002–0.01 and G^-1.70 for 0.01–0.03. Real Chandrasekhar scaling is G^-3/2, a qualitative match. At G=0.1, N_c=61 is close to the lattice floor.
- Does blast spill set a sensible max radius? Yes. At G=0 it gives R ∝ N^{1/3} with no extra knob. With pull switched on, R stays at or below the blast radius at every point.
- Is congestion alone enough for runaway? Yes. The pull in this model is congestion from other fermions only, and once the push hits the 8-neighbour cap, R falls to 1 (the grid floor) at every G>0 and never grows back. Central density grows ∝ N. At G=0 there is no runaway, so congestion is what drives it.
- Negative branch: no. There are only short dips (−0.06 to −0.32) on the plateau before a sharp plunge (−1.8 to −5) at onset. There is no sustained R ∝ N^-1/3 white-dwarf branch.
Real-data comparison: real stars show a radius maximum, then the white-dwarf R ∝ M^-1/3 branch, then a cutoff scaling as G^-3/2, then collapse. v4 gets the radius maximum with no knob, the cutoff with roughly G^-3/2 scaling, and the runaway. The −1/3 branch is still missing. R=1 is the lattice floor, not a physical radius.
