import pytest
from datetime import date, timedelta
from testing.serializers import TaskSerializer, UserSerializer


@pytest.mark.django_db
class TestUserSerializer:
    """
    Тестування серіалізатора UserSerializer.
    """

    def test_user_serializer_valid(self):
        """
        Тест валідності UserSerializer із правильними даними.
        """
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_user_serializer_invalid(self):
        """
        Тест помилок у UserSerializer з некоректними даними.
        """
        data = {
            "username": "",  # Пусте ім'я користувача
            "email": "invalid-email",  # Некоректний email
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors  # Очікуємо помилку для пустого імені
        assert "email" in serializer.errors  # Очікуємо помилку для некоректного email


@pytest.mark.django_db
class TestTaskSerializer:
    """
    Тестування серіалізатора TaskSerializer.
    """

    def test_serializer_valid(self):
        """
        Тест валідності серіалізатора з правильними даними.
        """
        data = {
            "title": "Тестове завдання",
            "description": "Опис завдання",
            "due_date": (date.today() + timedelta(days=1)).isoformat(),  # Формат ISO-8601
        }
        serializer = TaskSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_serializer_invalid_missing_title(self):
        """
        Тест помилок, якщо обов'язкове поле `title` відсутнє.
        """
        data = {
            "description": "Опис завдання",
            "due_date": (date.today() + timedelta(days=1)).isoformat(),
        }
        serializer = TaskSerializer(data=data)
        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_serializer_invalid_due_date(self):
        """
        Тест кастомної валідації для поля `due_date`.
        """
        data = {
            "title": "Тестове завдання",
            "description": "Опис завдання",
            "due_date": (date.today() - timedelta(days=1)).isoformat(),  # Дата у минулому
        }
        serializer = TaskSerializer(data=data)
        assert not serializer.is_valid()
        assert "due_date" in serializer.errors


@pytest.mark.django_db
class TestNestedSerializers:
    """
    Тестування вкладених серіалізаторів.
    """

    def test_valid_nested_serializer(self):
        """
        Тест валідності даних із вкладеним серіалізатором.
        """
        user_data = {"username": "newuser", "email": "newuser@example.com"}
        data = {
            "user": user_data,
            "title": "Тестове завдання",
            "description": "Опис завдання",
            "due_date": (date.today() + timedelta(days=1)).isoformat(),
        }
        serializer = TaskSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
