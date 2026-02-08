"""
Tests for AI provider abstract interface.
"""

import pytest

from core.interfaces.ai_provider import AbstractAIProvider


class TestAbstractAIProvider:
    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            AbstractAIProvider()
