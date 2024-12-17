"""
Модуль визначає GraphQL-схему для взаємодії з моделями додатка, включаючи операції створення,
отримання та видалення даних через GraphQL API.
"""

import graphene
from django.db.models import Count
from graphene_django.types import DjangoObjectType
from elasticsearch_dsl import Q
from elasticsearch.exceptions import NotFoundError

from .models import DataDocument, DataDocumentIndex, Author, Category, Tag


class DataDocumentType(DjangoObjectType):
    """
    Визначає тип GraphQL для моделі DataDocument.
    """

    class Meta:
        model = DataDocument


class AuthorType(DjangoObjectType):
    """
    Визначає тип GraphQL для моделі Author.
    """

    class Meta:
        model = Author


class CategoryType(DjangoObjectType):
    """
    Визначає тип GraphQL для моделі Category.
    """

    class Meta:
        model = Category


class TagType(DjangoObjectType):
    """
    Визначає тип GraphQL для моделі Tag.
    """

    class Meta:
        model = Tag


class AggregationType(graphene.ObjectType):
    name = graphene.String(description="Назва групи")
    count = graphene.Int(description="Кількість документів")


class CreateDataDocument(graphene.Mutation):
    """
    Мутація для створення нового об'єкта DataDocument.
    """

    class Arguments:
        title = graphene.String(required=True, description="Заголовок документа")
        description = graphene.String(required=True, description="Опис документа")

    data_document = graphene.Field(DataDocumentType, description="Створений документ")

    def mutate(self, info, title: str, description: str):
        """
        Виконує створення нового документа в базі даних.
        """
        data_document = DataDocument.objects.create(title=title, description=description)
        return CreateDataDocument(data_document=data_document)


class CreateAuthor(graphene.Mutation):
    """
    Мутація для створення нового автора.
    """

    class Arguments:
        name = graphene.String(required=True, description="Ім'я автора")
        email = graphene.String(required=True, description="Електронна пошта автора")

    author = graphene.Field(AuthorType, description="Створений автор")

    def mutate(self, info, name: str, email: str):
        author = Author.objects.create(name=name, email=email)
        return CreateAuthor(author=author)


class CreateCategory(graphene.Mutation):
    """
    Мутація для створення нової категорії.
    """

    class Arguments:
        name = graphene.String(required=True, description="Назва категорії")

    category = graphene.Field(CategoryType, description="Створена категорія")

    def mutate(self, info, name: str):
        category = Category.objects.create(name=name)
        return CreateCategory(category=category)


class CreateTag(graphene.Mutation):
    """
    Мутація для створення нового тегу.
    """

    class Arguments:
        name = graphene.String(required=True, description="Назва тегу")

    tag = graphene.Field(TagType, description="Створений тег")

    def mutate(self, info, name: str):
        tag = Tag.objects.create(name=name)
        return CreateTag(tag=tag)


class DeleteDataDocument(graphene.Mutation):
    """
    Мутація для видалення об'єкта DataDocument з бази даних та індексу ElasticSearch.
    """

    class Arguments:
        id = graphene.ID(required=True, description="ID документа, який потрібно видалити")

    success = graphene.Boolean(description="Чи був документ успішно видалений")

    def mutate(self, info, id: int):
        """
        Видаляє документ з бази даних Django та індексу ElasticSearch.

        :param info: Контекст виконання мутації.
        :param id: ID документа для видалення.
        :return: Екземпляр DeleteDataDocument з результатом виконання.
        """
        from .models import DataDocument, DataDocumentIndex

        # Крок 1: Видалення з бази даних Django
        try:
            data_document = DataDocument.objects.get(pk=id)
            data_document.delete()
        except DataDocument.DoesNotExist:
            return DeleteDataDocument(success=False)

        # Крок 2: Видалення з індексу ElasticSearch
        try:
            # Використовуємо метод `get` для видалення з ElasticSearch
            doc = DataDocumentIndex.get(id=id)
            doc.delete()
        except NotFoundError:
            pass  # Ігноруємо помилку, якщо документ вже відсутній у індексі

        return DeleteDataDocument(success=True)


