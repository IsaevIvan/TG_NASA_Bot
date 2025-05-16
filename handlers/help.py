from aiogram import types, Dispatcher
from aiogram.filters import Filter

async def help_handler(message: types.Message):
    """Обработчик команды 'Помощь'."""
    help_text = (
        "Этот бот предоставляет фотографии NASA APOD (Astronomy Picture of the Day).\n\n"
        "**Команды:**\n"
        "- /start: Запуск бота и отображение главного меню.\n"
        "- 🌌 Получить фото: Получить фото дня.\n"
        "- 📅 Выбор даты фото: Выбрать фото дня за определенную дату (YYYY-MM-DD).\n"
    )
    await message.reply(help_text, parse_mode="HTML")

# Фильтр для кнопки "❓ Помощь"
class HelpButtonFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.text == "❓ Помощь"

def register_handlers_help(dp: Dispatcher):
    """Регистрирует обработчики для раздела 'Помощь'."""
    dp.message.register(help_handler, HelpButtonFilter())