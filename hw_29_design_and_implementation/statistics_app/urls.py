"""
Модуль з шляхами
"""

from django.urls import path
from . import views

urlpatterns = [
    path('detailed/', views.detailed_statistics, name='detailed_statistics'),
]
