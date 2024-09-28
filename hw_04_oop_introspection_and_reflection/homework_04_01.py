"""
Завдання 1: Перевірка типів і атрибутів об'єктів
Напишіть функцію analyze_object(obj), яка приймає будь-який об'єкт та виводить:
Тип об'єкта.
Список всіх методів та атрибутів об'єкта.
Тип кожного атрибута.
"""


def analyze_object(obj):
    """
    Функція для аналізу об'єкта.
  
    Аргументи:
      obj: Будь-який об'єкт Python.
  
    Повертає:
      None (виводить інформацію безпосередньо)
    """

    print(f"Тип об'єкта: {type(obj)}")
    print("Атрибути і методи:")

    for attr in dir(obj):
        attribute = getattr(obj, attr)
        print(f"- {attr}: {type(attribute)}")


# Приклад використання
class MyClass:
    def __init__(self, value):
        self.value = value

    def say_hello(self):
        return f"Hello, {self.value}"


obj = MyClass("World")
analyze_object(obj)
