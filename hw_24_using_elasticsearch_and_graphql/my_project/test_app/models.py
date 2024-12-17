"""
Модуль містить моделі для взаємодії з базою даних і ElasticSearch.
"""

from django.db import models
from elasticsearch_dsl import Document, Text, Date, Keyword
from elasticsearch_dsl.connections import connections

# Підключення до ElasticSearch
connections.create_connection(hosts=['http://localhost:9201'])


class DataDocument(models.Model):
    """
    Модель для збереження даних у базі даних.

    Поля:
    - title: Заголовок документа (рядок, максимум 100 символів).
    - description: Опис документа (текст).
    - created_at: Дата та час створення документа (автоматично).
    - author: Автор документа (ForeignKey до Author).
    - category: Категорія документа (ForeignKey до Category).
    - tags: Теги для документа (ManyToManyField до Tag).
    """
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='documents', verbose_name="Автор")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='documents',
                                 verbose_name="Категорія")
    tags = models.ManyToManyField('Tag', blank=True, related_name="documents", verbose_name="Теги")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документи"

    def __str__(self) -> str:
        return self.title


class DataDocumentIndex(Document):
    """
    Індекс ElasticSearch для DataDocument.

    Поля:
    - title: Заголовок документа.
    - description: Опис документа.
    - created_at: Дата та час створення документа.
    - author: Ім'я автора документа.
    - category: Назва категорії документа.
    - tags: Теги документа.
    """
    title = Text()
    description = Text()
    created_at = Date()
    author = Keyword()  # Поле для зберігання імені автора
    category = Keyword()  # Поле для зберігання назви категорії
    tags = Keyword(multi=True)  # Поле для зберігання списку тегів

    class Index:
        name = 'data_index'

    def save(self, **kwargs) -> None:
        """
        Зберігає об'єкт у індексі ElasticSearch.

        :param kwargs: Додаткові аргументи.
        """
        return super().save(**kwargs)


class Author(models.Model):
    """
    Модель для авторів документів.

    Поля:
    - name: Ім'я автора.
    - email: Електронна пошта автора.
    """
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    email = models.EmailField(verbose_name="Електронна пошта", unique=True)

    def __str__(self) -> str:
        """
        Повертає рядкове представлення автора.

        :return: Ім'я автора.
        """
        return self.name


class Category(models.Model):
    """
    Модель для категорій документів.

    Поля:
    - name: Назва категорії.
    """
    name = models.CharField(max_length=50, verbose_name="Категорія")

    def __str__(self) -> str:
        """
        Повертає рядкове представлення категорії.

        :return: Назва категорії.
        """
        return self.name


class Tag(models.Model):
    """
    Модель для тегів.

    Поля:
    - name: Назва тегу.
    """
    name = models.CharField(max_length=30, verbose_name="Тег")

    def __str__(self) -> str:
        """
        Повертає рядкове представлення тегу.

        :return: Назва тегу.
        """
        return self.name


# Індекс для моделі Author
class AuthorIndex(Document):
    name = Text()
    email = Text()

    class Index:
        name = 'author_index'

    def save(self, **kwargs) -> None:
        return super().save(**kwargs)


# Індекс для моделі Category
class CategoryIndex(Document):
    name = Text()

    class Index:
        name = 'category_index'

    def save(self, **kwargs) -> None:
        return super().save(**kwargs)


# Індекс для моделі Tag
class TagIndex(Document):
    name = Text()

    class Index:
        name = 'tag_index'

    def save(self, **kwargs) -> None:
        return super().save(**kwargs)
