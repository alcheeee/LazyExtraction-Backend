import json
from typing import Optional, Any
import redis.asyncio as redis
from ..config import settings
from ..utils import MyLogger


class RedisClient:
    def __init__(self):
        self.redis_pool = redis.ConnectionPool(
            host=settings.redis_host,
            port=settings.redis_port,
            db=0,
            decode_responses=True
        )
        self._redis = redis.Redis(connection_pool=self.redis_pool)

    async def get_cache(self, key: str) -> Optional[Any]:
        data = await self._redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def set_cache(self, key: str, value: Any, expire: int = settings.redis_tte):
        await self._redis.set(key, json.dumps(value), ex=expire)

    async def delete_cache(self, key: str):
        await self._redis.delete(key)

    async def clear_all_cached(self):
        await self._redis.flushdb()


redis_client = RedisClient()
