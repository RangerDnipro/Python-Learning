"""
Модуль для обробки акторів
"""

from .entities import Actor
from .menu import print_edit_actor_menu
from .database import link_actor_to_movie, list_movies_by_actor
from .search import search_actor_by_name, search_movie_by_title, print_search_results


def add_actor(cursor, name: str, birth_year: int) -> int:
    """
    Додає нового актора до бази даних
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param name: Ім'я актора
    :param birth_year: Рік народження актора
    :return: Ідентифікатор доданого актора
    """
    cursor.execute('INSERT INTO actors (name, birth_year) VALUES (?, ?)', (name, birth_year))
    print(f"Доданий Актор: {name}, Рік: {birth_year}")
    return cursor.lastrowid


def delete_actor(cursor, actor_id: int) -> None:
    """
    Видаляє актора з бази даних та всі його зв'язки з фільмами
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param actor_id: Ідентифікатор актора
    """
    cursor.execute('DELETE FROM movie_cast WHERE actor_id = ?', (actor_id,))
    cursor.execute('DELETE FROM actors WHERE id = ?', (actor_id,))


def handle_add_or_edit_actor(cursor) -> None:
    """
    Додає, редагує або видаляє актора в базі даних
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    keyword = input("Введіть ім'я актора або його частину для пошуку: ")
    rows = search_actor_by_name(cursor, keyword)
    if rows:
        print("Знайдені актори:")
        print_search_results(rows, 'actor')
        print("0. Додати нового актора")
        actor_choice = int(input("Введіть номер актора для редагування або 0 для додавання нового: "))
        if actor_choice == 0:
            actor = create_actor(cursor)
        else:
            actor = Actor.get_from_db(cursor, rows[actor_choice - 1][0])
            edit_actor(cursor, actor)
    else:
        print("Акторів з таким ім'ям не знайдено. Створюємо нового актора.")
        actor = create_actor(cursor)


def create_actor(cursor) -> Actor:
    """
    Створює екземпляр класу Actor та додає його до бази даних
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :return: Екземпляр класу Actor
    """
    name = input("Введіть ім'я актора: ")
    birth_year = int(input("Введіть рік народження актора: "))
    actor = Actor(name=name, birth_year=birth_year)
    actor.save_to_db(cursor)
    print(f"Доданий Актор: {actor.name}, Рік: {actor.birth_year}")
    return actor


def edit_actor(cursor, actor: Actor) -> None:
    """
    Редагує екземпляр класу Actor
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param actor: Екземпляр класу Actor для редагування
    """
    while True:
        print_edit_actor_menu()
        edit_choice = input("Виберіть дію: ")
        if edit_choice == '1':
            actor.name = input("Введіть нове ім'я актора: ")
            actor.save_to_db(cursor)
            print(f"Ім'я актора змінено на: {actor.name}")
        elif edit_choice == '2':
            actor.birth_year = int(input("Введіть новий рік народження актора: "))
            actor.save_to_db(cursor)
            print(f"Рік народження актора змінено на: {actor.birth_year}")
        elif edit_choice == '3':
            keyword = input("Введіть назву фільму для пошуку: ")
            movies = search_movie_by_title(cursor, keyword)
            if movies:
                print_search_results(movies, 'movie')
                movie_choice = int(input("Введіть номер фільму для прив'язки актора або 0 для повернення: "))
                if movie_choice != 0:
                    movie_id = movies[movie_choice - 1][0]
                    link_actor_to_movie(cursor, movie_id, actor.id)
            else:
                print("Фільмів з таким ключовим словом не знайдено.")
        elif edit_choice == '4':
            list_movies_by_actor(cursor, actor.id)
        elif edit_choice == '5':
            delete_actor(cursor, actor.id)
            print(f"Актор: {actor.name} видалений разом з усіма прив'язками.")
            break
        elif edit_choice == '0':
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")
