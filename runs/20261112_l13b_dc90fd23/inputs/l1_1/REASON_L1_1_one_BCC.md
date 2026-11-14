# L1.1 for the canonical `dirac4` rule: the physical lattice is one BCC orbit

Quantized Space-Ledger. Written 12 November 2026, America/New_York. This note records a lattice choice made by Edmond Ying and the reason that follows from it. It runs no new computation. Every number below is quoted from an existing record, named with its sha256 where one is known.

## 1. The choice

In the chat of 12 November 2026, Edmond Ying wrote, in order:

- t2542u: "ok, let's move the less is more approach to one bcc orbit"
- t2543u: "ok, changing this will fix L1.1"
- t2544u: "ok, go ahead and write the reason"

The choice is that the physical lattice of the ledger is **one** body-centred cubic (BCC) orbit, the one through the origin: the sites of the integer grid whose three coordinates are all even or all odd. The other three orbits of the integer grid are not part of the physical state space. This is a choice about what the lattice is. It is not a repair of the rule, it changes no symbol, and it is not a new run.

## 2. Sources

All files were read on the box, read-only, and hashed with `sha256sum` when this note was written.

| Document | Path | sha256 |
|---|---|---|
| Live plan, `layered_plan_v3.3.md` (v3.3 r2) | `/workspace/layered_plan_v3_3_r2_20261111/` | `89b3972a0af418bfcb260b978842e79dc73945c61ec2bd85fe3a5e7d1785aa39` |
| L0 canonical-rule verification, `VERIFY.md` | `/workspace/L0_canonical_20261109/` | `02945be65e529feb5d7cd10b70e566e3d49e3ab474dc0dec86098348be0ce179` |
| Official V5 v2 census, `results.json` | `/workspace/L0_V4V5_runs_20261111/v5v2_official/` | `ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708` |
| V5 v2 census code, `v5_census.py` (as pinned in that `results.json`) | `/workspace/L0_V5v2_code_r2_20261111/` | `7c6f7ed5aaa6c8fbfe5c823170e1ef3e2c60b3771b9c1406d8bcda394f8f5850` |
| Live paper copy, `space-ledger-v2.md` | `/workspace/whitepaper/` | `53f5050660f3fe11e86e033c5618d82fe639d1b18ed70f0c1a703ec498497944` |
| Unapplied §6.2 text, `space-ledger-v2.md.v3.2` | `/workspace/paper_62_draft_20261109/` | `1c88f4a3baa756c2074c86a7ac369ef7c28d62682693088f2485eee076db4678` |
| L1.1 repair specification r8, `REPAIR_SPEC_L1_1_r8.md` | `/workspace/L1_1_repair_spec_r8_20261111/` | `ad02c20147677e527fc81f5f3b6e27a0dd2f1b300cf8dcde4152cc8fdab63afc` |
| r8 sign-off record, `L1_1_repair_spec_r8_20261111_SIGNOFF.txt` (bigbang `/home/eying/spacetime_files/`; box copy in `/workspace/` hashes the same) | see left | `00c9a8707c4d9880d06a92bd5bb432a8e651dcd4399aa0aa9ad0759813cdf154` |
| Generating stack, `qca/dirac4.py` (scan script with `dist_gamma`) | `/workspace/qca/` | `9f01ea8f10947eb6a30506e1499de22e373fc7e1a25fa2689e38c873e2b5aedd` |
| Generating stack, `qca/dirac4s.py` | `/workspace/qca/` | `4db41fe71ce2844f58f1c61c3c84a768b37b82de1bd546a468d3980c3f0627b4` |
| Generating stack, `qca/sym.py` | `/workspace/qca/` | `7b1bbafd4b01464c8f4d4643582c60994f34ed3e119c4167625f2e5905131764` |
| Generating stack, `qca/dw.py` | `/workspace/qca/` | `769833f0393dc1599d5944f6a2837c6ff5ac207ce6ca169eaa2ba9b2ca5fd651` |
| Chain global search, `qca/dw_gscan.py` | `/workspace/qca/` | `5bf6af5d089fd17dbe922f335855e9bf961dc731be4025b591e3e0ff16bf938e` |
| Frozen symbol module `dirac4.py` (the one `VERIFY.md` checks; for example `/workspace/chiral_rscan_20261109/src_readonly/dirac4.py`) | see left | `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff` |
| OP4 production source, `op4_local_gpu.py` | `/workspace/gpu/op4_bcc_local/loaded_packet_L320/` | `e2164af661b9993b3ec588b06c4969a71333ba35d72e59ec720fcaa363c5cfb3` |
| Real-space checks, `qca/dirac4_checks.py` | `/workspace/qca/` | `4e316d9895f035966bb0aa269216dcc38c3986c50c5118907ab609af8e519c05` |
| L1.2 pre-registration, `PREREGISTRATION.md` (staged copy found on the box) | `/tmp/l12_prereg_stage/` | `733752444dfdbaab68654e583b15fdc97619883224fc30357f8ecba998747239` |

