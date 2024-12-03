"""
Файл views.py для додатку accounts.

Містить обробники запитів для реєстрації користувачів, входу, виходу,
перегляду, редагування та видалення профілів, а також надсилання вітальних листів.
"""

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import UserRegisterForm, ProfileUpdateForm
from .models import Profile


def register(request):
    """
    Обробник для реєстрації нового користувача.

    Якщо метод запиту POST, обробляє введені дані для створення нового користувача
    та його профілю. Надсилає вітальний email і автоматично авторизує користувача.

    :param request: Об'єкт запиту Django.
    :return: HTTP-відповідь із формою реєстрації або перенаправленням на головну сторінку.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                bio=form.cleaned_data.get('bio'),
                phone=form.cleaned_data.get('phone'),
                avatar=form.cleaned_data.get('avatar'),
            )
            send_welcome_email(user.email)
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """
    Обробник для входу користувача в систему.

    Використовує стандартну форму автентифікації для перевірки даних
    і авторизації користувача.

    :param request: Об'єкт запиту Django.
    :return: HTTP-відповідь із формою входу або перенаправленням на головну сторінку.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """
    Обробник для виходу користувача з системи.

    :param request: Об'єкт запиту Django.
    :return: Перенаправлення на головну сторінку.
    """
    logout(request)
    return redirect('/')


@login_required
def profile(request):
    """
    Відображає профіль авторизованого користувача.

    Якщо профіль не існує, він автоматично створюється.

    :param request: Об'єкт запиту Django.
    :return: HTTP-відповідь із даними профілю користувача.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


def send_welcome_email(user_email: str) -> None:
    """
    Надсилає вітальний email новому користувачу.

    :param user_email: Email-адреса користувача.
    :return: None.
    """
    from django.core.mail import send_mail
    try:
        send_mail(
            'Ласкаво просимо!',
            'Дякуємо за реєстрацію на нашому сайті!',
            'test_for_django@ukr.net',
            [user_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Помилка під час надсилання листа: {e}")


@login_required
def edit_profile(request):
    """
    Обробник для редагування профілю користувача.

    :param request: Об'єкт запиту Django.
    :return: HTTP-відповідь із формою редагування профілю або перенаправленням до профілю.
    """
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def delete_profile(request):
    """
    Обробник для видалення профілю користувача.

    :param request: Об'єкт запиту Django.
    :return: Перенаправлення на головну сторінку після видалення профілю.
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('/')
    return render(request, 'accounts/delete_profile.html')
