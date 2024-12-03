"""
Завдання 4: Створення класу динамічно
Напишіть функцію create_class(class_name, methods), яка створює клас з заданим іменем та методами.
Методи передаються у вигляді словника, де ключі — це назви методів, а значення — функції
"""


def create_class(class_name, methods):
    """
    Створює динамічний клас з заданим ім'ям та методами
    :param class_name: Назва нового класу (рядок)
    :param methods: Словник, де ключі - назви методів, а значення - функції
    :return: Новий клас з заданими методами
    """
    # Створюємо клас динамічно за допомогою функції type
    return type(class_name, (object,), methods)


# Функції, які будемо додавати до класу
def say_hello(self):
    return "Hello!"


def say_goodbye(self):
    return "Goodbye!"


# Словник методів
methods = {"say_hello": say_hello, "say_goodbye": say_goodbye}

# Створюємо динамічний клас
MyDynamicClass = create_class("MyDynamicClass", methods)

# Створюємо об'єкт цього класу
obj = MyDynamicClass()

# Викликаємо методи
print(obj.say_hello())
print(obj.say_goodbye())
