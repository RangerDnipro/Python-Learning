"""
Відповідає за фільтрацію новин на основі дати
"""

from datetime import datetime, timedelta


class Filtering:
    """
    Клас для фільтрації новин на основі їх дати публікації
    """

    @staticmethod
    def parse_date_ua(date_str: str) -> datetime:
        """
        Перетворює дату у форматі українською мовою у об'єкт datetime
        :param date_str: Дата у форматі, наприклад, "31 жовтня 2024"
        :return: Об'єкт datetime, що представляє вказану дату
        """
        month_map = {
            "січня": "01", "лютого": "02", "березня": "03",
            "квітня": "04", "травня": "05", "червня": "06",
            "липня": "07", "серпня": "08", "вересня": "09",
            "жовтня": "10", "листопада": "11", "грудня": "12"
        }
        parts = date_str.split()
        day = parts[0]
        month = month_map[parts[1].lower()]
        year = parts[2]
        return datetime.strptime(f"{day} {month} {year}", "%d %m %Y")

    @staticmethod
    def filter_news_by_date(data: list[dict[str, str]], days: int = 7) -> list[dict[str, str]]:
        """
        Фільтрує новини за вказану кількість днів від поточної дати
        :param data: Список новин для фільтрації. Новина представлена як словник з ключем 'date'
        :param days: Кількість днів для фільтрації (за замовчуванням 7 днів)
        :return: Список новин, опублікованих протягом вказаного періоду
        """
        filtered_news = []
        current_date = datetime.now()
        date_threshold = current_date - timedelta(days=days)

        for news in data:
            try:
                news_date = Filtering.parse_date_ua(news['date'])
                if news_date >= date_threshold:
                    filtered_news.append(news)
            except ValueError:
                continue

        return filtered_news
