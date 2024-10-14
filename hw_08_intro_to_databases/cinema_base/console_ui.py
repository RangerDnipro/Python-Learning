"""
Модуль для взаємодії з користувачем з використанням класів
"""

import sqlite3
from database import *
from .search import search_movie_by_title, search_actor_by_name


class Movie:
    def __init__(self, title: str, release_year: int = None, genre: str = None, movie_id: int = None) -> None:
        """
        Ініціалізує екземпляр класу Movie
        :param title: Назва фільму
        :param release_year: Рік випуску фільму
        :param genre: Жанр фільму
        :param movie_id: Ідентифікатор фільму (за замовчуванням None)
        """
        self.id = movie_id
        self.title = title
        self.release_year = release_year
        self.genre = genre

    def save_to_db(self, cursor) -> None:
        """
        Зберігає або оновлює інформацію про фільм у базі даних
        :param cursor: Курсор бази даних для виконання SQL-запитів
        """
        if self.id is None:
            cursor.execute(
                'INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)',
                (self.title, self.release_year, self.genre)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                'UPDATE movies SET title = ?, release_year = ?, genre = ? WHERE id = ?',
                (self.title, self.release_year, self.genre, self.id)
            )

    @classmethod
    def get_from_db(cls, cursor, movie_id: int) -> 'Movie':
        """
        Отримує інформацію про фільм з бази даних за ідентифікатором
        :param cursor: Курсор бази даних для виконання SQL-запитів
        :param movie_id: Ідентифікатор фільму
        :return: Екземпляр класу Movie або None, якщо фільм не знайдено
        """
        cursor.execute('SELECT id, title, release_year, genre FROM movies WHERE id = ?', (movie_id,))
        row = cursor.fetchone()
        if row:
            return cls(movie_id=row[0], title=row[1], release_year=row[2], genre=row[3])
        return None


class Actor:
    def __init__(self, name: str, birth_year: int = None, actor_id: int = None) -> None:
        """
        Ініціалізує екземпляр класу Actor
        :param name: Ім'я актора
        :param birth_year: Рік народження актора (за замовчуванням None)
        :param actor_id: Ідентифікатор актора (за замовчуванням None)
        """
        self.id = actor_id
        self.name = name
        self.birth_year = birth_year

    def save_to_db(self, cursor) -> None:
        """
        Зберігає або оновлює інформацію про актора у базі даних
        :param cursor: Курсор бази даних для виконання SQL-запитів
        """
        if self.id is None:
            cursor.execute(
                'INSERT INTO actors (name, birth_year) VALUES (?, ?)',
                (self.name, self.birth_year)
            )
            self.id = cursor.lastrowid

    @classmethod
    def get_from_db(cls, cursor, actor_id: int) -> 'Actor':
        """
        Отримує інформацію про актора з бази даних за ідентифікатором
        :param cursor: Курсор бази даних для виконання SQL-запитів
        :param actor_id: Ідентифікатор актора
        :return: Екземпляр класу Actor або None, якщо актор не знайдений
        """
        cursor.execute('SELECT id, name, birth_year FROM actors WHERE id = ?', (actor_id,))
        row = cursor.fetchone()
        if row:
            return cls(actor_id=row[0], name=row[1], birth_year=row[2])
        return None


class CinemaBaseApp:
    def __init__(self, db_file: str = 'kinobaza.db') -> None:
        """
        Ініціалізує екземпляр програми CinemaBaseApp
        :param db_file: Назва файлу бази даних
        """
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def run(self) -> None:
        """
        Запускає головний цикл роботи програми, що взаємодіє з користувачем
        """
        while True:
            self.print_menu()
            choice = input("Виберіть дію: ")
            self.handle_menu_choice(choice)
            self.conn.commit()

    def print_menu(self) -> None:
        """
        Виводить головне меню програми
        """
        print("\nМеню:")
        print("1. Додати, редагувати або видалити фільм")
        print("2. Додати, редагувати або видалити актора")
        print("3. Показати всі фільми з акторами")
        print("4. Показати унікальні жанри")
        print("5. Показати кількість фільмів за жанром")
        print("6. Показати середній рік народження акторів у фільмах певного жанру")
        print("7. Пошук фільму за назвою")
        print("8. Показати фільми (з пагінацією)")
        print("9. Показати імена всіх акторів та назви всіх фільмів")
        print("0. Вихід")

    def handle_menu_choice(self, choice: str) -> None:
        """
        Обробляє вибір користувача з головного меню
        :param choice: Вибір користувача
        """
        if choice == '1':
            self.handle_add_or_edit_movie()
        elif choice == '2':
            self.handle_add_or_edit_actor()
        elif choice == '3':
            list_movies_with_actors(self.cursor)
        elif choice == '4':
            list_unique_genres(self.cursor)
        elif choice == '5':
            self.handle_list_movies_count_by_genre()
        elif choice == '6':
            genre = input("Введіть жанр: ")
            average_birth_year_by_genre(self.cursor, genre)
        elif choice == '7':
            keyword = input("Введіть ключове слово для пошуку: ")
            rows = search_movie_by_title(self.cursor, keyword)
            for row in rows:
                print(f"Фільм: {row[1]}, Рік: {row[2]}")
        elif choice == '8':
            page = int(input("Введіть номер сторінки: "))
            paginate_movies(self.cursor, page)
        elif choice == '9':
            list_actors_and_movies(self.cursor)
        elif choice == '0':
            self.conn.close()
            exit()
        else:
            print("Невірний вибір. Спробуйте ще раз.")
