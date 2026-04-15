"""
JWT token service for the Auth Service.

Uses wordfix_shared.auth.jwt_utils for token creation.
Uses Redis for refresh token blacklisting.
"""

from uuid import UUID

import redis.asyncio as aioredis

from wordfix_shared.auth.jwt_utils import (
    create_access_token,
    create_refresh_token,
    create_token_pair,
    decode_token,
)

from ..config import settings


class JWTService:
    """Handles JWT token operations with Redis-backed blacklist."""

    def __init__(self, redis_url: str | None = None):
        self.redis_url = redis_url or settings.REDIS_URL
        self._redis: aioredis.Redis | None = None

    async def _get_redis(self) -> aioredis.Redis:
        if self._redis is None:
            self._redis = aioredis.from_url(self.redis_url)
        return self._redis

    def generate_tokens(self, user_id: UUID | str) -> dict[str, str]:
        """Generate access + refresh token pair."""
        return create_token_pair(
            user_id=user_id,
            secret_key=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
            access_lifetime_minutes=settings.JWT_ACCESS_LIFETIME_MINUTES,
            refresh_lifetime_days=settings.JWT_REFRESH_LIFETIME_DAYS,
        )

    def generate_access_token(self, user_id: UUID | str) -> str:
        """Generate a new access token."""
        return create_access_token(
            user_id=user_id,
            secret_key=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
            lifetime_minutes=settings.JWT_ACCESS_LIFETIME_MINUTES,
        )

    def validate_token(self, token: str) -> dict:
        """Validate and decode a token. Raises jwt errors on failure."""
        return decode_token(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)

    async def blacklist_refresh_token(self, token: str) -> None:
        """Add a refresh token to the blacklist in Redis."""
        try:
            payload = decode_token(token, settings.JWT_SECRET, settings.JWT_ALGORITHM, verify_exp=False)
            jti = payload.get("jti", "")
            # Store for the remaining lifetime of the token (7 days max)
            ttl = settings.JWT_REFRESH_LIFETIME_DAYS * 86400
            r = await self._get_redis()
            await r.setex(f"bl:token:{jti}", ttl, "1")
        except Exception:
            pass  # If token is invalid, it can't be used anyway

    async def is_token_blacklisted(self, token: str) -> bool:
        """Check if a refresh token has been blacklisted."""
        try:
            payload = decode_token(token, settings.JWT_SECRET, settings.JWT_ALGORITHM, verify_exp=False)
            jti = payload.get("jti", "")
            r = await self._get_redis()
            return await r.exists(f"bl:token:{jti}") > 0
        except Exception:
            return True  # Invalid tokens are effectively blacklisted

    async def close(self) -> None:
        """Close Redis connection."""
        if self._redis:
            await self._redis.aclose()
