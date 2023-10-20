import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# FSM for get prognos
class GetWeatherState(StatesGroup):
    wait_city = State()


# command start
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    kb = [
            [types.KeyboardButton(text="Узнать погоду")],
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer('Здравствуйте! Чтобы узнать погоду нажмите кнопку\n"Узнать погоду"', reply_markup=keyboard)

# get city function
async def get_city(message: types.Message, state: FSMContext):
    kb = [
            [types.KeyboardButton(text="Узнать погоду")],
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Введите название города", reply_markup=keyboard)
    await state.set_state(GetWeatherState.wait_city.state)

# get weather function
async def get_weather(message: types.Message, state: FSMContext):
    city = message.text.lower()
    # make request to geocoder api and get lat and long
    api_key_geocoder = os.getenv("API_GEOCODER")
    url_yndex_geocoder = f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key_geocoder}&geocode={city}&format=json'
    try:
        response_api_geocoder = requests.get(url_yndex_geocoder).json()
        city_position = response_api_geocoder['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    except:
        await message.answer("Произошла ошибка, пожалуйста, введите город еще раз:")
        return
    city_lat = float(city_position.split(' ')[1])
    city_lon = float(city_position.split(' ')[0])

    # make request to weather api and get prognos
    api_key_weather = os.getenv("API_WEATHER")
    url_yndex_weather = f'https://api.weather.yandex.ru/v2/informers/?lat={city_lat}&lon={city_lon}&lang=ru_RU'
    try:
        response_api_weather = requests.get(url_yndex_weather, headers={'X-Yandex-API-Key': api_key_weather}).json()
        response_api_weather['now']
    except:
        await message.answer("Произошла ошибка, на данный момент мы не можем узнать погоду")
        await state.clear()
        return
    prognos_date = response_api_weather['forecast']['date']
    prognos_sunrise = response_api_weather['forecast']['sunrise']
    prognos_sunset = response_api_weather['forecast']['sunset']
    prognos_parts = response_api_weather['forecast']['parts']
    prognose_text = f"Прогноз на {prognos_date}\nВосход солнца {prognos_sunrise}\nЗакат {prognos_sunset}\n\n"
    for part in prognos_parts:
        part_name = part['part_name']
        temp_avg = part['temp_avg']
        wind_speed = part['wind_speed']
        pressure_mm = part['pressure_mm']
        prognose_text += f"{part_name}:\nСредняя температура: {temp_avg} по Цельсию\n"
        prognose_text += f"Скорость ветра: {wind_speed}м/с\n"
        prognose_text += f"Атмосферное давление: {pressure_mm}мм.рт.ст\n"


    await state.clear()
    kb = [
            [types.KeyboardButton(text="Узнать погоду")],
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(prognose_text,reply_markup=keyboard)


async def main():

    bot = Bot(token=os.getenv("API_TOKEN_BOT"))

    storage = MemoryStorage()

    dp = Dispatcher(storage=MemoryStorage())

    logging.basicConfig(level=logging.INFO)

    dp.message.register(cmd_start, Command("start"))
    dp.message.register(get_city, F.text.lower() == "узнать погоду")
    dp.message.register(get_weather, GetWeatherState.wait_city)
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())


    
    
