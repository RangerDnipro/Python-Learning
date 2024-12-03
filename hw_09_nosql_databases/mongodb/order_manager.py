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
        actual_product_list = []
        for product in product_list:
            prod = self.product_manager.products.find_one({"name": product["name"]})
            if prod:
                available_quantity = min(prod["stock"], product["quantity"])
                if available_quantity > 0:
                    total_amount += prod["price"] * available_quantity
                    # Оновлення кількості продукту на складі
                    self.product_manager.products.update_one(
                        {"name": product["name"]}, {"$inc": {"stock": -available_quantity}})
                    actual_product_list.append({"name": product["name"],
                                                "quantity": available_quantity})
                else:
                    print(f"Недостатньо товару {product['name']} на складі для замовлення {client}")

        if total_amount > 0:
            order = {
                "order_number": self.orders.count_documents({}) + 1,
                "client": client,
                "product_list": actual_product_list,
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

    def count_sold_products(self, start_date: datetime,
                            end_date: datetime) -> Dict[str, Dict[str, int]]:
        """
        Порахує загальну кількість проданих продуктів за певний період часу
        :param start_date: Початкова дата періоду
        :param end_date: Кінцева дата періоду
        :return: Словник категорій з товарами та їх кількістю
        """
        orders = self.orders.find({"date": {"$gte": start_date, "$lte": end_date}})
        sold_products = {}
        for order in orders:
            for product in order["product_list"]:
                product_info = self.product_manager.products.find_one({"name": product["name"]})
                if product_info:
                    category = product_info["category"]
                    if category not in sold_products:
                        sold_products[category] = {}
                    if product["name"] not in sold_products[category]:
                        sold_products[category][product["name"]] = 0
                    sold_products[category][product["name"]] += product["quantity"]
        return sold_products

    def calculate_total_amount_for_clients(self) -> Dict[str, float]:
        """
        Використовує агрегацію для підрахунку загальної суми всіх замовлень клієнтів
        :return: Словник клієнтів з загальною сумою їх замовлень
        """
        pipeline = [
            {"$group": {"_id": "$client", "total": {"$sum": "$total_amount"}}}
        ]
        results = list(self.orders.aggregate(pipeline))
        client_totals = {result["_id"]: result["total"] for result in results}
        return client_totals

    def load_orders_from_file(self, file_path: str):
        """
        Зчитує замовлення з JSON файлу та додає їх у базу даних
        :param file_path: Шлях до файлу з замовленнями
        """
        try:
            with open(file_path, 'r', encoding='UTF-8') as file:
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
