"""
Модуль з маршрутами проєкту
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('greeting/', views.greeting, name='greeting'),
    path('logout/', views.logout, name='logout'),
    path('books_no_opt/', views.books_without_optimization, name='books_no_opt'),
    path('books_opt/', views.books_with_optimization, name='books_opt'),
    path('books_list/', views.books_list, name='books_list'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('task_status/<str:task_id>/', views.task_status, name='task_status'),
    path('book_stats/', views.book_stats, name='book_stats'),
    path('raw_sql_stats/', views.raw_sql_stats, name='raw_sql_stats'),
    path('mongodb_books/', views.mongodb_books, name='mongodb_books'),
]
