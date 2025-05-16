import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers.start import register_handlers_start
from handlers.photo import register_handlers_photo
from handlers.calendar import register_handlers_calendar

logging.basicConfig(level=logging.DEBUG)  # Установите уровень отладки

async def set_default_commands(bot: Bot):
    """Установка команд бота в меню."""
    commands = [
        BotCommand(command="start", description="Запустить бота"),
    ]
    await bot.set_my_commands(commands)

async def main():
    """Запуск бота."""
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)

    # Регистрация обработчиков
    register_handlers_start(dp)
    register_handlers_photo(dp)
    register_handlers_calendar(dp)

    # Установка команд бота
    await set_default_commands(bot)

    # Запуск polling
    try:
        await dp.start_polling(bot)  #  Передаём bot в start_polling
    except Exception as e:
        logging.exception("Произошла ошибка при запуске бота: %s", e)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")