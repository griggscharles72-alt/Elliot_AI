#!/usr/bin/env bash
# --------------------------------------------
# ElliotCore Root Launcher — Final Consolidated
# --------------------------------------------
# Purpose:
#   - Activate Python venv
#   - Verify/install Olama offline brain
#   - Launch Stage 9 Observability Logger
#   - Launch Stage 9 Watchdog
#   - Save PIDs for monitoring/control
# --------------------------------------------

set -euo pipefail

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_DIR="$BASE_DIR/venv"
LOGS_DIR="$BASE_DIR/logs"

mkdir -p "$LOGS_DIR"

# -----------------------------
# Activate venv
# -----------------------------
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    echo "[INFO] Python virtual environment activated."
else
    echo "[ERROR] Virtual environment not found at $VENV_DIR"
    exit 1
fi

# -----------------------------
# Olama offline brain check
# -----------------------------
OLAMA_SCRIPT="$BASE_DIR/install_olama_brain.sh"
OLAMA_LOG="$LOGS_DIR/olama_brain_install.log"

if [ ! -f "$BASE_DIR/olama_brain.py" ]; then
    echo "[INFO] Olama offline brain not detected. Installing..."
    if [ -f "$OLAMA_SCRIPT" ]; then
        bash "$OLAMA_SCRIPT" &> "$OLAMA_LOG"
        echo "[INFO] Olama offline brain installed."
    else
        echo "[ERROR] Olama install script missing: $OLAMA_SCRIPT"
        exit 1
    fi
else
    echo "[INFO] Olama offline brain already present."
fi

# -----------------------------
# Initialize delta logs safely
# -----------------------------
echo "{}" > "$LOGS_DIR/file_delta_change.log"
echo "[INFO] Delta change log initialized."

# -----------------------------
# Launch Stage 9 Observability Logger
# -----------------------------
OBS_LOG="$LOGS_DIR/observability.log"
nohup python3 "$BASE_DIR/workspace/stage9_observability_logger.py" >> "$OBS_LOG" 2>&1 &
echo $! > "$LOGS_DIR/stage9_pid.txt"
echo "[INFO] Stage 9 Observability Logger started. PID saved to $LOGS_DIR/stage9_pid.txt"

# -----------------------------
# Launch Stage 9 Watchdog
# -----------------------------
WATCHDOG_LOG="$LOGS_DIR/watchdog.log"
nohup python3 "$BASE_DIR/workspace/stage9_watchdog.py" >> "$WATCHDOG_LOG" 2>&1 &
echo $! > "$LOGS_DIR/stage9_watchdog_pid.txt"
echo "[INFO] Stage 9 Watchdog started. PID saved to $LOGS_DIR/stage9_watchdog_pid.txt"

echo "[INFO] Launcher completed. Stage 9 logger + watchdog running in background."
