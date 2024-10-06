import xml.etree.ElementTree as ET


def create_initial_xml(file_name='original_xml.xml'):
    """
    Створює XML файл з товарами та зберігає його у file_name
    :param file_name: Шлях для збереження XML-файлу
    """
    # Створення словників для товарів
    iphone = {
        'назва': 'iPhone 16 Pro Max',
        'опис': 'Потужний смартфон Apple',
        'ціна': '75000',
        'виробник': 'Apple',
        'країна': 'США'
    }

    ecoflow = {
        'назва': 'EcoFlow River 2 Pro',
        'опис': 'Портативна зарядна станція',
        'ціна': '35000',
        'виробник': 'EcoFlow',
        'країна': 'Китай'
    }

    laptop = {
        'назва': 'Acer Aspire 5',
        'опис': 'Ноутбук для роботи та розваг',
        'ціна': '55000',
        'виробник': 'Acer',
        'країна': 'Тайвань'
    }

    # Створення кореневого елемента
    root = ET.Element('магазин')

    # Функція для створення елементів товару
    def create_product(product_dict):
        product = ET.SubElement(root, 'товар')
        for key, value in product_dict.items():
            sub_element = ET.SubElement(product, key)
            sub_element.text = str(value)
        return product

    # Створення елементів товарів
    create_product(iphone)
    create_product(ecoflow)
    create_product(laptop)

    # Запис XML файлу
    tree = ET.ElementTree(root)
    with open(file_name, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)

    print(f"Файл {file_name} створено")

