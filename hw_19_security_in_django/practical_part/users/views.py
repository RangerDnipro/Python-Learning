"""
Представлення (Views) для Django-додатка
"""

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect

from .forms import UserRegisterForm, UserLoginForm, CommentForm
from .models import Comment


def home_view(request):
    """
    Відображає головну сторінку
    Дозволяє користувачам залишати коментарі та переглядати наявні коментарі
    При поданні форми з коментарем обробляється збереження коментаря від користувача
    :param request: HTTP-запит
    :return: HTTP-відповідь, що містить головну сторінку з формою коментарів та списком коментарів
    """
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Прив'язуємо коментар до користувача
            comment.save()
            messages.success(request, 'Ваш коментар успішно додано!')
            return redirect('home')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = CommentForm()

    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'users/home.html', {'form': form, 'comments': comments})


def register_view(request):
    """
    Відображає форму реєстрації нового користувача та обробляє її
    Після успішної реєстрації здійснює спробу автоматичної авторизації
    :param request: HTTP-запит
    :return: HTTP-відповідь, що містить сторінку реєстрації або перенаправлення на головну сторінку після успішної реєстрації
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data['password1']
            user.set_password(raw_password)  # Хешуємо пароль
            user.save()
            messages.success(request, 'Реєстрація пройшла успішно!')

            # Аутентифікація після реєстрації
            authenticated_user = authenticate(request, username=user.username, password=raw_password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')
            else:
                messages.error(request, 'Автоматична авторизація не вдалася. Спробуйте увійти вручну.')
        else:
            print("Помилки форми реєстрації:", form.errors)
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    Відображає форму входу в систему та обробляє авторизацію користувача
    Підтримує тільки POST-запити для забезпечення безпеки передачі даних
    :param request: HTTP-запит
    :return: HTTP-відповідь, що містить сторінку входу або перенаправлення на головну сторінку після успішного входу
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = UserLoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Невірний логін або пароль')

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """
    Виконує вихід з системи користувача
    Після виходу користувача перенаправляє на головну сторінку
    :param request: HTTP-запит
    :return: HTTP-відповідь, що містить перенаправлення на головну сторінку
    """
    logout(request)
    messages.success(request, 'Ви вийшли з системи')
    return redirect('home')


class UserSearchForm(forms.Form):
    """
    Форма для пошуку користувача за іменем
    Містить одне поле для введення імені користувача, яке є обов'язковим
    """
    username = forms.CharField(max_length=150, required=True, label='Ім\'я користувача')


def execute_safe_query(query: str, params: tuple):
    """
    Виконує безпечний SQL-запит, використовуючи параметризовані запити
    :param query: SQL-запит у вигляді рядка
    :param params: Параметри для запиту у вигляді кортежу
    :return: Список результатів виконання запиту або None
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if query.strip().lower().startswith("select"):
            # Повертає всі результати для SELECT-запиту
            return cursor.fetchall()
    return None


def user_search_view(request):
    """
    Представлення для пошуку користувачів за іменем
    Відображає форму пошуку та обробляє запити на пошук користувачів
    :param request: HTTP-запит
    :return: HTTP-відповідь, що містить сторінку пошуку користувачів з результатами пошуку, якщо такі є
    """
    form = UserSearchForm()
    users = None

    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            query = "SELECT username, email FROM users_user WHERE username = %s"
            params = (username,)
            users = execute_safe_query(query, params)

    return render(request, 'users/user_search.html', {'form': form, 'users': users})
