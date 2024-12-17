"""
Модуль для генерації даних
"""

import os
import django

# Налаштовуємо середовище Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')  # Шлях до settings.py
django.setup()

import random
from faker import Faker
from test_app.models import DataDocument, Author, Category, Tag

fake = Faker()


def generate_authors(n=10):
    """Генерує авторів."""
    authors = []
    for _ in range(n):
        author = Author.objects.create(
            name=fake.name(),
            email=fake.email()
        )
        authors.append(author)
    print(f"Створено {n} авторів.")
    return authors


def generate_categories(n=5):
    """Генерує категорії."""
    categories = []
    for _ in range(n):
        category = Category.objects.create(
            name=fake.word().capitalize()
        )
        categories.append(category)
    print(f"Створено {n} категорій.")
    return categories


def generate_tags(n=8):
    """Генерує теги."""
    tags = []
    for _ in range(n):
        tag = Tag.objects.create(
            name=fake.word()
        )
        tags.append(tag)
    print(f"Створено {n} тегів.")
    return tags


def generate_data_documents(n=50, authors=None, categories=None, tags=None):
    """Генерує документи."""
    for _ in range(n):
        document = DataDocument.objects.create(
            title=fake.sentence(nb_words=4),
            description=fake.paragraph(nb_sentences=3),
            author=random.choice(authors) if authors else None,  # Додаємо випадкового автора
            category=random.choice(categories) if categories else None  # Додаємо випадкову категорію
        )
        # Додаємо випадкові теги
        if tags:
            document.tags.add(*random.sample(tags, k=random.randint(1, 3)))

        document.save()
    print(f"Створено {n} документів.")


if __name__ == "__main__":
    # Очищаємо існуючі дані
    DataDocument.objects.all().delete()
    Author.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()

    # Генеруємо нові дані
    authors = generate_authors(n=10)
    categories = generate_categories(n=5)
    tags = generate_tags(n=8)
    generate_data_documents(n=50, authors=authors, categories=categories, tags=tags)

    print("Генерацію тестових даних завершено.")
