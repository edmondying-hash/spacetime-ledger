#!/usr/bin/env python3
"""L0' census r1 driver: runs S0-S7 (and the repair round when its condition holds),
each step as a separate process under its own caps (r1 Section 7).
Design: /workspace/L0p_census_design_r1_20261114/L0P_CENSUS_DESIGN_r1.md
sha256 c2673a6426ca5728738c7e7e63871bd26577e8475e9b2819d9980aeccb642fd1
Usage: census.py --mode census|smoke --run-root DIR --code-sums-sha HEX
"""
import os, sys, json, time, signal, hashlib, subprocess, resource, argparse, traceback

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CODE_DIR)
import census_steps as cs

CENSUS_ORDER = ['S0', 'S1', 'S2', 'S4', 'S3', 'S5a', 'S5b', 'S6', 'S7']
REPAIR_ORDER = ['S0', 'S1', 'S2b', 'S4', 'S3', 'S5a', 'S6', 'S7']
TOTAL_CAPS = {'cpu_s': 18180, 'wall_s': 24240, 'rss_mib': 3072, 'out_mib': 193}


def dir_bytes(p):
    t = 0
    for root, _, files in os.walk(p):
        for f in files:
            try:
                t += os.lstat(os.path.join(root, f)).st_size
            except OSError:
                pass
    return t


def vmrss_kb(pid):
    try:
        with open(f'/proc/{pid}/status') as f:
            for line in f:
                if line.startswith('VmRSS:'):
                    return int(line.split()[1])
    except OSError:
        return None
    return None


def log(run_dir, ev):
    ev = dict(ev); ev['time_local'] = time.strftime('%Y-%m-%d %H:%M:%S %Z')
    with open(os.path.join(run_dir, 'run_log.jsonl'), 'a') as f:
        f.write(json.dumps(ev) + '\n')


