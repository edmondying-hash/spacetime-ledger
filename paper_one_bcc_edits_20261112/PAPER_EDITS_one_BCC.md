# Paper edits for the one-BCC lattice: every changed line of `space-ledger-v2.md` on main

Quantized Space-Ledger. Written 12 November 2026, America/New_York.

## 1. Base and scope

- Repository `edmondying-hash/spacetime-ledger`, branch main, commit `8251f96564a3394ce093a5260a0d307bb4e2f637`.
- File `space-ledger-v2.md`, sha256 `e86ef5c3f1ad9331d61c6033e300dfd37232f4836ce39a55b206bf3985335dc8`, 1531 lines. All line numbers below refer to this file.
- The choice being applied, made by Edmond Ying in the chat of 12 November 2026 (t2542u–t2544u; t2546u "yes, please go ahead and make all changes"): the physical lattice is **one** BCC orbit of the integer grid, the orbit through the origin. These are the sites whose three coordinates are all even or all odd, joined by the integer corner hops (±1,±1,±1).
- This folder gives the exact text changes, a fully patched copy (`main_patched.md`) and a unified diff (`main_vs_patched.diff`). Main, the box paper copy, the earlier note, the plan and every frozen file were left as they were. Nothing was pushed.
- Earlier proposals cited "line 58", "line 524" and "line 544" of a stale box copy (`/workspace/whitepaper/space-ledger-v2.md`, sha256 `53f5050660f3fe11e86e033c5618d82fe639d1b18ed70f0c1a703ec498497944`). On main, those sentences are lines **57**, **523** and **543**, and line 543 now reads differently (it carries the four-taste census sentence).
- Main already carries the four-taste wording. Its line 518 is byte-identical to line 518 of `paper_62_draft_20261109/space-ledger-v2.md.v3.2` (sha256 `1c88f4a3baa756c2074c86a7ac369ef7c28d62682693088f2485eee076db4678`), so that text was applied to main.

## 2. Findings that the edits rest on

### 2.1 The r = 0.05 Wilson term on main is the sum form

The repair adopted in main lines 519 and 588 (gap 2.663×10⁻² E_P at N_s = 32) uses the **sum form** r Σᵢ(1 − cos kᵢ). It does not use a product or BCC-periodic form.

- Frozen `dirac4.py`, sha256 `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff` (copies in `/workspace/chiral_rscan_20261109/src_readonly/` and `/workspace/chiral_wall_count_20261109/src_readonly/`), function `S_step`, **line 66**: `t = np.arcsin(m) + wilson * float(np.sum(1.0 - np.cos(k)))`. Its docstring, line 57, names it: "A Wilson mass m_W = r sum_i (1 - cos k_i)".
- The chain operator `U_slab` passes `wilson=wilson_mass` to that `S_step`: `/workspace/chiral_wall_count_20261109/run_chiral_wall_count.py`, sha256 `aa5d0cf86a660594a04aa4157b2dff90fe7a0cac9341406d2bbdae30e1eb2c2c`, lines 184–195.
- The r-scan uses `U_slab` with `wilson_mass=r`: `/workspace/chiral_rscan_20261109/run_rscan.py`, sha256 `489bf6902b7145bcbb8aeb2b4cf9ff2f87ad48bc383ebc9f87890db2d9136880`, line 79 (`omega_abs_only`). It defines the 41³ grid at lines 193–197, `linspace(-π,π,41)`, which excludes |k| < 0.3 around the origin only. The r = 0.05 runs are `run_low_r.py` (`8c6c6ab5…`), `run_low_r_continue.py` (`4b57bcb7…`), `run_low_r_continue2.py` (`45dcba16…`) and `run_low_r_followup.py` (`ed72b2cb0d39225ef7ac4d1e8cf693867d272b57afabf3d482a41f54f8a6ca80`). Each one checks the frozen sha `f71c782e…` before it runs.
- The numbers are in `/workspace/chiral_rscan_20261109/results_low_r_followup.json`, sha256 `0f16b0811f88bb105ed299015b5d1d6864ecba2e0afb7697c56f00e0408533f4`: `results/0.05/by_Ns/32/interior41/omega_min` = 0.026625477907575197 and `results/0.05/by_Ns/16/interior41/omega_min` = 0.027790346055109307.
- `VERIFY.md` (`/workspace/L0_canonical_20261109/VERIFY.md`, sha256 `02945be65e529feb5d7cd10b70e566e3d49e3ab474dc0dec86098348be0ce179`) agrees. Line 34: the sum form breaks π(1,1,0) invariance, with t = 0 at Γ, 4r = 0.2 at the edge copies, 2r = 0.1 at the faces and 6r = 0.3 at the corners. Line 59: "standard Wilson 0.027790 and 0.026625 (the adopted 2.663×10⁻²)". Line 70: the r = 0.05 chain moves about 0.0022 of the norm to each other orbit, because the axis hops of length 1 leave a BCC sublattice.

On one BCC orbit, this term is not a lattice term. Every number derived from it is withdrawn below. No number is replaced.

### 2.2 The twelve "edge zeros" are Γ on one orbit

- `VERIFY.md` lines 13–16: the symbol is invariant under π(1,1,0) and its permutations, and π(1,1,0) is a reciprocal vector of the hop lattice. The primitive zone has volume 2π³, so the cube [−π,π]³ is four primitive zones. U(π,π,0) = U(Γ) to 6.83×10⁻¹⁶.
- `VERIFY.md` lines 30–33: the invariance residual is 3.51×10⁻¹⁶ on the three generators and 8.01×10⁻¹⁶ over all twelve sign patterns. U at the twelve two-π labels equals U(Γ) to 6.83×10⁻¹⁶, for the four-layer cycle and for the chain at N_s = 8. The 27 labels form two classes, Γ and H, and H has gap π/2 − φ = 0.17079632679489665 at φ = 1.4.
- `VERIFY.md` line 45: one primitive cell (V = 2π³) has **1** massless point. Line 46: the four cones arise only when the cube is read as the zone of a dense ℤ³ grid with four tastes.

