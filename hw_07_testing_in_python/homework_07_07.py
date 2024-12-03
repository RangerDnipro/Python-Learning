"""
Завдання 7. Тестування з використанням фікстур та тимчасових файлів
Напишіть програму для роботи з файлами та протестуйте її, використовуючи
тимчасові файли та фікстури в pytest. Реалізуйте клас FileProcessor,
який має такі методи:
write_to_file(file_path: str, data: str): записує дані у файл.
read_from_file(file_path: str) -> str: читає дані з файлу.
У тестах використовуйте фікстуру tmpdir для створення тимчасового файлу:
def test_file_write_read(tmpdir):
    file = tmpdir.join("testfile.txt")
    FileProcessor.write_to_file(file, "Hello, World!")
    content = FileProcessor.read_from_file(file)
    assert content == "Hello, World!"
Додайте тести для перевірки методів з великими обсягами даних, порожніми рядками,
а також тести на наявність винятків, якщо файл не знайдено.
"""

import os
import pytest


class FileProcessor:
    """
    Клас для роботи з файлами, що включає методи для запису та читання файлів.
    """

    @staticmethod
    def write_to_file(file_path: str, data: str) -> None:
        """
        Записує дані у файл за заданим шляхом
        :param file_path: Шлях до файлу, у який будуть записані дані
        :param data: Дані, які мають бути записані у файл
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(data)

    @staticmethod
    def read_from_file(file_path: str) -> str:
        """
        Читає дані з файлу за заданим шляхом
        :param file_path: Шлях до файлу, з якого будуть прочитані дані
        :return: Вміст файлу як рядок
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл за шляхом {file_path} не знайдено.")

        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()


# Тести для класу FileProcessor з використанням фікстури tmpdir
# для створення тимчасових файлів та каталогів, що дозволяє ізолювати тести
# та перевіряти роботу методів класу в різних сценаріях
def test_file_write_read(tmpdir):
    """
    Перевіряє, що дані правильно записуються у файл і читаються з нього
    """
    file = tmpdir.join("testfile.txt")
    FileProcessor.write_to_file(file, "Hello, World!")
    content = FileProcessor.read_from_file(file)
    assert content == "Hello, World!"


def test_large_data(tmpdir):
    """
    Перевіряє роботу з великим обсягом даних
    """
    file = tmpdir.join("largefile.txt")
    # 1 мільйон символів 'A'
    large_data = "A" * 10 ** 6
    FileProcessor.write_to_file(file, large_data)
    content = FileProcessor.read_from_file(file)
    assert content == large_data


def test_empty_string(tmpdir):
    """
    Перевіряє запис та читання порожнього рядка
    """
    file = tmpdir.join("emptyfile.txt")
    FileProcessor.write_to_file(file, "")
    content = FileProcessor.read_from_file(file)
    assert content == ""


def test_file_not_found():
    """
    Перевіряє виклик винятку, якщо файл не знайдено
    """
    with pytest.raises(FileNotFoundError, match="Файл за шляхом .* не знайдено."):
        FileProcessor.read_from_file("non_existent_file.txt")
