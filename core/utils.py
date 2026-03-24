#!/usr/bin/env python3
from pathlib import Path
import json
import logging
import time

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
CONFIG_DIR = BASE_DIR / "config"
LOG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Logging Setup
# -----------------------------
def setup_logger(name: str, log_file: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = logging.FileHandler(LOG_DIR / log_file)
    fh.setLevel(level)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(fh)
    return logger

# -----------------------------
# JSON State Helpers
# -----------------------------
STATE_FILE = CONFIG_DIR / "state.json"
def load_state():
    if not STATE_FILE.exists():
        return {}
    with open(STATE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

# -----------------------------
# Utilities
# -----------------------------
def timestamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
