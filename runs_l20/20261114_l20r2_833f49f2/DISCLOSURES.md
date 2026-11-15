# Post-run disclosures (implementation facts; no re-scoring, nothing rerun)

1. Code changes against the first run's harness are exactly those in /workspace/L2_0_r2_codefix_20261114/R2_NOTE.md
   (C5 geometry cache keeps scalars and fine charges only; C4 shots from default_rng([seed, partition_index]); run_all.py
   check list S0, C4, C5). C4 states are still built from default_rng(seed), so states match the first run's
   (channel charges Q identical cell by cell).
2. A memory-only check of the C5 geometry stage and a synthetic full-size record, with no shots and no gates, ran before
   this run under the same meter and cap: /workspace/L2_0_r2_smoke_NOT_SCORED_20261114/ (peak 139.4 MiB).
3. First-run DISCLOSURES item 3 applies unchanged: the C4 control weight is additive under merging, so the merged A and D
   weights equal the unmerged ones before shot noise.
4. The C5(b) and C5(c) gates require every scored cell within 3 sigma over 2,500 and 1,800 cells respectively.
5. post/make_readout.py was not used; READOUT.md was written after the checks ran (formatting only, numbers copied from
   out/*.json and logs/*_meter.json).
6. The design folder was re-verified (sha256sum -c) before launch and no bytecode was written.
