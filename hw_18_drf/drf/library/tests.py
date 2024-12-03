"""
Модуль для тестування
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book


class LibraryAPITestCase(APITestCase):
    """
    Тестування функціонала API бібліотеки
    """

    def setUp(self):
        """
        Налаштування для тестів: створення користувача та книги
        """
        # Створюємо тестового користувача
        self.user = User.objects.create_user(
            username="testuser",
            password="MyStrongP@ssword123"
        )
        self.client.force_authenticate(user=self.user)  # Примусова автентифікація
        self.book = Book.objects.create(
            title="Тестова книга",
            author="Тестовий автор",
            genre="Фантастика",
            publication_year=2023,
            user=self.user
        )
        # Отримуємо токен для авторизації
        response = self.client.post('/api/auth/jwt/create/', {
            'username': "testuser",
            'password': "MyStrongP@ssword123"
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_books(self):
        """
        Тест на отримання списку книг
        """
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Тестова книга")

    def test_create_book(self):
        """
        Тест на створення нової книги.
        """
        data = {
            "title": "Нова книга",
            "author": "Новий автор",
            "genre": "Драма",
            "publication_year": 2020
        }
        response = self.client.post('/api/books/', data)
        print(response.json())  # Лог для відстеження створення книги
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.order_by('-id').first().title, "Нова книга")

    def test_update_book(self):
        """
        Тест на оновлення інформації про книгу
        """
        data = {
            "title": "Оновлена книга"
        }
        response = self.client.patch(f'/api/books/{self.book.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Оновлена книга")

    def test_delete_book(self):
        """
        Тест на видалення книги
        """
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Тестовий користувач не адміністратор

        # Робимо користувача адміністратором і повторюємо тест
        self.user.is_staff = True
        self.user.save()
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books(self):
        """
        Тест на фільтрацію книг за жанром
        """
        response = self.client.get('/api/books/', {'genre': 'Фантастика'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['genre'], "Фантастика")
