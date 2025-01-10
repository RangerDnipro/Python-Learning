"""
Модуль для запуску Flask-додатку.

Цей модуль створює додаток Flask за допомогою функції `create_app` та запускає сервер додатку.

Містить:
- Імпорт функції `create_app` з пакету `app`.
- Ініціалізацію додатку `app`.
- Умову для запуску додатку у відлагоджувальному режимі.

Як використовувати:
1. Запустіть цей файл, щоб стартувати сервер.
2. Додаток буде доступний за замовчуванням на http://127.0.0.1:5000.
"""
from app import create_app

# Ініціалізація Flask-додатку
app = create_app()

# Запуск серверу
if __name__ == '__main__':
    import os

    # Якщо змінна оточення "DOCKER" встановлена, використовуємо конфігурацію для Docker
    if os.environ.get('DOCKER'):
        app.run(host="0.0.0.0", port=5000)  # Для Docker
    else:
        app.run(debug=True)  # Для локального запуску
