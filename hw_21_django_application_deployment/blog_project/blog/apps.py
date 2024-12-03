"""
Файл apps.py для додатку blog.

Містить конфігурацію додатку blog у проєкті Django.
"""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    Конфігурація додатку blog.

    Атрибути:
        default_auto_field (str): Тип автоматично створюваного первинного ключа для моделей.
        name (str): Назва додатку, яка використовується у Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
