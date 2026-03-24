#!/usr/bin/env bash
# File: launch_delta_dashboard.sh
# -----------------------------
# One-command launcher for Delta Tracker Dashboard Stage 24
# Location: ~/ElliotCoreRoot
# Usage: ./launch_delta_dashboard.sh
# -----------------------------

set -e

BASE_DIR="$HOME/ElliotCoreRoot"
VENV_DIR="$BASE_DIR/venv"
WORKSPACE_DIR="$BASE_DIR/workspace"

# Step 1: Create virtual environment if missing
if [ ! -d "$VENV_DIR" ]; then
    echo "[+] Creating Python venv..."
    python3 -m venv "$VENV_DIR"
fi

# Step 2: Activate virtual environment
source "$VENV_DIR/bin/activate"

# Step 3: Upgrade pip and install required packages
pip install --upgrade pip setuptools wheel >/dev/null
pip install --upgrade matplotlib >/dev/null

# Step 4: Ensure workspace exists
mkdir -p "$WORKSPACE_DIR"

# Step 5: Launch Delta Dashboard Stage 24
echo "[+] Launching Delta Tracker Dashboard Stage 24..."
python3 "$WORKSPACE_DIR/delta_dashboard.py"
