"""
Модуль для конфігурації додатка.

Цей модуль містить клас `Config`, який використовується для налаштування
параметрів Flask-додатка, зокрема налаштувань для бази даних і секретного ключа.
"""
import os


class Config:
    """
    Клас конфігурації для Flask-додатка.

    Поля:
    - SECRET_KEY: Секретний ключ додатка, зчитується з середовищних змінних.
    - SQLALCHEMY_DATABASE_URI: Шлях до бази даних SQLite.
    - SQLALCHEMY_TRACK_MODIFICATIONS: Вмикає або вимикає відстеження змін в об'єктах SQLAlchemy.

    Використання:
        Цей клас передається в метод `app.config.from_object` для налаштування додатка.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', "supersecretkey")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///film_library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
