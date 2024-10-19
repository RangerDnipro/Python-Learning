"""
Основний файл для запуску програми
"""

from sqlite_crud import SQLiteCRUD
from mongodb_crud import MongoDBCRUD

# SQLite CRUD операції
sqlite_crud = SQLiteCRUD()
print("SQLite: Створення нового фільму")
sqlite_crud.create_movie('Inception', 2010, ['Sci-Fi', 'Action'], 'Christopher Nolan')
print("SQLite: Читання інформації про фільм")
print(sqlite_crud.read_movie('Inception'))
print("SQLite: Оновлення року випуску фільму")
sqlite_crud.update_movie('Inception', 2011)
print("SQLite: Читання оновленої інформації про фільм")
print(sqlite_crud.read_movie('Inception'))
print("SQLite: Видалення фільму")
sqlite_crud.delete_movie('Inception')
print("SQLite: Читання після видалення")
print(sqlite_crud.read_movie('Inception'))

# MongoDB CRUD операції
mongodb_crud = MongoDBCRUD()
print("MongoDB: Створення нового фільму")
mongodb_crud.create_movie('Inception', 2010, ['Sci-Fi', 'Action'], 'Christopher Nolan')
print("MongoDB: Читання інформації про фільм")
print(mongodb_crud.read_movie('Inception'))
print("MongoDB: Оновлення року випуску фільму")
mongodb_crud.update_movie('Inception', 2011)
print("MongoDB: Читання оновленої інформації про фільм")
print(mongodb_crud.read_movie('Inception'))
print("MongoDB: Видалення фільму")
mongodb_crud.delete_movie('Inception')
print("MongoDB: Читання після видалення")
print(mongodb_crud.read_movie('Inception'))

# Порівняння
print("\nПорівняння:")
print(
    "SQLite - реляційна база даних, де структура строго визначена і підходить для збереження "
    "чітко структурованих даних.")
print("Переваги: Транзакційна цілісність, складні запити.")
print("Недоліки: Складно змінювати структуру даних, обмежена масштабованість.")

print("\nMongoDB - NoSQL база даних, яка надає гнучку структуру збереження даних "
      "у вигляді документів.")
print("Переваги: Гнучкість моделі даних, горизонтальна масштабованість.")
print("Недоліки: Обмежена підтримка транзакцій, складні запити виконуються менш ефективно.")
