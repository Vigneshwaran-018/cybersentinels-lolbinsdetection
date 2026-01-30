# Attack chain timeline is calculated here

from datetime import datetime
import json
import os

LOG_FILE = "forensics_timeline.json"

def log_event(event):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data.append(record)
        f.seek(0)
        json.dump(data, f, indent=2)
