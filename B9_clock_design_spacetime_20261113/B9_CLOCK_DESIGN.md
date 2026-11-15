# B9 clock-factor check under $B_m$: Mercury's $46.3''$, redshift, and $\gamma$

Quantized Space-Ledger. Written 13 November 2026 (America/New_York) by `spacetime` (the Grok bot) at Edmond Ying's request. Edmond's widget answer of 1:59 PM ET, 13 November 2026, asked to settle B9 before closing L1.5, starting with the $46.3''$ double-count check under $B_m$. The same answer records $B_m$ as the L1.5b rule by a later closure note citing the comparison run, with no rerun of L1.5b; that note is later, not this work.

This document is a design for Edmond's review. It runs nothing scored, and it edits no paper, plan, repository, Sheet or archived record. Nothing in it may be run until Edmond names its sha256 in his own words. Open decisions are numbered K1, K2, … and listed in the sidecar `B9_OPEN_DECISIONS.md` in this folder; this document decides none of them. Where a default is written below, it is a proposal that applies only if Edmond gives no other value.

## 0. Why this check exists

L1.5b has already been run. The recorded verdict is the $A_m$ run (folder `20261112_l15ab_865660ec_56a19950`, SHA256SUMS sha256

`7ba13b2f4df104e67058c88359b554683b218ccb3a19f95dc772c0dbddd7b01a`). A later $B_m$ comparison run (folder `20261113_l15b_Bm_comparison`, SHA256SUMS sha256

`328ffb90b9ceb79dd5f3d14178f27d562a493f420a03a7f7e605501a011fd671`) passed every L1.5b gate as a would-be result, and measured the rest-clock factor. Under $B_m$, with Edmond's option (b) identifying $g = f^2 = s$ and $s = (1+\ell)^{-1/2}$, both the rest clock and the massless speed scale by $s = f^2$, not by the paper's clock factor $f$. None of the L1.5b gates catches this, because a uniform factor cancels in the ratios they check.

B9 is the remaining clock-factor question: the paper's clock $f$ and light $f^2$, versus $B_m$'s common factor $f^2$. Edmond's picture is that light carries a small load like electrons, so all excitations slow by one common factor at a fixed tick, which fits line 842 and the measured $B_m$ ratios, and clashes with §6.13. Line 1024 calls own-load clock slowing a double count, and quotes $46.3''$ for Mercury. This design pre-registers a check of that number under $B_m$, together with the gravitational-redshift and $\gamma$ (light-bending / Shapiro) consequences of changing the clock factor.

## 1. Sources (read-only)

**Paper.** Read from `main` of `edmondying-hash/spacetime-ledger` at commit

`fdf3e72a958bdc0e3ed95f06530b0a96d0a45d61`,

file `space-ledger-v2.md`, sha256

`ce22701ca6e5e2dfa143ab43a6062e80025c1afeba5137f7e271c239bc75555c`.

Not from `/workspace/whitepaper`. Line numbers below are those of that file (YAML header included). Distant-observer labelling of light-cost lines entered in commit

`5a00f03e6dd0849a77f189ff3f4836d3dd216e16`

and is present on this `main`.

**L1.5b and $B_m$.** Design `L1_5b_RUN_DESIGN.md`, sha256

`56a19950375881c16815aebe7f219eba0dc06c0c4c7c39e7efbdde3859b5073f`,

folder `/workspace/L1_5ab_design_spacetime_20261112/`, with its open-decisions sidecar. $A_m$ record and $B_m$ comparison hashes as in §0. Post-run note of the comparison run: $w_0^{B_m}/w_0^{\mathrm{OFF}} = s = f^2$ to $2.7\times10^{-51}$, and $c_0^{B_m}/c_0^{\mathrm{OFF}}$ is the same $s$ at every $\varphi$.

**Original $46.3''$ computation.** Box folder `/workspace/mercury/`:

- `RESULTS.md`

  `f6723571b6aed238d5f779a1d607be6c6901073083577e2fa47ae02be3919557`
- `field.py`

  `a3b7a951ec4c31bfbecdd88f3febd1d71290636f5e6ecd7c643b20f3f31b3b87`
- `orbit.py`

  `a0cefdf9d6816ec30fdbff352fd7e527eb4cbe2ee7f0ffc203c6cf9a09d402ad`
