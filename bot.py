import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage  #  Импортируем из aiogram.fsm.storage.memory
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties # Новый импорт
from config import BOT_TOKEN
from handlers.start import register_handlers_start
from handlers.photo import register_handlers_photo
from handlers.calendar import register_handlers_calendar

logging.basicConfig(level=logging.INFO)

async def set_default_commands(bot: Bot):
    """Установка команд бота в меню."""
    commands = [
        BotCommand(command="start", description="Запустить бота"), #  Используем именованные аргументы
    ]
    await bot.set_my_commands(commands)

async def main():
    """Запуск бота."""
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # Используем DefaultBotProperties
    storage = MemoryStorage()  #  Используем MemoryStorage
    dp = Dispatcher(bot=bot, storage=storage) # storage - keyword-only аргумент

    # Регистрация обработчиков
    register_handlers_start(dp)
    register_handlers_photo(dp)
    register_handlers_calendar(dp)

    # Установка команд бота
    await set_default_commands(bot)

    # Запуск polling
    try:
        await dp.start_polling() # skip_updates больше не нужен. Он выполняется автоматически.
    except Exception as e:
        logging.exception("Произошла ошибка при запуске бота: %s", e)
    finally:
        await bot.session.close()  # Закрываем сессию бота.