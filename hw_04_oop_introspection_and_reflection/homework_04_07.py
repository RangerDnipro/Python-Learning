"""
Завдання 7: Декоратор для логування викликів методів
Реалізуйте декоратор log_methods, який додається до класу і логуватиме виклики всіх його методів
(назва методу та аргументи).
"""


def log_methods(cls):
    """
    Декоратор для логування викликів методів класу
    :param cls: Клас, методи якого потрібно логувати
    :return: Клас із логованими методами
    """
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            # Перевіряємо, чи атрибут є методом
            original_method = attr_value

            # Створюємо обгортку для кожного методу
            def log_method_call(method):
                def wrapper(*args, **kwargs):
                    print(f"Logging: {method.__name__} called with {args[1:]}")
                    return method(*args, **kwargs)

                return wrapper

            # Обертаємо метод у логуючу обгортку
            setattr(cls, attr_name, log_method_call(original_method))

    return cls


# Використання декоратора
@log_methods
class MyClass:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b


# Тестування
obj = MyClass()

# Виклики методів з логуванням
obj.add(5, 3)
obj.subtract(5, 3)