- `orbit.json`

  `64d13f100821979984c7148cdaf7bbd90f5fe415cad4650f92b90f269fd52499`
- `beta.json`

  `841f7240568b60008c3fca13219725171289871c3b1284fd0e3d49071ed28930`

A related 1PN table, used by paper §6.12, is `results.json`, sha256

`0ea1da674234c172b90f1434d802af5a210405b523ffe4a0fa2cc1258db28d60`,

and `run.log`, sha256

`f569a468f71e8acb93d5ab2ec9b0735ffa17ed73d7fdeb141db62be51abf8394`.

## 2. Verbatim paper lines (with numbers)

**Line 842 (equivalence; §6.11).** “Any such mechanism, including the load proposal above, must satisfy the **equivalence principle**: all excitations, massive or massless, must respond identically to the local graph geometry. In ledger language, gravity must change the ‘network’ itself (effective routing cost and tick rate), not apply species-dependent per-hop processing.”

**Line 860 (clock versus light, after commit `5a00f03e`).** Static clocks run at $d\tau/dt \approx 1 - GM/(rc^2)$, “the gravitational time dilation that the GPS system corrects for.” In ledger terms, $n(r)$ is the extra routing cost and $d\tau/dt$ is the reduced tick rate. “Here $c/n$ is the speed a distant observer infers (a coordinate delay); light measured locally still moves one node per tick at $c$ (Secs. 1 and 6.1).”

**Line 961 (§6.12, $f = e^{-U}$ and light cost $e^{2U}$).** “With load share $\rho = 1 - e^{-U}$, light's share of each link is then $f = e^{-U}$ with no separate rule, and its cost per link is $1/(1-\rho)^2 = e^{2U}$, a delay seen by a distant observer (local light speed is still one hop per tick).”

**Lines 1022–1024 (§6.13, including the $46.3''$ sentence).** “In the ledger, a node's clock rate is relayed from neighbour to neighbour. If each hop *compounds* the slowdown (multiplies it) instead of adding to it, the time part of the metric comes out as $g_{00} = e^{-2U}$. Expanded to second order, that gives the post-Newtonian parameter $\beta = 1$; with $\gamma = 1$ from the space part, the perihelion advance, which scales as $(2 + 2\gamma - \beta)/3$, matches general relativity. In simulation, the compounding relay gave $\beta = 1.00$, $\gamma = 1.000$ and $42.98''$ per century ($42.91''$ from the orbit integration; the $0.07''$ gap is a read-out artifact of the osculating perihelion vector), against the observed $\approx 43''$. An additive relay gave $\beta = 0.5$ and $50.1''$, so it is ruled out. Letting a node's own load also slow its clock double-counts the effect ($46.3''$).”

**Line 1020 (nearby, §6.12 update).** With load diffusion and $f = e^{-U}$, “a geodesic orbit test gives $42.98''$/cy and $\beta = 1.000$ … assuming the equivalence principle for matter.”

**Line 898.** The net GPS satellite clock-rate offset, about 38 µs per day, is listed among the calibration checks.

**Line 897.** Cassini tracking: $\gamma - 1 = (2.1 \pm 2.3)\times 10^{-5}$ (Bertotti, Iess and Tortora, 2003).

## 3. What $46.3''$ was, quantitatively

The number in line 1024 comes from `/workspace/mercury/`, not from a packet run (the later `gpu/mercury` compact-packet job is a different test and did not produce $46.3''$).

Method, from `RESULTS.md` and `field.py` / `orbit.py`. Radial shells around a point mass, $G=c=1$. The potential $\psi$ solves $\nabla^2\psi = 4\pi G\rho + a|\nabla\psi|^2$, with $a$ the self-load weight on field energy. Each shell adds a load step $\delta_n$, relayed inward from infinity ($\sum\Delta = U = GM/rc^2$).

- Additive clock (A): rate $= 1 - \sum\delta$, $g_{00} = \mathrm{rate}^2$.
- Multiplicative clock (B): $\mathrm{rate}_n = \mathrm{rate}_{n-1}(1-\delta_n)\to e^{-U}$, $g_{00} = \mathrm{rate}^2$.
- Link stretch is relayed the same way; $\gamma$ is fitted from it.
- $\beta$ is fitted from $g_{00} = 1 - 2U + 2\beta U^2$ at $GM = 10^{-3}$ to $8\times10^{-3}$ and extrapolated. $U$ in the fit uses the asymptotic (Kepler) mass.

