"""
Налаштування адміністративної панелі Django для моделі користувача
"""

from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Конфігурація адміністративної панелі для моделі User
    Відображає основні поля користувача та забезпечує можливість пошуку
    """
    list_display = ('username', 'email', 'is_active', 'is_admin', 'is_staff')
    search_fields = ('username', 'email')
