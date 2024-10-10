"""
Реалізація класу WebService, який використовує бібліотеку requests
для отримання даних з вебсайтів
"""

import requests


class WebService:
    """
    Клас для отримання даних з вебсайтів за допомогою GET-запиту
    """

    def get_data(self, url: str, timeout: int = 5) -> dict:
        """
        Виконує GET-запит на вказаний URL та повертає JSON-відповідь
        :param url: URL для отримання даних
        :param timeout: Час очікування відповіді у секундах (за замовчуванням 5 секунд)
        :return: JSON-відповідь у вигляді словника або None, якщо запит завершився невдало
        :raises: Викликає помилку, якщо запит завершився невдало
        """
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return response.json()

        response.raise_for_status()
        # Явне повернення None у випадку помилки
        return None

    def get_status(self, url: str, timeout: int = 5) -> int:
        """
        Виконує GET-запит на вказаний URL та повертає статус код
        :param url: URL для отримання статусу
        :param timeout: Час очікування відповіді у секундах (за замовчуванням 5 секунд)
        :return: Статус код відповіді
        """
        response = requests.get(url, timeout=timeout)
        return response.status_code
