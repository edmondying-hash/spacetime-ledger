# B9 open decisions (sidecar to `B9_CLOCK_DESIGN.md`)

Written 13 November 2026 (America/New_York) by `spacetime`. None of these is decided by the design or by this file. Each item names the design default that applies only if Edmond gives no other value. Edmond's own words decide each item.

- **K1. Map from $B_m$ to a gravitational metric.** The L1.5b run measured a uniform-load fact: under $B_m$ with $s=f^2$, the rest clock and the massless speed both scale by $s$. Which identification in the design's §5 is the gravity map? I3 (common factor, rigid nodes, $G$ calibrated to Kepler: $\gamma=0$, perihelion $14.33''$, redshift GR); I4 (paper $U$ held fixed, no $G$ retuning: linear redshift $2\times$ and Kepler also wrong at leading order); I5 (clock at $e^{-2U_{\mathrm{load}}}$ but the paper's load-first routing left on: relabels to GR after $G$ calibration); some combination; or another map. Default: compute and report I3, I4 and I5; do not treat any one as adopted. Edmond's "light carries a small load … all excitations slow by one common factor" is the verbal content of I3, not of I5.

- **K2. Is the paper's $46.3''$ own-load the same thing as $B_m$'s clock at $f^2$?** The original $46.3''$ is a $\beta$ shift from booking field energy ($a=-1/2$) on top of compounding, with $\gamma=1$ and linear redshift unchanged. $B_m$'s $f^2$ versus $f$ is a linear clock factor. Default: they are different mechanisms; I2 stays a control, not the $B_m$ prediction; I6 is not scored unless Edmond identifies them.

- **K3. If the analytic table already lies far outside the measured windows, is a numeric orbit still required before you settle B9?** Default: still run the short controls C1 and C2 and the analytic table; numeric $B_m$ orbits are a cross-check of $(2+2\gamma-\beta)/3$, not a new source of $\beta$ or $\gamma$. The analytic expectation under I3 can be read without a new run; settling B9 remains yours.

- **K4. Official perihelion target.** The request named $42.98\pm0.04''$/cy. The paper also quotes Clemence's residual $42.56\pm0.94''$/cy and, in the plan, Will (2014) $|\beta-1|<8\times10^{-5}$. Default: gate at $42.98\pm0.04$; record the other two.

- **K5. Official redshift target.** Default: Gravity Probe A $|\alpha|\le1.4\times10^{-4}$ (Vessot et al., 1980). Record Pound–Rebka / Pound–Snider and the paper's GPS 38 µs/day offset.

- **K6. Official $\gamma$ target.** Default: Cassini $\gamma-1=(2.1\pm2.3)\times10^{-5}$ as in paper line 897. A predicted $\gamma$ must lie in that interval to meet the target.

- **K7. Machine.** The agent's box (default) or sparky. Not bigbang, which is occupied with the mass-gap work.

- **K8. Caps.** 1 thread, no GPU, 512 MiB peak RSS, 2 minutes per step, 10 minutes total wall, 32 MiB output, one attempt per step. Expected cost is well under one minute and under 128 MiB.

- **K9. Closure and paper.** No paper edit, no plan edit, and no L1.5 closure note in this work. Recording $B_m$ as the L1.5b rule by a closure note that cites the comparison run (no rerun) is later, as you already said.

- **K10. Approval form.** Your own message naming the sha256 of `B9_CLOCK_DESIGN.md` for a scored run of S0–S5, with values for any of K1–K11 you wish to set.

- **K11. Re-running `field.py`.** Default: no. Control C2 uses the archived $\beta=0.766$ from `orbit.json`, like with like with the $46.28/46.33$ record. A fresh self-load solve would be a new computation, not the original number.
