"""
Модуль з моделями додатка
"""

import re

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class UpperCaseCharField(models.CharField):
    """
    Кастомне поле моделі, яке автоматично переводить текст у верхній регістр.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Переводить значення у верхній регістр перед збереженням у базу даних.
        :param model_instance: Екземпляр моделі
        :param add: Чи є це новим записом
        :return: Модифіковане значення у верхньому регістрі
        """
        value = getattr(model_instance, self.attname, None)
        if isinstance(value, str):
            value = value.upper()
            setattr(model_instance, self.attname, value)
        return value


class PhoneNumberField(models.CharField):
    """
    Кастомне поле для перевірки та зберігання телефонних номерів.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15  # Максимальна довжина номера
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        """
        Перевірка правильності формату телефонного номера.
        """
        super().validate(value, model_instance)
        phone_regex = r'^\+?1?\d{9,15}$'  # Формат: +123456789 або 123456789
        if not re.match(phone_regex, value):
            raise ValidationError(f"{value} не є коректним номером телефону.")


class CustomModel(models.Model):
    """
    Модель для тестування кастомного поля UpperCaseCharField.
    """
    name = UpperCaseCharField(max_length=100, verbose_name="Текст")
    description = models.TextField(verbose_name="Опис", blank=True, null=True)
    hex_color = models.CharField(max_length=7, verbose_name="HEX-код кольору", blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name="Телефонний номер", blank=True, null=True)
    created_at = models.DateTimeField(default=now)

    def word_count(self) -> int:
        """
        Підраховує кількість слів у полі name.
        :return: Кількість слів
        """
        return len(self.name.split())

    def __str__(self):
        return self.name


class RelatedModel(models.Model):
    """
    Пов'язана модель для демонстрації вкладених полів.
    """
    custom_model = models.ForeignKey(CustomModel, related_name='related_objects', on_delete=models.CASCADE)
    related_field = models.CharField(max_length=100, verbose_name="Пов'язане поле")

    def __str__(self):
        return self.related_field


@receiver(post_save, sender=CustomModel)
def create_related_object(sender, instance, created, **kwargs):
    """
    Автоматично створює пов'язаний об'єкт після збереження CustomModel.
    """
    if created:
        RelatedModel.objects.create(
            custom_model=instance,
            related_field=f"Автоматично створено для {instance.name}"
        )


class Profile(models.Model):
    """
    Модель профілю користувача з додатковими полями.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, verbose_name="Телефонний номер", blank=True, null=True)

    def __str__(self):
        return f"Профіль {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Автоматично створює або оновлює профіль користувача при збереженні User.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
