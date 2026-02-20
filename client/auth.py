# jupyter_client/auth.py
import requests
from config import BASE_URL, HEADERS


def login(username: str, password: str):
    """Authenticate and store token in HEADERS"""
    r = requests.post(f"{BASE_URL}/auth", json={"username": username, "password": password})
    r.raise_for_status()
    token = r.json()["token"]
    HEADERS.update({"Authorization": f"Bearer {token}"})
    return token
