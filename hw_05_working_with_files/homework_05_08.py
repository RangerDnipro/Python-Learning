"""
Завдання 8. Конфігурація через контекстні менеджери
Напишіть власний контекстний менеджер для роботи з файлом конфігурацій (формат .ini або .json).
Менеджер має автоматично зчитувати конфігурацію при вході в контекст і записувати зміни в файл після завершення роботи.
"""

import json


class ConfigManager:
    """
    Контекстний менеджер для роботи з конфігураційним файлом у форматі .json
    Автоматично зчитує конфігурацію при вході та зберігає зміни після завершення роботи
    """

    def __init__(self, file_name):
        """
        Ініціалізація контекстного менеджера
        :param file_name: Шлях до конфігураційного файлу
        """
        self.file_name = file_name
        self.config = None
        self._changed = False

    def __enter__(self):
        """
        Вхід у контекст: зчитування конфігураційного файлу
        """
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                self.config = json.load(file)
            print(f"Конфігурація зчитана з файлу: {self.file_name}")
        except FileNotFoundError:
            self.config = {}
            print(f"Файл конфігурації не знайдено, створюємо новий: {self.file_name}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Вихід з контексту: збереження змін у конфігураційному файлі, якщо вони були
        """
        if self._changed:
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(self.config, file, indent=4)
            print(f"Конфігурація збережена у файл: {self.file_name}")
        else:
            print("Зміни у конфігурацію не були внесені, файл не оновлено.")

    def update(self, key, value):
        """
        Оновлює значення конфігурації
        """
        if self.config.get(key) != value:
            self.config[key] = value
            self._changed = True
            print(f"Оновлено: {key} = {value}")

    def get(self, key, default=None):
        """
        Повертає значення конфігурації за ключем або дефолтне значення
        """
        return self.config.get(key, default)


# Приклад використання контекстного менеджера
config_file = 'homework_05_08.json'

# Читання та оновлення конфігурації, після виходу з контексту зміни автоматично збережуться у файл 'config.json'
with ConfigManager(config_file) as config_manager:
    # Отримання значення з конфігурації
    db_host = config_manager.get('db_host', 'localhost')
    print(f"Поточний db_host: {db_host}")

    # Оновлення конфігурації
    config_manager.update('db_host', '192.168.1.1')
    config_manager.update('db_port', 5432)
