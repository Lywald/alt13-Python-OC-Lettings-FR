"""Application configuration for the profiles app."""
from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """Default configuration for the profiles application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "profiles"
