# Mass density of the two star types (Pauli v4, unit mass per fermion). Verdict: PASS (qualitative)

Provenance excerpt for the OP2 collapse video. "PASS (qualitative)" is the toy scan's own note about ordering inside the model. It is not an empirical validation of the illustration against real stars. The video uses the G = 0.01 row. Local copy: [`../data/pauli_massdens_G0.01_excerpt.json`](../data/pauli_massdens_G0.01_excerpt.json).
Volume definitions:
- Primary: half-mass density ρ_m = (N/2) / (4/3 π R_half³). Exactly half the mass lies inside R_half, so this is the real mass density of the core.
- Secondary: ρ_m,out = N / (4/3 π R_out³), with R_out = the outermost occupied shell (the blast/support radius).
Units: mass in fermions, length in node spacings, about 1 node per unit volume. One filled ground level holds 2 fermions per node, so ρ_m = 2.

| G | A: N, ρ_half / ρ_out | B (just before collapse): N, ρ_half / ρ_out | C (~10× collapse N): N, ρ_half / ρ_out | B/A half (out) | C/B half (out) |
|---|---|---|---|---|---|
| 0.002 | 141: 1.93 / 1.25 | 46,127: 9.4 / 1.89 | 552k: 65,900 / 2.06 | 4.9 (1.5) | 7,000 (1.0) |
| 0.01 | 141: 1.93 / 1.25 | 3,853: 8.1 / 1.80 | 46k: 5,500 / 1.89 | 4.2 (1.4) | 680 (1.0) |
| 0.03 | 141: 1.93 / 1.25 | 599: 8.2 / 1.14 | 7.2k: 856 / 1.71 | 4.2 (0.9) | 105 (1.0) |

- Planet-like star (A): ρ_m ≈ 2, i.e. one full ground level, the plain Pauli packing density.
- Near collapse (B): core mass density reaches about 8–9, so 4–5× A, as fermions get pushed into higher levels. That is the white-dwarf direction (denser at higher mass).
- After collapse (C): core mass density runs away (10²–10⁴ × B) as mass piles into the central node.
- The R_out version barely moves (about 1–2) because a thin halo of the outermost occupied shells stays filled at ground level. It measures how far that envelope reaches, not how dense the star is, so the half-mass density is the meaningful number.
- Real comparison, qualitative only: the ordering planet < WD < collapsed matches. The real planet-to-WD gap is about 10⁵; the toy gives 4–5× before collapse.
