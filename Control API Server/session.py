import time


class SessionManager:

    TIMEOUT = 15

    def __init__(self):
        # user_id → last_activity_time
        self.sessions = {}

    def create(self, user_id):
        self.sessions[user_id] = time.time()

    def touch(self, user_id):
        """
        Called when user sends:
        /ping
        /move
        /lock
        It updates activity time.
        """
        self.sessions[user_id] = time.time()

    def is_active(self, user_id):
        last = self.sessions.get(user_id)
        if not last:
            return False
        return time.time() - last < self.TIMEOUT

    def remove(self, user_id):
        self.sessions.pop(user_id, None)
