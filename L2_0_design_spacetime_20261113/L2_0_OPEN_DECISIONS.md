# L2.0 open decisions (sidecar to `L2_0_RUN_DESIGN.md`)

Written 13 November 2026 (America/New_York) by `spacetime`. None of these is decided by the design or by this file. Each item names the design default that applies only if Edmond gives no other value. Edmond's own words decide each item.

- **D1. Congestion ON or OFF, and which load rule.** Plan C1–C5 say "canonical L0 rule, congestion ON with OFF as a labelled diagnostic." L1.1–L1.3 used the §6.2 vacuum symbol (no load term; uniform load only rescales velocity). C1's commutant search is a linear-algebra statement about the cycle symbol `U_k`. Under a *uniform* vacuum load the symbol is a function of the same `U_k` (rule A: `U^g`; rule B: each factor to the power g), so the commutant of `U_k` is unchanged. A *non-uniform* congestion would make the update state-dependent and would take C1 outside the linear search written in the design. Default: score C1–C5 on the §6.2 vacuum symbol, load rule "none"; run a uniform-load ON diagnostic (rule B at one load, s = f² = 0.81, φ = 1.4, m = 0) and record it, not as a gate. Non-uniform congestion is out of scope for L2.0.

- **D2. Whether to restate or edit paper §5.5.** C5(a) finds, as the plan expected, that `read(a, i, basis, setting)` is a two-outcome attribute with `cos²` inserted, so it does not meet R-d2. Default: record the finding; no paper edit and no plan edit in this work. Whether §5.5 is later restated as shorthand for a link-channel read is yours, and is not done here.

- **D3. The client-record object of gap G-4.** The paper's read-out postulate says a read does not alter the server ledger, so the per-channel martingale (i) has to act on a client-side conditional record. Default: the server state is a complex array that a read never writes; the client holds its own copy; a lock replaces the client copy by the exclusive channel content renormalised to the same total charge Q; two clients correlated with each other start from the same post-lock copy. The design does not claim that this object is grounded in server dynamics; that is part of the S1 residue.

- **D4. The factor-dependent hop used by C5(b).** The plan wants a σ-only or τ-only read "done by a factor-dependent hop then link channels." A product of vacuum `dirac4` layers does not, by itself, separate σ eigenvalues in space (the hop mixes τ, σ and position every tick, but it is not a Stern–Gerlach magnet). Default: a discrete Stern–Gerlach *embedding* on the BCC orbit — the on-site projectors of n·σ (or n·τ), followed by a translation of ±d lattice steps along the nearest coordinate axis — then exclusive spatial regions. This is a unitary of the lattice Hilbert space, not itself one `dirac4` cycle. If you would rather require a product of `dirac4` layers (with, for example, a position-dependent Wilson angle), say so; that would be a different construction and would need its own exclusivity check.

- **D5. Mass m.** Default: m = 0 for every gated check, matching the massless §6.2 symbol used in L1. A labelled diagnostic at m = 0.3 (the born3 value, on this rule rather than on `bcc.py`) is recorded and does not gate.

- **D6. Grid size L.** Default: cubic cell L = 16 (one BCC orbit: all-even union all-odd sites) for C1 drift and for C2–C4; L = 32 for C5(b)–(d), so that a shift d = 8 can separate a packet of width 1.5 from its image and from the mid-plane. If, on a gated state, more than 10⁻⁶ of Q sits on an unassigned mid-band or within two hops of a periodic image of another channel, that cell is UNINFORMATIVE and is rerun at L = 32 (C1–C4) or L = 64 (C5) inside the same cap, once.

- **D7. Machine.** Default: the agent's box. sparky is allowed. `bigbang` is not used (it is occupied with the mass-gap work).

- **D8. Caps.** Default: 1 thread, no GPU, 512 MiB peak RSS, per-check wall 10 min for S0 and C1–C4, 15 min for C5, 40 min total wall, 64 MiB of output, one attempt per check. The probe in this folder projects a whole scored run well under 10 min and under 256 MiB on the box; the caps are a margin, not a target.

- **D9. Wilson and φ.** Default: frozen `U_cycle` defaults, φ = 1.4, `wilson=True`, `wilson_mass=0`, `patch=False`. The 4N_s domain-wall chain is out of scope.

- **D10. How C5(a) interacts with the C5 gate and with C5(b)–(d).** As written, C5 fails if any read primitive is not unitary + link channels, "which leaves R-d2 as an open assumption that S1 must carry." C5(a) has already found that for §5.5 and has found that the L1 harness has no such primitive. Default: keep that as the C5(a) finding; still run C5(b)–(d) as labelled measurements of the new interface in `l20_measure.py`; do not treat C5 as passed while §5.5 remains a two-outcome primitive. If C1–C4 and C5(b)–(d) later pass, the L2.0 exit is the plan's mixed case: S1 narrowed to postulate (i) plus assumption R-d2, not to (i) alone.

- **D11. C1 search: what fails the gate.** Default: only a *positive* local conserved quadratic density other than c Σ\|a\|² (c > 0) fails C1. Extra conserved forms that are indefinite (currents, signed charges) are recorded in full, with their dimension and a basis, and do not fail the gate. If the numerical nullspace has a grey singular value in [10⁻⁸, 10⁻⁴), the search cell is UNINFORMATIVE, not a pass or a fail.

- **D12. Seeds.** Default: five seeds 20261113, 20261114, 20261115, 20261116, 20261117, used in that order for every check that asks for ≥ 5 seeds.

- **D13. C1 tick count and p-norm family.** Default: 1,000 full `dirac4` cycles (each cycle is V⁻ S⁻ V⁺ S⁺). The family is the plan's {0.5, 1, 1.5, 2.5, 3, 4} plus p = 2. Relative drift of p = 2 must be ≤ 10⁻¹²; each other p must drift by more than 10⁻³ on the random-orbit and localized-packet states.

- **D14. Official k-grid for the C1 commutant search.** Default: the 12³ product grid k_i = −π + 2π n_i / 12, n_i = 0…11 (1,728 points in the cube), plus the origin and the six axis mid-points, after reducing by the one-orbit reciprocal identifications only for reporting, not for the linear system. A nested on-site-only search (kernel supported on a single node, 16 real parameters) is reported alongside the 560-parameter node-plus-neighbours search.

- **D15. L2.0 entry versus B9 / L1.5.** The plan's L2.0 entry is the L1 exit gate. L1.1–L1.4 are closed on `main`; L1.5 has been run and passed its gates, with B9 and the B_m record still yours to settle. Default: this design may be hashed and C5(a) stands now; a scored C1–C5 run waits until you name the design sha256 and, unless you say otherwise, until L1.5 is closed. C5(a) does not wait.

- **D16. Approval form.** A scored run of S0 and C1–C5 starts only when your own message names the sha256 of `L2_0_RUN_DESIGN.md` and, if you wish, values for any of D1–D16. Naming the hash of this sidecar or of the audit is not sufficient.
