"""
Модуль з додатковими тегами Django
"""

from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(value, arg):
    """
    Додає CSS клас до віджета поля форми
    :param value: Віджет поля форми
    :param arg: Ім'я CSS класу, який потрібно додати
    :return: Віджет поля форми з доданим CSS класом
    """
    return value.as_widget(attrs={'class': arg})
