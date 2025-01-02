"""
Модуль з шляхами генератора QR-кодів
"""

from django.urls import path
from . import views

urlpatterns = [
    path('<str:short_url>/', views.generate_qr_code, name='generate_qr_code'),
]
