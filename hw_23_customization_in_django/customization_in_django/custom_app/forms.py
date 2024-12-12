"""
Модуль з моделями проєкту
"""

import re
from django import forms
from .models import Profile
from .validators import no_prohibited_words, PROHIBITED_WORDS
from .widgets import CustomSelect


class HexColorField(forms.CharField):
    """
    Кастомне поле форми для перевірки HEX-коду кольору.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7  # Формат: #RRGGBB
        kwargs['widget'] = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Наприклад, #FFFFFF',
        })
        super().__init__(*args, **kwargs)

    def clean(self, value):
        """
        Перевіряє, чи значення відповідає формату HEX-коду.
        """
        value = super().clean(value)
        if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
            raise forms.ValidationError("Некоректний HEX-код кольору.")
        return value


class CustomForm(forms.Form):
    """
    Кастомна форма для демонстрації валідатора та кастомного віджета з полем телефону
    з полем HEX-коду кольору.
    """
    name = forms.CharField(
        max_length=100,
        label="Текст",
        validators=[no_prohibited_words],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': f"Заповніть це поле без слів {', '.join(PROHIBITED_WORDS)}",
        })
    )
    hex_color = HexColorField(
        label="HEX-код кольору",
        required=False,
    )
    category = forms.ChoiceField(
        choices=[('cat1', 'Категорія 1'), ('cat2', 'Категорія 2')],
        label="Категорія",
        widget=CustomSelect()
    )

    def clean_name(self):
        """
        Перетворює текст у верхній регістр після валідації.
        """
        name = self.cleaned_data.get('name')
        return name.upper()


class ProfileForm(forms.ModelForm):
    """
    Форма для редагування профілю.
    """

    class Meta:
        model = Profile
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть номер телефону у форматі +123456789',
            }),
        }
