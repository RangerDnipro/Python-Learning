"""
Модуль для розширень Flask, використовуваних у проєкті.

Цей модуль містить об'єкти для роботи з базою даних і міграціями:
- db: Об'єкт SQLAlchemy для взаємодії з базою даних.
- migrate: Об'єкт Migrate для керування міграціями бази даних.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Ініціалізація SQLAlchemy для роботи з базою даних
db = SQLAlchemy()

# Ініціалізація Flask-Migrate для міграцій бази даних
migrate = Migrate()

# Менеджер входу
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
