"""
Модуль для запуску асинхронного веб-сервера, завдання 5 
"""

import asyncio
from aiohttp import web, ClientSession


async def handle_root(request: web.Request) -> web.Response:  # pylint: disable=unused-argument
    """
    Обробляємо маршрут /, повертаючи простий текст "Hello, World!"
    :param request: Запит до сервера, аргумент необхідний для того,
    щоб функція могла відповідати вимогам бібліотеки aiohttp і отримувати запити
    :return: Відповідь з текстом "Hello, World!"
    """
    return web.Response(text="Hello, World!")


async def handle_slow(request: web.Request) -> web.Response:  # pylint: disable=unused-argument
    """
    Обробляємо маршрут /slow, імітуючи довгу операцію
    з затримкою в 5 секунд і повертаючи текст "Operation completed"
    :param request: Запит до сервера, аргумент необхідний для того,
    щоб функція могла відповідати вимогам бібліотеки aiohttp і отримувати запити
    :return: Відповідь з текстом "Operation completed" після затримки в 5 секунд
    """
    await asyncio.sleep(5)
    return web.Response(text="Operation completed")


async def init_app() -> web.Application:
    """
    Ініціалізуємо вебзастосунок з двома маршрутами: / і /slow.
    :return: Вебзастосунок
    """
    app = web.Application()
    app.router.add_get('/', handle_root)
    app.router.add_get('/slow', handle_slow)
    return app


async def make_requests() -> None:
    """
    Створюємо кілька запитів до маршрутів / і /slow одночасно та виводить відповідні повідомлення
    """
    async with ClientSession() as session:
        tasks = []
        for _ in range(3):
            tasks.append(session.get('http://localhost:8080/'))
            tasks.append(session.get('http://localhost:8080/slow'))

        responses = await asyncio.gather(*tasks)
        for response in responses:
            text = await response.text()
            print(f"Отримано відповідь: {text}")


async def main() -> None:
    """
    Основна функція для запуску вебсервера, виконання запитів та зупинки сервера
    """
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    print("Сервер запущено на http://localhost:8080")
    await site.start()

    # Запускаємо запити до серверу
    await make_requests()

    # Зупиняємо сервер
    await runner.cleanup()
    print("Сервер зупинено")


if __name__ == "__main__":
    asyncio.run(main())