### 2.3 Checks run for this edit set (read-only, single thread, under one second)

Script `one_bcc_checks.py` (sha256 `f6418b4157adaad4dfa19538a1a8370563a7187c1c8f94ee5bbfbfc81ed075a8`), output `one_bcc_checks_out.json` (sha256 `34142225576a79a1eb8ed678a9902294b3460702e86bfca9ae413aebdd61fd2f`). Both are in this folder. The script calls the existing frozen `dirac4.py` (`f71c782e…`) and the `qca` stack (`dw.py` `769833f0…` → `dirac4s.py` `4db41fe7…` → `qca/dirac4.py` `9f01ea8f…` → `sym.py` `7b1bbafd…`). It evaluates 20 random k (seed 20261112) under the three shifts π(1,1,0), π(1,0,1) and π(0,1,1). It fits nothing.

| Check | Result |
|---|---|
| C1. Sum-form t = 0.05 Σ(1−cos kᵢ) at Γ, (π,π,0), (π,0,0), (π,π,π) | 0, 0.2, 0.1, 0.3 |
| C2. max ‖U_cycle(k+G) − U_cycle(k)‖, frozen `dirac4.py`, r = 0 / r = 0.05 | 1.12×10⁻¹⁵ / 0.2998 |
| C2′. ‖U(π,π,0) − U(Γ)‖, r = 0 / r = 0.05 | 6.83×10⁻¹⁶ / 0.389 |
| C3. max shift difference, qca 4-tick cycle `periodS` (m = 0, φ = 1.4) and chain `floq` (N_s = 4, b = 0.2) | 1.12×10⁻¹⁵ and 1.12×10⁻¹⁵ |
| C4. qca `dist_gamma((π,π,0))` | 0.0, so (π,π,0) is in the Γ-image exclusion set |

### 2.4 Which numbers on main stay, and which go

**These stay without a new run.** They come from the unrepaired, π(1,1,0)-periodic rule, or their exclusion already removes exactly the Γ images of one orbit.

- Table `tab:dirac4` (main lines 558–564), 0.217 / 0.262 / 0.232 / 0.167 / 0.082 / 0.035. They come from `global_min` with `dist_gamma` in `qca/dirac4.py` (`9f01ea8f…`, lines 19–34), and the official V5 v2 census reproduced them (`/workspace/L0_V4V5_runs_20261111/v5v2_official/results.json`, sha256 `ca6793ea0f2a245c556aabcd65373313fc751902cfb799ea962256e22d212708`; 0.08212694658054251 at φ = 1.4, with the argmin 1.936 from the nearest Γ image). So 0.082 is an interior gap.
- c₀(φ = 1.4) = 0.98911 (the Γ cone slope 0.98910736, `VERIFY.md` line 37) and the light speeds in the table.
- The r = 0 chain global-search gaps 0.058 / 0.046 / 0.034 / 0.022 at N_s = 16 (`qca/gscan_0.1.txt` `acfb869d…`, `gscan_0.15.txt` `51c36455…`, `gscan_0.2.txt` `75f4c677…`, `gscan_0.25.txt` `75a4224d…`). These are the outputs of `qca/dw_gscan.py` (`5bf6af5d089fd17dbe922f335855e9bf961dc731be4025b591e3e0ff16bf938e`), which excludes 0.3 around the even-sum Γ images through `dist_gamma` at line 11. The argmins are interior points.
- The bulk (ring) gap 0.0331 (`qca/ring.txt`; `qca/RESULTS.md` line 175), and line 624's "0.082 to 0.034".
- The residual masses, chirality, localisation and roundness of the chain, the 0.9855 speed, and the b ≥ 0.3 end mode near (π/2,π/2,±π/2) with its requirement b ≲ 0.25 (`qca/RESULTS.md` line 174). That point is not a Γ image.
- The exactness and roundness numbers of lines 520, 521, 581 and 590. They need a lattice label only (§3).

**These are withdrawn, because they are tied to the sum-form Wilson term (§2.1).** All of them are in main lines 519 and 588: the adopted 2.663×10⁻² E_P (N_s = 32) and 2.779×10⁻² (N_s = 16) on the interior 41³ grid; the r = 0.1 minimum 2.004×10⁻² and the 1.10 gate 2.2044×10⁻²; "20.8% above"; 3.2×10¹⁷ GeV and 2.5×10¹³ times the LHC reach; "one third (1/3.0)"; "0.81 of the bulk"; "1.33 times"; the r = 1/3 plateau 3.25×10⁻³ and "about eight times"; the N_s = 12 dip 2.739×10⁻³; the 1/N and 1/N² fits 0.025461 (15.5%) and 0.026237 (19.0%); and the 0.030 E_P crossing.

**These are relabelled, because they are tied to the four-taste reading.** Lines 518, 543, 552, 572, 588 and 616: "four cones", "four decoupled BCC orbits" as physical, "three distinct momenta (twelve sign labels)" as massless doublers, "not a global minimum while r = 0", and "two-π points excluded" read as a miss.

## 3. Line-by-line edits

Text in each "current" block is quoted verbatim from main (sha256 `e86ef5c3…`). Text in each "proposed" block is the full replacement line, exactly as it appears in `main_patched.md`. 14 lines change. No lines are added or removed, so the line numbers are the same in both files.

### 3.1 Line 57

**Current (main line 57):**

