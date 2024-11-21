"""
Налаштування додатка Library
"""

from django.apps import AppConfig


class LibraryConfig(AppConfig):
    """
    Конфігурація додатка Library
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Поле за замовчуванням для первинних ключів
    name = 'library'  # Ім'я додатка
