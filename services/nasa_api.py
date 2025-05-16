import httpx
from typing import Optional, Dict
from config import NASA_API_KEY
from utils.date_utils import is_valid_date_format


async def get_apod(date: Optional[str] = None) -> Optional[Dict]:
    """Получает Astronomy Picture of the Day (APOD) от NASA API."""

    if date and not is_valid_date_format(date):
        raise ValueError("Неверный формат даты. Используйте YYYY-MM-DD.")

    params = {  "date": date,
                "api_key": NASA_API_KEY,
            }

    try:
        async with httpx.AsyncClient() as client:
            url = "https://api.nasa.gov/planetary/apod"
            response = await client.get(url, params=params)
            response.raise_for_status()  # Проверка на ошибки HTTP

            print(f"URL запроса: {response.url}")  # Выводим URL из ответа

            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Ошибка HTTP: {e}")
        return None
    except httpx.RequestError as e:
        print(f"Ошибка подключения: {e}")
        return None


# import asyncio
#
# async def main():
#     apod_data = await get_apod('2025-05-15')
#     if apod_data:
#         print(apod_data)
#
# asyncio.run(main())