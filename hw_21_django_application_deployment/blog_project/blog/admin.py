"""
Файл admin.py для додатку blog.

Цей файл налаштовує адмінпанель Django для управління моделями Post, Category, Tag, та Comment.
"""

from django.contrib import admin
from .models import Post, Category, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Налаштування для моделі Post в адмінпанелі Django.

    Визначає:
        - Поля для відображення у списку записів (`list_display`).
        - Можливості фільтрації (`list_filter`).
        - Поля для пошуку (`search_fields`).

    Атрибути:
        list_display (tuple): Поля, які відображаються у списку записів.
        list_filter (tuple): Поля для фільтрації.
        search_fields (tuple): Поля, доступні для пошуку.
    """
    list_display = ('title', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'content')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Налаштування для моделі Category в адмінпанелі Django.

    Визначає:
        - Поля для відображення у списку категорій (`list_display`).
        - Поля для пошуку (`search_fields`).

    Атрибути:
        list_display (tuple): Поля, які відображаються у списку категорій.
        search_fields (tuple): Поля, доступні для пошуку.
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Налаштування для моделі Tag в адмінпанелі Django.

    Визначає:
        - Поля для відображення у списку тегів (`list_display`).
        - Поля для пошуку (`search_fields`).

    Атрибути:
        list_display (tuple): Поля, які відображаються у списку тегів.
        search_fields (tuple): Поля, доступні для пошуку.
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Налаштування для моделі Comment в адмінпанелі Django.

    Визначає:
        - Поля для відображення у списку коментарів (`list_display`).
        - Можливості фільтрації (`list_filter`).
        - Поля для пошуку (`search_fields`).

    Атрибути:
        list_display (tuple): Поля, які відображаються у списку коментарів.
        list_filter (tuple): Поля для фільтрації.
        search_fields (tuple): Поля, доступні для пошуку.
    """
    list_display = ('post', 'author', 'created_at')
    list_filter = ('post', 'author')
    search_fields = ('text',)
