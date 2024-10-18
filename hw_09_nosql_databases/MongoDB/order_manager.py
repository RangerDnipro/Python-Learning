"""
Модуль для управління замовленнями
"""

from datetime import datetime, timedelta
from typing import List, Dict
import json


class OrderManager:
    """
    Клас для управління замовленнями в базі даних онлайн-магазину на основі MongoDB
    """

    def __init__(self, db, product_manager):
        self.orders = db['orders']
        self.product_manager = product_manager

    def add_order(self, client: str, product_list: List[Dict[str, int]]):
        """
        Додає нове замовлення до колекції orders
        :param client: Ім'я клієнта
        :param product_list: Список продуктів із кількістю у вигляді словників
        """
        total_amount = 0
        for product in product_list:
            prod = self.product_manager.products.find_one({"name": product["name"]})
            if prod:
                if prod["stock"] < product["quantity"]:
                    print(f"Недостатньо товару {product['name']} на складі для замовлення {client}")
                    continue
                total_amount += prod["price"] * product["quantity"]
                # Оновлення кількості продукту на складі
                self.product_manager.products.update_one({"name": product["name"]},
                                                         {"$inc": {"stock": -product["quantity"]}})

        if total_amount > 0:
            order = {
                "order_number": self.orders.count_documents({}) + 1,
                "client": client,
                "product_list": product_list,
                "total_amount": total_amount,
                "date": datetime.now()
            }
            self.orders.insert_one(order)

    def get_recent_orders(self, days: int = 30) -> List[Dict]:
        """
        Витягує всі замовлення за останні вказані дні
        :param days: Кількість днів для фільтрації замовлень
        :return: Список замовлень
        """
        date_threshold = datetime.now() - timedelta(days=days)
        return list(self.orders.find({"date": {"$gte": date_threshold}}))

    def count_sold_products(self, start_date: datetime, end_date: datetime) -> int:
        """
        Порахує загальну кількість проданих продуктів за певний період часу
        :param start_date: Початкова дата періоду
        :param end_date: Кінцева дата періоду
        :return: Загальна кількість проданих продуктів
        """
        orders = self.orders.find({"date": {"$gte": start_date, "$lte": end_date}})
        total_sold = 0
        for order in orders:
            for product in order["product_list"]:
                total_sold += product["quantity"]
        return total_sold

    def calculate_total_amount_for_client(self, client: str) -> float:
        """
        Використовує агрегацію для підрахунку загальної суми всіх замовлень клієнта
        :param client: Ім'я клієнта
        :return: Загальна сума всіх замовлень клієнта
        """
        pipeline = [
            {"$match": {"client": client}},
            {"$group": {"_id": "$client", "total": {"$sum": "$total_amount"}}}
        ]
        result = list(self.orders.aggregate(pipeline))
        return result[0]["total"] if result else 0.0

    def load_orders_from_file(self, file_path: str):
        """
        Зчитує замовлення з JSON файлу та додає їх у базу даних
        :param file_path: Шлях до файлу з замовленнями
        """
        try:
            with open(file_path, 'r') as file:
                orders = json.load(file)
                for order in orders:
                    self.add_order(
                        client=order['client'],
                        product_list=order['product_list']
                    )
        except FileNotFoundError:
            print(f"Файл {file_path} не знайдено")
        except json.JSONDecodeError:
            print(f"Помилка при зчитуванні файлу {file_path}")
