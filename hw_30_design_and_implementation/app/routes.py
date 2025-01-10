"""
Модуль містить маршрути для роботи з фільмами та режисерами.
Включає функціонал для створення, оновлення, видалення та перегляду записів.
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.models import Film, Director
from app.extensions import db
from typing import Any, Dict

main = Blueprint('main', __name__)


@main.route('/')
def index() -> Dict[str, str]:
    """
    Початкова сторінка API.
    :return: Повідомлення-привітання.
    """
    return {"message": "Welcome to the Film Library API"}


@main.route('/add-director', methods=['POST'])
@login_required
def add_director() -> Any:
    """
    Додає нового режисера.
    :return: JSON з інформацією про створеного режисера або помилка.
    """
    data = request.get_json()
    existing_director = Director.query.filter_by(name=data['name']).first()
    if existing_director:
        return jsonify({"error": "Director already exists", "id": existing_director.id}), 409

    director = Director(name=data['name'])
    db.session.add(director)
    db.session.commit()
    return jsonify({"id": director.id, "name": director.name}), 201


@main.route('/directors-list', methods=['GET'])
def get_directors() -> Any:
    """
    Отримує список усіх режисерів.
    :return: JSON зі списком режисерів.
    """
    directors = Director.query.all()
    result = [{"id": d.id, "name": d.name} for d in directors]
    return jsonify(result), 200


@main.route('/update-director/<int:director_id>', methods=['PUT'])
@login_required
def update_director(director_id: int) -> Any:
    """
    Оновлює інформацію про режисера за ID.
    :param director_id: ID режисера.
    :return: Повідомлення про успішне оновлення або помилка.
    """
    director = Director.query.get_or_404(director_id)
    data = request.get_json()
    name = data.get('name')
    if name:
        director.name = name
    db.session.commit()
    return jsonify({"message": "director updated successfully"}), 200


@main.route('/director-delete/<int:director_id>', methods=['DELETE'])
@login_required
def delete_director(director_id):
    """
    Видаляє режисера за його ID. Перепризначає фільми до режисера "unknown".
    Якщо "unknown" не існує, створює його автоматично.

    :param director_id: ID режисера для видалення.
    :return: JSON-відповідь із результатом операції.
    """
    director = Director.query.get(director_id)
    if not director:
        return jsonify({"error": "director not found"}), 404

    # Перевірка чи існує "unknown"
    unknown = Director.query.filter_by(name="unknown").first()
    if not unknown:
        unknown = Director(name="unknown")
        db.session.add(unknown)
        db.session.commit()

    try:
        # Оновлення всіх фільмів цього режисера
        films = Film.query.filter_by(director_id=director.id).all()
        for film in films:
            film.director_id = unknown.id

        # Застосування змін для фільмів
        db.session.flush()

        # Видалення режисера
        db.session.delete(director)
        db.session.commit()

        return jsonify({"message": "director deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/films', methods=['POST'])
@login_required
def add_films() -> Any:
    """
    Додає новий фільм.
    :return: JSON з інформацією про створений фільм або помилка.
    """
    data = request.get_json()
    title = data.get('title')
    release_year = data.get('release_year')
    rating = data.get('rating')
    poster = data.get('poster', 'default_poster.jpg')  # Значення за замовчуванням
    description = data.get('description')
    director_id = data.get('director_id')

    if not all([title, release_year, rating, description, director_id]):
        return jsonify({"error": "all fields are required"}), 400

    film = Film(
        title=title,
        release_year=int(release_year),
        director_id=int(director_id),
        rating=float(rating),
        poster=poster,
        description=description
    )
    db.session.add(film)
    db.session.commit()
    return jsonify({"id": film.id, "title": film.title}), 201


@main.route('/films-list', methods=['GET'])
def get_films():
    """
    Повертає список фільмів з бази даних, включаючи опис та постер.
    """
    films = Film.query.all()
    result = [{
        "id": f.id,
        "title": f.title,
        "release_year": f.release_year,
        "rating": f.rating,
        "description": f.description,
        "poster": f"/static/images/{f.poster}" if f.poster else None,
        "director": f.director.name,
    } for f in films]
    return jsonify(result), 200


@main.route('/delete-film/<int:film_id>', methods=['DELETE'])
@login_required
def delete_film(film_id: int) -> Any:
    """
    Видаляє фільм за ID.
    :param film_id: ID фільму.
    :return: Повідомлення про успішне видалення або помилка.
    """
    film = Film.query.get(film_id)
    if not film:
        return jsonify({"error": "film not found"}), 404
    try:
        db.session.delete(film)
        db.session.commit()
        return jsonify({"message": "film deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/update-film/<int:film_id>', methods=['PUT', 'PATCH'])
@login_required
def update_film(film_id: int) -> Any:
    """
    Оновлює інформацію про фільм за ID.
    :param film_id: ID фільму.
    :return: Повідомлення про успішне оновлення або помилка.
    """
    film = Film.query.get(film_id)
    if not film:
        return jsonify({"error": "film not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "no input data provided"}), 400

    try:
        if 'title' in data:
            film.title = data['title']
        if 'release_year' in data:
            film.release_year = int(data['release_year'])
        if 'rating' in data:
            film.rating = float(data['rating'])
        if 'description' in data:
            film.description = data['description']
        if 'director_id' in data:
            director = Director.query.get(data['director_id'])
            if not director:
                return jsonify({"error": "director not found"}), 404
            film.director_id = data['director_id']

        db.session.commit()
        return jsonify({"message": "film updated successfully", "film": {
            "id": film.id,
            "title": film.title,
            "release_year": film.release_year,
            "rating": film.rating,
            "description": film.description,
            "director_id": film.director_id
        }}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
