#!/usr/bin/env bash
# ====================================================
# ElliotCore — Ollama Offline Installer (REAL)
# ====================================================
# Installs Ollama binary + validates runtime
# ====================================================

set -euo pipefail

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/.."
PKG_DIR="$BASE_DIR/offline_packages"
LOG_DIR="$BASE_DIR/logs"
LOG_FILE="$LOG_DIR/ollama_install.log"

mkdir -p "$PKG_DIR" "$LOG_DIR"

echo "[INFO] Starting Ollama installation..." | tee -a "$LOG_FILE"

# -----------------------------
# STEP 1: Detect existing install
# -----------------------------
if command -v ollama >/dev/null 2>&1; then
    echo "[INFO] Ollama already installed: $(which ollama)" | tee -a "$LOG_FILE"
else
    echo "[INFO] Ollama not found. Installing..." | tee -a "$LOG_FILE"

    # -----------------------------
    # ONLINE INSTALL (fallback)
    # -----------------------------
    if curl -fsSL https://ollama.com/install.sh | sh >> "$LOG_FILE" 2>&1; then
        echo "[SUCCESS] Ollama installed via online installer." | tee -a "$LOG_FILE"
    else
        echo "[ERROR] Online install failed. Expect offline package." | tee -a "$LOG_FILE"

        PACKAGE="$PKG_DIR/ollama-linux-amd64.tgz"

        if [ ! -f "$PACKAGE" ]; then
            echo "[ERROR] Missing offline binary: $PACKAGE" | tee -a "$LOG_FILE"
            exit 1
        fi

        echo "[INFO] Extracting offline package..." | tee -a "$LOG_FILE"
        tar -xzf "$PACKAGE" -C /usr/local/bin >> "$LOG_FILE" 2>&1

        chmod +x /usr/local/bin/ollama
        echo "[SUCCESS] Offline install complete." | tee -a "$LOG_FILE"
    fi
fi

# -----------------------------
# STEP 2: Start service
# -----------------------------
echo "[INFO] Starting Ollama service..." | tee -a "$LOG_FILE"

if pgrep -x "ollama" >/dev/null; then
    echo "[INFO] Ollama already running." | tee -a "$LOG_FILE"
else
    nohup ollama serve > "$LOG_DIR/ollama_runtime.log" 2>&1 &
    sleep 2
fi

# -----------------------------
# STEP 3: Verify
# -----------------------------
if command -v ollama >/dev/null 2>&1; then
    echo "[SUCCESS] Ollama binary verified." | tee -a "$LOG_FILE"
    ollama --version | tee -a "$LOG_FILE"
else
    echo "[FAIL] Ollama still not available." | tee -a "$LOG_FILE"
    exit 1
fi

echo "[SUCCESS] Ollama installation + runtime ready."
