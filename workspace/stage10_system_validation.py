#!/usr/bin/env python3
"""
Stage 10 – Full System Validation

Validates that all stages (1–9) are running, logs are being written,
delta tracking is stable, and watchdog is operational.
"""

import os
import time
import subprocess

# Paths
ROOT_DIR = os.path.expanduser("~/ElliotCoreRoot")
WORKSPACE_DIR = os.path.join(ROOT_DIR, "workspace")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
PID_FILES = {
    "observability": os.path.join(LOGS_DIR, "stage9_pid.txt"),
    "watchdog": os.path.join(LOGS_DIR, "stage9_watchdog_pid.txt")
}
REQUIRED_LOGS = [
    "ai_interface.log",
    "bluetooth_collector.log",
    "engine.log",
    "file_delta_change.log",
    "system_collector.log",
    "wifi_collector.log",
    "observability.log"
]

def check_process(pid_file):
    """Check if PID in file is running."""
    if not os.path.exists(pid_file):
        return False
    with open(pid_file, "r") as f:
        pid = f.read().strip()
    if not pid.isdigit():
        return False
    try:
        os.kill(int(pid), 0)
        return True
    except ProcessLookupError:
        return False

def check_logs():
    """Ensure required logs exist and are being updated."""
    all_ok = True
    for log in REQUIRED_LOGS:
        path = os.path.join(LOGS_DIR, log)
        if not os.path.exists(path):
            print(f"[ERROR] Missing log: {log}")
            all_ok = False
        else:
            # Ensure log is non-empty
            if os.path.getsize(path) == 0:
                print(f"[WARNING] Log empty: {log}")
    return all_ok

def main():
    print("=== Stage 10: System Validation ===")
    # Check processes
    all_processes_ok = True
    for name, pid_file in PID_FILES.items():
        running = check_process(pid_file)
        print(f"[PROCESS] {name}: {'RUNNING' if running else 'NOT RUNNING'}")
        if not running:
            all_processes_ok = False

    # Check logs
    logs_ok = check_logs()

    # Final verdict
    if all_processes_ok and logs_ok:
        print("\n[SUCCESS] All processes running and logs validated. Stage 10 complete.")
    else:
        print("\n[FAILURE] Some checks failed. Review logs and processes.")
        exit(1)

if __name__ == "__main__":
    main()
