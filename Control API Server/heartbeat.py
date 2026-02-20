import asyncio
from server import lock, session_manager


async def start_heartbeat(user_id):
    async def loop():
        while True:
            # 1. Check session is still active
            if not session_manager.is_active(user_id):
                break

            # 2. Check user still owns the lock
            owner = lock.redis.get(lock.lock_key)
            if owner is None or owner.decode() != user_id:
                break

            # 3. Refresh lock
            if not lock.refresh(user_id):
                break

            # 4. Wait before next heartbeat
            await asyncio.sleep(2)

        # Cleanup if loop exits
        lock.release(user_id)
        print(f"Heartbeat stopped for {user_id}, lock released if held.")

    asyncio.create_task(loop())
