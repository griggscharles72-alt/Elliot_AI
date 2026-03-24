from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = BASE_DIR / "workspace"
MODULES_DIR = BASE_DIR / "modules"
OBSERVATORY_DIR = BASE_DIR / "ElliotCore_Observatory/collectors"
LOG_DIR = BASE_DIR / "logs"
CONFIG_DIR = BASE_DIR / "config"

# Extend sys.path for deterministic imports
sys.path.extend([
    str(WORKSPACE_DIR),
    str(MODULES_DIR),
    str(OBSERVATORY_DIR)
])
#!/usr/bin/env python3
"""
Tinker Validator
----------------
Purpose:
    Validates that the Tinker subsystem is correctly installed and operational.
    Performs:
        - Python version check
        - Workspace folder verification
        - Log write test
Usage:
    python3 tinker_validator.py
"""

import sys
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
ROOT_DIR = Path(__file__).parent.parent
TINKER_DIR = ROOT_DIR / "workspace" / "Tinker_Validator_and_Installer"
LOG_DIR = ROOT_DIR / "logs"
LOG_FILE = LOG_DIR / "tinker_check.log"

# -----------------------------
# VALIDATION
# -----------------------------
errors = []

# Python version check
if sys.version_info < (3, 12):
    errors.append(f"Python 3.12+ required. Found {sys.version_info.major}.{sys.version_info.minor}")

# Workspace folder check
if not TINKER_DIR.exists():
    errors.append(f"Tinker directory missing at {TINKER_DIR}")

# Log write test
try:
    LOG_DIR.mkdir(exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write("[Tinker Validator] Log test OK\n")
except Exception as e:
    errors.append(f"Cannot write to log file: {e}")

# -----------------------------
# RUN TRACKED SCRIPTS (Optional)
# -----------------------------
from importlib.util import spec_from_file_location, module_from_spec

def run_script(script_path):
    spec = spec_from_file_location(script_path.stem, script_path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    if hasattr(mod, "main"):
        print(f"[Tinker] Running {script_path.name}")
        mod.main()
    else:
        print(f"[Tinker] {script_path.name} has no main(), skipping.")

tracked_scripts = [
    WORKSPACE_DIR / "stage1_root_setup.py",
    WORKSPACE_DIR / "stage2_core_verification.py",
    WORKSPACE_DIR / "tage3_workspace_integration.py",
    WORKSPACE_DIR / "stage4_observatory_verification.py",
    WORKSPACE_DIR / "stage5_health_optimization.py",
    WORKSPACE_DIR / "stage6_ai_interface_test.py",
    WORKSPACE_DIR / "stage7_peripheral_system_test.py",
    WORKSPACE_DIR / "stage8_workspace_delta_hooks.py",
    WORKSPACE_DIR / "stage9_observability_logger.py",
    WORKSPACE_DIR / "stage9_watchdog.py",
    WORKSPACE_DIR / "stage10_system_validation.py",
    WORKSPACE_DIR / "elliot_brain_full.py",
    WORKSPACE_DIR / "ai_interface.py",
    WORKSPACE_DIR / "peripheral_loader.py"
]

# Example: run the first script
run_script(tracked_scripts[0])

# -----------------------------
# REPORT
# -----------------------------
if errors:
    print("[Tinker Validator] ERRORS FOUND:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
else:
    print("[Tinker Validator] All checks passed.")
    sys.exit(0)

