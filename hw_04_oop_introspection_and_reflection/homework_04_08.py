"""
Завдання 8: Перевірка успадкування та методів класу
Напишіть функцію analyze_inheritance(cls), яка приймає клас, аналізує його спадкування та виводить усі методи,
які він наслідує від базових класів.
"""

import inspect


def analyze_inheritance(cls):
    """
    Функція для аналізу спадкування класу та виведення методів, наслідуваних від базових класів
    :param cls: Клас, що аналізується
    """
    # Отримуємо базові класи
    base_classes = cls.__bases__

    # Якщо клас не має явно вказаного базового класу
    if base_classes == (object,):
        print(f"Клас {cls.__name__} не має користувацьких базових класів.")
        return

    # Перебираємо всі базові класи
    print(f"Клас {cls.__name__} наслідує:")
    for base_class in cls.__bases__:
        # Отримуємо методи базового класу
        methods = inspect.getmembers(base_class, predicate=inspect.isfunction)
        for method_name, _ in methods:
            # Перевіряємо чи метод наслідується
            if hasattr(cls, method_name) and method_name not in cls.__dict__:
                print(f"- {method_name} з {base_class.__name__}")


# Тестування
class Parent:
    def parent_method(self):
        pass


class Child(Parent):
    def child_method(self):
        pass


class Grandchild(Child):
    def grandchild_method(self):
        pass


analyze_inheritance(Parent)
analyze_inheritance(Child)
analyze_inheritance(Grandchild)
