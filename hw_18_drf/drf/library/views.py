"""
Представлення (Views) для додатка Library
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для моделі Book. Використовується для автоматичного створення маршрутів
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Доступ лише для автентифікованих користувачів
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'genre', 'publication_year']
    search_fields = ['title']
    ordering_fields = ['title', 'publication_year']

    def perform_create(self, serializer):
        """
        Зберігає нову книгу з прив'язкою до користувача, який створив запис
        """
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Надає доступ до видалення тільки адміністраторам
        """
        if self.action == 'destroy':
            return [IsAdminUser()]
        return super().get_permissions()
