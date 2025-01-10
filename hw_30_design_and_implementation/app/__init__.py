"""
Модуль ініціалізації додатка Flask.

Цей модуль створює додаток Flask, налаштовує базу даних SQLAlchemy,
реєструє маршрути та забезпечує створення всіх таблиць бази даних у разі їх відсутності.

Функції:
- create_app: Створює та налаштовує екземпляр додатка Flask.

Модулі:
- Flask: Бібліотека для створення веб-додатків.
- app.extensions: Модуль для ініціалізації розширень.
- app.models: Модуль моделей бази даних.
- app.routes: Модуль з маршрутами для додатка.
- app.config: Модуль для конфігурації додатка.
"""

from flask import Flask
from app.extensions import db, migrate, login_manager
from app.models import User
from app.routes import main
from routes.auth import auth
from app.config import Config

def create_app():
    """
    Створює екземпляр додатка Flask, налаштовує базу даних,
    реєструє маршрути та забезпечує створення всіх таблиць.

    :return: Налаштований екземпляр Flask-додатка.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ініціалізація розширень
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Реєстрація маршрутів
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    # Налаштування менеджера входу
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Створення таблиць бази даних, якщо вони відсутні
    with app.app_context():
        db.create_all()

    return app
