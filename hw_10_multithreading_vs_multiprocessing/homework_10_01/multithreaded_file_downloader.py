"""
Модуль програми для завантаження кількох файлів із мережі за допомогою потоків,
використовуючи бібліотеку threading та requests
"""

# pylint: disable=line-too-long

import os
from typing import List
from urllib.parse import urlparse
import threading
import requests


def download_file(url: str, filename: str) -> None:
    """
    Завантажує файл з вказаної URL-адреси та зберігає його з заданим іменем
    :param url: URL-адреса файлу, який потрібно завантажити
    :param filename: Ім'я файлу для збереження на локальному диску
    :return: None
    """
    try:
        response = requests.get(url, stream=True, timeout=10)
        # Перевіряємо, чи немає помилок HTTP
        response.raise_for_status()

        # Завантажуємо файл по частинах для ефективної роботи з великими файлами
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[INFO] Файл '{filename}' успішно завантажено.")
    except requests.RequestException as e:
        print(f"[ERROR] Помилка при завантаженні '{filename}': {e}")


def download_files(urls: List[str]) -> None:
    """
    Створює потоки для паралельного завантаження файлів із заданих URL-адрес
    :param urls: Список URL-адрес файлів для завантаження
    :return: None
    """
    # Список для зберігання потоків
    threads = []

    # Створюємо та запускаємо окремий потік для кожного файлу
    for url in urls:
        # Отримуємо оригінальне ім'я файлу з URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        thread = threading.Thread(target=download_file, args=(url, filename))
        threads.append(thread)
        thread.start()

    # Чекаємо завершення всіх потоків
    for thread in threads:
        thread.join()

    print("[INFO] Всі файли завантажені.")


if __name__ == "__main__":
    # Приклад URL-адрес для завантаження файлів
    urls_examples = [
        "https://file-examples.com/storage/feb05093336710053a32bc1/2017/11/file_example_MP3_5MG.mp3",
        "https://file-examples.com/storage/feb05093336710053a32bc1/2017/10/file_example_JPG_2500kB.jpg",
        "https://file-examples.com/storage/feb05093336710053a32bc1/2017/04/file_example_MP4_1920_18MG.mp4"
    ]

    download_files(urls_examples)
