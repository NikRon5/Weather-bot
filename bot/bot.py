import asyncio
from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

import config
from geocodeapi import GeocodeApi
from weatherapi import WeatherApi
import texts

bot = Bot(token=config.bot_token)
weather_api = WeatherApi(config.weather_api_key)
geocode_api = GeocodeApi(config.geocoding_api_key)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(texts.start)

@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        cities = geocode_api.get_cities(message.text)
    except Exception:
        await message.answer("Ошибка получения координат!")
    else:
        if len(cities) != 0:
            city = cities[0]
            try:
                weather = weather_api.get_current_weather(city["coords"])
            except Exception:
                await message.answer("Ошибка получения погоды!")
            else:
                text = texts.current_weather([
                    city["address"],
                    weather["current_weather"]["time"],
                    weather["current_weather"]["temperature"],
                    weather["current_weather"]["apparent_temperature"],
                    weather["current_weather"]["precipitation_probability"],
                    weather["current_weather"]["pressure"],
                    weather["current_weather"]["cloud_cover"],
                    weather["hourly_weather"]
                ])
                await message.answer(text)
        else:
            await message.answer("Город не найден")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())