# L1.1 for the canonical `dirac4` rule: the physical lattice is one BCC orbit (r2)

Quantized Space-Ledger. Written 12 November 2026, America/New_York. This note records a lattice choice made by Edmond Ying and the reason that follows from it. It runs no new computation. Every number below is quoted from an existing record, named with its sha256 where one is known.

This is r2 of `REASON_L1_1_one_BCC.md` (`/workspace/L1_1_one_bcc_reason_20261112/`, sha256 `82e58c43d17f7cafe1f5d6e43d8367e22aaa6fac88590bca5d1052ed018c117e`). That note quoted its paper lines from a stale box copy of the paper, not from main, and it called main's four-taste sentence unapplied, which is false. For every paper citation, this r2 note supersedes it. Every paper citation here refers to main: repository `edmondying-hash/spacetime-ledger`, commit `8251f96564a3394ce093a5260a0d307bb4e2f637`, `space-ledger-v2.md` sha256 `e86ef5c3f1ad9331d61c6033e300dfd37232f4836ce39a55b206bf3985335dc8`. The physics content of the earlier note is kept wherever it is still correct.

## 1. The choice

In the chat of 12 November 2026, Edmond Ying wrote, in order:

- t2542u: "ok, let's move the less is more approach to one bcc orbit"
- t2543u: "ok, changing this will fix L1.1"
- t2544u: "ok, go ahead and write the reason"
- t2546u, on the paper edits: "yes, please go ahead and make all changes"

The choice is that the physical lattice of the ledger is **one** body-centred cubic (BCC) orbit, the one through the origin: the sites of the integer grid whose three coordinates are all even or all odd. The other three orbits of the integer grid are not part of the physical state space. This is a choice about what the lattice is. It is not a repair of the rule, it changes no symbol, and it is not a new run.

## 2. Sources

All files were read on the box, read-only, and hashed with `sha256sum` when this note was written.

