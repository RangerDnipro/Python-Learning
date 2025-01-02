"""
Модуль містить моделі для скорочення URL-адрес і відстеження кліків.
Моделі:
- URL: Зберігає оригінальні та скорочені URL-адреси.
- URLClick: Відстежує кліки за скороченими URL-адресами з інформацією про пристрій, країну та час кліку.
"""

from django.contrib.auth.models import User
from django.db import models
import random
import string


def generate_short_url():
    """
    Генерує випадковий короткий URL з 8 символів.
    Використовуються букви латинського алфавіту (великі та малі) і цифри.
    :return: Випадковий рядок довжиною 8 символів.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


class URL(models.Model):
    """
    Модель для зберігання оригінальних і скорочених URL.
    Поля:
    - original_url: Оригінальна URL-адреса (унікальна).
    - short_url: Скорочена URL-адреса (унікальна, довжиною до 8 символів).
    - created_by: Користувач, який створив запис.
    - created_at: Дата і час створення запису.
    """
    original_url = models.URLField(unique=True)
    short_url = models.URLField(max_length=8, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Перевіряє, чи є скорочений URL. Якщо його немає, генерує новий.
        Викликає батьківський метод save() для збереження даних у базу.
        """
        if not self.short_url:
            self.short_url = generate_short_url()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Повертає скорочений URL у вигляді рядка.
        :return: Скорочений URL.
        """
        return self.short_url


class URLClick(models.Model):
    """
    Модель для відстеження кліків за скороченими URL.
    Поля:
    - url: URL, до якого прив’язаний клік.
    - user: Користувач, який здійснив клік (може бути Null, якщо не автентифікований).
    - clicked_at: Дата і час кліку.
    - device_type: Тип пристрою, з якого здійснено клік (PC, Mobile, Tablet, Unknown).
    - country: Країна, з якої здійснено клік.
    """
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='clicks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)
    device_type = models.CharField(max_length=10, choices=[('PC', 'PC'), ('Mobile', 'Mobile'), ('Tablet', 'Tablet'), ('Unknown', 'Unknown')], default='Unknown')
    country = models.CharField(max_length=50, default='Unknown')

    def __str__(self):
        """
        Повертає строкове представлення кліку.
        Формат: <URL>|<User>|<Дата кліку>.
        :return: Строкове представлення кліку.
        """
        return f"{self.url}|{self.user}|{self.clicked_at}"
