Ви розробляєте REST API для управління бібліотекою книг. Ваше API повинно включати такі можливості:

## 1. CRUD операції для книг:

- Додавання нової книги.
- Отримання списку всіх книг (з можливістю фільтрації).
- Перегляд деталей окремої книги.
- Оновлення інформації про книгу.
- Видалення книги.

## 2. Фільтрація і пошук:

- Фільтрація книг за автором, жанром або роком видання.
- Пошук книг за частиною назви.

## 3. Пагінація:

Розділіть результати на сторінки по 10 елементів.

## 4. Авторизація і аутентифікація:

- Використовуйте аутентифікацію за допомогою токенів (TokenAuthentication або JWT).
- Надайте доступ до CRUD операцій лише автентифікованим користувачам.

## 5. Адміністраторський доступ:

Тільки адміністратор може видаляти книги.

## 6. Документація API:

Використайте Swagger або ReDoc для автоматичної генерації документації.

# Технічні вимоги:

## 1. Модель Book:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

## 2. Серилізатори (Serializers):

Створіть серіалізатор для моделі Book.

## 3. Views:

Використайте Generic Views або ViewSets.

## 4. Роутинг:

Використайте DRF Routers для автоматичної генерації URL-адрес.

## 5. Фільтрація:

Використайте бібліотеку django-filter для фільтрації та пошуку.

## 6. Тестування:

Напишіть тести для перевірки основних функцій API.

# Результат виконання:

1. Функціонуюче API з усіма перерахованими можливостями.
2. Документація API, доступна за URL /docs/.
3. Мінімум 5 тестів для перевірки коректної роботи API.
4. Код повинен відповідати принципам DRY і бути організованим у стилі REST.

# Додаткове завдання (за бажанням):

1. Реалізуйте сортування книг за роком видання або назвою.
2. Додайте поле user до моделі Book для збереження інформації про те, хто створив запис (ForeignKey на User).
3. Реалізуйте реєстрацію і вхід користувачів через API.
