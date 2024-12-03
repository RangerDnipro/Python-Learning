"""
Функція обчислює, скільки років минуло з моменту виходу кожного фільму
"""

import sqlite3
from datetime import datetime


def movie_age(release_year: int) -> int:
    """
    Обчислює кількість років, що минули з року випуску фільму
    :param release_year: Рік випуску фільму
    :return: Кількість років, що минули з моменту виходу фільму
    """
    current_year = datetime.now().year
    return current_year - release_year


# Підключення до бази даних
connection = sqlite3.connect('kinobaza.db')
cursor = connection.cursor()

# Реєстрація функції movie_age в SQLite
connection.create_function("movie_age", 1, movie_age)

# Виконання запиту з використанням функції movie_age
cursor.execute('''
    SELECT title, release_year, movie_age(release_year) AS age
    FROM movies
    ORDER BY age DESC
''')

rows = cursor.fetchall()
print("\nФільми та їхній вік:")
for idx, row in enumerate(rows, start=1):
    print(f"{idx}. Фільм: \"{row[0]}\" — {row[2]} років")

# Закриття з'єднання з базою даних
connection.close()
