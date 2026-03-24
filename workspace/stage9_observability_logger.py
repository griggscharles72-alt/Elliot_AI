#!/usr/bin/env python3
"""
Stage 9 Observability Logger — Safe Version
-------------------------------------------
Purpose:
    Continuously monitor workspace changes and system observability.
    Avoids JSON parse errors on empty or malformed delta logs.

Files:
    - logs/file_delta_change.log : Delta tracking log (initialized if missing)
    - logs/observability.log     : Main logger output

Behavior:
    - Initializes missing or empty logs safely
    - Catches JSON errors and logs them instead of crashing
"""

import json
import time
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DELTA_LOG = ROOT_DIR / "logs/file_delta_change.log"
OBS_LOG = ROOT_DIR / "logs/observability.log"

# -----------------------------
# Ensure delta log exists and is valid JSON
# -----------------------------
if not DELTA_LOG.exists():
    DELTA_LOG.write_text("{}")  # Initialize empty JSON

# Attempt safe load
try:
    with DELTA_LOG.open("r") as f:
        delta_data = json.load(f)
except json.JSONDecodeError:
    delta_data = {}
    with DELTA_LOG.open("w") as f:
        json.dump(delta_data, f)
    with OBS_LOG.open("a") as log:
        log.write(f'{{"error": "Invalid JSON in delta log. Reinitialized.", "file": "{DELTA_LOG}"}}\n')

# -----------------------------
# Main loop
# -----------------------------
while True:
    try:
        # Simulate delta tracking (replace with actual logic)
        with DELTA_LOG.open("r") as f:
            delta_data = json.load(f)

        # Example logging
        with OBS_LOG.open("a") as log:
            log.write(f'{{"status": "Logger running", "timestamp": {int(time.time())}}}\n')

        # Sleep between iterations
        time.sleep(5)

    except Exception as e:
        with OBS_LOG.open("a") as log:
            log.write(f'{{"error": "Unexpected exception: {e}"}}\n')
        time.sleep(5)
