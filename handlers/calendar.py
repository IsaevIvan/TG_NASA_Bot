from aiogram import types, Dispatcher
from aiogram.filters import Command, Filter  # Для фильтров
from aiogram.filters.callback_data import CallbackData
from aiogram.exceptions import TelegramAPIError
from keyboards.calendar import create_calendar
from .photo import send_apod
import datetime

# Создаем CallbackData для календаря
class CalendarCallback(CallbackData, prefix="calendar"):
    action: str
    year: int
    month: int
    day: int

async def show_calendar(message: types.Message):
    """Отправляет Inline-календарь."""
    now = datetime.datetime.now()
    markup = create_calendar(now.year, now.month)
    await message.reply("Выберите дату:", reply_markup=markup)

# Определяем фильтр для кнопки "📅 Выбор даты фото"
class CalendarButtonFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.text == "📅 Выбор даты фото"

def register_handlers_calendar(dp: Dispatcher):
     dp.message.register(show_calendar, CalendarButtonFilter()) # Кнопка главного меню
     dp.callback_query.register(calendar_callback_handler, CalendarCallback.filter()) # Обработчик callback'ов


async def calendar_callback_handler(query: types.CallbackQuery, callback_data: CalendarCallback): # Изменили тип callback_data
    """Обработчик callback-запросов для Inline-календаря."""
    action = callback_data.action
    year = callback_data.year
    month = callback_data.month

    if action == "ignore":
        await query.answer(cache_time=60)  # Просто игнорируем нажатие
    elif action == "day":
        day = callback_data.day
        selected_date = f"{year}-{month:02}-{day:02}" # Форматируем дату
        await query.message.edit_text(f"Вы выбрали дату: {selected_date}") # Изменено на edit_text
        await send_apod(query.message, selected_date)  # Отправляем APOD для выбранной даты
    elif action in ["next", "prev"]:
        if action == "next":
            month += 1
            if month > 12:
                month = 1
                year += 1
        else: # action == "prev"
            month -= 1
            if month < 1:
                month = 12
                year -= 1
        try:
             markup = create_calendar(year, month)
             await query.message.edit_reply_markup(reply_markup=markup) # Обновляем клавиатуру
        except TelegramAPIError:
            await query.answer("Кажется, я не могу отредактировать это сообщение.", show_alert=True)