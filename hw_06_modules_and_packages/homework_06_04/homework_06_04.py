"""
Завдання 4: Робота з JSON
Створи JSON-файл з інформацією про книги, кожна книга повинна мати:
Назву Автора Рік видання Наявність (True або False)

[
    {"назва": "Книга 1", "автор": "Автор 1", "рік": 2015, "наявність": true},
    {"назва": "Книга 2", "автор": "Автор 2", "рік": 2018, "наявність": false}
]

Напиши програму, яка:
Завантажує JSON-файл.
Виводить список доступних книг (наявність True).
Додає нову книгу в цей файл.
"""

import json
import os


def create_default_file(filename):
    """
    Створює JSON-файл з дефолтними даними, якщо файл не існує
    :param filename: Ім'я файлу, який потрібно створити
    """
    if not os.path.exists(filename):
        default_books = [
            {"назва": "Книга 1", "автор": "Автор 1", "рік": 2015, "наявність": True},
            {"назва": "Книга 2", "автор": "Автор 2", "рік": 2018, "наявність": False}
        ]
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(default_books, file, ensure_ascii=False, indent=4)


def load_books(filename):
    """
    Завантажує дані з JSON-файлу
    :param filename: Ім'я файлу, з якого будуть зчитані дані
    :return: Список книг
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            books = json.load(file)
            return books
    except FileNotFoundError:
        print("Файл не знайдено")
        return []
    except json.JSONDecodeError:
        print("Помилка зчитування JSON")
        return []


def available_books(books):
    """
    Виводить список доступних книг
    :param books: Список книг
    """
    print("Доступні книги:")
    for book in books:
        if book["наявність"]:
            print(f"{book['назва']} - {book['автор']} ({book['рік']})")


def add_book(filename, new_book):
    """
    Додає нову книгу до JSON-файлу
    :param filename: Ім'я файлу, до якого буде додана книга
    :param new_book: Словник з даними нової книги
    """
    books = load_books(filename)  # Завантажуємо існуючі книги

    # Перевірка на існування книги
    for book in books:
        # Пропускаємо додавання, якщо книга вже є
        if (book["назва"] == new_book["назва"] and
                book["автор"] == new_book["автор"] and
                book["рік"] == new_book["рік"]):
            print(
                f"Книга з назвою {new_book["назва"]}, автором {new_book["автор"]} і роком {new_book["рік"]} вже існує")
            return

    # Додаємо нову книгу
    books.append(new_book)
    print(f"Нова книга {new_book["назва"]} {new_book["автор"]} {new_book["рік"]} додана")

    with open(filename, 'w', encoding='utf-8') as file:
        # Записуємо оновлений список книг
        json.dump(books, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    filename = "homework_06_04.json"

    # Створюємо файл з дефолтними даними, якщо він не існує
    create_default_file(filename)

    # Завантажуємо книги
    books = load_books(filename)

    # Виводимо доступні книги
    available_books(books)

    # Додаємо нову книгу
    new_book = {"назва": "Книга 3", "автор": "Автор 3", "рік": 2020, "наявність": True}
    add_book(filename, new_book)
