"""
Модуль для асинхронного завантаження сторінок
"""

import asyncio
import random
from typing import List


async def download_page(url: str) -> None:
    """
    Симулює завантаження сторінки за випадковий проміжок часу від 1 до 5 секунд
    :param url: URL сторінки, яку потрібно завантажити.
    :return: None
    """
    # Випадковий час завантаження сторінки від 1 до 5 секунд
    load_time = random.randint(1, 5)
    await asyncio.sleep(load_time)
    print(f"Сторінку {url} завантажено за {load_time} секунд.")


async def main(urls: List[str]) -> None:
    """
    Приймає список URL і завантажує їх одночасно, використовуючи функцію download_page
    :param urls: Список URL, які потрібно завантажити.
    :return: None
    """
    # Використання asyncio.gather для паралельного завантаження всіх сторінок
    await asyncio.gather(*(download_page(url) for url in urls))


# Тестування
if __name__ == "__main__":
    # Список URL для завантаження
    test_urls = [
        "http://google.com",
        "http://youtube.com",
        "http://facebook.com"
    ]
    # Запуск асинхронної головної функції
    asyncio.run(main(test_urls))
