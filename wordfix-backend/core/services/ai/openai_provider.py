"""
OpenAI AI Provider implementation.
"""

import json
import logging
import time

from django.conf import settings

from core.interfaces.ai_provider import AbstractAIProvider, AIProviderError

logger = logging.getLogger(__name__)


class OpenAIProvider(AbstractAIProvider):
    """AI provider using the OpenAI API."""

    def __init__(self):
        self._api_key = getattr(settings, "OPENAI_API_KEY", "")
        self._model = getattr(settings, "OPENAI_MODEL", "gpt-4o-mini")
        self._timeout = getattr(settings, "AI_TIMEOUT", 30)
        self._max_retries = getattr(settings, "AI_MAX_RETRIES", 3)
        self._client = None
        self._availability_cache = None
        self._availability_cache_time = 0
        try:
            from apps.common.circuit_breaker import get_circuit
            self.circuit = get_circuit("openai")
        except Exception:
            self.circuit = None

    def _get_client(self):
        if self._client is None:
            try:
                import openai

                self._client = openai.OpenAI(
                    api_key=self._api_key,
                    timeout=self._timeout,
                )
            except ImportError:
                raise AIProviderError("openai package not installed", provider="openai")
        return self._client

    def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        if not self.is_available():
            raise AIProviderError("No API key configured", provider="openai")

        if self.circuit and not self.circuit.is_available():
            raise AIProviderError("Circuit breaker open", provider="openai")

        for attempt in range(self._max_retries):
            try:
                client = self._get_client()
                response = client.chat.completions.create(
                    model=self._model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                result = response.choices[0].message.content or ""
                if self.circuit:
                    self.circuit.record_success()
                return result
            except Exception as e:
                error_name = type(e).__name__
                if "RateLimitError" in error_name:
                    if attempt < self._max_retries - 1:
                        wait = (2**attempt)
                        logger.warning(f"OpenAI rate limit, retrying in {wait}s...")
                        time.sleep(wait)
                        continue
                    if self.circuit:
                        self.circuit.record_failure()
                    raise AIProviderError(f"Rate limit exceeded: {e}", provider="openai")
                if "APIError" in error_name or "APIConnectionError" in error_name:
                    if attempt < self._max_retries - 1:
                        time.sleep(2**attempt)
                        continue
                    if self.circuit:
                        self.circuit.record_failure()
                    raise AIProviderError(f"API error: {e}", provider="openai")
                if "APITimeoutError" in error_name:
                    if self.circuit:
                        self.circuit.record_failure()
                    raise AIProviderError(f"Request timed out: {e}", provider="openai")
                if self.circuit:
                    self.circuit.record_failure()
                raise AIProviderError(f"Unexpected error: {e}", provider="openai")

        raise AIProviderError("Max retries exceeded", provider="openai")

    def generate_json(
        self,
        prompt: str,
        response_schema: dict | None = None,
        max_tokens: int = 1500,
        temperature: float = 0.3,
    ) -> dict:
        if not self.is_available():
            raise AIProviderError("No API key configured", provider="openai")

        json_prompt = f"{prompt}\n\nRespond ONLY with valid JSON. No extra text."
        max_json_retries = 2

        for attempt in range(max_json_retries + 1):
            try:
                client = self._get_client()
                response = client.chat.completions.create(
                    model=self._model,
                    messages=[{"role": "user", "content": json_prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    response_format={"type": "json_object"},
                )
                text = response.choices[0].message.content or ""
                return json.loads(text)
            except json.JSONDecodeError:
                if attempt < max_json_retries:
                    logger.warning(
                        f"OpenAI JSON parse failed (attempt {attempt + 1}), retrying..."
                    )
                    continue
                raise AIProviderError(
                    "Failed to parse JSON response after retries", provider="openai"
                )
            except Exception as e:
                error_name = type(e).__name__
                if "RateLimitError" in error_name:
                    if attempt < max_json_retries:
                        time.sleep(2**attempt)
                        continue
                    raise AIProviderError(f"Rate limit exceeded: {e}", provider="openai")
                raise AIProviderError(f"JSON generation error: {e}", provider="openai")

    def generate_chat(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        if not self.is_available():
            raise AIProviderError("No API key configured", provider="openai")

        for attempt in range(self._max_retries):
            try:
                client = self._get_client()
                response = client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                return response.choices[0].message.content or ""
            except Exception as e:
                error_name = type(e).__name__
                if "RateLimitError" in error_name:
                    if attempt < self._max_retries - 1:
                        time.sleep(2**attempt)
                        continue
                    raise AIProviderError(f"Rate limit exceeded: {e}", provider="openai")
                if attempt < self._max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                raise AIProviderError(f"Chat error: {e}", provider="openai")

        raise AIProviderError("Max retries exceeded", provider="openai")

    def get_provider_name(self) -> str:
        return "openai"

    def is_available(self) -> bool:
        now = time.time()
        if self._availability_cache is not None and (now - self._availability_cache_time) < 300:
            return self._availability_cache
        available = bool(self._api_key)
        self._availability_cache = available
        self._availability_cache_time = now
        return available
