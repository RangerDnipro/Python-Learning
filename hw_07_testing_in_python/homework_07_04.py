"""
Завдання 4. Тестування з використанням doctest

Додайте документацію з прикладами використання та напишіть тести з використанням doctest.
Напишіть функції для роботи з числами:
is_even(n: int) -> bool: перевіряє, чи є число парним.
factorial(n: int) -> int: повертає факторіал числа.

Додайте doctest-приклади для кожної функції
Переконайтеся, що doctest проходить для кожної функції запустивши тести через python -m doctest.
"""


def is_even(n: int) -> bool:
    """
    Перевіряє, чи є число парним
    :param n: Ціле число, яке потрібно перевірити
    :return: True, якщо число парне, інакше False

    Приклади:
    >>> is_even(2)
    True
    >>> is_even(3)
    False
    >>> is_even(0)
    True
    >>> is_even(-4)
    True
    >>> is_even(-5)
    False
    """
    return n % 2 == 0


def factorial(n: int) -> int:
    """
    Обчислює факторіал числа
    :param n: Ціле невід'ємне число, для якого потрібно знайти факторіал
    :return: Факторіал числа n

    Приклади:
    >>> factorial(0)
    1
    >>> factorial(1)
    1
    >>> factorial(5)
    120
    >>> factorial(3)
    6

    Важливо: для від'ємних значень викликається ValueError
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: Факторіал визначений тільки для невід'ємних цілих чисел
    """
    if n < 0:
        raise ValueError("Факторіал визначений тільки для невід'ємних цілих чисел")

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
