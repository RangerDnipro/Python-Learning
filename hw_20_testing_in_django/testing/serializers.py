"""
Серіалізатори для додатка
"""

from datetime import date

from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """
    Спрощений серіалізатор для користувача, без перевірки унікальності
    """
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()


class TaskSerializer(serializers.Serializer):
    """
    Серіалізатор для задач із прив'язкою до користувача.
    """
    user = UserSerializer(required=False)  # Поле може бути відсутнім
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False)
    due_date = serializers.DateField(required=True)

    def validate_due_date(self, value: date) -> date:
        """
        Кастомна перевірка, чи дата не в минулому.
        """
        if value < date.today():
            raise serializers.ValidationError("Дата не може бути в минулому.")
        return value
