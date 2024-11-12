"""
Модуль з формами, що використовуються в проєкті
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import EmailField
from django.forms import CharField
from .models import Comment, UserProfile


class UserRegistrationForm(UserCreationForm):
    email: EmailField = forms.EmailField(required=True, label="Електронна пошта")
    phone_number: CharField = forms.CharField(max_length=15, required=False, label="Номер телефону")
    address: CharField = forms.CharField(max_length=255, required=False, label="Адреса")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'address']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Паролі не співпадають")
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишіть свій коментар тут...'}),
        }
        labels = {
            'content': '',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']
