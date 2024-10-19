"""
Модуль для CRUD операцій з реляційною базою даних SQLite
"""

from typing import List, Dict
import sqlite3


# Створення SQL-з'єднання з базою даних SQLite
class SQLiteCRUD:
    """
    Клас для виконання CRUD операцій у SQLite базі даних
    """

    def __init__(self, db_name: str = 'movies.db'):
        """
        Ініціалізує з'єднання з базою даних SQLite
        :param db_name: Ім'я файлу бази даних SQLite
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self) -> None:
        """
        Створює таблицю movies для збереження інформації про фільми
        """
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER,
            genres TEXT,
            director TEXT
        )
        ''')
        self.connection.commit()

    def create_movie(self, title: str, year: int, genres: List[str], director: str) -> None:
        """
        Додає новий фільм у таблицю
        :param title: Назва фільму
        :param year: Рік випуску
        :param genres: Список жанрів
        :param director: Режисер
        """
        genres_str = ', '.join(genres)
        self.cursor.execute('INSERT INTO movies (title, year, genres, director) '
                            'VALUES (?, ?, ?, ?)',
                            (title, year, genres_str, director))
        self.connection.commit()

    def read_movie(self, title: str) -> Dict:
        """
        Знаходить фільм за назвою
        :param title: Назва фільму
        :return: Інформація про фільм у вигляді словника
        """
        self.cursor.execute('SELECT * FROM movies WHERE title = ?', (title,))
        movie = self.cursor.fetchone()
        return {
            'id': movie[0],
            'title': movie[1],
            'year': movie[2],
            'genres': movie[3],
            'director': movie[4]
        } if movie else {}

    def update_movie(self, title: str, year: int) -> None:
        """
        Оновлює рік випуску фільму
        :param title: Назва фільму
        :param year: Новий рік випуску
        """
        self.cursor.execute('UPDATE movies SET year = ? WHERE title = ?', (year, title))
        self.connection.commit()

    def delete_movie(self, title: str) -> None:
        """
        Видаляє фільм за назвою
        :param title: Назва фільму
        """
        self.cursor.execute('DELETE FROM movies WHERE title = ?', (title,))
        self.connection.commit()
