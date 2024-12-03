"""
Модуль реалізує простий менеджер сесій користувачів для веб-додатку за допомогою Redis
Він дозволяє створювати, читати, оновлювати та видаляти сесії користувачів, а також
налаштовує TTL для автоматичного видалення неактивних сесій через 30 хвилин
"""

import time
from typing import Optional
import redis

# Підключення до Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


class UserSessionManager:
    """
    Клас для управління сесіями користувачів
    """
    # Час життя сесії в секундах (30 хвилин)
    SESSION_TTL_SECONDS = 30 * 60

    @staticmethod
    def create_session(user_id: str, session_token: str, login_time: float) -> None:
        """
        Додає нову сесію для користувача
        :param user_id: Ідентифікатор користувача
        :param session_token: Токен сесії
        :param login_time: Час входу в систему
        """
        session_key = f"session:{user_id}"
        session_data = {
            'session_token': session_token,
            'login_time': login_time,
            'last_activity_time': login_time
        }
        # Зберігаємо дані в Redis з TTL
        for key, value in session_data.items():
            redis_client.hset(session_key, key, value)
        redis_client.expire(session_key, UserSessionManager.SESSION_TTL_SECONDS)

    @staticmethod
    def get_session(user_id: str) -> Optional[dict]:
        """
        Отримує активну сесію для конкретного користувача
        :param user_id: Ідентифікатор користувача
        :return: Дані сесії або None, якщо сесія не існує
        """
        session_key = f"session:{user_id}"
        if redis_client.exists(session_key):
            return redis_client.hgetall(session_key)
        return None

    @staticmethod
    def update_last_activity(user_id: str) -> None:
        """
        Оновлює час останньої активності користувача
        :param user_id: Ідентифікатор користувача
        """
        session_key = f"session:{user_id}"
        if redis_client.exists(session_key):
            current_time = time.time()
            redis_client.hset(session_key, 'last_activity_time', current_time)
            # Оновлюємо TTL для продовження життя сесії
            redis_client.expire(session_key, UserSessionManager.SESSION_TTL_SECONDS)

    @staticmethod
    def delete_session(user_id: str) -> None:
        """
        Видаляє сесію після виходу користувача з системи
        :param user_id: Ідентифікатор користувача
        """
        session_key = f"session:{user_id}"
        redis_client.delete(session_key)


# Приклад використання
if __name__ == "__main__":
    USER_ID = "user_123"
    SESSION_TOKEN = "abc123token"
    LOGIN_TIME = time.time()

    # Створення нової сесії
    UserSessionManager.create_session(USER_ID, SESSION_TOKEN, LOGIN_TIME)
    print("Сесія створена.")

    # Отримання сесії
    session = UserSessionManager.get_session(USER_ID)
    if session:
        print("Отримана сесія:", session)
    else:
        print("Сесія не знайдена.")

    # Оновлення часу останньої активності
    UserSessionManager.update_last_activity(USER_ID)
    print("Час останньої активності оновлено.")

    # Видалення сесії
    UserSessionManager.delete_session(USER_ID)
    print("Сесія видалена.")
