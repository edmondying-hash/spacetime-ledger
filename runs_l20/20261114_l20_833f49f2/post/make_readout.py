#!/usr/bin/env python3
"""Post-run formatter (written after the checks ran; scores nothing). Reads out/*.json and logs/*_meter.json."""
import sys
sys.dont_write_bytecode = True
import json, os, hashlib
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def sh(p):
    return hashlib.sha256(open(os.path.join(RUN, p), "rb").read()).hexdigest()
def J(p):
    return json.load(open(os.path.join(RUN, p)))
S = J("logs/run_summary.json")
L = []
w = L.append
w("# L2.0 scored run read-out")
w("")
w("Design `L2_0_RUN_DESIGN.md` sha256 `833f49f26418b2267cc0a9b389a46220078b453eebe92cf149145af330077ed9`; design folder SHA256SUMS `ae005712b98eb2263e702cdc5701abfd1fb0e9e0bef102367c40d28dab858edc`; `l20_measure.py` `08e98af5d2936474260f233f85c4b1ef06b4564d6533409f36c34a7bfa5dd516`; `frozen/dirac4.py` `f71c782ed7089680e4c8e2441d12a926de9b8c18b57a9a28253b018ebbab8aff`.")
w("Harness: `harness/l20_score.py` `%s`; `harness/run_all.py` `%s`; `harness/meter.py` `%s`; `harness/IMPLEMENTATION_NOTES.md` `%s`; `harness/PRE_RUN_SHA256SUMS` `%s`." % (
    sh("harness/l20_score.py"), sh("harness/run_all.py"), sh("harness/meter.py"), sh("harness/IMPLEMENTATION_NOTES.md"), sh("harness/PRE_RUN_SHA256SUMS")))
w("Machine: the box. One attempt per check. Defaults D1-D16. Start %s, end %s, total wall %.1f s." % (S["start_local"], S["end_local"], S["total_wall_s"]))
w("")
w("## Resources (meter)")
w("")
w("| Check | Ceiling s | Exit | Killed | Wall s | CPU s | Peak tree RSS MiB |")
w("|---|---|---|---|---|---|---|")
for c in S["checks"]:
    w("| %s | %.0f | %s | %s | %.2f | %.2f | %.1f |" % (c["check"], c["ceiling_s"], c["exit_code"], c["killed"] or "no", c["wall_s"], c["cpu_s"], c["peak_tree_rss_MiB"]))
w("")
w("Run-folder size after last check: %d bytes (cap 64 MiB)." % S["checks"][-1]["run_folder_bytes_after"])
w("")
w("## Gate labels")
w("")
s0 = J("out/S0.json")
w("- **S0**: %s (P0 %s, P1 %s, P2 %s, P3 %s, P4 %s). `out/S0.json` `%s`" % (s0["label"], *[("MET" if s0[p]["ok"] else "NOT MET") for p in ("P0","P1","P2","P3","P4")], sh("out/S0.json")))
c1 = J("out/C1.json")
w("- **C1**: %s. `out/C1.json` `%s`; `out/C1_series.npz` `%s`" % (c1["label"], sh("out/C1.json"), sh("out/C1_series.npz")))
w("  - 5.1 p-norm drift: %s. Failures: %s. S3 quiet-p reported: %s." % (c1["drift_gate"]["label"], c1["drift_gate"]["failures"] or "none", c1.get("S3_quiet_p_reported") or "none"))
w("  - 5.1 L = 32 reruns (edge > 1e-6 at L = 16): %s" % "; ".join("%s %s %s" % (r["seed"], r["state"], r["label"]) for r in c1["drift_L32_reruns"]))
s = c1["search"]
w("  - 5.2 search: %s (%s). n_clear %d, n_grey %d, s_min %.3e, s_max %.3e; on-site n_clear %d, n_grey %d." % (s["label"], s["reason"], s["n_clear"], s["n_grey"], s["s_min"], s["s_max"], s["onsite"]["n_clear"], s["onsite"]["n_grey"]))
w("  - Controls: (1) %s (identity residual %.2e, projection residual %.2e); (2) %s (sigma_z residual %.4f); (3) %s (6^3 n_clear %d n_grey %d; 8^3 n_clear %d n_grey %d)." % (
    "MET" if s["control1_ok"] else "NOT MET", s["identity_residual_maxabs"], s["identity_projection_residual"],
    "MET" if s["control2_ok"] else "NOT MET", s["sigma_z_residual_maxabs"], "MET" if s["control3_ok"] else "NOT MET",
    s["control3"]["6^3"]["n_clear"], s["control3"]["6^3"]["n_grey"], s["control3"]["8^3"]["n_clear"], s["control3"]["8^3"]["n_grey"]))
