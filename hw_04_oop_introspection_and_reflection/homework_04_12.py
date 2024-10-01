"""
Завдання 12: Автоматичне логування доступу до атрибутів (опціонально)
Створіть метаклас LoggingMeta, який автоматично додає логування при доступі до будь-якого атрибута класу.
Кожен раз, коли атрибут змінюється або читається, повинно з'являтися повідомлення в консолі.
"""


class LoggedAttribute:
    """
    Дескриптор для логування доступу до атрибутів класу
    """

    def __init__(self, name):
        """
        Ініціалізуємо дескриптор з ім'ям атрибута
        :param name: Ім'я атрибута (рядок)
        """
        self.name = name

    def __get__(self, instance, owner):
        """
        Отримуємо значення атрибута з логуванням доступу
        :param instance: Екземпляр класу
        :param owner: Клас, до якого належить атрибут
        :return: Значення атрибута
        """
        print(f"Logging: accessed '{self.name}'")
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        """
        Встановлюємо нове значення атрибута з логуванням зміни
        :param instance: Екземпляр класу
        :param value: Нове значення для атрибута
        """

        # Логування зміни значення тільки якщо атрибут вже існує
        if self.name in instance.__dict__:
            print(f"Logging: modified '{self.name}'")
        instance.__dict__[self.name] = value


class MyClass:
    """
    Клас, що демонструє використання дескриптора LoggedAttribute
    """

    # Оголошуємо атрибут name як дескриптор
    name = LoggedAttribute('name')

    def __init__(self, name):
        """
        Ініціалізує екземпляр класу з ім'ям
        :param name: Ім'я для ініціалізації (рядок)
        """

        # Використовуємо дескриптор
        self.name = name


# Тестування
if __name__ == "__main__":
    # Створюємо екземпляр класу MyClass з ім'ям Python
    obj = MyClass("Python")
    # Зчитуємо атрибут name через print для виводу Logging: accessed 'name' (також друкується саме ім'я)
    print(obj.name)
    # Змінюємо атрибут name для виводу Logging: modified 'name'
    obj.name = "New Python"
    # Зчитуємо атрибут name для виводу Logging: accessed 'name'
    value = obj.name
    print(value)
