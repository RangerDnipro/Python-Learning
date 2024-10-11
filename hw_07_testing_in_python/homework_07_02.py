"""
Завдання 2. Мокування за допомогою unittest.mock
Напишіть програму для отримання даних з вебсайту та протестуйте його за допомогою моків.
Напишіть клас WebService, який має метод get_data(url: str) -> dict.
Цей метод повинен використовувати бібліотеку requests, щоб робити GET-запит
та повертати JSON-відповідь. Використовуйте unittest.mock для мокування HTTP-запитів.
Замокуйте метод requests.get таким чином, щоб він повертав фейкову відповідь
(наприклад, {"data": "test"}), та протестуйте метод get_data.
Напишіть кілька тестів:
- перевірка успішного запиту (200),
- перевірка обробки помилки (404 чи інші коди).
"""

import unittest
from unittest.mock import patch
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


class TestWebService(unittest.TestCase):
    """
    Набір тестів для перевірки функціональності класу WebService з
    використанням мокування HTTP-запитів
    """

    @patch('requests.get')
    def test_get_data_success(self, mock_get) -> None:
        """
        Перевіряє успішне отримання даних (статус-код 200)
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "test"}

        service = WebService()
        result = service.get_data('http://fakeurl.com')

        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with('http://fakeurl.com', timeout=5)

    @patch('requests.get')
    def test_get_data_404(self, mock_get) -> None:
        """
        Перевіряє обробку помилки, коли сервер повертає 404
        """
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

        service = WebService()

        with self.assertRaises(requests.exceptions.HTTPError):
            service.get_data('http://fakeurl.com')

        mock_get.assert_called_once_with('http://fakeurl.com', timeout=5)

    @patch('requests.get')
    def test_get_data_none_return_on_error(self, mock_get) -> None:
        """
        Перевіряє, що метод get_data повертає None, коли викликається raise_for_status
        """
        mock_get.return_value.status_code = 500
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

        service = WebService()

        with self.assertRaises(requests.exceptions.HTTPError):
            service.get_data('http://fakeurl.com')

        mock_get.assert_called_once_with('http://fakeurl.com', timeout=5)

    @patch('requests.get')
    def test_get_status_success(self, mock_get) -> None:
        """
        Перевіряє отримання статус-коду запиту
        """
        mock_get.return_value.status_code = 200

        service = WebService()
        result = service.get_status('http://fakeurl.com')

        self.assertEqual(result, 200)
        mock_get.assert_called_once_with('http://fakeurl.com', timeout=5)


if __name__ == '__main__':
    unittest.main()
