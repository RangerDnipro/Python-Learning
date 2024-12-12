# Generated by Django 5.1.2 on 2024-12-10 13:23

import custom_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom_app.models.UpperCaseCharField(max_length=100, verbose_name="Ім'я")),
            ],
        ),
    ]