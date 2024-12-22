# ДЗ 26. Deployment of Flask and Django applications using Docker

## 1. Перевірка на іншому комп'ютері
1. Склонуйте цей репозиторій `hw_26_deployment_using_docker`
2. Перейдіть у потрібну папку (`flask_app/` або `django_app/`).
3. Встановіть залежності з відповідного `requirements.txt`
4. Запустіть Docker Compose

## 2. Flask Application

### Опис
Flask-застосунок, який виводить текст `Flask in Docker is working!`.

### Запуск
1. Перейдіть до папки `flask_app/`:
2. Запустіть Docker-контейнер:
   ```bash
   docker-compose up --build
   ```
3. Відкрийте [http://127.0.0.1:5000](http://127.0.0.1:5000) у браузері.

## 3. Django Application

### Опис
Django-застосунок, який виводить текст `Django in Docker is working!`.

### Запуск
1. Перейдіть до папки `django_app/`:
2. Запустіть Docker-контейнер:
   ```bash
   docker-compose up --build
   ```
3. Відкрийте [http://127.0.0.1:8000](http://127.0.0.1:8000) у браузері.

## 3. Налаштування Docker

У кожному проекті є `.dockerignore`, який виключає зайві файли:
- `.git`
- `__pycache__`
- Локальні бази даних (для Django)

## 4. Вимоги
- Docker
- Docker Compose