def run_step(a, run_dir, rnd, step):
    cpu, wall, rss_mib, out_mib = cs.CAPS[rnd][step]
    out_bytes = out_mib * 1024 * 1024
    def limits():
        os.setsid()
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu + 5))
        resource.setrlimit(resource.RLIMIT_FSIZE, (out_bytes, out_bytes))
    env = dict(os.environ)
    env.update({'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1',
                'NUMEXPR_NUM_THREADS': '1', 'PYTHONHASHSEED': '0', 'PYTHONDONTWRITEBYTECODE': '1'})
    errp = os.path.join(run_dir, 'steps', f'{rnd}_{step}.stderr')
    outp = os.path.join(run_dir, 'steps', f'{rnd}_{step}.stdout')
    base = dir_bytes(run_dir)
    t0 = time.time()
    with open(outp, 'w') as fo, open(errp, 'w') as fe:
        p = subprocess.Popen([sys.executable, os.path.join(CODE_DIR, 'census_steps.py'), '--mode', a.mode,
                              '--run-dir', run_dir, '--step', step, '--round', rnd,
                              '--code-sums-sha', a.code_sums_sha],
                             cwd=CODE_DIR, env=env, stdout=fo, stderr=fe, preexec_fn=limits)
        trip = None; peak_rss = 0; last_out = 0.0; out_now = 0
        while True:
            r = os.wait4(p.pid, os.WNOHANG)
            if r[0] != 0:
                status, ru = r[1], r[2]
                break
            rk = vmrss_kb(p.pid)
            if rk:
                peak_rss = max(peak_rss, rk)
                if rk > rss_mib * 1024 and trip is None:
                    trip = f'RSS cap {rss_mib} MiB exceeded ({rk} kB)'
            el = time.time() - t0
            if el > wall and trip is None:
                trip = f'wall cap {wall} s exceeded'
            if time.time() - last_out > 2.0:
                out_now = dir_bytes(run_dir) - base; last_out = time.time()
                if out_now > out_bytes and trip is None:
                    trip = f'output cap {out_mib} MiB exceeded ({out_now} bytes)'
            if trip is not None:
                try:
                    os.killpg(p.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            time.sleep(0.5)
    wall_s = time.time() - t0
    cpu_s = ru.ru_utime + ru.ru_stime
    rc = os.waitstatus_to_exitcode(status)
    if trip is None and rc == -signal.SIGXCPU:
        trip = f'CPU cap {cpu} s exceeded (SIGXCPU)'
    if trip is None and rc == -signal.SIGXFSZ:
        trip = f'output cap {out_mib} MiB exceeded (SIGXFSZ)'
    rec = {'round': rnd, 'step': step, 'caps': {'cpu_s': cpu, 'wall_s': wall, 'rss_mib': rss_mib, 'out_mib': out_mib},
           'cpu_s': round(cpu_s, 3), 'wall_s': round(wall_s, 3), 'peak_rss_mib_wait4': round(ru.ru_maxrss / 1024, 1),
           'peak_rss_mib_polled': round(peak_rss / 1024, 1), 'output_bytes': dir_bytes(run_dir) - base,
           'exit_code': rc, 'cap_trip': trip,
           'step_label_if_tripped_or_crashed': (cs.UNI if (trip or (rc not in (0, 10))) else None)}
    with open(os.path.join(run_dir, 'steps', f'{rnd}_{step}.json'), 'w') as f:
        json.dump(rec, f, indent=1)
    log(run_dir, {'event': 'step_end', **rec})
    return rec


def finish(run_dir, kind, reason, extra):
    with open(os.path.join(run_dir, kind), 'w') as f:
        f.write(f'{kind}\nreason: {reason}\ntime: {time.strftime("%Y-%m-%d %H:%M:%S %Z")}\n')
        f.write(json.dumps(extra, indent=1) + '\n')
    files = []
    for root, _, fs in os.walk(run_dir):
        for fn in fs:
            pth = os.path.join(root, fn)
            rel = os.path.relpath(pth, run_dir)
            if rel == 'SHA256SUMS':
                continue
            files.append(rel)
    with open(os.path.join(run_dir, 'SHA256SUMS'), 'w') as f:
        for rel in sorted(files):
            f.write(f'{cs.sha256_file(os.path.join(run_dir, rel))}  {rel}\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['census', 'smoke'], required=True)
    ap.add_argument('--run-root', required=True)
    ap.add_argument('--code-sums-sha', required=True)
    a = ap.parse_args()
    if a.mode == 'smoke' and os.path.abspath(a.run_root).startswith('/workspace/runs_l0p'):
        print('smoke must not use runs_l0p'); return 2
    if a.mode == 'census' and 'NOT_CENSUS' in a.run_root:
        return 2
    date = time.strftime('%Y%m%d')
    name = f'{date}_l0p_census_r1_c2673a64' if a.mode == 'census' else f'{date}_SMOKE_NOT_CENSUS'
    run_dir = os.path.join(a.run_root, name)
    os.makedirs(a.run_root, exist_ok=True)
    try:
        os.mkdir(run_dir)          # exclusive: one attempt only
    except FileExistsError:
        print('run folder exists; refusing (one attempt only):', run_dir); return 3
    os.mkdir(os.path.join(run_dir, 'steps'))
    t_start = time.time()
    attempt = {'mode': a.mode, 'design_sha256': cs.R1_SHA, 'code_manifest_sha256': a.code_sums_sha,
               'code_dir': CODE_DIR, 'driver_pid': os.getpid(), 'start_local': time.strftime('%Y-%m-%d %H:%M:%S %Z'),
               'MemAvailable_kB_at_start': cs.meminfo_kb(), 'total_caps': TOTAL_CAPS,
               'NOTICE': 'NOT CENSUS - tiny smoke test' if a.mode == 'smoke' else None}
    with open(os.path.join(run_dir, 'attempt.json'), 'w') as f:
        json.dump(attempt, f, indent=1)
    recs = []
    try:
        if cs.sha256_file(cs.R1_PATH) != cs.R1_SHA:
            finish(run_dir, 'STOPPED', 'design file sha256 mismatch', {}); return 4
        man = os.path.join(CODE_DIR, 'SHA256SUMS')
        if not os.path.exists(man) or cs.sha256_file(man) != a.code_sums_sha:
            finish(run_dir, 'STOPPED', 'code manifest sha256 mismatch', {}); return 4
        for step in CENSUS_ORDER:
            r = run_step(a, run_dir, 'census', step); recs.append(r)
            if step == 'S0' and r['exit_code'] != 0:
                s0 = os.path.join(run_dir, '_global', 'S0', 'result.json')
                why = 'S0 did not pass'
                if os.path.exists(s0):
                    with open(s0) as f:
                        j = json.load(f)
                    why = f"S0 preflight stop: {j.get('stop_reasons')} MemAvailable={j.get('MemAvailable_kB')} kB (threshold {cs.MEM_THRESHOLD_KB} kB); census UNINFORMATIVE"
                if r['cap_trip']:
                    why += f"; cap trip: {r['cap_trip']}"
                finish(run_dir, 'STOPPED', why, {'steps': recs}); return 5
        # repair round condition
        s7p = os.path.join(run_dir, '_global', 'S7', 'result.json')
        cond = False
        if os.path.exists(s7p):
            with open(s7p) as f:
                cond = bool(json.load(f).get('repair_round_condition_met'))
        log(run_dir, {'event': 'repair_condition', 'C3_F1_NOT_MET': cond})
        repair_note = 'repair round not run (C3 F1 cell is not NOT MET)'
        if cond:
            repair_note = 'repair round run for R-C3'
            for step in REPAIR_ORDER:
                r = run_step(a, run_dir, 'repair', step); recs.append(r)
                if step == 'S0' and r['exit_code'] != 0:
                    repair_note = 'repair round stopped at its S0 preflight; repair round UNINFORMATIVE, census results stand'
                    break
        tot = {'cpu_s': sum(r['cpu_s'] for r in recs), 'wall_s': time.time() - t_start,
               'max_peak_rss_mib': max(r['peak_rss_mib_wait4'] for r in recs),
               'output_bytes': dir_bytes(run_dir)}
        finish(run_dir, 'DONE', 'all steps executed once; ' + repair_note,
               {'totals': tot, 'steps': recs, 'total_caps': TOTAL_CAPS})
        return 0
    except Exception as e:
        finish(run_dir, 'STOPPED', 'driver exception: ' + repr(e), {'traceback': traceback.format_exc(), 'steps': recs})
        return 6


if __name__ == '__main__':
    sys.exit(main())