```text
**Refinement: an organized, rigid grid.** We take the nodes to form an organized, rigid, cube-like network: the body-centred cubic (BCC) grid with 8 links per node, used in the simulations of this paper. The nodes are fixed in place; they do not move or fluctuate. A regular grid has preferred directions and could in principle pick out a preferred frame. However, link-only path sums on this grid leave a direction dependence of $c$ only at order $(E/E_P)^2$ (Sec. 6.1), far below current bounds. A random, causal-set-like arrangement is excluded in this model (Sec. 7.3).
```

**Proposed:**

```text
**Refinement: an organized, rigid grid.** We take the nodes to form an organized, rigid, cube-like network: the body-centred cubic (BCC) grid with 8 links per node (one BCC orbit of the integer cubic grid: the sites whose three coordinates are all even or all odd, joined by the corner links $(\pm1,\pm1,\pm1)$), used in the simulations of this paper. The nodes are fixed in place; they do not move or fluctuate. A regular grid has preferred directions and could in principle pick out a preferred frame. However, link-only path sums on this grid leave a direction dependence of $c$ only at order $(E/E_P)^2$ (Sec. 6.1), far below current bounds. A random, causal-set-like arrangement is excluded in this model (Sec. 7.3).
```

**Reason and source.** §1.2 clarification. States which lattice the BCC grid is: one orbit of the integer cubic grid, with integer corner hops. Choice by Edmond Ying (chat t2542u–t2544u, t2546u); VERIFY.md lines 7, 63.

### 3.2 Line 518

**Current (main line 518):**

```text
- **Doublers.** The 8 corner links are $h\in\{(\pm1,\pm1,\pm1)\}$ in units of $a/2$, so $\sum_h \exp(ik\cdot h)=8\prod_i\cos(k_i a/2)$. In the cube this distinguishes three classes among the momenta with each $k_i\in\{0,\pm\pi\}$: faces, with one component at $\pm\pi$ (6 points); edges, with two components at $\pm\pi$ (12 points); and corners, with three (8 points); together with $\Gamma$, $1+6+12+8=27$. This is the four-taste cubic-grid rule: the grid is $\mathbb{Z}^3$, the diagonal hops $h=(\pm1,\pm1,\pm1)$ split it into four decoupled BCC orbits, at $r=0$ there are four cones — $\Gamma$ plus the three two-$\pi$ momenta, one per taste — and the cube $[-\pi,\pi]^3$ is four times the primitive $2\pi^3$ zone. The raw hop sum vanishes identically on the six planes $k_i=\pm\pi$, but the zero set is not those planes: on $k_x=\pi$ the hop symbol has $|\mathbf{n}|^2=1-\cos^2 k_y\cos^2 k_z$, so $\mathbf{n}=0$ only at isolated points, and the Wilson layer leaves a frequency zero only at those isolated points with $u=+1$. A census of the 27 points at $\varphi=1.4$ finds three distinct momenta (twelve sign labels) — the $\Gamma$ cone on the other three tastes — and none of the 6 faces and none of the 8 corners (the label count $12/12/0/0$ as edge / one-$\pi$ face / corner, with $\Gamma$ itself massless). That census, 0 of 6 faces and 0 of 8 corners, is the evidence that the zeros are not the union of the planes. An identity of the hop symbol, $u^2+|\mathbf{n}|^2=1$ (both signs $\varepsilon$), splits the would-be zeros into two families, which can be enumerated rather than sampled: family 1 is these 27 isolated $n=0$ points, and family 2 is the surface $u=0$ (hence $|\mathbf{n}|=1$), which includes lines on which $u$ vanishes identically. The twelve edge zeros are a set of measure zero in the Brillouin zone, so a uniform or random global search misses them. Without the Wilson layer, or without alternating the handedness, further zero modes remain.
```

**Proposed:**

```text
- **Doublers.** The 8 corner links are $h\in\{(\pm1,\pm1,\pm1)\}$ in integer units of $a/2$, and $k$ is measured in radians per $a/2$, so $\sum_h \exp(ik\cdot h)=8\prod_i\cos k_i$ and every symbol below is $2\pi$-periodic in each $k_i$. The cores occupy one BCC orbit of this integer grid, the orbit through the origin: the sites whose three coordinates are all even or all odd. The other three orbits of $\mathbb{Z}^3$ are not part of the ledger. The reciprocal lattice of this orbit is the set of momenta $\pi g$ with $g$ an integer triple of even sum, so $\pi(1,1,0)$ and its permutations are reciprocal lattice vectors, and the cube $[-\pi,\pi]^3$ covers the primitive zone, of volume $2\pi^3$, four times. In the cube there are 27 labels with each $k_i\in\{0,\pm\pi\}$: $\Gamma$; faces, with one component at $\pm\pi$ (6 labels); edges, with two components at $\pm\pi$ (12 labels); and corners, with three (8 labels); $1+6+12+8=27$. On the one-orbit lattice these 27 labels are only two points. The twelve edge labels $(\pm\pi,\pm\pi,0)$, $(\pm\pi,0,\pm\pi)$ and $(0,\pm\pi,\pm\pi)$ differ from $\Gamma$ by reciprocal lattice vectors, so they are $\Gamma$ itself: the symbol is invariant under $\pi(1,1,0)$ and its permutations, and the cycle $U$ at the twelve edge labels equals $U(\Gamma)$ to $7\times10^{-16}$. The 6 faces and the 8 corners are likewise one point, which we call $H$. The raw hop sum vanishes identically on the six planes $k_i=\pm\pi$, but the zero set is not those planes: on $k_x=\pi$ the hop symbol has $|\mathbf{n}|^2=1-\cos^2 k_y\cos^2 k_z$, so $\mathbf{n}=0$ only at isolated points, and the Wilson layer leaves a frequency zero only at those isolated points with $u=+1$. These are $\Gamma$ and the twelve edge labels, that is, $\Gamma$ alone. $H$ has $u=-1$ and is gapped, with gap $\pi/2-\varphi\approx 0.171$ at $\varphi=1.4$. A census of the 27 labels at $\varphi=1.4$ confirms this: frequency zeros at $\Gamma$ and the twelve edge labels, and none at the 6 faces or the 8 corners. An identity of the hop symbol, $u^2+|\mathbf{n}|^2=1$ (both signs $\varepsilon$), splits the would-be zeros into two families, which can be enumerated rather than sampled: family 1 is these 27 isolated $\mathbf{n}=0$ labels, and family 2 is the surface $u=0$ (hence $|\mathbf{n}|=1$), which includes lines on which $u$ vanishes identically. Without the Wilson layer, or without alternating the handedness, further zero modes remain.
```

