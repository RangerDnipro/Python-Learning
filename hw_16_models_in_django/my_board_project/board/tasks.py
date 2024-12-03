"""
Реалізація автоматичної деактивації оголошення через 30 днів
"""

from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from .models import Ad


@shared_task
def deactivate_expired_ads():
    threshold_date = timezone.now() - timedelta(days=30)
    expired_ads = Ad.objects.filter(created_at__lt=threshold_date, is_active=True)
    for ad in expired_ads:
        ad.is_active = False
        ad.save()
