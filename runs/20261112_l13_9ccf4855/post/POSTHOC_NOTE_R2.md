# Post-hoc note on R2 (written after seeing the S2 result; NOT a score, NOT an input to the verdict)

Written 2026-11-12 America/New_York by the Grok bot. The recorded R2 result (FAIL) stands as recorded; nothing was re-run or re-scored.

Observation from the recorded values in out/S2/result_S2.json, worst pair (phi2, phi4) = (0.5, pi/2):
- Axis directions: v(kappa) = 0.814284096, 0.814283575, 0.814281495, 0.814273170 for kappa = 0.0025 ... 0.02 (quadratic in kappa); v0 = 0.814284269, equal to the factor-1/4 closed form 0.814284269.
- [110]: v(kappa) = 0.814121810, 0.813957362, 0.813622476, 0.812928571. Successive differences roughly double with kappa (1.6e-4, 3.3e-4, 6.9e-4), i.e. v has a term LINEAR in kappa for phi2 != phi4. The pre-declared Richardson in kappa^2 does not remove a linear term, so v0 is biased by about 1e-4.
- By hand, a linear extrapolation of the [110] values from the two smallest kappas gives about 0.814286, close to the closed form, which suggests (not shown) that the kappa -> 0 speed may still match the factor-1/4 formula while the first correction for phi2 != phi4 is O(|k|) and direction dependent. At phi2 = phi4 the linear term is absent (R1 and the R2 diagonal pass at ~4e-14).
- Possible readings (for Edmond, not decided here): the design's measurement protocol (kappa^2 Richardson) and/or its generalised formula are incomplete for phi2 != phi4; or unequal Wilson angles break the symmetry that cancels the O(|k|) direction dependence. Testing either needs a new pre-registered run with its own id and approval.
