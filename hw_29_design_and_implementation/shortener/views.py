"""
Модуль містить view-функції для обробки запитів, пов’язаних зі скороченням URL-адрес та їх статистикою.
Функції:
- home: Обробка головної сторінки для створення скорочених URL.
- get_country_from_ip: Визначення країни за IP-адресою.
- redirect_to_url: Перенаправлення за скороченим URL і логування кліка.
- user_statistics: Відображення статистики URL-адрес для авторизованих користувачів.
"""

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from geoip2.database import Reader
from user_agents import parse

from .forms import URLForm
from .models import URL, URLClick


@login_required(login_url='login')
def home(request):
    """
    Обробляє запити на головну сторінку для створення скорочених URL-адрес.
    Підтримує методи GET і POST.

    Якщо POST-запит успішний, створює новий скорочений URL або повертає існуючий.

    :param request: Об'єкт запиту Django.
    :return: Відображення шаблону 'shortener/home.html'.
    """
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            url, created = URL.objects.get_or_create(
                original_url=original_url,
                created_by=request.user if request.user.is_authenticated else None
            )
            if created:
                url.save()
            clicks = url.clicks.count()
            return render(request, 'shortener/home.html',
                          context={'short_url': request.build_absolute_uri(url.short_url), 'clicks': clicks})
    else:
        form = URLForm()
    return render(request, 'shortener/home.html', {'form': form})


def get_country_from_ip(ip_address):
    """
    Визначає країну за IP-адресою.

    :param ip_address: IP-адреса користувача.
    :return: Назва країни або 'Unknown', якщо визначити країну не вдалося.
    """
    if ip_address == '127.0.0.1':
        return "Localhost"
    geoip_path = settings.BASE_DIR / 'geoip/GeoLite2-Country.mmdb'
    reader = Reader(str(geoip_path))
    try:
        response = reader.country(ip_address)
        return response.country.name
    except Exception:
        return "Unknown"


def redirect_to_url(request, short_url):
    """
    Перенаправляє користувача на оригінальний URL і логує інформацію про клік.

    Логування включає:
    - Тип пристрою.
    - Країну користувача.
    - IP-адресу.

    :param request: Об'єкт запиту Django.
    :param short_url: Скорочений URL для пошуку оригінального.
    :return: Перенаправлення на оригінальний URL.
    """
    url = get_object_or_404(URL, short_url=short_url)
    user_agent = parse(request.META['HTTP_USER_AGENT'])

    # Визначення типу пристрою
    device_type = 'Unknown'
    if user_agent.is_mobile:
        device_type = 'Mobile'
    elif user_agent.is_tablet:
        device_type = 'Tablet'
    elif user_agent.is_pc:
        device_type = 'PC'

    # Визначення IP-адреси
    ip_address = request.META.get('REMOTE_ADDR', '')
    country = get_country_from_ip(ip_address)

    # Запис кліку
    URLClick.objects.create(
        url=url,
        user=request.user if request.user.is_authenticated else None,
        device_type=device_type,
        country=country
    )

    return redirect(url.original_url)


@login_required
def user_statistics(request):
    """
    Відображає статистику URL-адрес для авторизованих користувачів.

    Адміністратори бачать статистику для всіх URL-адрес,
    звичайні користувачі — лише для власних.

    :param request: Об'єкт запиту Django.
    :return: Відображення шаблону 'shortener/statistics.html' зі статистикою.
    """
    if request.user.is_staff:
        urls = URL.objects.all()  # Адміністратор бачить всі URL
    else:
        urls = URL.objects.filter(created_by=request.user)  # Звичайний користувач бачить лише свої URL
    return render(request, 'shortener/statistics.html', {'urls': urls})
