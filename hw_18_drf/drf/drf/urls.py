"""
URL configuration for drf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from library.views import BookViewSet

# Конфігурація для Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version='v1',
        description="API for managing бібліотекою книг",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@library.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Ініціалізація роутера
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('admin/', admin.site.urls),  # Адміністративна панель
    path('api/drf-auth/', include('rest_framework.urls', namespace='drf-auth')),  # Авторизація для DRF
    path('', lambda request: redirect('/api/books/', permanent=True)),  # Переадресація на список книг
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('api/schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # JSON специфікація
    path('api/', include(router.urls)),  # Додаємо маршрути з роутера
    path('api/auth/', include('djoser.urls')),  # Маршрути для реєстрації, зміни пароля тощо
    path('api/auth/', include('djoser.urls.jwt')),  # Маршрути для отримання та оновлення токенів
]
