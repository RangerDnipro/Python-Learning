"""
Відповідає за підключення до сайту та завантаження HTML-коду сторінок
"""

import requests
from bs4 import BeautifulSoup


class Network:
    """
    Клас для завантаження HTML-коду сторінки з новинного сайту
    """

    def __init__(self, base_url: str):
        """
        Ініціалізує об'єкт класу з базовим URL
        :param base_url: URL сторінки
        """
        self.base_url = base_url
        self.session = requests.Session()

    def get_page(self, url: str) -> BeautifulSoup:
        """
        Завантажує HTML-сторінку за URL та повертає BeautifulSoup-об'єкт
        :param url: URL сторінки, яку необхідно завантажити
        :return: BeautifulSoup-об'єкт, що представляє HTML-код. Повертає None у разі помилки
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Не вдалося завантажити сторінку: {e}")
            return None
