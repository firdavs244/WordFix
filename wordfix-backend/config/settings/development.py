"""
Development settings for WordFix project.
"""

from .base import *  # noqa: F401, F403

# =============================================================================
# DEBUG
# =============================================================================

DEBUG = True

ALLOWED_HOSTS = ["*"]

# =============================================================================
# INSTALLED APPS (Development extras)
# =============================================================================

INSTALLED_APPS += [  # noqa: F405
    "django.contrib.staticfiles",
]

# Remove duplicate staticfiles if present
INSTALLED_APPS = list(dict.fromkeys(INSTALLED_APPS))  # noqa: F405

# =============================================================================
# DATABASE (Use same as base for Docker)
# =============================================================================

# Database config inherited from base.py (PostgreSQL via Docker)

# =============================================================================
# EMAIL (Console backend for development)
# =============================================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# =============================================================================
# CORS (Allow all in development)
# =============================================================================

CORS_ALLOW_ALL_ORIGINS = True

# =============================================================================
# CACHE (Local memory for faster dev, Redis for integration testing)
# =============================================================================

# Redis cache inherited from base.py for Docker consistency

# =============================================================================
# LOGGING
# =============================================================================

LOGGING["loggers"]["apps"]["level"] = "DEBUG"  # noqa: F405
