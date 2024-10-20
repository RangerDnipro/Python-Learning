"""
Модуль використовує модуль multiprocessing для паралельного обчислення суми великого масиву чисел,
розділяючи його на частини та обробляючи кожну частину у окремому процесі
"""

import multiprocessing
from typing import List


def calculate_partial_sum(numbers: List[int],
                          result_queue: multiprocessing.Queue, index: int) -> None:
    """
    Підраховує суму частини великого масиву чисел і передає результат у чергу
    :param numbers: Список чисел для підрахунку суми
    :param result_queue: Черга для збереження результату підрахунку суми
    :param index: Індекс частини, яку обробляє даний процес (для ідентифікації результату)
    :return: None
    """
    partial_sum = sum(numbers)
    # Додаємо результат у чергу разом з індексом для подальшого збирання
    result_queue.put((index, partial_sum))


def parallel_sum(array: List[int], num_parts: int) -> int:
    """
    Ділить великий масив чисел на кілька частин і рахує суму кожної частини
    паралельно в різних процесах
    :param array: Великий масив чисел, для якого потрібно підрахувати суму
    :param num_parts: Кількість частин, на які слід розділити масив
    :return: Загальна сума всіх чисел у масиві
    """
    # Розбиваємо масив на частини приблизно однакового розміру
    chunk_size = len(array) // num_parts
    chunks = [array[i * chunk_size:(i + 1) * chunk_size] for i in range(num_parts)]
    if len(array) % num_parts != 0:
        # Додаємо залишок, якщо є
        chunks.append(array[num_parts * chunk_size:])

    # Створюємо чергу для зберігання результатів
    result_queue = multiprocessing.Queue()
    processes = []

    # Створюємо процеси для обробки кожної частини масиву
    for index, chunk in enumerate(chunks):
        process = multiprocessing.Process(target=calculate_partial_sum,
                                          args=(chunk, result_queue, index))
        processes.append(process)
        process.start()

    # Очікуємо завершення всіх процесів
    for process in processes:
        process.join()

    # Збираємо результати з черги
    results = [result_queue.get() for _ in processes]
    # Сортуємо результати за індексом, щоб зберегти правильний порядок
    results.sort()
    total_sum = sum(partial_sum for _, partial_sum in results)

    return total_sum


if __name__ == "__main__":
    # Приклад використання
    # Масив чисел від 1 до 1000000
    large_array = list(range(1, 1000001))
    # Кількість процесів для паралельної обробки
    NUM_PROCESSES = 4

    # Обчислюємо суму масиву паралельно
    total = parallel_sum(large_array, NUM_PROCESSES)
    print(f"Загальна сума: {total}")