w("  - Positivity (m(k) >= 0 fallback, no SDP solver): positive complement rays %s; on-site %s." % (s["positive_other_indices"] or "none", s["positive_other_onsite_indices"] or "none"))
c2 = J("out/C2.json")
w("- **C2**: %s. `out/C2.json` `%s`" % (c2["label"], sh("out/C2.json")))
w("  - Q-share cells beyond 3 sigma: %s (%d of %d channel tests; max z %.3f)." % (c2["qshare_failures"] or "none", c2["qshare_n_beyond_3sigma"], c2["n_qshare_channel_tests"], c2["qshare_max_z"]))
w("  - Control (p = 1, p = 4) cells without a > 5 sigma channel at t = 0: %s." % (c2["control_failures"] or "none"))
c3 = J("out/C3.json")
w("- **C3**: %s. Repeat disagreements %d, second-client disagreements %d, server byte differences %d. `out/C3.json` `%s`" % (c3["label"], c3["total_repeat_disagreements"], c3["total_second_client_disagreements"], c3["total_server_differences"], sh("out/C3.json")))
c4 = J("out/C4.json")
w("- **C4**: %s. Q-share cells outside 3 sigma: %s. Control shift > 5 sigma found: p1 %s, p4 %s. `out/C4.json` `%s`" % (c4["label"], c4["qshare_failures"] or "none", c4["control_shift_found"]["p1"], c4["control_shift_found"]["p4"], sh("out/C4.json")))
c5m = [c for c in S["checks"] if c["check"] == "C5"][0]
w("- **C5(a)**: does not pass (read-only audit `L2_0_C5A_AUDIT.md` `423920fe845e26df1871e0e2a5ebc044c780735919c1df1af3c47ecabf683090`, already performed, not rerun).")
if os.path.exists(os.path.join(RUN, "out/C5.json")):
    w("- **C5(b)-(d)**: see out/C5.json")
else:
    w("- **C5(b)**: UNINFORMATIVE. **C5(c)**: UNINFORMATIVE. **C5(d)**: UNINFORMATIVE. Cap trip: meter killed C5 (`%s`, exit %s) at %.2f s wall, sampled tree RSS %.1f MiB > 512 MiB; no `out/C5.json` was written. Log `logs/C5.log` `%s`; meter `logs/C5_meter.json` `%s`." % (c5m["killed"], c5m["exit_code"], c5m["wall_s"], c5m["peak_tree_rss_MiB"], sh("logs/C5.log"), sh("logs/C5_meter.json")))
w("- **C5 overall**: not passed (D10).")
w("")
w("## Diagnostics (not gated)")
w("")
d = c1["diagnostics"]
w("- m = 0.3, seed 20261113, S1, L = 16: drift %s; stepper fault at cycle 1: %s." % ({k: float("%.3g" % v) for k, v in d["m0.3"]["drift"].items()}, d["m0.3"]["stepper_fault"]))
b = d["uniform_load_ON_ruleB"]
w("- Uniform load ON, rule B, s = 0.81, phi = 1.4, m = 0, seed 20261113, S1, L = 16: p = 2 drift at cycle 1 %.3e (> 1e-12, series stopped after cycle 1 by the C1 stepper-fault rule); drift over recorded cycles %s; max |factor eigenphase| %.15f; max unitarity deviation %.2e." % (b["drift"]["2.0"], {k: float("%.3g" % v) for k, v in b["drift"].items()}, b["max_abs_factor_eigenphase"], b["max_unitarity_dev"]))
w("")
w("## UNINFORMATIVE cells")
w("")
w("- C1 5.1: L = 32 reruns of S1 and S3, all five seeds (edge fraction > 1e-6 at L = 32).")
w("- C1 5.2: the search (control 3).")
w("- C2, C3, C4: none.")
w("- C5(b), C5(c), C5(d): all cells (cap trip).")
open(os.path.join(RUN, "READOUT.md"), "w").write("\n".join(L) + "\n")
