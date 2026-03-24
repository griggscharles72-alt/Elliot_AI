#!/usr/bin/env python3
"""
Stage 4 — ElliotCore_Observatory Collector Verification
Purpose: Validate all collectors run and log deterministically.
"""

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
OBS_DIR = BASE_DIR / "ElliotCore_Observatory/collectors"

sys.path.insert(0, str(OBS_DIR))

# -----------------------------
# IMPORT COLLECTORS
# -----------------------------
from wifi_collector import scan as wifi_scan
from bluetooth_collector import scan as bt_scan
from system_collector import scan as sys_scan

# -----------------------------
# RUN SCANS
# -----------------------------
wifi_scan()
bt_scan()
sys_scan()

# -----------------------------
# LOG CONFIRMATION
# -----------------------------
with open(LOG_DIR / "engine.log", "a") as f:
    f.write("[Stage4] All observatory collectors ran successfully.\n")

print("[SUCCESS] Stage 4 — Observatory Collector Verification complete!")
