# Використовуємо офіційний образ Python
FROM python:3.10-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо залежності
COPY requirements.txt /app/

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код проекту
COPY . /app

# Відкриваємо порт для Django
EXPOSE 8000

# Запускаємо сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
