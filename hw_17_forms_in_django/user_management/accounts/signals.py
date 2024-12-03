"""
Модуль з сигналами для автоматичного створення
та збереження профілю користувача після збереження моделі User
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Створює профіль користувача після створення об'єкта User
    :param sender: Модель, що відправила сигнал (User)
    :param instance: Екземпляр моделі User
    :param created: Булевий прапорець, що вказує, чи об'єкт було створено
    :param kwargs: Додаткові аргументи
    """
    if created:
        UserProfile.objects.create(user=instance)  # pylint: disable=no-member


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Зберігає профіль користувача після збереження об'єкта User
    :param sender: Модель, що відправила сигнал (User)
    :param instance: Екземпляр моделі User
    :param kwargs: Додаткові аргументи
    """
    instance.userprofile.save()
