"""
Test settings for WordFix project.

Optimized for speed: SQLite in-memory, MD5 hasher, eager Celery.
"""

from .base import *  # noqa: F401, F403

# =============================================================================
# DEBUG
# =============================================================================

DEBUG = False

# =============================================================================
# SECRET KEY (stable for tests)
# =============================================================================

SECRET_KEY = "test-secret-key-not-for-production"

# =============================================================================
# DATABASE (Use SQLite in-memory for speed)
# =============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# =============================================================================
# PASSWORD HASHERS (MD5 for speed)
# =============================================================================

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# =============================================================================
# CACHE (Local memory for tests)
# =============================================================================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# =============================================================================
# CELERY (Synchronous for tests)
# =============================================================================

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# =============================================================================
# EMAIL
# =============================================================================

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# =============================================================================
# FILE STORAGE (In-memory for tests)
# =============================================================================

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.InMemoryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# =============================================================================
# THROTTLING (Disabled for tests)
# =============================================================================

REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []  # noqa: F405
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {}  # noqa: F405

# =============================================================================
# AI SETTINGS (Disabled for tests — we mock everything)
# =============================================================================

WORD_ENRICHMENT_ENABLED = False  # Don't auto-enrich in test AddWord
GROQ_API_KEY = ""
OPENAI_API_KEY = ""
