"""
Модуль для представлень додатку
"""

from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    """
    Вихід із системи через GET або POST.
    """
    logout(request)
    return redirect("/login/")


def home_redirect_view(request):
    """
    Перенаправлення користувача залежно від його автентифікації.
    """
    if request.user.is_authenticated:
        # Якщо користувач автентифікований, перенаправляємо на /api/docs#/
        return redirect("/api/docs#/")
    else:
        # Якщо ні, перенаправляємо на /login/
        return redirect("/login/")
