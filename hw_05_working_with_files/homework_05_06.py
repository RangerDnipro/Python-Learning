"""
Завдання 6. Ітерація через файли в каталозі
Напишіть ітератор, який буде повертати всі файли в заданому каталозі по черзі.
Для кожного файлу виведіть його назву та розмір.
"""

import os


class DirectoryFileIterator:
    """
    Ітератор для перебору файлів у вказаному каталозі
    """

    def __init__(self, directory):
        """
        Ініціалізація ітератора
        :param directory: Шлях до каталогу для ітерації
        """
        self.directory = directory
        self.files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        self.index = 0

    def __iter__(self):
        """
        Повертає сам ітератор
        """
        return self

    def __next__(self):
        """
        Повертає наступний файл у каталозі, його ім'я та розмір. Якщо файли закінчились — піднімає StopIteration
        :return: Словник з інформацією про файл (ім'я, розмір)
        """
        if self.index >= len(self.files):
            raise StopIteration

        file_name = self.files[self.index]
        file_path = os.path.join(self.directory, file_name)
        file_size = os.path.getsize(file_path)

        self.index += 1

        return {'file_name': file_name, 'size': file_size}


# Використання ітератора
directory = 'homework_05_03_images'
file_iterator = DirectoryFileIterator(directory)

for file_info in file_iterator:
    print(f"File: {file_info['file_name']}, Size: {file_info['size']} bytes")