Archived table (`RESULTS.md`):

| Rule | $a$ | $\beta$ | $\gamma$ | orbit / formula ($''$/cy) |
|---|---|---|---|---|
| A additive | 0 | 0.50 | 1.000 | 50.10 / 50.14 |
| A + Newtonian field energy | $-1/2$ | 0.27 | 1.000 | 53.45 / 53.48 |
| B multiplicative | 0 | 1.00 | 1.000 | 42.91 / 42.98 |
| B + Newtonian field energy | $-1/2$ | 0.77 | 1.000 | 46.28 / 46.33 |
| GR | | 1 | 1 | 42.98 |

`orbit.json` stores the precise values used in the orbit step: $\beta = 0.766$, $\gamma = 1$, formula $46.333188$, orbit $46.277592$; and for B with $a=0$: formula $42.980694$, orbit $42.912294$. Constants in `orbit.py`: $GM = 1.32712440018\times10^{20}$, $c = 299792458$, $a = 5.7909050\times10^{10}$ m, $e = 0.205630$, year $= 3.15576\times10^7$ s, 100-year DOP853 endpoint of the osculating Laplace–Runge–Lenz vector, $10^{-13}$ relative tolerance. The $0.07''$ orbit-versus-formula gap is the read-out artifact named in line 1024. The §6.12 table in `results.json` used a different integrator window (200 orbits, linear fit to the Runge–Lenz direction) and got $42.9837$ against formula $42.9820$.

**What “double count” means here.** It is a second-order ($\beta$) effect, not a change of the linear clock factor. Compounding already supplies the nonlinearity $\beta = 1$ and the GR perihelion $42.98''$. Booking the field's own energy as extra load ($a = -1/2$, the Newtonian weight) on top of compounding shifts $\beta$ to about $0.77$ and the perihelion to $46.3''$. The linear redshift and $\gamma$ stay at their GR values in that table. This is a different mechanism from “the rest clock slows by $f^2$ rather than $f$.” Identifying the two is an open decision (K2), not a consequence of the L1.5b measurement.

## 4. The $B_m$ fact, and why a gravity map is a choice

Under uniform load, L1.5b measured:

- Rule P (paper split): rest clock slows by $f$, light speed by $f^2$; continuum $E = f\sqrt{\omega_0^2 + f^2 c_0^2 k^2}$ with $g_{00} = f^2$, $g_{ij} = f^{-2}$.
- Rule $A_m$: the whole cycle, including the rest frequency, slows by $f^2$. Dimensionless ratios are unchanged (a pure time rescaling).
- Rule $B_m$, option (b): $s = f^2 = (1+\ell)^{-1/2}$. Every rotation angle, including the mass angle, is scaled by $s$. Measured: $w_0$ and $c_0$ both scale by $s$. Local $c = w_0$ ratios stay put, which is Edmond's “light speed is constant.” Dimensionless moving-clock residuals do change (T4b, record only).

Uniform load is not a gravitational potential. Promoting $s$ to a static $s(r)$, and naming $U$ in $f = e^{-U}$, requires a map from congestion to the metric. That map is Edmond's (K1). This design does not choose it. It pre-registers named identifications, computes each one, and scores each against the same measured targets. Two calibration readings must be kept apart:

- **Hold the paper's $U$ fixed** (the $U$ already used so that $\Phi = e^{-U}$ and a light cost $e^{2U}$ give Kepler plus GR light delay). Then changing only the clock to $e^{-2U}$ doubles the linear redshift and also doubles the linear $g_{00}$ term, so Keplerian orbits would be wrong at leading order.
- **Recalibrate $G$ (or the load-to-$U$ scale) so that Newtonian orbits stay right**, then predict redshift, $\gamma$ and perihelion. This is the comparison that experimental bounds test, because Pound–Rebka, GPS and Gravity Probe A compare clocks to a potential taken from orbits.

A factor-of-two redshift appears in the first reading and not, at linear order, in the second.

## 5. Named identifications (none is selected)

