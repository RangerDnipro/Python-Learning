"""
Завдання 9. Порівняння сеттерів/геттерів, декоратора @property та дескрипторів
Реалізуйте клас Product, який представляє товар з наступними атрибутами:
1.	name – назва товару (рядок).
2.	price – ціна товару (число з плаваючою комою).
Вам потрібно реалізувати три варіанти роботи з атрибутом price:
1.	Сеттери/геттери: реалізуйте методи get_price() і set_price(), які будуть дозволяти отримувати та встановлювати
значення атрибута price. Додайте перевірку, що ціна не може бути від'ємною. Якщо ціна менше ніж 0, викиньте виняток ValueError.
2.	Декоратор @property: використайте декоратор @property для створення властивості price. Також реалізуйте перевірку
на від'ємне значення ціни.
3.	Дескриптори: створіть окремий клас дескриптора PriceDescriptor, який буде контролювати встановлення та отримання ціни.
Додайте до класу Product атрибут price, що використовує дескриптор для перевірки ціни.

Завдання:
1.	Реалізуйте всі три класи: ProductWithGetSet, ProductWithProperty та ProductWithDescriptor.
2.	Напишіть тестову програму, яка створює об'єкти кожного з цих класів та намагається:
-	Отримати та змінити ціну товару.
-	Встановити від'ємне значення ціни та впевнитись, що воно правильно обробляється (викидання ValueError).
3.	Порівняйте переваги та недоліки кожного з підходів (сеттери/геттери, @property, дескриптори).
Напишіть висновок, який підхід більш зручний у вашому випадку та чому.

Додаткове завдання (опціонально):

4.	Для класу з дескриптором додайте можливість встановлення значень ціни в євро або доларах
(через додатковий атрибут валюти), використовуючи ще один дескриптор для конвертації валют.
"""


class ProductWithGetSet:
    """
    Клас ProductWithGetSet представляє товар з можливістю встановлення та отримання ціни
    через сеттери/геттери.
    """

    def __init__(self, name, price):
        """
        Ініціалізує продукт з назвою та ціною
        :param name: Назва товару
        :param price: Початкова ціна товару
        """
        self.name = name
        self.price = price

    def get_price(self):
        """
        Повертає ціну товару
        :return: Ціна товару
        """
        return self.price

    def set_price(self, price):
        """
        Встановлює нову ціну товару. Якщо ціна від'ємна, викидається ValueError
        :param price: Нова ціна
        :raises ValueError: Якщо ціна менша за 0
        """
        if price < 0:
            raise ValueError("Ціна не може бути від'ємною")
        self.price = price

    def __repr__(self):
        """
        Повертає рядкове представлення об'єкта ProductWithGetSet
        :return: Назва товару та його ціна у вигляді рядка
        """
        return f"ProductWithGetSet {self.name} {self.price}"


class ProductWithProperty:
    """
    Клас ProductWithProperty представляє товар з використанням декоратора @property
    для роботи з атрибутом ціни
    """

    def __init__(self, name, price):
        """
        Ініціалізує продукт з назвою та ціною.
        :param name: Назва товару
        :param price: Початкова ціна товару
        """
        self.name = name
        # Зберігаємо фактичне значення ціни
        self._price = price

    @property
    def price(self):
        """
        Повертає ціну товару.
        :return: Ціна товару
        """
        return self._price

    @price.setter
    def price(self, value):
        """
        Встановлює нову ціну товару. Якщо ціна від'ємна, викидається ValueError
        :param value: Нова ціна
        :raises ValueError: Якщо ціна менша за 0
        """
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною")
        self._price = value

    def __repr__(self):
        """
        Повертає рядкове представлення об'єкта ProductWithProperty
        :return: Назва товару та його ціна у вигляді рядка
        """
        return f"ProductWithProperty {self.name} {self._price}"


class PriceDescriptor:
    """
    Дескриптор PriceDescriptor забезпечує контроль за встановленням та отриманням ціни
    """

    def __set__(self, instance, value):
        """
        Встановлює значення ціни для інстансу класу. Якщо ціна від'ємна, викидається ValueError
        :param instance: Об'єкт класу, до якого застосовується дескриптор
        :param value: Значення ціни
        :raises ValueError: Якщо ціна менша за 0
        """
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною")
        instance.__dict__['price'] = value

    def __get__(self, instance, owner):
        """
        Повертає значення ціни з інстансу класу
        :param instance: Об'єкт класу, до якого застосовується дескриптор
        :param owner: Власник класу
        :return: Значення ціни
        """
        return instance.__dict__.get('price')


class ProductWithDescriptor:
    """
    Клас ProductWithDescriptor використовує дескриптор для керування атрибутом ціни
    """

    price = PriceDescriptor()  # Використовуємо дескриптор для атрибута price

    def __init__(self, name, price):
        """
        Ініціалізує продукт з назвою та ціною
        :param name: Назва товару
        :param price: Початкова ціна товару
        """
        self.name = name
        self.price = price

    def __repr__(self):
        """
        Повертає рядкове представлення об'єкта ProductWithDescriptor
        :return: Назва товару та його ціна у вигляді рядка
        """
        return f"ProductWithDescriptor {self.name} {self.price}"


# Тестування ProductWithGetSet
my_product = ProductWithGetSet("Телефон", 1000)
print(my_product)
# Зміна ціни через сеттер
ProductWithGetSet.set_price(my_product, 1500)
print(my_product)

# Тестування ProductWithProperty
my_product = ProductWithProperty("Комп'ютер", 2000)
print(my_product)
# Зміна ціни через властивість
my_product.price = 2500
print(my_product)

# Тестування ProductWithDescriptor
my_product = ProductWithDescriptor("Ноутбук", 1500)
print(my_product)
# Зміна ціни через дескриптор
my_product.price = 2000
print(my_product)
