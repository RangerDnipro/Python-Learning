"""
Модуль для роботи з базою даних Cassandra
"""

from datetime import datetime, timedelta
from uuid import uuid4  # Імпорт функції uuid4 для генерації UUID
from contextlib import contextmanager
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement, BatchStatement


# Контекстний менеджер для керування сесією Cassandra
@contextmanager
def cassandra_session():
    """
    Контекстний менеджер для підключення до кластера Cassandra та автоматичного закриття підключення
    :return: Об'єкт сесії Cassandra
    """
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    try:
        session.set_keyspace('event_logs')  # Встановлення keyspace при кожному підключенні
        yield session
    finally:
        session.shutdown()
        cluster.shutdown()


# Створення ключового простору та таблиць
with cassandra_session() as cassandra_session_object:
    cassandra_session_object.execute("""
        CREATE KEYSPACE IF NOT EXISTS event_logs 
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3}
    """)
    cassandra_session_object.set_keyspace('event_logs')
    cassandra_session_object.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            event_id UUID PRIMARY KEY,
            user_id UUID,
            event_type TEXT,
            timestamp TIMESTAMP,
            metadata TEXT
        )
    """)
    cassandra_session_object.execute("""
        CREATE TABLE IF NOT EXISTS old_logs (
            event_id UUID PRIMARY KEY,
            user_id UUID,
            event_type TEXT,
            timestamp TIMESTAMP,
            metadata TEXT
        )
    """)


# Додати новий лог події до таблиці
def create_event(cassandra_session_obj, event_id: uuid4, user_id: uuid4,
                 event_type: str, metadata: str) -> None:
    """
    Додає новий лог події до таблиці logs
    :param cassandra_session_obj: Об'єкт сесії Cassandra
    :param event_id: UUID події
    :param user_id: UUID користувача
    :param event_type: Тип події
    :param metadata: Додаткова інформація про подію
    """
    cassandra_session_obj.execute("""
        INSERT INTO logs (event_id, user_id, event_type, timestamp, metadata)
        VALUES (%s, %s, %s, %s, %s)
    """, (event_id, user_id, event_type, datetime.now(), metadata))


# Отримати всі події певного типу за останні 24 години
def read_events(cassandra_session_obj, event_type: str):
    """
    Отримує всі події певного типу за останні 24 години
    :param cassandra_session_obj: Об'єкт сесії Cassandra
    :param event_type: Тип події
    :return: Результат запиту (події за останні 24 години)
    """
    query = SimpleStatement("""
        SELECT * FROM logs WHERE event_type=%s AND timestamp >= %s ALLOW FILTERING
    """, fetch_size=10)
    last_24_hours = datetime.now() - timedelta(hours=24)
    return cassandra_session_obj.execute(query, (event_type, last_24_hours))


# Оновити додаткову інформацію в полі metadata для певного event_id
def update_event_metadata(cassandra_session_obj, event_id: uuid4, new_metadata: str) -> None:
    """
    Оновлює додаткову інформацію в полі metadata для певного event_id
    :param cassandra_session_obj: Об'єкт сесії Cassandra
    :param event_id: UUID події
    :param new_metadata: Нове значення для поля metadata
    """
    cassandra_session_obj.execute("""
        UPDATE logs SET metadata=%s WHERE event_id=%s
    """, (new_metadata, event_id))


# Додати події до старих логів
def add_old_event(cassandra_session_obj, event_id: uuid4, user_id: uuid4,
                  event_type: str, metadata: str, timestamp: datetime) -> None:
    """
    Додає старий лог події до таблиці old_logs
    :param cassandra_session_obj: Об'єкт сесії Cassandra
    :param event_id: UUID події
    :param user_id: UUID користувача
    :param event_type: Тип події
    :param metadata: Додаткова інформація про подію
    :param timestamp: Час події
    """
    cassandra_session_obj.execute("""
        INSERT INTO old_logs (event_id, user_id, event_type, timestamp, metadata)
        VALUES (%s, %s, %s, %s, %s)
    """, (event_id, user_id, event_type, timestamp, metadata))


# Видалити старі події (старші за 7 днів) з бази даних
def delete_old_events(cassandra_session_obj) -> None:
    """
    Видаляє старі події (старші за 7 днів) з таблиці logs та переміщує їх до таблиці old_logs
    :param cassandra_session_obj: Об'єкт сесії Cassandra
    """
    seven_days_ago = datetime.now() - timedelta(days=7)
    old_events = cassandra_session_obj.execute("""
        SELECT * FROM logs WHERE timestamp < %s ALLOW FILTERING
    """, (seven_days_ago,))

    batch = BatchStatement()
    for event in old_events:
        add_old_event(cassandra_session_obj, event.event_id, event.user_id,
                      event.event_type, event.metadata, event.timestamp)
        batch.add(SimpleStatement("""
            DELETE FROM logs WHERE event_id=%s
        """), (event.event_id,))
    cassandra_session_obj.execute(batch)


# Приклад використання з контекстним менеджером
with cassandra_session() as cassandra_session_object:
    create_event(cassandra_session_object, uuid4(), uuid4(), 'login', 'metadata content')
    events = read_events(cassandra_session_object, 'login')
    for new_event in events:
        print(new_event)
    update_event_metadata(cassandra_session_object, uuid4(), 'new metadata content')
    delete_old_events(cassandra_session_object)
