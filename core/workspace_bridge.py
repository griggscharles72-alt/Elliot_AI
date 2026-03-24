#!/usr/bin/env python3
"""
Workspace Bridge: Central command execution layer between interface and modules.
Handles command dispatch, logging, and fallback mechanisms.
"""

import sys
from pathlib import Path

# Add project root to sys.path for reliable absolute imports
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.utils import setup_logger

# -----------------------------
# Logging Setup
# -----------------------------
logger = setup_logger("workspace_bridge", "workspace_bridge.log")

# -----------------------------
# Safe import Personality
# -----------------------------
try:
    from modules.personality import Personality
except ImportError:
    logger.critical("Personality module missing, loading fallback class.")
    class Personality:
        def respond(self, command: str) -> str:
            return "[Fallback Personality] Personality module missing."

# -----------------------------
# WorkspaceBridge Class
# -----------------------------
class WorkspaceBridge:
    def __init__(self):
        self.personality = Personality()
        logger.info("WorkspaceBridge initialized with Personality.")

    def execute_command(self, command: str) -> str:
        """
        Execute a command string and return the result.
        Placeholder for future module dispatch.
        """
        logger.info(f"Received command: {command}")
        try:
            # Currently forwards command to Personality
            response = self.personality.respond(command)
            logger.info(f"Response: {response}")
            return response
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return f"[WorkspaceBridge Error] {e}"
