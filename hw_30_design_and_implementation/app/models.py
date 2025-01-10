"""
Модуль містить визначення моделей бази даних для застосунку "Фільмотека".

Моделі:
- Director: представляє режисера фільму, включає ідентифікатор та ім'я.
- Film: представляє фільм, включає інформацію про назву, рік випуску, рейтинг, постер, опис та режисера.

Зв'язки:
- Кожен фільм пов'язаний з одним режисером.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db


class Director(db.Model):
    """
    Модель для зберігання інформації про режисерів.

    Поля:
    - id (Integer): Унікальний ідентифікатор режисера.
    - name (String): Ім'я режисера, унікальне, не може бути порожнім.
    """
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self) -> str:
        """
        Повертає рядкове представлення моделі.
        :return: Рядок у форматі '<Director {name}>'.
        """
        return f'<Director {self.name}>'


class Film(db.Model):
    """
    Модель для зберігання інформації про фільми.

    Поля:
    - id (Integer): Унікальний ідентифікатор фільму.
    - title (String): Назва фільму, унікальна, не може бути порожньою.
    - release_year (Integer): Рік випуску фільму.
    - rating (Float): Рейтинг фільму, за замовчуванням 0.0.
    - poster (String): Шлях до постеру фільму, унікальний, не може бути порожнім.
    - description (Text): Опис фільму, унікальний, не може бути порожнім.
    - director_id (Integer): Ідентифікатор режисера, пов'язаний з фільмом.
    - director (Relationship): Відношення до моделі Director.
    """
    __tablename__ = 'films'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)
    poster = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'), nullable=False)
    director = db.relationship('Director', backref='films', lazy=True)

    def __repr__(self) -> str:
        """
        Повертає рядкове представлення моделі.
        :return: Рядок у форматі '<Film {title}>'.
        """
        return f'<Film {self.title}>'


class User(UserMixin, db.Model):
    """
    Модель для користувачів.
    Поля:
    - id: Унікальний ідентифікатор.
    - username: Ім'я користувача.
    - password_hash: Хеш пароля.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password: str) -> None:
        """
        Хешує пароль і зберігає його.
        :param password: Пароль у відкритому вигляді.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Перевіряє пароль.
        :param password: Пароль у відкритому вигляді.
        :return: True, якщо пароль правильний.
        """
        return check_password_hash(self.password_hash, password)
