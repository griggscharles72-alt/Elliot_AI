#!/usr/bin/env python3
from pathlib import Path
import sys
import importlib
from utils import setup_logger

MODULES_DIR = Path(__file__).resolve().parent.parent / "modules"
OBSERVATORY_DIR = Path(__file__).resolve().parent.parent / "ElliotCore_Observatory/collectors"

sys.path.insert(0, str(MODULES_DIR))
sys.path.insert(0, str(OBSERVATORY_DIR))

logger = setup_logger("loader", "engine.log")

# -----------------------------
# Dynamic Module Loader
# -----------------------------
def load_module(name: str):
    try:
        module = importlib.import_module(name)
        logger.info(f"Module loaded: {name}")
        return module
    except Exception as e:
        logger.error(f"Failed to load module {name}: {e}")
        return None
