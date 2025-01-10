"""
Модуль для тестів
"""

import pytest
from flask import Flask
from app import create_app


@pytest.fixture
def app() -> Flask:
    """
    Надає тестовий Flask-додаток.
    :return: Тестовий додаток Flask.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app


@pytest.fixture
def client(app: Flask):
    """
    Надає клієнт для тестування додатку.
    :param app: Тестовий додаток Flask.
    :return: Тестовий клієнт.
    """
    return app.test_client()


def test_home_page(client):
    """
    Тестуємо, чи домашня сторінка працює.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Film Library API" in response.data


def test_register_user(client):
    """
    Тестуємо реєстрацію користувача.
    """
    # Видалення існуючого користувача (опціонально)
    client.post("/auth/register", json={
        "username": "testuser",
        "password": "password123"
    })

    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "password123"
    })
    if response.status_code == 400:  # Якщо користувач вже існує
        assert b"already exists" in response.data
    else:
        assert response.status_code == 201
        assert b"User registered successfully" in response.data


def test_add_director(client):
    """
    Тестуємо додавання режисера.
    """
    # Логін для отримання доступу
    client.post("/auth/register", json={
        "username": "testuser",
        "password": "password123"
    })
    client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })

    response = client.post("/add-director", json={
        "name": "Ridley Scott"
    })

    if response.status_code == 409:  # Якщо режисер вже існує
        assert b"already exists" in response.data
    else:
        assert response.status_code == 201
        json_data = response.get_json()
        assert "id" in json_data
        assert json_data["name"] == "Ridley Scott"


def test_add_film(client):
    """
    Тестуємо додавання фільму.
    """
    # Логін для отримання доступу
    client.post("/auth/register", json={
        "username": "testuser",
        "password": "password123"
    })
    client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })

    # Перевірка чи режисер вже існує
    response = client.post("/add-director", json={
        "name": "Ridley Scott"
    })
    director_id = response.get_json()["id"] if response.status_code == 201 else 1

    # Додавання фільму
    response = client.post("/films", json={
        "title": "Alien",
        "description": "A terrifying journey into space.",
        "release_year": 1979,
        "rating": 8.4,
        "director_id": director_id,
        "poster": "/static/images/alien.jpg"
    })

    if response.status_code == 409:  # Якщо фільм вже існує
        assert b"already exists" in response.data
    else:
        assert response.status_code == 201
        json_data = response.get_json()
        assert "id" in json_data
        assert json_data["title"] == "Alien"
