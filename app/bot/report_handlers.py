"""
Модуль для формирования отчетов в Telegram-боте.

Этот модуль содержит хэндлеры для создания и отправки финансовых отчетов:
- Выбор периода для отчета (месяц, 3 месяца, полгода, год, всё время).
- Формирование отчета в формате XLSX.
- Отправка отчета пользователю.

Основные компоненты:
- `report_command`: Обработчик команды "Отчёт". Предлагает выбрать период для отчета.
- `process_report_period`: Обработчик выбора периода. Формирует и отправляет отчет.

Логирование:
- Логируются действия пользователей (выбор периода, формирование отчета).
- Логи включают идентификатор пользователя и детали выполняемых операций.
- Ошибки при формировании отчета также логируются.

"""

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from loguru import logger

from app.api.routers import get_report
from app.bot.keyboards import get_main_keyboard, get_report_period_keyboard

# Создаем роутер для хэндлеров
router = Router()

@router.message(lambda message: message.text == "Отчёт")
async def report_command(message: types.Message, state: FSMContext):
    """
    Обработчик команды "Отчёт". Предлагает пользователю выбрать период для формирования отчёта.
    """
    logger.info(f"Пользователь {message.from_user.id} запросил отчёт.")
    await message.answer("Выберите период для отчёта:", reply_markup=get_report_period_keyboard())

@router.message(lambda message: message.text in ["Месяц", "3 месяца", "Полгода", "Год", "Всё время", "Назад"])
async def process_report_period(message: types.Message, state: FSMContext):
    """
    Обработчик выбора периода для отчёта. Формирует отчёт за выбранный период или возвращает в главное меню.
    """
    logger.info(f"Пользователь {message.from_user.id} выбрал период: {message.text}")

    if message.text == "Назад":
        logger.info(f"Пользователь {message.from_user.id} нажал 'Назад'. Возврат в главное меню.")
        await state.clear()
        await message.answer(
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
        return

    periods = {
        "Месяц": "month", 
        "3 месяца": "3months", 
        "Полгода": "6months",
        "Год": "year", 
        "Всё время": "all"
    }
    period = periods.get(message.text)

    # Запрашиваем отчёт
    logger.info(f"Формирование отчёта за период: {period} для пользователя {message.from_user.id}")
    response = await get_report(period=period, format="xlsx")

    if response.get("msg") in ["Данные выгружены в XLSX"]:
        logger.info(f"Отчёт успешно сформирован для пользователя {message.from_user.id}.")
        file = FSInputFile("data/output.xlsx")
        await message.answer_document(file, caption="Ваш отчёт готов!")
    else:
        logger.error(f"Ошибка при формировании отчёта для пользователя {message.from_user.id}. Ответ API: {response}")
        await message.answer("Произошла ошибка при формировании отчёта.")

    # Возврат в главное меню
    logger.info(f"Возврат в главное меню для пользователя {message.from_user.id}.")
    await message.answer(
        "Выберите действие:",
        reply_markup=get_main_keyboard()
    )
