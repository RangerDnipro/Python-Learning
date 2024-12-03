"""
Модуль містить конфігурацію додатку, зокрема його ім’я
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Конфігурація додатка Accounts
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """
        Метод, який виконується під час готовності додатка
        Імпорт сигналів здійснено тут, щоб уникнути побічних ефектів при завантаженні модулів
        """
        try:
            import accounts.signals
        except ImportError:
            pass
