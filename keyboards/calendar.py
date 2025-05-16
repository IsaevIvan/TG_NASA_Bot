import calendar
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
import datetime

# Создаем CallbackData для навигации по календарю
class CalendarCallback(CallbackData, prefix="calendar"):
    action: str
    year: int
    month: int
    day: int

def create_calendar(year: int, month: int) -> InlineKeyboardMarkup:
    """Создает Inline-календарь для указанного года и месяца."""
    markup = InlineKeyboardMarkup(inline_keyboard=[])  # Инициализируем пустой клавиатурой

    # Добавляем кнопки с названиями месяцев
    month_names = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]
    markup.inline_keyboard.append([InlineKeyboardButton(text=month_names[month - 1] + " " + str(year), callback_data="ignore")])

    # Создаем заголовки дней недели
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    markup.inline_keyboard.append([InlineKeyboardButton(text=day, callback_data="ignore") for day in days])

    # Создаем календарь для месяца
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
            else:
                callback_data = CalendarCallback(action="day", year=year, month=month, day=day).pack()
                row.append(InlineKeyboardButton(text=str(day), callback_data=callback_data))
        markup.inline_keyboard.append(row)

    # Добавляем кнопки навигации
    nav_buttons = [
        InlineKeyboardButton(text="<", callback_data=CalendarCallback(action="prev", year=year, month=month, day=1).pack()),
        InlineKeyboardButton(text=" ", callback_data="ignore"),  # Пустая кнопка для центровки
        InlineKeyboardButton(text=">", callback_data=CalendarCallback(action="next", year=year, month=month, day=1).pack()),
    ]
    markup.inline_keyboard.append(nav_buttons)

    return markup