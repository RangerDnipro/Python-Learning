import csv
import json


class CSVJSONConverter:
    """
    Клас для перетворення CSV-файлу в JSON та JSON в CSV
    """

    def csv_to_json(self, csv_file, json_file):
        """
        Перетворює CSV-файл у JSON і зберігає результат у json_file
        :param csv_file: Шлях до CSV-файлу
        :param json_file: Шлях для збереження JSON-файлу
        """
        data = []
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def json_to_csv(self, json_file, csv_file):
        """
        Перетворює JSON-файл у CSV
        :param json_file: Шлях до JSON-файлу
        :param csv_file: Шлях для збереження CSV-файлу
        """
        with open(json_file, mode='r', encoding='utf-8') as file:
            data = json.load(file)

        # Створюємо повний список ключів
        fieldnames = data[0].keys()

        # Записуємо дані у CSV
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
