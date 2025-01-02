"""
Модуль з представленнями
"""

import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from shortener.models import URL  # Імпортуємо модель URL


def generate_qr_code(request, short_url):
    """
    Генерує QR-код для заданого скороченого URL і повертає його як зображення.
    """
    # Отримуємо об'єкт URL за short_url
    url_object = get_object_or_404(URL, short_url=short_url)
    # Створення QR-коду
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url_object.original_url)
    qr.make(fit=True)

    # Генерація зображення QR-коду
    img = qr.make_image(fill_color="black", back_color="white")

    # Повертаємо зображення як HTTP-відповідь
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response
