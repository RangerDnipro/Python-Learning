"""
Модуль для створення представлень (views) додатку. Представлення обробляють HTTP-запити
та повертають HTTP-відповіді (наприклад, шаблони чи текст)
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає головну сторінку, використовуючи шаблон home.html
    """
    return render(request, 'home/home.html')


def about_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає сторінку "Про нас", використовуючи шаблон about.html
    """
    return render(request, 'home/about.html')


def contact_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає сторінку контактів, використовуючи шаблон contact.html
    """
    return render(request, 'home/contact.html')


def post_view(request: HttpRequest, id: int) -> HttpResponse:
    """
    Відображає сторінку поста за ідентифікатором, використовуючи шаблон post.html
    :param id: Ідентифікатор поста
    """
    return render(request, 'home/post.html', {'id': id})


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    """
    Відображає сторінку профілю користувача, використовуючи шаблон profile.html
    :param username: Ім'я користувача
    """
    return render(request, 'home/profile.html', {'username': username})


def event_view(request: HttpRequest, year: str, month: str, day: str) -> HttpResponse:
    """
    Відображає сторінку події з датою, використовуючи шаблон event.html
    :param year: Рік події
    :param month: Місяць події
    :param day: День події
    """
    return render(request, 'home/event.html', {'year': year, 'month': month, 'day': day})
