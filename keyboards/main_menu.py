from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Создает клавиатуру главного меню."""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text="🌌 Получить фото"),
            KeyboardButton(text="📅 Выбор даты фото")
        ],
        [
            KeyboardButton(text="❓ Помощь"),
            KeyboardButton(text="ℹ️ Информация")
        ]
    ], row_width=2) # row_width больше не нужен, т.к. структура задана в keyboard
    return keyboard