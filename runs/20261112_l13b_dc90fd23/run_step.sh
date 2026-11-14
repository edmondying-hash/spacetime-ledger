#!/bin/bash
# usage: run_step.sh <STEP>   (one attempt per step; refuses if the step already has a resources file)
# Caps (design Sec. 6): 1 thread (pinned in harness/meter.py), 10 min per step (meter kills at 600 s),
# 30 min total (refuses a step if S0..S(n-1) wall already >= 1800 s), memory: address-space ulimit 2 GiB.
set -u
R="$(cd "$(dirname "$0")" && pwd)"; S=$1
PY=/home/eying/spacetime_files/runs/20261112_l12_7e09b7c4/env/venv/bin/python   # L1.2 venv, used read-only
mkdir -p "$R/logs"
if [ -e "$R/logs/resources_$S.json" ]; then echo "step $S already attempted; refusing"; exit 9; fi
TOT=$("$PY" -c "import json,glob;print(sum(json.load(open(f))['wall_s'] for f in glob.glob('$R/logs/resources_S*.json')))")
if "$PY" -c "import sys;sys.exit(0 if $TOT >= 1800 else 1)"; then echo "30 min total cap reached ($TOT s); $S not run"; exit 8; fi
ulimit -v 2097152
cd "$R"
exec "$PY" -B "$R/harness/meter.py" "$S" "$R/logs/$S.log" "$R/logs/resources_$S.json" "$PY" -B -u "$R/harness/l13b_measure.py" "$S"
