"""
Модуль для обробки фільмів
"""

from .entities import Movie
from .menu import print_edit_movie_menu
from .search import search_movie_by_title


def add_movie(cursor, title: str, release_year: int, genre: str) -> int:
    """
    Додає новий фільм до бази даних
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param title: Назва фільму
    :param release_year: Рік випуску фільму
    :param genre: Жанр фільму
    :return: Ідентифікатор доданого фільму
    """
    cursor.execute('INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)', (title, release_year, genre))
    movie_id = cursor.lastrowid
    print(f"Доданий Фільм: {title}, Рік: {release_year}")
    return movie_id


def handle_add_or_edit_movie(cursor) -> Movie:
    """
    Додає або редагує фільм у базі даних
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :return: Екземпляр класу Movie
    """
    title = input("Введіть назву фільму: ")
    rows = search_movie_by_title(cursor, title)
    if rows:
        print("Знайдені фільми:")
        for idx, row in enumerate(rows, start=1):
            print(f"{idx}. Фільм: {row[1]}, Рік: {row[2]}")
        print("0. Додати новий фільм")
        movie_choice = int(input("Введіть номер фільму для редагування або 0 для додавання нового: "))
        if movie_choice != 0:
            movie = Movie.get_from_db(cursor, rows[movie_choice - 1][0])
            edit_movie(cursor, movie)
            return movie
    movie = create_movie(title)
    movie.save_to_db(cursor)
    return movie


def create_movie(title: str) -> Movie:
    """
    Створює екземпляр класу Movie
    :param title: Назва фільму
    :return: Екземпляр класу Movie
    """
    release_year = int(input("Введіть рік випуску: "))
    genre = input("Введіть жанр: ")
    print(f"Створено фільм {title}, рік виходу {release_year} у жанрі {genre}")
    return Movie(title=title, release_year=release_year, genre=genre)


def edit_movie(cursor, movie: Movie) -> None:
    """
    Редагує екземпляр класу Movie
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param movie: Екземпляр класу Movie для редагування
    """
    while True:
        print_edit_movie_menu()
        edit_choice = input("Виберіть дію: ")
        if edit_choice == '1':
            movie.title = input("Введіть нову назву фільму: ")
            movie.save_to_db(cursor)
            print(f"Назву фільму змінено на: {movie.title}")
        elif edit_choice == '2':
            movie.release_year = int(input("Введіть новий рік випуску: "))
            movie.save_to_db(cursor)
            print(f"Рік випуску фільму змінено на: {movie.release_year}")
        elif edit_choice == '3':
            movie.genre = input("Введіть новий жанр: ")
            movie.save_to_db(cursor)
            print(f"Жанр фільму змінено на: {movie.genre}")
        elif edit_choice == '4':
            delete_movie(cursor, movie.id)
        elif edit_choice == '0':
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


def delete_movie(cursor, movie_id: int) -> None:
    """
    Видаляє фільм з бази даних та всі його зв'язки з акторами
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param movie_id: Ідентифікатор фільму
    """
    # Отримуємо назву фільму перед видаленням
    cursor.execute('SELECT title FROM movies WHERE id = ?', (movie_id,))
    movie_title_row = cursor.fetchone()
    if movie_title_row:
        movie_title = movie_title_row[0]
    else:
        print(f"Фільм з id {movie_id} не знайдено.")
        return

    # Видаляємо зв'язки з акторами та сам фільм
    cursor.execute('DELETE FROM movie_cast WHERE movie_id = ?', (movie_id,))
    cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    print(f"Фільм '{movie_title}' (id: {movie_id}) видалений разом з усіма прив'язками.")
