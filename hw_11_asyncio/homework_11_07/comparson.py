"""
Модуль для виконання запитів за допомогою синхронного, багатопотокового,
багатопроцесорного та асинхронного режимів з прогрес баром для наочності
"""

import time
import threading
import multiprocessing
import asyncio
import requests
import aiohttp
from tqdm import tqdm

# URL для виконання запитів
URL = "https://jsonplaceholder.typicode.com/posts/1"


# Синхронний підхід
def synchronous_requests() -> None:
    """
    Виконуємо 500 синхронних HTTP запитів та вимірюємо час виконання
    """
    start_time = time.time()
    for _ in tqdm(range(500), desc="Синхронний підхід"):
        try:
            response = requests.get(URL, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error: {e}")
    end_time = time.time()
    print(f"Синхронний підхід, 500 запитів виконано за {end_time - start_time:.2f} секунд")


# Багатопотоковий підхід
def multithreaded_requests() -> None:
    """
    Виконуємо 500 HTTP запитів у багатопотоковому режимі та вимірюємо час виконання
    """

    def fetch() -> None:
        try:
            response = requests.get(URL, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error: {e}")

    start_time = time.time()
    threads = []
    for _ in tqdm(range(500), desc="Багатопотоковий підхід"):
        thread = threading.Thread(target=fetch)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Багатопотоковий підхід, 500 запитів виконано за {end_time - start_time:.2f} секунд")


# Багатопроцесорний підхід
def fetch_multiprocess(url: str) -> None:
    """
    Виконуємо HTTP запит за вказаною URL-адресою.
    :param url: URL для виконання запиту
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")


def multiprocessed_requests() -> None:
    """
    Виконуємо 500 HTTP запитів у багатопроцесорному режимі та вимірюємо час виконання
    """
    start_time = time.time()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for _ in tqdm(pool.imap_unordered(fetch_multiprocess, [URL] * 500),
                      total=500, desc="Багатопроцесорний підхід"):
            pass
    end_time = time.time()
    print(f"Багатопроцесорний підхід, 500 запитів виконано за {end_time - start_time:.2f} секунд")


# Асинхронний підхід з aiohttp
async def async_requests() -> None:
    """
    Виконуємо 500 асинхронних HTTP запитів та вимірюємо час виконання
    """
    async with aiohttp.ClientSession() as session:
        async def fetch() -> None:
            try:
                async with session.get(URL, timeout=10) as response:
                    await response.text()
            except aiohttp.ClientError as e:
                print(f"Error: {e}")

        start_time = time.time()
        tasks = [fetch() for _ in range(500)]
        for _ in tqdm(asyncio.as_completed(tasks), total=500, desc="Асинхронний підхід"):
            await _
        end_time = time.time()
        print(f"Асинхронний підхід, 500 запитів виконано за {end_time - start_time:.2f} секунд")


if __name__ == "__main__":
    # Синхронне виконання
    synchronous_requests()
    time.sleep(1)

    # Багатопотокове виконання
    multithreaded_requests()
    time.sleep(1)

    # Багатопроцесорне виконання
    multiprocessed_requests()
    time.sleep(1)

    # Асинхронне виконання
    asyncio.run(async_requests())
