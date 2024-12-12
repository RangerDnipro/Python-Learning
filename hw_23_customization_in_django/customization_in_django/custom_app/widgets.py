"""
Модуль з віджетом користувача
"""

from django.forms.widgets import Select


class CustomSelect(Select):
    """
    Кастомний віджет для поля вибору.
    """

    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs, choices)
