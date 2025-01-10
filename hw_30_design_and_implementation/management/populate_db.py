"""
Тестове заповнення бази даних режисерів та фільмів
"""

import os
from app import create_app
from app.extensions import db
from app.models import Director, Film


def populate_database():
    """
    Заповнює базу даних тестовими даними для таблиць Director і Film.
    """
    app = create_app()
    with app.app_context():
        # Перевіряємо, чи база даних уже заповнена
        # if Director.query.first() or Film.query.first():
        #     print("База даних уже заповнена!")
        #     return

        # Шлях до папки з постерами
        root_path = os.path.dirname(app.root_path)
        static_path = os.path.join(root_path, 'static', 'images')

        # Тестові режисери
        directors = [
            Director(name="Christopher Nolan"),
            Director(name="Steven Spielberg"),
            Director(name="Quentin Tarantino"),
            Director(name="Martin Scorsese"),
        ]

        db.session.add_all(directors)
        db.session.commit()

        # Отримуємо ID доданих режисерів
        nolan_id = Director.query.filter_by(name="Christopher Nolan").first().id
        spielberg_id = Director.query.filter_by(name="Steven Spielberg").first().id
        tarantino_id = Director.query.filter_by(name="Quentin Tarantino").first().id
        scorsese_id = Director.query.filter_by(name="Martin Scorsese").first().id

        # Тестові фільми
        films = [
            {"title": "Inception", "release_year": 2010, "rating": 8.8, "poster": "inception.jpg",
             "description": "A mind-bending thriller.", "director_id": nolan_id},
            {"title": "Interstellar", "release_year": 2014, "rating": 8.6, "poster": "interstellar.jpg",
             "description": "A journey beyond the stars.", "director_id": nolan_id},
            {"title": "Jaws", "release_year": 1975, "rating": 8.0, "poster": "jaws.jpg",
             "description": "A tale of a great white shark.", "director_id": spielberg_id},
            {"title": "Pulp Fiction", "release_year": 1994, "rating": 8.9, "poster": "pulp_fiction.jpg",
             "description": "A cult classic crime story.", "director_id": tarantino_id},
            {"title": "The Wolf of Wall Street", "release_year": 2013, "rating": 8.2,
             "poster": "wolf_of_wall_street.jpg",
             "description": "The rise and fall of a stockbroker.", "director_id": scorsese_id},
        ]

        for film_data in films:
            poster_path = os.path.join(static_path, film_data["poster"])
            if not os.path.exists(poster_path):
                print(
                    f"Увага: Постер {film_data['poster']} не знайдено у {static_path}. Використовується 'default_poster.jpg'.")
                film_data["poster"] = "default_poster.jpg"
            film = Film(**film_data)
            db.session.add(film)

        db.session.commit()
        print("База даних успішно заповнена тестовими даними!")


if __name__ == "__main__":
    populate_database()
