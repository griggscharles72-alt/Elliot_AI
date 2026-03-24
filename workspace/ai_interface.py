#!/usr/bin/env python3
"""
AI Interface: Primary interactive console for ElliotCore AI.
Handles console input/output and dispatches commands via WorkspaceBridge.
Includes robust error handling, logging, and graceful exit.
"""

import sys
from pathlib import Path

# -----------------------------
# Add project root to sys.path
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# -----------------------------
# Imports
# -----------------------------
from core.workspace_bridge import WorkspaceBridge
from core.utils import setup_logger

# -----------------------------
# Logger Setup
# -----------------------------
logger = setup_logger("ai_interface", "ai_interface.log")

# -----------------------------
# AIInterface Class
# -----------------------------
class AIInterface:
    def __init__(self):
        try:
            self.bridge = WorkspaceBridge()
            logger.info("AIInterface initialized successfully.")
        except Exception as e:
            logger.critical(f"Failed to initialize WorkspaceBridge: {e}")
            raise

    def start_console(self):
        """
        Starts the interactive console for user commands.
        Supports 'exit' and robust error handling.
        """
        print("=== ElliotCore AI Interface ===")
        print("Type 'exit' to quit.")
        while True:
            try:
                command = input(">> ").strip()
                if command.lower() in ("exit", "quit"):
                    print("Exiting AI Interface.")
                    break
                if not command:
                    continue
                response = self.bridge.execute_command(command)
                print(response)
            except KeyboardInterrupt:
                print("\nInterrupted. Exiting.")
                break
            except Exception as e:
                logger.error(f"Interface error: {e}")
                print(f"Error: {e}")

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    try:
        interface = AIInterface()
        interface.start_console()
    except Exception as critical_error:
        logger.critical(f"AIInterface failed to start: {critical_error}")
        print(f"[CRITICAL] {critical_error}")
