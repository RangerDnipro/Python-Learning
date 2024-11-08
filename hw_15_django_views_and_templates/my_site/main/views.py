"""
Модуль для створення представлень (views) додатку. Представлення обробляють HTTP-запити
та повертають HTTP-відповіді (наприклад, шаблони чи текст)
"""

from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse


# Функціональне відображення для головної сторінки
def home(request: HttpRequest) -> HttpResponse:
    """
    Відображає головну сторінку із привітальним текстом
    :param request: HTTP-запит
    :return: HTTP-відповідь із відображенням головної сторінки
    """
    return render(request, 'main/home.html')


# Функціональне відображення для сторінки "Про нас"
def about(request: HttpRequest) -> HttpResponse:
    """
    Відображає сторінку "Про нас" із інформацією про компанію
    :param request: HTTP-запит
    :return: HTTP-відповідь із відображенням сторінки "Про нас"
    """
    context = {'last_updated': datetime(2024, 11, 8)}
    return render(request, 'main/about.html', context)


# Класове відображення для сторінки контактів
class ContactView(View):
    """
    Відображає контактну сторінку з інформацією про контакти
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        # Контактні дані
        context = {
            'address': 'вул. Центральна 123, Київ, Україна',
            'phone': '+38 (044) 123-45-67',
            'email': 'contact@mycompany.com',
        }
        return render(request, 'main/contact.html', context)


# Класове відображення для сторінки послуг
class ServiceView(View):
    """
    Відображає сторінку "Послуги", де представлені послуги компанії
    з можливістю фільтрації за ключовим словом
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        # Дефолтний список послуг
        services = [
            {'name': 'Консультація', 'description':
                'Ми надаємо консультації з усіх аспектів вашого бізнесу.'},
            {'name': 'Маркетинг', 'description':
                'Наші маркетингові стратегії допоможуть збільшити ваші продажі.'},
            {'name': 'Розробка веб-сайтів', 'description':
                'Створюємо сучасні та зручні веб-сайти.'},
            {'name': 'SEO Оптимізація', 'description':
                'Оптимізуємо ваш сайт для покращення позицій у пошукових системах.'},
        ]

        # Отримання значення з GET параметра 'q' (ключове слово)
        query = request.GET.get('q', '').strip().lower()

        # Фільтрація послуг на основі ключового слова в назві або описі
        if query:
            services = [service for service in services if query in service['name'].lower()
                        or query in service['description'].lower()]

        context = {
            'services': services,
            'query': query  # Передача пошукового запиту для збереження його в шаблоні
        }
        return render(request, 'main/services.html', context)
