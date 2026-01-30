import psutil

def block_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        print("🛑 DEFENSE ACTION: Process terminated")
    except Exception as e:
        print("⚠️ DEFENSE FAILED:", e)
