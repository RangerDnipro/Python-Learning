"""
Основний модуль для запуску Python-пакету скрапінгу новин, пакет має таку структуру:

hw_13_web_scrapping/
│
├── web_scrapping/          # Пакет для модулів веб-скрапінгу
│   ├── __init__.py         # Ініціалізація пакета
│   ├── network.py          # Робота з мережею та отримання даних
│   ├── parser.py           # Парсинг HTML
│   ├── storage.py          # Збереження даних, робота з файлами
│   ├── filtering.py        # Фільтрація новин за датою
│   └── report.py           # Генерація звітів
│
└── main.py                 # Основний скрипт для запуску процесу
"""

import time
from web_scrapping import Network
from web_scrapping import Parser
from web_scrapping import Storage
from web_scrapping import Filtering
from web_scrapping import Report

if __name__ == "__main__":
    # URL головної сторінки новинного сайту
    BASE_URL = "https://www.bbc.com/ukrainian/topics/czp6w66edqpt"

    # Створення об'єктів для роботи
    network = Network(BASE_URL)
    parser = Parser(network)

    # Парсинг кількох сторінок новин
    all_news = []
    # Кількість сторінок для парсингу
    PAGES = 1
    for page in range(1, PAGES + 1):
        PAGE_URL = f"{BASE_URL}?page={page}"
        soup = network.get_page(PAGE_URL)
        news = parser.parse_news(soup)
        all_news.extend(news)
        # Затримка між запитами для уникнення блокування
        time.sleep(2)

    # Збереження даних у CSV файл
    Storage.save_to_csv(all_news)

    # Фільтрація новин за останні 7 днів
    recent_news = Filtering.filter_news_by_date(all_news, days=7)
    Storage.save_to_csv(recent_news, filename='recent_news.csv')

    # Генерація звіту
    Report.generate_report(recent_news)
