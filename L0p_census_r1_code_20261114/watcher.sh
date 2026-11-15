#!/bin/bash
# L0' census r1 memory-gated launcher. Launches the attempt exactly once when
# MemAvailable >= 3670016 kB; checks immediately, then every 300 s.
# Usage: watcher.sh <sha256 of code SHA256SUMS>
CODE_DIR=/workspace/L0p_census_r1_code_20261114
SUMS_SHA="$1"
ROOT=/workspace/runs_l0p
LOG="$ROOT/watcher.log"
THR=3670016
MARK="$ROOT/.launched_c2673a64"
log() { echo "$(date '+%Y-%m-%d %H:%M:%S %Z') [watcher pid $$] $*" >> "$LOG"; }
log "start; code SHA256SUMS sha256=$SUMS_SHA threshold=${THR} kB interval=300 s"
got=$(sha256sum "$CODE_DIR/SHA256SUMS" | cut -d' ' -f1)
if [ "$got" != "$SUMS_SHA" ]; then log "code manifest hash mismatch ($got); exiting without launch"; exit 1; fi
while true; do
  if [ -e "$MARK" ]; then log "launch marker already exists; exiting without launch"; exit 0; fi
  mem=$(awk '/^MemAvailable:/{print $2}' /proc/meminfo)
  if [ "$mem" -ge "$THR" ]; then
    if mkdir "$MARK" 2>/dev/null; then
      log "MemAvailable=${mem} kB >= ${THR} kB; launching the single attempt"
      cd "$CODE_DIR" || exit 1
      PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
        python3 "$CODE_DIR/census.py" --mode census --run-root "$ROOT" --code-sums-sha "$SUMS_SHA" \
        >> "$ROOT/driver_c2673a64.out" 2>&1 &
      dp=$!
      echo "$dp" > "$MARK/driver.pid"
      log "driver started pid=$dp"
      wait "$dp"; rc=$?
      log "driver exited rc=$rc; watcher exiting"
      exit 0
    fi
  else
    log "MemAvailable=${mem} kB < ${THR} kB; next check in 300 s"
  fi
  sleep 300
done
