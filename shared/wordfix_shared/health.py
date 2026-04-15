"""
Common health check utilities for WordFix microservices.
"""

from typing import Any


async def check_postgres(engine) -> dict[str, str]:
    """Check PostgreSQL connectivity via SQLAlchemy async engine."""
    try:
        from sqlalchemy import text
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "up"}
    except Exception as e:
        return {"status": "down", "error": str(e)}


async def check_redis(redis_url: str) -> dict[str, str]:
    """Check Redis connectivity."""
    try:
        import redis.asyncio as aioredis
        r = aioredis.from_url(redis_url)
        await r.ping()
        await r.aclose()
        return {"status": "up"}
    except Exception as e:
        return {"status": "down", "error": str(e)}


async def check_rabbitmq(rabbitmq_url: str) -> dict[str, str]:
    """Check RabbitMQ connectivity."""
    try:
        import aio_pika
        connection = await aio_pika.connect_robust(rabbitmq_url, timeout=5)
        await connection.close()
        return {"status": "up"}
    except Exception as e:
        return {"status": "down", "error": str(e)}
