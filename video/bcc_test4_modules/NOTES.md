# bcc_test4 explainer videos: run notes (Nov 13, 2026)

Source: exact copy of bigbang:~/bcc_test4 (bcc_test4.tgz), extracted to src/ and never modified.
Suite run: `python3 run_bcc_suite.py` in a scratch copy -> suite_output.txt (exit 0, 34 tests OK, 50.5 s).
Horizon CLI: `python3 bcc3dhorizonsim.py --size 17 --workload 2400 --packets 260` -> horizon_cli_output.txt.
JSON export attempt: `run_bcc_suite.py --skip-tests --json-out ...` -> json_out_attempt.txt (exit 2).

Every renderer imports the module unchanged. Where it needs per-tick state, it copies a loop and
asserts that the copy reproduces the module's printed numbers.

## README vs actual output
- README says 31/31 unit tests; the run gives 34 (it misses the 3 tests in test_bcc3dhorizonsim.py).
  benchmark_report.json also says 31; validation.txt is an older 11-test baryon-only log.
- README says "all 6 simulation modules"; the runner executes 7.
- The README's JSON export command fails: baryon_calculator.main() parses sys.argv and rejects
  --skip-tests/--json-out (exit 2). collect_json_snapshot() also references names that don't exist
  (BCCMesonSimulator, DEFAULT_MESONS, base_mass_per_step=, packets=).
- "1/r Poisson congestion": r*W(r) drops from 86.85 to 29.76 over r = 1..8, so the falloff is steeper than 1/r on the 25^3 box.
- "single local rule / 6-face": bcc_unified_sim and bcc_em_wave_sim use 8 diagonal BCC neighbours,
  not 6 faces. baryon_calculator calls itself "not a BCC or time-evolution simulation", and
  bcc_meson_sim is a closed-form formula with hand-set quark masses.
- The meson README lists the model values but leaves out that D and D* miss PDG by -103.20 and -116.55 MeV.
- escaped_packets = 0 is hard-coded in all three deadlock routines. Packets are only ever placed on
  the shell, so zero escape is a property of the setup, not something the code measures.
- Glueball "mass gap" 2001.18: average links (about 4.7) x (145 route + 280 self) ticks. The tick costs are chosen inputs.
- Born/wave "convergence": the target is a hand-picked exp(-x^2/N)*cos^2(pi x/4) curve whose zeros
  fall on the dark nodes. It is not a solved wave equation. The error is still 0.067 at N=100.
- Double slit: the no-detector pattern alternates row to row (2-row period, i.e. the grid scale).
  The detector pattern is irregular and peaks at y=17, which is the monitored slit row.
- Unified sim grid masses are tick counts (N = 544.65 at 1 tick := 1 MeV). The "emergent" m_light/m_strange/A
  are refitted to the grid's own N, Delta, Lambda, so those three match by construction.
- Runner cosmetic issue: unified and born_pascal have no matching entry-function names, so they run as
  subprocesses and print before the suite header. The runner's horizon step uses the defaults
  (19^3, 300 packets -> 105 nodes), not the README CLI example (17^3, 260 -> 98).
