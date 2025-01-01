"""
Модуль для завантаження конфігураційних змінних із .env файлу.
"""

import os
from dotenv import load_dotenv

# Завантаження змінних із .env
load_dotenv()

# API ключ OpenWeather
API_KEY = os.getenv("API_KEY")

# Telegram токен
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
