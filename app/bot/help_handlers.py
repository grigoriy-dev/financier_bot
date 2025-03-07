"""
Модуль для предоставления помощи в Telegram-боте.

Этот модуль содержит хэндлеры для отправки пользователю справочной информации:
- Чтение текста помощи из файла `help.txt`.
- Отправка текста с поддержкой MarkdownV2.

Основные компоненты:
- `help_command`: Обработчик команды "Помощь". Отправляет пользователю содержимое файла `help.txt`.

Логирование:
- Логируются запросы пользователей на помощь.
- Логируются ошибки (например, если файл `help.txt` не найден).
- Логи включают идентификатор пользователя и детали выполняемых операций.
"""

from aiogram import Router, types
from aiogram.filters import Command
import os
from loguru import logger
from app.bot.keyboards import get_main_keyboard

# Создаем роутер для хэндлеров
router = Router()

@router.message(lambda message: message.text == "Помощь")
async def help_command(message: types.Message):
    """
    Обработчик команды "Помощь". Отправляет пользователю содержимое файла help.txt
    Если файл не найден, отправляет сообщение об ошибке.
    """
    logger.info(f"Пользователь {message.from_user.id} запросил помощь.")

    try:
        # Открываем файл с помощью
        with open("app/bot/help.txt", "r", encoding="utf-8") as file:
            help_text = file.read()
        
        logger.info(f"Файл help.txt прочитан для пользователя {message.from_user.id}.")

        # Отправляем текст с MarkdownV2 разметкой
        await message.answer(
            help_text,
            reply_markup=get_main_keyboard(),
            parse_mode="MarkdownV2"  # Включаем поддержку MarkdownV2
        )

    except FileNotFoundError:
        logger.error(f"Файл help.txt не найден для пользователя {message.from_user.id}.")
        await message.answer("Файл с помощью не найден.", reply_markup=get_main_keyboard())
    except Exception as e:
        logger.error(f"Ошибка при обработке команды 'Помощь' для пользователя {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка при обработке запроса.", reply_markup=get_main_keyboard())
