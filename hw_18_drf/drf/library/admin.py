"""
Налаштування адміністративної панелі для додатка Library
"""

from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Налаштування адміністративної панелі для моделі Book
    """
    list_display = (
        'title', 'author', 'genre', 'publication_year', 'user', 'created_at')  # Поля для відображення у списку
    search_fields = ('title', 'author', 'genre')  # Поля для пошуку
    list_filter = ('genre', 'publication_year')  # Поля для фільтрації
