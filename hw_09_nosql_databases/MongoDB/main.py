"""
Основний модуль для запуску програми онлайн-магазину на основі MongoDB
"""

from datetime import datetime
from pymongo import MongoClient
from product_manager import ProductManager
from order_manager import OrderManager

# Приклад використання
store_db = MongoClient("mongodb://localhost:27017/")["online_store"]
product_manager = ProductManager(store_db)
order_manager = OrderManager(store_db, product_manager)

try:
    # Створення колекцій
    product_manager.create_indexes()

    # Очищення колекцій перед завантаженням даних
    product_manager.products.delete_many({})
    order_manager.orders.delete_many({})

    # Завантаження продуктів з файлу
    product_manager.load_products_from_file('products.json')

    # Завантаження замовлень з файлу
    order_manager.load_orders_from_file('orders.json')

    # Отримання замовлень за останні 30 днів
    recent_orders = order_manager.get_recent_orders()
    for order in recent_orders:
        print(
            f"\n{order['date'].strftime('%d.%m.%Y')} клієнт {order['client']} "
            f"згідно замовлення {order['order_number']} купив:")
        for product in order['product_list']:
            print(f"Товар {product['name']} у кількості {product['quantity']}")
        print(f"Загальна сума замовлення: {order['total_amount']}")

    # Видалення недоступних продуктів
    product_manager.delete_unavailable_products()

    # Виведення залишків на складі
    print(f"\nНа {datetime.now().strftime('%d.%m.%Y')} є залишки по таким позиціям:")
    for product in product_manager.products.find():
        print(f"Товар {product['name']} у кількості {product['stock']}")
except (ConnectionError, TimeoutError, ValueError) as e:
    print(f"Помилка під час виконання: {e}")
