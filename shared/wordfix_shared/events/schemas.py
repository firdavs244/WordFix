"""
Event envelope schema for WordFix microservices.

Every event published to RabbitMQ follows this envelope format.
"""

import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class EventEnvelope(BaseModel):
    """Standard event envelope for all WordFix events."""

    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str  # e.g. "user.registered"
    event_version: str = "1.0"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source: str  # e.g. "auth-service"
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    payload: dict[str, Any] = Field(default_factory=dict)

    def to_json_bytes(self) -> bytes:
        """Serialize to JSON bytes for RabbitMQ."""
        return self.model_dump_json().encode("utf-8")

    @classmethod
    def from_json_bytes(cls, data: bytes) -> "EventEnvelope":
        """Deserialize from JSON bytes."""
        return cls.model_validate_json(data)


def create_event(
    event_type: str,
    payload: dict[str, Any],
    source: str,
    correlation_id: str | None = None,
) -> EventEnvelope:
    """Helper to create a new event envelope."""
    return EventEnvelope(
        event_type=event_type,
        payload=payload,
        source=source,
        correlation_id=correlation_id or str(uuid.uuid4()),
    )
