"""
Модуль з представленнями
"""

from datetime import timedelta
from urllib.parse import quote, unquote

from celery.result import AsyncResult
from django.db.models import Avg, Count
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.decorators.cache import cache_page
from pymongo import MongoClient

from .forms import UserForm
from .models import Author, Book
from .raw_sql_queries import get_authors_with_many_reviews, get_total_books
from .tasks import import_books_from_csv


def index(request):
    """
    Головна сторінка для введення імені та віку користувача.
    Зберігає ім'я в cookies, а вік у сесії.
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            # Зберігаємо дані
            response = redirect('greeting')
            response.set_cookie('name', quote(name))  # Зберігаємо ім'я у cookies
            request.session['age'] = age  # Зберігаємо вік у сесії
            request.session.set_expiry(300)  # Сесія дійсна 5 хвилин
            return response
    else:
        form = UserForm()

    return render(request, 'session_app/index.html', {'form': form})


def greeting(request):
    """
    Сторінка привітання з використанням даних з cookies та сесії.
    Автоматично подовжує термін дії cookies.
    """
    name = request.COOKIES.get('name')
    age = request.session.get('age')

    if not name or not age:
        return redirect('index')

    # Розкодування cookies
    name = unquote(name)

    # Створюємо відповідь
    response = render(request, 'session_app/greeting.html', {'name': name, 'age': age})

    # Подовжуємо термін дії cookies (наприклад, ще на 5 хвилин)
    expires_at = now() + timedelta(minutes=5)
    response.set_cookie('name', quote(name), expires=expires_at)

    return response


def logout(request):
    """
    Видаляє сесійні дані та cookies.
    """
    response = redirect('index')
    response.delete_cookie('name')  # Видаляємо cookies
    request.session.flush()  # Видаляємо сесійні дані
    return response


def books_without_optimization(request):
    """
    Отримує список книг із авторами та відгуками без оптимізації.
    """
    books_data = []
    for book in Book.objects.all():
        reviews = book.reviews.all()  # Проблема N+1 запитів тут
        books_data.append({
            'title': book.title,
            'author': book.author.name,
            'reviews': [{'text': review.review_text, 'rating': review.rating} for review in reviews]
        })

    return render(request, 'session_app/debug_books_no_opt.html', {'books_data': books_data})


@cache_page(60 * 5)  # Кешування на 5 хвилин
def books_with_optimization(request):
    """
    Отримує список книг із авторами та відгуками з оптимізацією.
    """
    books = Book.objects.select_related('author').prefetch_related('reviews')

    books_data = [
        {
            'title': book.title,
            'author': book.author.name,
            'reviews': [{'text': review.review_text, 'rating': review.rating} for review in book.reviews.all()]
        }
        for book in books
    ]

    return render(request, 'session_app/debug_books.html', {'books_data': books_data})


def books_list(request):
    """
    Відображає список книг із бази SQLite.
    """
    books = Book.objects.select_related('author').prefetch_related('reviews').all()
    return render(request, 'session_app/books_list.html', {'books': books})


def upload_csv(request):
    """
    Завантаження CSV-файлу та запуск завдання імпорту.
    """
    if request.method == 'POST' and request.FILES['file']:
        csv_file = request.FILES['file']
        file_path = f'tmp/{csv_file.name}'
        with open(file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        # Запуск асинхронного завдання
        task = import_books_from_csv.delay(file_path)
        return render(request, 'session_app/upload_status.html', {'task_id': task.id})

    return render(request, 'session_app/upload_csv.html')


def task_status(request, task_id):
    """
    Перегляд статусу завдання.
    """
    task = AsyncResult(task_id)
    return render(request, 'session_app/task_status.html', {'task': task})


def book_stats(request):
    """
    Відображає статистику книг з можливістю сортування.
    """
    # Отримуємо параметри сортування з запиту
    sort_field = request.GET.get('sort', 'review_count')  # За замовчуванням сортуємо за кількістю відгуків
    sort_direction = request.GET.get('direction', 'desc')  # За замовчуванням сортування за спаданням

    # Визначаємо поле для сортування
    if sort_field == 'review_count':
        order_field = 'review_count'
    elif sort_field == 'avg_rating':
        order_field = 'avg_rating'
    else:
        order_field = 'review_count'  # Значення за замовчуванням

    # Визначаємо напрямок сортування
    if sort_direction == 'asc':
        order_by = order_field  # За зростанням
    else:
        order_by = f'-{order_field}'  # За спаданням

    # Анотуємо та сортуємо книги
    books = Book.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).order_by('-review_count', '-avg_rating')

    # Анотуємо авторів
    authors = Author.objects.annotate(avg_rating=Avg('books__reviews__rating'))

    context = {
        'authors': authors,
        'books': books,
        'current_sort_field': sort_field,
        'current_sort_direction': sort_direction,
    }

    return render(request, 'session_app/book_stats.html', context)


def raw_sql_stats(request):
    """
    Відображає статистику за допомогою Raw SQL-запитів.
    """
    authors = get_authors_with_many_reviews(threshold=10)
    total_books = get_total_books()
    return render(request, 'session_app/raw_sql_stats.html', {
        'authors': authors,
        'total_books': total_books,
    })


def mongodb_books(request):
    """
    Відображає список книг із бази даних MongoDB
    """
    # Підключення до MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client['django_books']

    # Отримуємо книги, авторів та відгуки
    books = list(db['books'].find())
    authors = {author['name']: author for author in db['authors'].find()}
    reviews = list(db['reviews'].find())

    # Співставлення авторів та відгуків із книгами
    for book in books:
        # Додаємо інформацію про автора
        author_name = book.get('author')
        book['author_details'] = authors.get(author_name, {})

        # Додаємо інформацію про відгуки
        book['reviews'] = [review for review in reviews if review.get('book') == book.get('title')]

    # Передача даних у шаблон
    return render(request, 'session_app/mongodb_books.html', {'books': books})
