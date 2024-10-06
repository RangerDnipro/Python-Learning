import xml.etree.ElementTree as ET
import json


class XMLJSONConverter:
    """
    Клас для конвертації XML у JSON та JSON у XML
    """

    def xml_to_json(self, xml_file, json_file):
        """
        Ця функція зчитує XML-файл, перетворює його у формат JSON і записує результат у визначений JSON-файл
        :param xml_file: Шлях до XML-файлу, який потрібно перетворити
        :param json_file: Шлях до JSON-файлу, де буде збережено результат
        """

        tree = ET.parse(xml_file)
        root = tree.getroot()

        def parse_element(element):
            """
            Допоміжна функція для перетворення елементів XML у словник
            :param element: XML-елемент для обробки
            :return: Словник, що містить теги та значення дочірніх елементів
            """
            parsed_data = {}
            for child in element:
                parsed_data[child.tag] = child.text
            return parsed_data

        data = [parse_element(product) for product in root.findall('товар')]

        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def json_to_xml(self, json_file, xml_file, root_element="магазин"):
        """
        Ця функція зчитує JSON-файл, перетворює його у формат XML і записує результат у визначений XML-файл
        :param json_file: Шлях до JSON-файлу, який потрібно перетворити
        :param xml_file: Шлях до XML-файлу, де буде збережено результат
        :param root_element: Назва кореневого елементу для XML-файлу (за замовчуванням "магазин")
        """

        with open(json_file, mode='r', encoding='utf-8') as file:
            json_data = json.load(file)

        root = ET.Element(root_element)

        def build_xml_tree(data, parent):
            """
            Допоміжна функція для створення XML-дерева на основі даних з JSON
            :param data: Дані у форматі словника або списку
            :param parent: Батьківський елемент, до якого додаються дочірні елементи
            """
            if isinstance(data, dict):
                for key, value in data.items():
                    child = ET.SubElement(parent, key)
                    child.text = str(value)
            elif isinstance(data, list):
                for item in data:
                    item_element = ET.SubElement(parent, "товар")
                    build_xml_tree(item, item_element)

        build_xml_tree(json_data, root)

        tree = ET.ElementTree(root)
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
