"""
Завдання 9: Кешування результатів функції
Написати програму для кешування результатів функції, щоб покращити продуктивність.
1.	Створити функцію memoize, яка приймає функцію та повертає нову функцію, що зберігає результати викликів.
2.	Використати цю функцію, щоб кешувати результати обчислень (наприклад, факторіал або Фібоначчі).
"""

# Глобальний словник для всіх функцій
cache = {}


# Функція для кешування результатів
def memoize(func):
    global cache

    # is_main_call потрібен, щоб на кожній ітерації не виводився надпис
    def memoized_func(n, name=None, is_main_call=True):
        if name is None:
            name = func.__name__

        # Ініціалізуємо словник для конкретної функції
        if name not in cache:
            cache[name] = {}

        # Якщо результат для аргументів є в кеші, повертаємо його
        if n in cache[name]:
            if is_main_call:
                print(f"Знайдено в кеші функції {name} для {n}: {cache[name][n]}")
            return cache[name][n]
        else:
            # Якщо кеша ще нема, викликаємо функцію та зберігаємо результат в кеш для всіх ітерацій
            result = func(n, name, is_main_call=False)
            cache[name][n] = result
            if is_main_call:
                print(f"Обчислено результат функції {name} для {n}: {result}")
            return result

    return memoized_func


# Функція для обчислення факторіала
@memoize
def factorial(n, name=__name__, is_main_call=True):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1, name, is_main_call=False)


# Функція для обчислення чисел Фібоначчі
@memoize
def fibonacci(n, name=__name__, is_main_call=True):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1, name, is_main_call=False) + fibonacci(n - 2, name, is_main_call=False)


# Тестування

# Обчислюємо Факторіал
factorial(10)

# Обчислюємо Фібоначчі
fibonacci(10)

# Шукаємо в кеші Факторіал
factorial(1)
factorial(5)
factorial(10)

# Шукаємо в кеші Фібоначчі
fibonacci(1)
fibonacci(5)
fibonacci(10)
