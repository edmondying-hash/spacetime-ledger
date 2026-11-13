# L1.2 pre-registration: chirality-chain reproduction (Table dw)

2026-11-12, America/New_York. Written before any L1.2 run. Nothing runs under this pre-registration until Edmond approves the caps and says to run.

**Authority.** Edmond, 2026-11-12, t2539u: "L1.2 then." Tightened against t2540u (the three cases the existing artifacts do not settle, and the two smaller pinning items). Live plan v3.3 r2, `layered_plan_v3.3.md` sha256 `89b3972a0af418bfcb260b978842e79dc73945c61ec2bd85fe3a5e7d1785aa39`, §3 L1.2.

**What L1.2 is (plan, verbatim).** "Reproduce Table `dw`: residual mass vs Ns, `|γ5|`, localisation length, smallest gap vs b. Pass: within 5%, and `b ≤ 0.25` boundary confirmed independently. Then test the *end-mode* dispersion against the physical-mode dispersion: the chiral mode's speed is 0.9855 of the hop rate; a difference would be a species-dependent `c`."

**This is not a retry of V5.** Official V5 v2 is spent: verdict "V5 FAIL (tables not reproduced: 6)", `results.json` sha256 `ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708`. That failure is the \(N_s=24\) residual under the V5 order-of-magnitude rule. L1.2 is a new pre-registration. Archived V5 outputs are not re-scored. The generating script's `r[:,1]>1e-15` cut is not changed. The paper is not edited.

**Existing artifacts are not the official L1.2 result.** Every Table `dw` cell except \(N_s=24\) already reproduces from pinned artifacts (residuals at \(N_s=2,4,8,12\) inside 5%; \(|\gamma_5|\) and localisation at the printed digits; prose doubler gaps at \(N_s=16\), \(b\le0.25\), within 0.2%; end-mode speed 0.98553 against 0.9855; spread slope \(k^{2.0016}\) against \(k^{2.00}\); decay slopes \(-1.3904\), \(-0.6977\) against \(-1.390\), \(-0.698\)). Those numbers are cited here as the reason this document concentrates on the awkward cases. The official run still measures the table. It does not treat those artifacts as the L1.2 result.

---

## Decisions this pre-registration settles

These are the three cases no existing artifact settles, and the two smaller pins. They are the point of the document.

**1. Floor clause for the \(N_s=24\) cell.** A 5% comparison is undefined. The residual is produced by a \(96\times96\) `np.linalg.eig`. Existing artifacts sit at about \(2.4\times10^{-15}\) at \(N_s=22\) and at \(1.211415271493058\times10^{-17}\) (official V5) at \(N_s=24\); the printed \(\sim10^{-16}\) is about eight times that regenerated value, at the eig noise floor. The V5 order-of-magnitude rule (`round(log10|x|) == printed exponent`) is not reused: that would be a retry of a spent attempt. This cell is **UNINFORMATIVE**: the official run reports the raw residual, \(\log_{10}\), and the \(N_s=22\) residual as a floor diagnostic; the cell is listed and does not block PASS. This is the same treatment D19 used for cells that cannot be compared, declared here for L1.2; it is not an amendment of the spent V5 verdict (V5 r2 had no UNINFORMATIVE-below-resolution class, and that stands for V5).

**2. Independent confirmation of \(b\le0.25\).** The stored scans (`gscan_0.1.txt` sha256 `acfb869d7ef8f054462e1c9f6b617837c7abe401ea45d0a51b778f4f35b230d7`, `gscan_0.15.txt` `51c364558deea2eac4c9122ff6a5a102addfd93577f9cd90c65a8db06e6a0bbf`, `gscan_0.2.txt` `75f4c677ea3f6d62735177b962b7ed8c53cbeb3b57f9fbb48064a1f3d625c148`, `gscan_0.25.txt` `75a4224d47723e92b5fa20e50f41dce269014c1dbb03972fd253bbff1e3009e6`) cover only \(b\le0.25\). The paper's claim rests on what happens at \(b\ge0.3\). Those stored files are not re-scored as L1.2. The independent confirmation is a new measurement, by two named estimators, on a pre-registered \(b\) ladder and \(N_s\) trend, including \(b\ge0.3\):

