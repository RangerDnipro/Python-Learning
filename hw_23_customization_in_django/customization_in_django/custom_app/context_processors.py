"""
Модуль для контекстного процесора
"""

from datetime import date
from .middleware import RequestMetricsMiddleware
from .models import CustomModel


def global_context(request):
    """
    Глобальні дані для всіх шаблонів.
    """
    return {
        'total_custom_texts': CustomModel.objects.count(),
        'current_date': date.today(),
        'total_requests': RequestMetricsMiddleware.get_total_requests(),
    }
