# Зразок використання декораторів в Python
def my_param_decorator(precision):
    """
    Декоратор, який округлює результат функції до заданої точності.
    """

    def my_decorator(func):
        def wrapper(*args, **kwargs):
            """
            Внутрішня функція, яка виконує обгортку.
            """
            return round(func(*args, **kwargs), precision)
        return wrapper
    return my_decorator


@my_param_decorator(2)
def my_func(digit: float) -> float:
    """
    Множить задане число на 10 та округлює результат до 2 знаків після коми.
    """
    return digit * 10


print(my_func(15.5566666))
