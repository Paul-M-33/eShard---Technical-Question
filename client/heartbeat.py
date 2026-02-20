# jupyter_client/heartbeat.py
import threading
import time
import requests
from config import BASE_URL, HEADERS


def start_heartbeat(interval=5):
    """Start background thread sending ping requests."""
    def keepalive():
        while True:
            try:
                requests.post(f"{BASE_URL}/ping", headers=HEADERS)
            except Exception:
                pass  # optionally log errors
            time.sleep(interval)

    thread = threading.Thread(target=keepalive, daemon=True)
    thread.start()
    return thread
