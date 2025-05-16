import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers.help import register_handlers_help
from handlers.info import register_handlers_info
from handlers.start import register_handlers_start
from handlers.photo import register_handlers_photo
from handlers.calendar import register_handlers_calendar

logging.basicConfig(level=logging.INFO)

async def set_default_commands(bot: Bot):
   commands = [
        BotCommand(command="start", description="Запустить бота"),
    ]
   await bot.set_my_commands(commands)

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)

    # Регистрация обработчиков
    register_handlers_start(dp)
    register_handlers_photo(dp)
    register_handlers_calendar(dp)
    register_handlers_info(dp)
    register_handlers_help(dp)

    await set_default_commands(bot)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.exception("Произошла ошибка при запуске бота: %s", e)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")