"""
Завдання 10: Створення товарів для онлайн-магазину
Розробити програму для управління товарами в онлайн-магазині, використовуючи карирувані функції.
1.	Написати функцію create_product, яка приймає назву, ціну та кількість товару.
2.	Використати замикання для створення функції, яка дозволяє змінювати ціну товару.
"""

# Глобальна змінна асортименту магазину
products = {}


# Функція для створення товару з карируванням
def create_product(name):
    """
    Функція для створення товару.
    
    Параметри:
    name (str): Назва товару.
    
    Повертає:
    function: Функцію для встановлення ціни.
    """
    def set_price(price):
        """
        Встановлює ціну товару.
        
        Параметри:
        price (float): Ціна товару.
        
        Повертає:
        function: Функцію для встановлення кількості.
        """
        def set_quantity(quantity):
            """
            Встановлює кількість товару.
            
            Параметри:
            quantity (int): Кількість товару.
            """
            if name not in products:
                products[name] = {'price': price, 'quantity': quantity}
                print(f"Товар '{name}' створено з ціною {price} та кількістю {quantity}")
            else:
                print(f"Товар '{name}' не було створено бо він вже є в базі")

        return set_quantity

    return set_price


# Функція для зміни ціни товару
def change_price(name):
    """
    Функція для зміни ціни існуючого товару.
    
    Параметри:
    name (str): Назва товару.
    
    Повертає:
    function: Функцію для встановлення нової ціни.
    """
    def set_new_price(new_price):
        """
        Встановлює нову ціну товару.
        
        Параметри:
        new_price (float): Нова ціна товару.
        
        Повертає:
        str: Повідомлення про успішну зміну ціни або про помилку.
        """
        if name in products:
            old_price = products[name]['price']
            products[name]['price'] = new_price
            return f"Ціна товару '{name}' змінена з {old_price} на {new_price}"
        else:
            return f"Товар '{name}' не знайдено"

    return set_new_price


# Приклад використання
create_product('Навушники')(1000)(15)
create_product('Телефон')(10000)(10)
create_product('Ноутбук')(25000)(5)
# Перевірка на дубль
create_product('Навушники')(900)(10)

print()
# Виводимо повну інформацію про товари
for product in products:
    print(
        f"В наявності є товар '{product}' з ціною {products[product]['price']} у кількості {products[product]['quantity']}")

print()
# Змінюємо ціну товару 'Ноутбук'
set_laptop_price = change_price('Ноутбук')
print(set_laptop_price(30000))

print()
# Виводимо оновлену інформацію про товари
for product in products:
    print(
        f"В наявності є товар '{product}' з ціною {products[product]['price']} у кількості {products[product]['quantity']}")
