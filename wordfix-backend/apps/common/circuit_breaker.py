"""
Circuit Breaker pattern implementation for WordFix.

Prevents cascading failures by tracking errors and stopping calls
to failing services after a threshold is reached.
"""

import enum
import logging
import time

from django.core.cache import cache

logger = logging.getLogger(__name__)


class CircuitState(enum.Enum):
    """States of a circuit breaker."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitOpenError(Exception):
    """Raised when a circuit breaker is open and rejecting calls."""

    def __init__(self, name: str, recovery_seconds: float = 0):
        self.name = name
        self.recovery_seconds = recovery_seconds
        super().__init__(f"Circuit '{name}' is OPEN. Service unavailable.")


class CircuitBreaker:
    """
    Circuit breaker that tracks failures and trips after a threshold.

    States:
        CLOSED  — Normal, calls pass through.
        OPEN    — All calls rejected immediately.
        HALF_OPEN — One test call allowed; success closes, failure re-opens.
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._cache_prefix = f"circuit_breaker:{name}"

    # -- Cache keys --

    @property
    def _state_key(self) -> str:
        return f"{self._cache_prefix}:state"

    @property
    def _failures_key(self) -> str:
        return f"{self._cache_prefix}:failures"

    @property
    def _last_failure_key(self) -> str:
        return f"{self._cache_prefix}:last_failure"

    # -- State management --

    def _get_raw_state(self) -> str:
        return cache.get(self._state_key, CircuitState.CLOSED.value)

    def _set_state(self, state: CircuitState) -> None:
        cache.set(self._state_key, state.value, timeout=None)

    def _get_failures(self) -> int:
        return cache.get(self._failures_key, 0)

    def _set_failures(self, count: int) -> None:
        cache.set(self._failures_key, count, timeout=None)

    def _get_last_failure_time(self) -> float:
        return cache.get(self._last_failure_key, 0.0)

    def _set_last_failure_time(self, ts: float) -> None:
        cache.set(self._last_failure_key, ts, timeout=None)

    def get_state(self) -> CircuitState:
        """
        Return the effective state, transitioning OPEN → HALF_OPEN
        if the recovery timeout has elapsed.
        """
        raw = self._get_raw_state()

        if raw == CircuitState.OPEN.value:
            last_failure = self._get_last_failure_time()
            if time.time() - last_failure >= self.recovery_timeout:
                self._set_state(CircuitState.HALF_OPEN)
                logger.info(f"Circuit '{self.name}' transitioned to HALF_OPEN")
                return CircuitState.HALF_OPEN
            return CircuitState.OPEN

        return CircuitState(raw)

    def record_success(self) -> None:
        """Record a successful call — reset failures, close circuit."""
        self._set_failures(0)
        self._set_state(CircuitState.CLOSED)

    def record_failure(self) -> None:
        """Record a failed call — increment counter, trip if threshold reached."""
        failures = self._get_failures() + 1
        self._set_failures(failures)
        self._set_last_failure_time(time.time())

        if failures >= self.failure_threshold:
            self._set_state(CircuitState.OPEN)
            logger.warning(
                f"Circuit '{self.name}' OPENED after {failures} failures"
            )

    def call(self, func, *args, **kwargs):
        """
        Execute *func* through the circuit breaker.

        Raises CircuitOpenError if the circuit is OPEN.
        """
        state = self.get_state()

        if state == CircuitState.OPEN:
            raise CircuitOpenError(
                self.name,
                recovery_seconds=self.recovery_timeout,
            )

        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except CircuitOpenError:
            raise
        except Exception as exc:
            self.record_failure()
            raise exc

    def is_available(self) -> bool:
        """Return True if the circuit is not OPEN."""
        return self.get_state() != CircuitState.OPEN

    def reset(self) -> None:
        """Reset the circuit breaker to CLOSED state."""
        self._set_failures(0)
        self._set_state(CircuitState.CLOSED)
        cache.delete(self._last_failure_key)


# ── Global circuit instances ────────────────────────────────────

CIRCUITS: dict[str, CircuitBreaker] = {
    "groq": CircuitBreaker("groq", failure_threshold=5, recovery_timeout=60),
    "openai": CircuitBreaker("openai", failure_threshold=5, recovery_timeout=60),
    "gemini": CircuitBreaker("gemini", failure_threshold=5, recovery_timeout=60),
    "tts": CircuitBreaker("tts", failure_threshold=3, recovery_timeout=30),
}


def get_circuit(name: str) -> CircuitBreaker:
    """
    Get a named circuit breaker, creating one if it doesn't exist.

    Args:
        name: Service name (e.g. 'groq', 'openai', 'tts').

    Returns:
        CircuitBreaker instance for the named service.
    """
    if name not in CIRCUITS:
        CIRCUITS[name] = CircuitBreaker(name)
    return CIRCUITS[name]
