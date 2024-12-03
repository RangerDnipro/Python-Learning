"""
Модуль для збереження класів Movie та Actor
"""


class Movie:
    def __init__(self, title: str, release_year: int = None, genre: str = None, movie_id: int = None):
        """
        Ініціалізація екземпляра класу Movie
        :param title: Назва фільму
        :param release_year: Рік випуску фільму
        :param genre: Жанр фільму
        :param movie_id: Ідентифікатор фільму (якщо є)
        """
        self.id = movie_id
        self.title = title
        self.release_year = release_year
        self.genre = genre

    def save_to_db(self, cursor) -> None:
        """
        Зберігає екземпляр фільму у базі даних
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
    def get_from_db(cls, cursor, movie_id: int):
        """
        Отримує екземпляр фільму з бази даних за його ідентифікатором
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
    def __init__(self, name: str, birth_year: int = None, actor_id: int = None):
        """
        Ініціалізація екземпляра класу Actor
        :param name: Ім'я актора
        :param birth_year: Рік народження актора
        :param actor_id: Ідентифікатор актора (якщо є)
        """
        self.id = actor_id
        self.name = name
        self.birth_year = birth_year

    def save_to_db(self, cursor) -> None:
        """
        Зберігає екземпляр актора у базі даних
        :param cursor: Курсор бази даних для виконання SQL-запитів
        """
        if self.id is None:
            cursor.execute(
                'INSERT INTO actors (name, birth_year) VALUES (?, ?)',
                (self.name, self.birth_year)
            )
            self.id = cursor.lastrowid

    @classmethod
    def get_from_db(cls, cursor, actor_id: int):
        """
        Отримує екземпляр актора з бази даних за його ідентифікатором
        :param cursor: Курсор бази даних для виконання SQL-запитів
        :param actor_id: Ідентифікатор актора
        :return: Екземпляр класу Actor або None, якщо актор не знайдений
        """
        cursor.execute('SELECT id, name, birth_year FROM actors WHERE id = ?', (actor_id,))
        row = cursor.fetchone()
        if row:
            return cls(actor_id=row[0], name=row[1], birth_year=row[2])
        return None
