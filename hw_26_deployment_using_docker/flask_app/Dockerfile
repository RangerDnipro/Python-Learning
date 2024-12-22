# Використовуємо офіційний образ Python
FROM python:3.10-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо залежності
COPY requirements.txt /app/

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код застосунку
COPY . /app

# Відкриваємо порт для Flask
EXPOSE 5000

# Запускаємо сервер Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
