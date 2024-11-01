"""
Генерує звіт на основі новин, наприклад, кількість новин на день
"""

import pandas as pd


class Report:
    """
    Клас для генерації звіту на основі новин
    """

    @staticmethod
    def generate_report(data: list[dict[str, str]]) -> None:
        """
        Створює та виводить звіт з даних про новини
        Генерує звіт, що показує кількість новин на кожну дату, якщо в даних присутнє поле 'date'
        Якщо поле 'date' відсутнє, виводить повідомлення про неможливість створення звіту
        :param data: Список словників, що містять інформацію про новини
        :type data: list[dict[str, str]]
        :return: None
        """
        df = pd.DataFrame(data)
        if 'date' in df.columns:
            report = df['date'].value_counts().sort_index()
            print("\nНа відповідну дату є така кількість новин:")
            print(report)
        else:
            print("Немає даних для створення звіту")
