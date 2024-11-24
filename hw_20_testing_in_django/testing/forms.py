"""
Опис форм Django-додатка
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import DateTimeInput
from django.utils.timezone import now


class TaskForm(forms.Form):
    """
    Форма для створення задачі
    """
    title = forms.CharField(max_length=255, required=True, label="Назва")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Опис")
    due_date = forms.DateTimeField(
        required=True,
        label="Термін виконання",
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%d.%m.%Y %H:%M']  # Формат дати та часу
    )

    def clean_due_date(self):
        """
        Перевірка, чи термін виконання не є минулою датою
        :return: Валідована дата
        :raises: ValidationError, якщо дата у минулому
        """
        due_date = self.cleaned_data['due_date']
        if due_date < now():
            raise forms.ValidationError("Дата не може бути в минулому")
        return due_date


class CustomUserCreationForm(UserCreationForm):
    """
    Кастомна форма для реєстрації з додатковим полем email
    """
    email = forms.EmailField(required=True, label="Електронна пошта")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        """
        Зберігає користувача з email
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
