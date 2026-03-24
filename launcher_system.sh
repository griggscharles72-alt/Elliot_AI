#!/usr/bin/env bash
# -----------------------------
# ElliotCore Full System Launcher
# Anchored, self-contained, real-time logging
# -----------------------------
set -euo pipefail

ROOT_DIR="$HOME/ElliotCoreRoot"
cd "$ROOT_DIR" || { echo "[ERROR] Failed to cd to $ROOT_DIR"; exit 1; }

# Activate Python virtual environment
VENV_DIR="$ROOT_DIR/venv"
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    echo "[INFO] Python virtual environment activated."
else
    echo "[ERROR] Virtual environment not found at $VENV_DIR"
    exit 1
fi

# Clear old logs & PID files
for f in logs/observability.log logs/watchdog.log logs/stage9_pid.txt logs/stage9_watchdog_pid.txt logs/tinker_check.log; do
    > "$f"
done
echo "[INFO] Cleared old logs and PID files."

# Start Stage 9 Observability Logger
nohup python3 workspace/stage9_observability_logger.py >> logs/observability.log 2>&1 &
echo $! > logs/stage9_pid.txt
echo "[INFO] Stage 9 Observability Logger started (PID $(cat logs/stage9_pid.txt))."

# Start Stage 9 Watchdog
nohup python3 workspace/stage9_watchdog.py >> logs/watchdog.log 2>&1 &
echo $! > logs/stage9_watchdog_pid.txt
echo "[INFO] Stage 9 Watchdog started (PID $(cat logs/stage9_watchdog_pid.txt))."

# Run Tinker Validator
"$ROOT_DIR/test_tinker.sh"

# Health check summary
echo "[INFO] Checking running processes..."
ps -p $(cat logs/stage9_pid.txt) >/dev/null && echo "[OK] Observability Logger running." || echo "[FAIL] Observability Logger not running."
ps -p $(cat logs/stage9_watchdog_pid.txt) >/dev/null && echo "[OK] Watchdog running." || echo "[FAIL] Watchdog not running."

# Tail logs continuously
echo "[INFO] Tailing logs (Ctrl+C to exit)..."
tail -f logs/observability.log logs/watchdog.log logs/tinker_check.log
