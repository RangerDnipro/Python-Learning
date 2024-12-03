"""
Завдання 3: Інспекція модулів
Напишіть програму, яка приймає на вхід назву модуля (рядок) та виводить список
усіх класів, функцій та їхніх сигнатур у модулі. Використовуйте модуль inspect.
"""

import inspect
import importlib


def format_signature(obj):
    """
    Форматує сигнатуру об'єкта
    :param obj: Об'єкт для форматування сигнатури
    :return: Рядок, що представляє сигнатуру
    """
    try:
        signature = inspect.signature(obj)
        params = []
        for param in signature.parameters.values():
            params.append(param.name)
        return f"({', '.join(params)})"
    except ValueError:
        return "(немає сигнатури)"


def analyze_module(module_name):
    """
    Аналізує модуль і виводить усі функції та класи з їхніми сигнатурами
    :param module_name: Назва модуля для аналізу
    :return: None (виводить інформацію безпосередньо)
    """
    try:
        # Завантажуємо модуль за його назвою
        module = importlib.import_module(module_name)
    except ImportError:
        print(f"Модуль '{module_name}' не знайдено.")
        return

    # Отримуємо функції та класи пропускаючи приватні атрибути
    functions = [member for member in inspect.getmembers(module, callable) if not member[0].startswith('_')]
    classes = [member for member in inspect.getmembers(module) if
               inspect.isclass(member[1]) and not member[0].startswith('_')]

    # Виведення функцій з сигнатурами
    print("Функції:")
    if functions:
        for name, obj in functions:
            print(f"- {name}{format_signature(obj)}")
    else:
        print(f"- <немає функцій у модулі {module_name}>")

    # Виведення класів з сигнатурами
    print("\nКласи:")
    if classes:
        for name, obj in classes:
            print(f"- {name}{format_signature(obj)}")
    else:
        print(f"- <немає класів у модулі {module_name}>")


# Приклад виконання програми
analyze_module("math")
