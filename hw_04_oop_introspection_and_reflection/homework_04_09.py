"""
Завдання 9: Динамічне додавання властивостей
Напишіть клас DynamicProperties, в якому можна динамічно додавати властивості через методи. Використовуйте вбудовані
функції property() для створення геттера та сеттера під час виконання програми.
"""


class DynamicProperties:
    """
    Клас, що дозволяє динамічно додавати властивості до об'єкта під час виконання програми
    Властивості створюються з використанням вбудованої функції property(),
    що надає геттери та сеттери для роботи з динамічними атрибутами
    """

    def __init__(self):
        """
        Ініціалізує об'єкт з порожнім словником для зберігання динамічних властивостей
        Всі властивості будуть зберігатись у словнику _properties
        """
        self._properties = {}

    def add_property(self, property_name, default_value=None):
        """
        Додає нову властивість до об'єкта динамічно
        :param property_name: Назва властивості, яку буде додано
        :param default_value: Значення за замовчуванням для нової властивості (необов'язковий параметр)
        Після виклику цього методу, до об'єкта можна звертатися за назвою властивості, яку було додано
        Властивість буде доступна як для читання, так і для запису
        """

        # Геттер для властивості
        def getter(instance):
            return instance._properties.get(property_name, default_value)

        # Сеттер для властивості
        def setter(instance, value):
            instance._properties[property_name] = value

        # Створюємо властивість за допомогою функції property()
        prop = property(fget=getter, fset=setter)

        # Додаємо властивість до класу
        setattr(self.__class__, property_name, prop)


# Приклад використання
obj = DynamicProperties()

# Додаємо властивість "name" з початковим значенням "default_name"
obj.add_property('name', 'default_name')

# Отримуємо значення властивості
print(obj.name)

# Змінюємо значення властивості
obj.name = "Python"
print(obj.name)
