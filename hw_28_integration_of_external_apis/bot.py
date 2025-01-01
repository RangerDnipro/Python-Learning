"""
Telegram-бот для взаємодії з OpenWeather API.
"""

import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

from config import TELEGRAM_BOT_TOKEN
from main import get_weather_with_cache


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробляє команду /start, вітає користувача.
    """
    logging.info(f"Команда /start отримана від користувача {update.effective_user.id}.")
    await update.message.reply_text(
        "Привіт! Я бот для отримання погоди. Напиши /help, щоб дізнатися більше."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробляє команду /help, показує список доступних команд.
    """
    logging.info(f"Команда /help отримана від користувача {update.effective_user.id}.")
    await update.message.reply_text(
        "Доступні команди:\n"
        "/start - початок роботи\n"
        "/help - список команд\n"
        "/weather - отримати погоду для міста"
    )


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробляє команду /weather, показує кнопки з вибором міст.
    """
    logging.info(f"Команда /weather отримана від користувача {update.effective_user.id}.")

    cities = ["Київ", "Львів", "Одеса", "Харків", "Дніпро"]
    buttons = [[InlineKeyboardButton(city, callback_data=city)] for city in cities]

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        "Оберіть місто для отримання погоди або введіть інше місто з клавіатури:",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробляє текстові повідомлення для отримання погоди.
    """
    city = update.message.text
    logging.info(f"Користувач ввів місто вручну: {city}")

    # Отримання погоди для введеного міста
    weather_info = get_weather_with_cache(city)

    await update.message.reply_text(weather_info)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробляє невідомі команди.
    """
    logging.warning(f"Невідома команда від користувача {update.effective_user.id}: {update.message.text}")
    await update.message.reply_text(
        "Я не розумію цієї команди. Напишіть /help для перегляду доступних команд."
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробляє вибір міста через кнопки.
    """
    query = update.callback_query
    await query.answer()

    city = query.data  # Отримання назви міста
    logging.info(f"Користувач обрав місто: {city}")

    # Отримання погоди для вибраного міста
    weather_info = get_weather_with_cache(city)

    # Залишаємо меню кнопок
    cities = ["Київ", "Львів", "Одеса", "Харків", "Дніпро"]
    buttons = [[InlineKeyboardButton(city, callback_data=city)] for city in cities]
    reply_markup = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(
        text=f"{weather_info}\n\nОберіть місто або введіть інше з клавіатури:",
        reply_markup=reply_markup,
    )


def main() -> None:
    """
    Основна функція для запуску Telegram-бота.
    """
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Реєстрація обробників команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Запуск бота
    application.run_polling()


if __name__ == "__main__":
    main()
