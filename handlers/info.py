from aiogram import types, Dispatcher
from aiogram.filters import Filter

async def info_handler(message: types.Message):
    """Обработчик команды 'Информация'."""
    info_text = (
        "**Информация о боте NASA ФОТО ДНЯ:**\n\n"
        "Этот бот использует API NASA APOD для получения фотографий космоса.\n"
        "Разработчик: @Isaev_Ivan\n"
        "Лицензия: MIT License\n"
        "Пишите в ТГ Ваши пожелания и замечания о работе бота.\n"
    )
    await message.reply(info_text, parse_mode="HTML", disable_web_page_preview=True)

# Фильтр для кнопки "ℹ️ Информация"
class InfoButtonFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.text == "ℹ️ Информация"

def register_handlers_info(dp: Dispatcher):
    """Регистрирует обработчики для раздела 'Информация'."""
    dp.message.register(info_handler, InfoButtonFilter())