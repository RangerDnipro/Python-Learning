"""
Модуль для налаштування додатків
"""

from django.apps import AppConfig


class TestAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "test_app"

    def ready(self):
        """
        Підключає сигнали при готовності додатка.
        """
        import test_app.signals
