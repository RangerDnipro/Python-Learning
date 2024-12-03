"""
Модуль для реалізації сигналів
"""

from datetime import timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Ad, UserProfile


@receiver(post_save, sender=Ad)
def check_ad_status(sender, instance, **kwargs):
    if instance.is_active and instance.created_at < timezone.now() - timedelta(days=30):
        instance.is_active = False
        instance.save(update_fields=['is_active'])


@receiver(post_save, sender=Ad)
def send_notification_email(sender, instance, created, **kwargs) -> None:
    """
    Сигнал для надсилання електронного листа при створенні нового оголошення
    :param sender: Модель, що надсилає сигнал
    :param instance: Екземпляр моделі
    :param created: Булеве значення, чи був екземпляр створений
    """
    if created:
        send_mail(
            'Нове оголошення на вашій дошці',
            f'Ваше оголошення "{instance.title}" було успішно створено.',
            'from@example.com',
            [instance.user.email],
            fail_silently=False,
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
