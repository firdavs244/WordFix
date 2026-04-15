"""Immersive game app configuration."""

from django.apps import AppConfig


class ImmersiveConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.immersive"
    verbose_name = "Immersive Game"
