"""
Модуль з асинхронним завданням для імпорту CSV
"""

import csv

from celery import shared_task
from django.core.mail import send_mail

from .models import Author, Book


@shared_task
def import_books_from_csv(file_path):
    """
    Імпорт книг із CSV-файлу та збереження їх у базі даних.
    """
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            author, _ = Author.objects.get_or_create(name=row['author'])
            Book.objects.create(
                title=row['title'],
                publication_date=row['publication_date'],
                author=author
            )

    # Надсилаємо email після завершення
    send_mail(
        'Імпорт завершено',
        'Імпорт даних з CSV завершено успішно.',
        'from@example.com',
        ['to@example.com']
    )
