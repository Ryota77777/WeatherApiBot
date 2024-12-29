import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Переменные окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHER_API_URL = os.getenv('API_URL')
WEATHER_API_KEY = os.getenv('API_KEY')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


def get_db_connection():
    """Подключение к базе данных."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def save_to_db(user_id: int, user_message: str, api_reply: str) -> None:
    """Сохранение данных в базу данных."""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            execute_values(
                cursor,
                """INSERT INTO interactions (user_id, user_message, api_reply) VALUES %s""",
                [(user_id, user_message, api_reply)]
            )
            conn.commit()
    except Exception as e:
        logger.error(f"Ошибка при сохранении в базу данных: {e}")
    finally:
        if conn:
            conn.close()


async def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start."""
    await update.message.reply_text(
        "Привет! Я бот. Используйте /weather для текущей погоды, /forecast для прогноза погоды, "
        "или /help для списка команд."
    )


async def help_command(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /help."""
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - Начать работу\n"
        "/help - Список команд\n"
        "/weather <город> - Узнать текущую погоду\n"
        "/forecast <город> - Узнать прогноз погоды\n"
    )


async def weather(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /weather."""
    if len(context.args) == 0:
        await update.message.reply_text("Пожалуйста, укажите город: /weather <город>")
        return

    city = " ".join(context.args)
    try:
        response = requests.get(
            f"{WEATHER_API_URL}/current.json",
            params={"key": WEATHER_API_KEY, "q": city, "aqi": "no"}
        )
        if response.status_code == 200:
            data = response.json()
            location = data.get("location", {}).get("name", "Неизвестно")
            temperature = data.get("current", {}).get("temp_c", "N/A")
            condition = data.get("current", {}).get("condition", {}).get("text", "N/A")
            reply = f"Текущая погода в {location}:\nТемпература: {temperature}°C\nСостояние: {condition}"
        else:
            reply = "Не удалось получить данные о погоде. Проверьте название города."
    except Exception as e:
        logger.error(f"Ошибка API: {e}")
        reply = "Произошла ошибка при запросе погоды. Попробуйте позже."

    await update.message.reply_text(reply)
    save_to_db(update.message.from_user.id, f"/weather {city}", reply)


async def forecast(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /forecast."""
    if len(context.args) == 0:
        await update.message.reply_text("Пожалуйста, укажите город: /forecast <город>")
        return

    city = " ".join(context.args)
    try:
        response = requests.get(
            f"{WEATHER_API_URL}/forecast.json",
            params={"key": WEATHER_API_KEY, "q": city, "days": 3, "aqi": "no"}
        )
        if response.status_code == 200:
            data = response.json()
            location = data.get("location", {}).get("name", "Неизвестно")
            forecast_data = data.get("forecast", {}).get("forecastday", [])
            reply = f"Прогноз погоды в {location} на 3 дня:\n"
            for day in forecast_data:
                date = day.get("date", "N/A")
                temp = day.get("day", {}).get("avgtemp_c", "N/A")
                condition = day.get("day", {}).get("condition", {}).get("text", "N/A")
                reply += f"{date}: {temp}°C, {condition}\n"
        else:
            reply = "Не удалось получить данные о прогнозе. Проверьте название города."
    except Exception as e:
        logger.error(f"Ошибка API: {e}")
        reply = "Произошла ошибка при запросе прогноза. Попробуйте позже."

    await update.message.reply_text(reply)
    save_to_db(update.message.from_user.id, f"/forecast {city}", reply)


def main():
    """Основной запуск бота."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("forecast", forecast))

    # Запуск
    application.run_polling()


if __name__ == "__main__":
    main()


