"""
Модуль з моделями проєкту
"""

from django.apps import apps
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Author(models.Model):
    """
    Модель автора книги.
    """
    name = models.CharField(max_length=255, verbose_name="Ім'я автора")
    birth_date = models.DateField(verbose_name="Дата народження", null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Модель книги.
    """
    title = models.CharField(max_length=255, verbose_name="Назва книги")
    publication_date = models.DateField(verbose_name="Дата публікації", null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books", verbose_name="Автор")

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Модель відгуку на книгу.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews", verbose_name="Книга")
    review_text = models.TextField(verbose_name="Текст відгуку")
    rating = models.PositiveIntegerField(default=0, verbose_name="Оцінка")

    def __str__(self):
        return f"Review for {self.book.title} ({self.rating})"


@receiver([post_save, post_delete], sender=None)
def clear_books_cache(sender, **kwargs):
    """
    Очищає кеш списку книг при додаванні, зміні або видаленні книги.
    """
    if sender == apps.get_model('session_app', 'Book'):
        cache.clear()  # Очищуємо кеш
