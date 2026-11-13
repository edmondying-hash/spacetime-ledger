#!/usr/bin/env python3
"""Run one step as a child process; record wall s, CPU s (self+all waited descendants), peak RSS of the process tree
(sampled 0.2 s), exit code. Threads pinned to 1. Soft per-step ceiling 600 s: if reached the child is killed and the
kill is recorded (no retry). Adapted from L1.2 harness/meter.py (run 20261112_l12_7e09b7c4)."""
import os, sys, time, json, subprocess, resource, threading
step, logpath, resjson = sys.argv[1], sys.argv[2], sys.argv[3]
cmd = sys.argv[4:]
CEIL_S = 600
env = dict(os.environ)
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS","BLIS_NUM_THREADS"):
    env[v] = "1"
env["PYTHONDONTWRITEBYTECODE"] = "1"; env["PYTHONHASHSEED"] = "0"
def tree_rss(root):
    pp = {}; rss = {}
    for d in os.listdir('/proc'):
        if not d.isdigit(): continue
        try:
            with open(f'/proc/{d}/stat') as f: s = f.read()
            ppid = int(s.rsplit(')',1)[1].split()[1]); pp[int(d)] = ppid
            with open(f'/proc/{d}/status') as f:
                for line in f:
                    if line.startswith('VmRSS:'): rss[int(d)] = int(line.split()[1]) * 1024
        except Exception: pass
    tot = 0; stack = [root]; seen = set(); nproc = 0
    while stack:
        p = stack.pop()
        if p in seen: continue
        seen.add(p); tot += rss.get(p, 0); nproc += 1
        stack += [c for c, q in pp.items() if q == p]
    return tot, nproc
peak = [0, 0]; killed = [False]
t0 = time.time()
with open(logpath, 'ab') as log:
    p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env)
    stop = threading.Event()
    def samp():
        while not stop.is_set():
            r, n = tree_rss(p.pid); peak[0] = max(peak[0], r); peak[1] = max(peak[1], n)
            if time.time() - t0 > CEIL_S and p.poll() is None:
                killed[0] = True; p.kill()
            time.sleep(0.2)
    th = threading.Thread(target=samp, daemon=True); th.start()
    rc = p.wait(); stop.set(); th.join()
wall = time.time() - t0
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
out = dict(step=step, cmd=cmd, exit_code=rc, wall_s=wall, cpu_user_s=ru.ru_utime, cpu_sys_s=ru.ru_stime, cpu_s=ru.ru_utime + ru.ru_stime,
           peak_tree_rss_bytes_sampled=peak[0], peak_tree_rss_MiB=peak[0] / 2**20, max_procs_in_tree=peak[1],
           max_single_child_rss_bytes=ru.ru_maxrss * 1024, killed_at_ceiling=killed[0], ceiling_s=CEIL_S,
           start_epoch=t0, end_epoch=t0 + wall, start_local=time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(t0)),
           thread_env={k: env[k] for k in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS")})
json.dump(out, open(resjson, 'w'), indent=1)
print(json.dumps(out)); sys.exit(rc)
