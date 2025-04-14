import os
import requests
import datetime
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Включаем nest_asyncio
import nest_asyncio
nest_asyncio.apply()

# Загружаем переменные окружения
load_dotenv()

API_KEY = os.getenv('NASA_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if API_KEY is None or TELEGRAM_TOKEN is None:
    raise ValueError("NASA_API_KEY или TELEGRAM_TOKEN не заданы в переменных окружения")

# Функция приветствия
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [{'text': 'Начать 🌟'}]  # Кнопка для инициации сеанса
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Привет! Нажмите 'Начать', чтобы продолжить.", reply_markup=markup)

# Функция обработки нажатия кнопки
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Начать 🌟":
        await update.message.reply_text("Бот успешно инициализирован! Выберите опцию:", reply_markup=generate_main_menu())
    elif text == "🌌 Получить фото":
        await get_photo(update, context)
    elif text == "📅 Выбор даты фото":
        await update.message.reply_text("Пожалуйста, введите дату в формате YYYY-MM-DD.")
    elif text.lower() in ["привет", "здравствуй", "здравствуйте"]:
        await welcome(update, context)
    else:
        # Проверка формата даты
        try:
            datetime.datetime.strptime(text, '%Y-%m-%d')
            await get_photo(update, context, text)
        except ValueError:
            await update.message.reply_text("Неправильный формат даты! Пожалуйста, используйте YYYY-MM-DD.")

# Генерация основного меню
def generate_main_menu():
    keyboard = [
        [{'text': '🌌 Получить фото'}, {'text': '📅 Выбор даты фото'}],
        [{'text': '❓ Помощь'}, {'text': 'ℹ️ Информация'}]
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

# Функция получения фото  
async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, date_input=None):
    date_input = date_input or (context.args[0] if context.args else datetime.datetime.now().strftime('%Y-%m-%d'))
    url = f'https://api.nasa.gov/planetary/apod?date={date_input}&api_key={API_KEY}'

    response = requests.get(url)
    if response.status_code != 200:
        await update.message.reply_text(f"Ошибка: {response.status_code}")
        return

    data = response.json()
    title = data.get('title', 'Нет названия')
    image_url = data.get('url')

    if image_url:
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            folder_path = "photo_of_day"
            os.makedirs(folder_path, exist_ok=True)
            safe_title = title.replace(' ', '_').replace('/', '_')
            image_filename = os.path.join(folder_path, f"{date_input}_{safe_title}.jpg")
            with open(image_filename, 'wb') as f:
                f.write(image_response.content)
            with open(image_filename, 'rb') as f:
                await update.message.reply_photo(photo=f, caption=title)
        else:
            await update.message.reply_text("Ошибка при загрузке изображения.")
    else:
        await update.message.reply_text("Нет доступного изображения.")


# Основная функция для запуска бота
async def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", welcome))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Запустить бот
    await application.run_polling()

if __name__ == '__main__':
    import asyncio

    # Проверяем, запущен ли уже цикл событий
    try:
        # Проверка наличия активно работающего цикла
        if not asyncio.get_event_loop().is_running():
            asyncio.run(main())
    except Exception as e:
        print(f"Произошла ошибка: {e}")
