import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
NASA_API_KEY = os.getenv('NASA_API_KEY')

if not BOT_TOKEN or not NASA_API_KEY:
    raise ValueError("Необходимо задать TELEGRAM_BOT_TOKEN и NASA_API_KEY в переменных окружения")

PHOTO_OF_DAY_DIR = "photo_of_day" # Директория для сохранения фото