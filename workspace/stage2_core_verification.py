#!/usr/bin/env python3
"""
Stage 2 — Core Engine Verification
Purpose: Verify modules load, logs writable, deterministic BASE_DIR paths.
"""

from pathlib import Path
import sys

# -----------------------------
# BASE DIRECTORY
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
MODULES_DIR = BASE_DIR / "modules"
OBS_DIR = BASE_DIR / "ElliotCore_Observatory/collectors"

# Add modules and collectors to sys.path
sys.path.insert(0, str(MODULES_DIR))
sys.path.insert(0, str(OBS_DIR))

# -----------------------------
# IMPORT CORE MODULES
# -----------------------------
from personality import Personality
from health_check import HealthCheck
from wifi_monitor import WifiMonitor

# -----------------------------
# INITIALIZE MODULES
# -----------------------------
ai_personality = Personality(mode="direct")
hc = HealthCheck()
wm = WifiMonitor(LOG_DIR / "wifi_collector.log")

# -----------------------------
# RUN MODULE CHECKS
# -----------------------------
print(f"[INFO] Personality mode: {ai_personality.mode}")
ai_personality.speak("Stage 2 verification: loaded successfully")

print("[INFO] Running health check...")
hc.run_all()

print("[INFO] Running Wi-Fi monitor scan...")
wm.scan()

# -----------------------------
# LOG RESULTS
# -----------------------------
engine_log = LOG_DIR / "engine.log"
with engine_log.open("a") as f:
    f.write("[Stage2] Core engine verification complete.\n")

print("[SUCCESS] Stage 2 — Core Engine Verification complete!")
print("Ready for Stage 3: Workspace Script Integration")
