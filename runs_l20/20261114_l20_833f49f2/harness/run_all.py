#!/usr/bin/env python3
"""Orchestrator: runs S0, C1, C2, C3, C4, C5 once each under meter.py (no retries). Caps D8: 1 thread, no GPU,
512 MiB sampled tree RSS (meter kill), 600 s wall each for S0 and C1-C4, 900 s for C5, 2400 s total wall
(each ceiling = min(per-check cap, remaining total)), 64 MiB output (checked after each check). S0 failure stops the run."""
import sys
sys.dont_write_bytecode = True
import os, json, time, subprocess
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HD = os.path.join(RUN, "harness")
OUTD, LOGD = os.path.join(RUN, "out"), os.path.join(RUN, "logs")
CHECKS = [("S0", 600), ("C1", 600), ("C2", 600), ("C3", 600), ("C4", 600), ("C5", 900)]
TOTAL, RSS = 2400.0, 512 * 2 ** 20
OUTCAP = 64 * 2 ** 20


def dsize(p):
    t = 0
    for r, _, fs in os.walk(p):
        for f in fs:
            t += os.path.getsize(os.path.join(r, f))
    return t


env = dict(os.environ, L20_SCORE="1", L20_OUT=OUTD, L20_METER="1", CUDA_VISIBLE_DEVICES="", PYTHONDONTWRITEBYTECODE="1")
t0 = time.time()
summary = dict(start_local=time.strftime("%Y-%m-%d %H:%M:%S %Z"), checks=[])
for name, cap in CHECKS:
    rem = TOTAL - (time.time() - t0)
    if rem <= 0:
        summary["checks"].append(dict(check=name, status="not started: total wall cap reached")); continue
    ceil = min(cap, rem)
    cmd = [sys.executable, os.path.join(HD, "meter.py"), name, os.path.join(LOGD, f"{name}.log"),
           os.path.join(LOGD, f"{name}_meter.json"), str(ceil), str(RSS), sys.executable, "-B", os.path.join(HD, "l20_score.py"), name]
    rc = subprocess.run(cmd, env=env).returncode
    m = json.load(open(os.path.join(LOGD, f"{name}_meter.json")))
    out_ok = os.path.exists(os.path.join(OUTD, f"{name}.json"))
    lab = json.load(open(os.path.join(OUTD, f"{name}.json"))).get("label") if out_ok else None
    size = dsize(RUN)
    summary["checks"].append(dict(check=name, ceiling_s=ceil, exit_code=m["exit_code"], killed=m["killed"],
                                  wall_s=m["wall_s"], cpu_s=m["cpu_s"], peak_tree_rss_MiB=m["peak_tree_rss_MiB"],
                                  label=lab, run_folder_bytes_after=size))
    print(name, lab, m["exit_code"], m["killed"], round(m["wall_s"], 1), flush=True)
    if size > OUTCAP:
        summary["stopped"] = "output cap 64 MiB exceeded"; break
    if name == "S0" and lab != "PASS":
        summary["stopped"] = "S0 did not pass; no physics check scored"; break
summary["total_wall_s"] = time.time() - t0
summary["end_local"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
json.dump(summary, open(os.path.join(LOGD, "run_summary.json"), "w"), indent=1)
