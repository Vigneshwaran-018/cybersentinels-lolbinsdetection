#This is the Orchestrator

from core.monitor.process_watcher import watch_processes
from simulation.simulator import run_simulation
from gui.dashboard import start_dashboard
import threading
import time

def start_engine():
    print("[+] LOLBins-X Engine Started")

    stop_flag = threading.Event()
    monitor_thread = threading.Thread(
        target=watch_processes, args=(stop_flag,), daemon=True
    )
    monitor_thread.start()

    time.sleep(2)
    run_simulation()

    try:
        start_dashboard()
    finally:
        stop_flag.set()
        monitor_thread.join(timeout=2)
        print("[+] Engine stopped cleanly")


