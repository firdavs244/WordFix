"""
FastAPI dependency injection for the Auth Service.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_session
from ..infrastructure.jwt_service import JWTService
from ..infrastructure.repositories import SQLAlchemyUserRepository


async def get_repository(session: AsyncSession = Depends(get_session)):
    """Get user repository with current session."""
    return SQLAlchemyUserRepository(session)


def get_jwt_service() -> JWTService:
    """Get JWT service instance."""
    return JWTService(settings.REDIS_URL)
