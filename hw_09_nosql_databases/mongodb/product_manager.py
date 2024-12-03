"""
Модуль для управління продуктами
"""

import json
from pymongo import ASCENDING


class ProductManager:
    """
    Клас для управління продуктами в базі даних онлайн-магазину на основі MongoDB
    """

    def __init__(self, db):
        self.products = db['products']

    def add_product(self, name: str, price: float, category: str, stock: int):
        """
        Додає новий продукт до колекції products
        :param name: Назва продукту
        :param price: Ціна продукту
        :param category: Категорія продукту
        :param stock: Кількість продукту на складі
        """
        product = {
            "name": name,
            "price": price,
            "category": category,
            "stock": stock
        }
        self.products.insert_one(product)

    def delete_unavailable_products(self):
        """
        Видаляє продукти, які більше не доступні для продажу (кількість на складі дорівнює нулю)
        """
        unavailable_products = self.products.find({"stock": 0})
        for product in unavailable_products:
            print(f"\nТовар {product['name']} видалено, бо закінчився")
        self.products.delete_many({"stock": 0})

    def create_indexes(self):
        """
        Створює індекси для поля category в колекції products,
        щоб прискорити пошук продуктів по категоріях
        """
        self.products.create_index([("category", ASCENDING)])

    def load_products_from_file(self, file_path: str):
        """
        Зчитує продукти з JSON файлу та додає їх у базу даних
        :param file_path: Шлях до файлу з продуктами
        """
        try:
            with open(file_path, 'r', encoding='UTF-8') as file:
                products = json.load(file)
                for product in products:
                    self.add_product(
                        name=product['name'],
                        price=product['price'],
                        category=product['category'],
                        stock=product['stock']
                    )
        except FileNotFoundError:
            print(f"Файл {file_path} не знайдено")
        except json.JSONDecodeError:
            print(f"Помилка при зчитуванні файлу {file_path}")
