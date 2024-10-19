"""
Модуль для бекапу бази даних MongoDB
"""

import subprocess
import datetime
import os


def backup_database():
    """
    Створює резервну копію бази даних MongoDB "online_store".
    Резервна копія зберігається в директорії з ім'ям "backup" та міткою часу,
    розташованій у тій самій папці, що й цей модуль.
    """
    # Отримуємо поточну директорію, де знаходиться скрипт
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Створюємо ім'я директорії для резервного копіювання з міткою часу
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_directory = os.path.join(current_directory, f"backup_{timestamp}")

    try:
        # Виконуємо команду mongodump для створення резервної копії
        subprocess.run([r"C:\Program Files\MongoDB\Server\8.0\bin\mongodump.exe",
                        "--db", "online_store", "--out", backup_directory], check=True)
        print(f"Резервне копіювання завершено успішно. Файли збережено у: {backup_directory}")
    except subprocess.CalledProcessError as e:
        print(f"Помилка при резервному копіюванні: {e}")


# Викликаємо функцію резервного копіювання
if __name__ == "__main__":
    backup_database()
