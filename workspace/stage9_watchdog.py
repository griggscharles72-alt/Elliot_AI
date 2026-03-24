#!/usr/bin/env python3
"""
Stage 9 Watchdog — Safe Version
-------------------------------
Purpose:
    Ensure stage9_observability_logger.py runs continuously.
    Auto-restarts on crash, logs output, saves PID for control.

Files:
    - workspace/stage9_observability_logger.py : main Stage 9 module
    - logs/observability.log                  : log output
    - logs/stage9_watchdog_pid.txt            : PID of the watchdog
"""

import os
import subprocess
import signal
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
STAGE9 = ROOT_DIR / "workspace/stage9_observability_logger.py"
OBS_LOG = ROOT_DIR / "logs/observability.log"
PID_FILE = ROOT_DIR / "logs/stage9_watchdog_pid.txt"

process = None
running = True

# -----------------------------
# Clean shutdown handler
# -----------------------------
def shutdown(sig, frame):
    global running, process
    running = False
    print(f"[Watchdog] Received signal {sig}. Shutting down...")
    if process and process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# -----------------------------
# Save watchdog PID
# -----------------------------
PID_FILE.write_text(str(os.getpid()))
print(f"[Watchdog] Watchdog PID saved to {PID_FILE}")

# -----------------------------
# Main watchdog loop
# -----------------------------
while running:
    print("[Watchdog] Starting Stage 9 Observability Logger...")
    with open(OBS_LOG, "a") as log:
        process = subprocess.Popen(
            [sys.executable, str(STAGE9)],
            stdout=log,
            stderr=subprocess.STDOUT
        )
        exit_code = process.wait()

    if running:
        print(f"[Watchdog] Stage 9 exited with {exit_code}. Restarting in 5s...")
        time.sleep(5)
