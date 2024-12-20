"""
URL configuration for student_course_api project.

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
from django.contrib.auth.views import LoginView
from django.urls import path
from ninja import NinjaAPI

from management.api import router as management_router, user_router
from management.views import logout_view, home_redirect_view

# Створення основного API
api = NinjaAPI(
    title="Student Course Management API",
    version="1.0",
    urls_namespace="api-1.0",
    description="API для управління студентами, курсами та результатами іспитів"
)

# Додаємо маршрути Management
api.add_router("/management/", management_router, tags=["Management"])

# Додаємо маршрути Users
api.add_router("/users/", user_router, tags=["Users"])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls, name="api-root"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("", home_redirect_view, name="home"),
]
