"""
Модуль містить серіалізатори
"""

from rest_framework import serializers
from .models import CustomModel, RelatedModel


class RelatedModelSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для RelatedModel.
    """

    class Meta:
        model = RelatedModel
        fields = ['id', 'related_field']


class CustomModelSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для CustomModel з вкладеними полями.
    """
    related_objects = RelatedModelSerializer(many=True, read_only=True)

    class Meta:
        model = CustomModel
        fields = ['id', 'name', 'description', 'created_at', 'related_objects']
