"""
Файл apps.py для додатку accounts.

Цей файл відповідає за конфігурацію додатку accounts у Django. 
Він також завантажує сигнали, визначені у цьому додатку.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Конфігурація додатку accounts.

    Атрибути:
        default_auto_field (str): Визначає тип автоматичного первинного ключа для моделей.
        name (str): Назва додатку, яка використовується у Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """
        Метод викликається, коли додаток готовий до використання.

        Він завантажує модуль signals для додатку accounts, 
        забезпечуючи активацію сигналів під час роботи програми.
        """
        import accounts.signals
