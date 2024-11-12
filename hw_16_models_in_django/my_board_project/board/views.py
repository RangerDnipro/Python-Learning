"""
Модуль для створення представлень (views) додатку. Представлення обробляють HTTP-запити
та повертають HTTP-відповіді (наприклад, шаблони чи текст)
"""

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from .forms import UserRegistrationForm, CommentForm, UserProfileForm
from .models import Ad, Category, UserProfile


def home(request):
    """
    Відображення головної сторінки
    """
    return render(request, 'board/home.html')


def active_ads_by_category_view(request, category_name):
    """
    Відображення активних оголошень у певній категорії.
    """
    try:
        category = Category.objects.get(name=category_name)
        active_ads = Ad.objects.filter(category=category, is_active=True)
    except Category.DoesNotExist:
        active_ads = []
        category = category_name
    return render(request, 'board/active_ads.html', {'active_ads': active_ads, 'category': category})


def signup(request):
    """
    View для реєстрації нового користувача
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Створення профілю користувача
            UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )
            # Авторизуємо користувача після реєстрації
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'board/signup.html', {'form': form})


@login_required
def edit_profile(request):
    """
    Використовується для редагування профіля користувача
    :param request:
    :return:
    """
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'board/edit_profile.html', {'form': form})


class CreateAdView(CreateView):
    """
    Використовується для створення оголошень
    """
    model = Ad
    template_name = 'board/ad_form.html'
    fields = ['title', 'description', 'price', 'category']
    success_url = reverse_lazy('home')
    # Перенаправляє на сторінку входу, якщо користувач не авторизований
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        Перевірка форми перед збереженням
        Додаємо поточного користувача як автора оголошення
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class MyAdsView(ListView):
    """
    Використовується для перегляду оголошень певного користувача
    """
    model = Ad
    template_name = 'board/my_ads.html'
    context_object_name = 'ads'

    def get_queryset(self):
        """
        Повертає оголошення, створені поточним користувачем
        """
        return Ad.objects.filter(user=self.request.user)


class EditAdView(UpdateView):
    """
    Використовується для редагування оголошення поточним користувачем
    """
    model = Ad
    template_name = 'board/ad_form.html'
    fields = ['title', 'description', 'price', 'category']
    success_url = reverse_lazy('my_ads')

    def get_queryset(self):
        """
        Дозволяє редагувати тільки власні оголошення.
        """
        return Ad.objects.filter(user=self.request.user)


class RecentAdsView(ListView):
    """
    Відображення всіх оголошень з можливістю фільтрації за різними критеріями:
    - Ціна (min_price, max_price)
    - Дата створення (start_date, end_date)
    - Активність (is_active)
    - Кількість коментарів (min_comments)
    """
    model = Ad
    template_name = 'board/home.html'
    context_object_name = 'ads'

    def get_queryset(self):
        # Отримуємо всі оголошення з підрахунком коментарів
        queryset = Ad.objects.annotate(comments_count=Count('comments'))

        # Пошук за заголовком
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        # Фільтрація за категорією
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        # Фільтрація за користувачем
        user_id = self.request.GET.get('user')
        if user_id:
            queryset = queryset.filter(user__id=user_id)

        # Фільтрація за активністю
        is_active = self.request.GET.get('is_active')
        if is_active:
            queryset = queryset.filter(is_active=(is_active.lower() == 'true'))

        # Фільтрація за ціною
        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Фільтрація за датою створення
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        # Фільтрація за кількістю коментарів
        min_comments = self.request.GET.get('min_comments')
        if min_comments:
            queryset = queryset.filter(comments_count__gte=min_comments)

        # Сортування
        sort_by = self.request.GET.get('sort', 'created_at')
        if sort_by in ['title', 'price', 'created_at', 'comments_count']:
            queryset = queryset.order_by(sort_by)

        # Повертаємо відфільтрований запит
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AdDetailView(DetailView):
    """
    Відображає детальну інформацію про оголошення
    """
    model = Ad
    template_name = 'board/ad_form.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Додаємо змінну для шаблону, щоб він знав, що це режим тільки для перегляду
        context['readonly'] = True
        # Отримання всіх коментарів до оголошення
        context['comments'] = self.object.comments.all().order_by('-created_at')
        # Форма для додавання коментаря
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Перенаправлення на сторінку входу, якщо користувач неавторизований
            return redirect('login')

        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ad = self.object
            comment.user = request.user
            comment.save()
            return redirect('ad_detail', pk=self.object.pk)

        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)
