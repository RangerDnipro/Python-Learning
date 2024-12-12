"""
Маршрути додатка
"""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import CustomModelListCreateAPIView, edit_profile, profile_view, filter_by_color, aggregate_texts_by_color

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form_view, name='form_view'),
    path('login/', auth_views.LoginView.as_view(template_name='custom_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('api/custom-models/', CustomModelListCreateAPIView.as_view(), name='custom_model_api'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/', profile_view, name='profile'),
    path('filter-by-color/', filter_by_color, name='filter_by_color'),
    path('aggregate-by-color/', aggregate_texts_by_color, name='aggregate_by_color'),
]
