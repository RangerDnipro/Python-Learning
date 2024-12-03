"""
Парсить HTML-сторінки та витягує новини (назва, дата, посилання, короткий опис)
"""

from bs4 import BeautifulSoup


class Parser:
    """
    Клас для парсингу новин зі сторінок
    """

    def __init__(self, network):
        """
        Ініціалізує Parser з об'єктом Network
        :param network: Об'єкт Network для завантаження сторінок
        """
        self.network = network

    def get_summary_from_link(self, link: str) -> str:
        """
        Отримує короткий опис (summary) зі сторінки новини за її посиланням
        :param link: URL сторінки новини
        :return: Короткий опис новини або 'N/A', якщо не вдалося знайти
        """
        soup = self.network.get_page(link)
        if soup is None:
            return 'N/A'

        meta_tag = soup.find('meta', property='og:description')
        return meta_tag['content'].strip() if meta_tag and meta_tag.has_attr('content') else 'N/A'

    def parse_news(self, soup: BeautifulSoup) -> list[dict[str, str]]:
        """
        Парсить HTML-код сторінки для витягання новин
        :param soup: BeautifulSoup об'єкт з HTML-кодом сторінки
        :return: Список словників, кожен з яких містить інформацію про новину
        """
        news_list = []
        if soup is None:
            return news_list

        news_items = soup.find_all('li', class_='bbc-t44f9r')
        for item in news_items:
            title_tag = item.find('a', class_='bbc-uk8dsi')
            date_tag = item.find('time')

            title = title_tag.text.strip() if title_tag else 'N/A'
            link = title_tag['href'] if title_tag else 'N/A'
            link = f"https://www.bbc.com{link}" if not link.startswith("http") else link
            date = date_tag.text.strip() if date_tag else 'N/A'
            summary = self.get_summary_from_link(link) if link != 'N/A' else 'N/A'

            news_list.append({'title': title, 'link': link, 'date': date, 'summary': summary})

        return news_list