**Reason and source.** Replaces the four-taste reading (ℤ³ split into four physical orbits, four cones, the cube as four physical zones, twelve edge zeros as extra points a search can miss) with the one-orbit reading, and fixes the units sentence: with integer hops and k in radians per a/2 the hop sum is 8∏cos kᵢ, not 8∏cos(kᵢa/2), which matches the symbol in line 525 (cᵢ = cos kᵢ). Sources: VERIFY.md lines 7, 13–18 (integer hops, 2π³ primitive zone, cube = four zones, π(1,1,0) reciprocal), 30–33 (invariance 3.51e−16 / 8.01e−16; U at the twelve labels = U(Γ) to 6.83e−16; two classes; H gap π/2−φ = 0.17079632679489665 at φ = 1.4), 45 (one massless point per primitive cell). The isolated-zero, |n|² and two-family sentences are kept from main. The census sentence keeps main's 0-of-6 / 0-of-8 result and reads the twelve labels as Γ.

### 3.3 Line 519

**Current (main line 519):**

```text
- **Gap versus speed.** The smallest doubler gap and the low-energy light speed trade off against each other (Table \ref{tab:dirac4}, Figure \ref{fig:dirac4}). At $\varphi\approx 1.4$ the *reference* gap in that trade-off is about $0.08\,E_P\approx 10^{18}$ GeV, roughly $10^{14}$ times the reach of the LHC. The adopted repaired gap, $\approx 2.66\times10^{-2}\,E_P$, is one third of this reference (see Doublers and bulk, under Chiral modes from internal component chains).
```

**Proposed:**

```text
- **Gap versus speed.** The smallest doubler gap and the low-energy light speed trade off against each other (Table \ref{tab:dirac4}, Figure \ref{fig:dirac4}). At $\varphi\approx 1.4$ the smallest doubler gap is about $0.08\,E_P\approx 10^{18}$ GeV, roughly $10^{14}$ times the reach of the LHC. On the one-orbit lattice this gap needs no repair, because the twelve edge labels with two components at $\pm\pi$ are $\Gamma$ (see Doublers, above).
```

**Reason and source.** Withdraws the 'adopted repaired gap ≈ 2.66e−2 E_P'. That number comes from a chain with the sum-form Wilson term r∑(1−cos kᵢ), r = 0.05 (frozen dirac4.py f71c782e… line 66), which is not a term of the one-orbit rule (VERIFY.md lines 34, 59, 70). The 0.08 E_P value is the interior gap of the unrepaired rule (V5 v2 census 0.08212694658054251 at φ = 1.4, argmin 1.936 from the nearest Γ image), so it stays, now named as the smallest doubler gap rather than a 'reference'.

### 3.4 Line 520

**Current (main line 520):**

```text
- **Roundness.** The direction spread of the group speed falls as $(ka)^2$ (fitted slope 1.96–2.01 for masses 0, 0.3 and 0.6 in lattice units), with a spread of about $4\times10^{-4}$ to $6\times10^{-4}$ at $ka = 0.025$. Smooth packets are round to 0.7% at $\sigma = 8$ cores.
```

**Proposed:**

```text
- **Roundness.** The direction spread of the group speed falls as $|k|^2$ (fitted slope 1.96–2.01 for masses 0, 0.3 and 0.6 in lattice units), with a spread of about $4\times10^{-4}$ to $6\times10^{-4}$ at $|k| = 0.025$. Smooth packets are round to 0.7% at $\sigma = 8$ grid steps of $a/2$. These packets were run on the full cubic grid, where a Gaussian puts one quarter of its weight on each of the four BCC orbits; this rule never couples the orbits, so each run is four decoupled one-orbit packets whose centres differ by one grid step.
```

**Reason and source.** Units and lattice labelling only, no number changed. k is in radians per a/2 (line 523), so 'ka' is replaced by |k|. The Gaussian packets of qca/dirac4_checks.py (4e316d98…, lines 28–35) sit on the full N³ cubic grid and put 0.2500 of the norm on each orbit; with the integer corner hops the orbits do not couple (leak ~1e−32 at r = 0). VERIFY.md lines 68, 70.

### 3.5 Line 521

**Current (main line 521):**

```text
- **Exactness.** In real-space runs ($48^3$ cores, 24 ticks), unitarity holds to $7\times10^{-16}$, the probability outside the one-hop light cone is exactly zero, total probability is conserved to $10^{-15}$, and running backward restores the initial state to $4\times10^{-16}$. The largest group speed equals the low-energy light speed.
```

**Proposed:**

```text
- **Exactness.** In real-space runs (a periodic $48^3$ cubic grid, 24 ticks, started from a point source, which occupies one orbit of $48^3/4$ cores), unitarity holds to $7\times10^{-16}$, the probability outside the one-hop light cone is exactly zero, total probability is conserved to $10^{-15}$, and running backward restores the initial state to $4\times10^{-16}$. The largest group speed equals the low-energy light speed.
```