Notation. $\Phi$ is the static clock rate $d\tau/dt$. In a static metric $\Phi = \sqrt{-g_{00}}$. $U_{\mathrm{phys}} = GM/(rc^2)$ with $G$ from Kepler. The first-order redshift to infinity is $z = 1/\Phi - 1$, and $\alpha$ is defined by $z = (1+\alpha)U_{\mathrm{phys}}$, so GR has $\alpha = 0$. Light's distant-observer index is $n = c/c_{\mathrm{coord}}$. In isotropic PPN form, $g_{00} = -(1-2U+2\beta U^2)$, $g_{ij} = (1+2\gamma U)\delta_{ij}$, $n \approx 1+(1+\gamma)U$, limb deflection $2(1+\gamma)GM/(c^2 b)$, Shapiro scale $(1+\gamma)/2$, perihelion factor $(2+2\gamma-\beta)/3$. Local light remains one hop per tick in every case (line 860; commit `5a00f03e`). Nodes stay rigid; any extra light delay is routing cost, not stretch, unless a case says otherwise.

**I1. Paper split, no self-load (control).** $\Phi = e^{-U}$, $g_{00} = -e^{-2U}$, distant light cost $e^{2U}$, $U = U_{\mathrm{phys}}$. Then $\beta = 1$, $\gamma = 1$, $\alpha = 0$, perihelion formula $42.980694''$/cy. This is §6.13 compounding and L1.5b rule P's gravity reading.

**I2. Paper own-load, the $46.3''$ (control).** I1 plus field-energy source $a = -1/2$. Use the archived orbit inputs $\beta = 0.766$, $\gamma = 1$. Formula $46.333188''$/cy, 100-year orbit $46.277592''$/cy. Linear $\alpha = 0$, $\gamma = 1$. This is line 1024's double count. It is not produced by changing $f$ to $f^2$ at linear order.

