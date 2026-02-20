# Jupyter notebook example_usage.ipynb

from client.auth import login
from client.heartbeat import start_heartbeat
from client.lock import acquire_lock, release_lock
from client.motor_commands import move_motor

# 1 Login
login("paul", "secret")

# 2 Start heartbeat
start_heartbeat(interval=5)

# 3 Acquire lock
acquire_lock()

# 4 Send motor commands
move_motor({"angle": 10, "speed": 5, "acceleration": 2})
move_motor({"angle": 20, "speed": 3, "acceleration": 5})

# 5 Release lock
release_lock()
