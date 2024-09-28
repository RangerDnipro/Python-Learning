"""
Завдання 2: Динамічний виклик функцій
Реалізуйте функцію call_function(obj, method_name, *args), яка приймає об'єкт, назву методу в вигляді рядка
та довільні аргументи для цього методу. Функція повинна викликати відповідний метод об'єкта і повернути результат.
"""


def call_function(obj, method_name, *args):
    """
    Динамічно викликає метод об'єкта.

    Args:
      obj: Об'єкт, у якого викликається метод.
      method_name: Назва методу у вигляді рядка.
      *args: Додаткові аргументи для методу.

    Returns:
      Результат виконання методу.
    """

    method = getattr(obj, method_name)
    return method(*args)


# Приклад використання
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b


calc = Calculator()
print(call_function(calc, "add", 10, 5))  # 15
print(call_function(calc, "subtract", 10, 5))  # 5