- **E1, special-point exact.** The lowest \(|\omega|\) at \(k=(\pi/2,\pi/2,\pm\pi/2)\) and all sign combinations (eight points). This is the paper figure's dashed line ("at the surviving special point only").
- **E2, global Nelder–Mead, `dw_gscan.py` protocol.** Exact protocol of the pinned generator sha256 `5bf6af5d089fd17dbe922f335855e9bf961dc731be4025b591e3e0ff16bf938e`: for each \((b,N_s)\), a fresh `numpy` `default_rng(1)`, 60 starts uniform on \([-\pi,\pi]^3\), Nelder–Mead, `xatol=1e-7`, `fatol=1e-12`, `maxiter=1500`, exclusion `dist_gamma(k)>0.3` (even-parity \(\Gamma\) images, which include the face centres). This is the paper figure's solid line ("global search"). The 60-start, re-seeded-`rng(1)` setting is part of the protocol, not a free choice.

**\(b\) ladder:** \(\{0.10, 0.15, 0.20, 0.25, 0.30, 0.35\}\).

**\(N_s\) trend:** E2 on the full ladder at \(N_s\in\{8,16\}\) (the generator's own pair). E1 on the full ladder at \(N_s\in\{8,12,16,24\}\), so that "falls exponentially with \(N_s\)" is a measured trend, not a two-point remark.

**Pass (boundary), predeclared reading.** The clause is met if and only if all three hold. A disagreement is a result and is preserved.

- (i) At \(N_s=16\), E2 for \(b=0.10,0.15,0.20,0.25\) is within 5% of the prose figures \(0.058\), \(0.046\), \(0.034\), \(0.022\) respectively (these figures appear only in the prose; the prose is authoritative for them).
- (ii) For each \(b\in\{0.30,0.35\}\), the E1 gap is strictly decreasing across \(N_s=8,12,16,24\) (or across the \(N_s\) still above \(10^{-12}\), if a later point hits the eig floor), and a linear fit of \(\log(\text{gap})\) versus \(N_s\) has negative slope.
- (iii) For each \(b\in\{0.10,0.15,0.20,0.25\}\), the E1 gap does not collapse: the \(N_s=16\) value is at least half the \(N_s=8\) value, and E2 at \(N_s=16\) is greater than \(10^{-3}\).

Separately, evaluate the chain exactly at the twelve face centres \((\pm\pi,\pm\pi,0)\) and permutations, at \(b=0.2\) and \(b=0.3\), \(N_s\in\{8,16\}\). This is a finding, not an L1.2 pass clause: whether the chain lifts the L1.1 zeros is reported and is not decided here. The prior counter `run_chiral_wall_count.py` sha256 `aa5d0cf86a660594a04aa4157b2dff90fe7a0cac9341406d2bbdae30e1eb2c2c` is a different stack (the later frozen rewrite `f71c782e…`) and is not used as an L1.2 estimator.

**3. Portability (pre-registered deviation).** Every generator begins `exec(open('/workspace/qca/….py').read())`, and `/workspace` does not exist on ED. The official run is on my computer (the box), not on ED and not on bigbang. Byte-identical copies of the six generating-stack files sit in this folder's `frozen/`. The harness redirects every open of a `/workspace/qca/` path, and the relative open of `sym.py`, to the sibling frozen file, without editing the frozen bytes. That path relocation is a pre-registered deviation. The relocated hashes must match the pins below at the start and at the end of the run, and must match `/workspace/qca/` on the box (read-only; that tree is not written). `dirac4s.py`'s hardcoded `/workspace/qca/dirac4.py` is included in the redirect.

**Authoritative figures.** Where a quantity appears in Table `dw`, the table cell is authoritative for the 5% reproduction gate (the prose sometimes carries more digits than the table: residual \(2.9\times10^{-3}\), and the prose-only \(-1.390\) and \(0.9855\)). Where a quantity appears only in the prose, that printed figure is the comparison value for that item: the doubler gaps \(0.058,0.046,0.034,0.022\) under (i) above; the decay slopes \(-1.390\), \(-0.698\) and the end-mode speed \(0.9855\) are reported against the prose and are not part of the 5% PASS (the plan's 5% names the table and the gap-versus-\(b\) figures; the speed test is a measurement, below).

---

## Generating stack (pinned, read-only)

Like-for-like with the paper's Table `dw` generator, not the later frozen rewrite sha256 `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff`. The chain's four-tick cycle is the one in `dirac4s.py` / `dw.py`: \(E^+\), \(V_h^+\), \(E^-\), \(W\,V_h^-\), with \(\omega=\arg\lambda/4\).

| file | sha256 |
|---|---|
| `sym.py` | `7b1bbafd4b01464c8f4d4643582c60994f34ed3e119c4167625f2e5905131764` |
| `dirac4.py` | `9f01ea8f10947eb6a30506e1499de22e373fc7e1a25fa2689e38c873e2b5aedd` |
| `dirac4s.py` | `4db41fe71ce2844f58f1c61c3c84a768b37b82de1bd546a468d3980c3f0627b4` |
| `dw.py` | `769833f0393dc1599d5944f6a2837c6ff5ac207ce6ca169eaa2ba9b2ca5fd651` |
| `dw_final.py` | `48046ea5332a12322d05ec11a0ea733dc920e05b6f7948a5387904bb43fc6aa1` |
| `dw_gscan.py` | `5bf6af5d089fd17dbe922f335855e9bf961dc731be4025b591e3e0ff16bf938e` |

All six are bit-identical, on this box, to every other copy of the same file. The harness loads the frozen copies through the deviation in decision 3.

**Congestion.** The generating stack is a free Floquet symbol and has no congestion rule. This run measures that symbol. No new load rule is introduced.

**Not in scope.** L1.1 census and the §3.4 floor decision; L1.3 \(\varphi\) scan; L1.4 and L1.5; paper, plan, or repo edits; the paper's \(40^3\) real-space exactness paragraph; any face-centre repair.

---

## A. Table dw reproduction

Parameters: \(\varphi=1.4\), \(b=0.2\). Method: `dw_final.py`. Residual mass at \(k=0\); profiles along direction \((1,2,3)/\sqrt{14}\); degeneracy resolved by the chain-position operator in the four-dimensional low-frequency subspace; localisation from the same log-profile fit as that script. Table cells are taken from `walls[0]`, as V5 D18.

**Residual mass.** \(m_0=0.05\), \(N_s=2,4,8,12,24\) (the paper cells), and \(N_s=22\) as the floor diagnostic for decision 1. The \(m_0=0.1\) series and the two decay-rate fits are computed and reported against the prose figures \(-1.390\) and \(-0.698\), labelled as references, not scored in the 5% PASS.

Printed residual cells (Table `dw`, \(m_0=0.05\); table is authoritative):

| \(N_s\) | Components | Residual mass | Gate |
|---|---|---|---|
| 2 | 8 | \(2.9\times10^{-3}\) | 5% |
| 4 | 16 | \(1.8\times10^{-4}\) | 5% |
| 8 | 32 | \(7.0\times10^{-7}\) | 5% |
| 12 | 48 | \(2.7\times10^{-9}\) | 5% |
| 24 | 96 | \(\sim10^{-16}\) | UNINFORMATIVE (floor clause) |

**Chirality and localisation.** \(N_s=16\), \(m_0=0\), \(|k|\in\{0.01,0.05,0.1,0.15,0.2\}\).

| \(|k|\) | \(|\gamma_5|\) | Loc. length |
|---|---|---|
| 0.01 | 1.0000 | 0.12 |
| 0.05 | 0.9999 | 0.20 |
| 0.1 | 0.9993 | 0.29 |
| 0.15 | 0.9953 | 0.40 |
| 0.2 | 0.954 | 0.64 |

**Pass (reproduction).** Every scored cell is within 5% of the Table `dw` printed value. Scored: residual at \(N_s=2,4,8,12\); all five \(|\gamma_5|\); all five localisation lengths. The \(N_s=24\) cell is UNINFORMATIVE under the floor clause and does not block this PASS. A scored-cell miss is a result, not a harness failure, and is preserved.

---

## B. Smallest gap versus \(b\), and the \(b\le0.25\) boundary

The two named estimators E1 and E2, the \(b\) ladder, the \(N_s\) trend, and the three-part pass clause are decision 2 above. The official run executes that procedure. The stored `gscan_*.txt` files are not re-scored as L1.2.

---

## C. End-mode versus physical-mode speed

The estimator is fixed and is the same on both sides: lowest-mode phase velocity \(|\omega_{\min}|/|k|\), the 13 directions in `dw_final.py`, \(\kappa\in\{0.0125,0.025,0.05\}\). The end-mode uses the chain at \(N_s=16\), \(m_0=0\), \(\varphi=1.4\), \(b=0.2\). The physical-mode (bulk) control is the four-component cycle of the same stack, no chain (`dirac4s.py` `periodS`, \(m=0\), \(\varphi=1.4\)); it is not \(N_s=1\) with `Wmat`.

Reported, for each side: `speed_mean` and `spread` at each \(\kappa\); the spread slope from `polyfit` of \(\log(\text{spread})\) versus \(\log(\kappa)\), as in `dw_final.py` (paper: \(k^{2.00}\)); and `speed_mean` at \(\kappa=0.0125\) (paper prose: \(0.9855\) for the end mode; \(0.989\) for the four-component rule). A difference between the two `speed_mean` values (end versus physical, same \(\kappa=0.0125\)) is a species-dependent \(c\). This comparison is a measurement and a finding; it is not scored as "pass if equal to \(0.9855\)."

---

## Harness checks

Stop on a failed harness check. A paper-cell miss is not a harness failure.

- **G0.** Frozen hashes match this pre-registration, and the `/workspace/qca/` sources still match those hashes, at the start and at the end (read-only).
- **G0b.** Floquet unitarity: \(\max\|U^\dagger U-I\|\le10^{-12}\) on the declared sample set \(k=0\), \(k=(0.05,0,0)\), and \(k=(0.1,0.1,0.1)\), for both the chain (\(N_s=16\), \(b=0.2\), \(m_0=0\)) and the four-component cycle (\(m=0\), \(\varphi=1.4\)).
- **G1.** At \(m_0=0\), \(k=0\), the chain residual mass is \(\le10^{-14}\) (paper: the end modes are exactly massless). If this fails, stop.

---

## Caps (proposed)

One CPU thread on the box (not GPU, not bigbang, not ED). 1 GiB combined process-tree RSS. 300 CPU seconds. 360 seconds wall. 16 MiB total new output. One attempt. Hard stop at the caps. New output only under this folder's `out/`, and only after approval. Production files are not written. The path relocation in decision 3 is the only deviation.

**Output.** `out/result.json` (all numbers, pins, seeds, scored-cell comparisons, E1 and E2 ladders, the three boundary clauses, speeds, and resources: CPU, wall, peak RSS) and `out/run.log`. Failed or partial runs are kept.

**Harness.** `run_l12.py`, hashed with this pre-registration. One attempt; no silent retry.

---

## Approval question

Approve one CPU-only L1.2 chirality-chain reproduction on the pinned generating stack, on my computer, with the path relocation recorded as a deviation (Table `dw` residual mass, \(|\gamma_5|\) and localisation, with the \(N_s=24\) cell UNINFORMATIVE under the floor clause; independent doubler-gap versus \(b\) by E1 and E2, including the \(b\le0.25\) boundary and the \(b\ge0.3\) \(N_s\) trend; end-mode versus physical-mode speed, same estimator)? Limits: one thread, 1 GiB, 300 CPU seconds, 360 seconds wall, 16 MiB output, one attempt. This is not a retry of V5.
