"""
Модуль в якому об'єднані завдання 1 та 2, для демонстрації можливості
обробки довготривалих завдань під час роботи з чергою
"""

import asyncio


async def producer(queue: asyncio.Queue) -> None:
    """
    Додає завдання до черги з інтервалом у 1 секунду
    :param queue: Асинхронна черга для завдань
    """
    for i in range(5):
        # Імітація затримки додавання завдання
        await asyncio.sleep(1)
        task = f"Завдання {i + 1}"
        await queue.put(task)
        print(f"Продюсер: додано {task} до черги")


async def consumer(queue: asyncio.Queue) -> None:
    """
    Забирає завдання з черги та обробляє його з затримкою у 2 секунди
    :param queue: Асинхронна черга для завдань
    """
    while True:
        task = await queue.get()
        if task is None:
            # Якщо отримали спеціальний маркер, завершуємо роботу споживача
            queue.task_done()
            break
        print(f"Споживач: починається обробка {task}")
        # Імітація обробки завдання
        await asyncio.sleep(2)
        print(f"Споживач: завершено обробку {task}")
        # Позначаємо завдання як виконане
        queue.task_done()


async def slow_task() -> None:
    """
    Імітує виконання завдання протягом 10 секунд
    """
    print("slow_task: початок виконання")
    await asyncio.sleep(10)
    print("slow_task: завершено виконання")


async def main() -> None:
    """
    Основна функція для запуску продюсера та споживачів
    """
    queue = asyncio.Queue()
    # Створюємо продюсера та двох споживачів
    producer_task = asyncio.create_task(producer(queue))
    consumer_tasks = [asyncio.create_task(consumer(queue)) for _ in range(2)]

    # Додамо виклик slow_task з таймаутом 5 секунд
    try:
        await asyncio.wait_for(slow_task(), timeout=5)
    except asyncio.TimeoutError:
        print("slow_task: перевищено час очікування (таймаут 5 секунд)")

    # Чекаємо завершення продюсера
    await producer_task

    # Додаємо спеціальні маркери для завершення споживачів
    for _ in range(2):
        await queue.put(None)

    # Чекаємо завершення всіх споживачів
    await asyncio.gather(*consumer_tasks)


# Запуск основної асинхронної функції
if __name__ == "__main__":
    asyncio.run(main())
