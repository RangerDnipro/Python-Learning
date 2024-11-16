"""
Модуль з класами адміністративного інтерфейсу
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


# Реєстрація моделі UserProfile в адмінпанелі
class UserProfileInline(admin.StackedInline):
    """
    Додає поля профілю користувача у адмінпанель
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'
    fk_name = 'user'


# Кастомізація адміністративного інтерфейсу для User
class CustomUserAdmin(BaseUserAdmin):
    """
    Налаштовує адміністративну панель для моделі User
    """
    inlines = (UserProfileInline,)
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_active', 'is_staff', 'get_location', 'get_birth_date')
    list_filter = ('is_active', 'is_staff', 'date_joined')

    def get_location(self, instance):
        """
        Отримує місце проживання користувача з профілю
        :param instance: Екземпляр користувача
        :return: Місце проживання користувача
        """
        return instance.userprofile.location

    get_location.short_description = 'Місце проживання'

    def get_birth_date(self, instance):
        """
        Отримує дату народження користувача з профілю
        :param instance: Екземпляр користувача
        :return: Дата народження користувача
        """
        return instance.userprofile.birth_date

    get_birth_date.short_description = 'Дата народження'


# Реєстрація User зі змінами
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Реєстрація UserProfile окремо
admin.site.register(UserProfile)
