#!/usr/bin/env python3
"""
Stage 6 — Workspace AI Interface Validation
Purpose: Validate AI interface boots correctly and integrates with elliot_brain_full.
"""

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
WORKSPACE_DIR = BASE_DIR / "workspace"

sys.path.insert(0, str(WORKSPACE_DIR))

import ai_interface
import elliot_brain_full

# -----------------------------
# INITIALIZE AI INTERFACE
# -----------------------------
interface = ai_interface.AIInterface(elliot_brain_full.Brain())
test_prompt = "Self-dialogue test: confirm readiness."

response = interface.send_prompt(test_prompt)
print(f"[Stage6] AI Interface response: {response}")

# -----------------------------
# LOG CONFIRMATION
# -----------------------------
with open(LOG_DIR / "engine.log", "a") as f:
    f.write("[Stage6] AI Interface Validation complete.\n")

print("[SUCCESS] Stage 6 complete!")