**Reason and source.** Lattice labelling only. The exactness test in qca/dirac4_checks.py (lines 14–23) starts from a point source at the origin on N = 48, which occupies one orbit (VERIFY.md line 68). An even N keeps the four orbits separate on the torus, so the orbit has N³/4 sites. No number changed.

### 3.6 Line 523

**Current (main line 523):**

```text
**Formal update rule (Hypothesis).** *State.* Each core $x$ on the BCC grid carries $\psi(x)=(\psi_R(x),\psi_L(x))^{T}\in\mathbb{C}^2\oplus\mathbb{C}^2$, a right- and a left-handed Weyl pair. The ledger Hilbert space is $\mathcal{H}=\ell^2(\mathrm{BCC})\otimes\mathbb{C}^4$. We use $\tau_a$ for Pauli matrices acting on the $(R,L)$ label and $\sigma_a$ for Pauli matrices acting inside each Weyl spinor. *Links.* The 8 corner links are $h\in\{(\pm1,\pm1,\pm1)\}$ in units of $a/2$, with $T_h\psi(x)=\psi(x-h)$. Since every layer is translation invariant, we give it at wavevector $k$ (the Fourier symbol of $\sum_h T_h\otimes M_h$).
```

**Proposed:**

```text
**Formal update rule (Hypothesis).** *State.* Each core $x$ on the BCC grid carries $\psi(x)=(\psi_R(x),\psi_L(x))^{T}\in\mathbb{C}^2\oplus\mathbb{C}^2$, a right- and a left-handed Weyl pair. The ledger Hilbert space is $\mathcal{H}=\ell^2(\mathrm{BCC})\otimes\mathbb{C}^4$. We use $\tau_a$ for Pauli matrices acting on the $(R,L)$ label and $\sigma_a$ for Pauli matrices acting inside each Weyl spinor. *Links.* The 8 corner links are $h\in\{(\pm1,\pm1,\pm1)\}$ in integer units of $a/2$, with $T_h\psi(x)=\psi(x-h)$, and $k$ is measured in radians per $a/2$, so every symbol below is $2\pi$-periodic in each $k_i$. The cores occupy one BCC orbit of this integer grid, the sites whose three coordinates are all even or all odd. Then $\pi(1,1,0)$ and its permutations are reciprocal lattice vectors, the momenta $(\pm\pi,\pm\pi,0)$ are the point $\Gamma$, and the cube $[-\pi,\pi]^3$ covers the primitive zone, of volume $2\pi^3$, four times. Since every layer is translation invariant, we give it at wavevector $k$ (the Fourier symbol of $\sum_h T_h\otimes M_h$).
```

**Reason and source.** The units sentence fix (the 'Links' sentence the earlier note cited as 'line 524' of a stale copy; on main it is in line 523). Wording from REASON_L1_1_one_BCC.md §6, with T_h kept. VERIFY.md lines 7, 13–18.

### 3.7 Line 543

**Current (main line 543):**

```text
*Low-energy limit.* With $\omega$ taken per layer ($e^{-4i\omega}$ = eigenvalue of $U_k$), the lowest band is $\omega^2\simeq\omega_0^2+c_0^2|k|^2$. This is the Dirac equation with $\omega_0=\tfrac12\arcsin m$ and $c_0(\varphi=1.4)=0.98911$, which is direction independent to $10^{-6}$ at this order. Besides $\Gamma$, a census at $\varphi=1.4$ finds three distinct momenta (twelve sign labels), the edges with two components at $\pm\pi$ (see Doublers, above).
```

**Proposed:**

```text
*Low-energy limit.* With $\omega$ taken per layer ($e^{-4i\omega}$ = eigenvalue of $U_k$), the lowest band is $\omega^2\simeq\omega_0^2+c_0^2|k|^2$. This is the Dirac equation with $\omega_0=\tfrac12\arcsin m$ and $c_0(\varphi=1.4)=0.98911$, which is direction independent to $10^{-6}$ at this order. At the tabulated values $0.5\le\varphi\le1.5$, a census finds no zero-frequency point other than $k=0$ (up to reciprocal lattice vectors): the twelve edge labels with two components at $\pm\pi$ are $\Gamma$ itself on the one-orbit lattice (see Doublers, above). At $\varphi=\pi/2$ the doublers return.
```

**Reason and source.** The k = 0 clarification ('up to reciprocal lattice vectors'), applied to main's text, which no longer says 'the only zero-frequency point is k = 0'. The range is limited to the tabulated φ, because that is what the census covers (V5 v2 census results.json ca6793ea…; table in REASON r2 §5). φ = π/2 is the table's '0 (doublers return)' row. c₀ = 0.98911 is kept: Γ cone slope 0.98910736 (VERIFY.md line 37).

### 3.8 Line 552

**Current (main line 552):**

```text
\caption{Four-component node with Wilson layer: smallest doubler gap and low-energy light speed versus the Wilson angle $\varphi$ (gap per tick in units of $E_P \approx 1.22\times10^{19}$ GeV; speed in units of the hop rate $\ell_P/t_P$). The tabulated gaps are for a search that does not evaluate the twelve edge points with two components at $\pm\pi$; at $\varphi=1.4$ the tabulated $0.082$ is the reference gap.}
```

**Proposed:**

```text
\caption{Four-component node with Wilson layer: smallest doubler gap and low-energy light speed versus the Wilson angle $\varphi$ (gap per tick in units of $E_P \approx 1.22\times10^{19}$ GeV; speed in units of the hop rate $\ell_P/t_P$). The tabulated gaps are the smallest frequency found outside a neighbourhood of radius 0.3 of every reciprocal lattice vector $\pi g$ ($g$ an integer triple of even sum). On the one-orbit lattice each such neighbourhood is a neighbourhood of $\Gamma$, so the twelve edge labels with two components at $\pm\pi$, which are $\Gamma$, are excluded as $\Gamma$ and not as doublers. At $\varphi=1.4$ the tabulated $0.082$ is the smallest doubler gap of the rule.}
```