Two file names need care. The `qca/dirac4.py` in the generating stack (`9f01ea8f…`) is a scan script that defines `dist_gamma` and `global_min`; it has no docstring. The module with the docstring that says hop vectors are `(±1,±1,±1)/2` is the frozen symbol module `dirac4.py` (`f71c782e…`), line 6. Section 6 refers to that one.

## 3. What L1.1 asks

The plan's L1.1 heading is "L1.1 Doubler census — OP3 (both rules)". Its pass clause reads, exactly:

> **Pass.** For each rule, either no zero except Γ in the closure, or a documented statement that the extra zeros are excluded from the physical state space, and why. **The same decision rule applies to both findings below:** repair it, or give a reason it is unphysical that survives a finite lattice with even L.

The two findings it refers to are the twelve exact zeros of the §6.2 symbol at the face centres `(±π,±π,0)` and permutations, with U = I to 7e−16, and OP4's three extra nodes H = (π,0,0), P = (π/2,π/2,π/2) and P′ = −P. The plan's "Decision needed" paragraph says "one decision, applied to both rules". The L1 exit gate reads "L1.1 decision made and census re-run for the chosen rule". The plan names `dirac4` as the canonical rule and OP4 as a labelled diagnostic branch (plan, L0 status line).

## 4. Why the twelve face-centre labels are Γ

The facts in this section are from `VERIFY.md` unless another source is named.

1. **The hops are integer.** The formula the code implements, u = ∏cos kᵢ − ε∏sin kᵢ (ε = ±1 is a sign), is the eight-corner hop sum for integer hops h = (±1,±1,±1) in the same units as k. OP4 agrees: its eight hop keys are the integer corners, and its real-space bond offsets are ±1.
2. **Four orbits.** Hops (±1,±1,±1) on the integer grid ℤ³ split the walk into four decoupled BCC orbits: (0,0,0)↔(1,1,1), (1,0,0)↔(0,1,1), and the two cyclic partners of the second. Each hop flips the parity of all three coordinates, so an orbit is never left. At r = 0 the measured leak between orbits is about 1e−32 of the norm.
3. **Zone volume.** For integer hops the primitive BCC zone has volume 2π³. The cube [−π,π]³ has volume 8π³, which is four times the primitive zone.
4. **Reciprocal vectors.** π(1,1,0) and its permutations are reciprocal vectors of the hop lattice, which is the FCC lattice generated by π(0,1,1) and cyclic. The symbol is invariant under them: the largest difference over 200 random k is 3.51e−16 on the three generators and 8.01e−16 over all twelve sign patterns.
5. **U at the twelve labels.** At the twelve labels of type (±π,±π,0), U equals U(Γ) to 6.83e−16.

The census code uses the same set. Its Γ images are the points πg with g an integer triple of even sum (`v5_census.py`, `GAMMA_IMAGES`; `qca/dirac4.py`, `dist_gamma`, which skips g when `sum(g)%2` is odd). Those even-sum points are exactly the reciprocal lattice of the orbit through the origin.

On one BCC orbit, therefore, the twelve face-centre labels name the point Γ itself, not twelve additional points. The plan's own L0 status line already records that "those twelve points are Γ images under the even-parity lattice and lie in the V5 exclusion set".

## 5. Why the first pass clause is met for `dirac4`

With one BCC orbit as the physical lattice, the zeros of `dirac4` in the closure are as follows.

- **The 27 high-symmetry labels.** Mod 2π they are 8 distinct momenta. On one orbit they fall into two classes, not four: Γ, and the H class (the faces and the corner). The H class has gap π/2 − φ, which is 0.17079632679489665 at φ = 1.4. Γ is the only zero among them.
- **The interior.** The official V5 v2 census is unrepaired `dirac4` at m = 0, run on a 129³ boundary-inclusive grid and from 300 random starts, with local minima refined by Nelder–Mead and a 0.3 exclusion around every even-parity Γ image. It reproduced Table `dirac4`. Outside the exclusion it found only a nonzero gap:

