"""
Тестування моделей та методів
"""

import os
import sys

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from ..models import Category, Ad, Comment

# Додаємо кореневу папку проєкту до Python-шляху
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCategoryModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Електроніка', description='Все для електроніки')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Електроніка')


class TestAdModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.category = Category.objects.create(name='Автомобілі')
        self.ad = Ad.objects.create(
            title='Продам авто',
            description='Чудовий стан',
            price=20000,
            created_at=timezone.now(),
            is_active=True,
            user=self.user,
            category=self.category
        )

    def test_ad_creation(self):
        self.assertEqual(self.ad.title, 'Продам авто')


class TestCommentModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='commentuser')
        self.ad = Ad.objects.create(
            title='Здам квартиру',
            description='Центр міста',
            price=500,
            user=self.user
        )
        self.comment = Comment.objects.create(
            content='Чудова пропозиція',
            ad=self.ad,
            user=self.user
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'Чудова пропозиція')
