"""
Опис моделей користувача та коментарів
"""

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Кастомний менеджер для моделі користувача
    Дозволяє створювати звичайних користувачів та адміністраторів
    """

    def create_user(self, username: str, email: str = None, password: str = None) -> 'User':
        """
        Створює звичайного користувача з заданими іменем користувача, електронною поштою та паролем
        :param username: Ім'я користувача
        :param email: Адреса електронної пошти (опціонально)
        :param password: Пароль користувача
        :return: Новий користувач
        """
        if not username:
            raise ValueError('Користувач повинен мати ім’я користувача')

        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email)
        user.set_password(password)  # Хешування пароля для безпеки
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, email: str, password: str) -> 'User':
        """
        Створює адміністратора із заданими іменем користувача, електронною поштою та паролем
        :param username: Ім'я користувача
        :param email: Адреса електронної пошти
        :param password: Пароль адміністратора
        :return: Новий адміністратор
        """
        user = self.create_user(username=username, email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Кастомна модель користувача, що замінює стандартну модель Django User
    Містить основні поля для аутентифікації та атрибути для авторизації
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self) -> str:
        """
        Повертає ім'я користувача як рядок
        :return: Ім'я користувача
        """
        return self.username

    def has_perm(self, perm: str, obj=None) -> bool:
        """
        Перевіряє, чи користувач має певний дозвіл
        :param perm: Назва дозволу
        :param obj: Об'єкт, до якого застосовується дозвіл
        :return: True, якщо користувач має дозвіл
        """
        return True

    def has_module_perms(self, app_label: str) -> bool:
        """
        Перевіряє, чи користувач має доступ до додатка
        :param app_label: Назва додатка
        :return: True, якщо користувач має доступ
        """
        return True

    @property
    def is_staff(self) -> bool:
        """
        Властивість, що вказує, чи є користувач співробітником (тобто, чи має доступ до адмін-панелі)
        :return: True, якщо користувач є адміністратором
        """
        return self.is_admin


class Comment(models.Model):
    """
    Модель для збереження коментарів користувачів
    Містить посилання на користувача, текст коментаря та дату створення
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Повертає представлення коментаря у вигляді рядка, що містить ім'я користувача та дату створення
        :return: Рядок у форматі "<ім'я користувача> - <дата створення>"
        """
        return f"{self.user.username} - {self.created_at}"
