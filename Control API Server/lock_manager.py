class DistributedLock:
    """Distributed lock manager using Redis."""
    def __init__(self, redis_client, lock_key="motor_lock", lease_time=30):
        self.redis = redis_client
        self.lock_key = lock_key
        self.lease_time = lease_time  # seconds

    def acquire(self, owner_id):
        """Try to acquire the lock. Returns True if successful."""
        # SETNX + EXPIRE ensures atomic acquisition with expiration
        acquired = self.redis.set(self.lock_key, owner_id, nx=True, ex=self.lease_time)
        return acquired is True

    def release(self, owner_id):
        """Release lock only if owned by owner_id."""
        current_owner = self.redis.get(self.lock_key)
        if current_owner and current_owner.decode() == owner_id:
            self.redis.delete(self.lock_key)
            return True
        return False

    def refresh(self, owner_id):
        """Extend the lock lease if owned."""
        current_owner = self.redis.get(self.lock_key)
        if current_owner and current_owner.decode() == owner_id:
            self.redis.expire(self.lock_key, self.lease_time)
            return True
        return False
