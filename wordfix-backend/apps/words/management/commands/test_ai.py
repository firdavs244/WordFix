"""
Management command to test AI provider connectivity.

Usage:
    python manage.py test_ai              # Test active provider
    python manage.py test_ai --provider gemini   # Test specific provider
    python manage.py test_ai --all         # Test all providers
    python manage.py test_ai --enrich apple  # Test word enrichment
"""

import json
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from core.services.ai.ai_factory import AIProviderFactory


class Command(BaseCommand):
    help = "Test AI provider connectivity and response quality"

    def add_arguments(self, parser):
        parser.add_argument(
            "--provider",
            type=str,
            choices=["gemini", "groq", "openai"],
            help="Test a specific provider (default: active provider from settings)",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Test all configured providers",
        )
        parser.add_argument(
            "--enrich",
            type=str,
            metavar="WORD",
            help='Test word enrichment for a specific word (e.g. --enrich "apple")',
        )

    def handle(self, *args, **options):
        self.stdout.write("")
        self.stdout.write(self.style.HTTP_INFO("=" * 60))
        self.stdout.write(self.style.HTTP_INFO("  WordFix AI Provider Test"))
        self.stdout.write(self.style.HTTP_INFO("=" * 60))

        # Show current config
        active = getattr(settings, "AI_PROVIDER", "gemini")
        self.stdout.write(f"\n  Active provider (settings): {self.style.SUCCESS(active)}")
        self.stdout.write(f"  GEMINI_API_KEY: {'***' + settings.GEMINI_API_KEY[-4:] if settings.GEMINI_API_KEY else self.style.WARNING('not set')}")
        self.stdout.write(f"  GROQ_API_KEY:   {'***' + settings.GROQ_API_KEY[-4:] if settings.GROQ_API_KEY else self.style.WARNING('not set')}")
        self.stdout.write(f"  OPENAI_API_KEY: {'***' + settings.OPENAI_API_KEY[-4:] if settings.OPENAI_API_KEY else self.style.WARNING('not set')}")
        self.stdout.write("")

        if options["all"]:
            self._test_all_providers()
        elif options["enrich"]:
            self._test_enrichment(options["enrich"], options.get("provider"))
        else:
            provider_name = options.get("provider") or active
            self._test_provider(provider_name)

    def _test_provider(self, name: str):
        """Test a single provider with generate_text and generate_json."""
        self.stdout.write(self.style.HTTP_INFO(f"--- Testing: {name.upper()} ---"))

        # Reset factory cache to force fresh creation
        AIProviderFactory.reset()

        try:
            provider = AIProviderFactory._create_provider(name)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  Failed to create provider: {e}"))
            return False

        # Check availability
        available = provider.is_available()
        if not available:
            self.stdout.write(self.style.ERROR(f"  Provider '{name}' is NOT available (API key missing or invalid)"))
            return False

        self.stdout.write(self.style.SUCCESS(f"  Provider created: {provider.get_provider_name()}"))
        self.stdout.write(f"  is_available(): {self.style.SUCCESS('True')}")

        # Test 1: generate_text
        self.stdout.write(f"\n  [1] generate_text:")
        prompt = 'Translate to Uzbek in 5 words or less: "Hello, how are you?"'
        start = time.time()
        try:
            result = provider.generate_text(prompt, max_tokens=50, temperature=0.3)
            elapsed = time.time() - start
            self.stdout.write(self.style.SUCCESS(f"      OK ({elapsed:.2f}s)"))
            self.stdout.write(f"      Prompt:   {prompt}")
            self.stdout.write(f"      Response: {result.strip()}")
        except Exception as e:
            elapsed = time.time() - start
            self.stdout.write(self.style.ERROR(f"      FAILED ({elapsed:.2f}s): {e}"))
            return False

        # Test 2: generate_json
        self.stdout.write(f"\n  [2] generate_json:")
        prompt_json = (
            'Return a JSON object with these keys: '
            '"word" (string), "translation" (string in Uzbek), "example" (string). '
            'The word is "beautiful".'
        )
        start = time.time()
        try:
            result_json = provider.generate_json(prompt_json, max_tokens=200, temperature=0.3)
            elapsed = time.time() - start
            self.stdout.write(self.style.SUCCESS(f"      OK ({elapsed:.2f}s)"))
            self.stdout.write(f"      Response: {json.dumps(result_json, ensure_ascii=False, indent=6)}")
        except Exception as e:
            elapsed = time.time() - start
            self.stdout.write(self.style.ERROR(f"      FAILED ({elapsed:.2f}s): {e}"))
            return False

        self.stdout.write(self.style.SUCCESS(f"\n  {name.upper()} — All tests PASSED\n"))
        return True

    def _test_all_providers(self):
        """Test all 3 providers."""
        results = {}
        for name in ["gemini", "groq", "openai"]:
            ok = self._test_provider(name)
            results[name] = ok
            self.stdout.write("")

        # Summary
        self.stdout.write(self.style.HTTP_INFO("=" * 60))
        self.stdout.write(self.style.HTTP_INFO("  Summary"))
        self.stdout.write(self.style.HTTP_INFO("=" * 60))
        for name, ok in results.items():
            status = self.style.SUCCESS("PASS") if ok else self.style.ERROR("FAIL")
            self.stdout.write(f"  {name:10s} — {status}")

        # Provider status from factory
        self.stdout.write("")
        AIProviderFactory.reset()
        status_data = AIProviderFactory.get_all_provider_status()
        self.stdout.write(f"  Active provider: {self.style.SUCCESS(status_data['active_provider'])}")
        self.stdout.write(f"  Fallback active: {status_data['fallback_active']}")
        self.stdout.write("")

    def _test_enrichment(self, word: str, provider_name: str | None = None):
        """Test word enrichment pipeline for a given word."""
        self.stdout.write(self.style.HTTP_INFO(f"--- Enrichment test: '{word}' ---\n"))

        AIProviderFactory.reset()
        if provider_name:
            provider = AIProviderFactory._create_provider(provider_name)
        else:
            provider = AIProviderFactory.get_provider()

        self.stdout.write(f"  Provider: {provider.get_provider_name()}")

        enrichment_prompt = f"""You are a language learning assistant. Provide enrichment data for the English word "{word}".
Return a JSON object with:
- "word": the word
- "definition": clear English definition (1-2 sentences)
- "uzbek_translation": translation in Uzbek
- "example_sentence": an example sentence using the word
- "difficulty_level": one of "beginner", "intermediate", "advanced"
- "part_of_speech": e.g. "noun", "verb", "adjective"
- "synonyms": list of 2-3 synonyms
- "pronunciation_guide": simple pronunciation guide

Return ONLY valid JSON, no extra text."""

        start = time.time()
        try:
            result = provider.generate_json(enrichment_prompt, max_tokens=500, temperature=0.3)
            elapsed = time.time() - start
            self.stdout.write(self.style.SUCCESS(f"  OK ({elapsed:.2f}s)\n"))
            self.stdout.write(f"  {json.dumps(result, ensure_ascii=False, indent=4)}")
        except Exception as e:
            elapsed = time.time() - start
            self.stdout.write(self.style.ERROR(f"  FAILED ({elapsed:.2f}s): {e}"))

        self.stdout.write("")
