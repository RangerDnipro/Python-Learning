"""
Модуль для пошуку інформації в базі даних
"""


def search_movie_by_title(cursor, keyword: str):
    """
    Пошук фільму за ключовим словом у назві
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param keyword: Ключове слово для пошуку фільму
    :return: Список знайдених фільмів з id, назвою та роком випуску
    """
    cursor.execute('SELECT id, title, release_year FROM movies WHERE title LIKE ?', (f'%{keyword}%',))
    rows = cursor.fetchall()
    return rows


def search_actor_by_name(cursor, keyword: str):
    """
    Пошук актора за ім'ям або його частиною
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param keyword: Ключове слово для пошуку актора
    :return: Список знайдених акторів з id, ім'ям та роком народження
    """
    cursor.execute('SELECT id, name, birth_year FROM actors WHERE name LIKE ?', (f'%{keyword}%',))
    rows = cursor.fetchall()
    return rows


def print_search_results(rows, result_type: str) -> None:
    """
    Виводить результати пошуку фільмів або акторів
    :param rows: Список результатів пошуку
    :param result_type: Тип результату ('movie' або 'actor')
    """
    if not rows:
        print("Нічого не знайдено.")
    for idx, row in enumerate(rows, start=1):
        if result_type == 'movie':
            print(f"{idx}. Фільм: {row[1]}, Рік: {row[2]}")
        elif result_type == 'actor':
            print(f"{idx}. Актор: {row[1]}, Рік народження: {row[2]}")
        else:
            print(f"{idx}. {row[1]}")
