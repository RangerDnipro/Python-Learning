"""
Модуль містить визначення моделей додатку, що відповідають за структуру даних у базі
"""

from datetime import timedelta
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import OneToOneField, CharField
from django.utils import timezone


class Category(models.Model):
    """
    Модель для представлення категорій оголошень
    """

    name: str = models.CharField(max_length=255, unique=True)
    description: str = models.TextField()

    def active_ads_count(self) -> int:
        """
        Повертає кількість активних оголошень у цій категорії
        :return: Кількість активних оголошень
        """
        return self.ad_set.filter(is_active=True).count()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Ad(models.Model):
    """
    Модель для представлення оголошень
    """

    title: str = models.CharField(max_length=255)
    description: str = models.TextField()
    price: float = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at: timezone.datetime = models.DateTimeField()
    updated_at: timezone.datetime = models.DateTimeField(auto_now=True)
    is_active: bool = models.BooleanField(default=True)
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    category: models.ForeignKey = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def short_description(self) -> str:
        """
        Повертає скорочений опис (до 100 символів)
        :return: Скорочений опис оголошення
        """
        return self.description[:100] + '...' if len(self.description) > 100 else self.description

    def deactivate(self):
        """
        Деактивує оголошення після 30 днів з моменту створення.
        """
        if self.created_at < timezone.now() - timedelta(days=30):
            self.is_active = False

    def save(self, *args, **kwargs):
        # Якщо поле created_at не встановлене, використовуємо поточний час
        if self.created_at is None:
            self.created_at = timezone.now()

        # Перевірка дати для автоматичної деактивації
        if self.created_at < timezone.now() - timedelta(days=30):
            self.is_active = False

    def __str__(self) -> str:
        return f"{self.title} - {self.price} грн"

    class Meta:
        verbose_name: str = "Оголошення"
        verbose_name_plural: str = "Оголошення"


class Comment(models.Model):
    """
    Модель для представлення коментарів до оголошень
    """

    content: str = models.TextField()
    created_at: timezone.datetime = models.DateTimeField(auto_now_add=True)
    ad: models.ForeignKey = models.ForeignKey(Ad, related_name='comments', on_delete=models.CASCADE)
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Коментар від {self.user.username} до {self.ad.title}"

    class Meta:
        verbose_name: str = "Коментар"
        verbose_name_plural: str = "Коментарі"


class UserProfile(models.Model):
    """
    Модель користувача яка містить додаткові атрибути, такі як номер телефону та адреса
    """
    user: OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number: CharField = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефону")
    address: CharField = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адреса")

    def __str__(self):
        return f"Профіль користувача: {self.user.username}"
