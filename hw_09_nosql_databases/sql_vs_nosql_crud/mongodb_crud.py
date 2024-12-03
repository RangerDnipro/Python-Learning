"""
Модуль для CRUD операцій з NoSQL базой MongoDB
"""

from typing import List, Dict
from pymongo import MongoClient


# Створення NoSQL-з'єднання з базою даних MongoDB
class MongoDBCRUD:
    """
    Клас для виконання CRUD операцій у MongoDB базі даних
    """

    def __init__(self, db_name: str = 'movies_db', collection_name: str = 'movies'):
        """
        Ініціалізує з'єднання з базою даних MongoDB
        :param db_name: Ім'я бази даних MongoDB
        :param collection_name: Ім'я колекції
        """
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_movie(self, title: str, year: int, genres: List[str], director: str) -> None:
        """
        Додає новий фільм у колекцію
        :param title: Назва фільму
        :param year: Рік випуску
        :param genres: Список жанрів
        :param director: Режисер
        """
        movie = {
            'title': title,
            'year': year,
            'genres': genres,
            'director': director
        }
        self.collection.insert_one(movie)

    def read_movie(self, title: str) -> Dict:
        """
        Знаходить фільм за назвою
        :param title: Назва фільму
        :return: Інформація про фільм у вигляді словника
        """
        movie = self.collection.find_one({'title': title})
        return movie if movie else {}

    def update_movie(self, title: str, year: int) -> None:
        """
        Оновлює рік випуску фільму
        :param title: Назва фільму
        :param year: Новий рік випуску
        """
        self.collection.update_one({'title': title}, {'$set': {'year': year}})

    def delete_movie(self, title: str) -> None:
        """
        Видаляє фільм за назвою
        :param title: Назва фільму
        """
        self.collection.delete_one({'title': title})
