"""
RabbitMQ event consumer base for WordFix microservices.

Provides a base class for consuming events from the topic exchange.
"""

import logging
from collections.abc import Awaitable, Callable
from typing import Any

import aio_pika

from .schemas import EventEnvelope

logger = logging.getLogger(__name__)

EXCHANGE_NAME = "wordfix.events"

EventHandler = Callable[[EventEnvelope], Awaitable[None]]


class EventConsumer:
    """Consumes events from RabbitMQ topic exchange."""

    def __init__(self, rabbitmq_url: str, queue_name: str):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._handlers: dict[str, list[EventHandler]] = {}

    def on(self, event_type: str, handler: EventHandler) -> None:
        """Register a handler for an event type."""
        self._handlers.setdefault(event_type, []).append(handler)

    async def start(self, binding_keys: list[str] | None = None) -> None:
        """
        Connect and start consuming events.

        Args:
            binding_keys: Routing key patterns to bind (e.g. ["user.*", "xp.awarded"]).
                         Defaults to ["#"] (all events).
        """
        self._connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=10)

        exchange = await self._channel.declare_exchange(
            EXCHANGE_NAME,
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        queue = await self._channel.declare_queue(
            self.queue_name,
            durable=True,
        )

        for key in (binding_keys or ["#"]):
            await queue.bind(exchange, routing_key=key)

        await queue.consume(self._process_message)
        logger.info(
            "Consumer started: queue=%s, bindings=%s",
            self.queue_name,
            binding_keys or ["#"],
        )

    async def _process_message(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        """Process an incoming message."""
        async with message.process():
            try:
                event = EventEnvelope.from_json_bytes(message.body)
                handlers = self._handlers.get(event.event_type, [])

                if not handlers:
                    logger.debug("No handler for event: %s", event.event_type)
                    return

                for handler in handlers:
                    await handler(event)

                logger.info(
                    "Processed event: %s (id=%s)",
                    event.event_type,
                    event.event_id,
                )
            except Exception:
                logger.exception("Failed to process message")

    async def close(self) -> None:
        """Close connection."""
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
