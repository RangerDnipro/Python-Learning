"""
Модуль для авторизації
"""

from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.extensions import db

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    """
    Реєструє нового користувача.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth.route('/login', methods=['POST'])
def login():
    """
    Логінить існуючого користувача.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Logged in successfully"}), 200

    return jsonify({"error": "Invalid username or password"}), 401


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    Вихід із системи.
    """
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
