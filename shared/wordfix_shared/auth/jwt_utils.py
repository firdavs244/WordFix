"""
JWT utility functions for WordFix microservices.

Generates tokens compatible with Django SimpleJWT so that
tokens issued by the Auth Service are accepted by the monolith.

SimpleJWT access token payload format:
    {
        "token_type": "access",
        "exp": <timestamp>,
        "iat": <timestamp>,
        "jti": <uuid>,
        "user_id": <uuid-string>
    }
"""

import uuid
from datetime import datetime, timedelta, timezone

import jwt


DEFAULT_ALGORITHM = "HS256"
DEFAULT_ACCESS_LIFETIME_MINUTES = 60
DEFAULT_REFRESH_LIFETIME_DAYS = 7


def create_access_token(
    user_id: str | uuid.UUID,
    secret_key: str,
    algorithm: str = DEFAULT_ALGORITHM,
    lifetime_minutes: int = DEFAULT_ACCESS_LIFETIME_MINUTES,
) -> str:
    """Create a JWT access token compatible with SimpleJWT."""
    now = datetime.now(timezone.utc)
    payload = {
        "token_type": "access",
        "exp": now + timedelta(minutes=lifetime_minutes),
        "iat": now,
        "jti": uuid.uuid4().hex,
        "user_id": str(user_id),
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def create_refresh_token(
    user_id: str | uuid.UUID,
    secret_key: str,
    algorithm: str = DEFAULT_ALGORITHM,
    lifetime_days: int = DEFAULT_REFRESH_LIFETIME_DAYS,
) -> str:
    """Create a JWT refresh token compatible with SimpleJWT."""
    now = datetime.now(timezone.utc)
    payload = {
        "token_type": "refresh",
        "exp": now + timedelta(days=lifetime_days),
        "iat": now,
        "jti": uuid.uuid4().hex,
        "user_id": str(user_id),
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def create_token_pair(
    user_id: str | uuid.UUID,
    secret_key: str,
    algorithm: str = DEFAULT_ALGORITHM,
    access_lifetime_minutes: int = DEFAULT_ACCESS_LIFETIME_MINUTES,
    refresh_lifetime_days: int = DEFAULT_REFRESH_LIFETIME_DAYS,
) -> dict[str, str]:
    """Create both access and refresh tokens. Returns {access, refresh}."""
    return {
        "access": create_access_token(user_id, secret_key, algorithm, access_lifetime_minutes),
        "refresh": create_refresh_token(user_id, secret_key, algorithm, refresh_lifetime_days),
    }


def decode_token(
    token: str,
    secret_key: str,
    algorithm: str = DEFAULT_ALGORITHM,
    verify_exp: bool = True,
) -> dict:
    """
    Decode and validate a JWT token.

    Returns the payload dict.
    Raises jwt.ExpiredSignatureError if expired.
    Raises jwt.InvalidTokenError for other issues.
    """
    return jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm],
        options={"verify_exp": verify_exp},
    )
