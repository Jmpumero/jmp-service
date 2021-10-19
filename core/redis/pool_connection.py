import aioredis
import logging

from config import config

global_settings = config.Settings()


async def get_redis() -> aioredis.Redis:

    if global_settings.redis_password:
        redis = await aioredis.from_url(
            global_settings.redis_url,
            password=global_settings.redis_password,
            encoding="utf-8",
            db=global_settings.redis_db,
        )

    redis = await aioredis.from_url(
        global_settings.redis_url,
        encoding="utf-8",
        db=global_settings.redis_db,
    )

    logger = logging.getLogger("uvicorn")

    logger.info(f"REDIS: {global_settings.redis_url}")

    try:
        yield redis
    finally:
        await redis.close()
