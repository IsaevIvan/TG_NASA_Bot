from aiogram import types, Dispatcher
from aiogram.utils.exceptions import TelegramAPIError
from services.nasa_api import get_apod
from config import PHOTO_OF_DAY_DIR
import os
import httpx


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

            # Скачивание изображения
            async with httpx.AsyncClient() as client:
                response = await client.get(photo_url)
                response.raise_for_status()

                # Сохранение во временный файл (или в оперативную память, если небольшое)
                photo_bytes = response.content

                await message.reply_photo(photo=photo_bytes, caption=photo_caption)  # Отправка как байты

        else:
            await message.reply("Сегодня не фото, а что-то другое.")  # Обработка случая, если это не картинка

    except TelegramAPIError as e:
        print(f"Ошибка Telegram API: {e}")
        await message.reply("Произошла ошибка при отправке фото.")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        await message.reply("Произошла неизвестная ошибка.")


def register_handlers_photo(dp: Dispatcher):
    dp.register_message_handler(send_apod, lambda message: message.text == "🌌 Получить фото")  # Кнопка главного меню

    # Обработчик команды с датой (YYYY-MM-DD)
    async def photo_with_date_handler(message: types.Message):
        from ..utils.date_utils import is_valid_date_format
        if is_valid_date_format(message.text):
            await send_apod(message, message.text)
        else:
            await message.reply("Неверный формат даты. Используйте YYYY-MM-DD.")

    dp.register_message_handler(photo_with_date_handler, content_types=types.ContentType.TEXT)