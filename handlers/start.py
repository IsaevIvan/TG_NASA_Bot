from aiogram import types, Dispatcher
from keyboards.main_menu import create_main_menu_keyboard

async def start_handler(message: types.Message):
    await message.reply("Привет! Нажмите 'Начать', чтобы продолжить.", reply_markup=create_main_menu_keyboard())

def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])