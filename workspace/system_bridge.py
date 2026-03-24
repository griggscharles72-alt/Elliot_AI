#!/usr/bin/env python3
"""
SYSTEM BRIDGE — ElliotCoreRoot

Purpose:
- Connect BrainChat → local system
- Safe read-only operations (phase 1)
- Callable from AI responses

Capabilities:
- File read
- Directory scan
- Log access
- Module trigger (basic)

"""

from pathlib import Path
import json
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
MODULES_DIR = BASE_DIR / "modules"
OBS_DIR = BASE_DIR / "ElliotCore_Observatory/collectors"


# -----------------------------
# FILE SYSTEM
# -----------------------------

def read_file(path: str, max_chars: int = 4000) -> str:
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return f"[ERROR] File not found: {p}"
        data = p.read_text(errors="ignore")
        return data[:max_chars]
    except Exception as e:
        return f"[ERROR] read_file failed: {e}"


def list_dir(path: str) -> str:
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return f"[ERROR] Path not found: {p}"
        return "\n".join([str(x) for x in p.iterdir()])
    except Exception as e:
        return f"[ERROR] list_dir failed: {e}"


# -----------------------------
# LOG ACCESS
# -----------------------------

def get_logs() -> str:
    try:
        logs = []
        for f in LOG_DIR.glob("*.log"):
            logs.append(f"--- {f.name} ---")
            logs.append(f.read_text(errors="ignore")[-2000:])
        return "\n".join(logs)
    except Exception as e:
        return f"[ERROR] get_logs failed: {e}"


# -----------------------------
# MODULE EXECUTION
# -----------------------------

def run_module(name: str) -> str:
    try:
        module_path = MODULES_DIR / f"{name}.py"
        if not module_path.exists():
            return f"[ERROR] Module not found: {name}"

        result = subprocess.run(
            ["python3", str(module_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        return result.stdout or result.stderr

    except Exception as e:
        return f"[ERROR] run_module failed: {e}"


# -----------------------------
# DISPATCH
# -----------------------------

def handle_command(cmd: dict) -> str:
    """
    Expected format from AI:
    {
        "action": "read_file",
        "path": "/path/to/file"
    }
    """

    action = cmd.get("action")

    if action == "read_file":
        return read_file(cmd.get("path", ""))

    elif action == "list_dir":
        return list_dir(cmd.get("path", ""))

    elif action == "get_logs":
        return get_logs()

    elif action == "run_module":
        return run_module(cmd.get("name", ""))

    return "[ERROR] Unknown action"
