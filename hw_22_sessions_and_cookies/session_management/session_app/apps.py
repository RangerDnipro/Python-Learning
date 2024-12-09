"""
Модуль для налаштувань додатків проєкту
"""

from django.apps import AppConfig


class SessionAppConfig(AppConfig):
    """
    Налаштування конфігурації додатку 'session_app'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'session_app'
