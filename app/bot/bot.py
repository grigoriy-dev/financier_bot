from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
# Импортируем хэндлеры
from app.bot.handlers import router as main_router
from app.bot.help_handlers import router as help_router
from app.bot.report_handlers import router as report_router

# Загружаем переменные из .env файла
load_dotenv("app/settings/.env")

# Получаем токен бота из переменной окружения
BOT_TOKEN = os.getenv('bot_token')
if not BOT_TOKEN:
    raise ValueError("Токен бота не найден в .env файле!")
else:
    print(f"Токен бота: {BOT_TOKEN}")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрируем хэндлеры
dp.include_router(main_router)
dp.include_router(help_router)
dp.include_router(report_router)
