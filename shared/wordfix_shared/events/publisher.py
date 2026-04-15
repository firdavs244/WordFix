"""
RabbitMQ event publisher for WordFix microservices.

Uses aio-pika for async publishing to a topic exchange.
"""

import logging
from typing import Any

import aio_pika

from .schemas import EventEnvelope, create_event

logger = logging.getLogger(__name__)

EXCHANGE_NAME = "wordfix.events"


class EventPublisher:
    """Publishes events to RabbitMQ topic exchange."""

    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._exchange: aio_pika.abc.AbstractExchange | None = None

    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        self._connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            EXCHANGE_NAME,
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )
        logger.info("Connected to RabbitMQ exchange: %s", EXCHANGE_NAME)

    async def close(self) -> None:
        """Close connection."""
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            logger.info("RabbitMQ connection closed")

    async def publish(
        self,
        event_type: str,
        payload: dict[str, Any],
        source: str,
        correlation_id: str | None = None,
        routing_key: str | None = None,
    ) -> EventEnvelope:
        """
        Publish an event to the exchange.

        Args:
            event_type: Event type string (e.g. "user.registered")
            payload: Event data
            source: Publishing service name
            correlation_id: Optional correlation ID for tracing
            routing_key: Optional routing key (defaults to event_type)

        Returns:
            The published EventEnvelope
        """
        if not self._exchange:
            await self.connect()

        event = create_event(event_type, payload, source, correlation_id)
        message = aio_pika.Message(
            body=event.to_json_bytes(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            message_id=event.event_id,
            correlation_id=event.correlation_id,
        )

        await self._exchange.publish(
            message,
            routing_key=routing_key or event_type,
        )

        logger.info("Published event: %s (id=%s)", event_type, event.event_id)
        return event