**Reason and source.** The tabulated values come from global_min with dist_gamma in qca/dirac4.py (9f01ea8f…, lines 19–34: 0.3 exclusion around πg with sum(g) even, 300 Nelder–Mead starts), and the V5 v2 census reproduced them (results.json ca6793ea…). They stay. Only the four-taste reading of the exclusion changes. 'Reference gap' is dropped because no repaired gap is adopted.

### 3.9 Line 572

**Current (main line 572):**

```text
\caption{Four-component node. Left: lowest frequency per tick ($m = 0$, units of $E_P$) along a path through the doubler points for single-step and alternating rules without a Wilson layer, a non-alternating rule with one, and the alternating rule with the mirrored Wilson layer at $\varphi = 0.8$ and $1.4$. At $\varphi=1.4$ a census still finds three distinct momenta (twelve sign labels) besides $\Gamma$, the edges with two components at $\pm\pi$; a path that does not pass through those points will not show them. Right: smallest doubler gap (global search) and low-energy light speed versus the Wilson angle $\varphi$; as on the left, a search that does not evaluate those twelve edges is not a global minimum while $r=0$.}
```

**Proposed:**

```text
\caption{Four-component node. Left: lowest frequency per tick ($m = 0$, units of $E_P$) along a path through the doubler points for single-step and alternating rules without a Wilson layer, a non-alternating rule with one, and the alternating rule with the mirrored Wilson layer at $\varphi = 0.8$ and $1.4$. The twelve edge labels with two components at $\pm\pi$ are zero-frequency labels of the cube, but on the one-orbit lattice they are $\Gamma$ itself, not doublers. Right: smallest doubler gap (global search, as in Table \ref{tab:dirac4}) and low-energy light speed versus the Wilson angle $\varphi$.}
```

**Reason and source.** Same change as lines 518 and 552: the twelve labels are Γ, so the 'not a global minimum while r = 0' qualifier no longer applies. The figure image is not changed.

### 3.10 Line 581

**Current (main line 581):**

```text
- *Narrow packets ($\sigma = 4$ cores) remain about 6% non-round; roundness is good only for features much larger than a node.*
```

**Proposed:**

```text
- *Narrow packets ($\sigma = 4$ grid steps of $a/2$, run on the full cubic grid as above) remain about 6% non-round; roundness is good only for features much larger than a node.*
```

**Reason and source.** Same labelling as line 520 (σ = 4 packet of qca/dirac4_checks.py, four decoupled orbit copies). No number changed.

### 3.11 Line 588

**Current (main line 588):**

```text
- **Doublers and bulk.** By global search, the smallest doubler gap at $N_s=16$ is 0.058, 0.046, 0.034 and 0.022 $E_P$ for $b=0.1, 0.15, 0.2, 0.25$; at $b=0.2$ this is about $4\times10^{17}$ GeV. Those four values are global-search values. The search did not evaluate the twelve edge points with two components at $\pm\pi$, namely $(\pm\pi,\pm\pi,0)$, $(\pm\pi,0,\pm\pi)$ and $(0,\pm\pi,\pm\pi)$; while $r=0$ those three distinct momenta (twelve sign labels) are exactly massless, so none of the four numbers is a global minimum. The bulk (interior-component) gap at $b=0.2$ is 0.033 $E_P$. The $4N_s$ chain alone does not lift those three cones. The same chain with a Wilson term of mass $r=0.05$ does lift them, and $\Gamma$ stays massless. After that repair the adopted smallest gap is the zone-interior $41^3$ minimum $2.663\times10^{-2}\,E_P$ at $N_s=32$ (the smallest $|\omega|$ on the $41^3$ boundary-inclusive grid $\mathrm{linspace}(-\pi,\pi,41)$, excluding $|k|<0.3$ of $\Gamma$), which is $20.8\%$ above $1.10$ times the $r=0.1$ minimum $2.004\times10^{-2}\,E_P$ at $N_s=32$ (that $r=0.1$ minimum was on the $u=0$ surface; $1.10\times 2.004\times10^{-2}=2.2044\times10^{-2}$). In the paper’s units this adopted gap is $3.2\times10^{17}$ GeV, or $2.5\times10^{13}$ times the LHC reach (13.4 orders); it is one third ($1/3.0$) of the $0.08\,E_P$ reference at $\varphi\approx 1.4$, $0.81$ of the $0.033\,E_P$ bulk (interior-component) gap, $1.33$ times the $r=0.1$ minimum, and about eight times the $r=1/3$ plateau of $3.25\times10^{-3}\,E_P$ ($1/25$ of the $0.08$ reference, 12.5 orders). The $N_s=12$ value $2.739\times10^{-3}\,E_P$ is a single-sample dip at $r=1/3$ ($1/29$ of the reference, 12.4 orders), not the quoted $r=1/3$ cost. The binding locus is that zone-interior $41^3$ grid, evaluated only at $N_s=16$ ($2.779\times10^{-2}$) and $N_s=32$ ($2.663\times10^{-2}$), so the $N_s$ extrapolation is labelled “assumed $1/N$, two points”: a $1/N$ fit through those two points gives $\omega_\infty=0.025461$ ($15.5\%$ above the same $0.022044$ threshold) and a $1/N^2$ fit gives $0.026237$ ($19.0\%$). A three-point fit of the $u=0$ surface is not binding. The zone-interior $41^3$ grid is the finest census used, not a proof that no narrower zone-interior feature remains. There is no optimality claim: a crossing of the two-$\pi$ gap with the $u=0$ surface near $0.030\,E_P$ is an upper bound, not the achieved minimum; the zone-interior sample is the limiting locus and has not been mapped below $r=0.05$. The two-family split of $u^2+|\mathbf{n}|^2=1$ made the zeros enumerable; earlier misses came from sampling the bulk and from extrapolating power laws below their fit range. For $b\geq 0.3$ a doubler end mode survives near $k=(\pi/2,\pi/2,\pm\pi/2)$ with a gap that falls exponentially with $N_s$, so the construction still requires $b\lesssim 0.25$.
```

