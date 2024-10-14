"""
Модуль для взаємодії з базою даних
"""


def link_actor_to_movie(cursor, movie_id: int, actor_id: int) -> None:
    """
    Зв'язує актора з фільмом
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param movie_id: Ідентифікатор фільму
    :param actor_id: Ідентифікатор актора
    """
    cursor.execute('INSERT OR IGNORE INTO movie_cast (movie_id, actor_id) VALUES (?, ?)', (movie_id, actor_id))
    cursor.execute('SELECT title FROM movies WHERE id = ?', (movie_id,))
    movie_title_row = cursor.fetchone()
    if movie_title_row is None:
        print("Помилка: фільм не знайдено.")
        return
    movie_title = movie_title_row[0]

    cursor.execute('SELECT name FROM actors WHERE id = ?', (actor_id,))
    actor_name_row = cursor.fetchone()
    if actor_name_row is None:
        print("Помилка: актор не знайдений.")
        return
    actor_name = actor_name_row[0]

    print(f"Актор: {actor_name} зв'язан з фільмом: {movie_title}")


def list_movies_by_actor(cursor, actor_id: int) -> None:
    """
    Виводить список фільмів, до яких прив'язаний актор
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param actor_id: Ідентифікатор актора
    """
    cursor.execute('SELECT name FROM actors WHERE id = ?', (actor_id,))
    actor_name_row = cursor.fetchone()
    if actor_name_row is None:
        print(f"Помилка: актор з id {actor_id} не знайдений.")
        return
    actor_name = actor_name_row[0]

    cursor.execute('''
        SELECT movies.title, movies.release_year
        FROM movies
        JOIN movie_cast ON movies.id = movie_cast.movie_id
        WHERE movie_cast.actor_id = ?
    ''', (actor_id,))
    rows = cursor.fetchall()
    if rows:
        print(f"\nФільми, до яких прив'язаний актор {actor_name}:")
        for row in rows:
            print(f"- Фільм: {row[0]}, Рік випуску: {row[1]}")
    else:
        print(f"Актор {actor_name} не прив'язаний до жодного фільму.")


def paginate_movies(cursor, page: int, page_size: int = 10) -> None:
    """
    Показує фільми з пагінацією
    :param cursor: Курсор бази даних для виконання SQL-запитів
    :param page: Номер сторінки
    :param page_size: Кількість фільмів на сторінці
    """
    offset = (page - 1) * page_size
    cursor.execute('SELECT title, release_year FROM movies LIMIT ? OFFSET ?', (page_size, offset))
    rows = cursor.fetchall()
    if rows:
        print(f"\nСторінка {page} з {len(rows)} фільмів:")
        for idx, row in enumerate(rows, start=1):
            print(f"{idx}. {row[0]}")
    else:
        print(f"Сторінка {page} не має фільмів.")


def average_birth_year_by_genre(cursor) -> None:
    """
    Виводить середній рік народження акторів по жанрах
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    cursor.execute('''
        SELECT movies.genre, AVG(actors.birth_year) AS avg_birth_year
        FROM actors
        JOIN movie_cast ON actors.id = movie_cast.actor_id
        JOIN movies ON movie_cast.movie_id = movies.id
        GROUP BY movies.genre
        ORDER BY avg_birth_year DESC
    ''')
    rows = cursor.fetchall()
    if rows:
        print("\nСередній рік народження акторів по жанрах:")
        for idx, row in enumerate(rows, start=1):
            print(f"{idx}. {row[0]}: {int(row[1])}")
    else:
        print("Немає даних для обчислення середнього року народження акторів")


def list_movies_with_actors(cursor) -> None:
    """
    Виводить список фільмів разом з акторами
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    cursor.execute('''
        SELECT movies.title, movies.release_year, group_concat(actors.name, ', ')
        FROM movies
        LEFT JOIN movie_cast ON movies.id = movie_cast.movie_id
        LEFT JOIN actors ON movie_cast.actor_id = actors.id
        GROUP BY movies.id
    ''')
    rows = cursor.fetchall()
    if rows:
        print("\nФільми та актори:")
        for idx, row in enumerate(rows, start=1):
            print(f"{idx}. Фільм: {row[0]}, рік виходу: {row[1]}. Актори: {row[2] if row[2] else 'Немає акторів'}")
    else:
        print("Немає даних для обчислення списку фільмів")


def list_unique_genres(cursor) -> None:
    """
    Виводить список унікальних жанрів
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    cursor.execute('SELECT DISTINCT genre FROM movies')
    rows = cursor.fetchall()
    if rows:
        print("\nУнікальні жанри:")
        for idx, row in enumerate(rows, start=1):
            print(f"{idx}. {row[0]}")
    else:
        print("Немає даних для обчислення жанрів")


def count_movies_by_genre(cursor) -> None:
    """
    Виводить кількість фільмів за жанрами
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    cursor.execute('SELECT genre, COUNT(*) FROM movies GROUP BY genre ORDER BY COUNT(*) DESC')
    rows = cursor.fetchall()
    if rows:
        print("\nЖанри та кількість фільмів:")
        for idx, row in enumerate(rows, start=1):
            print(f"{idx}. {row[0]}: {row[1]}")
    else:
        print("Немає даних для обчислення списку жанрів")


def list_actors_and_movies(cursor) -> None:
    """
    Виводить імена всіх акторів та назви всіх фільмів
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    cursor.execute('SELECT name, "Актор" as type FROM actors UNION SELECT title, "Фільм" as type FROM movies')
    rows = cursor.fetchall()
    if rows:

        for row in rows:
            if row[1] == "Актор":
                print(f"Актор: {row[0]}")
            elif row[1] == "Фільм":
                print(f"Фільм: {row[0]}")
