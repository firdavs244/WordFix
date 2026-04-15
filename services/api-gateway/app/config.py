"""
API Gateway configuration.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """API Gateway settings from environment."""

    # Auth Service gRPC endpoint
    AUTH_SERVICE_GRPC: str = "auth-service:50051"

    # Monolith HTTP endpoint (Django)
    MONOLITH_URL: str = "http://web:8000"

    # JWT (for token validation at gateway level)
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"

    # CORS
    CORS_ORIGINS: str = "http://localhost"

    # RabbitMQ (for event publishing if needed)
    RABBITMQ_URL: str = "amqp://wordfix:wordfix_mq@rabbitmq:5672/"

    # Service info
    SERVICE_NAME: str = "api-gateway"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    HTTP_PORT: int = 8080

    model_config = {"env_prefix": "", "case_sensitive": True}


settings = Settings()
