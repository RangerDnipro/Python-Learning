"""
Модуль для взаємодії з користувачем з використанням класів
"""

import sqlite3
from database import *
from .search import search_movie_by_title, search_actor_by_name


class Movie:
    def __init__(self, title, release_year=None, genre=None, movie_id=None):
        self.id = movie_id
        self.title = title
        self.release_year = release_year
        self.genre = genre

    def save_to_db(self, cursor):
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
    def get_from_db(cls, cursor, movie_id):
        cursor.execute('SELECT id, title, release_year, genre FROM movies WHERE id = ?', (movie_id,))
        row = cursor.fetchone()
        if row:
            return cls(movie_id=row[0], title=row[1], release_year=row[2], genre=row[3])
        return None


class Actor:
    def __init__(self, name, birth_year=None, actor_id=None):
        self.id = actor_id
        self.name = name
        self.birth_year = birth_year

    def save_to_db(self, cursor):
        if self.id is None:
            cursor.execute(
                'INSERT INTO actors (name, birth_year) VALUES (?, ?)',
                (self.name, self.birth_year)
            )
            self.id = cursor.lastrowid

    @classmethod
    def get_from_db(cls, cursor, actor_id):
        cursor.execute('SELECT id, name, birth_year FROM actors WHERE id = ?', (actor_id,))
        row = cursor.fetchone()
        if row:
            return cls(actor_id=row[0], name=row[1], birth_year=row[2])
        return None


class CinemaBaseApp:
    def __init__(self, db_file='kinobaza.db'):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def run(self):
        while True:
            self.print_menu()
            choice = input("Виберіть дію: ")
            self.handle_menu_choice(choice)
            self.conn.commit()

    def print_menu(self):
        print("\nМеню:")
        print("1. Додати фільм")
        print("2. Додати актора")
        print("3. Показати всі фільми з акторами")
        print("4. Показати унікальні жанри")
        print("5. Показати кількість фільмів за жанром")
        print("6. Показати середній рік народження акторів у фільмах певного жанру")
        print("7. Пошук фільму за назвою")
        print("8. Показати фільми (з пагінацією)")
        print("9. Показати імена всіх акторів та назви всіх фільмів")
        print("0. Вихід")

    def handle_menu_choice(self, choice):
        if choice == '1':
            self.handle_add_or_edit_movie()
        elif choice == '2':
            self.handle_add_actor()
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

    def handle_add_or_edit_movie(self):
        title = input("Введіть назву фільму: ")
        rows = search_movie_by_title(self.cursor, title)
        if rows:
            print("Знайдені фільми:")
            for idx, row in enumerate(rows, start=1):
                print(f"{idx}. Фільм: {row[1]}, Рік: {row[2]}")
            print("0. Додати новий фільм")
            movie_choice = int(input("Введіть номер фільму для редагування або 0 для додавання нового: "))
            if movie_choice != 0:
                movie = Movie.get_from_db(self.cursor, rows[movie_choice - 1][0])
                self.edit_movie(movie)
            else:
                release_year = int(input("Введіть рік випуску: "))
                genre = input("Введіть жанр: ")
                movie = Movie(title=title, release_year=release_year, genre=genre)
                movie.save_to_db(self.cursor)
        else:
            release_year = int(input("Введіть рік випуску: "))
            genre = input("Введіть жанр: ")
            movie = Movie(title=title, release_year=release_year, genre=genre)
            movie.save_to_db(self.cursor)

        self.handle_add_actors_to_movie(movie)

    def edit_movie(self, movie):
        while True:
            print("\nРедагувати фільм:")
            print("1. Змінити назву фільму")
            print("2. Змінити рік випуску")
            print("3. Змінити жанр")
            print("0. Повернутися до основного меню")

            edit_choice = input("Виберіть дію: ")
            if edit_choice == '1':
                movie.title = input("Введіть нову назву фільму: ")
                movie.save_to_db(self.cursor)
                print(f"Назву фільму змінено на: {movie.title}")
            elif edit_choice == '2':
                movie.release_year = int(input("Введіть новий рік випуску: "))
                movie.save_to_db(self.cursor)
                print(f"Рік випуску фільму змінено на: {movie.release_year}")
            elif edit_choice == '3':
                movie.genre = input("Введіть новий жанр: ")
                movie.save_to_db(self.cursor)
                print(f"Жанр фільму змінено на: {movie.genre}")
            elif edit_choice == '0':
                break
            else:
                print("Невірний вибір. Спробуйте ще раз.")

    def handle_add_actors_to_movie(self, movie):
        while True:
            print("\nДодати акторів до фільму:")
            print("1. Вибрати актора з існуючих")
            print("2. Додати нового актора")
            print("0. Вихід")

            actor_choice = input("Виберіть дію: ")
            if actor_choice == '1':
                rows = search_actor_by_name(self.cursor)
                if not rows:
                    print("Акторів з таким ім'ям не знайдено.")
                    continue
                actor_number = int(input("Введіть номер актора (або 0 для повернення): "))
                if actor_number == 0:
                    continue
                else:
                    actor = Actor.get_from_db(self.cursor, rows[actor_number - 1][0])
                    link_actor_to_movie(self.cursor, movie.id, actor.id)
            elif actor_choice == '2':
                name = input("Введіть ім'я актора: ")
                birth_year = int(input("Введіть рік народження актора: "))
                actor = Actor(name=name, birth_year=birth_year)
                actor.save_to_db(self.cursor)
                link_actor_to_movie(self.cursor, movie.id, actor.id)
                print(f"Доданий Актор: {actor.name}, Рік: {actor.birth_year}")
            elif actor_choice == '0':
                break
            else:
                print("Невірний вибір. Спробуйте ще раз.")

    def handle_add_actor(self):
        name = input("Введіть ім'я актора: ")
        birth_year = int(input("Введіть рік народження актора: "))
        actor = Actor(name=name, birth_year=birth_year)
        actor.save_to_db(self.cursor)
        print(f"Доданий Актор: {actor.name}, Рік: {actor.birth_year}")

    def handle_list_movies_count_by_genre(self):
        self.cursor.execute('SELECT genre, COUNT(*) FROM movies GROUP BY genre ORDER BY COUNT(*) DESC')
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"Жанр: {row[0]}, Кількість фільмів: {row[1]}")


if __name__ == '__main__':
    app = CinemaBaseApp()
    app.run()
