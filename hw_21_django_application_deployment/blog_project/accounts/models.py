"""
Файл models.py для додатку accounts.

Містить модель `Profile`, яка розширює стандартну модель користувача Django (`User`),
та сигнал для автоматичного створення або оновлення профілю користувача.
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Модель для зберігання додаткової інформації про користувача.

    Поля:
        user (OneToOneField): Зв'язок один до одного з моделлю `User`.
        bio (TextField): Біографія користувача (необов'язкове поле).
        avatar (ImageField): Аватар користувача, який завантажується в директорію `avatars/` (необов'язкове поле).
        phone (CharField): Номер телефону користувача, обмежений 15 символами (необов'язкове поле).

    Методи:
        __str__: Повертає рядок із назвою профілю користувача.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        """
        Повертає читабельне представлення моделі.
        """
        return f"Профіль користувача {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Сигнал для автоматичного створення або оновлення профілю користувача.

    Параметри:
        sender: Модель, яка відправила сигнал (`User`).
        instance: Екземпляр моделі `User`, для якого викликається сигнал.
        created (bool): Флаг, що вказує, чи був створений новий користувач.
        kwargs: Додаткові аргументи.

    Дії:
        - Якщо користувач створений, створюється новий профіль.
        - Якщо користувач існує, його профіль оновлюється.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
