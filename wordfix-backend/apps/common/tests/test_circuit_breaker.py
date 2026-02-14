"""
Tests for Circuit Breaker.
"""

import time

import pytest
from django.core.cache import cache

from apps.common.circuit_breaker import (
    CircuitBreaker,
    CircuitOpenError,
    CircuitState,
    get_circuit,
)


@pytest.mark.django_db
class TestCircuitBreaker:

    def setup_method(self):
        cache.clear()
        self.cb = CircuitBreaker("test_service", failure_threshold=3, recovery_timeout=1)
        self.cb.reset()

    def test_initial_state_closed(self):
        """A new circuit breaker starts in CLOSED state."""
        assert self.cb.get_state() == CircuitState.CLOSED

    def test_record_success_keeps_closed(self):
        """Successful calls keep the circuit CLOSED."""
        self.cb.record_success()
        assert self.cb.get_state() == CircuitState.CLOSED

    def test_failures_open_circuit(self):
        """Reaching failure_threshold opens the circuit."""
        for _ in range(3):
            self.cb.record_failure()
        assert self.cb.get_state() == CircuitState.OPEN

    def test_open_rejects_calls(self):
        """OPEN circuit raises CircuitOpenError."""
        for _ in range(3):
            self.cb.record_failure()

        with pytest.raises(CircuitOpenError):
            self.cb.call(lambda: "should not run")

    def test_half_open_after_timeout(self):
        """After recovery_timeout, circuit transitions to HALF_OPEN."""
        for _ in range(3):
            self.cb.record_failure()
        assert self.cb.get_state() == CircuitState.OPEN

        # Wait for recovery
        time.sleep(1.1)
        assert self.cb.get_state() == CircuitState.HALF_OPEN

    def test_success_closes_half_open(self):
        """A success in HALF_OPEN moves the circuit back to CLOSED."""
        for _ in range(3):
            self.cb.record_failure()
        time.sleep(1.1)
        assert self.cb.get_state() == CircuitState.HALF_OPEN

        self.cb.record_success()
        assert self.cb.get_state() == CircuitState.CLOSED

    def test_failure_reopens_from_half_open(self):
        """A failure in HALF_OPEN re-opens the circuit."""
        for _ in range(3):
            self.cb.record_failure()
        time.sleep(1.1)
        assert self.cb.get_state() == CircuitState.HALF_OPEN

        # Enough failures to trip again
        for _ in range(3):
            self.cb.record_failure()
        assert self.cb.get_state() == CircuitState.OPEN
