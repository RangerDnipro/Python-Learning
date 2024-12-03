"""
Файл urls.py для додатку blog.

Містить маршрути для відображення списку дописів, деталей допису,
а також для створення нового допису.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
]
