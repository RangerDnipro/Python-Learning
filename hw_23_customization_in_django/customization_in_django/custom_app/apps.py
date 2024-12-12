"""
Модуль для налаштування додатків
"""

from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    """
    Конфігурація додатку `custom_app`.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_app'
    verbose_name = "Кастомний додаток"

    def ready(self):
        """
        Метод викликається, коли додаток готовий до роботи.
        Тут можна імпортувати та реєструвати сигнали або виконувати інші ініціалізації.
        """
        import custom_app.models  # Імпортуємо моделі для сигналів
