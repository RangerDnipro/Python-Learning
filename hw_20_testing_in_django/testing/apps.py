"""
Налаштування конфігурації додатка
"""

from django.apps import AppConfig


class TestingConfig(AppConfig):
    """
    Конфігурація додатка, дозволяє налаштувати основні параметри додатка
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testing'
