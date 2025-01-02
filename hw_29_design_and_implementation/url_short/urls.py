from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shortener.urls')),
    path('qr/', include('qr_generator.urls')),
    path('statistics/', include('statistics_app.urls')),
]
