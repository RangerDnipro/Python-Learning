"""
Модуль призначений для видобування інформації з сайту Вікіпедії
щодо 100 найрейтинговіших фільмів IMDb та акторів які в них знімались.
Отримана інформація використовується для початкового наповнення
бази даних kinobaza.db з таблицями movies, actors та movie_cast
"""

# pylint: disable=line-too-long

import re
import sqlite3
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class Actor:
    """
    Клас, що представляє актора
    :param name: Ім'я актора
    :param birth_year: Рік народження актора
    """

    def __init__(self, name: str, birth_year: int):
        self.name = name
        self.birth_year = birth_year

    def __repr__(self):
        """
        Повертає рядкове представлення об'єкта Actor
        :return: Рядкове представлення актора у форматі "Actor(name, birth_year)"
        """
        return f"Actor(name={self.name}, birth_year={self.birth_year})"


class Movie:
    """
    Клас, що представляє фільм
    :param title: Назва фільму
    :param release_year: Рік випуску фільму
    :param genre: Жанр фільму
    """

    def __init__(self, title: str, release_year: int, genre: str):
        self.title = title
        self.release_year = release_year
        self.genre = genre
        self.actors = []

    def add_actor(self, actor: Actor):
        """
        Додає актора до списку акторів фільму
        :param actor: Об'єкт Actor, який потрібно додати до списку акторів
        """
        self.actors.append(actor)

    def __repr__(self):
        """
        Повертає рядкове представлення об'єкта Movie
        :return: Рядкове представлення фільму у форматі "Movie(title, release_year, genre, actors)"
        """
        return f"Movie(title={self.title}, release_year={self.release_year}, genre={self.genre}, actors={self.actors})"


