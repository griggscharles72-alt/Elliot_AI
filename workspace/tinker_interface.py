#!/usr/bin/env python3
"""
Tinker Interface – Stage 12 (Updated)
-------------------------------------
Purpose:
    Integrate observatory collectors into the deterministic engine loop.
    Monitors delta changes, runs workspace scripts, and logs live data.
Location:
    /home/pc-1/ElliotCoreRoot/workspace/tinker_interface.py
"""

from pathlib import Path
import sys
import logging
from importlib.util import spec_from_file_location, module_from_spec

# -----------------------------
# Deterministic Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = BASE_DIR / "workspace"
MODULES_DIR = BASE_DIR / "modules"
OBSERVATORY_DIR = BASE_DIR / "ElliotCore_Observatory/collectors"
LOG_DIR = BASE_DIR / "logs"

sys.path.insert(0, str(MODULES_DIR))
sys.path.insert(0, str(OBSERVATORY_DIR))

# -----------------------------
# Setup Logging
# -----------------------------
ENGINE_LOG = LOG_DIR / "engine.log"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    filename=str(ENGINE_LOG),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("engine")

# -----------------------------
# Import Core Modules
# -----------------------------
try:
    from delta_tracker import DeltaTracker
    from wifi_collector import WifiCollector
    from bluetooth_collector import BluetoothCollector
    from system_collector import SystemCollector
except ImportError as e:
    logger.error(f"Failed to import one or more modules: {e}")
    raise

# -----------------------------
# Utility: Run workspace script
# -----------------------------
def run_script(script_path: Path):
    """
    Dynamically executes a Python script if it has a main() function.
    """
    if not script_path.exists():
        logger.warning(f"Script not found: {script_path}")
        return

    try:
        spec = spec_from_file_location(script_path.stem, script_path)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "main"):
            logger.info(f"Running {script_path.name}")
            mod.main()
        else:
            logger.info(f"{script_path.name} has no main(), skipped.")
    except Exception as e:
        logger.error(f"Error executing {script_path.name}: {e}")

# -----------------------------
# Stage 12: Main Integration Loop
# -----------------------------
def main():
    print(f"[INFO] Base Dir: {BASE_DIR}")
    logger.info(f"Tinker Stage 12 started. Base Dir: {BASE_DIR}")

    # Initialize Delta Tracker
    dt = DeltaTracker(base_dir=str(BASE_DIR))
    logger.info("DeltaTracker initialized.")

    # Initialize observatory collectors
    wifi = WifiCollector(log_file=LOG_DIR / "wifi.log")
    bt = BluetoothCollector(log_file=LOG_DIR / "bluetooth.log")
    sysc = SystemCollector(log_file=LOG_DIR / "system.log")
    logger.info("Collectors initialized.")

    # List of tracked workspace scripts
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

    # Sequentially run workspace scripts
    for script in tracked_scripts:
        run_script(script)

    # Collect live observatory data
    try:
        wifi.scan()
        bt.scan()
        sysc.collect_metrics()
        logger.info("Collectors run complete.")
    except Exception as e:
        logger.error(f"Collector execution error: {e}")

    # Track workspace changes deterministically
    try:
        dt.scan()
        logger.info("DeltaTracker scan complete.")
    except Exception as e:
        logger.error(f"DeltaTracker scan failed: {e}")

    print("[INFO] Stage 12 loop complete.")
    logger.info("Stage 12 completed successfully.")

# -----------------------------
# Execute Main
# -----------------------------
if __name__ == "__main__":
    main()
