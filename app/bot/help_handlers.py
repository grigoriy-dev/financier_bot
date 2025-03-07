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
        
        # Отправляем текст с MarkdownV2 разметкой
        await message.answer(
            help_text,
            reply_markup=get_main_keyboard(),
            parse_mode="MarkdownV2"  # Включаем поддержку MarkdownV2
        )
    except FileNotFoundError:
        await message.answer("Файл с помощью не найден.", reply_markup=get_main_keyboard())