from aiogram import types, Dispatcher
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Filter
from services.nasa_api import get_apod
from config import PHOTO_OF_DAY_DIR
from utils.date_utils import is_valid_date_format
import os
import httpx  # Для скачивания изображений


async def send_apod(message: types.Message, date: str = None):
    """Получает и отправляет APOD."""
    try:
        await message.reply("Загрузка...")
        data = await get_apod(date)
        if not data:
            await message.reply("Не удалось получить фото.")
            return

        if data.get("media_type") == "image":
            photo_url = data["url"]
            photo_caption = data.get("title", "Фото дня")

            #  Отправляем фото по URL
            try:
                await message.reply_photo(photo=photo_url, caption=photo_caption)

            except httpx.HTTPStatusError as e:
                print(f"Ошибка при скачивании изображения: {e}")
                await message.reply("Не удалось скачать изображение.")

        else:
            await message.reply("Сегодня не фото, а что-то другое.")  # Обработка случая, если это не картинка

    except TelegramAPIError as e:
        print(f"Ошибка Telegram API: {e}")
        await message.reply("Произошла ошибка при отправке фото.")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        await message.reply("Произошла неизвестная ошибка.")


# Определяем фильтр для кнопки "🌌 Получить фото"
class GetPhotoButtonFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.text == "🌌 Получить фото"


# Определяем фильтр для проверки формата даты
class DateFormatFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return is_valid_date_format(message.text)


def register_handlers_photo(dp: Dispatcher):
    dp.message.register(send_apod, GetPhotoButtonFilter())  # Кнопка главного меню

    # Обработчик команды с датой (YYYY-MM-DD)
    dp.message.register(send_apod, DateFormatFilter())