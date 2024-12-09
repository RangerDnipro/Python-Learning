"""
Модуль для використання Raw SQL
"""

from typing import List, Tuple

from django.db import connection


def get_authors_with_many_reviews(threshold: int = 10) -> List[Tuple[int, str]]:
    """
    Повертає список авторів, книги яких мають більше threshold відгуків.
    :param threshold: Мінімальна кількість відгуків.
    :return: Список авторів у форматі (id, name).
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT author.id, author.name
            FROM session_app_author AS author
            JOIN session_app_book AS book ON author.id = book.author_id
            JOIN session_app_review AS review ON book.id = review.book_id
            GROUP BY author.id
            HAVING COUNT(review.id) > %s
        """, [threshold])
        authors = cursor.fetchall()
    return authors


def get_total_books() -> int:
    """
    Повертає загальну кількість книг.
    :return: Кількість книг.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM session_app_book")
        total_books = cursor.fetchone()[0]
    return total_books
