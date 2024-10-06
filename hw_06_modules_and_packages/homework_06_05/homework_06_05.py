"""
Завдання 5: Робота з XML
Створи XML-файл, що містить інформацію про продукти магазину:
Назва продукту Ціна Кількість на складі

<products>
    <product>
        <name>Молоко</name>
        <price>25</price>
        <quantity>50</quantity>
    </product>
    <product>
        <name>Хліб</name>
        <price>10</price>
        <quantity>100</quantity>
    </product>
</products>

2.Напиши програму, яка:
Читає XML-файл і виводить назви продуктів та їхню кількість.
Змінює кількість товару та зберігає зміни в XML-файл.
"""

import xml.etree.ElementTree as ET
import os


def create_xml_file(filename):
    """
    Створюємо XML-файл з даними про продукти, якщо він не існує
    :param filename: Ім'я файлу для створення
    """
    if not os.path.exists(filename):
        products = ET.Element("products")

        # Продукт 1: Молоко
        product1 = ET.SubElement(products, "product")
        ET.SubElement(product1, "name").text = "Молоко"
        ET.SubElement(product1, "price").text = "25"
        ET.SubElement(product1, "quantity").text = "50"

        # Продукт 2: Хліб
        product2 = ET.SubElement(products, "product")
        ET.SubElement(product2, "name").text = "Хліб"
        ET.SubElement(product2, "price").text = "10"
        ET.SubElement(product2, "quantity").text = "100"

        tree = ET.ElementTree(products)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"Файл {filename} створено.")
    else:
        print(f"Файл {filename} вже існує.")


def read_products(filename):
    """
    Читаємо XML-файл і виводить назви продуктів та їх кількість
    :param filename: Ім'я файлу для зчитування
    """
    tree = ET.parse(filename)
    root = tree.getroot()

    print("Список продуктів та їх кількість:")
    for product in root.findall("product"):
        name = product.find("name").text
        quantity = product.find("quantity").text
        print(f"{name}: {quantity} шт.")


def update_product_quantity(filename, product_name, new_quantity):
    """
    Оновлюємо кількість товару у файлі XML та зберігає зміни
    :param filename: Ім'я файлу, в якому треба оновити кількість товару
    :param product_name: Назва продукту, кількість якого треба змінити
    :param new_quantity: Нова кількість товару
    """
    tree = ET.parse(filename)
    root = tree.getroot()

    for product in root.findall("product"):
        name = product.find("name").text
        if name == product_name:
            product.find("quantity").text = str(new_quantity)
            print(f"Кількість товару '{product_name}' оновлено до {new_quantity} шт.")
            tree.write(filename, encoding="utf-8", xml_declaration=True)
            return
    # Якщо такого продукту нема в .xml файлі, виводимо повідомлення
    print(f"Продукт '{product_name}' не знайдено у файлі.")


if __name__ == "__main__":
    filename = "homework_06_05.xml"

    # Створюємо XML-файл, якщо він не існує
    create_xml_file(filename)

    # Читаємо та виводимо інформацію про продукти
    read_products(filename)

    # Оновлюємо кількість товару
    update_product_quantity(filename, "Молоко", 60)

    # Перевіряємо зміни
    read_products(filename)
