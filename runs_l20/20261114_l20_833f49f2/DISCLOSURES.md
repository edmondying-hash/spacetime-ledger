# Post-run disclosures (implementation facts; no re-scoring, nothing rerun)

1. C5 cap trip. The meter killed C5 at 2.88 s (sampled tree RSS 532.8 MiB > 512 MiB). Most likely cause, from reading the
   glue code (not confirmed by a rerun): `check_C5` keeps every post-hop array (`moved`, 4 x 32^3 complex128, 2 MiB each)
   in its geometry cache `geo` for every (state, direction, factor[, seed]) cell. This is a fault in the run-folder glue
   code, not a design parameter. Per the one-attempt rule C5 was not retried; C5(b)-(d) are UNINFORMATIVE.
2. C4 seeding. Each (partition, seed) cell uses a fresh default_rng(seed); for seeds 1-4 the state's channel weights are
   0.4/0.3/0.2/0.1 on every partition, so the Q-share draws are identical across the three partitions. The seed 20261114
   Q-share failure (D shift z = 3.46) is one draw set that appears in all three partitions.
3. C4 controls follow design §2 (w_k proportional to the per-site sum of |a_i|^p over channel k). That weight is additive under
   merging, so the merged A and D weights equal the unmerged ones before shot noise.
4. C1 rule-B diagnostic. The C1 stepper-fault rule (p = 2 drift > 1e-12 at cycle 1) was also applied to the diagnostic
   series, so it stopped after cycle 1. Sums of |a|^p are taken over orbit sites only (all of C1); off-orbit charge was not
   recorded. The maximum |eigenphase| of the rule-B factors reached pi (principal-branch edge).
5. C2 states P1 and P2 share the same spatial envelope, so their channel charges are identical; only the spinor differs.
6. `post/make_readout.py` (formatting only) was written after the checks ran.
7. The S0 P0 check confirmed the design-folder hashes; the design folder was re-verified after the run (sha256sum -c OK) and
   no __pycache__ was created there.
