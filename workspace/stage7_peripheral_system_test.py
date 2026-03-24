#!/usr/bin/env python3
"""
Stage 7 — Peripheral Loader & System Bridge Verification
Purpose: Validate peripheral detection and system bridge integration.
"""

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
WORKSPACE_DIR = BASE_DIR / "workspace"

sys.path.insert(0, str(WORKSPACE_DIR))

import peripheral_loader
import system_bridge

# -----------------------------
# SCAN CONNECTED PERIPHERALS
# -----------------------------
devices = peripheral_loader.scan_devices()
print(f"[Stage7] Detected peripherals: {devices}")

# -----------------------------
# VERIFY SYSTEM BRIDGE
# -----------------------------
bridge_status = system_bridge.verify_bridge()
print(f"[Stage7] System Bridge status: {bridge_status}")

# -----------------------------
# LOG RESULTS
# -----------------------------
with open(LOG_DIR / "peripheral_loader.log", "a") as f:
    f.write(f"[Stage7] Detected peripherals: {devices}\n")

with open(LOG_DIR / "system_bridge.log", "a") as f:
    f.write(f"[Stage7] System Bridge status: {bridge_status}\n")

with open(LOG_DIR / "engine.log", "a") as f:
    f.write("[Stage7] Peripheral & System Bridge verification complete.\n")

print("[SUCCESS] Stage 7 complete!")
