"""
Програма для паралельного пошуку тексту у файлах, використовуючи потоки
"""

import os
import concurrent.futures
from typing import List


def search_in_file(filename: str, text: str) -> List[int]:
    """
    Пошук заданого тексту в файлі
    :param filename: Шлях до файлу, в якому виконується пошук
    :param text: Текст, який потрібно знайти
    :return: Список номерів рядків, в яких знайдено текст
    """
    line_numbers = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, start=1):
                if text in line:
                    line_numbers.append(i)
    except (OSError, IOError) as e:
        print(f"Помилка при обробці файлу {filename}: {e}")
    return line_numbers


def parallel_search(files: List[str], text: str) -> None:
    """
    Паралельний пошук заданого тексту у кількох файлах за допомогою потоків
    :param files: Список файлів для пошуку
    :param text: Текст, який потрібно знайти
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Створюємо пул потоків, який буде обробляти кожен файл окремо
        future_to_file = {executor.submit(search_in_file, file, text): file for file in files}
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                if result:
                    print(f"Текст знайдено у файлі {file} на рядках: {result}")
                else:
                    print(f"Текст не знайдено у файлі {file}")
            except (OSError, IOError) as e:
                print(f"Помилка при обробці результату файлу {file}: {e}")


if __name__ == "__main__":
    # Вказуємо список файлів, які знаходяться у папці big_files
    files_to_search = [
        filename for filename in os.listdir("big_files")
        if os.path.isfile(os.path.join("big_files", filename))
    ]
    files_to_search = [os.path.join("big_files", filename) for filename in files_to_search]

    # Вказуємо текст, який потрібно знайти
    TEXT_TO_FIND = "under"

    # Запускаємо паралельний пошук
    parallel_search(files_to_search, TEXT_TO_FIND)
