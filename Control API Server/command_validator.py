MAX_SPEED = 100
MAX_ANGLE = 180
MAX_ACCELERATION = 50


def validate_motor_command(command: dict) -> bool:
    """
    Checks if the command respects motor constraints.
    Example command: {'speed': 50, 'angle': 90, 'acceleration': 30}
    """
    if not (0 <= command.get("speed", 0) <= MAX_SPEED):
        return False
    if not (0 <= command.get("angle", 0) <= MAX_ANGLE):
        return False
    if not (0 <= command.get("acceleration", 0) <= MAX_ACCELERATION):
        return False
    return True
