import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .config import BOT_TOKEN
from .keyboards.main_menu import create_main_menu_keyboard
from .handlers.start import register_handlers_start
from .handlers.photo import register_handlers_photo
from .handlers.calendar import register_handlers_calendar

logging.basicConfig(level=logging.INFO)

async def set_default_commands(dp):
    """Установка команд бота в меню."""
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
    ])

async def main():
    """Запуск бота."""
    bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    storage = MemoryStorage()  # Или используйте RedisStorage для хранения в Redis
    dp = Dispatcher(bot, storage=storage)

    # Регистрация обработчиков
    register_handlers_start(dp)
    register_handlers_photo(dp)
    register_handlers_calendar(dp)

    # Установка команд бота
    await set_default_commands(dp)

    # Запуск polling
    try:
        await dp.start_polling()
    finally:
        await bot.close() # Корректное закрытие сессии

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")