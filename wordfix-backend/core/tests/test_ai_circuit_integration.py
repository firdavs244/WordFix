"""
Tests for AI circuit breaker integration.
"""

import pytest
from unittest.mock import MagicMock, patch
from django.core.cache import cache

from apps.common.circuit_breaker import CircuitBreaker, CircuitState, get_circuit
from core.services.ai.ai_factory import AIProviderFactory, FallbackAIProvider


@pytest.mark.django_db
class TestAICircuitIntegration:

    def setup_method(self):
        cache.clear()
        AIProviderFactory.reset()

    def test_groq_circuit_breaker(self):
        """Groq circuit breaker exists and starts closed."""
        circuit = get_circuit("groq")
        assert circuit.get_state() == CircuitState.CLOSED

    def test_fallback_when_circuit_open(self):
        """When all circuits are open, the factory returns FallbackAIProvider."""
        groq_circuit = get_circuit("groq")
        openai_circuit = get_circuit("openai")
        for _ in range(5):
            groq_circuit.record_failure()
            openai_circuit.record_failure()
        assert groq_circuit.get_state() == CircuitState.OPEN
        assert openai_circuit.get_state() == CircuitState.OPEN

        provider = AIProviderFactory.get_provider()
        assert isinstance(provider, FallbackAIProvider)
        # Fallback should return a string without raising
        result = provider.generate_text("hello")
        assert isinstance(result, str)

    def test_factory_switches_provider(self):
        """When groq circuit opens, factory can switch to openai or fallback."""
        groq_circuit = get_circuit("groq")
        for _ in range(5):
            groq_circuit.record_failure()
        assert groq_circuit.get_state() == CircuitState.OPEN

        # Factory should not return groq
        provider = AIProviderFactory.get_provider("groq")
        # It should be either openai (if available) or fallback
        assert provider.get_provider_name() in ("openai", "fallback")