class Query(graphene.ObjectType):
    """
    Визначає запити для отримання та аналітики даних.
    """
    # Існуючі запити
    all_data_documents = graphene.List(DataDocumentType, description="Отримати список всіх документів")
    all_authors = graphene.List(AuthorType, description="Отримати список всіх авторів")
    all_categories = graphene.List(CategoryType, description="Отримати список всіх категорій")
    all_tags = graphene.List(TagType, description="Отримати список всіх тегів")

    # Нові аналітичні запити
    document_count_by_author = graphene.List(graphene.String, description="Отримати кількість документів за авторами")
    document_count_by_category = graphene.List(graphene.String,
                                               description="Отримати кількість документів за категоріями")
    document_count_by_tag = graphene.List(graphene.String, description="Отримати кількість документів за тегами")

    documents_by_authors = graphene.List(AggregationType, description="Групування документів за авторами")
    documents_by_categories = graphene.List(AggregationType, description="Групування документів за категоріями")
    documents_by_tags = graphene.List(AggregationType, description="Групування документів за тегами")

    def resolve_documents_by_authors(self, info):
        """
        Групує документи за авторами.
        """
        return [
            {"name": author['author__name'], "count": author['count']}
            for author in DataDocument.objects.values('author__name').annotate(count=Count('id'))
        ]

    def resolve_documents_by_categories(self, info):
        """
        Групує документи за категоріями.
        """
        return [
            {"name": category['category__name'], "count": category['count']}
            for category in DataDocument.objects.values('category__name').annotate(count=Count('id'))
        ]

    def resolve_documents_by_tags(self, info):
        """
        Групує документи за тегами.
        """
        return [
            {"name": tag['tags__name'], "count": tag['count']}
            for tag in DataDocument.objects.values('tags__name').annotate(count=Count('id'))
        ]

    def resolve_all_data_documents(self, info):
        """
        Повертає всі об'єкти DataDocument.
        """
        return DataDocument.objects.all()

    def resolve_all_authors(self, info):
        """
        Повертає всі об'єкти Author.
        """
        return Author.objects.all()

    def resolve_all_categories(self, info):
        """
        Повертає всі об'єкти Category.
        """
        return Category.objects.all()

    def resolve_all_tags(self, info):
        """
        Повертає всі об'єкти Tag.
        """
        return Tag.objects.all()

    # Методи для аналітичних запитів
    def resolve_document_count_by_author(self, info):
        """
        Підраховує кількість документів для кожного автора.
        """
        results = DataDocument.objects.values('author__name').annotate(total=Count('id'))
        return [f"{result['author__name']}: {result['total']} документів" for result in results]

    def resolve_document_count_by_category(self, info):
        """
        Підраховує кількість документів для кожної категорії.
        """
        results = DataDocument.objects.values('category__name').annotate(total=Count('id'))
        return [f"{result['category__name']}: {result['total']} документів" for result in results]

    def resolve_document_count_by_tag(self, info):
        """
        Підраховує кількість документів для кожного тегу.
        """
        results = DataDocument.objects.values('tags__name').annotate(total=Count('id'))
        return [f"{result['tags__name']}: {result['total']} документів" for result in results]

    search_documents = graphene.List(
        DataDocumentType,
        search=graphene.String(required=True, description="Ключові слова для пошуку"),
        description="Пошук документів у ElasticSearch за ключовими словами"
    )

    def resolve_search_documents(self, info, search):
        """
        Пошук документів у ElasticSearch за ключовими словами в title та description.
        """
        query = Q("multi_match", query=search, fields=["title", "description"])
        search_result = DataDocumentIndex.search().query(query).execute()
        return [
            DataDocument(
                id=hit.meta.id,
                title=hit.title,
                description=hit.description,
                created_at=hit.created_at
            )
            for hit in search_result
        ]


class Mutation(graphene.ObjectType):
    """
    Визначає мутації для роботи з даними.
    """
    create_data_document = CreateDataDocument.Field(description="Створити новий документ")
    delete_data_document = DeleteDataDocument.Field(description="Видалити документ")
    create_author = CreateAuthor.Field(description="Створити нового автора")
    create_category = CreateCategory.Field(description="Створити нову категорію")
    create_tag = CreateTag.Field(description="Створити новий тег")


schema = graphene.Schema(query=Query, mutation=Mutation)
