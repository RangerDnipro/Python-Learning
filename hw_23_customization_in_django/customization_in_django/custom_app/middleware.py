"""
Модуль для кастомних middleware
"""

import logging
from django.utils.deprecation import MiddlewareMixin


class RequestMetricsMiddleware(MiddlewareMixin):
    """
    Middleware для підрахунку запитів.
    """
    total_requests = 0

    def process_request(self, request):
        # Підрахунок запитів
        RequestMetricsMiddleware.total_requests += 1

    @staticmethod
    def get_total_requests():
        """
        Повертає загальну кількість запитів.
        """
        return RequestMetricsMiddleware.total_requests


logger = logging.getLogger('django')


class RequestLoggingMiddleware:
    """
    Middleware для логування кожного HTTP-запиту.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логування інформації про запит
        logger.info(f"Запит {request.method} до {request.path}")

        response = self.get_response(request)

        # Логування інформації про відповідь
        logger.info(f"Відповідь {response.status_code} для {request.path}")

        return response


class CustomHeaderMiddleware:
    """
    Middleware для додавання кастомного заголовка до кожної відповіді.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Перед обробкою запиту
        response = self.get_response(request)

        # Додавання кастомного заголовка
        response['X-Custom-Header'] = 'Hello from Django Middleware'

        return response
