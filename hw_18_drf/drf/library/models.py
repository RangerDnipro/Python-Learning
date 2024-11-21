"""
Опис моделей для додатка Library
"""

from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """
    Модель для представлення книги
    """
    title = models.CharField(max_length=255, verbose_name="Назва")  # Назва книги
    author = models.CharField(max_length=255, verbose_name="Автор")  # Автор книги
    genre = models.CharField(max_length=100, verbose_name="Жанр")  # Жанр книги
    publication_year = models.PositiveIntegerField(verbose_name="Рік видання")  # Рік видання
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")  # Дата створення запису
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")  # Користувач, що створив запис

    def __str__(self):
        """
        Повертає текстове представлення моделі
        """
        return self.title

    class Meta:
        """
        Налаштування моделі
        """
        ordering = ['title']  # Сортування за назвою
        verbose_name = "Книга"  # Назва моделі у однині
        verbose_name_plural = "Книги"  # Назва моделі у множині
