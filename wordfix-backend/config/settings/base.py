"""
Base Django settings for WordFix project.

Common settings shared across all environments.
All ENV variables have graceful defaults — project starts without .env file.
"""

import os
from datetime import timedelta
from pathlib import Path

from decouple import Csv, config

# =============================================================================
# PATHS
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =============================================================================
# SECURITY
# =============================================================================

SECRET_KEY = config("SECRET_KEY", default="dev-secret-key-change-in-production")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1,0.0.0.0", cast=Csv())

# =============================================================================
# APPLICATIONS
# =============================================================================

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django.contrib.sites",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_celery_beat",
    "django_filters",
    "drf_spectacular",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "dj_rest_auth",
    "dj_rest_auth.registration",
]

LOCAL_APPS = [
    "apps.common",
    "apps.users.apps.UsersConfig",
    "apps.words.apps.WordsConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# =============================================================================
# CUSTOM USER MODEL
# =============================================================================

AUTH_USER_MODEL = "users.CustomUser"

# =============================================================================
# MIDDLEWARE
# =============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.common.middleware.request_id.RequestIDMiddleware",
    "apps.common.idempotency.IdempotencyMiddleware",
    "apps.common.logging.RequestLoggingMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

# =============================================================================
# TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# =============================================================================
# DATABASE — SQLite fallback when no env
# =============================================================================

_db_engine = config("DB_ENGINE", default="")

if _db_engine == "postgresql" or config("POSTGRES_DB", default=""):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_DB", default="wordfix"),
            "USER": config("POSTGRES_USER", default="wordfix_user"),
            "PASSWORD": config("POSTGRES_PASSWORD", default="wordfix_pass"),
            "HOST": config("POSTGRES_HOST", default="db"),
            "PORT": config("POSTGRES_PORT", default="5432"),
            "OPTIONS": {
                "connect_timeout": 10,
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC FILES
# =============================================================================

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# =============================================================================
# DEFAULT PRIMARY KEY
# =============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============================================================================
# REST FRAMEWORK
# =============================================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "apps.common.pagination.StandardResultsPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_RENDERER_CLASSES": (
        "apps.common.renderers.CustomJSONRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "EXCEPTION_HANDLER": "apps.common.exception_handler.custom_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "apps.common.rate_limiter.CRUDRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# =============================================================================
# SIMPLE JWT
# =============================================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# =============================================================================
# CORS
# =============================================================================

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173",
    cast=Csv(),
)

CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# CACHE — LocMemCache fallback when no Redis
# =============================================================================

_redis_url = config("REDIS_URL", default="")

if _redis_url:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": _redis_url,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "wordfix",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "wordfix-cache",
        }
    }

# =============================================================================
# CELERY — eager mode fallback when no Redis
# =============================================================================

CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="")

if not CELERY_BROKER_URL:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
else:
    CELERY_TASK_ALWAYS_EAGER = False

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# =============================================================================
# =============================================================================
# AI PROVIDER
# =============================================================================

AI_PROVIDER = config("AI_PROVIDER", default="groq")
GROQ_API_KEY = config("GROQ_API_KEY", default="")
GROQ_MODEL = config("GROQ_MODEL", default="llama-3.3-70b-versatile")
OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
OPENAI_MODEL = config("OPENAI_MODEL", default="gpt-4o-mini")
AI_MAX_RETRIES = config("AI_MAX_RETRIES", default=3, cast=int)
AI_TIMEOUT = config("AI_TIMEOUT", default=30, cast=int)
WORD_ENRICHMENT_ENABLED = config("WORD_ENRICHMENT_ENABLED", default=True, cast=bool)

# =============================================================================
# LOGGING
# =============================================================================

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "apps.common.logging.JSONFormatter",
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "wordfix.log",
            "formatter": "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# =============================================================================
# APP VERSION
# =============================================================================

APP_VERSION = "1.0.0"

# =============================================================================
# SITE ID (required by django-allauth)
# =============================================================================

SITE_ID = 1

# =============================================================================
# ALLAUTH
# =============================================================================

ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_ADAPTER = "apps.users.infrastructure.adapters.CustomSocialAccountAdapter"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": config("GOOGLE_CLIENT_ID", default=""),
            "secret": config("GOOGLE_CLIENT_SECRET", default=""),
        },
        "FETCH_USERINFO": True,
    }
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# =============================================================================
# REST AUTH (dj-rest-auth)
# =============================================================================

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
    "JWT_AUTH_RETURN_EXPIRATION": True,
    "USER_DETAILS_SERIALIZER": "apps.users.presentation.serializers.UserProfileSerializer",
    "TOKEN_MODEL": None,
}

# =============================================================================
# DRF SPECTACULAR (Swagger/OpenAPI)
# =============================================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "WordFix API",
    "DESCRIPTION": "AI-powered word learning application API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
