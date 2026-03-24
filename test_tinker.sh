#!/usr/bin/env bash
# -----------------------------
# Test Tinker Validator
# -----------------------------
set -euo pipefail

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VALIDATOR="$BASE_DIR/workspace/tinker_validator.py"
LOG_FILE="$BASE_DIR/logs/tinker_check.log"

echo "=== Tinker Validation Test ===" >> "$LOG_FILE"
echo "Timestamp: $(date)" >> "$LOG_FILE"

if [ -f "$VALIDATOR" ]; then
    echo "[INFO] Running Tinker Validator..." | tee -a "$LOG_FILE"
    python3 "$VALIDATOR" >> "$LOG_FILE" 2>&1
else
    echo "[ERROR] Tinker Validator script not found at $VALIDATOR" | tee -a "$LOG_FILE"
    exit 1
fi
