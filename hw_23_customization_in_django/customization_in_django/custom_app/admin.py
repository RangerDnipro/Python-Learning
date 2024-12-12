"""
Модуль адміністрування
"""

from django.contrib import admin
from .models import CustomModel


@admin.register(CustomModel)
class CustomModelAdmin(admin.ModelAdmin):
    """
    Кастомне відображення моделі CustomModel в адмінці.
    """
    list_display = ('name', 'word_count')
    search_fields = ('name',)
