"""
Файл forms.py для додатку accounts.

Містить форми для реєстрації користувачів, а також оновлення профілю.
Використовуються стандартні форми Django з додатковими полями.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserRegisterForm(UserCreationForm):
    """
    Форма для реєстрації нових користувачів.

    Додаткові поля:
        - email: Обов'язкове поле для введення email-адреси.
        - bio: Поле для біографії, необов'язкове.
        - phone: Поле для номера телефону, необов'язкове.
        - avatar: Поле для завантаження аватару, необов'язкове.

    Атрибути Meta:
        model (Model): Вказує модель User.
        fields (list): Поля, доступні для заповнення у формі.
    """
    email = forms.EmailField(required=True)
    bio = forms.CharField(required=False, widget=forms.Textarea, label='Біографія')
    phone = forms.CharField(required=False, max_length=15, label='Телефон')
    avatar = forms.ImageField(required=False, label='Аватар')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'phone', 'avatar']


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма для оновлення профілю користувача.

    Поля:
        - bio: Поле для оновлення біографії.
        - phone: Поле для оновлення номера телефону.
        - avatar: Поле для завантаження або оновлення аватару.

    Атрибути Meta:
        model (Model): Вказує модель Profile.
        fields (list): Поля, доступні для редагування.
    """

    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'avatar']
