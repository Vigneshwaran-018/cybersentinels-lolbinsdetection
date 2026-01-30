import subprocess
import time

def run_simulation():
    print("\n🧪 SIMULATION DATASET LOADED")

    scenarios = [
        {
            "label": "Benign PowerShell",
            "cmd": ["powershell.exe", "-Command", "Write-Output 'Hello World'"],
            "sleep": 2
        },
        {
            "label": "Suspicious PowerShell",
            "cmd": ["powershell.exe", "-Command", "Get-Process"],
            "sleep": 2
        },
        {
            "label": "Malicious Encoded PowerShell",
            "cmd": ["powershell.exe", "-enc", "d2hvYW1p"],
            "sleep": 2
        },
        {
            "label": "CMD Execution",
            "cmd": ["cmd.exe", "/c", "echo test"],
            "sleep": 2
        }
    ]

    for s in scenarios:
        print(f"▶ Running: {s['label']}")
        subprocess.Popen(
            s["cmd"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(s["sleep"])

    print("🧪 SIMULATION COMPLETED\n")
