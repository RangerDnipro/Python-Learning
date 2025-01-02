# Generated by Django 5.1.4 on 2025-01-02 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_alter_url_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlclick',
            name='country',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='urlclick',
            name='device_type',
            field=models.CharField(choices=[('PC', 'PC'), ('Mobile', 'Mobile'), ('Tablet', 'Tablet'), ('Unknown', 'Unknown')], default='Unknown', max_length=10),
        ),
    ]