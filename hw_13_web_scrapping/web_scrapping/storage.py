"""
Зберігає зібрані новини у CSV-файли
"""

import csv


class Storage:
    @staticmethod
    def save_to_csv(data: list[dict[str, str]], filename: str = 'news.csv') -> None:
        try:
            keys = data[0].keys() if data else []
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            print(f"Дані успішно збережено у файл {filename}")
        except IOError as e:
            print(f"Помилка збереження файлу: {e}")
