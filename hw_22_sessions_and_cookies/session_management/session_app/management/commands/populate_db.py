"""
Модуль для заповнення бази даних MongoDB та SQLite
"""

import random

from django.core.management.base import BaseCommand
from faker import Faker
from pymongo import MongoClient
from session_app.models import Author, Book, Review


class Command(BaseCommand):
    """
    Команда для заповнення бази даних тестовими даними.
    """
    help = 'Заповнення баз даних MongoDB та SQLite тестовими даними'

    def handle(self, *args, **kwargs):
        """
        Основний метод для виконання команди
        Використовує Faker для генерації авторів, книг та відгуків.
        """
        faker = Faker()

        # Підключення до MongoDB
        mongo_client = MongoClient('mongodb://127.0.0.1:27017/')
        mongo_db = mongo_client['django_books']
        mongo_authors = mongo_db['authors']
        mongo_books = mongo_db['books']
        mongo_reviews = mongo_db['reviews']

        # Створення авторів
        authors = []
        for _ in range(10):
            author = Author.objects.using('default').create(
                name=faker.name(),
                birth_date=faker.date_of_birth(minimum_age=25, maximum_age=70)
            )
            authors.append(author)

            # Додавання автора в MongoDB
            mongo_authors.insert_one({
                'name': author.name,
                'birth_date': author.birth_date.isoformat()
            })

        # Створення книг
        books = []
        for _ in range(30):
            book = Book.objects.using('default').create(
                title=faker.sentence(nb_words=4),
                publication_date=faker.date_this_century(),
                author=random.choice(authors)
            )
            books.append(book)

            # Додавання книги в MongoDB
            mongo_books.insert_one({
                'title': book.title,
                'publication_date': book.publication_date.isoformat(),
                'author': book.author.name
            })

        # Створення відгуків
        for _ in range(100):
            book = random.choice(books)
            review = Review.objects.using('default').create(
                book=book,
                review_text=faker.text(max_nb_chars=200),
                rating=random.randint(1, 5)
            )

            # Додавання відгуку в MongoDB
            mongo_reviews.insert_one({
                'book': book.title,
                'review_text': review.review_text,
                'rating': review.rating
            })

        self.stdout.write(self.style.SUCCESS('Дані успішно додано до обох баз даних!'))
