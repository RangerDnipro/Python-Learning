"""
Завдання 3. Збір статистики про зображення
У вас є каталог з великою кількістю зображень. Напишіть ітератор, який по черзі відкриває кожне зображення
(наприклад, за допомогою модуля PIL), витягує з нього метадані (розмір, формат тощо) і зберігає ці дані у файл CSV.
"""

import os
import csv
from PIL import Image


class ImageMetadataIterator:
    """
    Ітератор для збору метаданих зображень з каталогу.
    """

    def __init__(self, directory):
        """
        Ініціалізація ітератора.
        :param directory: Шлях до каталогу, де зберігаються зображення.
        """
        self.directory = directory
        self.files = [f for f in os.listdir(directory) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
        self.index = 0

    def __iter__(self):
        """
        Повертає сам ітератор.
        """
        return self

    def __next__(self):
        """
        Витягує метадані з наступного зображення. Якщо зображення закінчились, зупиняє ітерацію.
        :return: Словник з метаданими зображення.
        """
        if self.index >= len(self.files):
            raise StopIteration

        file_name = self.files[self.index]
        file_path = os.path.join(self.directory, file_name)

        with Image.open(file_path) as img:
            metadata = {
                'file_name': file_name,
                'format': img.format,
                'size': img.size,  # (width, height)
                'mode': img.mode  # колірний режим
            }

        self.index += 1
        return metadata


def save_metadata_to_csv(directory, output_csv):
    """
    Збирає метадані зі зображень та зберігає їх у файл CSV.
    :param directory: Каталог, в якому зберігаються зображення.
    :param output_csv: Файл CSV, куди зберігатимуться метадані.
    """
    # Заголовки для CSV-файлу
    fieldnames = ['file_name', 'format', 'size', 'mode']

    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        image_iterator = ImageMetadataIterator(directory)
        for metadata in image_iterator:
            writer.writerow(metadata)

    print(f"Метадані успішно збережено у файл {output_csv}")


# Використання ітератора для збору метаданих
directory = "homework_05_03_images"
output_csv = 'homework_05_03.csv'
save_metadata_to_csv(directory, output_csv)
