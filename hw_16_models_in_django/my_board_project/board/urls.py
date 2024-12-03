"""
Модуль містить маршрутизацію, визначає шляхи для кожного представлення в додатку
"""

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    # Використовуємо RecentAdsView для домашньої сторінки
    path('', views.RecentAdsView.as_view(), name='home'),
    path('active_ads/<str:category_name>/', views.active_ads_by_category_view, name='active_ads_by_category'),
    path('create_ad/', views.CreateAdView.as_view(), name='create_ad'),
    # URL для "Мої оголошення"
    path('my_ads/', views.MyAdsView.as_view(), name='my_ads'),
    # URL для редагування оголошення
    path('edit_ad/<int:pk>/', views.EditAdView.as_view(), name='edit_ad'),
    # Сторінка входу
    path('login/', LoginView.as_view(template_name='board/login.html'), name='login'),
    # Сторінка виходу з перенаправленням на головну
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    # URL для перегляду оголошення
    path('ad/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    # Додаємо маршрут для редагування профілю
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
