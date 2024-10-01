"""
Завдання 14: Метаклас для перевірки типів полів (опціонально)
Задача: Реалізуйте метаклас TypeCheckedMeta, який перевіряє типи атрибутів при їх встановленні
Якщо тип значення не відповідає типовому опису, має виникати помилка
"""


class TypeCheckedMeta(type):
    """
    Метаклас TypeCheckedMeta перевіряє типи атрибутів при їх встановленні, використовуючи анотації типів
    """

    def __new__(cls, name, bases, class_dict):
        """
        Створює новий клас з перевіркою типів для атрибутів, використовуючи анотації типів
        :param name: Назва класу
        :param bases: Базові класи
        :param class_dict: Словник атрибутів класу
        :return: Новий клас
        """
        # Створюємо новий клас
        new_class = super().__new__(cls, name, bases, class_dict)

        # Зберігаємо оригінальний метод __setattr__ для подальшого використання
        original_setattr = new_class.__setattr__

        # Перевизначаємо __setattr__, щоб додати перевірку типів
        def __setattr__(self, key, value):
            # Перевіряємо, чи атрибут має анотацію типу
            if key in getattr(self.__class__, '__annotations__', {}):
                expected_type = self.__class__.__annotations__[key]
                # Перевіряємо, чи значення відповідає очікуваному типу
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Для атрибута '{key}' класу '{self.__class__.__name__}' "
                        f"очікується тип '{expected_type.__name__}', але отримано '{type(value).__name__}'.")

            # Викликаємо оригінальний метод __setattr__ для встановлення значення
            original_setattr(self, key, value)

        # Замінюємо __setattr__ в класі
        new_class.__setattr__ = __setattr__

        return new_class


# Тестування метакласу TypeCheckedMeta
class Person(metaclass=TypeCheckedMeta):
    """
    Клас Person з атрибутами 'name' (тип str) і 'age' (тип int)
    """
    name: str = ""
    age: int = 0


# Створюємо об'єкт класу Person
p = Person()

# Коректне встановлення значень
p.name = "John"
p.age = 30

# При неправильному типі буде помилка "Для атрибута 'age' класу 'Person' очікується тип 'int', але отримано 'str'"
try:
    p.age = "30"
except TypeError as e:
    print(e)
