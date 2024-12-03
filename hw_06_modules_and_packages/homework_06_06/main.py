"""
Додаткове завдання 1. Перетворення між форматами:
Реалізуй класи, які перетворюватимуть CSV-файл до JSON та навпаки.
Додай функціонал для перетворення XML-файлу до JSON.

Щоб було цікавіше, реалізуємо ланцюжок трансформацій файлу с товарами та їх характеристиками за шляхом
XML в JSON -> JSON в CSV -> CSV в JSON -> JSON в XML
Для реалізації цього завдання створюємо Python-пакет із наступною структурою:

homework_06_06/
├── data_converter/
│   ├── __init__.py
│   ├── csv_json_converter.py
│   ├── xml_json_converter.py
│   └── xml_creator.py
└── main.py
"""


def main():
    """
    Головна функція для демонстрації роботи функцій пакета
    Використовує методи для перетворень між XML, JSON і CSV
    """
    from data_converter import CSVJSONConverter, XMLJSONConverter, create_initial_xml

    # Створюємо початковий XML файл
    create_initial_xml('original_xml.xml')

    # Створюємо об'єкти конвертерів
    csv_json_converter = CSVJSONConverter()
    xml_json_converter = XMLJSONConverter()

    # Перетворення XML в JSON
    xml_json_converter.xml_to_json('original_xml.xml', 'xml_to_json.json')
    # Перетворення JSON в CSV
    csv_json_converter.json_to_csv('xml_to_json.json', 'json_to_csv.csv')
    # Перетворення CSV в JSON
    csv_json_converter.csv_to_json('json_to_csv.csv', 'csv_to_json.json')
    # Перетворення JSON в XML
    xml_json_converter.json_to_xml("csv_to_json.json", "json_to_xml.xml")


if __name__ == "__main__":
    main()