**Proposed:**

```text
- **Doublers and bulk.** By global search, the smallest doubler gap at $N_s=16$ is 0.058, 0.046, 0.034 and 0.022 $E_P$ for $b=0.1, 0.15, 0.2, 0.25$; at $b=0.2$ this is about $4\times10^{17}$ GeV. The search excludes a neighbourhood of radius 0.3 of every reciprocal lattice vector $\pi g$ ($g$ an integer triple of even sum). On the one-orbit lattice each of these is a neighbourhood of $\Gamma$: the twelve edge labels with two components at $\pm\pi$, namely $(\pm\pi,\pm\pi,0)$, $(\pm\pi,0,\pm\pi)$ and $(0,\pm\pi,\pm\pi)$, are $\Gamma$ itself, and the chain's cycle there equals its cycle at $\Gamma$. Excluding them therefore removes no doubler. The four values come from 60 random starts each and are not a proof that no lower point remains. The bulk (interior-component) gap at $b=0.2$ is 0.033 $E_P$. The chain needs no Wilson repair on the one-orbit lattice. The sum-form Wilson term $r\sum_i(1-\cos k_i)$ is not a term of the one-orbit rule: its axis hops of length one leave the orbit, and it is not invariant under the reciprocal lattice vector $\pi(1,1,0)$. Gaps computed with that term are therefore not quoted here. The identity $u^2+|\mathbf{n}|^2=1$ still splits the would-be zeros into two families that can be enumerated rather than sampled. For $b\geq 0.3$ a doubler end mode survives near $k=(\pi/2,\pi/2,\pm\pi/2)$ with a gap that falls exponentially with $N_s$. That point differs from $\Gamma$ by a vector that is not a reciprocal lattice vector, so it is a genuine doubler of the one-orbit rule, and the construction still requires $b\lesssim 0.25$.
```

**Reason and source.** Withdraws the whole r = 0.05 Wilson repair (adopted 2.663e−2 E_P at N_s = 32 on the interior 41³ grid, 2.779e−2 at N_s = 16, the r = 0.1 minimum 2.004e−2, the 1.10 gate 2.2044e−2, the r = 1/3 plateau 3.25e−3, the N_s = 12 dip 2.739e−3, the 1/N and 1/N² fits 0.025461 and 0.026237, the 0.030 crossing, and every ratio built from them). Every one of these was computed with wilson_mass > 0 in frozen dirac4.py (f71c782e…) S_step, line 66: t = arcsin(m) + wilson·∑(1 − cos kᵢ), the sum form. This goes through U_slab in chiral_wall_count_20261109/run_chiral_wall_count.py (aa5d0cf8…, lines 184–195) and the chiral_rscan_20261109 r-scan (run_rscan.py 489bf690…; run_low_r*.py; results_low_r_followup.json 0f16b081…: interior41 0.026625477907575197 at N_s = 32, 0.027790346055109307 at N_s = 16). That term breaks π(1,1,0) invariance (VERIFY.md line 34; check C2 here: max shift difference 0.2998 at r = 0.05, against 1.1e−15 at r = 0) and couples the orbits (VERIFY.md line 70). Kept without a new run: the r = 0 global-search values (qca/gscan_0.1/0.15/0.2/0.25.txt, from qca/dw_gscan.py 5bf6af5d…, which uses dist_gamma, the even-sum Γ-image exclusion), the 4e17 GeV conversion, the ring bulk gap 0.0331 (qca/ring.txt; qca/RESULTS.md line 175), the two-family identity, and the b ≥ 0.3 end mode and b ≲ 0.25 requirement (qca/RESULTS.md line 174). The chain stack is π(1,1,0)-periodic at r = 0 (check C3 here, 1.1e−15). The orbit-preservation reason for the b ≥ 0.3 point is that P = (π/2,π/2,π/2) − Γ is not of the form πg with g even-sum (REASON r2 §7). The sentence about 'earlier misses' is dropped, because on one orbit the twelve labels were never missed doublers.

### 3.12 Line 590

**Current (main line 590):**

```text
- **Exactness.** In a real-space run ($40^3$ nodes, $N_s = 8$, 24 ticks), unitarity holds to $9\times10^{-16}$, the probability outside the one-hop light cone is exactly zero, probability is conserved to $2\times10^{-15}$, and reversal restores the initial state to $2\times10^{-15}$.
```

**Proposed:**

```text
- **Exactness.** In a real-space run (a periodic $40^3$ cubic grid, started from a point source, which occupies one orbit of $40^3/4$ nodes; $N_s = 8$, 24 ticks), unitarity holds to $9\times10^{-16}$, the probability outside the one-hop light cone is exactly zero, probability is conserved to $2\times10^{-15}$, and reversal restores the initial state to $2\times10^{-15}$.
```

**Reason and source.** Lattice labelling only. qca/dw_real.py (276c5fdc…, lines 3, 8) uses a point source at the origin on N = 40, which occupies one orbit (VERIFY.md line 68). No number changed.

### 3.13 Line 616

**Current (main line 616):**

