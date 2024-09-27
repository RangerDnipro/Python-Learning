"""
Завдання 6. Access-like
1.	Реалізуйте клас User з атрибутами first_name, last_name, email.
Додайте методи для отримання та встановлення цих атрибутів через декоратор @property.
2.	Додайте методи для перевірки формату email-адреси.
"""

import re


class User:
    def __init__(self, first_name, last_name, email):
        """
        Ініціалізує об'єкт User з атрибутами first_name, last_name, email.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @property
    def first_name(self):
        """
        Повертає ім'я користувача.
        :return: first_name
        """
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """
        Встановлює ім'я користувача.
        :param value: нове ім'я
        """
        if not isinstance(value, str):
            raise TypeError("Ім'я має бути рядком")
        self._first_name = value

    @property
    def last_name(self):
        """
        Повертає прізвище користувача.
        :return: last_name
        """
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """
        Встановлює прізвище користувача.
        :param value: нове прізвище
        """
        if not isinstance(value, str):
            raise TypeError("Прізвище має бути рядком")
        self._last_name = value

    @property
    def email(self):
        """
        Повертає email користувача.
        :return: email
        """
        return self._email

    @email.setter
    def email(self, value):
        """
        Встановлює email користувача після перевірки формату.
        :param value: новий email
        """
        if not self._validate_email(value):
            raise ValueError("Некоректний формат email")
        self._email = value

    @staticmethod
    def _validate_email(email):
        """
        Перевіряє формат email-адреси за допомогою регулярного виразу.
        :param email: email для перевірки
        :return: True, якщо формат правильний, інакше False
        """
        regex = r'\S+@\S+\.\S+'
        return re.match(regex, email)

    def __repr__(self):
        """
        Повертає рядкове представлення об'єкта User.
        :return: рядок з інформацією про користувача
        """
        return f"Ім'я: '{self.first_name}', Прізвище: '{self.last_name}', email '{self.email}')"


# Тестове введення користувача
user = User("Тарас", "Шевченко", "slava.ukraini@example.com")
print(user)

# Спроба встановити некоректний email
try:
    user.email = "invalid_email"
except ValueError as e:
    print(e)
