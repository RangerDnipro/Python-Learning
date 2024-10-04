"""
Завдання 10. Архівування та зберігання великих даних
Реалізуйте менеджер контексту для архівування файлів (за допомогою модуля zipfile).
Менеджер автоматично створює архів, додає файли, а після виходу з блоку with – завершує архівування та закриває архів.
"""

import zipfile
import os


class ZipManager:
    """
    Контекстний менеджер для автоматичного створення ZIP-архіву
    Додає файли до архіву під час роботи та завершує архівування після виходу з контексту
    """

    def __init__(self, zip_name):
        """
        Ініціалізація менеджера контексту
        :param zip_name: Назва архіву, який буде створений
        """
        self.zip_name = zip_name
        self.zip_file = None

    def __enter__(self):
        """
        Вхід у контекст: створення ZIP-архіву
        :return: Об'єкт для подальшої роботи з архівом
        """
        # Створюємо архів у режимі запису
        self.zip_file = zipfile.ZipFile(self.zip_name, 'w', zipfile.ZIP_DEFLATED)
        print(f"Архів '{self.zip_name}' створено")
        return self

    def add_file(self, file_path):
        """
        Додає файл до архіву, якщо він існує
        :param file_path: Шлях до файлу, який потрібно додати в архів
        """
        try:
            if os.path.exists(file_path):
                self.zip_file.write(file_path, os.path.basename(file_path))
                print(f"Файл '{file_path}' додано до архіву")
            else:
                print(f"Файл '{file_path}' не знайдено. Пропускаємо")
        except Exception as e:
            print(f"Не вдалося додати файл '{file_path}': {e}")

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Вихід з контексту: закриваємо архів після завершення роботи
        :param exc_type: Тип винятку
        :param exc_value: Значення винятку
        :param traceback: Трейсбек винятку
        """
        if self.zip_file:
            self.zip_file.close()
            print(f"Архів '{self.zip_name}' закрито")
        # Повертаємо False, щоб виняток не подавлявся
        return False


# Приклад використання менеджера контексту для архівування файлів
files_to_archive = ['homework_05_01.txt', 'test_missing_file.txt', 'homework_05_05.txt', 'homework_05_09.txt']
zip_name = 'homework_05_10_backup.zip'

# Використовуємо менеджер для створення архіву та додавання файлів
try:
    with ZipManager(zip_name) as archive:
        for file in files_to_archive:
            archive.add_file(file)
except Exception as e:
    print(f"Сталася помилка: {e}")
