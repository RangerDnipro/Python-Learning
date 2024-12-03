"""
Серіалізатори для додатка Library
"""

from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для моделі Book
    """

    url = serializers.SerializerMethodField()  # Додаємо поле URL для зручного переходу в конкретну книгу

    class Meta:
        model = Book  # Модель для серіалізації
        fields = ['id', 'title', 'author', 'genre', 'publication_year', 'user', 'created_at',
                  'url']  # Поля для серіалізації
        read_only_fields = ['user']  # Поле user доступне лише для читання

    def get_url(self, obj):
        """
        Генерує URL для доступу до конкретної книги.
        """
        request = self.context.get('request')
        return reverse('book-detail', args=[obj.id], request=request)
