"""
Представлення (Views) для Django-додатка
"""

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import TaskForm, CustomUserCreationForm
from .models import Task


def login_view(request):
    """
    Вхід користувача
    """

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """
    Вихід користувача
    """
    logout(request)
    return redirect('login')


def register_view(request):
    """
    Реєстрація нового користувача
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def task_list(request):
    """
    Сторінка завдань
    """
    tasks = Task.objects.all()
    # Перевірка, чи користувач авторизований
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                Task.objects.create(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    due_date=form.cleaned_data['due_date'],
                    created_by=request.user
                )
                return redirect('task_list')
        else:
            form = TaskForm()
        return render(request, 'tasks.html', {'tasks': tasks, 'form': form})
    else:
        # Для неавторизованих користувачів
        return render(request, 'tasks.html', {'tasks': tasks})
