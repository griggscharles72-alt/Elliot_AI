#!/usr/bin/env python3
from pathlib import Path
import sys
from utils import setup_logger

logger = setup_logger("tinker_bridge", "engine.log")

# -----------------------------
# Workspace Tinker Interface
# -----------------------------
def execute_tinker(script_path: Path):
    """
    Safely execute a workspace Tinker script.
    Returns execution success boolean and output dictionary.
    """
    script_path = script_path.resolve()
    if not script_path.exists():
        logger.warning(f"Tinker script not found: {script_path}")
        return False, {}

    try:
        namespace = {}
        with open(script_path, "r") as f:
            code = f.read()
        exec(code, namespace)
        logger.info(f"Tinker executed: {script_path.name}")
        return True, namespace
    except Exception as e:
        logger.error(f"Tinker execution error ({script_path.name}): {e}")
        return False, {}
