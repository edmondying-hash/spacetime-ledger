#!/usr/bin/env python3
# Supplement to b9_measure.py: design items the harness does not implement.
#  mode "sources": §1 / S0 source hashes (paper at pinned commit via `git show`, read-only; mercury files).
#  mode "gates":   §7 control/UNINFORMATIVE gates absent from the harness:
#     (a) C1 200-orbit linear-fit cross-check within 0.02'' of 42.982;
#     (b) secular drift of recorded Newtonian energy <= 1e-6 per century in each 1PN linear-fit run
#         (two-point start/end relative change, scaled to 100 yr; only those two values are recorded);
#     (c) Newtonian-only 100-year endpoint (1PN term removed; same DOP853, rtol 1e-13, atol 1e-3,
#         LRL read-out) consistent with 0 to 0.01''/cy.
# No parameter changes; constants and integrator imported from harness/b9_measure.py.
import hashlib, json, subprocess, sys, time, resource
from pathlib import Path
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here)); sys.dont_write_bytecode = True
mode, out = sys.argv[1], Path(sys.argv[2])
def sha(b): return hashlib.sha256(b).hexdigest()
if mode == "sources":
    repo = "/workspace/spacetime-ledger"; commit = "fdf3e72a958bdc0e3ed95f06530b0a96d0a45d61"
    paper = subprocess.run(["git", "-C", repo, "show", f"{commit}:space-ledger-v2.md"], capture_output=True, check=True).stdout
    exp = {"/workspace/mercury/RESULTS.md": "f6723571b6aed238d5f779a1d607be6c6901073083577e2fa47ae02be3919557",
           "/workspace/mercury/field.py": "a3b7a951ec4c31bfbecdd88f3febd1d71290636f5e6ecd7c643b20f3f31b3b87",
           "/workspace/mercury/orbit.py": "a0cefdf9d6816ec30fdbff352fd7e527eb4cbe2ee7f0ffc203c6cf9a09d402ad",
           "/workspace/mercury/orbit.json": "64d13f100821979984c7148cdaf7bbd90f5fe415cad4650f92b90f269fd52499",
           "/workspace/mercury/beta.json": "841f7240568b60008c3fca13219725171289871c3b1284fd0e3d49071ed28930",
           "/workspace/mercury/results.json": "0ea1da674234c172b90f1434d802af5a210405b523ffe4a0fa2cc1258db28d60",
           "/workspace/mercury/run.log": "f569a468f71e8acb93d5ab2ec9b0735ffa17ed73d7fdeb141db62be51abf8394"}
    rec = {"paper": {"commit": commit, "file": "space-ledger-v2.md", "sha256": sha(paper),
                     "expected": "ce22701ca6e5e2dfa143ab43a6062e80025c1afeba5137f7e271c239bc75555c"}}
    rec["paper"]["match"] = rec["paper"]["sha256"] == rec["paper"]["expected"]
    anc = subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor", "5a00f03e6dd0849a77f189ff3f4836d3dd216e16", commit])
    rec["paper"]["5a00f03e_is_ancestor"] = anc.returncode == 0
    rec["mercury"] = {p: {"sha256": sha(Path(p).read_bytes()), "expected": e, "match": sha(Path(p).read_bytes()) == e} for p, e in exp.items()}
    rec["all_match"] = rec["paper"]["match"] and all(v["match"] for v in rec["mercury"].values())
    (out / "sources.json").write_text(json.dumps(rec, indent=2) + "\n"); print(json.dumps(rec, indent=2)); sys.exit(0)
import numpy as np
from scipy.integrate import solve_ivp
import b9_measure as m
t0 = time.perf_counter()
S1 = json.loads((out / "S1.json").read_text()); S2 = json.loads((out / "S2.json").read_text())
S4 = json.loads((out / "S4.json").read_text()) if (out / "S4.json").exists() else {}
g = {}
fit = S1.get("orbit_200_linear_fit")
g["C1_linear_fit"] = {"value": fit, "ref": 42.982, "abs_diff": None if fit is None else abs(fit - 42.982),
                      "tol": 0.02, "gate": None if fit is None else ("MET" if abs(fit - 42.982) <= 0.02 else "NOT MET")}
period = 2 * np.pi * np.sqrt(m.SEMI**3 / m.GM)
drift = {}
runs = [("S1", S1.get("orbit_200_linear_fit_meta")), ("S2", S2.get("orbit_200_linear_fit_meta"))]
for k, v in (S4.get("results") or {}).items():
    if isinstance(v, dict) and "orbit_200_linear_fit_meta" in v: runs.append(("S4_" + k, v["orbit_200_linear_fit_meta"]))
for k, meta in runs:
    if not meta: drift[k] = {"gate": "UNINFORMATIVE", "reason": "no recorded energy"}; continue
    t_end_yr = meta["n_orbits"] * period / m.YEAR
    per_cy = abs(meta["newton_E_rel_change"]) * 100.0 / t_end_yr
    drift[k] = {"rel_change": meta["newton_E_rel_change"], "span_yr": t_end_yr, "per_century": per_cy,
                "limit": 1e-6, "gate": "MET" if per_cy <= 1e-6 else "NOT MET"}
g["newtonian_energy_drift"] = drift
def newton(t, y):
    r = np.array(y[:2]); v = np.array(y[2:]); R = np.hypot(*r)
    return [*v, *(-m.GM * r / R**3)]
rp = m.SEMI * (1 - m.ECC); vp = np.sqrt(m.GM / m.SEMI * (1 + m.ECC) / (1 - m.ECC))
s = solve_ivp(newton, [0, 100 * m.YEAR], [rp, 0, 0, vp], method="DOP853", rtol=1e-13, atol=1e-3)
val = float(np.degrees(m.lrl_angle(s.y[:2, -1], s.y[2:, -1])) * 3600)
g["newtonian_only_100yr"] = {"value_arcsec_cy": val, "tol": 0.01, "nfev": int(s.nfev), "success": bool(s.success),
                             "gate": "MET" if abs(val) <= 0.01 else "NOT MET"}
ru = resource.getrusage(resource.RUSAGE_SELF)
g["resources"] = {"wall_s": time.perf_counter() - t0, "cpu_s": ru.ru_utime + ru.ru_stime, "peak_rss_mib": ru.ru_maxrss / 1024}
(out / "supplement.json").write_text(json.dumps(g, indent=2) + "\n"); print(json.dumps(g, indent=2))
