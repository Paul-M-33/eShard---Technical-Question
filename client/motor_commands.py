# jupyter_client/motor_commands.py
import requests
from config import BASE_URL, HEADERS


def move_motor(command: dict):
    """Send move command to motor via server API"""
    payload = {"angle": command[angle], "speed": command[speed], "acceleration": command[acceleration]}
    r = requests.post(f"{BASE_URL}/move", headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()
