"""
Скрипт для отримання даних про погоду через OpenWeather API з підтримкою кешування.
"""

import requests
from datetime import datetime, timedelta
from config import API_KEY
import logging

# Налаштування логування
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
    encoding="utf-8"
)

# Кеш для збереження результатів запитів
weather_cache = {}


def get_weather(city: str) -> str:
    """
    Отримує поточну погоду для заданого міста через API OpenWeather.
    :param city: Назва міста.
    :return: Текстовий опис погоди або повідомлення про помилку.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ua"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        result = f"Погода в {city}: {temp}°C, {description}."
        logging.info(f"Успішний запит для міста '{city}': {result}")
        return result
    else:
        error_message = f"Помилка: не вдалося отримати дані про погоду для міста '{city}'."
        logging.error(error_message)
        return error_message


def get_weather_with_cache(city: str) -> str:
    """
    Отримує погоду з кешуванням. Уникає повторних запитів протягом 10 хвилин.
    :param city: Назва міста.
    :return: Текстовий опис погоди.
    """
    now = datetime.now()

    # Перевірка, чи є дані в кеші і чи вони не застаріли
    if city in weather_cache and now - weather_cache[city]["time"] < timedelta(minutes=10):
        logging.info(f"Кешований результат для міста '{city}' використано.")
        return weather_cache[city]["data"]

    # Якщо даних немає в кеші або вони застаріли, виконуємо новий запит
    result = get_weather(city)
    weather_cache[city] = {"data": result, "time": now}
    logging.info(f"Новий запит для міста '{city}' виконано.")
    return result


# Тестовий виклик
if __name__ == "__main__":
    city_name = "Київ"
    print(get_weather_with_cache(city_name))
    # Додатковий тест кешування
    print(get_weather_with_cache(city_name))
