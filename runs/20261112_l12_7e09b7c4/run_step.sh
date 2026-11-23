#!/bin/bash
# usage: run_step.sh <STEP>   (one attempt per step; refuses if the step already has a resources file)
set -u
R="$(cd "$(dirname "$0")" && pwd)"; S=$1
mkdir -p "$R/out/$S" "$R/logs"
if [ -e "$R/logs/resources_$S.json" ]; then echo "step $S already attempted; refusing"; exit 9; fi
cd "$R"
exec "$R/env/venv/bin/python" "$R/harness/meter.py" "$S" "$R/logs/$S.log" "$R/logs/resources_$S.json" \
     "$R/env/venv/bin/python" -u "$R/harness/l12.py" "$S"
