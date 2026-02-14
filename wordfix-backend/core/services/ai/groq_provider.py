"""
Groq AI Provider implementation.
"""

import json
import logging
import time

from django.conf import settings

from core.interfaces.ai_provider import AbstractAIProvider, AIProviderError

logger = logging.getLogger(__name__)


class GroqProvider(AbstractAIProvider):
    """AI provider using the Groq API."""

    def __init__(self):
        self._api_key = getattr(settings, "GROQ_API_KEY", "")
        self._model = getattr(settings, "GROQ_MODEL", "llama-3.3-70b-versatile")
        self._timeout = getattr(settings, "AI_TIMEOUT", 30)
        self._max_retries = getattr(settings, "AI_MAX_RETRIES", 3)
        self._client = None
        self._availability_cache = None
        self._availability_cache_time = 0
        try:
            from apps.common.circuit_breaker import get_circuit
            self.circuit = get_circuit("groq")
        except Exception:
            self.circuit = None

    def _get_client(self):
        if self._client is None:
            try:
                import groq

                self._client = groq.Groq(
                    api_key=self._api_key,
                    timeout=self._timeout,
                )
            except ImportError:
                raise AIProviderError("groq package not installed", provider="groq")
        return self._client

    def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        if not self.is_available():
            raise AIProviderError("No API key configured", provider="groq")

        if self.circuit and not self.circuit.is_available():
            raise AIProviderError("Circuit breaker is open", provider="groq")

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
                        logger.warning(f"Groq rate limit, retrying in {wait}s...")
                        time.sleep(wait)
                        continue
                    if self.circuit:
                        self.circuit.record_failure()
                    raise AIProviderError(f"Rate limit exceeded: {e}", provider="groq")
                if "APIError" in error_name or "APIConnectionError" in error_name:
                    if attempt < self._max_retries - 1:
                        wait = (2**attempt)
                        time.sleep(wait)
                        continue
                    if self.circuit:
                        self.circuit.record_failure()
                    raise AIProviderError(f"API error: {e}", provider="groq")
                if "APITimeoutError" in error_name:
                    if self.circuit:
                        self.circuit.record_failure()
                    raise AIProviderError(f"Request timed out: {e}", provider="groq")
                if self.circuit:
                    self.circuit.record_failure()
                raise AIProviderError(f"Unexpected error: {e}", provider="groq")

        raise AIProviderError("Max retries exceeded", provider="groq")

    def generate_json(
        self,
        prompt: str,
        response_schema: dict | None = None,
        max_tokens: int = 1500,
        temperature: float = 0.3,
    ) -> dict:
        if not self.is_available():
            raise AIProviderError("No API key configured", provider="groq")

        json_prompt = f"{prompt}\n\nRespond ONLY with valid JSON. No extra text."
        max_json_retries = 2

        for attempt in range(max_json_retries + 1):
            try:
                text = self.generate_text(json_prompt, max_tokens, temperature)
                # Try to extract JSON from the response
                text = text.strip()
                if text.startswith("```"):
                    lines = text.split("\n")
                    text = "\n".join(lines[1:-1]) if len(lines) > 2 else text
                    text = text.strip()
                return json.loads(text)
            except json.JSONDecodeError:
                if attempt < max_json_retries:
                    logger.warning(
                        f"Groq JSON parse failed (attempt {attempt + 1}), retrying..."
                    )
                    continue
                raise AIProviderError(
                    "Failed to parse JSON response after retries", provider="groq"
                )

    def generate_chat(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        if not self.is_available():
            raise AIProviderError("No API key configured", provider="groq")

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
                    raise AIProviderError(f"Rate limit exceeded: {e}", provider="groq")
                if attempt < self._max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                raise AIProviderError(f"Chat error: {e}", provider="groq")

        raise AIProviderError("Max retries exceeded", provider="groq")

    def get_provider_name(self) -> str:
        return "groq"

    def is_available(self) -> bool:
        now = time.time()
        if self._availability_cache is not None and (now - self._availability_cache_time) < 300:
            return self._availability_cache
        available = bool(self._api_key)
        self._availability_cache = available
        self._availability_cache_time = now
        return available
