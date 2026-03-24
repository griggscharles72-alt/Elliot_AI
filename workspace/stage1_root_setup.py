#!/usr/bin/env python3
"""
Stage 1 — Root Setup & Paths Verification
Purpose: Ensure deterministic folder structure exists and BASE_DIR references are correct.
"""

from pathlib import Path
import sys

# -----------------------------
# BASE DIRECTORY SETUP
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = BASE_DIR / "workspace"
MODULES_DIR = BASE_DIR / "modules"
OBSERVATORY_DIR = BASE_DIR / "ElliotCore_Observatory/collectors"
LOG_DIR = BASE_DIR / "logs"
CONFIG_DIR = BASE_DIR / "config"

ALL_DIRS = [
    WORKSPACE_DIR,
    MODULES_DIR,
    OBSERVATORY_DIR,
    LOG_DIR,
    CONFIG_DIR
]

# -----------------------------
# CREATE DIRECTORIES IF MISSING
# -----------------------------
for d in ALL_DIRS:
    if not d.exists():
        d.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Created folder: {d}")
    else:
        print(f"[INFO] Verified folder exists: {d}")

# -----------------------------
# TEST WRITE PERMISSIONS
# -----------------------------
try:
    for d in [LOG_DIR, CONFIG_DIR]:
        test_file = d / "stage1_test.txt"
        test_file.write_text("Stage 1 verification\n", encoding="utf-8")
        test_file.unlink()  # cleanup
        print(f"[INFO] Verified write permissions in: {d}")
except Exception as e:
    print(f"[ERROR] Write permission test failed: {e}")
    sys.exit(1)

print("==================================================")
print("[SUCCESS] Stage 1 — Root Setup & Paths Verification complete!")
print("Ready for Stage 2: Core Engine Verification")
print("==================================================")