| Document | Path | sha256 |
|---|---|---|
| Live plan, `layered_plan_v3.3.md` (v3.3 r2) | `/workspace/layered_plan_v3_3_r2_20261111/` | `89b3972a0af418bfcb260b978842e79dc73945c61ec2bd85fe3a5e7d1785aa39` |
| L0 canonical-rule verification, `VERIFY.md` | `/workspace/L0_canonical_20261109/` | `02945be65e529feb5d7cd10b70e566e3d49e3ab474dc0dec86098348be0ce179` |
| Official V5 v2 census, `results.json` | `/workspace/L0_V4V5_runs_20261111/v5v2_official/` | `ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708` |
| V5 v2 census code, `v5_census.py` (as pinned in that `results.json`) | `/workspace/L0_V5v2_code_r2_20261111/` | `7c6f7ed5aaa6c8fbfe5c823170e1ef3e2c60b3771b9c1406d8bcda394f8f5850` |
| Paper on main, `space-ledger-v2.md` (commit `8251f96564a3394ce093a5260a0d307bb4e2f637`) | `edmondying-hash/spacetime-ledger`, main | `e86ef5c3f1ad9331d61c6033e300dfd37232f4836ce39a55b206bf3985335dc8` |
| Stale box copy of the paper, not main (cited by the earlier note) | `/workspace/whitepaper/space-ledger-v2.md` | `53f5050660f3fe11e86e033c5618d82fe639d1b18ed70f0c1a703ec498497944` |
| v3.2 §6.2 text, `space-ledger-v2.md.v3.2` (its line 518 is byte-identical to main's line 518) | `/workspace/paper_62_draft_20261109/` | `1c88f4a3baa756c2074c86a7ac369ef7c28d62682693088f2485eee076db4678` |
| Paper edit set, `PAPER_EDITS_one_BCC.md` | `/workspace/paper_one_bcc_edits_20261112/` | `a6fa09accdae4e89f070a4bb863a4496278e74f096e4bda0f546576ce6c4a167` |
| Its patched paper, `main_patched.md` | same folder | `8cbb94ec481b3332f074ea028505478dd2d576a8b5d60915f072b653ab6aad70` |
| Its diff, `main_vs_patched.diff` | same folder | `ab2f323d2e71c05c4efe9a06c6d69eb268e036e130eb8cb3b46072d9274430dd` |
| Its `SHA256SUMS` | same folder | `05639f944b2f4a43fd79dc2b8c887f3297f51744a2f594cfb27fcac5ef6578f3` |
| r = 0.05 chain operator, `run_chiral_wall_count.py` (`U_slab`) | `/workspace/chiral_wall_count_20261109/` | `aa5d0cf86a660594a04aa4157b2dff90fe7a0cac9341406d2bbdae30e1eb2c2c` |
| r = 0.05 results, `results_low_r_followup.json` | `/workspace/chiral_rscan_20261109/` | `0f16b0811f88bb105ed299015b5d1d6864ecba2e0afb7697c56f00e0408533f4` |
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

The two findings it refers to are the twelve exact zeros of the §6.2 symbol at the face centres `(±π,±π,0)` and permutations (the plan calls them face centres; main's §6.2 calls the same twelve labels "edges, with two components at ±π", line 518), with U = I to 7e−16, and OP4's three extra nodes H = (π,0,0), P = (π/2,π/2,π/2) and P′ = −P. The plan's "Decision needed" paragraph says "one decision, applied to both rules". The L1 exit gate reads "L1.1 decision made and census re-run for the chosen rule". The plan names `dirac4` as the canonical rule and OP4 as a labelled diagnostic branch (plan, L0 status line).

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

These are proposals only. This note does not edit the paper. The exact line-by-line changes are in the paper edit set, `/workspace/paper_one_bcc_edits_20261112/` (`PAPER_EDITS_one_BCC.md`, sha256 `a6fa09accdae4e89f070a4bb863a4496278e74f096e4bda0f546576ce6c4a167`; `SHA256SUMS` sha256 `05639f944b2f4a43fd79dc2b8c887f3297f51744a2f594cfb27fcac5ef6578f3`). It changes 14 lines of main: 57, 518, 519, 520, 521, 523, 543, 552, 572, 581, 588, 590, 616 and 623.

**Main already carries the four-taste wording.** Main's §6.2 "Doublers" bullet, line 518, reads in part: "This is the four-taste cubic-grid rule: the grid is $\mathbb{Z}^3$, the diagonal hops $h=(\pm1,\pm1,\pm1)$ split it into four decoupled BCC orbits, at $r=0$ there are four cones — $\Gamma$ plus the three two-$\pi$ momenta, one per taste — and the cube $[-\pi,\pi]^3$ is four times the primitive $2\pi^3$ zone." This line is byte-identical to line 518 of `space-ledger-v2.md.v3.2` (`1c88f4a3…`), so that text is applied on main. The earlier note called it unapplied. That was wrong. The same reading appears on main at lines 543, 552, 572, 588 and 616. The edit set replaces all of them with the one-orbit reading.

**The units sentence** is on main **line 523**, not line 524 as the earlier note said: "*Links.* The 8 corner links are $h\in\{(\pm1,\pm1,\pm1)\}$ in units of $a/2$, with $T_h\psi(x)=\psi(x-h)$." The same "units of $a/2$" phrase opens line 518, which also writes the hop sum as $8\prod_i\cos(k_i a/2)$. The sentence is right only if k is also read in radians per a/2. If k is read per a, the cubic cell, the hops become (±1,±1,±1)/2. That gives a 4π period and a zone of volume 16π³ that the cube only half covers, and it makes (π,π,0) a zone-boundary point distinct from Γ. `VERIFY.md` refutes that reading, because the symbol is invariant under π(1,1,0) (residual 2.05e−15 for integer hops against 2.0 for half hops). The identification in Section 4 depends on the hops being integer in the units of k. With integer hops, the hop sum is $8\prod_i\cos k_i$, matching line 525 ($c_i=\cos k_i$). The edit set changes line 523 to the sentence proposed earlier: "The 8 corner links are h∈{(±1,±1,±1)} in integer units of a/2, and k is measured in radians per a/2, so every symbol below is 2π-periodic in each kᵢ. The cores occupy one BCC orbit of this integer grid, the sites whose three coordinates are all even or all odd. Then π(1,1,0) and its permutations are reciprocal lattice vectors, the momenta (±π,±π,0) are the point Γ, and the cube [−π,π]³ covers the primitive zone, of volume 2π³, four times." It keeps $T_h$ as well, and it rewrites line 518 to match.

**§1.2** is main **line 57**, not line 58: "the body-centred cubic (BCC) grid with 8 links per node". This already agrees with the choice. The edit set adds "(one BCC orbit of the integer cubic grid: the sites whose three coordinates are all even or all odd, joined by the corner links $(\pm1,\pm1,\pm1)$)".

**§6.2 low-energy limit** is main **line 543**, not line 544. Main no longer says "the only zero-frequency point is k=0". It says: "Besides $\Gamma$, a census at $\varphi=1.4$ finds three distinct momenta (twelve sign labels), the edges with two components at $\pm\pi$ (see Doublers, above)." The edit set replaces this with: at the tabulated values 0.5 ≤ φ ≤ 1.5, a census finds no zero-frequency point other than k = 0 (up to reciprocal lattice vectors), because the twelve edge labels are Γ itself on the one-orbit lattice, and at φ = π/2 the doublers return.

**The frozen `dirac4.py` docstring** (`f71c782e…`, line 6) gives "hop vectors h = (+-1,+-1,+-1)/2". That is wrong for the code, which uses integer hops. The file is frozen and is not edited.

**Plan frozen conventions** (plan line 100) read "BCC links `h = (±1,±1,±1)/2`, `ℓ = a√3/2`". These have the same dependence on the unit of k. This is flagged here and not edited.

## 7. Consequences

- **Sum-form terms are off the table.** The standard Wilson term r Σᵢ(1 − cos kᵢ) and the face-centre patch g(k) = (1/3) Σᵢ(1 − cos kᵢ) (frozen `dirac4.py`, `_u_n` with `patch` at line 37, and `S_step` with `wilson` at line 66) are not periodic under π(1,1,0). Their axis hops of length 1 leave a BCC orbit. `VERIFY.md` measures this: at r = 0.05 the sum form gives t = 0.2 at the edge copies against 0 at Γ, and about 0.0022 of the norm leaks to each other orbit. On one orbit these terms are not lattice terms.
- **Main's r = 0.05 repair uses the sum form.** Main lines 519 and 588 adopt a chain gap of 2.663×10⁻² E_P, with a Wilson term of mass r = 0.05, on the interior 41³ grid at N_s = 32. That number is `results/0.05/by_Ns/32/interior41/omega_min` = 0.026625477907575197 in `results_low_r_followup.json` (`0f16b081…`). It was computed through `U_slab` (`run_chiral_wall_count.py`, `aa5d0cf8…`, lines 184–195), which passes `wilson_mass` to frozen `dirac4.py` `S_step` line 66, `t = arcsin(m) + wilson·Σ(1 − cos kᵢ)`. `VERIFY.md` line 59 also names it "standard Wilson … the adopted 2.663×10⁻²". A check in the edit set's folder (`one_bcc_checks.py`, `f6418b41…`) gives a shift difference of 0.2998 under π(1,1,0) at r = 0.05, against 1.1×10⁻¹⁵ at r = 0. The edit set therefore withdraws the repair and every number derived from it from lines 519 and 588, without replacing them. It keeps the r = 0 numbers, which do not depend on it.
- **The product form stays.** r(1 − ∏cos kᵢ) uses only on-site and the eight corner hops, stays inside one BCC orbit, and keeps π(1,1,0) periodicity (largest Δt 2.78e−17).
- **Real-space packets.** The Gaussian packets in `dirac4_checks.py` sit on the full cubic grid and put 0.2500 of the norm on each of the four orbits (σ = 4 and σ = 8). Under the choice, such a run reads as four decoupled copies of the one-orbit rule at r = 0. A point source at the origin, as in the unitarity and light-cone tests and in `dw_real.py`, occupies one orbit already.
- **Table `dw` and the L1.2 pre-registration are unaffected.** The chain stack (`dw.py` → `dirac4s.py` → `dirac4.py` → `sym.py`) builds every layer from cos kᵢ and sin kᵢ of the corner hops, plus on-site and inter-copy mixing, so it is periodic under the BCC reciprocal vectors. Its exclusion (`dist_gamma`, used by `dw_gscan.py` and named in the L1.2 pre-registration as "even-parity Γ images, which include the face centres") already removes exactly the Γ images of one orbit. So the r = 0 chain gaps on main line 588 (0.058, 0.046, 0.034 and 0.022 E_P at N_s = 16) and the table values on main lines 558–563 stay valid as doubler gaps of the one-orbit rule. Main's statement that they are "not a global minimum while r=0" falls away, and the edit set removes it. The doubler wall mode that survives for b ≥ 0.3 near (π/2,π/2,±π/2) is a genuine BCC point. It differs from Γ by a vector that is not a reciprocal vector, so the choice does not remove it, and the paper's requirement b ≤ 0.25 stands.

## 8. Status of r7, r8 and the additive route

The choice is recorded as a lattice choice. It is not a repair, and nothing was run to make this note.

- `REPAIR_SPEC_L1_1_r8.md` (`ad02c20147677e527fc81f5f3b6e27a0dd2f1b300cf8dcde4152cc8fdab63afc`) stays hashed and signed off, per its sign-off record (`00c9a8707c4d9880d06a92bd5bb432a8e651dcd4399aa0aa9ad0759813cdf154`). `REPAIR_SPEC_L1_1_r7.md` (`aeca56e4a60bf57a929bb48b1651a23863651e97b41ebeb1b87a06663380ebbb`) is unchanged.
- Under the choice, r8 is no longer the required L1.1 path for `dirac4`, because the first pass clause is met without a repair. Nothing in r8 is withdrawn. Its findings stand as recorded, including the closure of the additive route (routes 1 and 2) by exact unitarity.
- This note does not decide the §3.4 floor of r8, "4/4", or what P is for.

## 9. OP4 is not covered

OP4 production stores one BCC orbit: packed all-even A and all-odd B sites, with no weight on the other three orbits. Its symbol has four isolated Weyl nodes per chirality block, at Γ, H = (π,0,0), P = (π/2,π/2,π/2) and P′ = −P, with chiralities (+,−,+,−) (plan, L1.1). None of H, P or P′ differs from Γ by a reciprocal vector, so all three are genuine points of one BCC zone. The one-orbit choice does not remove them.

OP4 is the labelled diagnostic branch, so this does not block the canonical gate. But the plan's L1.1 is written for "both rules", and that requirement still needs a separate reason or a repair for OP4. This note does not claim that OP4 passes L1.1.

## 10. What remains for Edmond

1. Whether to apply the paper edit set (`/workspace/paper_one_bcc_edits_20261112/`, 14 lines of main) to the paper, and the matching L1.1 line (and the frozen-conventions line) to the plan. The edit set lists its own open items, including which length is ℓ_P (a or a√3/2) and the figure images, which are not regenerated.
2. How the plan's "both rules" requirement is handled for OP4: a reason, a repair, or a change to the requirement.
3. Whether the existing V5 v2 census is accepted as the census for the chosen rule under the L1 exit gate wording ("census re-run for the chosen rule"), or a new census is wanted. This note does not run one.
