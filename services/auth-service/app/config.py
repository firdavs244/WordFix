"""
Auth Service configuration via environment variables.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Auth Service settings loaded from environment."""

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://auth_user:auth_pass@auth-db:5432/wordfix_auth"

    # JWT (must match monolith SECRET_KEY for token compatibility)
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_LIFETIME_MINUTES: int = 60
    JWT_REFRESH_LIFETIME_DAYS: int = 7

    # RabbitMQ
    RABBITMQ_URL: str = "amqp://wordfix:wordfix_mq@rabbitmq:5672/"

    # Redis (for token blacklist)
    REDIS_URL: str = "redis://redis:6379/3"

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    # gRPC
    GRPC_PORT: int = 50051

    # HTTP
    HTTP_PORT: int = 8001

    # Service info
    SERVICE_NAME: str = "auth-service"
    VERSION: str = "0.1.0"
    DEBUG: bool = False

    model_config = {"env_prefix": "", "case_sensitive": True}


settings = Settings()
