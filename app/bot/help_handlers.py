from aiogram import Router, types
from aiogram.filters import Command
import os
from app.bot.keyboards import get_main_keyboard

router = Router()

@router.message(lambda message: message.text == "Помощь")
async def help_command(message: types.Message):
    try:
        with open("app/bot/help.txt", "r", encoding="utf-8") as file:
            help_text = file.read()
        await message.answer(help_text, reply_markup=get_main_keyboard())
    except FileNotFoundError:
        await message.answer("Файл HELP не найден.", reply_markup=get_main_keyboard())