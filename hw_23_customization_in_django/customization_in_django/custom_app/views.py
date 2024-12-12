"""
Модуль з представленнями додатка
"""

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CustomForm, ProfileForm
from .models import CustomModel, Profile
from .permissions import IsAdminOrReadOnly
from .serializers import CustomModelSerializer


def index(request):
    """
    Головна сторінка додатка.
    :param request: HTTP-запит
    :return: HTTP-відповідь із текстом
    """
    return render(request, 'custom_app/index.html')


def form_view(request):
    """
    Відображає кастомну форму та зберігає введені дані.
    :param request: HTTP-запит
    :return: HTTP-відповідь
    """
    if request.method == 'POST':
        form = CustomForm(request.POST)
        if form.is_valid():
            # Зберігаємо текст та телефон
            CustomModel.objects.create(
                name=form.cleaned_data['name'],
                description="Користувацький ввід",
                hex_color=form.cleaned_data['hex_color'],
            )
            return redirect('form_view')
    else:
        form = CustomForm()

    # Отримуємо всі попередні тексти
    texts = CustomModel.objects.all()

    return render(request, 'custom_app/form.html', {'form': form, 'texts': texts})


def signup(request):
    """
    Реєстрація нового користувача.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Зберігаємо користувача
            user = form.save()

            # Аутентифікуємо користувача
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            # Логінимо користувача
            if user is not None:
                login(request, user)

            # Переходимо на головну сторінку або іншу сторінку
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'custom_app/signup.html', {'form': form})


class CustomModelListCreateAPIView(APIView):
    """
    API для отримання та створення записів CustomModel.
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        """
        Отримання всіх записів із фільтрацією за параметром 'name'.
        """
        name_filter = request.query_params.get('name', None)
        if name_filter:
            objects = CustomModel.objects.filter(name__icontains=name_filter)
        else:
            objects = CustomModel.objects.all()

        serializer = CustomModelSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Створення нового запису.
        """
        serializer = CustomModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@login_required
def edit_profile(request):
    """
    Відображає форму редагування профілю користувача.
    """
    # Створення профілю, якщо він не існує
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль успішно оновлено!")  # Додано повідомлення
            return redirect('profile')  # Перенаправлення на сторінку профілю
        else:
            messages.error(request, "Виправте помилки у формі.")  # Повідомлення про помилку
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'custom_app/edit_profile.html', {'form': form})


@login_required
def profile_view(request):
    """
    Відображення профілю користувача.
    """
    profile = request.user.profile
    return render(request, 'custom_app/profile.html', {'profile': profile})


def filter_by_color(request):
    """
    Відображає тексти з фільтром за HEX-кольором.
    """
    hex_color = request.GET.get('hex_color', '#FFFFFF')  # За замовчуванням білий
    texts = CustomModel.objects.filter(hex_color=hex_color)

    return render(request, 'custom_app/filter_by_color.html', {'texts': texts, 'hex_color': hex_color})


def aggregate_texts_by_color(request):
    """
    Агрегація текстів за HEX-кольором.
    """
    color_stats = CustomModel.objects.values('hex_color').annotate(total=Count('hex_color')).order_by('-total')

    return render(request, 'custom_app/aggregate_by_color.html', {'color_stats': color_stats})
