"""
Модуль для налаштування тестового середовища
"""

import pytest
from app import create_app
from app.extensions import db


@pytest.fixture(autouse=True)
def clear_database():
    """
    Очищення бази даних перед кожним тестом.
    """
    db.drop_all()
    db.create_all()


@pytest.fixture
def app():
    """
    Створює тестовий додаток Flask.
    """
    test_app = create_app()
    test_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "testsecretkey"
    })

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Створює клієнт для тестування.
    """
    return app.test_client()
