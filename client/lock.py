# jupyter_client/lock.py
import requests
from config import BASE_URL, HEADERS


def acquire_lock():
    r = requests.post(f"{BASE_URL}/lock", headers=HEADERS)
    if r.status_code != 200:
        raise Exception(f"Lock refused: {r.text}")
    return True


def release_lock():
    r = requests.post(f"{BASE_URL}/unlock", headers=HEADERS)
    r.raise_for_status()
    return True