| φ | smallest non-excluded ω (search a) | distance of argmin to nearest Γ image |
|---|---|---|
| 0.5 | 0.217127955311918 | 2.2214 |
| 0.8 | 0.26167630634482675 | 2.2214 |
| 1.0 | 0.23202826004369173 | 1.8901 |
| 1.2 | 0.1668769618006517 | 1.8616 |
| 1.4 | 0.08212694658054251 | 1.9360 |
| 1.5 | 0.034884422707531004 | 2.0266 |

At φ = π/2 the census value is 1.4e−17, in line with the paper's table entry "0 (doublers return)". That endpoint is not a pass, and it is not the canonical setting. The paper's default is φ = 1.4.

- **Inside the exclusion balls.** Every ball is centred on a Γ image, so on one orbit every ball is a neighbourhood of Γ itself. Near Γ the band is the Dirac cone, with slope ±0.98910736 (`VERIFY.md`, Richardson).

So, for 0 < φ < π/2 at the tabulated values, `dirac4` on one BCC orbit has no zero except Γ in the closure. This is the **first** pass clause of L1.1. It does not rely on the second clause, the "documented exclusion".

**The even-L condition.** The plan asks that a reason survive "a finite lattice with even L", because k = π lies on the momentum grid of an even lattice. On one orbit this holds for the following reason. Take a periodic cubic grid of even side N, as in the real-space runs (N = 48 or 128 in `dirac4_checks.py`, N = 40 in `dw_real.py`). Wrapping by an even N preserves coordinate parity, so the four orbits stay separate on the torus, and the orbit through the origin is itself a periodic BCC torus with N³/4 sites. For every site x of that orbit, π(1,1,0)·x = π(x₁ + x₂) is a multiple of 2π, so the plane wave at k + π(1,1,0) is the same function on the orbit as the plane wave at k. The label (π,π,0) is on the momentum grid when N is even, as the plan says, but on the orbit it is the same state as Γ, not a second state. The finite even lattice therefore leaves the identification intact.

## 6. Wording in the paper

These are proposals only. The paper is not edited by this note.

**§6.2 "Links" sentence** (live copy, line 524): "The 8 corner links are h∈{(±1,±1,±1)} in units of a/2, with T_h ψ(x) = ψ(x − h)." The sentence is right only if k is also read in radians per a/2. If k is read per a, the cubic cell, the hops become (±1,±1,±1)/2. That gives a 4π period, a zone of volume 16π³ that the cube only half covers, and makes (π,π,0) a zone-boundary point distinct from Γ. `VERIFY.md` refutes that reading, because the symbol is invariant under π(1,1,0) (residual 2.05e−15 for integer hops against 2.0 for half hops). The identification in Section 4 depends on the hops being integer in the units of k.

Proposed replacement: "The 8 corner links are h∈{(±1,±1,±1)} in integer units of a/2, and k is measured in radians per a/2, so every symbol below is 2π-periodic in each kᵢ. The cores occupy one BCC orbit of this integer grid, the sites whose three coordinates are all even or all odd. Then π(1,1,0) and its permutations are reciprocal lattice vectors, the momenta (±π,±π,0) are the point Γ, and the cube [−π,π]³ covers the primitive zone, of volume 2π³, four times."

**§1.2** (live copy, line 58) says "the body-centred cubic (BCC) grid with 8 links per node". That already agrees with the choice. A possible addition is "(one BCC orbit of the integer cubic grid, with corner links (±1,±1,±1))".

**§6.2 low-energy limit** (live copy, line 544) says "For 0<φ<π/2 the only zero-frequency point is k=0." Under the choice this is correct when k = 0 is read up to reciprocal lattice vectors. A possible clarification is "k = 0 (up to reciprocal lattice vectors)".

**The unapplied v3.2 four-taste sentence** (`space-ledger-v2.md.v3.2`, line 518) reads "This is the four-taste cubic-grid rule: the grid is ℤ³ …". It describes all four orbits as physical, so it is withdrawn and should not be applied.

**The frozen `dirac4.py` docstring** (`f71c782e…`, line 6) gives "hop vectors h = (+-1,+-1,+-1)/2". That is wrong for the code, which uses integer hops. The file is frozen and is not edited.

