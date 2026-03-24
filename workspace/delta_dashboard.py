#!/usr/bin/env python3
"""
Delta Tracker Dashboard – Stage 24
----------------------------------
Purpose:
    Stage 23 GUI + historical timeline filters, search, and detailed file diff inspection.
Location:
    /home/pc-1/ElliotCoreRoot/workspace/delta_dashboard.py
"""

from pathlib import Path
import sys
import logging
from datetime import datetime
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import shutil
import time
import difflib

# -----------------------------
# Resolve modules path
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = BASE_DIR / "workspace"
MODULES_DIR = BASE_DIR / "modules"
for p in [str(MODULES_DIR.resolve()), str(WORKSPACE_DIR.resolve())]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Logging setup
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
DASHBOARD_LOG = LOG_DIR / "delta_dashboard.log"
logging.basicConfig(
    filename=str(DASHBOARD_LOG),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("delta_dashboard")

# -----------------------------
# Delta Scanner Module (embedded/foolproof)
# -----------------------------
class DeltaScanner:
    """Tracks added and removed files in base_dir."""
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self._seen_files = set(f.name for f in self.base_dir.glob("*.py"))
        self._added = set()
        self._removed = set()

    def scan(self):
        """Detect added/removed .py files in base_dir."""
        current_files = set(f.name for f in self.base_dir.glob("*.py"))
        self._added = current_files - self._seen_files
        self._removed = self._seen_files - current_files
        self._seen_files = current_files

    def get_changes(self):
        """Return (added, removed, None) to match dashboard usage."""
        return self._added, self._removed, None

# -----------------------------
# HealthCheck import fallback
# -----------------------------
try:
    from modules.health_check import HealthCheck
except ImportError:
    class HealthCheck:
        def run_all(self):
            logger.info("HealthCheck stub called")

# -----------------------------
# Dummy collectors
# -----------------------------
class DummyCollector:
    def __init__(self, log_file):
        self.log_file = log_file
    def scan(self):
        logger.info(f"Collector scan: {self.log_file}")
    def collect_metrics(self):
        logger.info(f"Collector metrics: {self.log_file}")

WIFI_LOG = LOG_DIR / "wifi.log"
BT_LOG = LOG_DIR / "bluetooth.log"
SYSTEM_LOG = LOG_DIR / "system.log"

WifiCollector = lambda log_file: DummyCollector(log_file)
BluetoothCollector = lambda log_file: DummyCollector(log_file)
SystemCollector = lambda log_file: DummyCollector(log_file)

BACKUP_DIR = BASE_DIR / "workspace_backup"
BACKUP_DIR.mkdir(exist_ok=True)

# -----------------------------
# Utility Functions
# -----------------------------
def run_script(script_path: Path):
    if not script_path.exists():
        logger.warning(f"Script not found: {script_path}")
        return
    try:
        from importlib.util import spec_from_file_location, module_from_spec
        spec = spec_from_file_location(script_path.stem, script_path)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "main"):
            mod.main()
        logger.info(f"Executed script: {script_path.name}")
    except Exception as e:
        logger.error(f"Error executing {script_path.name}: {e}")

def rollback_file(file_path: Path):
    backup_file = BACKUP_DIR / file_path.relative_to(WORKSPACE_DIR)
    if backup_file.exists():
        shutil.copy2(backup_file, file_path)
        logger.info(f"Rolled back {file_path} from backup")
        return True
    else:
        logger.warning(f"No backup found for {file_path}, cannot rollback")
        return False

def show_diff(file1: Path, file2: Path):
    try:
        with open(file1, "r") as f1, open(file2, "r") as f2:
            diff = difflib.unified_diff(
                f1.readlines(), f2.readlines(),
                fromfile=str(file1), tofile=str(file2)
            )
            return "".join(diff)
    except Exception as e:
        logger.error(f"Error generating diff: {e}")
        return f"Error generating diff: {e}"

