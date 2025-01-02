"""
Модуль з тестами для генерації QR-кодів
"""

from django.test import TestCase
from django.urls import reverse
from shortener.models import URL


class QRCodeTests(TestCase):
    def setUp(self):
        """
        Налаштовуємо тестові дані перед виконанням тестів.
        """
        self.url = URL.objects.create(original_url="https://example.com", short_url="short123")

    def test_qr_code_generation(self):
        """
        Тестуємо генерацію QR-коду для заданого short_url.
        """
        response = self.client.get(reverse('generate_qr_code', args=[self.url.short_url]))
        # Перевіряємо, що відповідь має статус 200
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, що відповідь містить зображення QR-коду
        self.assertEqual(response['Content-Type'], 'image/png')
