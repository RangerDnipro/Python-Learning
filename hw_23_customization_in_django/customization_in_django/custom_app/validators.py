"""
Модуль містить кастомний валідатор
"""

from django.core.exceptions import ValidationError

# Заборонені слова
PROHIBITED_WORDS = ['spam', 'advertisement', 'banned']


def no_prohibited_words(value: str):
    """
    Валідатор, який перевіряє, чи текст не містить заборонених слів.
    :param value: Значення для перевірки
    :raises ValidationError: Якщо знайдено заборонені слова
    """
    for word in PROHIBITED_WORDS:
        if word in value.lower():
            raise ValidationError(f"Текст містить заборонене слово: '{word}'")
