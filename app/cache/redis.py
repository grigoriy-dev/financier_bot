"""

"""


from aioredis import Redis, create_redis_pool

# Глобальная переменная для хранения пула подключений Redis
redis: Redis = None

async def get_redis() -> Redis:
    global redis
    if redis is None:
        redis = await create_redis_pool("redis://localhost")
    return redis
