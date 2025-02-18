"""
Модуль містить маршрутизацію, визначає шляхи для кожного представлення в додатку
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('services/', views.ServiceView.as_view(), name='services'),
]
