import time

# key -> last_seen_timestamp
_recent = {}
WINDOW_SECONDS = 5

def is_duplicate(key):
    now = time.time()
    last = _recent.get(key)
    _recent[key] = now
    if last is None:
        return False
    return (now - last) < WINDOW_SECONDS
