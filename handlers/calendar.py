import datetime
from aiogram import types
from aiogram.dispatcher import dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import TelegramAPIError
from ..keyboards.calendar import create_calendar
from .photo import send_apod

# Создаем CallbackData для календаря
calendar_callback = CallbackData("calendar", "action", "year", "month", "day")  # calendar:<action>:<year>:<month>:<day>


async def show_calendar(message: types.Message):
    """Отправляет Inline-календарь."""
    now = datetime.datetime.now()
    markup = create_calendar(now.year, now.month)
    await message.reply("Выберите дату:", reply_markup=markup)


def register_handlers_calendar(dp: Dispatcher):
    dp.register_message_handler(show_calendar,
                                lambda message: message.text == "📅 Выбор даты фото")  # Кнопка главного меню
    dp.register_callback_query_handler(calendar_callback_handler, calendar_callback.filter())  # Обработчик callback'ов


async def calendar_callback_handler(query: types.CallbackQuery, callback_data: dict):
    """Обработчик callback-запросов для Inline-календаря."""
    action = callback_data["action"]
    year = int(callback_data["year"])
    month = int(callback_data["month"])

    if action == "ignore":
        await query.answer(cache_time=60)  # Просто игнорируем нажатие
    elif action == "day":
        day = int(callback_data["day"])
        selected_date = f"{year}-{month:02}-{day:02}"  # Форматируем дату
        await query.message.reply_text(f"Вы выбрали дату: {selected_date}")
        await send_apod(query.message, selected_date)  # Отправляем APOD для выбранной даты
    elif action in ["next", "prev"]:
        if action == "next":
            month += 1
            if month > 12:
                month = 1
                year += 1
        else:  # action == "prev"
            month -= 1
            if month < 1:
                month = 12
                year -= 1
        try:
            markup = create_calendar(year, month)
            await query.message.edit_reply_markup(reply_markup=markup)  # Обновляем клавиатуру
        except TelegramAPIError:
            await query.answer("Кажется, я не могу отредактировать это сообщение.", show_alert=True)