"""
Модуль з класами адміністративного інтерфейсу
"""

from django.contrib import admin
from django.db.models import Count
from .models import Category, Ad, Comment, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Адміністративний інтерфейс для моделі Category
    Відображає поля 'name' та 'description' у списку категорій
    """
    list_display = ('name', 'description', 'active_ads_count')

    def active_ads_count(self, obj):
        return obj.active_ads_count()

    active_ads_count.short_description = 'Активні оголошення'


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """
    Адміністративний інтерфейс для моделі Ad (Оголошення)
    - Відображає інформацію про оголошення, такі як 'title', 'price', 'created_at', 'is_active', 'user', 'category'
    - Надає можливість фільтрувати оголошення за категоріями, активністю та датою створення
    - Поля 'created_at' і 'updated_at' показуються у формі, але лише 'updated_at' є тільки для читання
    """
    list_display = ('title', 'price', 'created_at', 'is_active', 'user', 'category')
    list_filter = ('is_active', 'category', 'created_at')
    fields = ['title', 'description', 'price', 'created_at', 'updated_at', 'is_active', 'user', 'category']
    readonly_fields = ['updated_at']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(comments_count=Count('comments'))

    def comments_count(self, obj):
        return obj.comments_count

    comments_count.admin_order_field = 'comments_count'
    comments_count.short_description = 'Кількість коментарів'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Адміністративний інтерфейс для моделі Comment
    Відображає поля 'content', 'created_at', 'ad', 'user' у списку коментарів
    """
    list_display = ('content', 'created_at', 'ad', 'user')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Адміністративний інтерфейс для моделі UserProfile
    - Відображає поля 'user', 'phone_number', 'address'
    - Надає можливість пошуку за ім'ям користувача та номером телефону
    """
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')
