"""
Завдання 5. Тестування винятків у pytest (опціонально)
Напишіть функцію divide(a: int, b: int) -> float, яка поділяє два числа. Якщо знаменник дорівнює
нулю, функція повинна викидати виняток ZeroDivisionError. Напишіть тести з використанням pytest,
які:
- перевіряють коректний поділ,
- перевіряють викидання виключення ZeroDivisionError, якщо знаменник дорівнює нулю.
Додайте тест із параметризацією для перевірки поділу з різними значеннями.
"""

# Тестування функції divide за допомогою pytest
import pytest


# Функція для поділу двох чисел з документацією та обробкою виключень
def divide(a: int, b: int) -> float:
    """
    Поділяє два числа
    :param a: Ділене, ціле число
    :param b: Дільник, ціле число
    :return: Результат ділення двох чисел
    :raises ZeroDivisionError: Якщо знаменник дорівнює нулю
    """
    if b == 0:
        raise ZeroDivisionError("Знаменник не може дорівнювати нулю.")
    return a / b


# Тест перевіряє коректний поділ двох чисел
def test_divide_correct():
    """
    Перевіряє коректний результат ділення чисел
    """
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0
    assert divide(-10, 2) == -5.0


# Тест перевіряє, що функція викликає виключення ZeroDivisionError, якщо знаменник дорівнює нулю
def test_divide_zero_division():
    """
    Перевіряє викидання виключення ZeroDivisionError, коли знаменник дорівнює нулю
    """
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


# Параметризований тест для перевірки ділення з різними значеннями
@pytest.mark.parametrize("a, b, expected", [
    (20, 5, 4.0),
    (15, 3, 5.0),
    (-30, 10, -3.0),
    (0, 5, 0.0),
])
def test_divide_parametrized(a: int, b: int, expected: float):
    """
    Параметризований тест для перевірки ділення з різними вхідними значеннями
    :param a: Ділене, ціле число
    :param b: Дільник, ціле число
    :param expected: Очікуваний результат ділення
    """
    assert divide(a, b) == expected


# Запуск тестів
if __name__ == "__main__":
    pytest.main()