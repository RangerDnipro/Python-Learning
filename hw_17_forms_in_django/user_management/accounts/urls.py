"""
Модуль містить маршрутизацію, визначає шляхи для кожного представлення в додатку
"""

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html'), name='change_password'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('delete_profile/', views.delete_profile_view, name='delete_profile'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:user_id>/', views.user_profile_view, name='user_profile'),
]
