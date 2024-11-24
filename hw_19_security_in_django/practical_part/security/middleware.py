"""
Middleware для логування запитів та обробки помилок
"""

import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class AccessLoggingMiddleware(MiddlewareMixin):
    """
    Middleware, який логує всі спроби доступу до захищених сторінок
    """

    def process_request(self, request):
        # Приклад перевірки доступу до захищених сторінок
        if request.path.startswith('/protected/'):
            logger.info(f'Спроба доступу до захищеної сторінки користувачем: {request.user}')


class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    Middleware для обробки помилок 404 та 500
    """

    def process_response(self, request, response):
        if response.status_code == 404:
            logger.warning(f'Помилка 404: Сторінку не знайдено за URL: {request.path}')
        elif response.status_code == 500:
            logger.error(f'Помилка 500: Помилка сервера під час доступу до URL: {request.path}')
        return response
