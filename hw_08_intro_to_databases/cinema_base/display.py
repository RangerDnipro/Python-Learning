"""
Модуль для відображення інформації з бази даних
"""


def list_movies_with_actors(cursor) -> None:
    """
    Виводить список фільмів разом з акторами
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    cursor.execute('''
        SELECT movies.title, movies.release_year, GROUP_CONCAT(actors.name, ', ')
        FROM movies
        LEFT JOIN movie_cast ON movies.id = movie_cast.movie_id
        LEFT JOIN actors ON movie_cast.actor_id = actors.id
        GROUP BY movies.id
        ORDER BY movies.title
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(f"Фільм: {row[0]}, Рік: {row[1]}, Актори: {row[2]}")


def list_unique_genres(cursor) -> None:
    """
    Виводить список унікальних жанрів
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    cursor.execute('SELECT DISTINCT genre FROM movies')
    rows = cursor.fetchall()
    for row in rows:
        print(f"Жанр: {row[0]}")


def count_movies_by_genre(cursor) -> None:
    """
    Виводить кількість фільмів за жанрами, відсортовану за спаданням
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    cursor.execute('SELECT genre, COUNT(*) FROM movies GROUP BY genre ORDER BY COUNT(*) DESC')
    rows = cursor.fetchall()
    for row in rows:
        print(f"Жанр: {row[0]}, Кількість фільмів: {row[1]}")


def list_actors_and_movies(cursor) -> None:
    """
    Виводить імена всіх акторів та назви всіх фільмів
    :param cursor: Курсор бази даних для виконання SQL-запитів
    """
    cursor.execute('SELECT name FROM actors UNION SELECT title FROM movies')
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])
