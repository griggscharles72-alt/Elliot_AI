#!/usr/bin/env python3
"""
delta_tracker.py — Official Delta Tracker Module
------------------------------------------------
Tracks added/removed files, maintains a baseline, logs changes,
and prints the full directory tree for your project.

Excludes:
    - Logs and baseline files themselves
    - Virtual environment folder (venv) contents: only surface-level shown
"""

import os
from datetime import datetime
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

BASELINE_FILENAME = "delta_baseline.log"
CHANGELOG_FILENAME = "delta_changes.log"

# ============================================================
# ROOT & PATHS
# ============================================================

try:
    ROOT = Path(__file__).resolve().parents[1]  # go up to project root
except NameError:
    ROOT = Path.cwd()

LOGS_DIR = ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

BASELINE_PATH = LOGS_DIR / BASELINE_FILENAME
CHANGELOG_PATH = LOGS_DIR / CHANGELOG_FILENAME

EXCLUDE_FILES = {BASELINE_FILENAME, CHANGELOG_FILENAME}

# Only show surface-level files for these folders
SURFACE_ONLY_FOLDERS = {"venv"}

# ============================================================
# UTILITIES
# ============================================================

def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def header(title: str) -> None:
    line = "=" * len(title)
    print(f"\n{title}\n{line}")

def print_tree(root: Path, prefix="") -> None:
    entries = sorted([p for p in root.iterdir() if p.name not in EXCLUDE_FILES])
    for i, path in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        print(f"{prefix}{connector}{path.name}")
        if path.is_dir():
            if path.name in SURFACE_ONLY_FOLDERS:
                # Only print immediate children
                children = sorted(list(path.iterdir()))
                for j, sub in enumerate(children):
                    sub_connector = "└── " if j == len(children) - 1 else "├── "
                    print(f"{prefix}    {sub_connector}{sub.name}")
            else:
                extension = "    " if i == len(entries) - 1 else "│   "
                print_tree(path, prefix + extension)

# ============================================================
# BASELINE HANDLING
# ============================================================

def load_baseline(path: Path) -> set[str]:
    if not path.exists():
        return set()
    entries = set()
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line and line not in EXCLUDE_FILES:
                entries.add(line)
    return entries

def save_baseline(path: Path, files: set[str]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for file in sorted(files):
            f.write(file + "\n")

# ============================================================
# CHANGE LOGGING
# ============================================================

def append_change_log(path: Path, added: set[str], removed: set[str]) -> None:
    with path.open("a", encoding="utf-8") as log:
        log.write("\n")
        log.write(f"[RUN {timestamp()}]\n")
        log.write("ADDED:\n" + ("\n".join(f"+ {a}" for a in sorted(added)) if added else "(none)") + "\n")
        log.write("REMOVED:\n" + ("\n".join(f"- {r}" for r in sorted(removed)) if removed else "(none)") + "\n")

# ============================================================
# SCANNING
# ============================================================

def scan_files(root: Path) -> set[str]:
    results = set()
    for dirpath, dirnames, filenames in os.walk(root):
        # Collect files
        for name in filenames:
            if name not in EXCLUDE_FILES:
                results.add(os.path.join(dirpath, name))

        # Prevent recursion into surface-only folders
        for folder in SURFACE_ONLY_FOLDERS:
            if folder in dirnames:
                dirnames.remove(folder)
    return results

# ============================================================
# DELTA ENGINE
# ============================================================

class DeltaScanner:
    def __init__(self, root: Path):
        self.root = root
        self.baseline_path = BASELINE_PATH
        self.change_log_path = CHANGELOG_PATH

    def run(self) -> None:
        previous = load_baseline(self.baseline_path)
        current = scan_files(self.root)

        added = current - previous
        removed = previous - current

        self.render_results(added, removed, current)
        append_change_log(self.change_log_path, added, removed)
        save_baseline(self.baseline_path, current)
        self.print_summary(added, removed, current)

        input("\nPress ENTER to exit and review logs...")

    @staticmethod
    def render_results(added: set[str], removed: set[str], seen: set[str]) -> None:
        header("ADDED FILES")
        print("\n".join(sorted(added)) if added else "(none)")

        header("REMOVED FILES")
        print("\n".join(sorted(removed)) if removed else "(none)")

        header("FULL DIRECTORY TREE")
        print_tree(ROOT)

    @staticmethod
    def print_summary(added: set[str], removed: set[str], seen: set[str]) -> None:
        header("SCAN SUMMARY")
        print(f"Timestamp : {timestamp()}")
        print(f"Root Path : {ROOT}")
        print(f"Added     : {len(added)} file(s)")
        print(f"Removed   : {len(removed)} file(s)")
        print(f"Seen      : {len(seen) - len(added) - len(removed)} file(s)")
        print("=" * 30)
        print(f"Baseline saved at : {BASELINE_PATH}")
        print(f"Changes logged at : {CHANGELOG_PATH}")
        print("=" * 30)
        print("Scan complete. Review results above.")

# ============================================================
# MAIN
# ============================================================

def main():
    scanner = DeltaScanner(ROOT)
    scanner.run()

if __name__ == "__main__":
    main()
