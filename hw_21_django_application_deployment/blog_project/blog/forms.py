"""
Файл forms.py для додатку blog.

Містить форми для створення нового допису та додавання коментарів.
"""

from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    Форма для створення нового допису.

    Додаткові поля:
        - categories: Текстове поле для введення категорій через кому.
        - tags: Текстове поле для введення тегів через кому.

    Атрибути Meta:
        model (Model): Вказує модель Post.
        fields (list): Поля, доступні для заповнення у формі.

    Поля:
        title: Заголовок допису.
        content: Зміст допису.
        categories: Поле для вводу категорій.
        tags: Поле для вводу тегів.
    """
    categories = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введіть категорії через кому'}),
        help_text="Наприклад: Технології, Мистецтво, Наука"
    )
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введіть теги через кому'}),
        help_text="Наприклад: Python, Django, Web"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'tags']


class CommentForm(forms.ModelForm):
    """
    Форма для додавання коментарів.

    Атрибути Meta:
        model (Model): Вказує модель Comment.
        fields (list): Поля, доступні для заповнення у формі.

    Поля:
        content: Текст коментаря.
    """

    class Meta:
        model = Comment
        fields = ['content']
