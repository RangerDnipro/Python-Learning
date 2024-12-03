"""
Модуль з формами, що використовуються в проєкті
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from .models import UserProfile


class RegistrationForm(forms.ModelForm):
    """
    Форма для реєстрації користувача
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        """
        Перевіряє, чи паролі співпадають
        :return: Відфільтровані дані форми
        :raises forms.ValidationError: Якщо паролі не співпадають
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Паролі не співпадають!")
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    Форма для редагування профілю користувача
    """

    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'location', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_avatar(self):
        """
        Перевіряємо розмір зображення у формі
        :return: Перевірене зображення аватара
        :raises forms.ValidationError: Якщо розмір аватара перевищує 2 MB
        """
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Розмір аватара не може перевищувати 2 MB.")
        return avatar


class PasswordChangeForm(DjangoPasswordChangeForm):
    """
    Форма для зміни пароля користувача
    """

    def clean_new_password2(self):
        """
        Перевіряє, чи новий пароль не є таким самим, як старий
        :return: Підтверджений новий пароль
        :raises forms.ValidationError: Якщо новий пароль збігається з поточним паролем
        """
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 == self.cleaned_data.get('old_password'):
            raise forms.ValidationError("Новий пароль не може бути таким самим, як старий")
        return new_password2