# -----------------------------
# GUI
# -----------------------------
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DeltaDashboardGUIStage24:
    REFRESH_INTERVAL = 5000  # ms
    CRITICAL_FILES = {"stage1_root_setup.py", "stage2_core_verification.py", "engine.py"}

    def __init__(self, root):
        self.root = root
        self.root.title("Delta Tracker Dashboard - Stage 24")
        self.dt = DeltaScanner(str(BASE_DIR))
        self.historical_data = []

        # Collectors & health
        self.wifi_collector = WifiCollector(WIFI_LOG)
        self.bt_collector = BluetoothCollector(BT_LOG)
        self.sys_collector = SystemCollector(SYSTEM_LOG)
        self.health = HealthCheck()

        # GUI frames
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.right_frame = tk.Frame(root, width=300)
        self.right_frame.pack(side="right", fill="y")

        self.text_area = scrolledtext.ScrolledText(self.left_frame, width=80, height=20)
        self.text_area.pack(fill="both", expand=True)

        # Timeline figure
        self.figure = Figure(figsize=(6, 3))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.left_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Search bar
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.right_frame, textvariable=self.search_var)
        self.search_entry.pack(pady=2)
        self.search_entry.bind("<Return>", lambda e: self.update_delta_view(filter_term=self.search_var.get()))

        # Stage buttons
        for i in range(1, 11):
            btn = tk.Button(self.right_frame, text=f"Stage {i}", command=lambda s=i: self.run_stage(s))
            btn.pack(pady=2)

        # Log buttons
        for name, path in [("Engine Log", LOG_DIR / "engine.log"),
                           ("Delta Changes", LOG_DIR / "delta_changes.log"),
                           ("Wi-Fi Log", WIFI_LOG),
                           ("Bluetooth Log", BT_LOG),
                           ("System Log", SYSTEM_LOG)]:
            btn = tk.Button(self.right_frame, text=f"View {name}", command=lambda p=path: self.show_log(p))
            btn.pack(pady=2)

        # Threads
        threading.Thread(target=self.periodic_delta_update, daemon=True).start()
        threading.Thread(target=self.self_healing_loop, daemon=True).start()
        threading.Thread(target=self.timeline_updater, daemon=True).start()

    # -----------------------------
    # Delta Tracker
    # -----------------------------
    def periodic_delta_update(self):
        while True:
            try:
                self.dt.scan()
                added, removed, _ = self.dt.get_changes()
                self.historical_data.append((datetime.now(), len(added), len(removed), list(added), list(removed)))
                self.update_delta_view()
            except Exception as e:
                logger.error(f"Periodic delta update failed: {e}")
            time.sleep(self.REFRESH_INTERVAL / 1000)

    def update_delta_view(self, filter_term=""):
        self.text_area.delete("1.0", tk.END)
        latest = self.historical_data[-1] if self.historical_data else (datetime.now(), [], [], [], [])
        _, _, _, added_files, removed_files = latest
        if filter_term:
            added_files = [f for f in added_files if filter_term in f]
            removed_files = [f for f in removed_files if filter_term in f]

        self.text_area.insert(tk.END, f"[Delta Tracker] Last Scan: {datetime.now()}\n")
        self.text_area.insert(tk.END, "\n=== Added Files ===\n")
        for f in added_files:
            self.text_area.insert(tk.END, f"  + {f}\n")
        self.text_area.insert(tk.END, "\n=== Removed Files ===\n")
        for f in removed_files:
            self.text_area.insert(tk.END, f"  - {f}\n")

    def run_stage(self, stage_number):
        script_path = WORKSPACE_DIR / f"stage{stage_number}_script.py"
        run_script(script_path)

    def show_log(self, log_file):
        if log_file.exists():
            with open(log_file) as f:
                content = f.read()
            win = tk.Toplevel(self.root)
            win.title(f"Viewing {log_file.name}")
            text_area = scrolledtext.ScrolledText(win, width=100, height=40)
            text_area.pack(fill="both", expand=True)
            text_area.insert(tk.END, content)
        else:
            messagebox.showwarning("Log Viewer", f"{log_file} not found")

    def timeline_updater(self):
        while True:
            try:
                if self.historical_data:
                    timestamps, added_counts, removed_counts, *_ = zip(*self.historical_data[-20:])
                    self.ax.clear()
                    self.ax.plot(timestamps, added_counts, label="Added")
                    self.ax.plot(timestamps, removed_counts, label="Removed")
                    self.ax.legend()
                    self.ax.set_title("Delta Changes Timeline")
                    self.ax.set_xlabel("Scan Timestamp")
                    self.ax.set_ylabel("Changes Count")
                    self.figure.autofmt_xdate()
                    self.canvas.draw()
            except Exception as e:
                logger.error(f"Timeline update failed: {e}")
            time.sleep(5)

    def self_healing_loop(self):
        while True:
            try:
                added, removed, _ = self.dt.get_changes()
                for f in removed:
                    if f in self.CRITICAL_FILES:
                        rollback_file(WORKSPACE_DIR / f)
                for f in added:
                    src = WORKSPACE_DIR / f
                    dst = BACKUP_DIR / f
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                try:
                    self.health.run_all()
                except Exception as e:
                    logger.error(f"Health check failed: {e}")
                # Run collectors
                for c in [self.wifi_collector, self.bt_collector, self.sys_collector]:
                    try:
                        c.scan() if hasattr(c, "scan") else c.collect_metrics()
                    except Exception as e:
                        logger.warning(f"Collector failed: {e}")
            except Exception as e:
                logger.error(f"Self-healing loop error: {e}")
            time.sleep(10)

# -----------------------------
# Run GUI
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = DeltaDashboardGUIStage24(root)
    root.mainloop()
