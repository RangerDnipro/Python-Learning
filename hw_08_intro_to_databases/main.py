"""
Основний файл для запуску програми "Кінобаза"
"""

import sqlite3
from cinema_base import (
    print_menu,
    handle_add_or_edit_movie,
    handle_add_or_edit_actor,
    list_movies_with_actors,
    list_unique_genres,
    count_movies_by_genre,
    average_birth_year_by_genre,
    search_movie_by_title,
    paginate_movies,
    list_actors_and_movies,
    print_search_results
)


def main():
    """
    Основна функція для роботи з консольним інтерфейсом програми "Кінобаза"
    """
    # Підключення до бази даних
    connection = sqlite3.connect('kinobaza.db')
    cursor = connection.cursor()

    while True:
        print_menu()
        choice = input("Виберіть дію: ")
        handle_user_choice(choice, cursor, connection)

    # Закриваємо з'єднання з базою даних
    connection.close()


def handle_user_choice(choice: str, cursor, connection) -> None:
    """
    Обробляє вибір користувача з меню
    :param choice: Вибір користувача
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param connection: З'єднання з базою даних для коміту змін
    """
    if choice == '1':
        handle_add_or_edit_movie(cursor)
        connection.commit()
    elif choice == '2':
        handle_add_or_edit_actor(cursor)
        connection.commit()
    elif choice == '3':
        list_movies_with_actors(cursor)
    elif choice == '4':
        list_unique_genres(cursor)
    elif choice == '5':
        count_movies_by_genre(cursor)
    elif choice == '6':
        average_birth_year_by_genre(cursor)
    elif choice == '7':
        handle_movie_search(cursor)
    elif choice == '8':
        page = int(input("Введіть номер сторінки: "))
        paginate_movies(cursor, page)
    elif choice == '9':
        list_actors_and_movies(cursor)
    elif choice == '10':
        movie_age(cursor)
    elif choice == '0':
        exit_program()
    else:
        print("Невірний вибір. Спробуйте ще раз.")


def handle_movie_search(cursor) -> None:
    """
    Обробляє пошук фільму за ключовим словом
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    keyword = input("Введіть ключове слово для пошуку фільму: ")
    movies = search_movie_by_title(cursor, keyword)
    if movies:
        print_search_results(movies, 'movie')
    else:
        print("Фільми з таким ключовим словом не знайдено.")


def exit_program() -> None:
    """
    Вихід з програми
    """
    print("Завершення програми...")
    exit()


def movie_age(cursor) -> None:
    """
    Виводить кількість років, що минули з моменту виходу кожного фільму
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    cursor.execute(
        "SELECT title, release_year, (strftime('%Y', 'now') - release_year) AS age FROM movies ORDER BY age DESC")
    rows = cursor.fetchall()
    print("Фільми та їхній вік:")
    for idx, row in enumerate(rows, start=1):
        print(f"{idx}. Фільм: \"{row[0]}\" — {row[2]} років")


if __name__ == "__main__":
    main()
