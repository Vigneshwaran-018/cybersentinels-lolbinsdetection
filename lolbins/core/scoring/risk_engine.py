#Scoring weights are calculate here

import json
import os

TRUSTED_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../config/trusted_parents.json"
)

with open(TRUSTED_PATH, "r") as f:
    TRUSTED = json.load(f)

def calculate_risk(process_name, command_line, parent_name=None):
    score = 0
    reasons = []

    if process_name == "powershell.exe":
        score += 20
        reasons.append("PowerShell execution")

        if parent_name and parent_name not in TRUSTED.get("powershell.exe", []):
            score += 20
            reasons.append("Untrusted parent process")

        if "-enc" in command_line:
            score += 60
            reasons.append("Encoded command")

    return score, reasons
