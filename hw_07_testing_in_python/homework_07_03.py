"""
Завдання 3. Використання фікстур у pytest
Напишіть програму для керування користувачами та напишіть тести з використанням фікстур у pytest.
Напишіть клас UserManager, який реалізує такі методи:
add_user(name: str, age: int): додає користувача.
remove_user(name: str): видаляє користувача на ім'я.
get_all_users() -> list: повертає список усіх користувачів.

Для тестів створіть фікстуру, яка попередньо додаватиме кількох користувачів
перед виконанням тестів:
@pytest.fixture
def user_manager():
 um = UserManager()
 um.add_user("Alice", 30)
 um.add_user("Bob", 25)
 return um

Напишіть тести для перевірки методів add_user, remove_user, get_all_users.
Використовуйте фікстуру в кожному тесті для попереднього налаштування.
Створіть тест, який скипатиметься за певних умов (наприклад,
якщо у користувача менше трьох користувачів).
"""

# pylint: disable=redefined-outer-name

from typing import List
import pytest


class UserManager:
    """
    Клас для керування користувачами
    """

    def __init__(self):
        self.users = {}

    def add_user(self, name: str, age: int):
        """
        Додає користувача у систему
        :param name: Ім'я користувача
        :param age: Вік користувача
        """
        self.users[name] = age

    def remove_user(self, name: str):
        """
        Видаляє користувача із системи
        :param name: Ім'я користувача
        """
        if name in self.users:
            del self.users[name]

    def get_all_users(self) -> List[str]:
        """
        Повертає список усіх користувачів
        :return: Список імен користувачів
        """
        return list(self.users.keys())


# Фікстура для підготовки UserManager з кількома користувачами
@pytest.fixture
def user_manager():
    """
    Фікстура для створення екземпляра UserManager з попередньо доданими користувачами
    :return: Екземпляр UserManager
    """
    um = UserManager()
    um.add_user("Alice", 30)
    um.add_user("Bob", 25)
    return um


def test_add_user(user_manager):
    """
    Тест для методу add_user
    :param user_manager: Екземпляр UserManager, підготовлений фікстурою
    """
    user_manager.add_user("Charlie", 40)
    assert "Charlie" in user_manager.get_all_users()


def test_remove_user(user_manager):
    """
    Тест для методу remove_user
    :param user_manager: Екземпляр UserManager, підготовлений фікстурою
    """
    user_manager.remove_user("Alice")
    assert "Alice" not in user_manager.get_all_users()


def test_get_all_users(user_manager):
    """
    Тест для методу get_all_users
    :param user_manager: Екземпляр UserManager, підготовлений фікстурою
    """
    users = user_manager.get_all_users()
    assert "Alice" in users
    assert "Bob" in users


@pytest.mark.skipif(len(UserManager().get_all_users()) < 3,
                    reason="Має бути принаймні три користувачі для цього тесту")
def test_skip_condition(user_manager):
    """
    Тест, який пропускається, якщо кількість користувачів менша за три
    :param user_manager: Екземпляр UserManager, підготовлений фікстурою
    """
    assert len(user_manager.get_all_users()) >= 3
