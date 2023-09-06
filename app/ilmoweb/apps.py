"""Module for app configuration."""
from django.apps import AppConfig


class IlmowebConfig(AppConfig):
    """
        Default app configuration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ilmoweb'
