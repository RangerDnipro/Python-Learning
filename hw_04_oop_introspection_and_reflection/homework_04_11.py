class LimitedAttributesMeta(type):
    """
    Метаклас LimitedAttributesMeta обмежує кількість атрибутів, які можна додати до класу
    """

    def __new__(cls, name, bases, class_dict):
        """
        Створює новий клас і перевіряє кількість атрибутів у ньому
        Якщо атрибутів більше, ніж дозволено, викликається TypeError
        :param cls: Метаклас, що створює новий клас
        :param name: назва класу
        :param bases: Базові класи для нового класу
        :param class_dict: Словник атрибутів класу
        :return class_instance: Екземпляр створеного класу
        """

        # Обмеження на кількість атрибутів
        max_attrs = 3

        # Фільтруємо тільки користувацькі атрибути, без спеціальних методів або атрибутів
        attributes = {key: value for key, value in class_dict.items() if not key.startswith('__')}

        # Перевіряємо кількість атрибутів
        if len(attributes) > max_attrs:
            raise TypeError(f"Клас {name} не може мати більше {max_attrs} атрибутів.")

        # Створюємо клас через стандартний виклик type.__new__
        return super().__new__(cls, name, bases, class_dict)


# Тестування метакласу LimitedAttributesMeta
try:
    class LimitedClass(metaclass=LimitedAttributesMeta):
        attr1 = 1
        attr2 = 2
        attr3 = 3
        # Розкоментування attr4 викличе помилку:
        # TypeError: Клас LimitedClass не може мати більше 3 атрибутів.
        # attr4 = 4

    obj = LimitedClass()
    print(f"Об'єкт класу LimitedClass створено з атрибутами: attr1={obj.attr1}, attr2={obj.attr2}, attr3={obj.attr3}")

except TypeError as e:
    print(e)
