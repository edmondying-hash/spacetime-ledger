#!/bin/bash
# usage: run_step.sh <STEP> <script> [args]   (one attempt per step; refuses if the step already has a resources file)
set -u
R="$(cd "$(dirname "$0")" && pwd)"; S=$1; shift
PY=/home/eying/spacetime_files/runs/20261112_l12_7e09b7c4/env/venv/bin/python   # L1.2 venv, used read-only
mkdir -p "$R/logs"
if [ -e "$R/logs/resources_$S.json" ]; then echo "step $S already attempted; refusing"; exit 9; fi
cd "$R"
exec "$PY" -B "$R/harness/meter.py" "$S" "$R/logs/$S.log" "$R/logs/resources_$S.json" "$PY" -B -u "$@"
