# Додаткові питання для роздумів:

Як можна інтегрувати асинхронний код у вже існуючий синхронний проект на Python?
Які підводні камені використання асинхронних бібліотек при роботі з базами даних?

Інтеграція асинхронного коду у синхронний проект на Python

Щоб інтегрувати асинхронний код у вже існуючий синхронний проект на Python, потрібно поступово адаптувати функціонал, зберігаючи баланс між старими та новими частинами.

Основні підходи інтеграції асинхронного коду

1. Перехід до використання asyncio та event loop

Додайте event loop у синхронний код і перетворюйте деякі блокуючі функції на асинхронні. Якщо синхронні частини викликають асинхронний код, використовуйте asyncio.run() або loop.run_until_complete(), щоб забезпечити коректне виконання.

Приклад використання asyncio:

import asyncio

def sync_function():
    print("Це синхронна функція")

async def async_function():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, sync_function)

if __name__ == "__main__":
    asyncio.run(async_function())

2. Мікс синхронних та асинхронних функцій

Для існуючого коду можна залишити синхронні функції, але використовувати асинхронні для нових задач, які потребують неблокуючого виконання (наприклад, запити до API або тривалі обчислення).

Приклад:

import asyncio
import time

def sync_function():
    print("Це синхронна функція")
    time.sleep(2)
    print("Синхронна функція завершена")

async def async_function():
    print("Це асинхронна функція")
    await asyncio.sleep(1)
    print("Асинхронна функція завершена")

async def main():
    loop = asyncio.get_event_loop()
    # Виклик синхронної функції в асинхронному контексті
    await loop.run_in_executor(None, sync_function)
    # Виклик асинхронної функції
    await async_function()

if __name__ == "__main__":
    asyncio.run(main())

3. Використання окремих потоків або процесів

Якщо є частини, що залишаються синхронними, їх можна відокремити в окремий потік або процес. Наприклад, для синхронних операцій з базою даних, в той час як асинхронні функції виконуються паралельно. Рекомендується використовувати модулі threading або multiprocessing для реалізації такого підходу.

Приклад використання потоків:

import threading
import time

def sync_function():
    print("Це синхронна функція")
    time.sleep(2)
    print("Синхронна функція завершена")

def main():
    thread = threading.Thread(target=sync_function)
    thread.start()
    print("Паралельне виконання триває...")
    thread.join()

if __name__ == "__main__":
    main()

Приклад використання процесів:

import multiprocessing
import time

def sync_function():
    print("Це синхронна функція")
    time.sleep(2)
    print("Синхронна функція завершена")

def main():
    process = multiprocessing.Process(target=sync_function)
    process.start()
    print("Паралельне виконання триває...")
    process.join()

if __name__ == "__main__":
    main()

Підводні камені використання асинхронних бібліотек при роботі з базами даних

1. Підтримка драйверами бази даних

Не всі бібліотеки баз даних підтримують асинхронні операції. Потрібно використовувати асинхронні клієнти, такі як aiomysql (для MySQL), asyncpg (для PostgreSQL) або motor (для MongoDB). Наприклад, для PostgreSQL ви можете використовувати asyncpg для асинхронного виконання запитів, а для MySQL — aiomysql. Це додає обмеження на вибір інструментів.

2. Блокування операцій

Навіть асинхронні бібліотеки можуть інколи блокувати event loop при виконанні певних важких запитів, що може призвести до затримок. Важливо враховувати цей аспект та оптимізувати запити або використовувати пул потоків для розвантаження. Рекомендується використовувати ThreadPoolExecutor з модуля concurrent.futures, щоб виконувати блокуючі функції в окремих потоках і мінімізувати блокування event loop.

Приклад:

import asyncio
from concurrent.futures import ThreadPoolExecutor

def blocking_function():
    # Симуляція важкої операції
    import time
    time.sleep(2)
    print("Блокуюча операція завершена")

async def main():
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        await loop.run_in_executor(executor, blocking_function)

if __name__ == "__main__":
    asyncio.run(main())

3. Робота з транзакціями

Асинхронне виконання транзакцій може бути складнішим через необхідність збереження цілісності даних. Важливо забезпечити коректне завершення або скасування транзакцій у випадку асинхронного збою.

Приклад використання asyncpg для PostgreSQL:

import asyncpg
import asyncio

async def run_transaction():
    conn = await asyncpg.connect(user='user', password='password', database='dbname', host='127.0.0.1')
    try:
        async with conn.transaction():
            await conn.execute('INSERT INTO users(name) VALUES($1)', 'Ім'я користувача')
            await conn.execute('INSERT INTO orders(user_id, amount) VALUES($1, $2)', 1, 100)
    except Exception as e:
        print(f"Помилка при виконанні транзакції: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(run_transaction())

4. Змішування синхронних та асинхронних викликів

Це може призводити до непередбачуваних блокувань. Наприклад, якщо ви викликаєте синхронну функцію всередині асинхронної, це потенційно блокує весь event loop. Рекомендується уникати змішування синхронних і асинхронних викликів або використовувати обгортки, такі як loop.run_in_executor(), для безпечного виконання синхронних функцій в асинхронному контексті.
