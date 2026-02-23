"""
Google Gemini AI Provider implementation.
"""

import json
import logging
import re
import time

from django.conf import settings

from core.interfaces.ai_provider import AbstractAIProvider, AIProviderError

logger = logging.getLogger(__name__)


class GeminiProvider(AbstractAIProvider):
    """AI provider using the Google Gemini API."""

    def __init__(self):
        self._api_key = getattr(settings, "GEMINI_API_KEY", "")
        self._model = getattr(settings, "GEMINI_MODEL", "gemini-2.0-flash")
        self._timeout = getattr(settings, "AI_TIMEOUT", 30)
        self._max_retries = getattr(settings, "AI_MAX_RETRIES", 3)
        self._client = None
        self._availability_cache = None
        self._availability_cache_time = 0
        try:
            from apps.common.circuit_breaker import get_circuit

            self.circuit = get_circuit("gemini")
        except Exception:
            self.circuit = None

    def _get_client(self):
        if self._client is None:
            try:
                import google.generativeai as genai

                genai.configure(api_key=self._api_key)
                self._client = genai.GenerativeModel(self._model)
            except ImportError:
                raise AIProviderError(
                    "google-generativeai package not installed", provider="gemini"
                )
        return self._client

    def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        if not self.is_available():
            raise AIProviderError("No API key configured", provider="gemini")

        if self.circuit and not self.circuit.is_available():
            raise AIProviderError("Circuit breaker is open", provider="gemini")

        for attempt in range(self._max_retries):
            try:
                client = self._get_client()
                response = client.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": max_tokens,
                        "temperature": temperature,
                    },
                )
                result = response.text or ""
                if self.circuit:
                    self.circuit.record_success()
                return result
            except Exception as e:
                error_str = str(e).lower()
                error_name = type(e).__name__

                if "rate" in error_str or "quota" in error_str or "429" in error_str:
                    if attempt < self._max_retries - 1:
                        wait = 2**attempt
                        logger.warning(f"Gemini rate limit, retrying in {wait}s...")
                        time.sleep(wait)
                        continue
                    if self.circuit:
                        self.circuit.record_failure()
                    raise AIProviderError(
                        f"Rate limit exceeded: {e}", provider="gemini"
                    )

                if "timeout" in error_str:
                    if self.circuit:
                        self.circuit.record_failure()
                    raise AIProviderError(
                        f"Request timed out: {e}", provider="gemini"
                    )

                if attempt < self._max_retries - 1:
                    wait = 2**attempt
                    time.sleep(wait)
                    continue

                if self.circuit:
                    self.circuit.record_failure()
                raise AIProviderError(f"Unexpected error: {e}", provider="gemini")

        raise AIProviderError("Max retries exceeded", provider="gemini")

    def generate_json(
        self,
        prompt: str,
        response_schema: dict | None = None,
        max_tokens: int = 1500,
        temperature: float = 0.3,
    ) -> dict:
        if not self.is_available():
            raise AIProviderError("No API key configured", provider="gemini")

        json_prompt = f"{prompt}\n\nRespond ONLY with valid JSON. No extra text."
        max_json_retries = 2

        for attempt in range(max_json_retries + 1):
            try:
                text = self.generate_text(json_prompt, max_tokens, temperature)
                text = text.strip()
                # Strip markdown code fences
                if text.startswith("```"):
                    lines = text.split("\n")
                    text = "\n".join(lines[1:-1]) if len(lines) > 2 else text
                    text = text.strip()
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    # Try regex extraction as fallback
                    json_match = re.search(r"\{[\s\S]*\}", text)
                    if json_match:
                        return json.loads(json_match.group())
                    json_arr_match = re.search(r"\[[\s\S]*\]", text)
                    if json_arr_match:
                        return json.loads(json_arr_match.group())
                    raise
            except json.JSONDecodeError:
                if attempt < max_json_retries:
                    logger.warning(
                        f"Gemini JSON parse failed (attempt {attempt + 1}), retrying..."
                    )
                    continue
                raise AIProviderError(
                    "Failed to parse JSON response after retries", provider="gemini"
                )

    def generate_chat(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        if not self.is_available():
            raise AIProviderError("No API key configured", provider="gemini")

        for attempt in range(self._max_retries):
            try:
                client = self._get_client()
                # Convert OpenAI-style messages to Gemini format
                chat = client.start_chat(history=[])
                gemini_history = []
                last_user_msg = ""
                for msg in messages:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    if role == "system":
                        # Prepend system message to first user message
                        gemini_history.append(
                            {"role": "user", "parts": [content]}
                        )
                        gemini_history.append(
                            {"role": "model", "parts": ["Understood."]}
                        )
                    elif role == "assistant":
                        gemini_history.append(
                            {"role": "model", "parts": [content]}
                        )
                    else:
                        last_user_msg = content
                        gemini_history.append(
                            {"role": "user", "parts": [content]}
                        )

                # Rebuild chat with history
                chat = client.start_chat(history=gemini_history[:-1])
                response = chat.send_message(
                    last_user_msg or "Hello",
                    generation_config={
                        "max_output_tokens": max_tokens,
                        "temperature": temperature,
                    },
                )
                result = response.text or ""
                if self.circuit:
                    self.circuit.record_success()
                return result
            except Exception as e:
                error_str = str(e).lower()
                if "rate" in error_str or "quota" in error_str:
                    if attempt < self._max_retries - 1:
                        time.sleep(2**attempt)
                        continue
                    raise AIProviderError(
                        f"Rate limit exceeded: {e}", provider="gemini"
                    )
                if attempt < self._max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                raise AIProviderError(f"Chat error: {e}", provider="gemini")

        raise AIProviderError("Max retries exceeded", provider="gemini")

    def get_provider_name(self) -> str:
        return "gemini"

    def is_available(self) -> bool:
        now = time.time()
        if (
            self._availability_cache is not None
            and (now - self._availability_cache_time) < 300
        ):
            return self._availability_cache
        available = bool(self._api_key)
        self._availability_cache = available
        self._availability_cache_time = now
        return available
