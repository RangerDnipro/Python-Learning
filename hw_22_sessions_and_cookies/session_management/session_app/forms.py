"""
Модуль з формами проєкту
"""

from django import forms


class UserForm(forms.Form):
    """
    Форма для введення імені та віку користувача.
    """
    name = forms.CharField(
        label='Ваше ім\'я',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Введіть ім\'я'})
    )
    age = forms.IntegerField(
        label='Ваш вік',
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Введіть вік'})
    )
