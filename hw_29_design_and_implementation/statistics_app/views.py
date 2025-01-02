"""
Модуль з представленням
"""

from django.shortcuts import render
from django.db.models import Count, Sum
from django.utils.timezone import now, timedelta
from shortener.models import URLClick


def detailed_statistics(request):
    """
    Відображає детальну статистику для авторизованого користувача.
    """
    # Статистика за типами пристроїв
    device_stats = (
        URLClick.objects.filter(url__created_by=request.user)
        .values('device_type')
        .annotate(count=Count('device_type'))
    )
    total_device_clicks = sum(stat['count'] for stat in device_stats)
    for stat in device_stats:
        stat['percentage'] = round((stat['count'] / total_device_clicks) * 100, 2)

    # Статистика за країнами
    country_stats = (
        URLClick.objects.filter(url__created_by=request.user)
        .values('country')
        .annotate(count=Count('country'))
    )
    total_country_clicks = sum(stat['count'] for stat in country_stats)
    for stat in country_stats:
        stat['percentage'] = round((stat['count'] / total_country_clicks) * 100, 2)

    # Поточний час
    current_time = now()
    last_hour = current_time - timedelta(hours=1)
    hourly_clicks = URLClick.objects.filter(
        url__created_by=request.user, clicked_at__gte=last_hour
    ).count()

    last_day = current_time - timedelta(days=1)
    daily_clicks = URLClick.objects.filter(
        url__created_by=request.user, clicked_at__gte=last_day
    ).count()

    last_month = current_time - timedelta(days=30)
    monthly_clicks = URLClick.objects.filter(
        url__created_by=request.user, clicked_at__gte=last_month
    ).count()

    total_time_clicks = hourly_clicks + daily_clicks + monthly_clicks
    time_stats = [
        {'period': 'Last Hour', 'count': hourly_clicks,
         'percentage': round((hourly_clicks / total_time_clicks) * 100, 2) if total_time_clicks > 0 else 0},
        {'period': 'Last Day', 'count': daily_clicks,
         'percentage': round((daily_clicks / total_time_clicks) * 100, 2) if total_time_clicks > 0 else 0},
        {'period': 'Last Month', 'count': monthly_clicks,
         'percentage': round((monthly_clicks / total_time_clicks) * 100, 2) if total_time_clicks > 0 else 0},
    ]

    context = {
        'device_stats': device_stats,
        'country_stats': country_stats,
        'time_stats': time_stats,
    }
    return render(request, 'statistics_app/detailed_statistics.html', context)
