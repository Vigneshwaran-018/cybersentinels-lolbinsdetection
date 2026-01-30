import psutil
import time
from datetime import datetime

from core.scoring.risk_engine import calculate_risk
from core.defense.defender import block_process
from forensics.timeline import log_event
from gui.dashboard import push_event, detector_state
from config.loader import load_config


config = load_config()

LOLBINS = config["lolbins"]
RISK_BLOCK_THRESHOLD = config.get("risk_block_threshold", 60)
DEFENSE_MODE = config.get("defense_mode", "block")


def watch_processes(stop_flag=None):
    seen = set()

    while True:
        if stop_flag and stop_flag.is_set():
            break

        # Check if detection is paused
        if not detector_state.get("running", True):
            time.sleep(1)
            continue

        for proc in psutil.process_iter(["pid", "ppid", "name", "cmdline"]):
            try:
                # Double-check pause state inside loop
                if not detector_state.get("running", True):
                    break

                if proc.pid in seen:
                    continue
                seen.add(proc.pid)

                name = proc.info["name"]
                if not name:
                    continue

                name = name.lower()
                if name not in LOLBINS:
                    continue

                cmdline = proc.info["cmdline"]
                cmd = " ".join(cmdline) if cmdline else ""

                # Get parent process name
                try:
                    parent_proc = proc.parent()
                    parent_name = parent_proc.name() if parent_proc else None
                except:
                    parent_name = None

                # Calculate risk - returns (score, reasons, threat_level, confidence)
                result = calculate_risk(name, cmd, parent_name)
                
                # Handle both old and new return formats
                if len(result) == 4:
                    risk, reasons, threat_level, confidence = result
                else:
                    risk, reasons = result
                    threat_level = "MEDIUM" if risk >= 50 else "LOW"
                    confidence = risk / 100.0

                event = {
                    "pid": proc.pid,
                    "ppid": proc.ppid(),
                    "process": name,
                    "command": cmdline,
                    "risk": risk,
                    "reasons": reasons,
                    "threat_level": threat_level,
                    "confidence": confidence
                }

                # Only alert and log if detection is enabled
                if detector_state.get("running", True):
                    # GUI color mapping
                    msg = (
                        f"[{datetime.now().strftime('%H:%M:%S')}] "
                        f"[{threat_level}] {name} | Risk={risk} | Reasons={', '.join(reasons) if reasons else 'None'}"
                    )

                    if risk < 30:
                        push_event("🟢 " + msg, "low")
                    elif risk < 60:
                        push_event("🟡 " + msg, "medium")
                    elif risk < 100:
                        push_event("🟠 " + msg, "high")
                    else:
                        push_event("🔴 " + msg, "critical")

                    log_event(event)

                    # Defense action
                    if risk >= RISK_BLOCK_THRESHOLD:
                        if DEFENSE_MODE == "alert":
                            push_event(f"🚨 [{threat_level}] HIGH RISK → ALERT ONLY", "blocked")
                        elif DEFENSE_MODE == "block":
                            push_event(f"🛑 🚨 [{threat_level}] HIGH RISK → PROCESS BLOCKED", "blocked")
                            block_process(proc.pid)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        time.sleep(1)
