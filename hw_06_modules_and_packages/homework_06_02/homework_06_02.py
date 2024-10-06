"""
Завдання 2: Робота з зовнішніми пакетами
Встанови пакет requests за допомогою pip.
Напиши скрипт, який завантажує сторінку з вказаного URL та зберігає її вміст у текстовий файл.
Додай обробку помилок на випадок, якщо сторінка недоступна.
"""

import requests


def download_page(url, file_name):
    """
    Завантаження вмісту веб-сторінки за вказаним URL та збереження його у текстовий файл
    :param url: URL веб-сторінки, яку потрібно завантажити
    :param file_name: Ім'я файлу, у який буде збережено вміст сторінки
    :return: None
    :raises Exception: Якщо не вдається завантажити сторінку
    """
    try:
        # Надсилаємо GET-запит до вказаного URL
        response = requests.get(url)

        # Перевіряємо статус-код відповіді
        response.raise_for_status()

        # Зберігаємо вміст сторінки у файл
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)

        print(f"Сторінка успішно збережена в {file_name}")

    except requests.exceptions.RequestException as e:
        # Обробляємо помилки, пов'язані з HTTP-запитами
        print(f"Помилка під час завантаження сторінки: {e}")

    except Exception as e:
        # Обробляємо інші помилки
        print(f"Несподівана помилка: {e}")


if __name__ == "__main__":
    # Вказуємо URL сторінки та ім'я файлу для збереження
    url = "https://refactoring.guru/uk/design-patterns/iterator"
    file_name = "homework_06_02_page.txt"

    download_page(url, file_name)
