from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import httpx
import asyncio

from app.settings.env import bot_token

# Токен вашего бота
BOT_TOKEN = bot_token
# URL вашего API
API_URL = "http://127.0.0.1:8000" 

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Состояния для FSM (Finite State Machine)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    category = State()
    amount = State()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Приветственное сообщение
    await message.answer("Привет! Я бот для учёта финансов. Используй кнопки ниже для добавления доходов или расходов.")
