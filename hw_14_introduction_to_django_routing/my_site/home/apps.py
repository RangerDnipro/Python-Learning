"""
Модуль містить конфігурацію додатку, зокрема його ім’я
"""

from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