**I3. $B_m$ common factor, rigid nodes, $G$ to Kepler (complete-theory reading of Edmond's picture).** Clock and coordinate light speed share one factor $s(r)$; local $c$ is constant; no leftover load-first split. Calibrate $s$ so that linear $g_{00} = -2U_{\mathrm{phys}}$: then $s = \Phi = e^{-U_{\mathrm{phys}}}$, $g_{00} = -e^{-2U_{\mathrm{phys}}}$ ($\beta = 1$), $n = e^{U_{\mathrm{phys}}}$ ($\gamma = 0$), $\alpha = 0$, perihelion factor $1/3$, formula $14.326898''$/cy, limb deflection $0.8756$ arcsec, Shapiro half of GR. Redshift matches Gravity Probe A at linear order; light delay and perihelion do not.

**I4. $B_m$ common factor, paper $U$ held fixed (diagnostic, Kepler not retuned).** Take the paper's $U$ and set $\Phi = s = e^{-2U}$ and $c_{\mathrm{coord}} = s\,c$. Then $\Phi \approx 1-2U$, $\alpha = 1$ (redshift twice GR), and linear $g_{00} \approx -(1-4U)$ (Newtonian gravity twice as strong for the same $G$). This is not a complete theory: orbits would already fail at leading order. It is recorded because the question “does $B_m$'s clock at $f^2$ double the redshift?” is this diagnostic. After the retuning that restores Kepler, the linear redshift returns to I3 and the surviving clash is $\gamma = 0$.

**I5. $B_m$ clock at $e^{-2U_{\mathrm{load}}}$ with the paper's load-first routing $e^{2U_{\mathrm{load}}}$ still on, $G$ to Kepler.** After retuning, $U_{\mathrm{load}} = U_{\mathrm{phys}}/2$, so $\Phi = e^{-U_{\mathrm{phys}}}$ (redshift GR) and a leftover routing $e^{U_{\mathrm{phys}}}$ can restore $n = e^{2U_{\mathrm{phys}}}$, $\gamma = 1$, $\beta = 1$, perihelion $42.98''$. This is a relabelling of I1. It is available only if the load-first split remains on. Edmond's words (“light carries a small load … all excitations slow by one common factor”) point away from a leftover split; whether I5 is live is K1.

**I6. Identifying $B_m$'s clock-at-$f^2$ with own-load I2.** This would predict $46.3''$, $\gamma = 1$, $\alpha = 0$. The L1.5b measurement does not imply this: $f^2$ versus $f$ is a linear clock factor, $46.3''$ is a $\beta$ shift from booking field energy. K2 decides whether I6 is used at all. The design reports I2 as a control in every case, and reports I6 only if Edmond identifies them.

Analytic first-order expectation, if K1 is I3 (the complete-theory common-factor map): B9 is already settled by Cassini and by Mercury, without a new orbit, because $\gamma = 0$ and $14.33''$/cy lie far outside the measured windows, while redshift does not fail. If K1 is I4 and one refuses to retune $G$, redshift alone fails Gravity Probe A ($\alpha = 1$ against $1.4\times10^{-4}$). If K1 is I5, the check is consistent with GR after relabelling and does not by itself settle B9. If K2 is yes (I6), the check reproduces $46.3''$ and fails the perihelion target by about $3.3''$, with redshift and $\gamma$ intact. This document does not pick among those readings.

## 6. Pre-registered method

CPU only, one thread, no GPU. Machine: the agent's box, or sparky if Edmond names it (K7). Not bigbang. One attempt per step, no retry, no re-score, no fitting to targets. Failures and vacuous outcomes stay on record. Resources (wall, CPU, peak RSS) are recorded for every step.

**S0. Pre-flight.** Hash this folder against `SHA256SUMS`. Confirm Python, NumPy and SciPy `solve_ivp` (DOP853) import. Recompute the three formula values of §5 (I1, I2 with $\beta=0.766$, I3) and require agreement to $10^{-9}$ relative with $42.98069352502894$, $46.333187619981196$, $14.326897841676312$ (these are `orbit.py`'s formula at the archived constants). Time one 5-year GR orbit as a cost check, not as a perihelion number (a 5-year endpoint is a poor read-out; disclosed probe: $44.16''$/cy). Any S0 failure stops the run; later steps are not started.

**S1. Control C1 (I1).** Formula at $\beta=\gamma=1$, and a 100-year DOP853 endpoint using the archived `orbit.py` constants and acceleration, with no change of integrator, tolerances, or read-out. Record also, as a labelled cross-check and not a replacement of the endpoint, a 200-orbit linear fit to the Runge–Lenz direction as in the §6.12 table.

**S2. Control C2 (I2).** The same two orbit methods at the archived $\beta = 0.766$, $\gamma = 1$. This reproduces the paper's $46.3''$ under the own-load case. `field.py` is not rerun (K11); $\beta = 0.766$ is taken from `orbit.json` so the comparison is like with like.

**S3. Analytic table for I1–I5 (and I6 only if K2 says so).** For each identification, report $\Phi(U)$, $g_{00}$, $\beta$, $\gamma$, $\alpha$, $z/z_{\mathrm{GR}}$ at linear order, perihelion formula, limb deflection, Shapiro scale relative to GR, and whether each measured target in §7 is met. No parameter is adjusted to meet a target. $G$ retuning, when a case uses it, is the single Newtonian calibration already named in the paper (line 961: “$G$ needs one calibration”), not a fit to redshift, $\gamma$, or perihelion.

**S4. Numeric orbits for identifications that have a definite $(\beta,\gamma)$.** I1 and I2 are S1–S2. I3 is $(\beta,\gamma)=(1,0)$; I5, if live, is $(1,1)$ and must match I1; I4 has no consistent 1PN orbit until $G$ is retuned, and is reported as UNINFORMATIVE for the orbit column, with the redshift and Kepler-diagnostic numbers still recorded. Same integrator as S1.

**S5. Records.** `result.json` (all numbers, hashes, resources, verdicts), a plain table, and resource logs. Nothing is written to the repo, the paper, or the L1.5 run folders.

The analytic table (S3) is the result that can settle B9. The numeric orbits are a cross-check of the $(2+2\gamma-\beta)/3$ factor, as in line 1024, not a new source of $\beta$ or $\gamma$.

## 7. Targets, pass/fail, and UNINFORMATIVE

Measured targets (defaults; K4–K6 may replace them). Theory or simulation values (GR's $42.98''$, the paper's own toys) are reference values, not targets, except where a target and the GR figure happen to coincide numerically.

- **Perihelion.** $42.98 \pm 0.04''$/cy, as named in the request that commissioned this design. Also recorded, not as the default gate: the paper's Clemence residual $42.56 \pm 0.94''$/cy (line 1002) and Will, *Living Rev. Relativ.* 17, 4 (2014), Table 4, $|\beta-1| < 8\times10^{-5}$ when $\gamma$ is taken from Cassini. A case meets the default perihelion target iff its formula value (and, when scored, its 100-year orbit after adding back the pre-registered $0.07''$ read-out offset of I1, or using the linear-fit method) lies in $[42.94, 43.02]$.
- **Redshift.** Gravity Probe A: $|\alpha| \le 1.4\times10^{-4}$ (Vessot, Levine et al., *Phys. Rev. Lett.* 45, 2081 (1980); the figure named in the request). Pound–Rebka / Pound–Snider and the paper's GPS 38 µs/day offset are recorded. A case meets the redshift target iff its linear $\alpha$ lies in that window. (I4's $\alpha = 1$ does not; I3's $\alpha = 0$ does.)
- **$\gamma$ (light bending and Shapiro).** Cassini: $\gamma-1 = (2.1 \pm 2.3)\times10^{-5}$ (paper line 897). A case meets the $\gamma$ target iff its predicted $\gamma$ lies in that interval. (I3's $\gamma = 0$ does not.)

An identification is reported as meeting all three, or as missing named ones, with the residuals. This design does not close B9 and does not choose the map.

**Controls must pass before any $B_m$ identification is scored.**

- C1 formula within $10^{-9}$ relative of $42.98069352502894$. C1 100-year endpoint within $0.02''$ of the archived $42.91229380880339$. C1 linear-fit cross-check, if it runs, within $0.02''$ of $42.982$.
- C2 formula within $10^{-9}$ relative of $46.333187619981196$. C2 100-year endpoint within $0.02''$ of the archived $46.27759181715892$.

**UNINFORMATIVE, and no $B_m$ scoring, if:** a control misses its tolerance; DOP853 or SciPy is missing (no substitute integrator); an orbit's Newtonian energy has a secular drift above $10^{-6}$ per century in the 1PN run's recorded Newtonian energy, or the Newtonian-only check at $(\beta,\gamma)$ unused (the archived code's `prec(0,0)` analogue) is not consistent with $0$ to $0.01''$/cy; a case has no well-defined $(\beta,\gamma)$ after the rules of §5 (the orbit column only; analytic $\alpha$ and the Kepler diagnostic are still reported). Vacuous rows are marked UNINFORMATIVE, not passed and not failed.

No fitting. The archived $\beta = 0.766$ is an input for C2, not a fitted output of this run. A disclosed, non-run linear fit of archived `beta.json` $\beta$ versus $1/GM$ has intercept $0.9986$ ($a=0$) and $0.7681$ ($a=-1/2$); those intercepts are not used to change C2.

## 8. Resources and proposed caps (K7, K8)

Disclosed unscored probes on the agent's box, 13 November 2026, each under one minute, no gate numbers taken from them except as already archived:

- Analytic formulae for I1, I2, I3: $0.0001$ s wall, about 9 MiB.
- Read-only intercept of archived `beta.json`, as above: $0.016$ s.
- A 5-year GR orbit (timing only): $0.19$ s wall; projected 100-year orbit about $4$ s each. Peak RSS during the probe, including SciPy import, about 96 MiB.

Expected official cost: S0 a few seconds; S1–S2 and S4 a few 100-year orbits, about $20$–$40$ s wall; S3 negligible; well under one minute, under 128 MiB. Caps, as a proposal: 1 thread, no GPU, 512 MiB peak RSS (meter kill), 2 minutes per step, 10 minutes total wall, 32 MiB output, one attempt per step. Default machine: the box. Not bigbang.

## 9. What this does not do

It does not edit the paper, the plan, or any hashed L1.5 or mercury file. It does not write or push a closure file. It does not rerun L1.5b. It does not treat I3, I4, I5 or I6 as the adopted map. It does not authorise a production run until Edmond names this design's sha256.

## 10. Code

`b9_measure.py` in this folder implements S0–S5 with the archived constants, the formula, the 100-year endpoint, the 200-orbit linear-fit cross-check, the analytic table, and resource recording. Its sha256 is in `SHA256SUMS`. In a later run folder it is installed as `harness/b9_measure.py` (same bytes). Running it is not authorised by the existence of this file.

## 11. Approval

Edmond's own message naming the sha256 of this design (the `B9_CLOCK_DESIGN.md` hash in `SHA256SUMS`) is what authorises a scored run of S0–S5 under the caps, together with any K1–K11 values he wishes to set. Until then, nothing scored is run.
