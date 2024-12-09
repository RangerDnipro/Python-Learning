"""
Модуль для тестування продуктивності
"""

import time

from django.db.models import Avg, Count

from .models import Book, Review


def test_query_performance():
    """
    Вимірює час виконання запитів для перевірки індексації.
    """

    # Тест 1: Запит середнього рейтингу для кожної книги
    start_time = time.time()
    books = Book.objects.annotate(avg_rating=Avg('reviews__rating'))
    print("Час виконання (без сортування): {:.5f} секунд".format(time.time() - start_time))

    # Тест 2: Запит із сортуванням за середнім рейтингом
    start_time = time.time()
    books_sorted = books.order_by('-avg_rating')
    print("Час виконання (з сортуванням): {:.5f} секунд".format(time.time() - start_time))

    # Тест 3: Запит із підрахунком кількості відгуків
    start_time = time.time()
    review_counts = Review.objects.values('rating').annotate(count=Count('rating'))
    print("Час виконання (підрахунок відгуків): {:.5f} секунд".format(time.time() - start_time))


def test_mongodb_vs_sqlite():
    """
    Порівняння продуктивності MongoDB та SQLite.
    """

    # Тест продуктивності для MongoDB
    start_time = time.time()
    books_mongo = Book.objects.using('mongodb').all()
    print(f"MongoDB: Отримано {books_mongo.count()} книг за {time.time() - start_time:.5f} секунд.")

    # Тест продуктивності для SQLite
    start_time = time.time()
    books_sqlite = Book.objects.using('default').all()
    print(f"SQLite: Отримано {books_sqlite.count()} книг за {time.time() - start_time:.5f} секунд.")
