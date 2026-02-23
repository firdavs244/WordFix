"""AI Provider Diagnostic Script"""
import os
print("=== ENV VARIABLES ===")
print(f"AI_PROVIDER: {os.environ.get('AI_PROVIDER', 'NOT SET')}")
groq_key = os.environ.get('GROQ_API_KEY', '')
gemini_key = os.environ.get('GEMINI_API_KEY', '')
print(f"GROQ_API_KEY: {groq_key[:20]}..." if groq_key else "GROQ_API_KEY: NOT SET")
print(f"GEMINI_API_KEY: {gemini_key[:20]}..." if gemini_key else "GEMINI_API_KEY: NOT SET")
print()

print("=== DJANGO SETTINGS ===")
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()
from django.conf import settings
print(f"AI_PROVIDER setting: {getattr(settings, 'AI_PROVIDER', 'NOT FOUND')}")
sk = getattr(settings, 'GROQ_API_KEY', '')
print(f"GROQ_API_KEY setting: {sk[:20]}..." if sk else "GROQ_API_KEY: EMPTY")
print(f"GROQ_MODEL: {getattr(settings, 'GROQ_MODEL', 'NOT FOUND')}")
gk = getattr(settings, 'GEMINI_API_KEY', '')
print(f"GEMINI_API_KEY setting: {gk[:20]}..." if gk else "GEMINI_API_KEY: EMPTY")
print(f"GEMINI_MODEL: {getattr(settings, 'GEMINI_MODEL', 'NOT FOUND')}")
print()

print("=== AI FACTORY TEST ===")
from core.services.ai.ai_factory import AIProviderFactory
AIProviderFactory.reset()
try:
    provider = AIProviderFactory.get_provider()
    print(f"Provider class: {type(provider).__name__}")
    print(f"Provider name: {provider.get_provider_name()}")
    print(f"Is available: {provider.is_available()}")
except Exception as e:
    print(f"Factory ERROR: {e}")
    import traceback
    traceback.print_exc()
    import sys
    sys.exit(1)
print()

print("=== ACTUAL API CALL TEST ===")
try:
    result = provider.generate_text("Reply with exactly one word: Hello")
    print(f"AI Response: {result}")
    print("AI IS WORKING!")
except Exception as e:
    print(f"API Call ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print()
print("=== GROQ PROVIDER DIRECT TEST ===")
try:
    AIProviderFactory.reset()
    groq_provider = AIProviderFactory.get_provider("groq")
    print(f"Groq class: {type(groq_provider).__name__}")
    print(f"Groq available: {groq_provider.is_available()}")
    result2 = groq_provider.generate_text("Say hello in one word")
    print(f"Groq Response: {result2}")
    print("GROQ IS WORKING!")
except Exception as e:
    print(f"Groq ERROR: {type(e).__name__}: {e}")

print()
print("=== GEMINI PROVIDER DIRECT TEST ===")
try:
    AIProviderFactory.reset()
    gemini_provider = AIProviderFactory.get_provider("gemini")
    print(f"Gemini class: {type(gemini_provider).__name__}")
    print(f"Gemini available: {gemini_provider.is_available()}")
    result3 = gemini_provider.generate_text("Say hello in one word")
    print(f"Gemini Response: {result3}")
    print("GEMINI IS WORKING!")
except Exception as e:
    print(f"Gemini ERROR: {type(e).__name__}: {e}")
