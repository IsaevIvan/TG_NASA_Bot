from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import calendar
import datetime


def create_calendar(year: int, month: int) -> InlineKeyboardMarkup:
    """Создает Inline-календарь."""
    markup = InlineKeyboardMarkup(row_width=7)  # Подстраиваем под дни недели

    # Шапка календаря (Месяц и навигация)
    markup.add(
        InlineKeyboardButton(text="<<", callback_data=f"calendar:prev-{year}-{month}"),
        InlineKeyboardButton(text=f"{calendar.month_name[month]} {year}", callback_data="calendar:ignore"),
        # Или пустая callback_data
        InlineKeyboardButton(text=">>", callback_data=f"calendar:next-{year}-{month}")
    )

    # Дни недели
    days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    markup.row(*[InlineKeyboardButton(text=day, callback_data="calendar:ignore") for day in days_of_week])

    # Заполнение дней
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        week_buttons = []
        for day in week:
            if day == 0:
                week_buttons.append(InlineKeyboardButton(text=" ", callback_data="calendar:ignore"))  # Пустая ячейка
            else:
                formatted_month = f"{month:02}"
                formatted_day = f"{day:02}"
                callback_data = f"calendar:day-{year}-{formatted_month}-{formatted_day}"
                week_buttons.append(InlineKeyboardButton(text=str(day), callback_data=callback_data))
        markup.row(*week_buttons)

    return markup