```text
\caption{Internal component chain. (a) Residual end-mode mass versus $N_s$ with the predicted $(\tan m_0/\tan b)^{N_s}$ (dashed). (b) Chirality $|\gamma_5|$ and end-component weight versus $|k|$. (c) Localisation length in components. (d) Global-search gap versus $b$ (two-$\pi$ points excluded) (solid: global search; dashed: at the surviving special point only). The global-search curve in (d) is a search that does not evaluate the twelve edge points with two components at $\pm\pi$, so those values are not global minima while $r=0$. The axis label in the existing figure image still says “smallest”; that image is not regenerated here.}
```

**Proposed:**

```text
\caption{Internal component chain. (a) Residual end-mode mass versus $N_s$ with the predicted $(\tan m_0/\tan b)^{N_s}$ (dashed). (b) Chirality $|\gamma_5|$ and end-component weight versus $|k|$. (c) Localisation length in components. (d) Global-search gap versus $b$, excluding a neighbourhood of every reciprocal lattice vector, that is, of $\Gamma$ on the one-orbit lattice (solid: global search; dashed: at the surviving special point only). The twelve edge labels with two components at $\pm\pi$ are $\Gamma$ on the one-orbit lattice, so excluding them removes no doubler, and the solid curve is the smallest gap found by that search, as the axis label of the image says.}
```

**Reason and source.** Same reason as line 588 (r = 0 dw_gscan values with the dist_gamma exclusion). The figure image is not changed.

### 3.14 Line 623

**Current (main line 623):**

```text
- *The chiral end mode holds only for $|k| \lesssim 0.25$, i.e. wavelengths above about 25 nodes; this covers all observed particles but not Planck-scale excitations.*
```

**Proposed:**

```text
- *The chiral end mode holds only for $|k| \lesssim 0.25$, i.e. wavelengths above about 25 grid steps of $a/2$; this covers all observed particles but not Planck-scale excitations.*
```

**Reason and source.** Units only. |k| is in radians per a/2, and 2π/0.25 ≈ 25.1 grid steps of a/2. 'Nodes' would count cores of the orbit, which is a different number. No number changed.

## 4. Lines checked and left unchanged

- **Line 104** ("The extra doubler modes … remain open (open problem 11)"), **516**, **536** ("of order one near the doubler momenta"), **564** (the φ = π/2 row) and **576** (c and the 1.1% / 1.5% offsets). None of these depends on the number of orbits.
- **Line 624**, "*The doubler gap at b=0.2 is reduced from about 0.082 to 0.034 E_P …*". Both numbers are interior gaps of the unrepaired, periodic rules (§2.4).
- **Line 762**, "four species per Brillouin zone". This is an earlier generation reading of the BCC rule's doublers. It is consistent with a single BCC zone, but its source run was not traced for this edit set.
- **Line 1243**, the zone boundary of the BCC grid is direction-dependent. This is true of one BCC orbit (a truncated-octahedron zone).

## 5. Open: not resolved here without a new run or a decision by Edmond

1. **Which length is ℓ_P.** Line 381 sets the node spacing a ≈ ℓ_P. With hops (±1,±1,±1) in units of a/2, the nearest-neighbour distance is a√3/2 and the cubic cell is a. Any conversion from k to E/E_P can depend on which of these is ℓ_P. Examples are line 651 (the cubic test), line 704 (Test 3, ξ₁) and line 1253 ("(E/E_P)²/18"). Gaps quoted as frequencies per tick in E_P are not affected. These lines are not changed.
2. **Figure images.** `dirac4.png` and `domainwall.png` are not regenerated. Only their captions change. The caption of line 572 assumes that the right-hand panel of `dirac4.png` used the same search as the table. That plotting script was not traced.
3. **Roundness of a single one-orbit packet.** The 0.7% (σ = 8) and about 6% (σ = 4) values are from full-cubic-grid runs that hold four decoupled orbit copies (lines 520 and 581 now say so). A one-orbit-only packet run was not made.
4. **The searches are not proofs.** The table and the chain gaps are the smallest values found by the stated searches. Lines 552 and 588 say so. They do not claim optimality.
5. **Periodic (product-form) Wilson.** No repair is proposed for `dirac4`, because none is needed on one orbit. `VERIFY.md` line 59 records only a cheap evaluation of the product form at one locus (0.03328 at N_s = 16, 0.03250 at N_s = 32). That is not a census, and it is not used here.
6. **OP4.** H, P and P′ remain genuine points of one BCC zone, and the plan's "both rules" L1.1 requirement for OP4 stays open. This edit set does not touch the plan. It does not decide the §3.4 floor, "4/4", or what P is for.
7. **The L1 exit gate.** It is still Edmond's decision whether the existing V5 v2 census counts as the "census re-run for the chosen rule".
8. **Not edited.** The plan's frozen-conventions line (`h = (±1,±1,±1)/2`) and the frozen `dirac4.py` docstring (line 6, `(+-1,+-1,+-1)/2`). The paper PDF on main is not rebuilt here.

## 6. Files in this folder

- `PAPER_EDITS_one_BCC.md` and `PAPER_EDITS_one_BCC.pdf`, this document.
- `main_patched.md`: main's `space-ledger-v2.md` with the 14 lines of §3 replaced. sha256 `8cbb94ec481b3332f074ea028505478dd2d576a8b5d60915f072b653ab6aad70`.
- `main_vs_patched.diff`: a unified diff from main to `main_patched.md`. sha256 `ab2f323d2e71c05c4efe9a06c6d69eb268e036e130eb8cb3b46072d9274430dd`. `patch` applies it cleanly to a copy of main (`e86ef5c3…`), and the result is byte-identical to `main_patched.md`.
- `one_bcc_checks.py` and `one_bcc_checks_out.json`, the checks of §2.3.
- `SHA256SUMS`, covering all of the above.
