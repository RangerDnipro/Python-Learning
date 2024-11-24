"""
Налаштування адміністративної панелі Django для моделі користувача
"""

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Конфігурація адміністративної панелі для моделі Task
    """
    list_display = ('title', 'due_date', 'created_by', 'created_at')  # Поля для відображення
    search_fields = ('title', 'description')  # Поля для пошуку
    list_filter = ('due_date', 'created_by')  # Фільтри


class CustomUserAdmin(UserAdmin):
    """
    Кастомна панель адміністратора для моделі User з відображенням email
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')  # Поля для відображення
    search_fields = ('username', 'email')  # Поля для пошуку
    list_filter = ('is_staff', 'is_superuser', 'is_active')  # Фільтри


# Перереєстрація моделі User із кастомною конфігурацією
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
