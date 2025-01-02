"""
Модуль адміністрування
"""

from django.contrib import admin

from .models import URL, URLClick

admin.site.register(URL)
admin.site.register(URLClick)
