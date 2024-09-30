"""
Завдання 5: Модифікація атрибутів під час виконання
Напишіть клас MutableClass, який має методи для динамічного додавання та видалення атрибутів об'єкта.
Реалізуйте методи add_attribute(name, value) та remove_attribute(name).
"""


class MutableClass:
    """
    Клас, що дозволяє динамічно додавати та видаляти атрибути об'єкта
    """

    def add_attribute(self, name, value):
        """
        Додає новий атрибут до об'єкта
        :param name: Назва атрибута
        :param value: Значення атрибута
        """
        setattr(self, name, value)

    def remove_attribute(self, name):
        """
        Видаляє атрибут з об'єкта, якщо він існує
        :param name: Назва атрибута
        """
        if hasattr(self, name):
            delattr(self, name)
        else:
            raise AttributeError(f"Атрибут '{name}' не існує")


# Приклад виконання програми
obj = MutableClass()

# Додавання атрибута
obj.add_attribute("name", "Python")
print(obj.name)

# Видалення атрибута
obj.remove_attribute("name")

# Спроба звернутися до видаленого атрибуту призведе до помилки
try:
    print(obj.name)
except AttributeError as e:
    print(e)
