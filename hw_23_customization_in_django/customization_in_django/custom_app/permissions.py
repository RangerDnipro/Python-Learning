"""
Модуль для дозволів
"""

from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Дозвіл для доступу: тільки адміністратори можуть змінювати, всі інші можуть лише читати.
    """

    def has_permission(self, request, view):
        # Дозвіл на читання для всіх
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Дозвіл на зміну тільки для адміністратора
        return request.user and request.user.is_staff
