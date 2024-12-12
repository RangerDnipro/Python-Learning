"""
Модуль з кастомизацією для тегів і фільтрів
"""

from django import template

register = template.Library()


@register.filter
def to_lowercase(value: str) -> str:
    """
    Переводить текст у нижній регістр.
    :param value: Вхідний текст
    :return: Текст у нижньому регістрі
    """
    if isinstance(value, str):
        return value.lower()
    return value


@register.simple_tag
def total_texts(queryset) -> int:
    """
    Повертає кількість об'єктів у заданому QuerySet.
    :param queryset: QuerySet моделі
    :return: Кількість об'єктів
    """
    return queryset.count()
