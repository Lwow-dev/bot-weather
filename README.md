# bot-weather
Test task project
Тестовый проект бота в Телеграм, который отдает прогноз погоды по указанному городу. Работает с помощью библиотек aiogram и yandex api.

Для запуска приложения после клонирования репозитория необходимо:

1. Создать виртуальное окружение (для linux Ubuntu: python3 -m venv env)
2. Активировать виртуальное окружение (для linux Ubuntu: source env/bin/activate)
3. Установить зависимости из файла requirements.txt (pip install -r requirements.txt)
4. В папке проекта (рядом с manage.py) создать файл .env, содержащий следующие переменные: 
  API_TOKEN_BOT=YUOR_TELEGRAM_TOKEN_BOT 
  API_GEOCODER=YUOR_YANDEX_GEOCODER_API_KEY 
  API_WEATHER=YUOR_YANDEX_WEATHER_API_KEY
5. Запустить бота командой python main.py
   
