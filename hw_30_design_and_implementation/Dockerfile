# Використовуємо базовий образ Python
FROM python:3.10-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл requirements.txt для встановлення залежностей
COPY requirements.txt /app/requirements.txt

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли проекту в контейнер
COPY . /app

# Відкриваємо порт 5000 для Flask
EXPOSE 5000

# Встановлюємо команду запуску Flask-додатку
CMD ["python", "run.py"]
