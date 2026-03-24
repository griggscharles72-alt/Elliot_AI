#!/usr/bin/env python3
"""
Stage 5 — Health Check & Optimization Module Validation
Purpose: Validate health and optimization modules run correctly.
"""

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
MODULES_DIR = BASE_DIR / "modules"

sys.path.insert(0, str(MODULES_DIR))

import health_check
import optimization

# -----------------------------
# RUN HEALTH CHECK
# -----------------------------
metrics = health_check.run()
print(f"[Stage5] Health metrics collected: {metrics}")

# -----------------------------
# RUN OPTIMIZATION
# -----------------------------
optimization.apply()
print("[Stage5] Optimization routines applied.")

# -----------------------------
# LOG CONFIRMATION
# -----------------------------
with open(LOG_DIR / "engine.log", "a") as f:
    f.write("[Stage5] Health Check & Optimization complete.\n")

print("[SUCCESS] Stage 5 complete!")
