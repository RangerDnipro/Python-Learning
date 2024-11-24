"""
Опис моделей завдань
"""

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Модель завдання
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
