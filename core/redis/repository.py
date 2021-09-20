from typing import Optional
from aioredis import Redis


class RedisRepository:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def set(self, key: str, value: str, expire: Optional[int] = None):
        if expire:
            return await self._redis.set(key, value, ex=expire)

        return await self._redis.set(key, value)

    async def get(self, key: str):
        return await self._redis.get(key)
