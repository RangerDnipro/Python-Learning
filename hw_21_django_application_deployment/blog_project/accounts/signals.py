"""
Файл signals.py для додатку accounts.

Містить сигнали для автоматичного створення та збереження профілю
користувача при створенні або оновленні екземпляра моделі User.
"""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Сигнал для створення профілю при створенні нового користувача.

    Викликається після збереження екземпляра моделі User, якщо він новий.

    Параметри:
        sender: Модель, яка відправила сигнал (User).
        instance: Екземпляр моделі User.
        created (bool): Флаг, чи був створений новий екземпляр.
        kwargs: Додаткові аргументи.

    Дія:
        - Створюється новий об'єкт Profile, пов'язаний із користувачем.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Сигнал для збереження профілю при оновленні користувача.

    Викликається після збереження екземпляра моделі User.

    Параметри:
        sender: Модель, яка відправила сигнал (User).
        instance: Екземпляр моделі User.
        kwargs: Додаткові аргументи.

    Дія:
        - Зберігається об'єкт Profile, пов'язаний із користувачем.
    """
    instance.profile.save()
