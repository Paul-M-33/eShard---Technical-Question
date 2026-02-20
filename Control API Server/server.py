from fastapi import FastAPI, HTTPException, Depends
import redis
import uuid

from lock_manager import DistributedLock
from command_validator import validate_motor_command
from heartbeat import start_heartbeat
from session import SessionManager
from motor_driver import MotorDriver


# =====================
# Initialization
# =====================

app = FastAPI()

# Redis connection
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True  # auto-decode bytes -> str
)

# Core components
lock = DistributedLock(redis_client)
motor = MotorDriver()
session_manager = SessionManager()

# Token -> user mapping
sessions = {}


# =====================
# Authentication
# =====================

def authenticate(token: str):
    """
    Validate token and session.
    Returns user_id if valid.
    """

    user_id = sessions.get(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not session_manager.is_active(user_id):
        # Cleanup expired session
        sessions.pop(token, None)
        raise HTTPException(status_code=401, detail="Session expired")

    # Refresh activity
    session_manager.touch(user_id)

    return user_id


def get_current_user(token: str):
    return authenticate(token)


# =====================
# API Endpoints
# =====================

@app.post("/auth")
def login(username: str, password: str):
    """
    Authenticate user and create session.
    """

    # TODO: real credential validation

    token = str(uuid.uuid4())

    sessions[token] = username

    session_manager.create(username)

    return {"token": token}


@app.post("/lock")
async def acquire_lock(user_id: str = Depends(get_current_user)):
    """
    Acquire exclusive motor control.
    """

    if lock.acquire(user_id):

        # Start background heartbeat
        await start_heartbeat(user_id)

        return {"status": "lock acquired"}

    raise HTTPException(status_code=423, detail="Lock already taken")


@app.post("/move")
def move_motor(
    command: dict,
    user_id: str = Depends(get_current_user)
):
    """
    Send validated motor command.
    """

    # Check ownership
    owner = lock.redis.get(lock.lock_key)
    if owner is None or owner.decode() != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not hold the lock"
        )

    # Validate command
    if not validate_motor_command(command):
        raise HTTPException(
            status_code=400,
            detail="Invalid motor command"
        )

    # Send to motor
    motor.send_command(command)

    # Renew lease
    lock.refresh(user_id)

    return {"status": "command executed"}


@app.post("/unlock")
def release_lock(user_id: str = Depends(get_current_user)):
    """
    Release motor control.
    """

    if lock.release(user_id):

        session_manager.remove(user_id)

        return {"status": "lock released"}

    raise HTTPException(
        status_code=403,
        detail="You do not hold the lock"
    )


@app.post("/ping")
def ping(user_id: str = Depends(get_current_user)):
    """
    Keep session alive.
    """

    session_manager.touch(user_id)

    return {"status": "alive"}
