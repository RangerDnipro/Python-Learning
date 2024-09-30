"""
Завдання 6: Інтерсепція методів класу (Proxy)
Напишіть клас Proxy, який приймає на вхід об'єкт і переадресовує виклики методів цього об'єкта,
додатково логуючи виклики (наприклад, виводячи назву методу та аргументи)
"""


class Proxy:
    """
    Клас Proxy для логування викликів методів об'єкта
    """

    def __init__(self, obj):
        """
        Ініціалізація проксі з реальним об'єктом
        :param obj: Об'єкт, методи якого потрібно перехоплювати
        """
        self._obj = obj

    def __getattr__(self, name):
        """
        Перехоплює доступ до атрибутів та методів об'єкта
        :param name: Назва атрибута або методу
        :return: Перехоплений метод або атрибут
        """
        # Отримуємо метод або атрибут з об'єкта
        attr = getattr(self._obj, name)

        # Якщо це метод, логуємо його виклик та аргументи
        if callable(attr):
            def logged(*args, **kwargs):
                print(f"Calling method:\n{name} with args: {args}")
                return attr(*args, **kwargs)

            return logged
        else:
            return attr


# Клас для тестування
class MyClass:
    def greet(self, name):
        return f"Hello, {name}!"


# Приклад використання Proxy
obj = MyClass()
proxy = Proxy(obj)

# Виклик методу через Proxy
print(proxy.greet("Alice"))
