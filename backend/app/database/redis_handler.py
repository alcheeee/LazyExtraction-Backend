import json
from typing import Optional, Any
import redis.asyncio as redis
from app.settings import settings


class RedisClient:
    def __init__(self):
        self.redis_pool = redis.ConnectionPool(
            host=settings.redis_host,
            port=settings.redis_port,
            db=0,
            decode_responses=True
        )
        self._redis = None

    async def init(self):
        self._redis = redis.Redis(connection_pool=self.redis_pool)

    async def get_cache(self, key: str) -> Optional[Any]:
        if not self._redis:
            await self.init()
        data = await self._redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def set_cache(self, key: str, value: Any, expire: int = settings.redis_tte):
        if not self._redis:
            await self.init()
        await self._redis.set(key, json.dumps(value), ex=expire)

    async def delete_cache(self, key: str):
        if not self._redis:
            await self.init()
        await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.close()
            self._redis = None

    async def clear_all_cached(self):
        if not self._redis:
            await self.init()
        await self._redis.flushdb()


redis_client = RedisClient()