**Plan frozen conventions** (plan line 100) read "BCC links `h = (±1,±1,±1)/2`, `ℓ = a√3/2`". These have the same dependence on the unit of k. This is flagged here and not edited.

## 7. Consequences

- **Sum-form terms are off the table.** The standard Wilson term r Σᵢ(1 − cos kᵢ) and the face-centre patch g(k) = (1/3) Σᵢ(1 − cos kᵢ) (frozen `dirac4.py`, `_u_n` with `patch`, and `S_step` with `wilson`) are not periodic under π(1,1,0). Their axis hops of length 1 leave a BCC orbit. `VERIFY.md` measures this: at r = 0.05 the sum form gives t = 0.2 at the edge copies against 0 at Γ, and about 0.0022 of the norm leaks to each other orbit. On one orbit these terms are not lattice terms.
- **The product form stays.** r(1 − ∏cos kᵢ) uses only on-site and the eight corner hops, stays inside one BCC orbit, and keeps π(1,1,0) periodicity (largest Δt 2.78e−17).
- **Real-space packets.** The Gaussian packets in `dirac4_checks.py` sit on the full cubic grid and put 0.2500 of the norm on each of the four orbits (σ = 4 and σ = 8). Under the choice, such a run reads as four decoupled copies of the one-orbit rule at r = 0. A point source at the origin, as in the unitarity and light-cone tests and in `dw_real.py`, occupies one orbit already.
- **Table `dw` and the L1.2 pre-registration are unaffected.** The chain stack (`dw.py` → `dirac4s.py` → `dirac4.py` → `sym.py`) builds every layer from cos kᵢ and sin kᵢ of the corner hops, plus on-site and inter-copy mixing, so it is periodic under the BCC reciprocal vectors. Its exclusion (`dist_gamma`, used by `dw_gscan.py` and named in the L1.2 pre-registration as "even-parity Γ images, which include the face centres") already removes exactly the Γ images of one orbit. The doubler wall mode that survives for b ≥ 0.3 near (π/2,π/2,±π/2) is a genuine BCC point. It differs from Γ by a vector that is not a reciprocal vector, so the choice does not remove it, and the paper's requirement b ≤ 0.25 stands.

## 8. Status of r7, r8 and the additive route

The choice is recorded as a lattice choice. It is not a repair, and nothing was run to make this note.

- `REPAIR_SPEC_L1_1_r8.md` (`ad02c20147677e527fc81f5f3b6e27a0dd2f1b300cf8dcde4152cc8fdab63afc`) stays hashed and signed off, per its sign-off record (`00c9a8707c4d9880d06a92bd5bb432a8e651dcd4399aa0aa9ad0759813cdf154`). `REPAIR_SPEC_L1_1_r7.md` (`aeca56e4a60bf57a929bb48b1651a23863651e97b41ebeb1b87a06663380ebbb`) is unchanged.
- Under the choice, r8 is no longer the required L1.1 path for `dirac4`, because the first pass clause is met without a repair. Nothing in r8 is withdrawn. Its findings stand as recorded, including the closure of the additive route (routes 1 and 2) by exact unitarity.
- This note does not decide the §3.4 floor of r8, "4/4", or what P is for.

## 9. OP4 is not covered

OP4 production stores one BCC orbit: packed all-even A and all-odd B sites, with no weight on the other three orbits. Its symbol has four isolated Weyl nodes per chirality block, at Γ, H = (π,0,0), P = (π/2,π/2,π/2) and P′ = −P, with chiralities (+,−,+,−) (plan, L1.1). None of H, P or P′ differs from Γ by a reciprocal vector, so all three are genuine points of one BCC zone. The one-orbit choice does not remove them.

OP4 is the labelled diagnostic branch, so this does not block the canonical gate. But the plan's L1.1 is written for "both rules", and that requirement still needs a separate reason or a repair for OP4. This note does not claim that OP4 passes L1.1.

## 10. What remains for Edmond

1. Whether to apply the §1.2 and §6.2 wording in Section 6 to the paper, and the matching L1.1 line (and the frozen-conventions line) to the plan.
2. How the plan's "both rules" requirement is handled for OP4: a reason, a repair, or a change to the requirement.
3. Whether the existing V5 v2 census is accepted as the census for the chosen rule under the L1 exit gate wording ("census re-run for the chosen rule"), or a new census is wanted. This note does not run one.
