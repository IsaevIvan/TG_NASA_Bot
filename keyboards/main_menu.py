from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Создает клавиатуру главного меню."""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    get_photo_button = KeyboardButton("🌌 Получить фото")
    select_date_button = KeyboardButton("📅 Выбор даты фото")
    help_button = KeyboardButton("❓ Помощь")
    info_button = KeyboardButton("ℹ️ Информация")
    keyboard.add(get_photo_button, select_date_button)
    keyboard.add(help_button, info_button)
    return keyboard