def fetch_page_content(url: str):
    """
    Завантажує HTML-контент сторінки за вказаним URL і повертає об'єкт BeautifulSoup
    :param url: URL веб-сторінки
    :return: Об'єкт BeautifulSoup або None, якщо сторінку не вдалося завантажити
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Помилка при завантаженні сторінки {url}: {e}")
        return None


def get_movie_genre(infobox) -> str:
    """
    Витягує жанр фільму зі сторінки
    :param infobox: Об'єкт BeautifulSoup, що містить інфобокс фільму
    :return: Жанр фільму або None, якщо не вдалося знайти жанр
    """
    genre_row = infobox.find('th', string=lambda text: text in ['Жанр', 'Жанри'])
    if genre_row and genre_row.find_next_sibling('td'):
        return genre_row.find_next_sibling('td').get_text(strip=True)
    return None


def get_movie_actors(infobox, actors_cache: dict) -> list:
    """
    Витягує список акторів зі сторінки фільму
    :param infobox: Об'єкт BeautifulSoup, що містить інфобокс фільму
    :param actors_cache: Словник з кешованими акторами для уникнення повторних запитів
    :return: Список об'єктів Actor
    """
    actors = []
    all_th = infobox.find_all('th')
    for th in all_th:
        if re.search(r'У головних\s*ролях', th.get_text(separator=' ', strip=True), re.IGNORECASE):
            actors_row = th
            if actors_row.find_next_sibling('td'):
                actors_links = actors_row.find_next_sibling('td').find_all('a')
                for actor_link in actors_links:
                    if ('wikidata.org' in actor_link.get('href', '') or
                            re.match(r'\[\d+\]|\[…\]|\[en\]', actor_link.get_text(strip=True)) or
                            'ще не написана' in actor_link.get('title', '')):
                        continue
                    actor_url = actor_link.get('href')
                    if actor_url in actors_cache:
                        actor = actors_cache[actor_url]
                    else:
                        actor = get_actor_details(actor_url)
                        actors_cache[actor_url] = actor

                    if actor.birth_year is not None and actor.name is not None:
                        actors.append(actor)
            break
    return actors


def get_movie_details(movie_url: str, actors_cache: dict) -> Movie:
    """
    Витягує деталі фільму, включаючи жанр та список акторів, зі сторінки фільму
    :param movie_url: URL сторінки фільму
    :param actors_cache: Словник з кешованими акторами для уникнення повторних запитів
    :return: Об'єкт Movie або None, якщо не вдалося отримати інформацію
    """
    movie_soup = fetch_page_content(f"https://uk.wikipedia.org{movie_url}")
    if not movie_soup:
        return None

    infobox = movie_soup.find('table', {'class': 'infobox'})
    if not infobox:
        return None

    # Отримуємо жанр фільму
    genre = get_movie_genre(infobox)

    # Отримуємо список акторів
    actors = get_movie_actors(infobox, actors_cache)

    # Визначення жанру фільму за заданими критеріями
    genre_mapping = [
        ('Фантастика', ['фантаст', 'пригоди,екшн', 'супергерой']),
        ('Гангстерский', ['гангстер', 'фільм-біографія']),
        ('Історичний', ['істор', "альтернативна історія", "історія,драма"]),
        ('Фентезі', ['фентез']),
        ('Вестерн', ['вестерн']),
        ('Мелодрама', ['мелодрам']),
        ('Трилер', ['трилер']),
        ('Пригодницький', ['пригодниц']),
        ('Детектив', ['детектив']),
        ('Трагедія', ['трагедія']),
        ('Мюзикл', ['мюзикл']),
        ('Драма', ['драма']),
        ('Комедія', ['комедія', "комп'ютерна анімація"])
    ]

    # Призначаємо жанр фільму за ключовими словами
    for mapped_genre, keywords in genre_mapping:
        for keyword in keywords:
            if genre and keyword.lower() in genre.lower():
                genre = mapped_genre
                break
        if genre == mapped_genre:
            break

    if genre is not None and actors:
        movie = Movie(title="", release_year=0, genre=genre)
        for actor in actors:
            movie.add_actor(actor)
        return movie
    return None


def get_actor_details(actor_url: str) -> Actor:
    """
    Витягує деталі актора, включаючи його ім'я та рік народження
    :param actor_url: URL сторінки актора
    :return: Об'єкт Actor або Actor(None, None), якщо інформацію не вдалося отримати
    """
    actor_soup = fetch_page_content(f"https://uk.wikipedia.org{actor_url}")
    if not actor_soup:
        return Actor(None, None)

    actor_name_tag = actor_soup.find('h1', {'id': 'firstHeading', 'class': 'firstHeading'})
    if actor_name_tag:
        actor_name = actor_name_tag.find('span', {'class': 'mw-page-title-main'}).get_text(strip=True) \
            if actor_name_tag.find('span', {'class': 'mw-page-title-main'}) else None
    else:
        actor_name = None

    actor_infobox = actor_soup.find('table', {'class': 'infobox'})
    birth_year = None
    if actor_infobox:
        birth_row = actor_infobox.find('th', string=lambda text: text in ['Дата народження', 'Народився', 'Народилася'])
        if birth_row and birth_row.find_next_sibling('td'):
            birth_date_text = birth_row.find_next_sibling('td').get_text(separator=' ', strip=True)
            birth_year_match = re.search(r'\b(\d{4})\b', birth_date_text)
            if birth_year_match:
                birth_year = int(birth_year_match.group(1))

    return Actor(actor_name, birth_year)


def create_tables(cursor):
    """
    Створює необхідні таблиці в базі даних, якщо вони ще не існують
    :param cursor: Об'єкт курсору SQLite для виконання SQL-запитів
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        release_year INTEGER,
        genre TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS actors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        birth_year INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movie_cast (
        movie_id INTEGER,
        actor_id INTEGER,
        PRIMARY KEY (movie_id, actor_id),
        FOREIGN KEY (movie_id) REFERENCES movies(id),
        FOREIGN KEY (actor_id) REFERENCES actors(id)
    )
    ''')


def add_movie_to_db(cursor, movie: Movie) -> int:
    """
    Додає фільм до бази даних і повертає його ідентифікатор
    :param cursor: Об'єкт курсору SQLite для виконання SQL-запитів
    :param movie: Об'єкт Movie, що представляє фільм
    :return: Ідентифікатор доданого фільму
    """
    cursor.execute('''
    INSERT INTO movies (title, release_year, genre)
    VALUES (?, ?, ?)
    ''', (movie.title, movie.release_year, movie.genre))
    return cursor.lastrowid


def add_actors_to_db(cursor, movie_id: int, actors: list):
    """
    Додає акторів до бази даних і встановлює зв'язки між акторами та фільмом
    :param cursor: Об'єкт курсору SQLite для виконання SQL-запитів
    :param movie_id: Ідентифікатор фільму
    :param actors: Список об'єктів Actor, що представляють акторів
    """
    for actor in actors:
        cursor.execute('''
        SELECT id FROM actors WHERE name = ? AND birth_year = ?
        ''', (actor.name, actor.birth_year))
        actor_record = cursor.fetchone()
        if actor_record:
            actor_id = actor_record[0]
        else:
            cursor.execute('''
            INSERT INTO actors (name, birth_year)
            VALUES (?, ?)
            ''', (actor.name, actor.birth_year))
            actor_id = cursor.lastrowid

        try:
            cursor.execute('''
            INSERT INTO movie_cast (movie_id, actor_id)
            VALUES (?, ?)
            ''', (movie_id, actor_id))
        except sqlite3.IntegrityError:
            print(f"Помилка: Неможливо додати актор з id {actor_id} для фільму з id {movie_id}, запис уже існує.")


def scrape_top_100_movies(url: str, db_file: str) -> None:
    """
    Завантажує інформацію про перші 100 фільмів зі списку IMDb та зберігає її в базу даних
    :param url: URL веб-сторінки з переліком фільмів
    :param db_file: Шлях до файлу бази даних SQLite
    :return: None
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Помилка при завантаженні сторінки {url}: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'sortable'})
    # У виборці 110 фільмів, тому що 10 не оформлені належним чином, щоб дістати інформацію
    rows = table.find_all('tr')[1:111]

    actors_cache = {}

    # Підключення до бази даних
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Створення таблиць
    create_tables(cursor)

    for row in tqdm(rows, desc="Завантаження фільмів", unit="фільм"):
        cells = row.find_all('td')
        if len(cells) < 5:
            continue

        title = re.sub(r'\s{2,}', ' ', cells[1].get_text(strip=True))
        year = int(cells[3].get_text(strip=True))
        movie_url = cells[1].find('a')['href']

        movie_details = get_movie_details(movie_url, actors_cache)
        if movie_details:
            movie = Movie(title=title, release_year=year, genre=movie_details.genre)
            movie.actors = movie_details.actors

            # Додавання фільму та акторів до бази даних
            movie_id = add_movie_to_db(cursor, movie)
            add_actors_to_db(cursor, movie_id, movie.actors)

    # Збереження змін та закриття з'єднання
    conn.commit()
    conn.close()
    print(f"Дані успішно збережено до {db_file}")


if __name__ == "__main__":
    scrape_top_100_movies(
        "https://uk.wikipedia.org/wiki/Список_250_найрейтинговіших_фільмів_IMDb",
        "kinobaza.db"
    )
