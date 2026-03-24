#!/usr/bin/env python3
from pathlib import Path
import sys
import logging

# -----------------------------
# Setup (FIXED ROOT)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
OFFLINE_DIR = BASE_DIR / "offline_packages"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / "olama_sanity.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("OlamaSanity")

# -----------------------------
# Sanity Check
# -----------------------------
try:
    olama_package = OFFLINE_DIR / "olama_offline_package.tar.gz"

    if not olama_package.exists():
        logger.error(f"Olama package missing: {olama_package}")
        print(f"[ERROR] Olama package missing: {olama_package}")
        sys.exit(1)

    logger.info(f"Olama package found: {olama_package}")
    print(f"[INFO] Olama package found: {olama_package}")

    # Simulated load
    logger.info("Attempting Olama offline brain load...")
    print("[INFO] Olama offline brain loaded successfully (simulated).")

except Exception as e:
    logger.error(f"Sanity check failed: {e}")
    print(f"[ERROR] Sanity check failed: {e}")
    sys.exit(1)

logger.info("Sanity check complete.")
print("[SUCCESS] Olama sanity check complete. Logs at:", log_file)
