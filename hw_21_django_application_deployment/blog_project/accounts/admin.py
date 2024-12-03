"""
Файл admin.py для додатку accounts
Містить налаштування моделі Profile для відображення та взаємодії з нею через адмінпанель Django.
"""

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Налаштування для моделі Profile в адмінпанелі Django.

    Цей клас визначає, як модель Profile буде відображатися в адмінпанелі.
    - list_display: Визначає поля, які будуть показані у списку об'єктів.
    - list_filter: Встановлює можливість фільтрувати список об'єктів за полями.
    - search_fields: Додає пошук за визначеними полями.

    Атрибути:
        list_display (tuple): Поля для відображення у списку об'єктів.
        list_filter (tuple): Поля, доступні для фільтрації.
        search_fields (tuple): Поля, доступні для пошуку.
    """
    list_display = ('user', 'phone', 'bio')
    list_filter = ('user',)
    search_fields = ('user__username', 'phone', 'bio')
