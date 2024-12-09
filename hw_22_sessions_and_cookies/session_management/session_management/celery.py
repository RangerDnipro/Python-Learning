"""
Модуль для налаштувань Celery у проєкті
"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Налаштування Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'session_management.settings')

app = Celery('session_management')

# Налаштування Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматичне завантаження завдань із додатків
app.autodiscover_tasks()
