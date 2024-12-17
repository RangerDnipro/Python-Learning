"""
Модуль містить сигнали для автоматичної індексації даних у ElasticSearch при
створенні, оновленні або видаленні об'єктів моделі DataDocument.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DataDocument, DataDocumentIndex
from .models import Author, Category, Tag
from .models import AuthorIndex, CategoryIndex, TagIndex


@receiver(post_save, sender=DataDocument)
def index_data_document(sender, instance: DataDocument, **kwargs) -> None:
    """
    Сигнал для автоматичного індексування даних у ElasticSearch після створення або оновлення.

    :param sender: Модель, яка викликала сигнал.
    :param instance: Екземпляр моделі, який збережено.
    """
    # Створюємо або оновлюємо індекс у ElasticSearch
    doc = DataDocumentIndex(
        meta={'id': instance.id},
        title=instance.title,
        description=instance.description,
        created_at=instance.created_at
    )
    doc.save()
    print(f"Документ '{instance.title}' проіндексовано у ElasticSearch.")


@receiver(post_delete, sender=DataDocument)
def delete_indexed_data_document(sender, instance: DataDocument, **kwargs) -> None:
    """
    Сигнал для автоматичного видалення даних з ElasticSearch після видалення об'єкта.

    :param sender: Модель, яка викликала сигнал.
    :param instance: Екземпляр моделі, який видалено.
    """
    # Видаляємо документ з індексу ElasticSearch
    try:
        doc = DataDocumentIndex.get(id=instance.id)
        doc.delete()
        print(f"Документ '{instance.title}' видалено з ElasticSearch.")
    except DataDocumentIndex.DoesNotExist:
        print(f"Документ '{instance.title}' не знайдено в ElasticSearch для видалення.")


# Сигнали для Author
@receiver(post_save, sender=Author)
def index_author(sender, instance, **kwargs):
    AuthorIndex(name=instance.name, email=instance.email).save()


@receiver(post_delete, sender=Author)
def delete_author(sender, instance, **kwargs):
    try:
        AuthorIndex.get(id=instance.id).delete()
    except:
        pass


# Сигнали для Category
@receiver(post_save, sender=Category)
def index_category(sender, instance, **kwargs):
    CategoryIndex(name=instance.name).save()


@receiver(post_delete, sender=Category)
def delete_category(sender, instance, **kwargs):
    try:
        CategoryIndex.get(id=instance.id).delete()
    except:
        pass


# Сигнали для Tag
@receiver(post_save, sender=Tag)
def index_tag(sender, instance, **kwargs):
    TagIndex(name=instance.name).save()


@receiver(post_delete, sender=Tag)
def delete_tag(sender, instance, **kwargs):
    try:
        TagIndex.get(id=instance.id).delete()
    except:
        pass
