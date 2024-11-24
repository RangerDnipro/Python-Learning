"""
Налаштування конфігурації додатка 'users'
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфігурація додатка Users
    Дозволяє налаштувати основні параметри додатка Users, такі як назва та тип поля за замовчуванням для моделей
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
