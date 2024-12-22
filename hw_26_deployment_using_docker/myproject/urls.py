"""
Модуль налаштувань маршрутів для проекту Django.
"""

from django.http import HttpResponse
from django.urls import path


def home(request):
    """
    Відображає текстове повідомлення.
    :param request: Запит від користувача.
    :return: Текстове повідомлення.
    """
    return HttpResponse("Django in Docker is working!")


urlpatterns = [
    path("", home),  # Головна сторінка
]
