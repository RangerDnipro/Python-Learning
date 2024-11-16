"""
Модуль для створення представлень (views) додатку. Представлення обробляють HTTP-запити
та повертають HTTP-відповіді (наприклад, шаблони чи текст)
"""

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, UserProfileForm, PasswordChangeForm
from .models import UserProfile


def home_view(request):
    """
    Представлення для головної сторінки
    """
    return render(request, 'accounts/home.html')


def register_view(request):
    """
    Обробляє реєстрацію користувача
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Перевірка на існування профілю перед створенням
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Реєстрація успішна!")
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_list_view(request):
    """
    Відображає список всіх користувачів
    """
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})


def user_profile_view(request, user_id):
    """
    Відображає профіль іншого користувача
    """
    user = get_object_or_404(User, id=user_id)
    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def edit_profile_view(request):
    """
    Обробляє редагування профілю користувача
    """
    # Перевірка, чи існує профіль користувача, якщо ні - створення нового
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    """
    Обробляє зміну пароля користувача
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Пароль успішно змінено!")
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def profile_view(request):
    """
    Відображає профіль користувача
    """
    return render(request, 'accounts/profile.html')


@login_required
def delete_profile_view(request):
    """
    Представлення для видалення облікового запису користувача
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Ваш обліковий запис було успішно видалено.')
        return redirect('home')

    return render(request, 'accounts/delete_profile.html')
