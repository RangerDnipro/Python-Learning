"""
Програма для обчислення факторіал великого числа за допомогою декількох процесів,
розподіляючи обчислення між ними.
"""

import multiprocessing
from functools import reduce
from operator import mul
import sys


def factorial_partial(start: int, end: int) -> int:
    """
    Обчислює частковий факторіал для заданого діапазону чисел [start, end]
    :param start: Початкове число діапазону, включно
    :param end: Кінцеве число діапазону, включно
    :return: Частковий результат факторіала для заданого діапазону
    """
    result = 1
    for i in range(start, end + 1):
        result *= i
    return result


def calculate_factorial(n: int, num_processes: int = 4) -> int:
    """
    Обчислює факторіал числа n, розподіляючи обчислення між декількома процесами
    :param n: Число, для якого обчислюється факторіал. Має бути додатним цілим числом
    :param num_processes: Кількість процесів для розподілу роботи. За замовчуванням 4
    :return: Факторіал числа n
    """
    if n in (0, 1):
        return 1

    # Ділимо діапазон на частини для розподілу між процесами
    chunk_size = n // num_processes
    ranges = [(i * chunk_size + 1, (i + 1) * chunk_size) for i in range(num_processes)]
    # Включаємо залишок до останнього процесу
    ranges[-1] = (ranges[-1][0], n)

    # Використовуємо multiprocessing для розподілу обчислень
    with multiprocessing.Pool(processes=num_processes) as pool:
        partial_results = pool.starmap(factorial_partial, ranges)

    # Обчислюємо загальний результат факторіала
    factorial_result = reduce(mul, partial_results, 1)

    return factorial_result


if __name__ == "__main__":
    # Задаємо максимальну кількість цифр для перетворення на рядок
    sys.set_int_max_str_digits(1000000)

    # Зчитування числа n від користувача
    try:
        number = int(input("Введіть число для обчислення факторіалу: "))
        if number < 0:
            raise ValueError("Число має бути невід'ємним.")
    except ValueError as e:
        sys.exit(f"Помилка: {e}")

    # Обчислення факторіала та вивід результату
    fact_result = calculate_factorial(number)
    print(f"Факторіал числа {number} дорівнює {fact_result}")
