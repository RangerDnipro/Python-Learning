"""
Генерує звіт на основі новин, наприклад, кількість новин на день
"""


import pandas as pd


class Report:
    @staticmethod
    def generate_report(data: list[dict[str, str]]) -> None:
        df = pd.DataFrame(data)
        if 'date' in df.columns:
            report = df['date'].value_counts().sort_index()
            print(report)
        else:
            print("Немає даних для створення звіту")
