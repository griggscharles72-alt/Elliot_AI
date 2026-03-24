#!/usr/bin/env python3
from pathlib import Path
import sys
import logging

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = BASE_DIR / "modules"
WORKSPACE_DIR = BASE_DIR / "workspace"
OBSERVATORY_DIR = BASE_DIR / "ElliotCore_Observatory/collectors"
LOG_DIR = BASE_DIR / "logs"

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Extend sys.path deterministically
sys.path[:0] = [str(MODULES_DIR), str(OBSERVATORY_DIR), str(WORKSPACE_DIR)]

# -----------------------------
# Logging
# -----------------------------
ENGINE_LOG = LOG_DIR / "engine.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(str(ENGINE_LOG)),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("engine")
logger.info("Engine starting...")

# -----------------------------
# Load Core Modules
# -----------------------------
try:
    from wifi_monitor import WifiMonitor
    from health_check import HealthCheck
    from personality import Personality
except ImportError as e:
    logger.error(f"Core module import failed: {e}")
    raise

# -----------------------------
# Load Olama Offline Brain
# -----------------------------
try:
    import olama_brain
    logger.info(f"Olama brain loaded: {getattr(olama_brain, '__version__', 'unknown')}")
except ImportError as e:
    logger.error(
        "Olama brain module not found. Ensure offline package is installed."
    )
    raise

# -----------------------------
# Engine Main
# -----------------------------
def main():
    logger.info(f"Base Dir: {BASE_DIR}")
    logger.info(f"Workspace Dir: {WORKSPACE_DIR}")

    # Initialize AI Personality
    ai_personality = Personality(mode="friendly")
    logger.info(f"AI Personality loaded: {ai_personality.mode}")

    # Run health checks
    hc = HealthCheck()
    hc.run_all()
    logger.info("Health checks completed.")

    # Start Wi-Fi monitoring
    wm = WifiMonitor(LOG_DIR / "wifi.log")
    wm.scan()
    logger.info("Wi-Fi scan completed.")

    # Initialize Olama brain
    brain = olama_brain.OfflineBrain(base_dir=str(BASE_DIR))
    logger.info("Olama OfflineBrain initialized.")

    # Test command
    try:
        response = brain.run("echo initialization test")
        logger.info(f"Olama brain test response: {response}")
    except Exception as e:
        logger.error(f"Olama brain test failed: {e}")

    logger.info("Engine run completed successfully.")

if __name__ == "__main__":
    main()
