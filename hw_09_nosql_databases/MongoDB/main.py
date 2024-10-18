"""
Основний модуль для запуску програми онлайн-магазину на основі MongoDB
"""

from datetime import datetime, timedelta
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
            f"\nЗамовлення #{order['order_number']} від {order['date'].strftime('%d.%m.%Y')} "
            f"клієнт {order['client']} купив:")
        for product in order['product_list']:
            print(f"- {product['name']} у кількості {product['quantity']} шт.")
        print(f"Загальна сума замовлення: {order['total_amount']} грн")

    # Виведення залишків на складі
    print(f"\nНа {datetime.now().strftime('%d.%m.%Y')} є залишки по таким позиціям:")
    for product in product_manager.products.find():
        print(f"Товар {product['name']} у кількості {product['stock']}")

    # Агрегація даних про продажі
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
    sold_products = order_manager.count_sold_products(start_date, end_date)
    print("\nЗагалом продано товарів по категоріям:")
    for category, products in sold_products.items():
        print(f"Категорія: {category}")
        for product_name, quantity in products.items():
            print(f"- {product_name} у кількості {quantity} шт.")

    # Загальна сума замовлень клієнтів
    client_totals = order_manager.calculate_total_amount_for_clients()
    print("\nЗагальна сума всіх замовлень в розрізі клієнтів:")
    for client, total in client_totals.items():
        print(f"Клієнт {client} замовив товарів на суму {total} грн")

    # Видалення недоступних продуктів
    product_manager.delete_unavailable_products()

except (ConnectionError, TimeoutError, ValueError) as e:
    print(f"Помилка під час виконання: {e}")
