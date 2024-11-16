"""
Модуль містить визначення моделей додатку, що відповідають за структуру даних у базі
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_image_size(image):
    """
    Обмежує максимальний розмір аватарки в мегабайтах
    :param image: зображення, яке завантажує користувач
    :raises ValidationError: якщо зображення перевищує обмеження по розміру
    """
    max_size_mb = 2
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Розмір файлу не може перевищувати {max_size_mb} MB.")


class UserProfile(models.Model):
    """
    Модель профілю користувача, розширює вбудовану модель User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True,
                               null=True, validators=[validate_image_size])

    def __str__(self) -> str:
        """
        Повертає ім'я користувача як текстове представлення моделі
        :return: ім'я користувача
        """
        return self.user.username  # pylint: disable=no-member
