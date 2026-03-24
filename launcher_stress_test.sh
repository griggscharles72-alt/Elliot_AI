#!/usr/bin/env bash
# -----------------------------------
# ElliotCore System Stress-Test Script
# -----------------------------------
set -euo pipefail

ROOT_DIR="$HOME/ElliotCoreRoot"
LOG_DIR="$ROOT_DIR/logs"
WORKSPACE="$ROOT_DIR/workspace"
VENV_DIR="$ROOT_DIR/venv"

# -----------------------------
# ACTIVATE VENV
# -----------------------------
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    echo "[INFO] Python virtual environment activated."
else
    echo "[ERROR] Virtual environment not found at $VENV_DIR"
    exit 1
fi

# -----------------------------
# CLEAR OLD LOGS/PIDs
# -----------------------------
echo "[INFO] Clearing old logs and PID files..."
rm -f "$LOG_DIR"/stage*_pid.txt
rm -f "$LOG_DIR"/*.log

# -----------------------------
# START SYSTEM PROCESSES
# -----------------------------
echo "[INFO] Starting Observability Logger..."
python3 "$ROOT_DIR/core/engine.py" &> "$LOG_DIR/observability.log" &
LOGGER_PID=$!

echo "[INFO] Starting Watchdog..."
python3 "$ROOT_DIR/workspace/stage9_watchdog.py" &> "$LOG_DIR/watchdog.log" &
WATCHDOG_PID=$!

sleep 2
echo "[INFO] Running Tinker Validator..."
python3 "$WORKSPACE/tinker_validator.py" &> "$LOG_DIR/tinker_check.log" || true

# -----------------------------
# WORKSPACE SIMULATION
# -----------------------------
echo "[INFO] Simulating workspace file changes..."
SIM_FILES=("test_file1.txt" "test_file2.txt" "test_file3.txt")
for f in "${SIM_FILES[@]}"; do
    touch "$WORKSPACE/$f"
    echo "Initial content for $f" > "$WORKSPACE/$f"
done

sleep 1
for f in "${SIM_FILES[@]}"; do
    echo "Updated content for $f" >> "$WORKSPACE/$f"
done

sleep 1
for f in "${SIM_FILES[@]}"; do
    rm -f "$WORKSPACE/$f"
done

# -----------------------------
# MONITOR LOGS FOR ERRORS
# -----------------------------
echo "[INFO] Checking logs for ERROR or WARNING..."
ERRORS=$(grep -iE "ERROR|WARNING" "$LOG_DIR"/*.log || true)

if [ -n "$ERRORS" ]; then
    echo "[ALERT] Issues detected during stress test:"
    echo "$ERRORS"
else
    echo "[OK] No errors or warnings detected."
fi

# -----------------------------
# CLEANUP
# -----------------------------
kill $LOGGER_PID $WATCHDOG_PID &> /dev/null || true
echo "[INFO] Stress test complete. Processes terminated."
