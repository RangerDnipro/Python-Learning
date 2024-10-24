"""
Модуль в якому об'єднані два перших завдання для асинхронного завантаження сторінок
"""

import asyncio
import random
from typing import List
import aiohttp


async def download_page(url: str) -> None:
    """
    Симулює завантаження сторінки за випадковий проміжок часу від 1 до 5 секунд
    :param url: URL сторінки, яку потрібно завантажити
    :return: None
    """
    # Випадковий час завантаження сторінки від 1 до 5 секунд
    load_time = random.randint(1, 5)
    await asyncio.sleep(load_time)
    print(f"Сторінку {url} завантажено за {load_time} секунд.")


async def fetch_content(url: str) -> str:
    """
    Виконує HTTP-запит до вказаного URL і повертає вміст сторінки
    :param url: URL сторінки, яку потрібно завантажити
    :return: Вміст сторінки або повідомлення про помилку
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Перевірка статусу відповіді
                response.raise_for_status()
                content = await response.text()
                print(f"Сторінку {url} успішно завантажено.")
                return content
    except aiohttp.ClientError as e:
        error_message = f"Помилка підключення до {url}: {str(e)}"
        print(error_message)
        return error_message


async def fetch_all(urls: List[str]) -> List[str]:
    """
    Приймає список URL і завантажує вміст усіх сторінок паралельно
    :param urls: Список URL, які потрібно завантажити
    :return: Список вмісту сторінок або повідомлень про помилки
    """
    # Використання asyncio.gather для паралельного завантаження всіх сторінок
    results = await asyncio.gather(*(fetch_content(url) for url in urls))
    return results


async def main(urls: List[str]) -> None:
    """
    Приймає список URL і завантажує їх одночасно, використовуючи функцію download_page
    :param urls: Список URL, які потрібно завантажити
    :return: None
    """
    # Використання asyncio.gather для паралельного завантаження всіх сторінок
    await asyncio.gather(*(download_page(url) for url in urls))


# Тестування
if __name__ == "__main__":
    # Список URL для завантаження
    test_urls = [
        "https://www.google.com/",
        "https://www.youtube.com/",
        "https://www.facebook.com/",
        "https://www.instagram.com/",
        "https://x.com/"
    ]
    # Запуск відповідної асинхронної функції
    # Симуляція завантаження сторінок за випадковий проміжок часу
    asyncio.run(main(test_urls))
    print()
    # Паралельне завантаження вмісту усіх сторінок
    asyncio.run(fetch_all(test_urls))
