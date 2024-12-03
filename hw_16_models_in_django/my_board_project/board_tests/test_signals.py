"""
Тестування сигналів
"""

import os
import sys
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from ..models import Ad, Category

# Додаємо кореневу папку проєкту до Python-шляху
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class AdSignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='signaluser')
        self.category = Category.objects.create(name='Меблі')

    def test_auto_deactivation_signal(self):
        """Тест сигналу автоматичної деактивації оголошення після 30 днів"""
        ad = Ad.objects.create(
            title='Продам стіл',
            description='Дерев’яний, як новий',
            price=300,
            created_at=timezone.now() - timedelta(days=31),
            is_active=True,
            user=self.user,
            category=self.category
        )
        # Перевіряємо, що оголошення автоматично деактивувалося
        ad.refresh_from_db()
        self.assertEqual(ad.is_active, False)
