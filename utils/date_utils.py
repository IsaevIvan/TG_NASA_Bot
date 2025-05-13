import datetime

def is_valid_date_format(date_string: str) -> bool:
    """Проверяет, является ли строка датой в формате YYYY-MM-DD."""
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# # Запрашиваем ввод у пользователя
# date_string = input("Введите дату в формате YYYY-MM-DD: ")
#
# # Проверяем введенную дату
# if is_valid_date_format(date_string):
#     print("Дата введена корректно.")
# else:
#     print("Некорректный формат даты. Пожалуйста, введите дату в формате YYYY-MM-DD.")