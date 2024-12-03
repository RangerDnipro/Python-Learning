"""
Файл models.py для додатку blog.

Містить моделі Category, Tag, Post та Comment, які описують структуру даних для блогу.
"""

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Модель для категорій блогу.

    Поля:
        name (CharField): Назва категорії (унікальна).

    Методи:
        __str__: Повертає рядок із назвою категорії.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Модель для тегів дописів.

    Поля:
        name (CharField): Назва тегу (унікальна).

    Методи:
        __str__: Повертає рядок із назвою тегу.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Модель для дописів блогу.

    Поля:
        title (CharField): Заголовок допису.
        content (TextField): Текст допису.
        author (ForeignKey): Зв'язок із користувачем, який створив допис.
        categories (ManyToManyField): Категорії, пов'язані з дописом.
        tags (ManyToManyField): Теги, пов'язані з дописом.
        created_at (DateTimeField): Дата створення допису.

    Методи:
        __str__: Повертає рядок із заголовком допису.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Модель для коментарів до дописів.

    Поля:
    post (ForeignKey): Зв'язок із дописом, до якого належить коментар.
    author (ForeignKey): Зв'язок із користувачем, який залишив коментар.
    content (TextField): Текст коментаря.
    created_at (DateTimeField): Дата створення коментаря.

    Методи:
        __str__: Повертає рядок із інформацією про автора коментаря та пов'язаний допис.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Коментар від {self.author} до {self.post.title}"
