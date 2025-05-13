import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
NASA_API_KEY = os.getenv('NASA_API_KEY')