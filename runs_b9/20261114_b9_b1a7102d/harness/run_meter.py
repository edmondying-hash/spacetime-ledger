#!/usr/bin/env python3
# Resource meter for the B9 run (implementation of design §6/§8 caps; not part of the physics).
# Launches one command as a child, 1 thread, pinned to one CPU; polls VmRSS every 20 ms;
# kills on peak RSS > 512 MiB, on any step > 120 s wall (step boundaries = appearance of
# <out>/S*.json files written by b9_measure.py), or on total wall > the remaining budget.
# Usage: run_meter.py <name> <out_dir> <total_budget_s> <log_json> -- cmd ...
import json, os, signal, sys, time, resource
name, out_dir, budget, log = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
cmd = sys.argv[sys.argv.index("--") + 1:]
RSS_CAP_MIB, STEP_CAP_S = 512.0, 120.0
env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1",
           NUMEXPR_NUM_THREADS="1", CUDA_VISIBLE_DEVICES="", PYTHONDONTWRITEBYTECODE="1")
t0 = time.perf_counter(); t0_wall = time.time()
pid = os.fork()
if pid == 0:
    os.sched_setaffinity(0, {0})
    os.execvpe(cmd[0], cmd, env)
peak = 0.0; killed = None; boundaries = []; seen = set(); step_t0 = t0
watch = ["S0.json", "S1.json", "S2.json", "S3.json", "S4.json", "S5.json", "supplement.json"]
while True:
    r = os.wait4(pid, os.WNOHANG)
    if r[0] == pid:
        status, ru = r[1], r[2]; break
    try:
        with open(f"/proc/{pid}/status") as fh:
            for line in fh:
                if line.startswith("VmRSS:"):
                    peak = max(peak, int(line.split()[1]) / 1024.0)
    except FileNotFoundError:
        pass
    now = time.perf_counter()
    for w in watch:
        if w not in seen and os.path.exists(os.path.join(out_dir, w)):
            seen.add(w); boundaries.append({"file": w, "t_s": now - t0, "step_wall_s": now - step_t0}); step_t0 = now
    if killed is None:
        if peak > RSS_CAP_MIB: killed = f"rss_cap {peak:.1f} MiB"
        elif now - step_t0 > STEP_CAP_S: killed = f"step_wall_cap after {boundaries[-1]['file'] if boundaries else 'start'}"
        elif now - t0 > budget: killed = "total_wall_budget"
        if killed: os.kill(pid, signal.SIGKILL)
    time.sleep(0.02)
wall = time.perf_counter() - t0
rec = {"name": name, "cmd": cmd, "start_epoch": t0_wall, "wall_s": wall,
       "cpu_user_s": ru.ru_utime, "cpu_sys_s": ru.ru_stime, "cpu_s": ru.ru_utime + ru.ru_stime,
       "peak_rss_mib_polled": peak, "peak_rss_mib_ru_maxrss": ru.ru_maxrss / 1024.0,
       "exit_code": os.waitstatus_to_exitcode(status), "killed": killed,
       "step_boundaries": boundaries, "affinity": [0], "threads_env": "1", "gpu": "none (CUDA_VISIBLE_DEVICES empty)"}
json.dump(rec, open(log, "w"), indent=2); print(json.dumps(rec, indent=2))
sys.exit(0)
