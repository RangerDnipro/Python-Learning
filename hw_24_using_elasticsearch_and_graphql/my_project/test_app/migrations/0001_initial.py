# Generated by Django 5.1.4 on 2024-12-17 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name="Ім'я")),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Електронна пошта')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Категорія')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Тег')),
            ],
        ),
        migrations.CreateModel(
            name='DataDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Опис')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='test_app.author', verbose_name='Автор')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='test_app.category', verbose_name='Категорія')),
                ('tags', models.ManyToManyField(blank=True, related_name='documents', to='test_app.tag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документи',
            },
        ),
    ]
