from aiogram import types, Dispatcher
from aiogram.filters import Command
from keyboards.main_menu import create_main_menu_keyboard

async def start_handler(message: types.Message):
    """Обработчик команды /start."""
    await message.reply("Привет! Нажмите 'Начать', чтобы продолжить.", reply_markup=create_main_menu_keyboard())

def register_handlers_start(dp: Dispatcher):
    dp.message.register(start_handler, Command("start")) # Используем register