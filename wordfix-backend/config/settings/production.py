"""
Production settings for WordFix project.

Supports both HTTP-only and HTTPS deployments.
Set USE_SSL=True in env to enable SSL-related settings.
"""

from .base import *  # noqa: F401, F403

from decouple import config as env_config

# =============================================================================
# SECURITY
# =============================================================================

DEBUG = False

# SSL settings — disabled by default for HTTP-only deployments
# Set USE_SSL=True in .env.production when you add SSL/HTTPS
_use_ssl = env_config("USE_SSL", default=False, cast=bool)

SECURE_SSL_REDIRECT = _use_ssl
SESSION_COOKIE_SECURE = _use_ssl
CSRF_COOKIE_SECURE = _use_ssl

if _use_ssl:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "SAMEORIGIN"

# Trust X-Forwarded-Proto from nginx
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF trusted origins — needed for nginx reverse proxy
_server_ip = env_config("SERVER_IP", default="")
CSRF_TRUSTED_ORIGINS = []
if _server_ip:
    CSRF_TRUSTED_ORIGINS.append(f"http://{_server_ip}")
    CSRF_TRUSTED_ORIGINS.append(f"https://{_server_ip}")
CSRF_TRUSTED_ORIGINS += [
    "http://localhost",
    "http://127.0.0.1",
]

# =============================================================================
# STATIC FILES
# =============================================================================

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# =============================================================================
# LOGGING
# =============================================================================

LOGGING["loggers"]["django"]["level"] = "WARNING"  # noqa: F405
LOGGING["loggers"]["apps"]["level"] = "INFO"  # noqa: F405
LOGGING["root"]["handlers"] = ["console", "file"]  # noqa: F405
