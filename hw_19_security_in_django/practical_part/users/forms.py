"""
Опис форм для реєстрації, авторизації та додавання коментарів
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Comment


class UserRegisterForm(UserCreationForm):
    """
    Форма для реєстрації нового користувача
    Використовує вбудовану форму UserCreationForm для створення користувачів
    Додає обов'язкове поле для введення електронної пошти
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Ім\'я користувача',
            'email': 'Електронна пошта',
            'password1': 'Пароль',
            'password2': 'Підтвердження пароля'
        }


class UserLoginForm(forms.Form):
    """
    Форма для входу користувача
    Містить два поля:
    - username: Ім'я користувача
    - password: Пароль (використовується PasswordInput для безпечного введення)
    """
    username = forms.CharField(max_length=150, label='Ім\'я користувача')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class CommentForm(forms.ModelForm):
    """
    Форма для додавання коментаря
    Містить одне поле:
    - text: Текст коментаря (обмеження до 500 символів)
    Використовує Textarea для більш зручного введення коментарів з можливістю розширення
    """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш коментар...'})
        }
        labels = {
            'text': 'Коментар'
        }
