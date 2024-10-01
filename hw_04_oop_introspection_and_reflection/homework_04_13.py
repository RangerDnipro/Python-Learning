"""
Завдання 13: Автоматична генерація методів для полів класу (опціонально)
Реалізуйте метаклас AutoMethodMeta, який автоматично генерує методи геттера та сеттера для кожного атрибута класу.
Метод повинен починатися з get_<attribute>() та set_<attribute>(value).
"""


class AutoMethodMeta(type):
    """
    Метаклас AutoMethodMeta автоматично створює геттери та сеттери для атрибутів класу
    Геттер має формат: get_<attribute>(), а сеттер - set_<attribute>(value)
    """

    def __new__(cls, name, bases, class_dict):
        """
        Створює новий клас з автоматично генерованими геттерами та сеттерами для атрибутів класу
        :param cls: Метаклас, що створює новий клас
        :param name: Назва класу
        :param bases: Базові класи
        :param class_dict: Словник атрибутів класу
        :return: Новий клас з геттерами та сеттерами для атрибутів класу
        """
        # Створюємо копію атрибутів класу для уникнення помилки зміни словника під час ітерації
        attr_names = [attr for attr in class_dict if not attr.startswith('__')]

        # Після ітерації додаємо геттери і сеттери для кожного атрибута класу
        for attr_name in attr_names:
            getter_name = f"get_{attr_name}"
            setter_name = f"set_{attr_name}"

            # Створюємо геттери і сеттери для атрибутів класу
            class_dict[getter_name] = cls.create_class_getter(attr_name)
            class_dict[setter_name] = cls.create_class_setter(attr_name)

        return super().__new__(cls, name, bases, class_dict)

    @staticmethod
    def create_class_getter(attr_name):
        """
        Створює геттер для атрибута класу
        :param attr_name: Назва атрибута
        :return: Геттер-функція для атрибута класу
        """

        def getter(cls):
            return getattr(cls, attr_name)

        return getter

    @staticmethod
    def create_class_setter(attr_name):
        """
        Створює сеттер для атрибута класу
        :param attr_name: Назва атрибута
        :return: Сеттер-функція для атрибута класу
        """

        def setter(cls, value):
            setattr(cls, attr_name, value)

        return setter


# Тестування метакласу AutoMethodMeta з атрибутами класу
class Person(metaclass=AutoMethodMeta):
    """
    Клас Person використовує метаклас AutoMethodMeta, який автоматично створює
    геттери та сеттери для атрибутів класу
    """
    name = "John"
    age = 30


# Створення об'єкта класу Person і тестування автоматично створених методів
p = Person()
print(p.get_name())
p.set_age(31)
print(p.get_age())
